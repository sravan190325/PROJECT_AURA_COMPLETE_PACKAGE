"""
Project Plan Engine for Project Aura.
Generates detailed project plans with phases, milestones, and dependencies.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class ProjectPlanEngine:
    """
    Engine for generating detailed project plans.
    """

    # Holidays in 2024-2025 (expand as needed)
    HOLIDAYS = [
        datetime(2025, 1, 1),   # New Year
        datetime(2025, 3, 17),  # St. Patrick's Day
        datetime(2025, 5, 26),  # Memorial Day
        datetime(2025, 7, 4),   # Independence Day
        datetime(2025, 9, 1),   # Labor Day
        datetime(2025, 11, 27), # Thanksgiving
        datetime(2025, 12, 25), # Christmas
    ]

    @staticmethod
    def is_business_day(date):
        """Check if date is a business day (not weekend or holiday)."""
        if date.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return False
        if date in ProjectPlanEngine.HOLIDAYS:
            return False
        return True

    @staticmethod
    def add_business_days(start_date, business_days):
        """Add business days to a date, excluding weekends and holidays."""
        current_date = start_date
        days_added = 0
        
        while days_added < business_days:
            current_date += timedelta(days=1)
            if ProjectPlanEngine.is_business_day(current_date):
                days_added += 1
        
        return current_date

    @staticmethod
    def generate_project_plan(project_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a detailed project plan.
        
        Args:
            project_info: Project information dictionary
        
        Returns:
            Dictionary with phases, milestones, and timeline
        """
        try:
            project_type = project_info.get('project_type', 'Application Development')
            start_date = datetime.strptime(project_info.get('start_date'), '%Y-%m-%d')
            duration_weeks = int(project_info.get('duration_weeks', 12))
            team_size = int(project_info.get('team_size', 1))
            
            # Define phases based on project type
            phases = ProjectPlanEngine._get_phases(project_type)
            
            # Allocate time to phases proportionally
            total_days = duration_weeks * 5  # Business days
            phase_allocations = ProjectPlanEngine._allocate_phase_time(phases, total_days)
            
            # Generate timeline
            timeline = ProjectPlanEngine._generate_timeline(
                start_date, phases, phase_allocations
            )
            
            # Generate milestones
            milestones = ProjectPlanEngine._generate_milestones(timeline, project_type)
            
            # Generate dependencies
            dependencies = ProjectPlanEngine._generate_dependencies(phases, milestones)
            
            return {
                'phases': timeline['phases'],
                'milestones': milestones,
                'dependencies': dependencies,
                'total_duration_weeks': duration_weeks,
                'critical_path': ProjectPlanEngine._identify_critical_path(dependencies),
                'success': True
            }
        
        except Exception as e:
            logger.error(f"Error generating project plan: {str(e)}")
            return {
                'phases': [],
                'milestones': [],
                'dependencies': [],
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def _get_phases(project_type: str) -> List[Dict[str, Any]]:
        """Get standard phases for project type."""
        phases_map = {
            'Data Engineering': [
                {'name': 'Initiation', 'effort_percent': 5},
                {'name': 'Requirements & Discovery', 'effort_percent': 15},
                {'name': 'Architecture Design', 'effort_percent': 15},
                {'name': 'Development', 'effort_percent': 40},
                {'name': 'Testing', 'effort_percent': 15},
                {'name': 'Deployment', 'effort_percent': 8},
                {'name': 'Closure', 'effort_percent': 2}
            ],
            'GenAI': [
                {'name': 'Initiation', 'effort_percent': 5},
                {'name': 'Requirements & POC', 'effort_percent': 20},
                {'name': 'Model Selection & Fine-tuning', 'effort_percent': 25},
                {'name': 'Integration Development', 'effort_percent': 30},
                {'name': 'Testing & Validation', 'effort_percent': 15},
                {'name': 'Deployment', 'effort_percent': 3},
                {'name': 'Closure', 'effort_percent': 2}
            ],
            'Cloud Migration': [
                {'name': 'Assessment', 'effort_percent': 10},
                {'name': 'Planning', 'effort_percent': 15},
                {'name': 'Design', 'effort_percent': 15},
                {'name': 'Pilot Migration', 'effort_percent': 15},
                {'name': 'Full Migration', 'effort_percent': 25},
                {'name': 'Validation & Testing', 'effort_percent': 12},
                {'name': 'Optimization', 'effort_percent': 5},
                {'name': 'Closure', 'effort_percent': 3}
            ],
            'Application Development': [
                {'name': 'Initiation', 'effort_percent': 5},
                {'name': 'Requirements', 'effort_percent': 10},
                {'name': 'Design', 'effort_percent': 15},
                {'name': 'Development', 'effort_percent': 40},
                {'name': 'Testing', 'effort_percent': 15},
                {'name': 'Deployment', 'effort_percent': 10},
                {'name': 'Support', 'effort_percent': 5}
            ]
        }
        
        return phases_map.get(project_type, phases_map['Application Development'])

    @staticmethod
    def _allocate_phase_time(phases: List[Dict], total_days: int) -> Dict[str, int]:
        """Allocate time to phases based on effort percentages."""
        allocation = {}
        for phase in phases:
            phase_name = phase['name']
            effort_percent = phase['effort_percent']
            days = max(1, int(total_days * effort_percent / 100))
            allocation[phase_name] = days
        return allocation

    @staticmethod
    def _generate_timeline(start_date: datetime, phases: List[Dict], 
                          allocations: Dict[str, int]) -> Dict[str, Any]:
        """Generate detailed timeline for all phases."""
        phases_timeline = []
        current_date = start_date
        
        for phase in phases:
            phase_name = phase['name']
            phase_days = allocations[phase_name]
            
            end_date = ProjectPlanEngine.add_business_days(current_date, phase_days)
            
            phases_timeline.append({
                'phase': phase_name,
                'start_date': current_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'duration_days': phase_days,
                'duration_weeks': max(1, phase_days // 5),
                'status': 'Planned'
            })
            
            current_date = end_date + timedelta(days=1)
        
        return {'phases': phases_timeline}

    @staticmethod
    def _generate_milestones(timeline: Dict, project_type: str) -> List[Dict[str, Any]]:
        """Generate key milestones."""
        milestones = []
        
        for i, phase in enumerate(timeline['phases'], 1):
            # Add phase completion milestone
            milestones.append({
                'milestone': f"{phase['phase']} Complete",
                'date': phase['end_date'],
                'phase': phase['phase'],
                'status': 'Planned',
                'priority': 'High' if i < 3 else 'Medium'
            })
        
        # Add overall project milestones
        if timeline['phases']:
            first_phase = timeline['phases'][0]
            milestones.insert(0, {
                'milestone': 'Project Kickoff',
                'date': first_phase['start_date'],
                'phase': first_phase['phase'],
                'status': 'Planned',
                'priority': 'Critical'
            })
            
            last_phase = timeline['phases'][-1]
            milestones.append({
                'milestone': 'Project Closure',
                'date': last_phase['end_date'],
                'phase': last_phase['phase'],
                'status': 'Planned',
                'priority': 'Critical'
            })
        
        return milestones

    @staticmethod
    def _generate_dependencies(phases: List[Dict], milestones: List[Dict]) -> List[Dict[str, Any]]:
        """Generate task dependencies."""
        dependencies = []
        
        # Create sequential dependencies between phases
        for i in range(len(phases) - 1):
            dependencies.append({
                'task': phases[i + 1]['phase'],
                'depends_on': phases[i]['phase'],
                'dependency_type': 'Finish to Start',
                'lead_lag': 0
            })
        
        # Add some cross-phase dependencies
        dependencies.extend([
            {
                'task': 'Testing',
                'depends_on': 'Development',
                'dependency_type': 'Finish to Start',
                'lead_lag': 0
            },
            {
                'task': 'Deployment',
                'depends_on': 'Testing',
                'dependency_type': 'Finish to Start',
                'lead_lag': 0
            }
        ])
        
        return dependencies

    @staticmethod
    def _identify_critical_path(dependencies: List[Dict]) -> List[str]:
        """Identify the critical path through the project."""
        # Simplified critical path (longest sequence of dependent tasks)
        critical_path = []
        for dep in dependencies:
            if dep['dependency_type'] == 'Finish to Start':
                if not critical_path:
                    critical_path.append(dep['depends_on'])
                critical_path.append(dep['task'])
        
        return critical_path

    @staticmethod
    def generate_gantt_data(phases: List[Dict]) -> List[Dict[str, Any]]:
        """
        Generate data for Gantt chart visualization.
        
        Args:
            phases: List of phase dictionaries
        
        Returns:
            List of Gantt chart data
        """
        gantt_data = []
        
        for phase in phases:
            start = datetime.strptime(phase['start_date'], '%Y-%m-%d')
            end = datetime.strptime(phase['end_date'], '%Y-%m-%d')
            
            gantt_data.append({
                'id': phase['phase'].replace(' ', '_'),
                'name': phase['phase'],
                'start': start.strftime('%Y-%m-%d'),
                'end': end.strftime('%Y-%m-%d'),
                'duration': (end - start).days,
                'progress': 0,
                'status': phase['status']
            })
        
        return gantt_data
