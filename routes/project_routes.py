"""
Project Routes for Project Aura Phase 2.
Handles project management endpoints.
"""

import os
import logging
from flask import Blueprint, request, render_template, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from services.claude_service import ClaudeService
from services.project_detector import ProjectDetector
from services.database_service import DatabaseService
from demo_mode import is_demo_mode, get_demo_project, get_demo_analysis

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

project_bp = Blueprint('project', __name__, url_prefix='/api/project')

# Initialize services
api_key = os.environ.get('ANTHROPIC_API_KEY')
claude_service = ClaudeService(api_key) if api_key else None
db_service = DatabaseService()

# Check for demo mode
DEMO_MODE = is_demo_mode()


@project_bp.route('/analyze', methods=['POST'])
def analyze_documents():
    """
    Analyze uploaded documents with Claude AI to detect project type and extract information.

    Returns:
        JSON response with analysis results
    """
    try:
        # Demo mode - return mock data
        if DEMO_MODE:
            demo_data = get_demo_analysis()
            session['project_analysis'] = demo_data
            session.modified = True

            return jsonify({
                'success': True,
                'analysis': demo_data,
                'validation': {'completeness': 95, 'confidence': 92},
                'risks': demo_data.get('risks', [])[:5],
                'config': {
                    'staffing_template': ['Tech Lead', 'Developers', 'QA', 'DevOps'],
                    'phases': ['Requirements', 'Design', 'Development', 'Testing', 'Deployment']
                }
            }), 200

        # Check if Claude API is configured
        if not claude_service:
            return jsonify({
                'success': False,
                'error': 'Claude API not configured. Please set ANTHROPIC_API_KEY.'
            }), 500

        # Get processed documents from session
        documents = session.get('processed_documents', [])

        if not documents:
            return jsonify({
                'success': False,
                'error': 'No documents found. Please upload documents first.'
            }), 400

        # Analyze with Claude
        analysis_result = claude_service.analyze_project_documents(documents)
        
        if not analysis_result['success']:
            return jsonify(analysis_result), 500

        analysis = analysis_result['analysis']
        
        # Validate extracted information
        validation = ProjectDetector.validate_project_info(analysis)
        
        # Get project-specific configuration
        project_type = analysis.get('project_type', 'Unknown')
        config = ProjectDetector.get_project_config(project_type)
        risks = ProjectDetector.get_risk_assessment(
            project_type,
            team_size=1,  # Default, will be updated in clarification
            duration_weeks=12  # Default, will be updated in clarification
        )
        
        # Store analysis in session
        session['project_analysis'] = analysis
        session['validation'] = validation
        session.modified = True
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'validation': validation,
            'risks': risks[:5],  # Top 5 risks
            'config': {
                'staffing_template': config.get('staffing'),
                'phases': config.get('phases')
            }
        }), 200

    except Exception as e:
        error_msg = f"Error analyzing documents: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500


