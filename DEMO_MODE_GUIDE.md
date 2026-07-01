# Demo Mode Guide - Platform Delivery Feature

## Overview

**Demo Mode** allows you to test the entire platform delivery feature **without needing real API credentials** for SmartSheet or Jira Cloud.

Simply use the token: **`demo`** to activate demo mode for any platform.

---

## 🎯 What Demo Mode Does

✅ **Simulates** platform API responses
✅ **Shows** what would be created
✅ **Generates** sample project structures
✅ **No real accounts needed** - no SmartSheet or Jira access required
✅ **Full UI flow** - test the entire experience
✅ **Returns realistic responses** - same format as real API calls

---

## 🚀 How to Use Demo Mode

### Step 1: Open Platform Selection Page
```
http://localhost:5000/api/platform/selection/1
```

### Step 2: Select a Platform

#### **Option A: Excel (Demo - No Credentials)**
1. Click "📊 Excel Workbook"
2. Click "Create Project Plan"
3. ✅ Excel file is generated instantly

#### **Option B: SmartSheet (Demo Mode)**
1. Click "📈 SmartSheet"
2. In the **"SmartSheet API Token"** field, enter: **`demo`**
3. Click "Test Connection"
4. ✅ Demo account response appears: "Demo SmartSheet Account"
5. Click "Create Project Plan"
6. ✅ Demo project created with sample structure

#### **Option C: Jira (Demo Mode)**
1. Click "🚀 Jira Scrum Board"
2. In the **"Jira Instance URL"** field, enter any URL (demo accepts anything)
3. In the **"Jira API Token"** field, enter: **`demo`**
4. Click "Test Connection"
5. ✅ Demo account response appears: "Demo Jira Cloud Account"
6. Click "Create Project Plan"
7. ✅ Demo Scrum project created with sample structure

---

## 📊 Demo Mode Responses

### SmartSheet Demo Response
```json
{
  "success": true,
  "platform": "smartsheet",
  "project_id": 1,
  "sheet_id": "demo_1_smartsheet",
  "sheet_url": "https://app.smartsheet.com/sheets/demo_1",
  "demo_mode": true,
  "message": "Demo mode: Project structure created successfully (not synced to actual SmartSheet)",
  "redirect_url": "/api/project/1/summary"
}
```

### Jira Demo Response
```json
{
  "success": true,
  "platform": "jira",
  "project_id": 1,
  "project_key": "DEMO1",
  "project_url": "https://demo.atlassian.net/browse/DEMO1",
  "demo_mode": true,
  "message": "Demo mode: Scrum board structure created successfully (not synced to actual Jira)",
  "redirect_url": "/api/project/1/summary"
}
```

---

## 🧪 Test Scenarios

### Scenario 1: Full Excel Workflow
**Time:** ~30 seconds

1. Navigate to platform selection page
2. Select Excel
3. Click "Create Project Plan"
4. Watch progress bar
5. See success message
6. ✅ Excel file created in `/workbooks` folder

**What happens:**
- Sample project data with 4 deliverables
- 5 team members
- 4 identified risks
- Complete task hierarchy

### Scenario 2: SmartSheet Demo Workflow
**Time:** ~45 seconds

1. Select SmartSheet
2. Enter token: `demo`
3. Click "Test Connection"
4. See green success: "Demo SmartSheet Account"
5. Click "Create Project Plan"
6. Progress bar animates (15-30 sec simulation)
7. ✅ Success message with demo sheet URL

**What demo creates:**
- Sheet named "Test Project Aura"
- 14-column PMO structure
- Task hierarchy (Phases → Deliverables → Tasks)
- Team member assignments
- Risk register
- Gantt view configuration

### Scenario 3: Jira Demo Workflow
**Time:** ~60 seconds

1. Select Jira Scrum Board
2. Enter URL: `https://demo.atlassian.net` (or any URL)
3. Enter token: `demo`
4. Click "Test Connection"
5. See green success: "Demo Jira Cloud Account"
6. Click "Create Project Plan"
7. Progress bar animates (30-60 sec simulation)
8. ✅ Success message with demo project URL

**What demo creates:**
- Scrum project with key "DEMO1"
- Epics for each phase
- User stories for each deliverable
- Subtasks for each task
- 2-week sprint schedule
- Risk tracking issues

---

## 🔑 Demo Mode Activation

Demo mode activates automatically when you use these tokens:

| Platform | Demo Token |
|----------|-----------|
| **SmartSheet** | `demo` or `demo123` |
| **Jira** | `demo` or `demo123` |
| **Excel** | (Always works, no token needed) |

---

## 📝 What Gets Logged

When using demo mode, you'll see log entries like:

```
[DEMO MODE] Creating SmartSheet project: demo_1_smartsheet
[DEMO MODE] Creating Jira Scrum project: DEMO1
```

No actual API calls are made to SmartSheet or Jira in demo mode.

---

## ✨ Benefits of Demo Mode

