# Project Aura Enhanced Workbook - Developer Quick Start Guide

## Overview
This guide helps developers understand and extend the enhanced workbook generation system.

---

## 📁 Module Structure

### `workbook_enhancements.py`
**Purpose:** Contains all enhancement sheet generators

**Key Classes:**
- `WorkbookEnhancements` - Static class with sheet generation methods

**Key Methods:**
```python
@staticmethod
def create_executive_dashboard(workbook, project_info, db_summary)
def create_project_roadmap(workbook, project_info)
def create_enhanced_project_plan(workbook, project_info, db_summary)
def create_milestone_tracker(workbook, project_info, db_summary)
def create_resource_plan(workbook, project_info, db_summary)
def create_raid_register(workbook, project_info, db_summary)
def create_leave_capacity_planner(workbook, project_info, db_summary)
def create_weekly_status_tracker(workbook, project_info)
def create_ai_project_summary(workbook, project_info, db_summary)
```

**Color Palette (Customize Here):**
```python
COLOR_PALETTE = {
    'primary_dark': '1F4E78',    # Headers
    'primary': '366092',          # Titles
    'success': '70AD47',          # Complete
    'warning': 'FFC000',          # In Progress
    'danger': 'C5504F',           # Delayed/Risks
    'info': '4472C4',             # Info sections
    'neutral': 'BFBFBF',          # Planned
}
```

---

### `workbook_generator_enhanced.py`
**Purpose:** Main entry point for enhanced workbook generation

**Key Classes:**
- `EnhancedWorkbookGenerator(WorkbookGenerator)` - Extended generator
- `WorkbookGeneratorFactory` - Factory pattern for flexible instantiation

**Usage Examples:**

```python
# Using factory (recommended)
generator = WorkbookGeneratorFactory.create_enhanced_generator(
    project_info, 
    db_summary
)
generator.generate('output.xlsx')

# Direct instantiation
from services.workbook_generator_enhanced import EnhancedWorkbookGenerator
generator = EnhancedWorkbookGenerator(project_info, db_summary)
generator.generate('output.xlsx')

# Disable enhancements (backward compatibility)
generator = EnhancedWorkbookGenerator(
    project_info, 
    db_summary, 
    include_enhancements=False
)
```

---

### `gantt_generator.py`
**Purpose:** Gantt chart visualization

**Key Classes:**
- `GanttGenerator` - Static class for Gantt chart generation

**Key Methods:**
```python
@staticmethod
def create_gantt_chart(workbook, project_info, plan_data)
def create_timeline_visualization(workbook, project_info, plan_data)
```

---

## 🔌 Integration Points

### Data Input
All generators expect these data structures:

**`project_info` Dictionary:**
```python
{
    'project_name': str,        # e.g., "Mobile App Redesign"
    'client_name': str,         # e.g., "Acme Corp"
    'project_type': str,        # e.g., "GenAI / AI Implementation"
    'start_date': str,          # Format: "YYYY-MM-DD"
    'duration_weeks': int,      # Number of weeks
    'team_size': int,           # Number of team members
    'delivery_model': str,      # e.g., "Fixed", "Time & Material"
    'scope': str                # Project scope description
}
```

**`db_summary` Dictionary:**
```python
{
    'risks': [                  # List of risks
        {
            'risk_description': str,
            'severity': str,     # Low, Medium, High
            'mitigation': str
        }
    ],
    'team_members': [           # List of team members
        {
            'role': str,         # e.g., "Developer", "QA"
            'count': int         # Number of people in role
        }
    ],
    'deliverables': [...],      # List of deliverables
    'milestones': [...]         # List of milestones
}
```

---

## 🎨 Using ExcelFormatter

The `ExcelFormatter` class provides professional formatting:

```python
from services.excel_formatter import ExcelFormatter

# Format header row
ExcelFormatter.format_header_row(worksheet, row_num, [col1, col2, col3])

# Format data row
ExcelFormatter.format_data_row(worksheet, row_num, [col1, col2, col3])

# Set column widths
ExcelFormatter.set_column_widths(worksheet, {'A': 20, 'B': 30})

# Freeze panes
ExcelFormatter.freeze_panes(worksheet, freeze_row=3, freeze_col='A')

# Add autofilter
ExcelFormatter.add_filter(worksheet, 'A3', 'E100')

# Format percentage column
ExcelFormatter.format_percentage_column(worksheet, start_row, end_row, column)
```

---

## 📝 Adding a New Enhancement Sheet

### Step 1: Create Method in `WorkbookEnhancements`

```python
@staticmethod
def create_custom_sheet(workbook, project_info: Dict, db_summary: Dict):
    """
    Create Custom Sheet description.
    
    Args:
        workbook: Excel workbook object
        project_info: Project information dictionary
        db_summary: Database project summary
    """
    # Create sheet
    ws = workbook.create_sheet('YY_Custom_Sheet')
    
    # Title
    from services.excel_formatter import ExcelFormatter
    ExcelFormatter.format_title(ws, 1, 1, 'Custom Sheet Title')
    ws.merge_cells('A1:D1')
    
    # Headers
    row = 3
    headers = ['Column1', 'Column2', 'Column3']
    for col, header in enumerate(headers, 1):
        ExcelFormatter.format_header_row(ws, row, [col])
        ws.cell(row=row, column=col).value = header
    
    # Data rows
    row += 1
    for item in data:
        ExcelFormatter.format_data_row(ws, row, list(range(1, 4)))
        ws.cell(row=row, column=1).value = item['field1']
        ws.cell(row=row, column=2).value = item['field2']
        ws.cell(row=row, column=3).value = item['field3']
        row += 1
    
    # Column widths and freeze
    ExcelFormatter.set_column_widths(ws, {'A': 20, 'B': 20, 'C': 20})
    ExcelFormatter.freeze_panes(ws, 3)
```

