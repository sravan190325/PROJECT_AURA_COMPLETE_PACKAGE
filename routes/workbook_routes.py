"""
Workbook Routes for Project Aura Phase 3.
Handles Excel workbook generation and download endpoints.
Uses PMO-grade workbook generator for professional consulting deliverables.
Supports backward compatibility with enhanced and standard generators.
"""

import os
import logging
from flask import Blueprint, request, render_template, jsonify, send_file, session
from services.pmo_workbook_generator import PMOWorkbookGenerator, PMOWorkbookFactory
from services.workbook_generator_enhanced import EnhancedWorkbookGenerator, WorkbookGeneratorFactory
from services.database_service import DatabaseService

logger = logging.getLogger(__name__)

workbook_bp = Blueprint('workbook', __name__, url_prefix='/api/workbook')

# Initialize database service
db_service = DatabaseService()


@workbook_bp.route('/generate/<int:project_id>', methods=['POST'])
def generate_workbook(project_id):
    """
    Generate Excel workbook for a project.
    
    Args:
        project_id: Project ID
    
    Returns:
        JSON response with download link
    """
    try:
        # Get project from database
        project = db_service.get_project(project_id)
        
        if not project:
            return jsonify({
                'success': False,
                'error': 'Project not found'
            }), 404

        # Get full project summary
        project_summary = db_service.get_project_summary(project_id)
        
        if not project_summary:
            return jsonify({
                'success': False,
                'error': 'Failed to retrieve project summary'
            }), 500

        # Prepare project info
        project_info = {
            'project_name': project.get('project_name', 'Project'),
            'project_type': project.get('project_type', 'Unknown'),
            'client_name': project.get('client_name', 'Client'),
            'scope': project.get('scope', ''),
            'start_date': project.get('start_date', ''),
            'duration_weeks': project.get('duration_weeks', 12),
            'team_size': project.get('team_size', 1),
            'delivery_model': project.get('delivery_model', 'Fixed'),
        }
        
        # Create output directory
        output_dir = 'workbooks'
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        filename = f"{project_info['client_name'].replace(' ', '_')}_{project_id}_ProjectPlan.xlsx"
        output_path = os.path.join(output_dir, filename)
        
        # Generate PMO-grade workbook with consolidated, executive-ready sheets
        # Uses PMOWorkbookGenerator by default for professional consulting deliverables
        # Set ?generator=enhanced for legacy enhanced workbook or ?generator=standard for original
        generator_type = request.args.get('generator', 'pmo').lower()

        if generator_type == 'enhanced':
            generator = WorkbookGeneratorFactory.create_enhanced_generator(project_info, project_summary)
        elif generator_type == 'standard':
            generator = WorkbookGeneratorFactory.create_standard_generator(project_info, project_summary)
        else:  # Default: PMO-grade
            generator = PMOWorkbookFactory.create_pmo_generator(project_info, project_summary)

        success = generator.generate(output_path)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Failed to generate workbook'
            }), 500

        logger.info(f"Workbook generated successfully: {output_path}")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'download_url': f'/api/workbook/download/{project_id}',
            'message': 'Workbook generated successfully!'
        }), 200

    except Exception as e:
        error_msg = f"Error generating workbook: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500


@workbook_bp.route('/download/<int:project_id>', methods=['GET'])
def download_workbook(project_id):
    """
    Download generated workbook.
    
    Args:
        project_id: Project ID
    
    Returns:
        File stream for download
    """
    try:
        # Get project from database
        project = db_service.get_project(project_id)
        
        if not project:
            return jsonify({
                'success': False,
                'error': 'Project not found'
            }), 404

        # Build filename
        client_name = project.get('client_name', 'Project').replace(' ', '_')
        filename = f"{client_name}_{project_id}_ProjectPlan.xlsx"
        filepath = os.path.join('workbooks', filename)
        
        # Check if file exists
        if not os.path.exists(filepath):
            # Try to regenerate
            logger.info(f"Workbook not found, regenerating: {filename}")
            
            project_summary = db_service.get_project_summary(project_id)
            project_info = {
                'project_name': project.get('project_name', 'Project'),
                'project_type': project.get('project_type', 'Unknown'),
                'client_name': project.get('client_name', 'Client'),
                'scope': project.get('scope', ''),
                'start_date': project.get('start_date', ''),
                'duration_weeks': project.get('duration_weeks', 12),
                'team_size': project.get('team_size', 1),
                'delivery_model': project.get('delivery_model', 'Fixed'),
            }
            
            os.makedirs('workbooks', exist_ok=True)
            # Regenerate using PMO generator (can be overridden with query param)
            generator_type = request.args.get('generator', 'pmo').lower()

            if generator_type == 'enhanced':
                generator = WorkbookGeneratorFactory.create_enhanced_generator(project_info, project_summary)
            elif generator_type == 'standard':
                generator = WorkbookGeneratorFactory.create_standard_generator(project_info, project_summary)
            else:
                generator = PMOWorkbookFactory.create_pmo_generator(project_info, project_summary)

            success = generator.generate(filepath)
            
            if not success:
                return jsonify({
                    'success': False,
                    'error': 'Failed to generate workbook'
                }), 500

        # Return file
        return send_file(
            filepath,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        error_msg = f"Error downloading workbook: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500


@workbook_bp.route('/preview/<int:project_id>', methods=['GET'])
def preview_workbook(project_id):
    """
    Get preview information about what will be in the workbook.
    
    Args:
        project_id: Project ID
    
    Returns:
        JSON with workbook preview
    """
    try:
        # Get project
        project = db_service.get_project(project_id)
        
        if not project:
            return jsonify({
                'success': False,
                'error': 'Project not found'
            }), 404

        # Get project summary
        project_summary = db_service.get_project_summary(project_id)
        
        # Preview sheets
        sheets = [
            '01_Project_Details',
            '02_Project_Charter',
            '03_Assumptions',
            '04_Staffing_Plan',
            '05_Project_Plan',
            '06_WBS',
            '07_Milestones',
            '08_Dependencies',
            '09_Risk_Register',
            '10_RACI_Matrix',
            '11_Leave_Planner',
            '12_Project_Tracker',
            '13_Holiday_Calendar',
            '14_Dashboard'
        ]
        
        return jsonify({
            'success': True,
            'project_name': project.get('project_name', ''),
            'client_name': project.get('client_name', ''),
            'project_type': project.get('project_type', ''),
            'sheets': sheets,
            'stats': {
                'total_sheets': len(sheets),
                'team_members': len(project_summary.get('team_members', [])),
                'risks': len(project_summary.get('risks', [])),
                'deliverables': len(project_summary.get('deliverables', []))
            }
        }), 200

    except Exception as e:
        error_msg = f"Error previewing workbook: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500
