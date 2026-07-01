# Interactive Platform Deployment - UI Preview

## What You'll See on Project Summary Page

### Section Heading
```
🚀 Deploy this project plan to Excel, SmartSheet, or Jira Cloud instantly

Create a fully populated project plan on your preferred platform with a single click. 
No manual setup required.
```

---

## Platform Cards Layout (Responsive Grid)

```
┌─────────────────────────────────────────────────────────────────────┐
│                  MULTI-PLATFORM PROJECT DELIVERY                    │
│                                                                       │
│   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│   │      📊          │  │      📈          │  │      🎯          │  │
│   │    Excel         │  │   SmartSheet     │  │  Jira Cloud      │  │
│   │                  │  │                  │  │                  │  │
│   │ PMO workbooks    │  │ Professional     │  │ Scrum boards     │  │
│   │ with dashboards  │  │ collaborative    │  │ with epics &     │  │
│   │ & Gantt          │  │ sheets           │  │ sprints          │  │
│   │                  │  │                  │  │                  │  │
│   │ [  Select  ]     │  │ [  Select  ]     │  │ [  Select  ]     │  │
│   └──────────────────┘  └──────────────────┘  └──────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Interaction Flow

### Option 1: Deploy to Excel
```
User Action: Click [Select] on Excel card
              ↓
System: Immediately generates Excel workbook
              ↓
Display: Alert "✅ EXCEL project created successfully!"
              ↓
Result: File created at workbooks/[ProjectName]_plan.xlsx
              ↓
Page: Reloads to show updated status
```

### Option 2: Deploy to SmartSheet
```
User Action: Click [Select] on SmartSheet card
              ↓
Display: Modal dialog appears

    ╔═══════════════════════════════════════╗
    ║  Connect SmartSheet Account           ║
    ║                                       ║
    ║  SmartSheet API Token                 ║
    ║  [________________|demo_________|     ║
    ║                                       ║
    ║  [Deploy]  [Cancel]                   ║
    ╚═══════════════════════════════════════╝

              ↓
User: Leave empty or enter API token
              ↓
User: Click [Deploy]
              ↓
System: Shows "⏳ Deploying..." on button
              ↓
API Call: POST /api/project/create-platform
              ↓
Display: Alert "✅ SMARTSHEET project created successfully!"
              ↓
Modal: Closes automatically
              ↓
Page: Reloads after 1 second
```

### Option 3: Deploy to Jira
```
User Action: Click [Select] on Jira Cloud card
              ↓
Display: Modal dialog appears

    ╔═══════════════════════════════════════╗
    ║  Connect Jira Cloud Account           ║
    ║                                       ║
    ║  Jira Instance URL                    ║
    ║  [https://your-domain.atlassian.net] ║
    ║                                       ║
    ║  Jira API Token                       ║
    ║  [________________|demo_________|     ║
    ║                                       ║
    ║  [Deploy]  [Cancel]                   ║
    ╚═══════════════════════════════════════╝

              ↓
User: Enter Jira URL (optional, defaults to demo)
User: Enter API Token (optional, defaults to "demo")
              ↓
User: Click [Deploy]
              ↓
System: Shows "⏳ Deploying..." on button
              ↓
API Call: POST /api/project/create-platform
              ↓
Display: Alert "✅ JIRA project created successfully!"
              ↓
Modal: Closes automatically
              ↓
Page: Reloads after 1 second
```

---

## Visual Effects

### Hover State on Cards
When you hover your mouse over any platform card:
- Card border changes from gray to blue
- A subtle shadow appears under the card
- Card slightly lifts up (2px elevation)
- Smooth 0.3s animation transition

---

## Modal Dialog Features

- **Overlay**: Semi-transparent dark background (clicks outside close modal)
- **Width**: Max 500px, responsive to 90% on mobile devices
- **Fields**: Only relevant fields show for selected platform
- **Buttons**:
  - Deploy: Primary button (turquoise), disabled during deployment
  - Cancel: Secondary button, closes modal
- **Form Reset**: All fields clear when modal closes

---

## Testing with Demo Mode

### Demo Mode (No Real Credentials Needed)

**Test Excel**
1. Navigate to project summary page
2. Click [Select] on Excel card
3. See instant success message
4. Check `workbooks/` folder for generated file

**Test SmartSheet**
1. Click [Select] on SmartSheet card
2. Modal appears
3. Leave token field empty (defaults to "demo")
4. Click [Deploy]
5. Success message shows demo URL: https://app.smartsheet.com/sheets/demo_15

**Test Jira**
1. Click [Select] on Jira Cloud card
2. Modal appears
3. Leave both fields empty (defaults to demo)
4. Click [Deploy]
5. Success message shows demo URL: https://demo.atlassian.net/browse/DEMO15

---

## Production Use (With Real Credentials)

### SmartSheet
1. Click [Select]
2. Enter your SmartSheet API token
3. Click [Deploy]
4. Project created in real SmartSheet account

### Jira
1. Click [Select]
2. Enter your Jira instance URL (https://your-domain.atlassian.net)
3. Enter your Jira API token
4. Click [Deploy]
5. Scrum board created in real Jira account

---

## Success Indicators

✅ Card hovers correctly (border/shadow change)
✅ Modal appears when clicking SmartSheet or Jira
✅ Modal closes on Cancel button
✅ Modal closes on outside click (overlay)
✅ Loading indicator shows during deployment
✅ Success alert appears with correct platform name
✅ Page reloads after successful deployment
✅ Excel creates file immediately without modal

---

## Error Handling

If something goes wrong:
1. Error alert appears with message
2. Deploy button is re-enabled
3. You can retry the deployment
4. Check browser console for detailed error logs

Common issues to check:
- Network connectivity
- API credentials validity (if not using demo)
- Flask server is running on localhost:5000