@project_bp.route('/clarify', methods=['GET', 'POST'])
def clarify_project():
    """
    GET: Display clarification form for project information
    POST: Process clarification form submission with user input for missing fields.

    Expected POST data:
        - start_date: Project start date
        - duration: Duration in weeks
        - team_size: Team size
        - delivery_model: Delivery model (Fixed/Time & Material/Hybrid)

    Returns:
        GET: HTML page with clarification form
        POST: JSON response with complete project information
    """
    # Handle GET request - show clarification form
    if request.method == 'GET':
        # Get analysis from session
        analysis = session.get('project_analysis', {})

        # If no analysis, redirect to home
        if not analysis or analysis == {}:
            logger.info("No analysis in session, redirecting to home")
            response = redirect('/')
            response.cache_control.no_cache = True
            response.cache_control.no_store = True
            return response

        return render_template('clarification_blend.html', analysis=analysis)

    # Handle POST request - process clarification form
    try:
        # Get user input
        user_input = {
            'start_date': request.json.get('start_date'),
            'duration': request.json.get('duration'),
            'team_size': request.json.get('team_size'),
            'delivery_model': request.json.get('delivery_model')
        }

        # Demo mode - return mock project
        if DEMO_MODE:
            demo_project = get_demo_project()
            demo_project.update({
                'start_date': user_input.get('start_date', demo_project['start_date']),
                'duration_weeks': int(user_input.get('duration', 26)),
                'team_size': int(user_input.get('team_size', 14)),
                'delivery_model': user_input.get('delivery_model', 'Fixed'),
            })

            project_id = db_service.create_project(demo_project)

            return jsonify({
                'success': True,
                'project_id': project_id,
                'project_name': demo_project['project_name'],
                'redirect': f'/api/project/{project_id}/summary'
            }), 200

        # Get analysis from session
        analysis = session.get('project_analysis', {})

        if not analysis:
            return jsonify({
                'success': False,
                'error': 'No analysis found. Please analyze documents first.'
            }), 400

        # Clarify with Claude
        clarification_result = claude_service.clarify_project_information(analysis, user_input)
        
        if not clarification_result['success']:
            return jsonify(clarification_result), 500

        project_info = clarification_result['project_info']
        
        # Get project type
        project_type = project_info.get('project_type', 'Unknown')
        
        # Estimate staffing
        team_size = int(user_input.get('team_size', 1))
        duration_weeks = int(user_input.get('duration', 12))
        
        staffing = ProjectDetector.estimate_staffing(project_type, team_size)
        risks = ProjectDetector.get_risk_assessment(project_type, team_size, duration_weeks)
        phases = ProjectDetector.get_project_phases(project_type)
        
        # Create project in database
        project_data = {
            'project_name': project_info.get('client_name', 'New Project'),
            'project_type': project_type,
            'client_name': project_info.get('client_name'),
            'scope': project_info.get('scope'),
            'start_date': user_input.get('start_date'),
            'duration_weeks': duration_weeks,
            'team_size': team_size,
            'delivery_model': user_input.get('delivery_model'),
            'analysis': project_info
        }
        
        project_id = db_service.create_project(project_data)
        
        if not project_id:
            return jsonify({
                'success': False,
                'error': 'Failed to create project in database'
            }), 500

        # Add documents to project
        documents = session.get('processed_documents', [])
        for doc in documents:
            db_service.add_document_to_project(project_id, doc)

        # Add deliverables
        deliverables = project_info.get('deliverables', [])
        if deliverables:
            db_service.add_deliverables(project_id, deliverables)

        # Add team members
        if staffing:
            db_service.add_team_members(project_id, staffing)

        # Add risks
        if risks:
            db_service.add_risks(project_id, risks)

        # Store in session
        session['project_id'] = project_id
        session['project_info'] = project_info
        session.modified = True

        return jsonify({
            'success': True,
            'project_id': project_id,
            'project_info': project_info,
            'staffing': staffing,
            'risks': risks[:10],
            'phases': phases,
            'message': f'Project "{project_data["project_name"]}" created successfully!'
        }), 200

    except Exception as e:
        error_msg = f"Error clarifying project: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500


@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """
    Get project details.
    
    Args:
        project_id: Project ID
    
    Returns:
        JSON response with project details
    """
    try:
        project_summary = db_service.get_project_summary(project_id)
        
        if not project_summary:
            return jsonify({
                'success': False,
                'error': 'Project not found'
            }), 404

        return jsonify({
            'success': True,
            'project': project_summary
        }), 200

    except Exception as e:
        error_msg = f"Error retrieving project: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500


@project_bp.route('/list', methods=['GET'])
def list_projects():
    """
    List all projects.
    
    Returns:
        JSON response with list of projects
    """
    try:
        projects = db_service.get_all_projects()
        
        return jsonify({
            'success': True,
            'projects': projects,
            'count': len(projects)
        }), 200

    except Exception as e:
        error_msg = f"Error listing projects: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500


@project_bp.route('/<int:project_id>/summary', methods=['GET'])
def get_project_summary_view(project_id):
    """
    Get project summary page.

    Args:
        project_id: Project ID

    Returns:
        Rendered HTML page with project summary
    """
    try:
        project_summary = db_service.get_project_summary(project_id)

        if not project_summary:
            return render_template('project_summary_blend.html', error='Project not found'), 404

        return render_template('project_summary_blend.html', project=project_summary, project_id=project_id), 200

    except Exception as e:
        error_msg = f"Error loading project summary: {str(e)}"
        logger.error(error_msg)
        return render_template('project_summary_blend.html', error=error_msg), 500
