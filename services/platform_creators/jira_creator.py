"""
Jira Platform Creator for Project Aura.
Handles Scrum project creation with epics, stories, and sprints.
"""

import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import base64

logger = logging.getLogger(__name__)


class JiraCreator:
    """Create Scrum projects in Jira Cloud"""

    def __init__(self, jira_url: str, api_token: str):
        """
        Initialize Jira creator
        jira_url: e.g., https://your-domain.atlassian.net
        api_token: API token from Jira
        """
        self.jira_url = jira_url.rstrip('/')
        self.api_token = api_token
        self.api_base = f"{self.jira_url}/rest/api/3"

        # Build auth header
        auth_str = f"api@atlassian.net:{api_token}"
        auth_bytes = base64.b64encode(auth_str.encode()).decode()
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_bytes}"
        }

    # ============================================================================
    # CONNECTION TESTING
    # ============================================================================

    def test_connection(self) -> Dict[str, Any]:
        """Test Jira API connection and retrieve account info"""
        try:
            # DEMO MODE: If token is "demo", return demo response
            if self.api_token == "demo" or self.api_token.lower() == "demo123":
                return {
                    'success': True,
                    'account_name': 'Demo Jira Cloud Account'
                }

            response = requests.get(
                f"{self.api_base}/myself",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'account_name': data.get('displayName', 'Jira Account')
                }
            else:
                return {
                    'success': False,
                    'error': f"Jira API error: {response.status_code} {response.text}"
                }

        except requests.exceptions.RequestException as e:
            logger.error(f"Jira connection error: {str(e)}")
            return {
                'success': False,
                'error': f"Connection failed: {str(e)}"
            }

    # ============================================================================
    # PROJECT CREATION
    # ============================================================================

    def create_scrum_project(
        self,
        project_data: Dict,
        deliverables: List[Dict],
        team_members: List[Dict],
        risks: List[Dict]
    ) -> Dict[str, Any]:
        """Create a complete Scrum project with epics, stories, and sprints"""
        try:
            # DEMO MODE: If token is "demo", return demo response
            if self.api_token == "demo" or self.api_token.lower() == "demo123":
                demo_key = f"DEMO{project_data.get('id', '1')}"
                logger.info(f"[DEMO MODE] Creating Jira Scrum project: {demo_key}")
                return {
                    'success': True,
                    'project_key': demo_key,
                    'project_url': f"https://demo.atlassian.net/browse/{demo_key}",
                    'mapping': self._create_demo_mapping(deliverables),
                    'demo_mode': True,
                    'message': 'Demo mode: Scrum board structure created successfully (not synced to actual Jira)'
                }

            # Step 1: Create Scrum project
            project_key = self._create_project(project_data)
            if not project_key:
                return {'success': False, 'error': 'Failed to create Jira project'}

            logger.info(f"Created Jira project: {project_key}")

            # Step 2: Create epics from phases
            epic_mapping = self._create_epics(project_key, deliverables)

            # Step 3: Create user stories from deliverables
            story_mapping = self._create_stories(project_key, deliverables, epic_mapping)

            # Step 4: Create tasks and subtasks
            task_mapping = self._create_tasks(project_key, deliverables, story_mapping)

            # Step 5: Create sprints
            sprint_ids = self._create_sprints(project_key, project_data)

            # Step 6: Create risk issues
            risk_mapping = self._create_risks(project_key, risks)

            # Get project URL
            project_url = f"{self.jira_url}/browse/{project_key}"

            mapping = {
                'epics': epic_mapping,
                'stories': story_mapping,
                'tasks': task_mapping,
                'sprints': sprint_ids,
                'risks': risk_mapping
            }

            return {
                'success': True,
                'project_key': project_key,
                'project_url': project_url,
                'mapping': mapping
            }

        except Exception as e:
            logger.error(f"Error creating Jira project: {str(e)}", exc_info=True)
            return {'success': False, 'error': str(e)}

    # ============================================================================
    # PROJECT STRUCTURE
    # ============================================================================

    def _create_project(self, project_data: Dict) -> Optional[str]:
        """Create Scrum project in Jira"""
        try:
            project_key = project_data.get('project_key', 'PROJ').upper()[:10]
            project_name = project_data.get('project_name', 'Project Aura')

            payload = {
                "key": project_key,
                "name": project_name,
                "projectTypeKey": "software",
                "projectTemplate": "com.pyxus.jira.plugin.cloud:scrum",
                "description": f"Project: {project_name} - Auto-generated by Project Aura"
            }

            response = requests.post(
                f"{self.api_base}/projects",
                json=payload,
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 201:
                return response.json().get('key', project_key)
            else:
                logger.error(f"Failed to create project: {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error creating project: {str(e)}")
            return None

    def _create_epics(self, project_key: str, deliverables: List[Dict]) -> Dict[str, str]:
        """Create epics from phases/phases"""
        try:
            epic_mapping = {}
            phases = set()

            # Collect unique phases
            for deliverable in deliverables:
                phase = deliverable.get('phase', 'General')
                phases.add(phase)

            # Create epic for each phase
            for phase in phases:
                payload = {
                    "fields": {
                        "project": {"key": project_key},
                        "summary": f"Phase: {phase}",
                        "description": f"Epic for {phase} phase",
                        "issuetype": {"name": "Epic"},
                        "customfield_10000": phase  # Epic name field
                    }
                }

                response = requests.post(
                    f"{self.api_base}/issues",
                    json=payload,
                    headers=self.headers,
                    timeout=30
                )

                if response.status_code == 201:
                    epic_key = response.json().get('key')
                    epic_mapping[phase] = epic_key
                    logger.info(f"Created epic {epic_key} for phase {phase}")
                else:
                    logger.warning(f"Failed to create epic for phase {phase}: {response.text}")

            return epic_mapping

        except Exception as e:
            logger.error(f"Error creating epics: {str(e)}")
            return {}

    def _create_stories(
        self,
        project_key: str,
        deliverables: List[Dict],
        epic_mapping: Dict[str, str]
    ) -> Dict[str, str]:
        """Create user stories from deliverables"""
        try:
            story_mapping = {}

            for deliverable in deliverables:
                phase = deliverable.get('phase', 'General')
                epic_key = epic_mapping.get(phase)

                payload = {
                    "fields": {
                        "project": {"key": project_key},
                        "summary": deliverable.get('name', 'Story'),
                        "description": deliverable.get('description', f"Deliverable: {deliverable.get('name')}"),
                        "issuetype": {"name": "Story"},
                        "customfield_10001": epic_key if epic_key else None  # Link to epic
                    }
                }

                response = requests.post(
                    f"{self.api_base}/issues",
                    json=payload,
                    headers=self.headers,
                    timeout=30
                )

                if response.status_code == 201:
                    story_key = response.json().get('key')
                    story_mapping[deliverable.get('id')] = story_key
                    logger.info(f"Created story {story_key} for deliverable {deliverable.get('name')}")
                else:
                    logger.warning(f"Failed to create story: {response.text}")

            return story_mapping

        except Exception as e:
            logger.error(f"Error creating stories: {str(e)}")
            return {}

    def _create_tasks(
        self,
        project_key: str,
        deliverables: List[Dict],
        story_mapping: Dict[str, str]
    ) -> Dict[str, str]:
        """Create tasks and subtasks from tasks in deliverables"""
        try:
            task_mapping = {}

            for deliverable in deliverables:
                parent_story_key = story_mapping.get(deliverable.get('id'))
                if not parent_story_key:
                    continue

                tasks = deliverable.get('tasks', [])

                for task in tasks:
                    payload = {
                        "fields": {
                            "project": {"key": project_key},
                            "parent": {"key": parent_story_key},
                            "summary": task.get('name', 'Task'),
                            "description": task.get('description', ''),
                            "issuetype": {"name": "Subtask"}
                        }
                    }

                    response = requests.post(
                        f"{self.api_base}/issues",
                        json=payload,
                        headers=self.headers,
                        timeout=30
                    )

                    if response.status_code == 201:
                        task_key = response.json().get('key')
                        task_mapping[task.get('id')] = task_key
                        logger.info(f"Created task {task_key} for {task.get('name')}")
                    else:
                        logger.warning(f"Failed to create task: {response.text}")

            return task_mapping

        except Exception as e:
            logger.error(f"Error creating tasks: {str(e)}")
            return {}

    def _create_sprints(self, project_key: str, project_data: Dict) -> List[str]:
        """Create sprints based on project duration"""
        try:
            sprint_ids = []
            duration_weeks = project_data.get('duration_weeks', 26)
            start_date = datetime.now()

            # Create sprints (2-week sprints)
            num_sprints = (duration_weeks + 1) // 2
            for i in range(min(num_sprints, 6)):  # Max 6 sprints
                sprint_start = start_date + timedelta(weeks=i*2)
                sprint_end = sprint_start + timedelta(weeks=2)

                payload = {
                    "name": f"Sprint {i+1}",
                    "startDate": sprint_start.strftime("%Y-%m-%d"),
                    "endDate": sprint_end.strftime("%Y-%m-%d"),
                    "state": "FUTURE"
                }

                # Get board ID first
                board_id = self._get_project_board(project_key)
                if not board_id:
                    continue

                response = requests.post(
                    f"{self.jira_url}/rest/agile/1.0/board/{board_id}/sprint",
                    json=payload,
                    headers=self.headers,
                    timeout=30
                )

                if response.status_code == 201:
                    sprint_id = response.json().get('id')
                    sprint_ids.append(sprint_id)
                    logger.info(f"Created sprint {i+1}")
                else:
                    logger.warning(f"Failed to create sprint: {response.text}")

            return sprint_ids

        except Exception as e:
            logger.error(f"Error creating sprints: {str(e)}")
            return []

    def _create_risks(self, project_key: str, risks: List[Dict]) -> Dict[str, str]:
        """Create risk issues"""
        try:
            risk_mapping = {}

            for risk in risks:
                payload = {
                    "fields": {
                        "project": {"key": project_key},
                        "summary": f"Risk: {risk.get('name', 'Risk')}",
                        "description": f"Probability: {risk.get('probability', 'Medium')}\nImpact: {risk.get('impact', 'Medium')}\nMitigation: {risk.get('mitigation', '')}",
                        "issuetype": {"name": "Task"},
                        "labels": ["RISK"]
                    }
                }

                response = requests.post(
                    f"{self.api_base}/issues",
                    json=payload,
                    headers=self.headers,
                    timeout=30
                )

                if response.status_code == 201:
                    risk_key = response.json().get('key')
                    risk_mapping[risk.get('id')] = risk_key
                    logger.info(f"Created risk issue {risk_key}")
                else:
                    logger.warning(f"Failed to create risk issue: {response.text}")

            return risk_mapping

        except Exception as e:
            logger.error(f"Error creating risks: {str(e)}")
            return {}

    # ============================================================================
    # HELPER METHODS
    # ============================================================================

    def _get_project_board(self, project_key: str) -> Optional[int]:
        """Get the first board ID for a project"""
        try:
            response = requests.get(
                f"{self.jira_url}/rest/agile/1.0/board",
                params={"projectKey": project_key},
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                boards = response.json().get('values', [])
                if boards:
                    return boards[0].get('id')

            return None

        except Exception as e:
            logger.error(f"Error getting board: {str(e)}")
            return None

    def _create_demo_mapping(self, deliverables: List[Dict]) -> Dict[str, Any]:
        """Create demo mapping structure"""
        mapping = {
            'epics': {},
            'stories': {},
            'tasks': {},
            'sprints': []
        }
        for deliverable in deliverables:
            mapping['stories'][f"del_{deliverable.get('id')}"] = f"DEMO-{deliverable.get('id')}"
            for task in deliverable.get('tasks', []):
                mapping['tasks'][f"tsk_{task.get('id')}"] = f"DEMO-{task.get('id')}-1"
        return mapping

    def delete_project(self, project_key: str) -> bool:
        """Delete a project (for rollback)"""
        try:
            response = requests.delete(
                f"{self.api_base}/projects/{project_key}",
                headers=self.headers,
                timeout=10
            )
            return response.status_code in [200, 204]
        except Exception as e:
            logger.error(f"Error deleting project: {str(e)}")
            return False
