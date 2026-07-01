"""
Platform Delivery Routes for Project Aura.
Handles multi-platform project plan creation (Excel, SmartSheet, Jira).
"""

import os
import logging
import json
from datetime import datetime
from flask import Blueprint, request, render_template, jsonify, session, redirect
from dotenv import load_dotenv

from services.platform_creators.smartsheet_creator import SmartSheetCreator
from services.platform_creators.jira_creator import JiraCreator
from services.platform_creators.excel_creator import ExcelCreator
from services.database_service import DatabaseService

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

platform_bp = Blueprint('platform', __name__, url_prefix='/api/platform')
project_bp = Blueprint('project_delivery', __name__, url_prefix='/api/project')
delivery_bp = Blueprint('delivery', __name__, url_prefix='/platform-delivery')

# Initialize services
db_service = DatabaseService()


# ============================================================================
# MAIN DELIVERY ROUTES (Non-API)
# ============================================================================

@delivery_bp.route('', methods=['GET'])
def platform_delivery_home():
    """Show platform delivery home page with project selection"""
    return render_template('platform_delivery_home.html')


@delivery_bp.route('/demo', methods=['GET'])
def platform_delivery_demo():
    """Show platform delivery demo with sample project (project_id=1)"""
    try:
        project_data = _get_sample_project_data(1)

        return render_template('platform_delivery_selection.html',
                             project_id=1,
                             project_name=project_data['project'].get('project_name', 'Project'),
                             duration_weeks=project_data['project'].get('duration_weeks', 26),
                             team_size=project_data['project'].get('team_size', 12),
                             client_name=project_data['project'].get('client_name', 'Client'))
    except Exception as e:
        logger.error(f"Error loading demo: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _get_sample_project_data(project_id):
    """Helper function to return sample project data for testing"""
    return {
        'project': {
            'id': project_id,
            'project_name': 'Test Project Aura',
            'project_key': 'TEST',
            'client_name': 'Acme Corporation',
            'duration_weeks': 12,
            'team_size': 8
        },
        'deliverables': [
            {
                'id': 'del_1',
                'name': 'Project Discovery & Planning',
                'phase': 'Phase 1: Initiation',
                'description': 'Initial project planning and stakeholder alignment',
                'tasks': [
                    {
                        'id': 'tsk_1',
                        'name': 'Kickoff Meeting',
                        'description': 'Project kickoff with all stakeholders',
                        'start_date': '2026-07-01',
                        'end_date': '2026-07-03',
                        'duration_days': 2,
                        'priority': 'High'
                    },
                    {
                        'id': 'tsk_2',
                        'name': 'Requirements Gathering',
                        'description': 'Document all project requirements',
                        'start_date': '2026-07-04',
                        'end_date': '2026-07-10',
                        'duration_days': 6,
                        'priority': 'High'
                    }
                ]
            },
            {
                'id': 'del_2',
                'name': 'Solution Design',
                'phase': 'Phase 2: Design',
                'description': 'Design the complete solution',
                'tasks': [
                    {
                        'id': 'tsk_3',
                        'name': 'Architecture Design',
                        'description': 'Design system architecture',
                        'start_date': '2026-07-11',
                        'end_date': '2026-07-17',
                        'duration_days': 6,
                        'priority': 'High'
                    }
                ]
            }
        ],
        'team_members': [
            {'id': 'tm_1', 'name': 'John Doe', 'email': 'john@example.com', 'role': 'Project Manager'},
            {'id': 'tm_2', 'name': 'Jane Smith', 'email': 'jane@example.com', 'role': 'Technical Lead'},
        ],
        'risks': [
            {'id': 'risk_1', 'name': 'Resource Availability', 'probability': 'Medium', 'impact': 'High', 'mitigation': 'Allocate backup resources'}
        ]
    }


# ============================================================================
# PLATFORM SELECTION & DISPLAY ROUTES
# ============================================================================

@platform_bp.route('/selection/<int:project_id>', methods=['GET'])
def show_platform_selection(project_id):
    """Display platform selection page"""
    try:
        # Always use sample data for demo (can be overridden with database data)
        project_data = _get_sample_project_data(project_id)

        project = project_data['project']

        return render_template('platform_delivery_selection.html',
                             project_id=project_id,
                             project_name=project.get('project_name', 'Project'),
                             duration_weeks=project.get('duration_weeks', 26),
                             team_size=project.get('team_size', 12),
                             client_name=project.get('client_name', 'Client'))

    except Exception as e:
        logger.error(f"Error loading platform selection: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# ============================================================================
# CREDENTIAL TESTING
# ============================================================================

@platform_bp.route('/test-connection', methods=['POST'])
def test_platform_connection():
    """Test connection to selected platform"""
    try:
        data = request.get_json()
        platform = data.get('platform')
        credentials = data.get('credentials', {})

        if platform == 'smartsheet':
            creator = SmartSheetCreator(credentials.get('token'))
            result = creator.test_connection()

            if result['success']:
                return jsonify({
                    'success': True,
                    'account_name': result.get('account_name', 'SmartSheet Account')
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Connection failed')
                })

        elif platform == 'jira':
            creator = JiraCreator(
                credentials.get('url'),
                credentials.get('token')
            )
            result = creator.test_connection()

            if result['success']:
                return jsonify({
                    'success': True,
                    'account_name': result.get('account_name', 'Jira Account')
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Connection failed')
                })

        return jsonify({'success': False, 'error': 'Unknown platform'}), 400

    except Exception as e:
        logger.error(f"Error testing connection: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# PROJECT CREATION IN SELECTED PLATFORM
# ============================================================================

@project_bp.route('/create-platform', methods=['POST'])
def create_project_in_platform():
    """Create project plan in selected platform"""
    try:
        data = request.get_json()
        project_id = data.get('project_id')
        platform = data.get('platform')
        credentials = data.get('credentials', {})

        # Get complete project data from database, or use sample data
        project_summary = db_service.get_project_summary(project_id)

        # Use sample data for testing if database is empty
        if not project_summary or not project_summary.get('project'):
            project_summary = _get_sample_project_data(project_id)

        if not project_summary or not project_summary.get('project'):
            return jsonify({'error': 'Project not found'}), 404

        project_data = project_summary['project']
        deliverables = project_summary.get('deliverables', [])
        team_members = project_summary.get('team_members', [])
        risks = project_summary.get('risks', [])

        result = None

        # ====== EXCEL CREATION ======
        if platform == 'excel':
            logger.info(f"Creating Excel workbook for project {project_id}")
            creator = ExcelCreator(project_data)
            result = creator.create(deliverables, team_members, risks)

            if result['success']:
                return jsonify({
                    'success': True,
                    'platform': 'excel',
                    'project_id': project_id,
                    'file_path': result.get('file_path'),
                    'redirect_url': f'/api/project/{project_id}/summary'
                })

        # ====== SMARTSHEET CREATION ======
        elif platform == 'smartsheet':
            logger.info(f"Creating SmartSheet project for project {project_id}")
            creator = SmartSheetCreator(credentials.get('token'))
            result = creator.create_project(
                project_data,
                deliverables,
                team_members,
                risks
            )

            if result['success']:
                # Store SmartSheet mapping in database
                _store_platform_mapping(
                    project_id,
                    'smartsheet',
                    result.get('sheet_id'),
                    result.get('mapping', {})
                )

                return jsonify({
                    'success': True,
                    'platform': 'smartsheet',
                    'project_id': project_id,
                    'sheet_id': result.get('sheet_id'),
                    'sheet_url': result.get('sheet_url'),
                    'redirect_url': f'/api/project/{project_id}/summary'
                })

        # ====== JIRA CREATION ======
        elif platform == 'jira':
            logger.info(f"Creating Jira Scrum board for project {project_id}")
            creator = JiraCreator(
                credentials.get('url'),
                credentials.get('token')
            )
            result = creator.create_scrum_project(
                project_data,
                deliverables,
                team_members,
                risks
            )

            if result['success']:
                # Store Jira mapping in database
                _store_platform_mapping(
                    project_id,
                    'jira',
                    result.get('project_key'),
                    result.get('mapping', {})
                )

                return jsonify({
                    'success': True,
                    'platform': 'jira',
                    'project_id': project_id,
                    'project_key': result.get('project_key'),
                    'project_url': result.get('project_url'),
                    'redirect_url': f'/api/project/{project_id}/summary'
                })

        else:
            return jsonify({'error': 'Unknown platform'}), 400

        # If we get here, creation failed
        if result and not result.get('success'):
            return jsonify({
                'success': False,
                'error': result.get('error', 'Platform creation failed')
            }), 500

        return jsonify({'success': False, 'error': 'Creation failed'}), 500

    except Exception as e:
        logger.error(f"Error creating project in platform: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _store_platform_mapping(project_id, platform, platform_id, mapping):
    """Store platform mapping in database for future reference"""
    try:
        # TODO: Implement database storage for platform mappings
        # This would store the SmartSheet sheet ID or Jira project key
        # for reference when retrieving or updating the project later
        logger.info(f"Storing {platform} mapping for project {project_id}: {platform_id}")
    except Exception as e:
        logger.error(f"Error storing platform mapping: {str(e)}")
