# Flask App Integration Guide

## Backend Routes Registration

The platform delivery routes have been created and need to be registered in your main Flask application.

### Files Created

1. **`routes/platform_delivery_routes.py`** — Main routes for platform selection and creation
   - `GET /api/platform/selection/<int:project_id>` — Display platform selection page
   - `POST /api/platform/test-connection` — Test platform credentials
   - `POST /api/project/create-platform` — Create project in selected platform

2. **`services/platform_creators/smartsheet_creator.py`** — SmartSheet API integration
   - `SmartSheetCreator` class with methods for creating sheets, adding hierarchy, enabling Gantt

3. **`services/platform_creators/jira_creator.py`** — Jira Cloud API integration
   - `JiraCreator` class with methods for creating Scrum projects, epics, stories, sprints

4. **`templates/platform_delivery_selection.html`** — Platform selection UI template

### Integration Steps

#### 1. Update Your Main Flask App (`app.py` or similar)

```python
from flask import Flask
from routes.platform_delivery_routes import platform_bp, project_bp

app = Flask(__name__)

# Register platform delivery blueprints
app.register_blueprint(platform_bp)
app.register_blueprint(project_bp)

# Your other routes...
```

#### 2. Ensure Required Services Exist

The `platform_delivery_routes.py` imports:
- `DatabaseService` from `services.database_service`
- `SmartSheetCreator` from `services.platform_creators.smartsheet_creator`
- `JiraCreator` from `services.platform_creators.jira_creator`
- `ExcelCreator` from `services.platform_creators.excel_creator`

**Update your `database_service.py`** to include these methods:

```python
class DatabaseService:
    def get_project_summary(self, project_id: int) -> Optional[Dict]:
        """
        Retrieve complete project data including:
        - project: {project_name, duration_weeks, team_size, client_name, ...}
        - deliverables: [{id, name, phase, description, tasks: [{...}]}, ...]
        - team_members: [{name, email, role}, ...]
        - risks: [{id, name, probability, impact, mitigation}, ...]
        """
        pass
```

#### 3. Environment Variables

Ensure your `.env` file includes:

```bash
# Optional: SmartSheet base configuration
SMARTSHEET_API_URL=https://api.smartsheet.com/2.0

# Optional: Jira base configuration
JIRA_AUTH_TYPE=api_token  # or oauth
```

**Security Note:** Never store API tokens in `.env`. Let users provide them via the UI.

### API Endpoints

#### Display Platform Selection Page
```bash
GET /api/platform/selection/123
# Returns: HTML page with project details and platform options
```

#### Test Platform Connection
```bash
POST /api/platform/test-connection
Content-Type: application/json

# SmartSheet:
{
  "platform": "smartsheet",
  "credentials": {
    "token": "your-api-token"
  }
}

# Jira:
{
  "platform": "jira",
  "credentials": {
    "url": "https://your-domain.atlassian.net",
    "token": "your-api-token"
  }
}

# Response:
{
  "success": true,
  "account_name": "Account Display Name"
}
```

#### Create Project in Platform
```bash
POST /api/project/create-platform
Content-Type: application/json

{
  "project_id": 123,
  "platform": "smartsheet",  # or "jira" or "excel"
  "credentials": {
    "token": "..."  # SmartSheet
    # or
    "url": "...",
    "token": "..."  # Jira
  }
}

# Response on Success:
{
  "success": true,
  "platform": "smartsheet",
  "project_id": 123,
  "sheet_id": "...",
  "sheet_url": "https://app.smartsheet.com/sheets/...",
  "redirect_url": "/api/project/123/summary"
}

# Response on Error:
{
  "success": false,
  "error": "Connection failed: Invalid token"
}
```

### Project Data Structure

The `get_project_summary()` method should return:

```python
{
    "project": {
        "id": 123,
        "project_name": "Project Aura",
        "project_key": "PROJ",  # For Jira
        "client_name": "Client Name",
        "duration_weeks": 26,
        "team_size": 12,
        "start_date": "2026-07-01",
        "end_date": "2027-12-31"
    },
    "deliverables": [
        {
            "id": "del_1",
            "name": "Deliverable 1",
            "phase": "Phase 1",
            "description": "Description...",
            "tasks": [
                {
                    "id": "tsk_1",
                    "name": "Task 1",
                    "description": "Task description",
                    "start_date": "2026-07-01",
                    "end_date": "2026-07-15",
                    "duration_days": 14,
                    "priority": "High"
                }
            ]
        }
    ],
    "team_members": [
        {
            "id": "tm_1",
            "name": "John Doe",
            "email": "john@example.com",
            "role": "Project Manager"
        }
    ],
    "risks": [
        {
            "id": "risk_1",
            "name": "Resource Availability",
            "probability": "Medium",
            "impact": "High",
            "mitigation": "Mitigation strategy..."
        }
    ]
}
```

### Platform-Specific Details

#### SmartSheet
- **Authentication:** API token (Bearer token in Authorization header)
- **Sheet Structure:** 14-column setup with hierarchy support
- **Gantt View:** Automatically enabled on creation
- **Rate Limit:** 300 requests/minute

#### Jira Cloud
- **Authentication:** Basic auth with email + API token
- **Project Type:** Scrum template (`com.pyxus.jira.plugin.cloud:scrum`)
- **Hierarchy:** Epic → Story → Subtask
- **Sprints:** Auto-created based on project duration (2-week sprints)
- **Rate Limit:** 1200 requests/hour

#### Excel
- **Requirements:** `services/platform_creators/excel_creator.py` must implement:
  ```python
  class ExcelCreator:
      def create(self, deliverables, team_members, risks) -> Dict[str, Any]:
          # Return: {'success': True, 'file_path': '...'}
  ```

### Error Handling

All endpoints follow this error response format:

```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

The routes include comprehensive error logging for debugging.

### Testing

#### Test with curl:
```bash
# Test SmartSheet Connection
curl -X POST http://localhost:5000/api/platform/test-connection \
  -H "Content-Type: application/json" \
  -d '{"platform":"smartsheet","credentials":{"token":"your-token"}}'

# Create SmartSheet Project
curl -X POST http://localhost:5000/api/project/create-platform \
  -H "Content-Type: application/json" \
  -d '{"project_id":123,"platform":"smartsheet","credentials":{"token":"your-token"}}'
```

#### Test with Python:
```python
import requests

# Test connection
response = requests.post('http://localhost:5000/api/platform/test-connection', json={
    'platform': 'smartsheet',
    'credentials': {'token': 'your-token'}
})
print(response.json())

# Create project
response = requests.post('http://localhost:5000/api/project/create-platform', json={
    'project_id': 123,
    'platform': 'jira',
    'credentials': {
        'url': 'https://domain.atlassian.net',
        'token': 'your-token'
    }
})
print(response.json())
```

### Next Steps

1. **Implement `DatabaseService.get_project_summary()`** in your database service
2. **Test the SmartSheet API token** format in your environment
3. **Test the Jira API connection** with proper Base64 encoding for auth
4. **Implement Excel creator** if using Excel platform
5. **Add proper error handling and logging** for production
6. **Implement credential encryption** for storing user tokens in database
7. **Add transaction management** for multi-platform atomic operations
8. **Create comprehensive test suite** for all three platforms
