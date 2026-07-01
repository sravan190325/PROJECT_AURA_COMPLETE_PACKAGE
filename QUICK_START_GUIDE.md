# Platform Delivery Quick Start Guide

## 5-Minute Setup

### 1. Register Routes in Flask App

Open your main Flask app file (e.g., `app.py` or `__init__.py`):

```python
from routes.platform_delivery_routes import platform_bp, project_bp

# Register blueprints after creating Flask app
app = Flask(__name__)
app.register_blueprint(platform_bp)
app.register_blueprint(project_bp)

# ... rest of your app configuration
```

### 2. Implement Database Method

Add this method to your `DatabaseService` class:

```python
def get_project_summary(self, project_id: int) -> Optional[Dict]:
    """Get complete project data for platform creation"""
    # Example using your existing database models
    project = Project.query.get(project_id)
    if not project:
        return None
    
    return {
        'project': {
            'id': project.id,
            'project_name': project.name,
            'project_key': project.name[:10].upper(),
            'client_name': project.client,
            'duration_weeks': project.duration_weeks,
            'team_size': project.team_size,
            'start_date': project.start_date.isoformat(),
            'end_date': project.end_date.isoformat()
        },
        'deliverables': [
            {
                'id': d.id,
                'name': d.name,
                'phase': d.phase,
                'description': d.description,
                'tasks': [
                    {
                        'id': t.id,
                        'name': t.name,
                        'description': t.description,
                        'start_date': t.start_date.isoformat(),
                        'end_date': t.end_date.isoformat(),
                        'duration_days': (t.end_date - t.start_date).days,
                        'priority': t.priority
                    }
                    for t in d.tasks
                ]
            }
            for d in project.deliverables
        ],
        'team_members': [
            {
                'id': m.id,
                'name': m.name,
                'email': m.email,
                'role': m.role
            }
            for m in project.team_members
        ],
        'risks': [
            {
                'id': r.id,
                'name': r.name,
                'probability': r.probability,
                'impact': r.impact,
                'mitigation': r.mitigation
            }
            for r in project.risks
        ]
    }
```

### 3. Start the App

```bash
cd PROJECT_AURA_COMPLETE_PACKAGE
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### 4. Access Platform Selection Page

Open browser and navigate to:
```
http://localhost:5000/api/platform/selection/1
```

(Replace `1` with actual project ID)

### 5. Test with Excel (No Credentials Needed)

1. Click "Excel Workbook" option
2. Click "Create Project Plan"
3. Excel file should be generated

## Testing with Real Platforms (Optional)

### SmartSheet Setup

1. **Get API Token:**
   - Log in to SmartSheet
   - Go to Account → Personal Settings → API Access
   - Generate new token
   - Copy token

2. **In Browser:**
   - Navigate to platform selection page
   - Select "SmartSheet"
   - Paste token in "SmartSheet API Token" field
   - Click "Test Connection"
   - If successful, click "Create Project Plan"

### Jira Setup

1. **Get API Token:**
   - Log in to Jira Cloud
   - Click Settings (gear icon) → Personal Settings
   - Go to Security tab
   - Create API token
   - Copy token and note your email

2. **In Browser:**
   - Navigate to platform selection page
   - Select "Jira Scrum Board"
   - Enter Jira URL: `https://your-domain.atlassian.net`
   - Enter API Token
   - Click "Test Connection"
   - If successful, click "Create Project Plan"

## Project Structure

```
routes/platform_delivery_routes.py       ← Flask routes
services/platform_creators/
  ├── smartsheet_creator.py              ← SmartSheet API
  ├── jira_creator.py                    ← Jira API
  └── excel_creator.py                   ← Excel workbook
templates/
  └── platform_delivery_selection.html   ← Frontend UI
```

## API Endpoints

### Get Platform Selection Page
```bash
GET /api/platform/selection/1
# Returns: HTML page with project details
```

### Test Connection
```bash
curl -X POST http://localhost:5000/api/platform/test-connection \
  -H "Content-Type: application/json" \
  -d '{"platform":"smartsheet","credentials":{"token":"your-token"}}'

# Or for Jira:
curl -X POST http://localhost:5000/api/platform/test-connection \
  -H "Content-Type: application/json" \
  -d '{
    "platform":"jira",
    "credentials":{
      "url":"https://domain.atlassian.net",
      "token":"your-token"
    }
  }'
```

### Create Project
```bash
curl -X POST http://localhost:5000/api/project/create-platform \
  -H "Content-Type: application/json" \
  -d '{
    "project_id":1,
    "platform":"smartsheet",
    "credentials":{"token":"your-token"}
  }'
```