✅ **Instant Testing** — No waiting for API approvals or credential setup
✅ **Risk-Free** — No actual projects created on real accounts
✅ **Educational** — See exactly what gets created on each platform
✅ **Complete Flow** — Test the entire UI and backend together
✅ **Reproducible** — Same response every time
✅ **Share With Team** — Show stakeholders the feature without credentials

---

## 🔄 Transitioning to Real Credentials

Once you have real SmartSheet or Jira credentials:

1. **Get SmartSheet API Token:**
   - Log in to SmartSheet
   - Account → Personal Settings → API Access
   - Generate new token
   - Copy and paste into form

2. **Get Jira API Token:**
   - Log in to Jira Cloud
   - Settings → Personal Settings
   - Security tab → API Tokens
   - Create new token
   - Copy and use in form

3. **Switch from Demo to Real:**
   - Just replace `demo` token with your real token
   - Click "Test Connection" again
   - Real project will be created instead

---

## 🧩 Sample Test Data

All demo/test modes use this sample project:

```
Project: Test Project Aura
Client: Acme Corporation
Duration: 12 weeks
Team Size: 8 people

Phases:
├─ Phase 1: Initiation
│  ├─ Project Discovery & Planning (Deliverable)
│  │  ├─ Kickoff Meeting (Task)
│  │  └─ Requirements Gathering (Task)
│
├─ Phase 2: Design
│  └─ Solution Design (Deliverable)
│     └─ Architecture Design (Task)
│
├─ Phase 3: Execution
│  ├─ Development & Testing (Deliverable)
│  │  └─ Dev Sprint 1 (Task)
│
└─ Phase 4: Closure
   └─ Deployment & Handover (Deliverable)
      └─ Production Deployment (Task)

Team:
- John Doe (Project Manager)
- Jane Smith (Technical Lead)

Risks:
- Resource Availability (Medium/High)
- Scope Creep (High/Medium)
- Tech Integration Issues (Medium/High)
- Schedule Delays (Medium/Medium)
```

---

## 🎬 Live Demo Walkthrough

### Quick 2-Minute Demo
```
1. Open http://localhost:5000/api/platform/selection/1
2. Click "📊 Excel Workbook"
3. Click "Create Project Plan"
4. ✅ See Excel success (fastest)
```

### Medium 5-Minute Demo
```
1. Open platform selection page
2. Click "📈 SmartSheet"
3. Enter token: demo
4. Click "Test Connection" → Green success
5. Click "Create Project Plan"
6. Watch progress bar animate
7. ✅ See demo sheet URL in response
```

### Full 10-Minute Demo
```
1. Test Excel workflow (2 min)
2. Test SmartSheet demo (3 min)
3. Test Jira demo (3 min)
4. Review sample output
5. ✅ Complete understanding of feature
```

---

## 📋 Checklist: Testing Demo Mode

- [ ] **Excel Test**
  - [ ] Platform loads
  - [ ] Excel option selectable
  - [ ] File generated successfully
  - [ ] Progress bar works

- [ ] **SmartSheet Demo**
  - [ ] SmartSheet option shows credential fields
  - [ ] Token field accepts "demo"
  - [ ] Test Connection returns success
  - [ ] Project creation responds with demo data
  - [ ] Progress animates during creation

- [ ] **Jira Demo**
  - [ ] Jira option shows credential fields
  - [ ] URL and token fields accept input
  - [ ] Test Connection returns success with demo token
  - [ ] Project creation responds with demo data
  - [ ] Scrum board structure shown in response

- [ ] **UI/UX**
  - [ ] Form validation works
  - [ ] Status messages display correctly
  - [ ] Redirect works on success
  - [ ] Error messages appear on wrong input

---

## 🐛 Troubleshooting Demo Mode

### Token not recognized
**Solution:** Use exactly `demo` (lowercase) or `demo123`

### Connection test fails with real token
**Solution:** Check token format and validity in real account settings

### Want to switch from demo to real
**Solution:** Stop Flask, replace `demo` with real token, restart server

### Want to see what would be created without our code
**Solution:** Check sample test data section above

---

## 🚀 Next Steps

1. ✅ **Test Demo Mode** — Try all three platforms with `demo` token
2. 📊 **Review Output** — Check the response structures
3. 🔐 **Get Real Credentials** — When ready
4. 🔄 **Upgrade to Production** — Replace demo tokens with real ones
5. 📚 **Full Integration** — Follow FLASK_APP_INTEGRATION.md

---

## 📞 Quick Reference

| What | How | Token |
|------|-----|-------|
| Test Excel | Select & create | (none) |
| Test SmartSheet | Select, enter token | `demo` |
| Test Jira | Select, enter URL+token | `demo` |
| Use Real SmartSheet | Same flow | (your token) |
| Use Real Jira | Same flow | (your token) |

---

**Demo mode is perfect for understanding the feature without API access.** 🎉

Once you have real credentials, just swap the token and connect to actual SmartSheet/Jira!
