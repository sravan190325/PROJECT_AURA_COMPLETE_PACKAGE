# Project Aura - Quick Start Guide (Production Ready)

Get Project Aura up and running in minutes!

---

## ⚡ 5-Minute Setup (Local Development)

### Windows Users

1. **Open Command Prompt** in the project folder

2. **Run the startup script**:
   ```cmd
   start.bat
   ```

3. **Edit `.env` file**:
   - Add your Claude API key: `ANTHROPIC_API_KEY=sk-ant-...`

4. **Open browser**:
   - Visit `http://localhost:5000`

### Mac/Linux Users

1. **Open Terminal** in the project folder

2. **Make script executable**:
   ```bash
   chmod +x start.sh
   ```

3. **Run the startup script**:
   ```bash
   ./start.sh
   ```

4. **Edit `.env` file**:
   - Add your Claude API key: `ANTHROPIC_API_KEY=sk-ant-...`

5. **Open browser**:
   - Visit `http://localhost:5000`

---

## 🐳 Docker Setup (Production-Like)

### Prerequisites
- Docker installed
- Claude API key ready

### Steps

1. **Create `.env` file**:
   ```bash
   cp .env.development .env
   ```

2. **Add API key** to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

3. **Start with Docker Compose**:
   ```bash
   docker-compose up
   ```

4. **Access application**:
   - Web: `http://localhost:5000`
   - Database: `postgresql://project_aura:password@localhost:5432/project_aura`

5. **Stop services**:
   ```bash
   docker-compose down
   ```

---

## 🚀 Heroku Deployment (1 Command)

### Prerequisites
- Heroku account
- Heroku CLI installed
- GitHub repository

### Steps

1. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```

2. **Add PostgreSQL**:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set ANTHROPIC_API_KEY=sk-ant-...
   heroku config:set SECRET_KEY=your-secret-key-here
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

5. **View live**:
   ```bash
   heroku open
   ```

---

## 📋 Directory Structure

```
PROJECT_AURA_COMPLETE_PACKAGE/
├── app.py                      # Main Flask application
├── wsgi.py                     # WSGI entry point (production)
├── config.py                   # Configuration classes
├── requirements.txt            # Python dependencies
├── Procfile                    # Heroku process configuration
├── runtime.txt                 # Python version (Heroku)
├── Dockerfile                  # Container image
├── docker-compose.yml          # Docker Compose config
├── .env.development            # Dev environment template
├── .env.production             # Prod environment template
├── start.bat                   # Windows startup
├── start.sh                    # Unix/Linux/Mac startup
│
├── routes/                     # Flask blueprints
│   ├── upload_routes.py       # File upload endpoints
│   ├── project_routes.py      # Project management endpoints
│   └── workbook_routes.py     # Workbook generation endpoints
│
├── services/                   # Business logic
│   ├── database_service.py    # Database operations
│   ├── claude_service.py      # AI integration
│   ├── document_processor.py  # File processing
│   ├── pmo_workbook_generator.py  # Workbook generation
│   └── ...
│
├── templates/                  # HTML templates
│   ├── base_blend.html        # Base layout (Blend brand)
│   ├── index_blend.html       # Landing page
│   ├── results_blend.html     # Results page
│   ├── clarification_blend.html # Project setup
│   └── project_summary_blend.html # Executive dashboard
│
├── static/                     # Static assets
│   ├── css/blend.css          # Blend design system
│   └── js/upload.js           # Upload functionality
│
└── docs/
    ├── DEPLOYMENT_GUIDE.md     # Full deployment guide
    ├── PRODUCTION_CHECKLIST.md # Pre-launch checklist
    └── README.md               # Project overview
```

---

## 🔑 Environment Variables

### Required

| Variable | Example | Purpose |
|----------|---------|---------|
| `ANTHROPIC_API_KEY` | `sk-ant-...` | Claude API access |
| `FLASK_ENV` | `production` | Environment mode |
| `SECRET_KEY` | `random-32-char` | Session encryption |

### Optional

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | `sqlite:///project_aura.db` | Database connection |
| `PORT` | `5000` | Server port |
| `WORKERS` | `1` (dev) / `4` (prod) | Gunicorn workers |

---

## 🧪 Test the Application

### 1. Verify Installation
```bash
python -c "from flask import Flask; print('Flask OK')"
```

### 2. Start Server
```bash
python app.py
```

### 3. Test Endpoints
```bash
# Health check
curl http://localhost:5000/health

# Homepage
curl http://localhost:5000/
```

### 4. Test Upload
- Open `http://localhost:5000` in browser
- Try uploading a PDF/DOCX/PPTX file
- Complete the project clarification form
- Download the generated workbook

---

## 🔧 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### ".env file not found"
```bash
cp .env.development .env
# Add your API key
```

### "Port 5000 already in use"
```bash
# Set custom port
set PORT=5001  # Windows
export PORT=5001  # Mac/Linux
python app.py
```

### "Database connection failed"
```bash
# Check DATABASE_URL is set correctly
echo %DATABASE_URL%  # Windows
echo $DATABASE_URL   # Mac/Linux
```

### "Claude API key error"
- Verify key starts with `sk-ant-`
- Check key is valid and has credits
- Ensure it's in `.env` file, not hardcoded

---

## 📊 Deployment Options

| Option | Ease | Cost | Scalability |
|--------|------|------|-------------|
| **Local** | ⭐⭐⭐⭐⭐ | Free | None |
| **Docker** | ⭐⭐⭐⭐ | Free (local) | Manual |
| **Heroku** | ⭐⭐⭐⭐ | $7-16/mo | Easy |
| **AWS** | ⭐⭐⭐ | Variable | High |
| **VPS** | ⭐⭐ | $5-20/mo | Manual |

---

## 📈 Next Steps

1. **Complete Production Checklist**
   - Review `PRODUCTION_CHECKLIST.md`
   - Run security verification
   - Test all functionality

2. **Set Up Monitoring**
   - Enable health checks
   - Set up error tracking
   - Configure log aggregation

3. **Plan Deployment**
   - Choose platform (Heroku recommended for simplicity)
   - Configure CI/CD pipeline
   - Establish backup procedure

4. **User Communication**
   - Prepare documentation
   - Plan training/onboarding
   - Set up support channel

---

## 🆘 Getting Help

### Documentation
- `DEPLOYMENT_GUIDE.md` - Detailed deployment instructions
- `PRODUCTION_CHECKLIST.md` - Pre-launch verification
- `README.md` - Project overview

### Common Issues
- Check the Troubleshooting section above
- Review logs: `docker-compose logs -f web`
- Check environment variables: `heroku config`

---

## ✅ Verification Checklist

Before going live, verify:

- [ ] Application runs locally without errors
- [ ] Upload functionality works
- [ ] Analysis generation works
- [ ] Workbook download works
- [ ] All pages display correctly
- [ ] Mobile responsive (test on phone)
- [ ] API key is valid and has credits
- [ ] Database connection works
- [ ] Backups enabled
- [ ] SSL certificate active (if deployed)

---

## 🎉 You're Ready!

Your Project Aura application is production-ready!

**Questions?** Check the deployment guides or review the code comments.

**Deployed successfully?** Great! Monitor logs for the first 24 hours.

---

Last Updated: June 28, 2026
Status: Production Ready ✓
