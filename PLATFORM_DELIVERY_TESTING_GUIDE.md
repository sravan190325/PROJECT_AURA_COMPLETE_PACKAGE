# Platform Delivery Testing Guide

## Overview

This guide covers testing the multi-platform project creation feature (Excel, SmartSheet, Jira Cloud).

## Test Environment Setup

### Prerequisites

- Python 3.9+
- Flask development server running
- Database with test project data
- API tokens/credentials for SmartSheet and Jira (optional for testing UI)

### Start Development Server

```bash
cd PROJECT_AURA_COMPLETE_PACKAGE
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

App will be available at: `http://localhost:5000`

## Testing Phases

### Phase 1: UI & Form Validation

**Test File:** `tests/test_platform_selection_ui.py`

#### Test Case 1.1: Platform Selection Page Loads
```python
def test_platform_selection_page_loads():
    response = client.get('/api/platform/selection/1')
    assert response.status_code == 200
    assert b'Select Your Delivery Platform' in response.data
    assert b'Excel Workbook' in response.data
    assert b'SmartSheet' in response.data
    assert b'Jira Scrum Board' in response.data
```

**Manual Test:**
1. Navigate to `http://localhost:5000/api/platform/selection/1`
2. Verify page loads with:
   - Project summary card (name, duration, team size)
   - Three platform options (Excel, SmartSheet, Jira)
   - No credentials section visible initially

#### Test Case 1.2: Excel Selection (No Credentials)
```python
def test_excel_selection_no_credentials():
    # Click Excel radio button
    # Credentials section should disappear
    # Submit button should be enabled
    pass
```

**Manual Test:**
1. Click "Excel Workbook" option
2. Verify credentials section is hidden
3. Verify submit button is enabled
4. Click "Create Project Plan" → Excel file should download

#### Test Case 1.3: SmartSheet Selection Shows Credentials
```python
def test_smartsheet_selection_shows_credentials():
    # Click SmartSheet radio button
    # Credentials section should appear
    # SmartSheet fields should be visible
    # Jira fields should be hidden
    pass
```

**Manual Test:**
1. Click "SmartSheet" option
2. Verify credentials section appears
3. Verify SmartSheet fields visible:
   - API Token input
   - Test Connection button
4. Submit button disabled (no credentials yet)
5. Enter token and click Test Connection
6. Verify success/error status appears

#### Test Case 1.4: Jira Selection Shows Credentials
```python
def test_jira_selection_shows_credentials():
    # Click Jira radio button
    # Credentials section should appear
    # Jira fields should be visible
    # SmartSheet fields should be hidden
    pass
```

**Manual Test:**
1. Click "Jira Scrum Board" option
2. Verify credentials section appears
3. Verify Jira fields visible:
   - Instance URL input
   - API Token input
   - Test Connection button
4. Submit button disabled
5. Enter URL and token
6. Click Test Connection
7. Verify success/error status

### Phase 2: Connection Testing

**Test File:** `tests/test_connection_endpoints.py`

#### Test Case 2.1: SmartSheet Connection - Valid Token
```python
def test_smartsheet_connection_valid():
    response = client.post('/api/platform/test-connection', json={
        'platform': 'smartsheet',
        'credentials': {'token': 'valid-token-here'}
    })
    assert response.status_code == 200
    data = response.json
    assert data['success'] == True
    assert 'account_name' in data
```

**Requirements:**
- Valid SmartSheet API token
- Test with token from `SmartSheet Account > Personal Settings > API Access`

**Manual Test:**
1. Get your SmartSheet API token
2. In browser, fill SmartSheet Token field
3. Click "Test Connection"
4. Verify green success message with account name

#### Test Case 2.2: SmartSheet Connection - Invalid Token
```python
def test_smartsheet_connection_invalid():
    response = client.post('/api/platform/test-connection', json={
        'platform': 'smartsheet',
        'credentials': {'token': 'invalid-token'}
    })
    assert response.status_code == 200
    data = response.json
    assert data['success'] == False
    assert 'error' in data
```

**Manual Test:**
1. Enter invalid/blank token
2. Click "Test Connection"
3. Verify red error message appears
4. Submit button remains disabled

#### Test Case 2.3: Jira Connection - Valid Credentials
```python
def test_jira_connection_valid():
    response = client.post('/api/platform/test-connection', json={
        'platform': 'jira',
        'credentials': {
            'url': 'https://your-domain.atlassian.net',
            'token': 'valid-jira-token'
        }
    })
    assert response.status_code == 200
    data = response.json
    assert data['success'] == True
```

