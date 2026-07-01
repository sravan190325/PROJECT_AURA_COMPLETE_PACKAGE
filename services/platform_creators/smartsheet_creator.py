"""
SmartSheet Platform Creator for Project Aura.
Handles project plan creation in SmartSheet.
"""

import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class SmartSheetCreator:
    """Create project plans in SmartSheet"""

    API_URL = "https://api.smartsheet.com/2.0"
    HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = self.HEADERS.copy()
        self.headers["Authorization"] = f"Bearer {api_token}"

    # ============================================================================
    # CONNECTION TESTING
    # ============================================================================

    def test_connection(self) -> Dict[str, Any]:
        """Test SmartSheet API connection and retrieve account info"""
        try:
            # DEMO MODE: If token is "demo", return demo response
            if self.api_token == "demo" or self.api_token.lower() == "demo123":
                return {
                    'success': True,
                    'account_name': 'Demo SmartSheet Account'
                }

            response = requests.get(
                f"{self.API_URL}/user/profile",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'account_name': data.get('result', {}).get('name', 'SmartSheet Account')
                }
            else:
                return {
                    'success': False,
                    'error': f"SmartSheet API error: {response.status_code} {response.text}"
                }

        except requests.exceptions.RequestException as e:
            logger.error(f"SmartSheet connection error: {str(e)}")
            return {
                'success': False,
                'error': f"Connection failed: {str(e)}"
            }

    # ============================================================================
    # PROJECT CREATION
    # ============================================================================

    def create_project(
        self,
        project_data: Dict,
        deliverables: List[Dict],
        team_members: List[Dict],
        risks: List[Dict]
    ) -> Dict[str, Any]:
        """Create a complete project plan in SmartSheet"""
        try:
            # DEMO MODE: If token is "demo", return demo response
            if self.api_token == "demo" or self.api_token.lower() == "demo123":
                demo_sheet_id = f"demo_{project_data.get('id', '1')}_smartsheet"
                logger.info(f"[DEMO MODE] Creating SmartSheet project: {demo_sheet_id}")
                return {
                    'success': True,
                    'sheet_id': demo_sheet_id,
                    'sheet_url': f"https://app.smartsheet.com/sheets/demo_{project_data.get('id', '1')}",
                    'mapping': self._create_demo_mapping(deliverables),
                    'demo_mode': True,
                    'message': 'Demo mode: Project structure created successfully (not synced to actual SmartSheet)'
                }

            # Step 1: Create the sheet with columns
            sheet_id = self._create_sheet(project_data)
            if not sheet_id:
                return {'success': False, 'error': 'Failed to create sheet'}

            # Step 2: Add project metadata rows
            self._add_metadata_rows(sheet_id, project_data)

            # Step 3: Add deliverable hierarchy
            mapping = self._add_deliverables(sheet_id, deliverables)

            # Step 4: Add team and resource info
            self._add_team_info(sheet_id, team_members)

            # Step 5: Add risks
            self._add_risks(sheet_id, risks)

            # Step 6: Enable Gantt view
            self._enable_gantt_view(sheet_id)

            # Get sheet URL
            sheet_url = self._get_sheet_url(sheet_id)

            return {
                'success': True,
                'sheet_id': sheet_id,
                'sheet_url': sheet_url,
                'mapping': mapping
            }

        except Exception as e:
            logger.error(f"Error creating SmartSheet project: {str(e)}")
            return {'success': False, 'error': str(e)}

    # ============================================================================
    # SHEET STRUCTURE
    # ============================================================================

    def _create_sheet(self, project_data: Dict) -> Optional[str]:
        """Create SmartSheet with column structure"""
        try:
            # Define columns
            columns = [
                {"title": "Task ID", "type": "TEXT_NUMBER"},
                {"title": "Task Name", "type": "TEXT_NUMBER", "primary": True},
                {"title": "Phase", "type": "PICKLIST"},
                {"title": "Owner", "type": "CONTACT_LIST"},
                {"title": "Start Date", "type": "DATE"},
                {"title": "End Date", "type": "DATE"},
                {"title": "Duration (Days)", "type": "TEXT_NUMBER"},
                {"title": "% Complete", "type": "PERCENT"},
                {"title": "Dependencies", "type": "TEXT_NUMBER"},
                {"title": "Status", "type": "PICKLIST"},
                {"title": "Priority", "type": "PICKLIST"},
                {"title": "Resource", "type": "TEXT_NUMBER"},
                {"title": "Effort (hrs)", "type": "TEXT_NUMBER"},
                {"title": "Notes", "type": "TEXT_NUMBER"}
            ]

            payload = {
                "name": project_data.get('project_name', 'Project Plan'),
                "columns": columns
            }

            response = requests.post(
                f"{self.API_URL}/sheets",
                json=payload,
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 200:
                sheet_id = response.json().get('result', {}).get('id')
                logger.info(f"Created SmartSheet: {sheet_id}")
                return sheet_id
            else:
                logger.error(f"Failed to create sheet: {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error creating sheet: {str(e)}")
            return None

    def _add_metadata_rows(self, sheet_id: str, project_data: Dict) -> bool:
        """Add project metadata to the top of the sheet"""
        try:
            rows = [
                {
                    "cells": [
                        {"columnId": self._get_column_id(sheet_id, "Task Name"), "value": "PROJECT SUMMARY"},
                    ]
                },
                {
                    "cells": [
                        {"columnId": self._get_column_id(sheet_id, "Task Name"), "value": f"Client: {project_data.get('client_name', 'N/A')}"},
                    ]
                },
                {
                    "cells": [
                        {"columnId": self._get_column_id(sheet_id, "Task Name"), "value": f"Duration: {project_data.get('duration_weeks', 26)} weeks"},
                    ]
                },
                {
                    "cells": [
                        {"columnId": self._get_column_id(sheet_id, "Task Name"), "value": f"Team Size: {project_data.get('team_size', 12)} people"},
                    ]
                }
            ]

            response = requests.post(
                f"{self.API_URL}/sheets/{sheet_id}/rows",
                json={"rows": rows},
                headers=self.headers,
                timeout=30
            )

            return response.status_code == 200

        except Exception as e:
            logger.error(f"Error adding metadata rows: {str(e)}")
            return False

    def _add_deliverables(
        self,
        sheet_id: str,
        deliverables: List[Dict]
    ) -> Dict[str, Any]:
        """Add deliverables with task hierarchy"""
        try:
            mapping = {}
            rows = []
            row_number = 5  # Start after metadata

            for deliverable in deliverables:
                # Parent deliverable row
                deliverable_row = {
                    "cells": [
                        {"columnId": self._get_column_id(sheet_id, "Task ID"), "value": f"DEL-{deliverable.get('id', '')}"},
                        {"columnId": self._get_column_id(sheet_id, "Task Name"), "value": deliverable.get('name', 'Deliverable')},
                        {"columnId": self._get_column_id(sheet_id, "Phase"), "value": deliverable.get('phase', '')},
                        {"columnId": self._get_column_id(sheet_id, "Status"), "value": "Not Started"},
                    ]
                }
                rows.append(deliverable_row)

                # Store mapping
                mapping[f"del_{deliverable.get('id')}"] = row_number

                # Add child tasks
                tasks = deliverable.get('tasks', [])
                for task in tasks:
                    start_date = task.get('start_date', '')
                    end_date = task.get('end_date', '')
                    duration = task.get('duration_days', 5)

                    task_row = {
                        "cells": [
                            {"columnId": self._get_column_id(sheet_id, "Task ID"), "value": f"TSK-{task.get('id', '')}"},
                            {"columnId": self._get_column_id(sheet_id, "Task Name"), "value": task.get('name', 'Task')},
                            {"columnId": self._get_column_id(sheet_id, "Phase"), "value": deliverable.get('phase', '')},
                            {"columnId": self._get_column_id(sheet_id, "Start Date"), "value": start_date},
                            {"columnId": self._get_column_id(sheet_id, "End Date"), "value": end_date},
                            {"columnId": self._get_column_id(sheet_id, "Duration (Days)"), "value": duration},
                            {"columnId": self._get_column_id(sheet_id, "Status"), "value": "Not Started"},
                            {"columnId": self._get_column_id(sheet_id, "Priority"), "value": task.get('priority', 'Medium')},
                        ]
                    }
                    rows.append(task_row)
                    row_number += 1

                row_number += 1

            # Add all rows
            if rows:
                response = requests.post(
                    f"{self.API_URL}/sheets/{sheet_id}/rows",
                    json={"rows": rows},
                    headers=self.headers,
                    timeout=60
                )
                if response.status_code != 200:
                    logger.warning(f"Failed to add deliverable rows: {response.text}")

            return mapping

        except Exception as e:
            logger.error(f"Error adding deliverables: {str(e)}")
            return {}

    def _add_team_info(self, sheet_id: str, team_members: List[Dict]) -> bool:
        """Add team member information"""
        try:
            if not team_members:
                return True

            rows = [
                {
                    "cells": [
                        {"columnId": self._get_column_id(sheet_id, "Task Name"), "value": "TEAM MEMBERS"},
                    ]
                }
            ]

            for member in team_members:
                team_row = {
                    "cells": [
                        {"columnId": self._get_column_id(sheet_id, "Task Name"), "value": member.get('name', 'Team Member')},
                        {"columnId": self._get_column_id(sheet_id, "Owner"), "value": member.get('email', '')},
                        {"columnId": self._get_column_id(sheet_id, "Phase"), "value": member.get('role', '')},
                    ]
                }
                rows.append(team_row)

            response = requests.post(
                f"{self.API_URL}/sheets/{sheet_id}/rows",
                json={"rows": rows},
                headers=self.headers,
                timeout=30
            )

            return response.status_code == 200

        except Exception as e:
            logger.error(f"Error adding team info: {str(e)}")
            return False

    def _add_risks(self, sheet_id: str, risks: List[Dict]) -> bool:
        """Add risk information"""
        try:
            if not risks:
                return True

            rows = [
                {
                    "cells": [
                        {"columnId": self._get_column_id(sheet_id, "Task Name"), "value": "RISKS"},
                    ]
                }
            ]

            for risk in risks:
                risk_row = {
                    "cells": [
                        {"columnId": self._get_column_id(sheet_id, "Task Name"), "value": risk.get('name', 'Risk')},
                        {"columnId": self._get_column_id(sheet_id, "Phase"), "value": risk.get('probability', 'Medium')},
                        {"columnId": self._get_column_id(sheet_id, "Status"), "value": risk.get('impact', 'Medium')},
                        {"columnId": self._get_column_id(sheet_id, "Notes"), "value": risk.get('mitigation', '')},
                    ]
                }
                rows.append(risk_row)

            response = requests.post(
                f"{self.API_URL}/sheets/{sheet_id}/rows",
                json={"rows": rows},
                headers=self.headers,
                timeout=30
            )

            return response.status_code == 200

        except Exception as e:
            logger.error(f"Error adding risks: {str(e)}")
            return False

    # ============================================================================
    # GANTT VIEW
    # ============================================================================

    def _enable_gantt_view(self, sheet_id: str) -> bool:
        """Enable Gantt view on the sheet"""
        try:
            gantt_config = {
                "name": "Gantt View",
                "viewType": "GANTT",
                "columns": [
                    {"index": 1, "hidden": False},
                    {"index": 4, "hidden": False},
                    {"index": 5, "hidden": False}
                ]
            }

            response = requests.post(
                f"{self.API_URL}/sheets/{sheet_id}/views",
                json=gantt_config,
                headers=self.headers,
                timeout=30
            )

            return response.status_code == 200

        except Exception as e:
            logger.warning(f"Could not enable Gantt view: {str(e)}")
            return False

    # ============================================================================
    # HELPER METHODS
    # ============================================================================

    def _get_column_id(self, sheet_id: str, column_title: str) -> str:
        """Get column ID by title (simplified - should cache in production)"""
        # In production, cache this to avoid repeated API calls
        try:
            response = requests.get(
                f"{self.API_URL}/sheets/{sheet_id}",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                columns = response.json().get('result', {}).get('columns', [])
                for col in columns:
                    if col.get('title') == column_title:
                        return str(col.get('id'))

            return ""
        except Exception as e:
            logger.error(f"Error getting column ID: {str(e)}")
            return ""

    def _get_sheet_url(self, sheet_id: str) -> str:
        """Generate SmartSheet URL"""
        return f"https://app.smartsheet.com/sheets/{sheet_id}"

    def _create_demo_mapping(self, deliverables: List[Dict]) -> Dict[str, Any]:
        """Create demo mapping structure"""
        mapping = {}
        for deliverable in deliverables:
            mapping[f"del_{deliverable.get('id')}"] = f"row_{deliverable.get('id')}"
            for task in deliverable.get('tasks', []):
                mapping[f"tsk_{task.get('id')}"] = f"row_{task.get('id')}"
        return mapping

    def delete_sheet(self, sheet_id: str) -> bool:
        """Delete a sheet (for rollback)"""
        try:
            response = requests.delete(
                f"{self.API_URL}/sheets/{sheet_id}",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error deleting sheet: {str(e)}")
            return False