### Step 2: Call from `EnhancedWorkbookGenerator.generate()`

```python
def generate(self, output_path: str) -> bool:
    # ... existing code ...
    
    if self.include_enhancements:
        # ... existing enhancement calls ...
        WorkbookEnhancements.create_custom_sheet(
            self.workbook, 
            self.project_info, 
            self.db_summary
        )
    
    # ... rest of method ...
```

### Step 3: Update Documentation

Add entry to ENHANCEMENTS.md with:
- Sheet name and number
- Purpose
- Column descriptions
- Data sources
- Any calculated fields

---

## 🧪 Testing New Features

### Unit Test Example

```python
import pytest
from services.workbook_generator_enhanced import EnhancedWorkbookGenerator

@pytest.fixture
def sample_data():
    return {
        'project_info': {
            'project_name': 'Test Project',
            'client_name': 'Test Client',
            'project_type': 'Data Engineering',
            'start_date': '2025-01-01',
            'duration_weeks': 16,
            'team_size': 5,
            'delivery_model': 'Fixed',
            'scope': 'Test scope'
        },
        'db_summary': {
            'risks': [],
            'team_members': [{'role': 'Developer', 'count': 2}],
            'deliverables': [],
        }
    }

def test_enhanced_workbook_generation(sample_data, tmp_path):
    output_file = tmp_path / "test.xlsx"
    
    generator = EnhancedWorkbookGenerator(
        sample_data['project_info'],
        sample_data['db_summary']
    )
    
    assert generator.generate(str(output_file)) == True
    assert output_file.exists()
    
    # Verify sheets
    from openpyxl import load_workbook
    wb = load_workbook(str(output_file))
    assert len(wb.sheetnames) == 21
    assert '00_Executive_Dashboard' in wb.sheetnames
```

---

## 🔍 Debugging Tips

### View Generated Workbook Structure

```python
from openpyxl import load_workbook

wb = load_workbook('output.xlsx')
print(f"Sheets: {wb.sheetnames}")
print(f"Total sheets: {len(wb.sheetnames)}")

for sheet in wb.sheetnames:
    ws = wb[sheet]
    print(f"{sheet}: {ws.max_row} rows, {ws.max_column} columns")
```

### Check Cell Formatting

```python
ws = workbook.active
cell = ws['A1']

print(f"Value: {cell.value}")
print(f"Font: {cell.font}")
print(f"Fill: {cell.fill}")
print(f"Alignment: {cell.alignment}")
print(f"Border: {cell.border}")
```

### Validate Formulas

```python
for row in worksheet.iter_rows():
    for cell in row:
        if cell.data_type == 'f':  # Formula
            print(f"{cell.coordinate}: {cell.value}")
```

---

## 🚀 Performance Optimization

### Tips for Large Datasets

```python
# Disable recalculation during generation
workbook.calculation.calcMode = 'manual'

# ... add data ...

# Re-enable for user
workbook.calculation.calcMode = 'auto'
```

### Memory Management

```python
# Process large data in chunks
for chunk in data_chunks:
    # Add chunk to worksheet
    pass

# Garbage collect after major operations
import gc
gc.collect()
```

---

## 🔗 Class Hierarchy

```
WorkbookGenerator (original)
    ↓
EnhancedWorkbookGenerator (extended)
    │
    ├─ Calls WorkbookEnhancements (for new sheets)
    └─ Calls WorkbookGeneratorFactory (for instantiation)

WorkbookGeneratorFactory (utility)
    ├─ create_enhanced_generator()
    ├─ create_standard_generator()
    └─ create_generator(enhanced=bool)
```

---

## 🔐 Code Standards

### Style Guide
- **Naming:** snake_case for functions, PascalCase for classes
- **Documentation:** Docstrings on all public methods
- **Type Hints:** Required on all function signatures
- **Comments:** Use for non-obvious logic only

### Example

```python
def calculate_project_health(
    project_info: Dict[str, Any], 
    db_summary: Dict[str, Any]
) -> Dict[str, str]:
    """
    Calculate project health status based on risk count and complexity.
    
    Args:
        project_info: Project metadata dictionary
        db_summary: Database summary with risks and team info
        
    Returns:
        Dictionary with 'status' and 'color' keys
    """
    risk_count = len(db_summary.get('risks', []))
    complexity = len(db_summary.get('team_members', [])) + risk_count
    
    if risk_count > 5 or complexity > 15:
        return {'status': 'RED - High Risk', 'color': 'C5504F'}
    elif risk_count > 2 or complexity > 8:
        return {'status': 'AMBER - Medium Risk', 'color': 'FFC000'}
    else:
        return {'status': 'GREEN - Low Risk', 'color': '70AD47'}
```

---

## 📚 References

- **ENHANCEMENTS.md** - Complete feature documentation
- **IMPLEMENTATION_SUMMARY.md** - Deployment and integration guide
- **workbook_generator.py** - Original generator (for reference)
- **ExcelFormatter** - Formatting utilities documentation

---

## ❓ Common Questions

**Q: How do I disable enhancements for a specific workbook?**
A: Use `EnhancedWorkbookGenerator(..., include_enhancements=False)`

**Q: Can I customize the color scheme?**
A: Yes, modify `COLOR_PALETTE` in `workbook_enhancements.py`

**Q: How are dates calculated?**
A: Using `datetime` library, stored as Excel date format (yyyy-mm-dd)

**Q: What if required data is missing?**
A: All methods use `.get()` with defaults, so missing data shows as "N/A" or empty

**Q: How do I add a new sheet?**
A: Follow the "Adding a New Enhancement Sheet" section above

---

**Last Updated:** 2026-06-28  
**Version:** 1.0  
**Status:** Production Ready