**Requirements:**
- Valid Jira Cloud instance URL
- Valid API token from `Jira > Settings > Security > API Tokens`

**Manual Test:**
1. Get your Jira instance URL and API token
2. Fill both Jira fields
3. Click "Test Connection"
4. Verify green success message

#### Test Case 2.4: Jira Connection - Invalid URL
```python
def test_jira_connection_invalid_url():
    response = client.post('/api/platform/test-connection', json={
        'platform': 'jira',
        'credentials': {
            'url': 'https://invalid-domain.atlassian.net',
            'token': 'token'
        }
    })
    data = response.json
    assert data['success'] == False
```

**Manual Test:**
1. Enter non-existent Jira URL
2. Enter any token
3. Click "Test Connection"
4. Verify error message (connection refused or 404)

### Phase 3: Project Creation

**Test File:** `tests/test_project_creation.py`

#### Test Case 3.1: Create Excel Project
```python
def test_create_excel_project():
    response = client.post('/api/project/create-platform', json={
        'project_id': 1,
        'platform': 'excel',
        'credentials': {}
    })
    assert response.status_code == 200
    data = response.json
    assert data['success'] == True
    assert 'file_path' in data
    assert data['platform'] == 'excel'
```

**Manual Test:**
1. Select "Excel Workbook"
2. Click "Create Project Plan"
3. Verify progress bar animates
4. On success:
   - Message shows "Project plan created successfully!"
   - Page redirects to project summary page
5. Verify Excel file was created/downloaded

#### Test Case 3.2: Create SmartSheet Project
```python
def test_create_smartsheet_project():
    response = client.post('/api/project/create-platform', json={
        'project_id': 1,
        'platform': 'smartsheet',
        'credentials': {'token': 'valid-token'}
    })
    assert response.status_code == 200
    data = response.json
    assert data['success'] == True
    assert data['platform'] == 'smartsheet'
    assert 'sheet_id' in data
    assert 'sheet_url' in data
```

**Manual Test (requires SmartSheet account):**
1. Select SmartSheet
2. Enter valid API token
3. Click "Create Project Plan"
4. Wait for creation (30-60 seconds)
5. On success, verify:
   - Page shows success message
   - Click link opens SmartSheet sheet
   - Sheet has:
     - Project name
     - Task hierarchy with phases → deliverables → tasks
     - Date columns for Gantt
     - Team member section
     - Risk section
     - Gantt view enabled

#### Test Case 3.3: Create Jira Project
```python
def test_create_jira_project():
    response = client.post('/api/project/create-platform', json={
        'project_id': 1,
        'platform': 'jira',
        'credentials': {
            'url': 'https://domain.atlassian.net',
            'token': 'token'
        }
    })
    assert response.status_code == 200
    data = response.json
    assert data['success'] == True
    assert data['platform'] == 'jira'
    assert 'project_key' in data
    assert 'project_url' in data
```

**Manual Test (requires Jira Cloud account):**
1. Select Jira Scrum Board
2. Enter Jira URL and API token
3. Click "Create Project Plan"
4. Wait for creation (60-90 seconds)
5. On success, verify:
   - Page shows success message
   - Click link opens Jira project
   - Project has:
     - Scrum board created
     - Epics created from phases
     - User stories created from deliverables
     - Subtasks created from tasks
     - Sprints created (2-week intervals)
     - Risk issues created with RISK label

### Phase 4: Error Handling

**Test File:** `tests/test_error_handling.py`

#### Test Case 4.1: Missing Project
```python
def test_missing_project():
    response = client.get('/api/platform/selection/99999')
    assert response.status_code == 404
```

#### Test Case 4.2: Invalid Credentials During Creation
```python
def test_smartsheet_creation_invalid_token():
    response = client.post('/api/project/create-platform', json={
        'project_id': 1,
        'platform': 'smartsheet',
        'credentials': {'token': 'invalid'}
    })
    data = response.json
    assert data['success'] == False
    assert 'error' in data
```

**Manual Test:**
1. Select SmartSheet with invalid token
2. Click "Create Project Plan"
3. Verify error message appears
4. Verify button is re-enabled for retry

