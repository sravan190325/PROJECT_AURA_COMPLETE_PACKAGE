# Project Aura – Multi-Platform Project Plan Generation
## Comprehensive Design Document

**Version**: 1.0  
**Status**: Design Phase  
**Date**: January 2025  
**Author**: Solution Architecture Team  

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [UI/UX Design](#uiux-design)
4. [Backend API Design](#backend-api-design)
5. [Platform Integration Specifications](#platform-integration-specifications)
6. [Data Mapping Models](#data-mapping-models)
7. [Agent Workflow Updates](#agent-workflow-updates)
8. [Database Schema Updates](#database-schema-updates)
9. [Security & Authentication](#security--authentication)
10. [Error Handling & Rollback Strategy](#error-handling--rollback-strategy)
11. [Implementation Plan & Milestones](#implementation-plan--milestones)
12. [Testing Strategy](#testing-strategy)
13. [Deployment & DevOps](#deployment--devops)

---

## Executive Summary

### Objective
Enhance Project Aura to automatically generate and deploy project plans to multiple delivery platforms simultaneously (Excel, SmartSheet, Jira, Azure DevOps) from a single document upload and project analysis.

### Scope
- **Phase 1**: SmartSheet, Jira, Azure DevOps, Excel (concurrent)
- **Extensibility**: Designed for future platforms (Monday.com, Asana, MS Project)
- **User Experience**: Single upload → Multi-platform generation
- **Authentication**: User-provided API tokens/OAuth
- **Rollback**: Atomic transactions with full rollback on any failure

### Key Features
✓ Simultaneous multi-platform creation  
✓ Configurable WBS → Platform mapping  
✓ User-provided credentials with secure storage  
✓ Automatic rollback on any platform failure  
✓ Placeholder resource assignments  
✓ Rich status dashboard with direct links  
✓ Enterprise-grade error handling  
✓ Extensible mapping engine  

---

## System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT AURA - FRONTEND                      │
│  (React/Vue with Enhanced UI for Platform Selection & Auth)     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    Document Upload & Analysis
                             │
┌────────────────────────────▼────────────────────────────────────┐
│              PROJECT AURA - API GATEWAY LAYER                   │
│         (Flask Blueprint Routes with Auth Middleware)           │
└──────┬──────────┬──────────┬──────────┬──────────┬──────────────┘
       │          │          │          │          │
   Analysis   Planning    Validation   Mapping    Delivery
    Agent       Agent       Agent      Engine      Agent
       │          │          │          │          │
└──────┴──────────┴──────────┴──────────┴──────────┴──────────────┐
│         PROJECT AURA CORE SERVICES LAYER                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Core Services:                                         │   │
│  │  - Claude AI Analysis Service                          │   │
│  │  - Project Planning Engine                             │   │
│  │  - WBS Generator                                       │   │
│  │  - Risk Assessment Service                             │   │
│  │  - Resource Planning Service                           │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────┬─────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────┐
│        DELIVERY PLATFORM AGENT (Multi-Platform Orchestration)  │
│  ┌──────────────┬──────────────┬──────────────┬─────────────┐  │
│  │   Excel      │  SmartSheet  │     Jira     │   Azure     │  │
│  │   Creator    │   Creator    │   Creator    │   DevOps    │  │
│  │              │              │              │   Creator   │  │
│  └──────┬───────┴──────┬───────┴──────┬───────┴──────┬──────┘  │
│         │              │              │              │         │
└─────────┼──────────────┼──────────────┼──────────────┼────────┘
          │              │              │              │
    ┌─────▼──┐      ┌────▼────┐    ┌───▼───┐    ┌────▼────┐
    │ Excel  │      │SmartSheet│   │ Jira  │    │  Azure  │
    │ API    │      │   API    │   │  API  │    │ DevOps  │
    │        │      │          │   │       │    │   API   │
    └────────┘      └──────────┘   └───────┘    └─────────┘
          │              │              │              │
    ┌─────▼──────────────▼──────────────▼──────────────▼─────┐
    │    Credentials & Connection Pool (Encrypted Storage)  │
    └──────────────────────────────────────────────────────┘
          │
    ┌─────▼──────────────────────────────────────────┐
    │  Database Layer                                │
    │  ├─ Projects                                   │
    │  ├─ Integration Credentials (Encrypted)        │
    │  ├─ Platform Creation History                  │
    │  ├─ Mapping Configurations                     │
    │  └─ Status & Error Logs                        │
    └───────────────────────────────────────────────┘
```

### 2.2 Service Layer Architecture

```
┌─────────────────────────────────────────────────────┐
│      Delivery Platform Agent (NEW)                  │
│  - Orchestrates multi-platform creation             │
│  - Manages transactional flow                       │
│  - Handles rollback on failures                     │
│  - Returns consolidated status                      │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
    ┌───▼──┐  ┌───▼──┐  ┌───▼──┐
    │ Exec │  │Validate│  │Map  │
    │ Task │  │Status  │  │Data │
    │      │  │        │  │     │
    └───┬──┘  └───┬──┘  └───┬──┘
        │         │         │
    ┌───▼─────────▼─────────▼──┐
    │  Platform Adapters       │
    │  - Excel Adapter         │
    │  - SmartSheet Adapter    │
    │  - Jira Adapter          │
    │  - Azure DevOps Adapter  │
    └───┬─────────┬─────────┬──┘
        │         │         │
    ┌───▼──┐  ┌───▼──┐  ┌──▼───┐
    │Auth  │  │Data  │  │Error │
    │Mgr   │  │Mapper│  │Hdlr  │
    └──────┘  └──────┘  └──────┘
```

### 2.3 Data Flow

```
1. Document Upload
   ↓
2. AI Analysis (Claude)
   ↓
3. Project Plan Generation
   ├─ WBS Structure
   ├─ Schedule
   ├─ Resources
   ├─ Risks
   └─ Deliverables
   ↓
4. Platform Selection UI
   ├─ Excel: ☑
   ├─ SmartSheet: ☑
   ├─ Jira: ☑
   └─ Azure DevOps: ☑
   ↓
5. Credential Management
   ├─ SmartSheet Token/OAuth
   ├─ Jira URL + Token
   ├─ Azure DevOps URL + PAT
   └─ Excel (Local - No Auth)
   ↓
6. Mapping Configuration (Optional)
   ├─ Epic Naming Convention
   ├─ Story Field Mapping
   ├─ Sprint Planning Strategy
   └─ Custom Fields
   ↓
7. Delivery Platform Agent
   ├─ Validate Credentials
   ├─ Transform Data
   ├─ Execute in Parallel
   │  ├─ Excel Creator
   │  ├─ SmartSheet Creator
   │  ├─ Jira Creator
   │  └─ Azure DevOps Creator
   ├─ Monitor Status
   └─ Rollback if Any Failure
   ↓
8. Return Status Dashboard
   ├─ Excel: ✓ Success (Download)
   ├─ SmartSheet: ✓ Success (Link)
   ├─ Jira: ✓ Success (Link)
   └─ Azure DevOps: ✓ Success (Link)
```

---

## UI/UX Design

### 3.1 Platform Selection Screen

**After AI Analysis Complete:**

```
╔════════════════════════════════════════════════════════╗
║  PROJECT AURA - DELIVERY PLATFORM SELECTION            ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  Project: Mobile Banking Platform                      ║
║  Duration: 26 weeks | Team: 12 people | Budget: $500K  ║
║                                                        ║
║  ┌──────────────────────────────────────────────────┐ ║
║  │ SELECT DELIVERY PLATFORMS                        │ ║
║  └──────────────────────────────────────────────────┘ ║
║                                                        ║
║  ☑ EXCEL WORKBOOK                                      ║
║    └─ Downloads 12-sheet PMO-grade workbook           ║
║       (Project Dashboard, Gantt, RAID, Resources)     ║
║                                                        ║
║  ☑ SMARTSHEET                                          ║
║    └─ Creates professional project sheet with         ║
║       Gantt chart, dependencies, resource view        ║
║    [ Configure SmartSheet Auth ]                       ║
║    [ Optional: Configure Mapping ]                     ║
║                                                        ║
║  ☑ JIRA (Cloud)                                        ║
║    └─ Auto-creates Epics, Stories, and Tasks          ║
║       with Scrum sprints                              ║
║    [ Configure Jira Auth ]                            ║
║    [ Optional: Configure Mapping ]                     ║
║                                                        ║
║  ☑ AZURE DEVOPS                                        ║
║    └─ Creates Work Items (Epic, Feature, Task)        ║
║       with Iterations and Backlogs                    ║
║    [ Configure Azure DevOps Auth ]                     ║
║    [ Optional: Configure Mapping ]                     ║
║                                                        ║
║  ┌─────────────────┬──────────────────────────────┐  ║
║  │ [ < Previous ]  │  [ Create All Platforms > ]  │  ║
║  └─────────────────┴──────────────────────────────┘  ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

### 3.2 Credential Entry Screen

**SmartSheet Example:**

```
╔════════════════════════════════════════════════════════╗
║  SMARTSHEET AUTHENTICATION                             ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  ┌──────────────────────────────────────────────────┐ ║
║  │ Authentication Method                            │ ║
║  │ ○ API Token  ● OAuth 2.0                        │ ║
║  └──────────────────────────────────────────────────┘ ║
║                                                        ║
║  API Token Option:                                     ║
║  ┌──────────────────────────────────────────────────┐ ║
║  │ SmartSheet API Token:                            │ ║
║  │ [________________________________] (Encrypted)  │ ║
║  │ ℹ Get token from smartsheet.com/user/settings   │ ║
║  └──────────────────────────────────────────────────┘ ║
║                                                        ║
║  OAuth Option:                                         ║
║  ┌──────────────────────────────────────────────────┐ ║
║  │ [ Authenticate with SmartSheet OAuth ]           │ ║
║  │ (Opens SmartSheet consent screen)                │ ║
║  └──────────────────────────────────────────────────┘ ║
║                                                        ║
║  ☐ Save credentials for future use                     ║
║  ℹ Encrypted and stored securely                      ║
║                                                        ║
║  ┌──────────────────┬──────────────────────────────┐  ║
║  │ [ Back ]         │  [ Test Connection ] [Next] │  ║
║  └──────────────────┴──────────────────────────────┘  ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

### 3.3 Mapping Configuration Screen

**WBS to Jira Mapping:**

```
╔════════════════════════════════════════════════════════╗
║  JIRA MAPPING CONFIGURATION (OPTIONAL)                ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  Project Key: [MOBANK__________]                       ║
║  Board Type:  ○ Scrum  ● Kanban                       ║
║                                                        ║
║  HIERARCHY MAPPING                                     ║
║  ┌──────────────────────────────────────────────────┐ ║
║  │ WBS Level         →  Jira Level     Customize?  │ ║
║  ├──────────────────────────────────────────────────┤ ║
║  │ Phase             →  Epic           [  Edit  ]  │ ║
║  │ Deliverable       →  Story          [  Edit  ]  │ ║
║  │ Task              →  Task           [  Edit  ]  │ ║
║  │ Subtask           →  Subtask        [  Edit  ]  │ ║
║  └──────────────────────────────────────────────────┘ ║
║                                                        ║
║  FIELD MAPPING                                         ║
║  ┌──────────────────────────────────────────────────┐ ║
║  │ Project Field         Jira Field                 │ ║
║  ├──────────────────────────────────────────────────┤ ║
║  │ Owner             → Assignee                     │ ║
║  │ Duration (days)   → Story Points (Auto-calc)    │ ║
║  │ Risk Level        → Custom Field: Risk          │ ║
║  │ Dependencies      → Link Issues                 │ ║
║  └──────────────────────────────────────────────────┘ ║
║                                                        ║
║  SPRINT PLANNING                                       ║
║  ┌──────────────────────────────────────────────────┐ ║
║  │ ○ Auto-create sprints by phase                  │ ║
║  │ ● Manual sprint mapping (below)                  │ ║
║  │ ○ Create 2-week sprints                         │ ║
║  └──────────────────────────────────────────────────┘ ║
║                                                        ║
║  Phase → Sprint Mapping:                              ║
║  Initiation Phase  → Sprint 1 (Start: 01/01/2025)    ║
║  Planning Phase    → Sprint 2 (Start: 01/15/2025)    ║
║                                                        ║
║  ┌──────────────────┬──────────────────────────────┐  ║
║  │ [ Back ]         │  [ Use Defaults ] [Apply] │  ║
║  └──────────────────┴──────────────────────────────┘  ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

### 3.4 Status Dashboard

**After Multi-Platform Creation:**

```
╔═══════════════════════════════════════════════════════════════════╗
║  PROJECT AURA - DELIVERY STATUS DASHBOARD                         ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Project: Mobile Banking Platform (Mobile Banking App)            ║
║  Status: ✓ ALL PLATFORMS CREATED SUCCESSFULLY                     ║
║  Timestamp: 2025-01-15 14:32:45 UTC                              ║
║                                                                   ║
║  ╔═══════════════════════════════════════════════════════════╗  ║
║  ║ EXCEL WORKBOOK                                   ✓ Success ║  ║
║  ╠═══════════════════════════════════════════════════════════╣  ║
║  ║ Status: Ready for Download                               ║  ║
║  ║ File: Project_Plan_Mobile_Banking_2025.xlsx             ║  ║
║  ║ Size: 2.4 MB                                             ║  ║
║  ║ Sheets: 12                                                ║  ║
║  ║ [ Download Excel ]                                       ║  ║
║  ╚═══════════════════════════════════════════════════════════╝  ║
║                                                                   ║
║  ╔═══════════════════════════════════════════════════════════╗  ║
║  ║ SMARTSHEET                                     ✓ Success  ║  ║
║  ╠═══════════════════════════════════════════════════════════╣  ║
║  ║ Status: Sheet Created and Shared                          ║  ║
║  ║ Sheet Name: Mobile Banking Platform - Project Plan        ║  ║
║  ║ Sheet ID: 4534923850749828                                ║  ║
║  ║ Rows: 127  | Gantt: Enabled                               ║  ║
║  ║ Shared with: (Your SmartSheet Account)                    ║  ║
║  ║ [ Open in SmartSheet ] [ Copy URL ]                       ║  ║
║  ║ https://app.smartsheet.com/sheets/... (Clickable)         ║  ║
║  ╚═══════════════════════════════════════════════════════════╝  ║
║                                                                   ║
║  ╔═══════════════════════════════════════════════════════════╗  ║
║  ║ JIRA (Cloud)                                   ✓ Success  ║  ║
║  ╠═══════════════════════════════════════════════════════════╣  ║
║  ║ Status: Project Created with Full Backlog                 ║  ║
║  ║ Project: MOBANK (Mobile Banking)                          ║  ║
║  ║ Epics: 7  | Stories: 42  | Tasks: 156                     ║  ║
║  ║ Sprints: 6  | First Sprint: Jan 15 - Jan 29, 2025        ║  ║
║  ║ Board: Scrum Board (Active)                               ║  ║
║  ║ [ Open in Jira ] [ View Backlog ]                         ║  ║
║  ║ https://your-domain.atlassian.net/browse/MOBANK           ║  ║
║  ╚═══════════════════════════════════════════════════════════╝  ║
║                                                                   ║
║  ╔═══════════════════════════════════════════════════════════╗  ║
║  ║ AZURE DEVOPS                                   ✓ Success  ║  ║
║  ╠═══════════════════════════════════════════════════════════╣  ║
║  ║ Status: Project Created with Backlog                      ║  ║
║  ║ Project: Mobile Banking Platform                          ║  ║
║  ║ Epics: 7  | Features: 21  | User Stories: 84              ║  ║
║  ║ Tasks: 168  | Iterations: 6                               ║  ║
║  ║ [ Open in Azure DevOps ]                                  ║  ║
║  ║ https://dev.azure.com/org/project                         ║  ║
║  ╚═══════════════════════════════════════════════════════════╝  ║
║                                                                   ║
║  SUMMARY STATISTICS                                               ║
║  ┌───────────────────────────────────────────────────────────┐  ║
║  │ Total Items Created:                                      │  ║
║  │ • Excel Sheets: 12                                        │  ║
║  │ • SmartSheet Rows: 127                                    │  ║
║  │ • Jira Issues: 205 (7 Epic + 42 Story + 156 Task)        │  ║
║  │ • Azure DevOps Items: 280 (7 Epic + 21 Feat + 252 Item) │  ║
║  │                                                           │  ║
║  │ Resources Assigned:                                       │  ║
║  │ • Team Members: 12                                        │  ║
║  │ • Placeholder Assignments: 205                            │  ║
║  │ • Roles Defined: 8                                        │  ║
║  └───────────────────────────────────────────────────────────┘  ║
║                                                                   ║
║  ACTIONS                                                          ║
║  ┌─────────────────┬──────────────┬─────────────────────────┐   ║
║  │ [ Back to Home] │ [ View Report ] │ [ Create Another ]  │   ║
║  └─────────────────┴──────────────┴─────────────────────────┘   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

### 3.5 Error Handling Screen

**If Any Platform Fails:**

```
╔═══════════════════════════════════════════════════════════════════╗
║  ⚠ CREATION FAILURE - ROLLING BACK ALL PLATFORMS                 ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Status: ROLLBACK IN PROGRESS (3/4 platforms being cleaned)      ║
║                                                                   ║
║  Failed Platform:                                                 ║
║  ╔═══════════════════════════════════════════════════════════╗  ║
║  ║ JIRA - Authentication Failed                 ✗ FAILED    ║  ║
║  ╠═══════════════════════════════════════════════════════════╣  ║
║  ║ Error: Invalid API Token                                  ║  ║
║  ║ Details: The provided Jira API token has expired.         ║  ║
║  ║          Please regenerate from Settings > Security       ║  ║
║  ║ Time: 2025-01-15 14:32:18 UTC                            ║  ║
║  ║                                                           ║  ║
║  ║ [ Provide New Token ] [ Retry ]                           ║  ║
║  ╚═══════════════════════════════════════════════════════════╝  ║
║                                                                   ║
║  Rollback Status:                                                 ║
║  ├─ Excel: ✓ Removed from temporary storage                     ║
║  ├─ SmartSheet: ✓ Sheet deleted from your account               ║
║  ├─ Azure DevOps: ✓ Project removed                             ║
║  └─ Jira: (Not yet created - no rollback needed)                ║
║                                                                   ║
║  Options:                                                         ║
║  ┌─────────────────────────────────────────────────────────┐   ║
║  │ ☐ Retry with same credentials                          │   ║
║  │ ☐ Retry without Jira (Excel + SmartSheet + Azure)      │   ║
║  │ ☐ Update Jira token and retry all platforms            │   ║
║  │ ☐ Cancel and start over                                │   ║
║  └─────────────────────────────────────────────────────────┘   ║
║                                                                   ║
║  ┌──────────────────┬──────────────────────────────────────┐   ║
║  │ [ View Log ]     │ [ Back ] [ Retry Selected ] [Cancel] │   ║
║  └──────────────────┴──────────────────────────────────────┘   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## Backend API Design

### 4.1 REST API Endpoints

#### Platform Selection & Credential Management

```
POST /api/project/platforms/select
Description: User selects delivery platforms
Request:
{
  "project_id": 123,
  "platforms": ["excel", "smartsheet", "jira", "azure_devops"],
  "credentials": {
    "smartsheet": {
      "method": "api_token",
      "token": "encrypted_token_value",
      "save_for_future": true
    },
    "jira": {
      "method": "oauth",
      "token": "jwt_token",
      "instance_url": "https://company.atlassian.net"
    },
    "azure_devops": {
      "method": "pat",
      "token": "encrypted_pat",
      "organization_url": "https://dev.azure.com/company"
    }
  },
  "mapping_config": {
    "jira": {
      "project_key": "MOBANK",
      "board_type": "scrum",
      "hierarchy": {
        "phase": "epic",
        "deliverable": "story",
        "task": "task"
      },
      "field_mapping": {
        "owner": "assignee",
        "duration_days": "story_points"
      },
      "sprint_strategy": "auto_create_by_phase"
    },
    "azure_devops": {
      "project_name": "Mobile Banking Platform",
      "process_template": "Scrum",
      "hierarchy": {
        "phase": "epic",
        "deliverable": "feature",
        "task": "user_story"
      }
    }
  }
}

Response:
{
  "success": true,
  "request_id": "req_12345",
  "platforms": {
    "excel": {
      "status": "queued",
      "priority": 1
    },
    "smartsheet": {
      "status": "validating_credentials",
      "priority": 2
    },
    "jira": {
      "status": "validating_credentials",
      "priority": 3
    },
    "azure_devops": {
      "status": "queued",
      "priority": 4
    }
  },
  "estimated_time": 120 // seconds
}
```

#### Create Multi-Platform

```
POST /api/project/platforms/create
Description: Initiate multi-platform creation (atomic transaction)
Request:
{
  "project_id": 123,
  "delivery_request_id": "req_12345"
}

Response:
{
  "success": true,
  "transaction_id": "txn_67890",
  "status": "processing",
  "platforms": {
    "excel": { "status": "processing", "progress": 0 },
    "smartsheet": { "status": "processing", "progress": 0 },
    "jira": { "status": "processing", "progress": 0 },
    "azure_devops": { "status": "processing", "progress": 0 }
  },
  "webhook_url": "/api/project/platforms/status/txn_67890"
}
```

#### Get Platform Status

```
GET /api/project/platforms/status/:transaction_id
Description: Poll for multi-platform creation status
Response:
{
  "transaction_id": "txn_67890",
  "overall_status": "in_progress", // or "completed", "failed", "rolled_back"
  "platforms": {
    "excel": {
      "status": "completed",
      "progress": 100,
      "result": {
        "file_path": "/downloads/project_plan_123.xlsx",
        "file_size": 2400000,
        "sheets": 12
      }
    },
    "smartsheet": {
      "status": "completed",
      "progress": 100,
      "result": {
        "sheet_id": "4534923850749828",
        "sheet_name": "Mobile Banking Platform - Project Plan",
        "sheet_url": "https://app.smartsheet.com/sheets/...",
        "rows_created": 127,
        "gantt_enabled": true
      }
    },
    "jira": {
      "status": "failed",
      "progress": 45,
      "error": {
        "code": "AUTH_001",
        "message": "Invalid API token",
        "details": "The provided Jira API token has expired"
      }
    },
    "azure_devops": {
      "status": "pending",
      "progress": 0
    }
  },
  "rollback_status": "in_progress",
  "rollback_progress": {
    "excel": "completed",
    "smartsheet": "completed",
    "azure_devops": "pending"
  }
}
```

#### Retry Platform Creation

```
POST /api/project/platforms/retry
Description: Retry failed platform creation with new credentials
Request:
{
  "transaction_id": "txn_67890",
  "platforms": ["jira"],
  "credentials": {
    "jira": {
      "method": "api_token",
      "token": "new_encrypted_token",
      "instance_url": "https://company.atlassian.net"
    }
  }
}

Response:
{
  "transaction_id": "txn_67890",
  "retry_id": "retry_001",
  "status": "processing",
  "platforms_retrying": ["jira"]
}
```

#### Test Platform Connection

```
POST /api/project/platforms/test-connection
Description: Validate platform credentials before creation
Request:
{
  "platform": "jira",
  "credentials": {
    "method": "api_token",
    "token": "encrypted_token",
    "instance_url": "https://company.atlassian.net"
  }
}

Response:
{
  "platform": "jira",
  "connection_valid": true,
  "account_info": {
    "name": "John Doe",
    "email": "john@company.com",
    "organization": "Company Inc"
  },
  "available_resources": {
    "projects": 5,
    "boards": 3,
    "custom_fields": 12
  }
}
```

---

## Platform Integration Specifications

### 5.1 SmartSheet Integration

#### Overview
- **API Version**: SmartSheet API v2.0
- **Authentication**: OAuth 2.0 or API Token
- **Primary Objects**: Workspace, Sheet, Row, Column
- **Rate Limits**: 300 requests/minute

#### Sheet Structure

```
Sheet: Mobile Banking Platform - Project Plan
├─ Column 1: Task ID (Text)
├─ Column 2: Task Name (Text with indentation)
├─ Column 3: Phase (Drop-down: Initiation, Planning, Design, Development, Testing, Deployment, Closure)
├─ Column 4: Owner (Contact List)
├─ Column 5: Start Date (Date)
├─ Column 6: End Date (Date)
├─ Column 7: Duration (days) (Number)
├─ Column 8: % Complete (Percent)
├─ Column 9: Dependencies (Link to Row)
├─ Column 10: Status (Drop-down: Not Started, In Progress, At Risk, Completed)
├─ Column 11: Priority (Drop-down: Low, Medium, High, Critical)
├─ Column 12: Resource (Contact List - Placeholder)
├─ Column 13: Effort (Story Points - Number)
└─ Column 14: Notes (Text)

Parent-Child Hierarchy:
├─ Phase (Level 0 - Summary Row)
│  ├─ Deliverable (Level 1)
│  │  ├─ Task (Level 2)
│  │  │  └─ Subtask (Level 3)
│  │  └─ Task (Level 2)
│  └─ Deliverable (Level 1)
└─ Phase (Level 0 - Summary Row)

Formatting:
- Phase rows: Bold, Blue background, 12pt font
- Deliverable rows: Bold, Light blue background, 11pt font
- Task rows: Normal, White background, 10pt font
- Summary rows: Bold, Total all metrics

Dependencies:
- Use SmartSheet Link column to show task dependencies
- Gantt chart shows dependency lines automatically

Gantt View:
- Enable SmartSheet Gantt view for visual timeline
- Show milestones as diamonds
- Color code by phase
```

#### SmartSheet API Calls

```python
# 1. Create Workspace
POST /workspaces
{
  "name": "Mobile Banking Platform Projects"
}

# 2. Create Sheet
POST /sheets
{
  "name": "Mobile Banking Platform - Project Plan",
  "columns": [
    { "title": "Task ID", "type": "TEXT_NUMBER", "width": 60 },
    { "title": "Task Name", "type": "TEXT_NUMBER", "width": 200 },
    { "title": "Phase", "type": "PICKLIST", "options": [...] },
    { "title": "Owner", "type": "CONTACT_LIST" },
    { "title": "Start Date", "type": "DATE", "format": "YYYY-MM-DD" },
    { "title": "End Date", "type": "DATE", "format": "YYYY-MM-DD" },
    { "title": "Duration", "type": "DURATION", "format": "DAYS" },
    { "title": "% Complete", "type": "PERCENT", "width": 60 },
    { "title": "Dependencies", "type": "LINK_ROW" },
    { "title": "Status", "type": "PICKLIST", "options": ["Not Started", "In Progress", "At Risk", "Completed"] },
    { "title": "Priority", "type": "PICKLIST", "options": ["Low", "Medium", "High", "Critical"] },
    { "title": "Resource", "type": "CONTACT_LIST" },
    { "title": "Effort", "type": "TEXT_NUMBER", "width": 60 },
    { "title": "Notes", "type": "TEXT" }
  ]
}

# 3. Add Rows (Hierarchical)
POST /sheets/{sheetId}/rows
{
  "toBottom": true,
  "rows": [
    {
      "cells": [
        { "columnId": 1, "value": "PHASE-001" },
        { "columnId": 2, "value": "Initiation Phase" },
        { "columnId": 3, "value": "Initiation" },
        { "columnId": 5, "value": "2025-07-07" },
        { "columnId": 6, "value": "2025-07-28" },
        { "columnId": 7, "value": 21 },
        { "columnId": 8, "value": 0 }
      ]
    },
    {
      "parentId": 1,  // Parent to PHASE-001
      "cells": [
        { "columnId": 1, "value": "DEL-001" },
        { "columnId": 2, "value": "Project Charter" },
        { "columnId": 3, "value": "Initiation" },
        { "columnId": 4, "value": "john@company.com" },  // Owner
        { "columnId": 5, "value": "2025-07-07" },
        { "columnId": 6, "value": "2025-07-14" },
        { "columnId": 7, "value": 7 },
        { "columnId": 12, "value": "project-lead@company.com" }  // Placeholder
      ]
    }
  ]
}

# 4. Enable Gantt View
PUT /sheets/{sheetId}
{
  "ganttEnabled": true,
  "ganttStartColumnId": 5,  // Start Date
  "ganttEndColumnId": 6,    // End Date
  "ganttStatusColumnId": 10 // Status
}

# 5. Share Sheet
POST /sheets/{sheetId}/share
{
  "accessLevel": "EDITOR",
  "email": "team@company.com"
}
```

#### Data Mapping: Project Plan → SmartSheet

```
Project Plan Field         SmartSheet Column       Transformation
─────────────────────────────────────────────────────────────────
phase.name                 Task Name               Uppercase + bold
phase.start_date          Start Date              ISO format
phase.end_date            End Date                Calculated from start + duration
phase.duration_weeks * 7  Duration               Convert to days
deliverable.name          Task Name (child)       Title case
deliverable.owner         Owner (Contact)         Lookup by email
task.dependencies         Dependencies (Link)     Create row references
task.status               Status (PICKLIST)       Map to: Not Started, In Progress, At Risk, Completed
team_member.email         Resource (Contact)      Placeholder assignment
task.effort_estimate      Effort (Story Points)   Calculate from duration
```

### 5.2 Jira Integration

#### Overview
- **API Version**: Jira Cloud REST API v3
- **Authentication**: OAuth 2.0 or API Token
- **Primary Objects**: Project, Issue, Epic, Sprint
- **Rate Limits**: 1200 requests/hour

#### Project Structure

```
Jira Project: MOBANK (Mobile Banking)
├─ Epic 1: Initiation Phase
│  ├─ Story 1: Project Charter
│  │  ├─ Task 1.1: Develop charter document
│  │  ├─ Task 1.2: Identify stakeholders
│  │  └─ Task 1.3: Get sign-off
│  └─ Story 2: Stakeholder Analysis
│     ├─ Task 2.1: Identify stakeholder groups
│     └─ Task 2.2: Document needs & expectations
├─ Epic 2: Planning Phase
│  ├─ Story 3: Project Plan
│  │  ├─ Task 3.1: Develop project schedule
│  │  ├─ Task 3.2: Resource planning
│  │  └─ Task 3.3: Budget allocation
│  ├─ Story 4: Resource Plan
│  │  ├─ Task 4.1: Team structure design
│  │  └─ Task 4.2: Skills assessment
│  └─ Story 5: Risk Register
│     ├─ Task 5.1: Risk identification
│     └─ Task 5.2: Mitigation planning

Sprints:
├─ Sprint 1: Initiation (Jul 7 - Jul 21, 2025)
├─ Sprint 2: Planning (Jul 22 - Aug 4, 2025)
├─ Sprint 3: Design (Aug 5 - Aug 25, 2025)
├─ Sprint 4: Development (Aug 26 - Oct 6, 2025)
├─ Sprint 5: Testing (Oct 7 - Oct 27, 2025)
└─ Sprint 6: Deployment (Oct 28 - Nov 10, 2025)

Fields:
- Summary: Task name / epic name
- Description: Task description with acceptance criteria
- Story Points: Auto-calculated from duration
- Assignee: Placeholder (PM Name <To Be Assigned>)
- Labels: [phase-name, project-type, risk-level]
- Custom Fields:
  - Project Phase (Drop-down)
  - Duration (Days) (Number)
  - Resource Type (Drop-down: Engineer, Designer, PM, QA)
  - Risk Level (Drop-down: Low, Medium, High, Critical)
  - Dependencies (Link Issues)
```

#### Jira API Calls

```python
# 1. Create Project
POST /rest/api/3/projects
{
  "key": "MOBANK",
  "name": "Mobile Banking Platform",
  "projectTypeKey": "software",
  "projectTemplateKey": "com.pyatilabs.jira-cloud-scrum",
  "description": "Mobile Banking Application Development Project"
}

# 2. Create Epic
POST /rest/api/3/issues
{
  "fields": {
    "project": { "key": "MOBANK" },
    "summary": "Initiation Phase",
    "description": "Project initiation and setup activities",
    "issuetype": { "name": "Epic" },
    "labels": ["phase-initiation", "mobile-banking"],
    "customfield_10001": "Initiation"  // Project Phase
  }
}

# 3. Create Story under Epic
POST /rest/api/3/issues
{
  "fields": {
    "project": { "key": "MOBANK" },
    "parent": { "key": "MOBANK-1" },  // Parent Epic
    "summary": "Project Charter",
    "description": "Develop and finalize project charter document\n\nAcceptance Criteria:\n- Charter document complete\n- Stakeholder sign-off obtained\n- Goals and objectives clear",
    "issuetype": { "name": "Story" },
    "customfield_10002": 7,  // Duration (days)
    "customfield_10003": "Initiation",
    "customfield_10004": "Medium",  // Risk Level
    "labels": ["project-charter", "deliverable"]
  }
}

# 4. Create Task under Story
POST /rest/api/3/issues
{
  "fields": {
    "project": { "key": "MOBANK" },
    "parent": { "key": "MOBANK-2" },  // Parent Story
    "summary": "Develop charter document",
    "description": "Create project charter with all required sections",
    "issuetype": { "name": "Task" },
    "assignee": { "id": "placeholder@company.com" },
    "customfield_10002": 3,  // Duration (days)
    "customfield_10005": "PM"  // Resource Type
  }
}

# 5. Create Sprint
POST /rest/api/3/board/{boardId}/sprint
{
  "name": "Sprint 1 - Initiation",
  "startDate": "2025-07-07T00:00:00Z",
  "endDate": "2025-07-21T23:59:59Z"
}

# 6. Move Issue to Sprint
POST /rest/api/3/sprint/{sprintId}/issue
{
  "issues": ["MOBANK-2", "MOBANK-3", "MOBANK-4"]
}

# 7. Create Issue Link (Dependencies)
POST /rest/api/3/issueLink
{
  "type": { "name": "depends on" },
  "inwardIssue": { "key": "MOBANK-5" },
  "outwardIssue": { "key": "MOBANK-2" }
}

# 8. Estimate Story Points
PUT /rest/api/3/issues/{issueKey}
{
  "fields": {
    "customfield_10000": 5  // Story Points (calculated from duration)
  }
}
```

#### Data Mapping: Project Plan → Jira

```
Project Plan Field         Jira Field              Mapping Rule
─────────────────────────────────────────────────────────────────
phase                      Epic                    Create Epic for each phase
deliverable                Story                   Create Story under Epic
task                       Task/Subtask            Create Task under Story
phase.start_date          Sprint Start Date       Align sprints to phases
task.owner                Assignee                Create "placeholder" account + task
task.duration_weeks * 7   Story Points            Calculate: duration / 7 (rounded)
deliverable.description   Story Description       Include acceptance criteria
dependencies              Issue Link              Create "depends on" links
task.status               Status                  Map to: To Do, In Progress, Done
team_member.role          Custom Field            Map to: Engineer, Designer, PM, QA
```

### 5.3 Azure DevOps Integration

#### Overview
- **API Version**: Azure DevOps REST API v7.1
- **Authentication**: PAT (Personal Access Token) or OAuth
- **Primary Objects**: Project, Work Item, Epic, Feature, User Story
- **Rate Limits**: Unlimited (throttled by service)

#### Project Structure

```
Azure DevOps Project: Mobile Banking Platform
├─ Backlog
│  └─ Epic 1: Initiation Phase
│     ├─ Feature 1: Project Governance
│     │  ├─ User Story 1: Project Charter
│     │  │  ├─ Task 1.1: Develop charter document
│     │  │  ├─ Task 1.2: Identify stakeholders
│     │  │  └─ Task 1.3: Get sign-off
│     │  └─ User Story 2: Stakeholder Analysis
│     │     ├─ Task 2.1: Identify stakeholder groups
│     │     └─ Task 2.2: Document needs & expectations
│     └─ Feature 2: Planning & Setup
│        └─ User Story 3: Resource Planning
│           ├─ Task 3.1: Create team structure
│           └─ Task 3.2: Allocate resources

├─ Iterations (Sprints)
│  ├─ Sprint 1: Initiation (Jul 7-21, 2025)
│  ├─ Sprint 2: Planning (Jul 22-Aug 4, 2025)
│  ├─ Sprint 3: Design (Aug 5-25, 2025)
│  ├─ Sprint 4: Development (Aug 26-Oct 6, 2025)
│  ├─ Sprint 5: Testing (Oct 7-27, 2025)
│  └─ Sprint 6: Deployment (Oct 28-Nov 10, 2025)

Areas:
├─ Initiation Phase
├─ Planning Phase
├─ Design Phase
├─ Development Phase
├─ Testing Phase
├─ Deployment Phase
└─ Closure Phase

Work Item Types:
- Epic: Major phase
- Feature: Deliverable group
- User Story: Individual deliverable
- Task: Work item
- Bug: Issue tracking
- Test Case: QA items
```

#### Azure DevOps API Calls

```python
# 1. Create Project
POST https://dev.azure.com/{organization}/_apis/projects
{
  "name": "Mobile Banking Platform",
  "description": "Mobile Banking Application Development Project",
  "capabilities": {
    "versioncontrol": {
      "sourceControlType": "Git"
    },
    "processTemplate": {
      "templateTypeId": "adcc42ab-9882-485e-a3ed-7678f01f66bc"  // Scrum
    }
  }
}

# 2. Create Epic
POST https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Epic
{
  "fields": {
    "System.Title": "Initiation Phase",
    "System.Description": "Project initiation and setup activities",
    "System.AreaPath": "Mobile Banking Platform\\Initiation Phase",
    "System.IterationPath": "Mobile Banking Platform\\Sprint 1",
    "Custom.ProjectPhase": "Initiation",
    "Custom.Duration": 21,
    "Custom.RiskLevel": "Medium"
  }
}

# 3. Create Feature
POST https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Feature
{
  "fields": {
    "System.Title": "Project Governance",
    "System.Description": "Establish project governance framework",
    "System.AreaPath": "Mobile Banking Platform\\Initiation Phase",
    "System.IterationPath": "Mobile Banking Platform\\Sprint 1",
    "System.Tags": "deliverable;governance",
    "Custom.Duration": 10,
    "Microsoft.VSTS.Scheduling.StoryPoints": 5
  },
  "relations": [
    {
      "rel": "System.LinkTypes.Hierarchy-reverse",
      "url": "https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/1"  // Parent Epic
    }
  ]
}

# 4. Create User Story
POST https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$User%20Story
{
  "fields": {
    "System.Title": "Project Charter",
    "System.Description": "Develop and finalize project charter document\n\nAcceptance Criteria:\n- Charter document complete\n- Stakeholder sign-off obtained",
    "System.AreaPath": "Mobile Banking Platform\\Initiation Phase",
    "System.IterationPath": "Mobile Banking Platform\\Sprint 1",
    "Microsoft.VSTS.Scheduling.StoryPoints": 3,
    "System.AssignedTo": "ProjectLead <To Be Assigned>"
  },
  "relations": [
    {
      "rel": "System.LinkTypes.Hierarchy-reverse",
      "url": "https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/2"  // Parent Feature
    }
  ]
}

# 5. Create Task
POST https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Task
{
  "fields": {
    "System.Title": "Develop charter document",
    "System.Description": "Create project charter with all required sections",
    "System.AreaPath": "Mobile Banking Platform\\Initiation Phase",
    "System.IterationPath": "Mobile Banking Platform\\Sprint 1",
    "System.AssignedTo": "ProjectManager <To Be Assigned>",
    "Microsoft.VSTS.Scheduling.RemainingWork": 8  // hours
  },
  "relations": [
    {
      "rel": "System.LinkTypes.Hierarchy-reverse",
      "url": "https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/3"  // Parent Story
    }
  ]
}

# 6. Create Iteration (Sprint)
POST https://dev.azure.com/{organization}/{project}/_apis/wit/classificationnodes/Iterations
{
  "name": "Sprint 1 - Initiation",
  "attributes": {
    "startDate": "2025-07-07T00:00:00Z",
    "finishDate": "2025-07-21T23:59:59Z"
  }
}

# 7. Add Work Item to Iteration
PATCH https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/3
{
  "fields": {
    "System.IterationPath": "Mobile Banking Platform\\Sprint 1"
  }
}

# 8. Create Area
POST https://dev.azure.com/{organization}/{project}/_apis/wit/classificationnodes/Areas
{
  "name": "Initiation Phase"
}

# 9. Create Link (Dependency)
POST https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/3/relations
{
  "rel": "System.LinkTypes.Dependency-forward",
  "url": "https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/2",
  "attributes": {
    "comment": "Feature development depends on story completion"
  }
}
```

#### Data Mapping: Project Plan → Azure DevOps

```
Project Plan Field         Azure DevOps Field      Mapping Rule
─────────────────────────────────────────────────────────────────
phase                      Epic                    Create Epic for each phase
deliverable                Feature                 Group by deliverable type
task                       User Story/Task         Create under Feature
phase.start_date          Iteration Start Date    Align iterations to phases
task.owner                AssignedTo              Create "placeholder" assignment
task.duration_weeks * 7   StoryPoints             Calculate: duration / 7
task.duration_days        RemainingWork           Calculate: duration * 8 hours
phase.name                AreaPath                Create area for each phase
dependencies              Link Relation           Create "depends on" links
task.status               State                   Map to: New, Active, Resolved, Closed
```

---

## Data Mapping Models

### 6.1 Universal Project Plan Schema

```javascript
// Generated by Project Planning Agent
{
  "project": {
    "id": "proj_123",
    "name": "Mobile Banking Platform",
    "client_name": "ABC Bank",
    "project_type": "Mobile Application Development",
    "start_date": "2025-07-07",
    "duration_weeks": 26,
    "team_size": 12,
    "budget": 500000,
    "delivery_model": "Fixed Price"
  },

  "wbs": {
    "phases": [
      {
        "id": "phase_001",
        "name": "Initiation",
        "start_date": "2025-07-07",
        "end_date": "2025-07-28",
        "duration_weeks": 3,
        "status": "Not Started",
        "priority": "High",
        "owner": "john.doe@company.com",
        "deliverables": [
          {
            "id": "del_001",
            "name": "Project Charter",
            "description": "Formalize project objectives, scope, and governance",
            "start_date": "2025-07-07",
            "end_date": "2025-07-14",
            "duration_weeks": 1,
            "owner": "john.doe@company.com",
            "acceptance_criteria": [
              "Charter document complete",
              "Stakeholder sign-off obtained",
              "Goals and objectives clear"
            ],
            "tasks": [
              {
                "id": "task_001",
                "name": "Develop charter document",
                "description": "Create comprehensive project charter",
                "start_date": "2025-07-07",
                "end_date": "2025-07-10",
                "duration_days": 3,
                "owner": "john.doe@company.com",
                "effort_estimate": 24,  // hours
                "priority": "High",
                "status": "Not Started",
                "dependencies": [],
                "assigned_to_role": "Project Manager",
                "resource_allocation": 100  // percentage
              },
              {
                "id": "task_002",
                "name": "Identify stakeholders",
                "description": "Identify all project stakeholders",
                "start_date": "2025-07-10",
                "end_date": "2025-07-12",
                "duration_days": 2,
                "owner": "john.doe@company.com",
                "effort_estimate": 16,
                "priority": "High",
                "status": "Not Started",
                "dependencies": ["task_001"],
                "assigned_to_role": "Project Manager",
                "resource_allocation": 100
              }
            ]
          }
        ]
      }
    ]
  },

  "resources": {
    "team_members": [
      {
        "id": "tm_001",
        "name": "John Doe",
        "email": "john.doe@company.com",
        "role": "Project Manager",
        "allocation": 100,
        "start_date": "2025-07-07",
        "end_date": "2027-01-05"
      }
    ],
    "roles_defined": [
      {
        "id": "role_001",
        "name": "Project Manager",
        "count": 1,
        "responsibilities": ["Project leadership", "Stakeholder management", "Schedule management"],
        "required_skills": ["Project Management", "Communication", "Leadership"]
      },
      {
        "id": "role_002",
        "name": "Technical Architect",
        "count": 2,
        "responsibilities": ["System design", "Technology selection", "Technical guidelines"],
        "required_skills": ["Architecture", "System Design", "Mobile Development"]
      }
    ]
  },

  "risks": [
    {
      "id": "risk_001",
      "title": "Scope Creep",
      "description": "Uncontrolled expansion of project scope",
      "probability": "High",
      "impact": "High",
      "severity": "Critical",
      "mitigation": "Strict change management process",
      "owner": "john.doe@company.com",
      "identified_date": "2025-01-15",
      "status": "Identified"
    }
  ],

  "dependencies": [
    {
      "id": "dep_001",
      "from_task": "task_001",
      "to_task": "task_002",
      "type": "Finish to Start",
      "lag_days": 0
    }
  ],

  "milestones": [
    {
      "id": "ms_001",
      "name": "Requirements Complete",
      "target_date": "2025-08-18",
      "phase": "Planning",
      "status": "Planned",
      "priority": "High"
    }
  ]
}
```

### 6.2 Platform-Specific Transformers

```python
# Transformer Pattern for Each Platform

class ProjectPlanToExcelTransformer:
    def transform(self, project_plan: dict) -> dict:
        """Transform universal schema to Excel format"""
        return {
            "sheets": {
                "Home": self._create_home_sheet(project_plan),
                "Executive_Dashboard": self._create_dashboard(project_plan),
                "Project_Plan": self._create_project_plan(project_plan),
                "Gantt_Chart": self._create_gantt(project_plan),
                "RAID_Register": self._create_raid(project_plan),
                "Resources": self._create_resources(project_plan),
                ...
            }
        }

class ProjectPlanToSmartSheetTransformer:
    def transform(self, project_plan: dict) -> dict:
        """Transform universal schema to SmartSheet format"""
        return {
            "sheet": {
                "name": f"{project_plan['project']['name']} - Project Plan",
                "columns": self._create_columns(),
                "rows": self._create_hierarchical_rows(project_plan),
                "gantt_config": {
                    "enabled": True,
                    "start_date_column_id": ...,
                    "end_date_column_id": ...,
                    "duration_column_id": ...
                }
            }
        }

class ProjectPlanToJiraTransformer:
    def transform(self, project_plan: dict) -> dict:
        """Transform universal schema to Jira format"""
        return {
            "project": {
                "key": self._generate_key(project_plan),
                "name": project_plan['project']['name'],
                "template": "com.pyatilabs.jira-cloud-scrum"
            },
            "epics": self._create_epics(project_plan),
            "stories": self._create_stories(project_plan),
            "tasks": self._create_tasks(project_plan),
            "sprints": self._create_sprints(project_plan),
            "links": self._create_links(project_plan)
        }

class ProjectPlanToAzureDevOpsTransformer:
    def transform(self, project_plan: dict) -> dict:
        """Transform universal schema to Azure DevOps format"""
        return {
            "project": {
                "name": project_plan['project']['name'],
                "process_template": "Scrum"
            },
            "epics": self._create_epics(project_plan),
            "features": self._create_features(project_plan),
            "user_stories": self._create_user_stories(project_plan),
            "tasks": self._create_tasks(project_plan),
            "iterations": self._create_iterations(project_plan),
            "areas": self._create_areas(project_plan)
        }
```

---

## Agent Workflow Updates

### 7.1 Updated Multi-Agent Orchestration

```
┌────────────────────────────────────────────────────────────────┐
│                    DOCUMENT UPLOAD                              │
│              (User uploads SOW + BRD + Requirements)             │
└────────────────────────┬─────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│      DOCUMENT ANALYSIS AGENT (Claude AI)                         │
│  ├─ Extract project information                                  │
│  ├─ Identify project type                                        │
│  ├─ Extract scope and deliverables                               │
│  └─ Identify risks and assumptions                               │
└────────────────────────┬─────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│      PROJECT TYPE DETECTION AGENT                                │
│  ├─ Classify project (Agile/Waterfall/Hybrid)                   │
│  ├─ Determine project complexity                                 │
│  └─ Select appropriate templates                                 │
└────────────────────────┬─────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│      PROJECT PLANNING AGENT                                      │
│  ├─ Generate WBS (Work Breakdown Structure)                      │
│  ├─ Create project phases                                        │
│  ├─ Define deliverables                                          │
│  ├─ Identify tasks and subtasks                                  │
│  └─ Calculate timeline                                           │
└────────────────────────┬─────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│      RISK & RESOURCE AGENT                                       │
│  ├─ Assess project risks                                         │
│  ├─ Create risk mitigation strategies                            │
│  ├─ Calculate resource requirements                              │
│  ├─ Define roles and skills                                      │
│  └─ Estimate effort (story points / days)                        │
└────────────────────────┬─────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│      PROJECT VALIDATION AGENT                                    │
│  ├─ Validate WBS completeness                                    │
│  ├─ Verify timeline feasibility                                  │
│  ├─ Check resource availability                                  │
│  ├─ Validate dependencies                                        │
│  └─ Generate project metrics                                     │
└────────────────────────┬─────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│   DISPLAY PLATFORM SELECTION UI (NEW)                            │
│  ├─ Show platform options                                        │
│  ├─ Collect platform selections                                  │
│  ├─ Collect platform credentials                                 │
│  └─ Show mapping configuration UI                                │
└────────────────────────┬─────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│   CREDENTIAL VALIDATION AGENT (NEW)                              │
│  ├─ Validate API tokens                                          │
│  ├─ Test OAuth flows                                             │
│  ├─ Verify platform connectivity                                 │
│  └─ Encrypt and store credentials                                │
└────────────────────────┬─────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│   DELIVERY PLATFORM AGENT (NEW - MAIN ORCHESTRATOR)              │
│  ├─ Parse universal project schema                               │
│  ├─ Apply user-provided mapping config                           │
│  ├─ Spawn parallel platform creators                             │
│  ├─ Monitor creation status                                      │
│  ├─ Handle partial failures with rollback                        │
│  └─ Consolidate results                                          │
│                                                                  │
│  ├─ Excel Creator (Non-blocking)                                │
│  │  ├─ Transform to Excel schema                                 │
│  │  ├─ Generate workbook                                         │
│  │  └─ Return download link                                      │
│  │                                                               │
│  ├─ SmartSheet Creator (Parallel with retry)                     │
│  │  ├─ Transform to SmartSheet schema                            │
│  │  ├─ API calls to create sheet                                 │
│  │  ├─ Add rows with hierarchy                                   │
│  │  ├─ Enable Gantt view                                         │
│  │  └─ Return sheet URL                                          │
│  │                                                               │
│  ├─ Jira Creator (Parallel with retry)                           │
│  │  ├─ Transform to Jira schema                                  │
│  │  ├─ Create project                                            │
│  │  ├─ Create epics, stories, tasks                              │
│  │  ├─ Create sprints                                            │
│  │  ├─ Link dependencies                                         │
│  │  └─ Return project URL                                        │
│  │                                                               │
│  └─ Azure DevOps Creator (Parallel with retry)                   │
│     ├─ Transform to Azure DevOps schema                          │
│     ├─ Create project                                            │
│     ├─ Create epics, features, stories, tasks                    │
│     ├─ Create iterations (sprints)                               │
│     ├─ Create areas                                              │
│     └─ Return project URL                                        │
│                                                                  │
│  TRANSACTION MANAGEMENT:                                         │
│  ├─ Start transaction                                            │
│  ├─ Execute all platforms concurrently                           │
│  ├─ If ANY fails:                                                │
│  │  ├─ Stop remaining platforms                                  │
│  │  ├─ Rollback completed platforms                              │
│  │  ├─ Return detailed failure report                            │
│  │  └─ Allow retry with fixes                                    │
│  └─ If ALL succeed:                                              │
│     ├─ Mark transaction complete                                 │
│     └─ Return consolidated status                                │
└────────────────────────┬─────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│      DISPLAY STATUS DASHBOARD (NEW)                              │
│  ├─ Show all platform results                                    │
│  ├─ Display direct links                                         │
│  ├─ Show statistics                                              │
│  └─ Allow next actions (download, open, etc.)                    │
└────────────────────────────────────────────────────────────────────┘
```

### 7.2 Delivery Platform Agent (Pseudocode)

```python
class DeliveryPlatformAgent:
    """
    Orchestrates multi-platform project plan creation
    Handles atomic transactions with rollback
    """

    def __init__(self, project_plan, platform_selections, credentials, mapping_config):
        self.project_plan = project_plan
        self.platforms = platform_selections
        self.credentials = credentials
        self.mapping_config = mapping_config
        self.transaction_id = generate_transaction_id()
        self.results = {}
        self.transaction_log = []

    async def execute(self):
        """Execute multi-platform creation atomically"""
        try:
            # 1. Validate all credentials upfront
            await self._validate_all_credentials()
            self._log("All credentials validated")

            # 2. Transform project plan for each platform
            transformed_data = await self._transform_for_all_platforms()
            self._log("Project plan transformed for all platforms")

            # 3. Execute platform creators in parallel
            tasks = []
            for platform in self.platforms:
                if platform == "excel":
                    task = self._create_excel(transformed_data["excel"])
                elif platform == "smartsheet":
                    task = self._create_smartsheet(transformed_data["smartsheet"])
                elif platform == "jira":
                    task = self._create_jira(transformed_data["jira"])
                elif platform == "azure_devops":
                    task = self._create_azure_devops(transformed_data["azure_devops"])

                tasks.append(task)

            # 4. Monitor results
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # 5. Check for failures
            failed_platforms = []
            for platform, result in zip(self.platforms, results):
                if isinstance(result, Exception):
                    failed_platforms.append(platform)
                    self.results[platform] = {
                        "status": "failed",
                        "error": str(result)
                    }
                else:
                    self.results[platform] = result
                    self._log(f"{platform}: Success")

            # 6. If ANY failed, rollback ALL
            if failed_platforms:
                await self._rollback_all()
                raise PlatformCreationError(
                    f"Creation failed on platforms: {failed_platforms}. All platforms rolled back."
                )

            # 7. Mark transaction complete
            self._log("Transaction completed successfully")
            return self._build_status_response()

        except Exception as e:
            self._log(f"Error: {str(e)}")
            await self._rollback_all()
            raise

    async def _validate_all_credentials(self):
        """Validate credentials for all selected platforms"""
        for platform in self.platforms:
            if platform == "excel":
                # No validation needed for local Excel
                continue
            
            creds = self.credentials.get(platform)
            connector = self._get_connector(platform)
            await connector.test_connection(creds)

    async def _transform_for_all_platforms(self):
        """Transform universal schema to platform-specific formats"""
        transformers = {
            "excel": ProjectPlanToExcelTransformer(),
            "smartsheet": ProjectPlanToSmartSheetTransformer(),
            "jira": ProjectPlanToJiraTransformer(),
            "azure_devops": ProjectPlanToAzureDevOpsTransformer()
        }

        transformed = {}
        for platform in self.platforms:
            transformer = transformers[platform]
            config = self.mapping_config.get(platform, {})
            transformed[platform] = transformer.transform(self.project_plan, config)

        return transformed

    async def _create_excel(self, excel_data):
        """Create Excel workbook"""
        creator = ExcelCreator()
        file_path = await creator.create(excel_data, self.project_plan)
        return {
            "status": "completed",
            "platform": "excel",
            "file_path": file_path,
            "file_size": get_file_size(file_path),
            "sheets": len(excel_data["sheets"])
        }

    async def _create_smartsheet(self, smartsheet_data):
        """Create SmartSheet project"""
        creator = SmartSheetCreator(self.credentials["smartsheet"])
        sheet_id = await creator.create(smartsheet_data)
        return {
            "status": "completed",
            "platform": "smartsheet",
            "sheet_id": sheet_id,
            "sheet_url": f"https://app.smartsheet.com/sheets/{sheet_id}",
            "rows_created": smartsheet_data["row_count"]
        }

    async def _create_jira(self, jira_data):
        """Create Jira project"""
        creator = JiraCreator(self.credentials["jira"])
        project_key = await creator.create(jira_data)
        return {
            "status": "completed",
            "platform": "jira",
            "project_key": project_key,
            "project_url": f"{self.credentials['jira']['instance_url']}/browse/{project_key}",
            "epics_created": len(jira_data["epics"]),
            "stories_created": len(jira_data["stories"]),
            "tasks_created": len(jira_data["tasks"])
        }

    async def _create_azure_devops(self, devops_data):
        """Create Azure DevOps project"""
        creator = AzureDevOpsCreator(self.credentials["azure_devops"])
        project_id = await creator.create(devops_data)
        return {
            "status": "completed",
            "platform": "azure_devops",
            "project_id": project_id,
            "project_url": f"{self.credentials['azure_devops']['instance_url']}/_web/tfs",
            "epics_created": len(devops_data["epics"]),
            "features_created": len(devops_data["features"]),
            "items_created": len(devops_data["work_items"])
        }

    async def _rollback_all(self):
        """Rollback all successfully created platforms"""
        self._log("Starting rollback...")

        for platform, result in self.results.items():
            if result.get("status") != "completed":
                continue

            try:
                if platform == "excel":
                    # Delete temporary file
                    delete_file(result["file_path"])
                elif platform == "smartsheet":
                    connector = SmartSheetConnector(self.credentials["smartsheet"])
                    await connector.delete_sheet(result["sheet_id"])
                elif platform == "jira":
                    connector = JiraConnector(self.credentials["jira"])
                    await connector.delete_project(result["project_key"])
                elif platform == "azure_devops":
                    connector = AzureDevOpsConnector(self.credentials["azure_devops"])
                    await connector.delete_project(result["project_id"])

                self._log(f"{platform}: Rollback complete")
                result["rollback_status"] = "completed"

            except Exception as e:
                self._log(f"{platform}: Rollback failed - {str(e)}")
                result["rollback_status"] = "failed"
                result["rollback_error"] = str(e)

    def _log(self, message):
        """Log transaction event"""
        self.transaction_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "message": message
        })

    def _build_status_response(self):
        """Build consolidated status response"""
        return {
            "transaction_id": self.transaction_id,
            "overall_status": "completed",
            "platforms": self.results,
            "transaction_log": self.transaction_log
        }
```

---

## Database Schema Updates

### 8.1 New Tables

```sql
-- Store platform selections and configurations
CREATE TABLE platform_delivery_configs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id INTEGER NOT NULL REFERENCES projects(id),
    platforms JSON NOT NULL,  -- ["excel", "smartsheet", "jira", "azure_devops"]
    mapping_config JSON,  -- Platform-specific mapping rules
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Store encrypted platform credentials
CREATE TABLE platform_credentials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id INTEGER NOT NULL,
    platform VARCHAR(50) NOT NULL,  -- "smartsheet", "jira", "azure_devops"
    credential_type VARCHAR(20) NOT NULL,  -- "api_token", "oauth", "pat"
    encrypted_token BYTEA NOT NULL,
    encryption_key_id VARCHAR(100),
    instance_url VARCHAR(255),  -- For Jira, Azure DevOps
    organization VARCHAR(255),  -- For Azure DevOps
    is_active BOOLEAN DEFAULT true,
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, platform)
);

-- Track platform creation transactions
CREATE TABLE platform_creation_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id INTEGER NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,  -- "create", "retry", "rollback"
    platforms JSON NOT NULL,
    status VARCHAR(20) NOT NULL,  -- "pending", "processing", "completed", "failed", "rolled_back"
    result JSON,  -- Contains results for each platform
    error_details JSON,  -- Error information if failed
    transaction_log JSONB,  -- Complete transaction audit log
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Map generated WBS to platform-specific identifiers
CREATE TABLE wbs_platform_mapping (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id INTEGER NOT NULL,
    transaction_id UUID NOT NULL REFERENCES platform_creation_transactions(id),
    wbs_element_id VARCHAR(100) NOT NULL,  -- Original WBS element ID
    wbs_type VARCHAR(20) NOT NULL,  -- "phase", "deliverable", "task", "subtask"
    platform VARCHAR(50) NOT NULL,
    platform_item_id VARCHAR(255) NOT NULL,  -- Jira issue key, SmartSheet row ID, etc.
    platform_url VARCHAR(512),  -- Direct link to platform item
    mapping_metadata JSON,  -- Platform-specific metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    UNIQUE(transaction_id, wbs_element_id, platform)
);

-- Platform API usage tracking and rate limits
CREATE TABLE platform_api_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_id UUID NOT NULL REFERENCES platform_creation_transactions(id),
    platform VARCHAR(50) NOT NULL,
    api_endpoint VARCHAR(255),
    method VARCHAR(10),
    status_code INTEGER,
    response_time_ms INTEGER,
    tokens_used INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES platform_creation_transactions(id)
);
```

### 8.2 Index Optimizations

```sql
CREATE INDEX idx_platform_credentials_user_platform 
ON platform_credentials(user_id, platform);

CREATE INDEX idx_platform_creation_project 
ON platform_creation_transactions(project_id);

CREATE INDEX idx_platform_creation_status 
ON platform_creation_transactions(status);

CREATE INDEX idx_wbs_platform_mapping_project_transaction 
ON wbs_platform_mapping(project_id, transaction_id);

CREATE INDEX idx_api_usage_transaction 
ON platform_api_usage(transaction_id);
```

---

## Security & Authentication

### 9.1 Credential Storage

```
Encryption Architecture:
─────────────────────────

1. Credential Input (from user form)
   ↓
2. Encrypt with AWS KMS (or Vault)
   - Master key rotation every 90 days
   - Key derivation: PBKDF2 + HSM
   - Algorithm: AES-256-GCM
   ↓
3. Store encrypted blob in database
   - Separate encryption keys per user
   - Audit log every access
   - TTL on tokens (90 days default)
   ↓
4. Retrieve & Decrypt (when needed)
   - User must be authenticated
   - IP whitelist check (optional)
   - Log audit trail
   ↓
5. Use temporarily
   - In-memory only
   - Never logged
   - Deleted after use
```

### 9.2 OAuth Flow

```
SmartSheet OAuth:
┌─────────────────────────────────────────────┐
│ User clicks "Authenticate with SmartSheet" │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ Redirect to SmartSheet consent screen       │
│ /auth/smartsheet/authorize?                 │
│   client_id=...                             │
│   redirect_uri=https://app.com/auth/callback
│   scope=ADMIN_SHEETS,WRITE_SHEETS           │
└────────────────┬────────────────────────────┘
                 │
         [User grants permission]
                 │
┌────────────────▼────────────────────────────┐
│ SmartSheet redirects with auth code         │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ Backend exchanges code for access token     │
│ POST https://smartsheet.com/token           │
│   grant_type=authorization_code             │
│   code=...                                   │
│   client_id=...                             │
│   client_secret=... (server-side)           │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ Store encrypted token in database           │
│ Redirect user to platform selection UI      │
└─────────────────────────────────────────────┘

Token Refresh:
- SmartSheet tokens expire in 14 days
- Use refresh_token to get new access_token
- Store both in database with expiry
- Refresh automatically when < 24hrs to expiry
```

### 9.3 API Token Security

```
API Token Storage:
─────────────────

1. User provides token (SmartSheet, Jira API Token, Azure PAT)
   
2. Validate token format
   - SmartSheet: 36-character alphanumeric
   - Jira: Base64-encoded email:token
   - Azure: 52-character alphanumeric PAT
   
3. Test token validity
   - Call platform's whoami/me endpoint
   - Verify permissions
   - Check expiry date
   
4. Encrypt token
   - Use user-specific key
   - Add timestamp to ciphertext
   - Store hash for rotation detection
   
5. Store securely
   - Separate column: platform_credentials
   - Never in logs
   - Never in error messages
   
6. Access control
   - Only owner can view/delete
   - Audit log all uses
   - Admin can revoke all
```

---

## Error Handling & Rollback Strategy

### 10.1 Failure Scenarios

```
Scenario 1: Credential Validation Fails
─────────────────────────────────────────
Before creation starts:
  └─ User must provide valid credentials
  └─ Test connection before proceeding
  └─ Block creation if validation fails
  └─ Return clear error message

Scenario 2: Single Platform Fails During Creation
───────────────────────────────────────────────────
During parallel creation:
  ├─ Excel: Creating workbook (no cleanup needed)
  ├─ SmartSheet: FAILED - API error
  ├─ Jira: In progress...
  ├─ Azure DevOps: Queued
  
Action taken:
  ├─ Cancel pending platforms (Jira, Azure DevOps)
  ├─ Rollback completed platforms
  │  ├─ Excel: Delete file from temp storage
  │  ├─ Jira: Delete project (if created)
  │  └─ Azure DevOps: Delete project (if created)
  ├─ Abort transaction
  └─ Return failure report with retry options

Scenario 3: Rollback Itself Fails
──────────────────────────────────
If rollback cannot delete a resource:
  ├─ Mark rollback as FAILED
  ├─ Log all failure details
  ├─ Alert operations team (webhook)
  ├─ Store orphaned resource IDs
  └─ Allow manual cleanup + retry

Scenario 4: Partial Rollback
──────────────────────────────
SmartSheet deletion fails, but others succeed:
  ├─ Continue rolling back other platforms
  ├─ Track which platforms failed rollback
  ├─ Return detailed status:
  │  {
  │    "status": "rolled_back_with_errors",
  │    "rollback": {
  │      "excel": "success",
  │      "smartsheet": "failed - cannot delete sheet 123",
  │      "jira": "success",
  │      "azure": "success"
  │    }
  │  }
  └─ Alert manual cleanup needed for SmartSheet

Scenario 5: Network Timeout
─────────────────────────────
Connection lost to Jira during creation:
  ├─ Detect timeout (30 seconds)
  ├─ Cancel remaining platforms
  ├─ Rollback completed platforms
  ├─ Mark as "timeout" in status
  └─ Allow retry with same settings
```

### 10.2 Rollback Implementation

```python
class TransactionRollback:
    """Handles atomic rollback of multi-platform creation"""
    
    async def rollback(self, transaction_id: str, results: dict):
        """
        Rollback created resources for any failed transaction
        """
        rollback_status = {
            "transaction_id": transaction_id,
            "rollback_results": {},
            "started_at": datetime.utcnow(),
            "errors": []
        }
        
        # Rollback in reverse order of creation
        for platform in ["azure_devops", "jira", "smartsheet", "excel"]:
            if platform not in results:
                continue
                
            result = results[platform]
            if result.get("status") != "completed":
                continue
            
            try:
                await self._rollback_platform(platform, result)
                rollback_status["rollback_results"][platform] = "success"
                
            except RollbackError as e:
                rollback_status["rollback_results"][platform] = "failed"
                rollback_status["errors"].append({
                    "platform": platform,
                    "error": str(e),
                    "resource_id": result.get("platform_item_id")
                })
        
        rollback_status["completed_at"] = datetime.utcnow()
        
        # If any rollback failed, alert operations
        if rollback_status["errors"]:
            await self._alert_operations(rollback_status)
        
        return rollback_status
    
    async def _rollback_platform(self, platform: str, result: dict):
        """Rollback specific platform"""
        if platform == "excel":
            # Delete temporary file
            os.remove(result["file_path"])
            
        elif platform == "smartsheet":
            connector = SmartSheetConnector(...)
            await connector.delete_sheet(result["sheet_id"])
            
        elif platform == "jira":
            connector = JiraConnector(...)
            await connector.delete_project(result["project_key"])
            
        elif platform == "azure_devops":
            connector = AzureDevOpsConnector(...)
            await connector.delete_project(result["project_id"])
```

---

## Implementation Plan & Milestones

### 11.1 Phased Implementation

```
PHASE 1: Foundation (Weeks 1-3)
───────────────────────────────────────────────────────────
Week 1: Design & Setup
├─ Create database schema (platform_credentials, transactions)
├─ Set up encryption infrastructure (KMS/Vault)
├─ Design universal project plan schema
├─ Create data transformation interfaces
└─ Set up testing environment

Week 2: Authentication & Credential Management
├─ Implement credential storage (encrypted)
├─ Build SmartSheet OAuth flow
├─ Build Jira OAuth flow
├─ Build Azure DevOps OAuth flow
├─ Create credential testing endpoints
└─ Build credential management UI

Week 3: Data Transformation Layer
├─ Implement ProjectPlanToExcelTransformer
├─ Implement ProjectPlanToSmartSheetTransformer
├─ Implement ProjectPlanToJiraTransformer
├─ Implement ProjectPlanToAzureDevOpsTransformer
├─ Create transformer interface for future platforms
└─ Unit test all transformers

DELIVERABLES:
├─ Credential management system
├─ Encryption infrastructure
├─ Data transformation layer
└─ Database schema

---

PHASE 2: Platform Integration (Weeks 4-6)
───────────────────────────────────────────────────────────
Week 4: SmartSheet Integration
├─ Build SmartSheetConnector class
├─ Implement create sheet method
├─ Implement add rows with hierarchy
├─ Implement enable Gantt
├─ Implement delete sheet (rollback)
├─ Build SmartSheetCreator orchestrator
└─ Integration tests

Week 5: Jira Integration
├─ Build JiraConnector class
├─ Implement create project
├─ Implement create epic/story/task/subtask
├─ Implement create sprints
├─ Implement create links (dependencies)
├─ Implement delete project (rollback)
├─ Build JiraCreator orchestrator
└─ Integration tests

Week 6: Azure DevOps Integration
├─ Build AzureDevOpsConnector class
├─ Implement create project
├─ Implement create epic/feature/story/task
├─ Implement create iterations
├─ Implement create areas
├─ Implement delete project (rollback)
├─ Build AzureDevOpsCreator orchestrator
└─ Integration tests

DELIVERABLES:
├─ SmartSheet integration
├─ Jira integration
├─ Azure DevOps integration
└─ Connector base classes

---

PHASE 3: Multi-Platform Orchestration (Weeks 7-9)
───────────────────────────────────────────────────────────
Week 7: Delivery Platform Agent
├─ Build DeliveryPlatformAgent class
├─ Implement parallel platform creation
├─ Implement transaction management
├─ Implement rollback logic
├─ Implement error handling
└─ Unit tests

Week 8: API & Backend Integration
├─ Create /api/project/platforms/select endpoint
├─ Create /api/project/platforms/create endpoint
├─ Create /api/project/platforms/status endpoint
├─ Create /api/project/platforms/retry endpoint
├─ Create /api/project/platforms/test-connection endpoint
├─ Implement request validation
├─ Implement error responses
└─ API documentation

Week 9: Failure Handling & Rollback
├─ Implement atomic transactions
├─ Implement rollback on partial failure
├─ Implement retry mechanism
├─ Implement operation alerting
├─ Implement transaction logging
├─ Build transaction history UI
└─ Failure scenario tests

DELIVERABLES:
├─ Delivery Platform Agent
├─ Multi-platform API
├─ Transaction management
├─ Rollback system

---

PHASE 4: Frontend & UI (Weeks 10-12)
───────────────────────────────────────────────────────────
Week 10: Platform Selection UI
├─ Build platform selection screen
├─ Build credential entry forms
├─ Build SmartSheet auth form
├─ Build Jira auth form
├─ Build Azure DevOps auth form
├─ Implement form validation
└─ Credential save/retrieve functionality

Week 11: Mapping Configuration UI
├─ Build optional mapping config screen
├─ Build WBS hierarchy mapper
├─ Build field mapper
├─ Build sprint planning config
├─ Implement configuration persistence
└─ UI tests

Week 12: Status Dashboard
├─ Build status dashboard component
├─ Show platform creation results
├─ Display direct links to created resources
├─ Show statistics
├─ Implement error display
├─ Build retry interface
└─ Build transaction history view

DELIVERABLES:
├─ Platform selection UI
├─ Credential management UI
├─ Mapping configuration UI
├─ Status dashboard

---

PHASE 5: Testing & Hardening (Weeks 13-14)
───────────────────────────────────────────────────────────
Week 13: Integration & End-to-End Testing
├─ End-to-end test: Upload → Excel
├─ End-to-end test: Upload → SmartSheet
├─ End-to-end test: Upload → Jira
├─ End-to-end test: Upload → Azure DevOps
├─ End-to-end test: Multi-platform creation
├─ Failure scenario testing
├─ Rollback testing
└─ Load testing

Week 14: Production Readiness
├─ Security audit
├─ Performance optimization
├─ Documentation
├─ Runbook creation
├─ Monitoring setup
├─ Logging & alerting
├─ Deployment preparation
└─ Staging environment validation

DELIVERABLES:
├─ Test suite
├─ Security audit report
├─ Operations runbook
├─ Deployment guide

---

PHASE 6: Deployment & Support (Weeks 15-16)
───────────────────────────────────────────────────────────
Week 15: Beta Rollout
├─ Deploy to staging
├─ Customer beta testing (selected users)
├─ Collect feedback
├─ Monitor performance
└─ Fix critical issues

Week 16: Production Deployment
├─ Deploy to production
├─ Monitor all platforms
├─ Customer support ready
├─ Documentation published
└─ Feature announcement

DELIVERABLES:
├─ Staged production rollout
├─ Customer documentation
├─ Support guide
└─ Feature announcement
```

### 11.2 Success Metrics

```
Functionality Metrics:
─────────────────────
├─ Excel creation: 100% success rate
├─ SmartSheet creation: 99% success rate (platform dependent)
├─ Jira creation: 99% success rate (platform dependent)
├─ Azure DevOps creation: 99% success rate (platform dependent)
├─ Multi-platform creation: 95% all-succeed rate
├─ Rollback success: 99% success rate
└─ Retry success: 95% on second attempt

Performance Metrics:
───────────────────
├─ Excel creation: < 10 seconds
├─ SmartSheet creation: < 60 seconds
├─ Jira creation: < 90 seconds
├─ Azure DevOps creation: < 60 seconds
├─ Parallel creation (all 4): < 150 seconds
├─ Rollback completion: < 30 seconds
└─ API response time: < 100ms

User Experience Metrics:
───────────────────────
├─ Credential validation time: < 5 seconds
├─ Platform selection UI load: < 2 seconds
├─ Status dashboard update: < 1 second
├─ Error clarity score: > 90%
└─ User satisfaction: > 4.5/5

Reliability Metrics:
───────────────────
├─ Platform unavailability impact: 0 (fallback to available platforms)
├─ Data integrity: 100% (no orphaned items)
├─ Credential security: SSL, encryption, audit log
├─ API rate limit compliance: 100%
└─ Transaction audit trail: Complete
```

---

## Testing Strategy

### 12.1 Test Plan

```
Unit Tests:
──────────
├─ Transformer tests
│  ├─ Project → SmartSheet transformation
│  ├─ Project → Jira transformation
│  ├─ Project → Azure DevOps transformation
│  ├─ Field mapping correctness
│  └─ Hierarchy preservation
├─ Connector tests
│  ├─ API call formatting
│  ├─ Response parsing
│  ├─ Error handling
│  └─ Pagination (if needed)
├─ Credential tests
│  ├─ Encryption/decryption
│  ├─ Token validation
│  ├─ OAuth flow
│  └─ Expiry handling
└─ Transaction tests
   ├─ Atomic operations
   ├─ Rollback logic
   ├─ Error scenarios
   └─ Partial failures

Integration Tests:
──────────────────
├─ SmartSheet API integration
│  ├─ Create sheet
│  ├─ Add rows
│  ├─ Enable Gantt
│  ├─ Delete sheet
│  └─ Error handling
├─ Jira API integration
│  ├─ Create project
│  ├─ Create epics/stories/tasks
│  ├─ Create sprints
│  ├─ Delete project
│  └─ Error handling
├─ Azure DevOps API integration
│  ├─ Create project
│  ├─ Create work items
│  ├─ Create iterations
│  ├─ Delete project
│  └─ Error handling
└─ Multi-platform execution
   ├─ Parallel creation
   ├─ Individual platform failure
   ├─ Rollback on failure
   └─ Retry mechanism

End-to-End Tests:
─────────────────
├─ Full workflow tests
│  ├─ Document upload → Platform selection → Excel only
│  ├─ Document upload → Platform selection → SmartSheet only
│  ├─ Document upload → Platform selection → Jira only
│  ├─ Document upload → Platform selection → Azure DevOps only
│  └─ Document upload → Platform selection → All 4 platforms
├─ Failure scenario tests
│  ├─ Invalid credentials
│  ├─ Platform timeout
│  ├─ API rate limit
│  ├─ Network disconnection
│  └─ Partial failures + rollback
└─ Data integrity tests
   ├─ WBS preservation
   ├─ Dependency creation
   ├─ Timeline accuracy
   └─ Resource assignment

Load Tests:
───────────
├─ Parallel platform creation
│  ├─ 10 concurrent projects
│  ├─ 100 concurrent projects
│  └─ Platform API rate limits
└─ Large project tests
   ├─ 200+ tasks
   ├─ 50+ dependencies
   └─ Deep WBS hierarchy

Security Tests:
───────────────
├─ Credential security
│  ├─ Encryption verification
│  ├─ No logs in error messages
│  ├─ Token rotation
│  └─ Access control
├─ OAuth security
│  ├─ State parameter validation
│  ├─ Redirect URI validation
│  ├─ Token expiry handling
│  └─ Refresh token security
└─ API security
   ├─ Input validation
   ├─ SQL injection prevention
   ├─ XSS prevention
   └─ CSRF protection
```

### 12.2 Test Data

```
Sample Project Plans:
─────────────────────
├─ Small project (5 phases, 10 deliverables, 30 tasks)
├─ Medium project (7 phases, 25 deliverables, 100 tasks)
├─ Large project (10 phases, 50 deliverables, 200+ tasks)
└─ Complex project (dependencies, sub-phases, cross-phase tasks)

Mock Platform Responses:
────────────────────────
├─ SmartSheet: Mock API responses for all operations
├─ Jira: Mock API responses for all operations
├─ Azure DevOps: Mock API responses for all operations
└─ Error scenarios: Timeout, rate limit, auth failure

Failure Scenarios:
──────────────────
├─ Invalid API token
├─ Expired OAuth token
├─ Network timeout
├─ Rate limit exceeded
├─ Platform maintenance (503)
├─ Invalid project configuration
└─ Partial creation + rollback needed
```

---

## Deployment & DevOps

### 13.1 Deployment Pipeline

```
CI/CD Pipeline:
───────────────
Code Commit
  ↓
1. Lint & Format Check (pre-commit hooks)
   ├─ Python: flake8, black, isort
   ├─ JavaScript: eslint, prettier
   └─ SQL: sqlfluff (if needed)
  ↓
2. Unit Tests (parallel)
   ├─ Backend: pytest (fast)
   ├─ Frontend: jest (fast)
   └─ Code coverage > 80%
  ↓
3. Integration Tests (sequential)
   ├─ SmartSheet API mocking
   ├─ Jira API mocking
   ├─ Azure DevOps API mocking
   └─ Database transaction tests
  ↓
4. Security Tests (parallel)
   ├─ SAST: SonarQube, Snyk
   ├─ Dependency check
   ├─ Credentials scanner
   └─ OWASP check
  ↓
5. Build Artifacts
   ├─ Docker image
   ├─ Database migrations
   ├─ Frontend bundle
   └─ Documentation
  ↓
6. Deploy to Staging
   ├─ Run migrations
   ├─ Deploy container
   ├─ Smoke tests
   └─ Health checks
  ↓
7. Deploy to Production
   ├─ Blue-green deployment
   ├─ Gradual rollout (10% → 50% → 100%)
   ├─ Health monitoring
   └─ Rollback if issues

Deployment Checklist:
────────────────────
├─ All tests passing
├─ Code review approved
├─ Security audit passed
├─ Documentation updated
├─ Database migrations tested
├─ Rollback plan in place
├─ On-call engineer assigned
└─ Customer communication ready
```

### 13.2 Monitoring & Alerting

```
Monitoring Dashboards:
──────────────────────
├─ Platform Creation Success Rate
│  ├─ Overall: 95%+ success
│  ├─ Per-platform: >99% when available
│  └─ Rollback: 99%+ success
├─ API Performance
│  ├─ Response time: p95 < 100ms
│  ├─ Error rate: < 1%
│  └─ Availability: > 99.9%
├─ Platform Connectivity
│  ├─ SmartSheet API: Up/Down status
│  ├─ Jira API: Up/Down status
│  ├─ Azure DevOps API: Up/Down status
│  └─ Last availability: Timestamp
└─ Credential & Security
   ├─ Failed auth attempts
   ├─ Credential expiry warnings
   ├─ Token refresh status
   └─ Access control violations

Alerting:
─────────
├─ Critical Alerts
│  ├─ Database connectivity lost
│  ├─ KMS/encryption unavailable
│  ├─ Multiple platform failures (>10% error rate)
│  └─ Unauthorized access attempts
├─ Warning Alerts
│  ├─ Single platform degraded (5-10% error rate)
│  ├─ Slow API response (>200ms p95)
│  ├─ Credential expiry in 7 days
│  └─ Disk usage > 80%
└─ Info Alerts
   ├─ Rollback execution
   ├─ Token refresh
   ├─ Migration completion
   └─ Daily summary report

Logging:
────────
├─ Transaction logs
│  ├─ Transaction ID
│  ├─ Platforms selected
│  ├─ Start/end time
│  ├─ Success/failure status
│  └─ Platform-specific results
├─ API logs
│  ├─ Request/response
│  ├─ Status code
│  ├─ Duration
│  └─ User ID
├─ Error logs
│  ├─ Error type
│  ├─ Stack trace (sanitized)
│  ├─ Context
│  └─ Recovery action
└─ Audit logs
   ├─ Credential access
   ├─ User actions
   ├─ Admin changes
   └─ Security events
```

---

## Conclusion

This comprehensive design document provides the complete specification for implementing multi-platform project plan generation in Project Aura. The phased 16-week implementation approach allows for:

1. **Foundation building** (Weeks 1-3): Database, security, and transformation infrastructure
2. **Platform integration** (Weeks 4-6): SmartSheet, Jira, and Azure DevOps connectors
3. **Orchestration** (Weeks 7-9): Multi-platform transaction management and rollback
4. **User experience** (Weeks 10-12): UI for selection, mapping, and status tracking
5. **Testing & hardening** (Weeks 13-14): Comprehensive testing and production readiness
6. **Deployment** (Weeks 15-16): Staged rollout with monitoring

**Key Success Factors:**
- ✓ Atomic transactions with rollback
- ✓ Enterprise-grade security
- ✓ Extensible architecture
- ✓ Comprehensive error handling
- ✓ User-friendly credential management
- ✓ Real-time status tracking

The design is extensible for future platforms (Monday.com, Asana, MS Project) through the universal project plan schema and platform adapter pattern.

---

**END OF DESIGN DOCUMENT**
