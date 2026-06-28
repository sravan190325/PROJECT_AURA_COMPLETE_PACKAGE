# PROJECT AURA - COMPLETE SETUP GUIDE

## 🚀 Quick Start (5 Minutes)

### Step 1: Get Claude API Key
1. Visit: https://console.anthropic.com/
2. Sign in or create account
3. Go to "API Keys"
4. Generate new key

### Step 2: Create .env File
```bash
cp .env.example .env
```

Edit `.env` and add your Claude API key:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

### Step 3: Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 4: Run Application
```bash
python app.py
```

Visit: http://localhost:5000

---

## 📁 Project Structure

```
PROJECT_AURA_COMPLETE_PACKAGE/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
│
├── services/                  # Business logic
│   ├── __init__.py
│   ├── pdf_parser.py
│   ├── docx_parser.py
│   ├── pptx_parser.py
│   ├── document_processor.py
│   ├── claude_service.py      # Claude AI integration
│   ├── project_detector.py    # Project detection
│   ├── database_service.py    # Database operations
│   ├── excel_formatter.py     # Excel formatting
│   ├── project_plan_engine.py # Timeline logic
│   └── workbook_generator.py  # Excel generation
│
├── routes/                    # API endpoints
│   ├── __init__.py
│   ├── upload_routes.py       # File upload
│   ├── project_routes.py      # Project management
│   └── workbook_routes.py     # Excel generation
│
├── templates/                 # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   ├── clarification.html
│   ├── project_summary.html
│   └── workbook_generator.html
│
├── static/                    # Frontend assets
│   ├── css/style.css
│   └── js/upload.js
│
├── uploads/                   # Temporary uploads
├── temp/                      # Working files
└── workbooks/                 # Generated Excel files
```

---

## 🔧 Configuration

### .env File (Required)
Create `.env` from `.env.example` and add:
- ANTHROPIC_API_KEY (from console.anthropic.com)
- FLASK_ENV (development/production)
- SECRET_KEY (any random string)

### config.py
Pre-configured for development. Update for production.

---

## 📚 Features

### Phase 1: Document Upload
- Upload PDF, DOCX, PPTX files
- Extract content automatically
- Display extracted text

### Phase 2: Claude AI Analysis
- Analyze documents with AI
- Detect project type (7 types)
- Extract key information
- Store in database

### Phase 3: Excel Workbook
- Generate 14-sheet Excel workbooks
- Professional formatting
- Ready-to-use templates
- Download as file

---

## 🧪 Testing

### Quick Test
1. Start app: `python app.py`
2. Upload a test PDF/DOCX/PPTX
3. View extracted content
4. Analyze with Claude
5. Provide project details
6. Generate Excel workbook
7. Download and review

---

## 🐛 Troubleshooting

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### ANTHROPIC_API_KEY not found
Create `.env` file with your API key

### Database locked
Only one app instance at a time

### Port 5000 already in use
```bash
python app.py --port 5001
```

---

## 📊 Supported Project Types

1. Data Engineering
2. GenAI
3. Cloud Migration
4. Data Analytics
5. Reporting / BI
6. Application Development
7. Data Platform Modernization

---

## 💾 Database

SQLite database with tables:
- projects
- documents
- deliverables
- team_members
- risks

Auto-created on first run.

---

## 🔐 Security Notes

- Never commit `.env` file
- Keep API key secret
- Use HTTPS in production
- Set DEBUG=False in production
- Update SECRET_KEY

---

## 📈 Performance

- Generation time: 10-30 seconds
- File size: 500KB - 2MB
- Handles 100+ projects

---

## 🆘 Need Help?

1. Check error messages in console
2. Verify .env file is correct
3. Ensure API key is valid
4. Check internet connection
5. Review logs for details

---

## 🎯 Next Steps

1. Set up .env with API key
2. Install dependencies
3. Run application
4. Test complete workflow
5. Generate sample workbook

---

**Ready to use Project Aura!** 🚀