#### Test Case 4.3: Network Timeout
```python
def test_connection_timeout(monkeypatch):
    def timeout_error(*args, **kwargs):
        raise requests.exceptions.Timeout()
    monkeypatch.setattr('requests.get', timeout_error)
    
    response = client.post('/api/platform/test-connection', json={
        'platform': 'smartsheet',
        'credentials': {'token': 'token'}
    })
    data = response.json
    assert data['success'] == False
```

### Phase 5: Performance & Load Testing

**Test File:** `tests/test_performance.py`

#### Test Case 5.1: SmartSheet API Rate Limiting
```python
def test_smartsheet_rate_limiting():
    """Verify rate limiting respected (300 req/min)"""
    for i in range(300):
        response = client.post('/api/platform/test-connection', ...)
    # Should all succeed
    # 301st request should be queued or fail gracefully
```

#### Test Case 5.2: Large Project Creation
```python
def test_large_project_creation():
    """Test with project containing 50+ deliverables"""
    large_project = generate_large_project(deliverables=50, tasks=5)
    response = client.post('/api/project/create-platform', json={...})
    assert response.status_code == 200
```

## Running Tests

### Unit Tests
```bash
pytest tests/test_platform_selection_ui.py -v
pytest tests/test_connection_endpoints.py -v
pytest tests/test_project_creation.py -v
```

### Integration Tests
```bash
pytest tests/integration/ -v --tb=short
```

### All Tests
```bash
pytest tests/ -v --cov=services/platform_creators
```

## Browser Testing Checklist

- [ ] Platform selection page loads correctly
- [ ] All three platform options display with icons and descriptions
- [ ] Excel selection hides credentials section
- [ ] SmartSheet selection shows SmartSheet credentials
- [ ] Jira selection shows Jira credentials
- [ ] Submit button enables/disables correctly
- [ ] Test Connection buttons work for both platforms
- [ ] Connection status messages display (success/error)
- [ ] Form submission animates progress bar
- [ ] Success redirects to project summary
- [ ] Error messages display and button re-enables
- [ ] SmartSheet project link opens correctly
- [ ] Jira project link opens correctly
- [ ] Excel file downloads successfully

## Known Limitations

1. **SmartSheet:**
   - Column IDs are fetched fresh each time (should be cached in production)
   - Parent-child hierarchy uses row numbering (may need refine)
   - Gantt view may need manual date column linking

2. **Jira:**
   - Basic auth requires email (not username)
   - Epic custom field ID may vary per Jira instance
   - Sprint creation requires Agile board to exist first

3. **Excel:**
   - Requires openpyxl library
   - May need formula recalculation after creation

## Troubleshooting

### SmartSheet Token Issues
```
Error: SmartSheet API error: 401
→ Verify token is copied completely
→ Check token not expired in SmartSheet settings
→ Ensure token has sheet management permissions
```

### Jira Connection Issues
```
Error: 401 Unauthorized
→ Verify email + token (not username + token)
→ Check token not expired in Jira settings
→ Ensure token has correct scopes

Error: 404 Not Found
→ Verify Jira instance URL (https://domain.atlassian.net)
→ Check for trailing slashes
```

### Excel Creation Issues
```
Error: openpyxl not installed
→ pip install openpyxl

Error: Permission denied writing file
→ Check file write permissions in working directory
```

## Test Data Generation

```python
# In tests/conftest.py
@pytest.fixture
def sample_project():
    return {
        'project': {
            'id': 1,
            'project_name': 'Test Project',
            'project_key': 'TEST',
            'client_name': 'Test Client',
            'duration_weeks': 12,
            'team_size': 5
        },
        'deliverables': [
            {
                'id': 'del_1',
                'name': 'Phase 1 Deliverable',
                'phase': 'Phase 1',
                'tasks': [
                    {
                        'id': 'tsk_1',
                        'name': 'Task 1',
                        'start_date': '2026-07-01',
                        'end_date': '2026-07-15'
                    }
                ]
            }
        ],
        'team_members': [
            {
                'name': 'Test User',
                'email': 'test@example.com',
                'role': 'Manager'
            }
        ],
        'risks': [
            {
                'id': 'risk_1',
                'name': 'Test Risk',
                'probability': 'High',
                'impact': 'High'
            }
        ]
    }
```

## Next Steps

1. Set up test database with sample projects
2. Create pytest fixtures for all test data
3. Implement mocking for external API calls
4. Add performance benchmarks
5. Set up CI/CD integration for automated testing
6. Create test reports and coverage tracking
