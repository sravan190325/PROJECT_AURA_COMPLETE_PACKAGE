"""
Demo Mode Configuration for Project Aura
Provides mock data for demonstrations without API key
"""

# Mock project data for demo
DEMO_PROJECT_DATA = {
    'project_id': 1,
    'project_name': 'Mobile Banking Platform - Phase 1',
    'client_name': 'Acme Financial Services Inc.',
    'project_type': 'Mobile App Development',
    'scope': 'Development of iOS and Android mobile banking applications with backend APIs, security implementation, and comprehensive testing.',
    'start_date': 'August 1, 2026',
    'end_date': 'February 28, 2027',
    'duration_weeks': 26,
    'duration_text': '6 Months',
    'team_size': 14,
    'delivery_model': 'Fixed',
    'budget': 1200,
    'health_score': 85,
    'completion_percentage': 0,
    'deliverable_count': 24,

    'deliverables': [
        {'name': 'iOS Mobile Application', 'description': 'Native Swift application with account management, fund transfers, and bill payment'},
        {'name': 'Android Mobile Application', 'description': 'Native Kotlin application with feature parity to iOS app'},
        {'name': 'Backend APIs', 'description': 'Account, transaction, authentication, and payment processing APIs'},
        {'name': 'Security & Compliance', 'description': 'PCI DSS certification, HIPAA compliance, encryption protocols'},
        {'name': 'Quality Assurance', 'description': 'Functional, security, performance, and UAT testing'},
        {'name': 'Documentation', 'description': 'Technical architecture, API docs, user guides, deployment guide'},
    ],

    'team_members': [
        {'role': 'Tech Lead / Architect', 'count': 1, 'responsibility': 'Technical direction and architecture'},
        {'role': 'iOS Developers', 'count': 2, 'responsibility': 'iOS app development'},
        {'role': 'Android Developers', 'count': 2, 'responsibility': 'Android app development'},
        {'role': 'Backend Developers', 'count': 3, 'responsibility': 'API and backend services'},
        {'role': 'QA Engineers', 'count': 2, 'responsibility': 'Quality assurance and testing'},
        {'role': 'DevOps Engineer', 'count': 1, 'responsibility': 'Infrastructure and deployment'},
        {'role': 'UI/UX Designer', 'count': 1, 'responsibility': 'User interface and experience design'},
        {'role': 'Business Analyst', 'count': 1, 'responsibility': 'Requirements and stakeholder management'},
        {'role': 'Project Manager', 'count': 1, 'responsibility': 'Project coordination and reporting'},
    ],

    'risks': [
        {
            'risk_description': 'Integration with legacy banking systems',
            'probability': 'High',
            'impact': 'High',
            'mitigation': 'Early integration testing and dedicated integration team'
        },
        {
            'risk_description': 'Security compliance delays',
            'probability': 'Medium',
            'impact': 'High',
            'mitigation': 'Early security reviews and compliance audits'
        },
        {
            'risk_description': 'Resource availability conflicts',
            'probability': 'Medium',
            'impact': 'Medium',
            'mitigation': 'Documented backup resources and contingency staffing'
        },
        {
            'risk_description': 'Third-party API availability',
            'probability': 'Low',
            'impact': 'High',
            'mitigation': 'Mock API development in parallel with real integrations'
        },
        {
            'risk_description': 'Scope creep from client',
            'probability': 'High',
            'impact': 'Medium',
            'mitigation': 'Strict change control process and requirements sign-off'
        },
    ],

    'dependencies': [
        'Payment gateway API availability',
        'Legacy banking system access and documentation',
        'Mobile app store approval process',
        'Third-party security certification completion',
    ],

    'assumptions': [
        'Client will provide timely feedback and approvals',
        'Third-party APIs will be available as planned',
        'No major scope changes after requirements sign-off',
        'Team members available full-time throughout project',
        'Client infrastructure meets security requirements',
    ],
}

# Mock analysis results
DEMO_ANALYSIS_RESULTS = {
    'status': 'success',
    'project_id': 1,
    'project_name': 'Mobile Banking Platform - Phase 1',
    'client_name': 'Acme Financial Services Inc.',
    'project_type': 'Mobile App Development',
    'duration_weeks': 26,
    'team_size': 14,
    'scope': 'Development of iOS and Android mobile banking applications with backend APIs, comprehensive security implementation, and quality assurance testing.',
    'deliverables': DEMO_PROJECT_DATA['deliverables'],
    'team_members': DEMO_PROJECT_DATA['team_members'],
    'risks': DEMO_PROJECT_DATA['risks'],
    'dependencies': DEMO_PROJECT_DATA['dependencies'],
    'assumptions': DEMO_PROJECT_DATA['assumptions'],
}

def is_demo_mode():
    """Check if demo mode is enabled"""
    import os
    return os.getenv('DEMO_MODE', 'false').lower() == 'true'

def get_demo_project():
    """Return demo project data"""
    return DEMO_PROJECT_DATA

def get_demo_analysis():
    """Return demo analysis results"""
    return DEMO_ANALYSIS_RESULTS