## Troubleshooting

### Page Not Found (404)
- ✓ Make sure blueprints are registered in `app.py`
- ✓ Check Flask app is running: `flask run`
- ✓ Verify project ID exists in database

### Connection Test Fails
- **SmartSheet:** Token may be invalid or expired
  - Generate new token from account settings
- **Jira:** Wrong email or token
  - Use email address associated with account
  - Regenerate token if expired

### Project Creation Fails
- Check Flask console for error logs
- Ensure database service returns proper data structure
- Verify API credentials are valid
- Check internet connectivity

## Next Steps

1. ✅ Integrate routes into Flask app
2. ✅ Implement `DatabaseService.get_project_summary()`
3. ✅ Test with sample project
4. ✅ (Optional) Get real API credentials
5. ✅ Test with SmartSheet/Jira platforms
6. 📖 Read full documentation:
   - `FLASK_APP_INTEGRATION.md` — Detailed integration guide
   - `PLATFORM_DELIVERY_TESTING_GUIDE.md` — Comprehensive testing
   - `PLATFORM_DELIVERY_IMPLEMENTATION_SUMMARY.md` — Architecture overview

## What Gets Created?

### SmartSheet
- New sheet with project name
- 14-column PMO structure
- Task hierarchy (phases → deliverables → tasks)
- Team member section
- Risk register
- Gantt view enabled

### Jira
- New Scrum project
- Epics (from phases)
- User stories (from deliverables)
- Subtasks (from tasks)
- 2-week sprints
- Risk issues with RISK label

### Excel
- Multi-sheet workbook (format depends on ExcelCreator implementation)
- Standard PMO workbook with:
  - Dashboard
  - Gantt chart
  - RAID register
  - Team assignments

## Example Project Data

If you don't have a real project, create test data:

```python
# In your database or test file
{
    'project': {
        'id': 1,
        'project_name': 'Test Project',
        'project_key': 'TEST',
        'client_name': 'Test Client',
        'duration_weeks': 12,
        'team_size': 5,
        'start_date': '2026-07-01',
        'end_date': '2026-09-30'
    },
    'deliverables': [
        {
            'id': 'del_1',
            'name': 'Project Kickoff',
            'phase': 'Phase 1',
            'description': 'Initial project setup and planning',
            'tasks': [
                {
                    'id': 'tsk_1',
                    'name': 'Stakeholder Meeting',
                    'description': 'Meet with all stakeholders',
                    'start_date': '2026-07-01',
                    'end_date': '2026-07-03',
                    'duration_days': 2,
                    'priority': 'High'
                },
                {
                    'id': 'tsk_2',
                    'name': 'Create Project Charter',
                    'description': 'Develop project charter document',
                    'start_date': '2026-07-04',
                    'end_date': '2026-07-10',
                    'duration_days': 6,
                    'priority': 'High'
                }
            ]
        },
        {
            'id': 'del_2',
            'name': 'Design Phase',
            'phase': 'Phase 2',
            'description': 'Design system architecture',
            'tasks': [
                {
                    'id': 'tsk_3',
                    'name': 'Create Architecture Diagram',
                    'description': 'Document system architecture',
                    'start_date': '2026-07-11',
                    'end_date': '2026-07-18',
                    'duration_days': 7,
                    'priority': 'Medium'
                }
            ]
        }
    ],
    'team_members': [
        {
            'id': 'tm_1',
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'Project Manager'
        },
        {
            'id': 'tm_2',
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'role': 'Technical Lead'
        }
    ],
    'risks': [
        {
            'id': 'risk_1',
            'name': 'Resource Availability',
            'probability': 'Medium',
            'impact': 'High',
            'mitigation': 'Cross-train backup resources'
        },
        {
            'id': 'risk_2',
            'name': 'Scope Creep',
            'probability': 'High',
            'impact': 'Medium',
            'mitigation': 'Strict change control process'
        }
    ]
}
```

## Questions?

Refer to:
- **Integration details:** `FLASK_APP_INTEGRATION.md`
- **Testing help:** `PLATFORM_DELIVERY_TESTING_GUIDE.md`
- **Architecture:** `PLATFORM_DELIVERY_IMPLEMENTATION_SUMMARY.md`
- **Specific API issues:** Check error logs in Flask console

---

**Ready to deploy?** You're now set up to create project plans in Excel, SmartSheet, or Jira automatically! 🚀
