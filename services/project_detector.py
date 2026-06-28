"""
Project Detector Service for Project Aura.
Handles project type-specific logic and configurations.
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class ProjectDetector:
    """
    Detects project type and provides type-specific configurations.
    """

    # Project type configurations
    PROJECT_CONFIGS = {
        'Data Engineering': {
            'staffing': {
                'PM': 1,
                'Architect': 1,
                'Data Engineer': 3,
                'QA': 1
            },
            'risks': [
                'Source system delays',
                'Data quality issues',
                'Environment access issues',
                'Integration complexity',
                'Performance optimization challenges'
            ],
            'phases': [
                'Initiation',
                'Requirements',
                'Architecture Design',
                'Development',
                'Testing',
                'Deployment',
                'Closure'
            ]
        },
        'Data Analytics': {
            'staffing': {
                'PM': 1,
                'Analytics Architect': 1,
                'Data Analyst': 2,
                'BI Developer': 1,
                'QA': 1
            },
            'risks': [
                'Data availability issues',
                'Requirement clarity',
                'Tool compatibility',
                'Report accuracy validation',
                'User adoption'
            ],
            'phases': [
                'Initiation',
                'Requirements',
                'Data Modeling',
                'Dashboard Development',
                'Testing',
                'Deployment',
                'Closure'
            ]
        },
        'Reporting / BI': {
            'staffing': {
                'PM': 1,
                'BI Architect': 1,
                'BI Developer': 2,
                'Report Designer': 1,
                'QA': 1
            },
            'risks': [
                'Data source changes',
                'Report requirement changes',
                'Performance issues',
                'User training challenges',
                'Maintenance complexity'
            ],
            'phases': [
                'Initiation',
                'Requirements',
                'Data Design',
                'Report Development',
                'Testing',
                'Deployment',
                'Closure'
            ]
        },
        'GenAI': {
            'staffing': {
                'PM': 1,
                'AI Architect': 1,
                'AI Engineer': 2,
                'Data Engineer': 2,
                'QA': 1,
                'ML Ops': 1
            },
            'risks': [
                'Hallucination risk',
                'Prompt accuracy issues',
                'Model performance degradation',
                'Data privacy concerns',
                'Integration challenges',
                'Cost management'
            ],
            'phases': [
                'Initiation',
                'Requirements & POC',
                'Model Selection',
                'Fine-tuning',
                'Integration',
                'Testing',
                'Deployment',
                'Closure'
            ]
        },
        'Cloud Migration': {
            'staffing': {
                'PM': 1,
                'Cloud Architect': 2,
                'Cloud Engineer': 3,
                'Network Engineer': 1,
                'Security Engineer': 1,
                'QA': 1
            },
            'risks': [
                'Downtime during migration',
                'Data loss risk',
                'Compatibility issues',
                'Network performance',
                'Security vulnerabilities',
                'Cost overruns'
            ],
            'phases': [
                'Assessment',
                'Planning',
                'Design',
                'Pilot Migration',
                'Full Migration',
                'Validation',
                'Optimization',
                'Closure'
            ]
        },
        'Application Development': {
            'staffing': {
                'PM': 1,
                'Tech Lead': 1,
                'Developer': 3,
                'QA Engineer': 2,
                'DevOps': 1
            },
            'risks': [
                'Requirement scope creep',
                'Integration issues',
                'Performance problems',
                'Security vulnerabilities',
                'Dependency delays',
                'Testing coverage gaps'
            ],
            'phases': [
                'Initiation',
                'Requirements',
                'Design',
                'Development',
                'Testing',
                'Deployment',
                'Support',
                'Closure'
            ]
        },
        'Data Platform Modernization': {
            'staffing': {
                'PM': 1,
                'Platform Architect': 2,
                'Data Engineer': 3,
                'DevOps Engineer': 1,
                'QA': 1
            },
            'risks': [
                'Legacy system complexity',
                'Data migration issues',
                'Performance tuning',
                'Compatibility challenges',
                'Team skill gaps',
                'Downtime risks'
            ],
            'phases': [
                'Assessment',
                'Planning',
                'Architecture Design',
                'Migration Design',
                'Development',
                'Testing',
                'Migration',
                'Optimization',
                'Closure'
            ]
        }
    }

    @staticmethod
    def get_project_config(project_type: str) -> Dict[str, Any]:
        """
        Get configuration for a project type.
        
        Args:
            project_type: Type of project
        
        Returns:
            Configuration dictionary for the project type
        """
        config = ProjectDetector.PROJECT_CONFIGS.get(
            project_type,
            ProjectDetector.PROJECT_CONFIGS['Application Development']  # Default
        )
        return config

    @staticmethod
    def validate_project_info(project_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate project information completeness.
        
        Args:
            project_info: Project information dictionary
        
        Returns:
            Validation result with missing fields
        """
        mandatory_fields = {
            'project_type': 'Project Type',
            'start_date': 'Start Date',
            'duration_weeks': 'Duration (weeks)',
            'team_size': 'Team Size',
            'delivery_model': 'Delivery Model'
        }
        
        missing_fields = []
        for field, label in mandatory_fields.items():
            if field not in project_info or not project_info[field]:
                missing_fields.append(label)
        
        return {
            'is_complete': len(missing_fields) == 0,
            'missing_fields': missing_fields,
            'completion_percentage': int(((len(mandatory_fields) - len(missing_fields)) / len(mandatory_fields)) * 100)
        }

    @staticmethod
    def estimate_staffing(project_type: str, team_size: int) -> Dict[str, int]:
        """
        Estimate staffing breakdown for a project.
        
        Args:
            project_type: Type of project
            team_size: Total team size
        
        Returns:
            Dictionary with role distribution
        """
        config = ProjectDetector.get_project_config(project_type)
        default_staffing = config.get('staffing', {})
        
        # Calculate ratio
        default_total = sum(default_staffing.values())
        if default_total == 0:
            return {}
        
        ratio = team_size / default_total
        
        # Distribute team size based on default ratios
        estimated_staffing = {}
        remaining = team_size
        
        for i, (role, count) in enumerate(default_staffing.items()):
            if i == len(default_staffing) - 1:
                # Last role gets remaining
                estimated_staffing[role] = remaining
            else:
                role_count = max(1, int(count * ratio))
                estimated_staffing[role] = role_count
                remaining -= role_count
        
        return estimated_staffing

    @staticmethod
    def get_risk_assessment(project_type: str, team_size: int, duration_weeks: int) -> List[Dict[str, Any]]:
        """
        Generate risk assessment for a project.
        
        Args:
            project_type: Type of project
            team_size: Team size
            duration_weeks: Duration in weeks
        
        Returns:
            List of risks with severity
        """
        config = ProjectDetector.get_project_config(project_type)
        base_risks = config.get('risks', [])
        
        risks = []
        for risk in base_risks:
            # Calculate severity based on project parameters
            severity = ProjectDetector._calculate_risk_severity(
                risk, project_type, team_size, duration_weeks
            )
            
            risks.append({
                'description': risk,
                'severity': severity,
                'mitigation': ProjectDetector._get_risk_mitigation(risk)
            })
        
        # Sort by severity
        risks.sort(key=lambda x: x['severity'], reverse=True)
        
        return risks

    @staticmethod
    def _calculate_risk_severity(risk: str, project_type: str, team_size: int, duration_weeks: int) -> str:
        """
        Calculate risk severity based on project parameters.
        
        Args:
            risk: Risk description
            project_type: Project type
            team_size: Team size
            duration_weeks: Duration
        
        Returns:
            Severity level (High, Medium, Low)
        """
        # Simple heuristic
        if team_size < 3:
            if 'team' in risk.lower() or 'resource' in risk.lower():
                return 'High'
        
        if duration_weeks < 4:
            if 'time' in risk.lower() or 'schedule' in risk.lower():
                return 'High'
        
        if project_type == 'GenAI' and 'hallucination' in risk.lower():
            return 'High'
        
        if project_type == 'Cloud Migration' and 'downtime' in risk.lower():
            return 'High'
        
        return 'Medium'

    @staticmethod
    def _get_risk_mitigation(risk: str) -> str:
        """
        Get mitigation strategy for a risk.
        
        Args:
            risk: Risk description
        
        Returns:
            Mitigation strategy
        """
        mitigations = {
            'team': 'Conduct thorough resource planning and identify cross-training opportunities',
            'data': 'Implement data validation and quality checks from the start',
            'schedule': 'Build buffer time and implement agile monitoring',
            'requirement': 'Conduct detailed requirements workshops upfront',
            'integration': 'Plan integration testing early and use API contracts',
            'performance': 'Conduct load testing and optimize before production',
            'security': 'Perform security audits and implement best practices',
            'cost': 'Monitor costs continuously and implement cost controls'
        }
        
        for key, mitigation in mitigations.items():
            if key in risk.lower():
                return mitigation
        
        return 'Develop detailed mitigation plan during project planning phase'

    @staticmethod
    def get_project_phases(project_type: str) -> List[str]:
        """
        Get project phases for a project type.
        
        Args:
            project_type: Type of project
        
        Returns:
            List of project phases
        """
        config = ProjectDetector.get_project_config(project_type)
        return config.get('phases', [])
