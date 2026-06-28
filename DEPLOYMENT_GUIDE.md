# Project Aura - Deployment Guide

Complete guide to deploying Project Aura to production.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Setup](#local-setup)
3. [Docker Deployment](#docker-deployment)
4. [Heroku Deployment](#heroku-deployment)
5. [Production Configuration](#production-configuration)
6. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- Heroku CLI (for Heroku deployment)
- Claude API key
- Git

---

## Local Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the appropriate `.env` file:

```bash
# For development
cp .env.development .env

# For production
cp .env.production .env
```

### 3. Update API Keys

Edit `.env` and add your Claude API key:

```env
ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Initialize Database

```bash
python -c "from services.database_service import DatabaseService; DatabaseService().init_db()"
```

### 5. Run Development Server

```bash
python app.py
```

Access at `http://localhost:5000`

---

## Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose installed

### 1. Build Docker Image

```bash
docker build -t project-aura:latest .
```

### 2. Run with Docker Compose

```bash
# Create .env file first
cp .env.development .env

# Start services
docker-compose up -d
```

### 3. Access Application

- Web: `http://localhost:5000`
- Database: `postgresql://project_aura:password@localhost:5432/project_aura`

### 4. View Logs

```bash
docker-compose logs -f web
```

### 5. Stop Services

```bash
docker-compose down
```

---

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed
- GitHub repository

### 1. Create Heroku App

```bash
heroku create project-aura-yourname
```

### 2. Add PostgreSQL Add-on

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### 3. Set Environment Variables

```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Configure Database URL

```bash
heroku config:set DATABASE_URL=$(heroku config:get DATABASE_URL)
```

### 5. Deploy

```bash
git add Procfile runtime.txt requirements.txt
git commit -m "Add Heroku configuration"
git push heroku main
```

### 6. Monitor Deployment

```bash
heroku logs --tail
```

### 7. Open Application

```bash
heroku open
```

---

## Production Configuration

### Security

1. **Set Strong Secret Key**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Add the output as `SECRET_KEY` in environment

2. **Enable HTTPS**
   - Heroku provides free HTTPS by default
   - For custom domains, use SSL certificate

3. **Database**
   - Use PostgreSQL in production (not SQLite)
   - Enable SSL connections
   - Regular backups

### Performance

1. **Gunicorn Workers**
   - Heroku: 4 workers (hobby dynos) or more for standard/professional
   - VPS: (2 × CPU cores) + 1

2. **Session Configuration**
   - SESSION_COOKIE_SECURE=true
   - SESSION_COOKIE_HTTPONLY=true
   - SESSION_COOKIE_SAMESITE=Lax

### Monitoring

1. **Health Check Endpoint**
   ```bash
   curl https://your-domain.com/health
   ```

2. **Error Tracking**
   - Set up Sentry or similar service
   - Monitor logs regularly

---

## Monitoring & Maintenance

### Daily Tasks
- Check application logs
- Monitor uptime
- Verify API health

### Weekly Tasks
- Database backup verification
- Performance metrics review
- User feedback check

### Monthly Tasks
- Security updates
- Dependency updates
- Cost review

### Emergency Procedures

**Application Won't Start**
1. Check logs: `heroku logs --tail`
2. Verify environment variables: `heroku config`
3. Check database connection: `heroku pg:psql`

**Database Issues**
1. Check database size: `heroku pg:info`
2. Run diagnostics: `heroku pg:diagnose`
3. Reset if necessary: `heroku pg:reset DATABASE`

---

## Environment Variables Reference

| Variable | Development | Production | Required |
|----------|-------------|-----------|----------|
| FLASK_ENV | development | production | ✓ |
| SECRET_KEY | dev-key | random-32-char | ✓ |
| ANTHROPIC_API_KEY | your-key | your-key | ✓ |
| DATABASE_URL | sqlite | postgresql | ✓ |
| PORT | 5000 | 5000 | ✗ |
| WORKERS | 1 | 4+ | ✗ |
| SESSION_COOKIE_SECURE | false | true | ✗ |

---

## Support & Troubleshooting

### Common Issues

**"No module named 'anthropic'"**
```bash
pip install -r requirements.txt
```

**"Database connection failed"**
```bash
# Check DATABASE_URL is set correctly
heroku config:get DATABASE_URL

# Reset if needed
heroku pg:reset DATABASE
```

**"Static files not loading"**
```bash
flask collect-static
git add static/
git commit -m "Update static files"
git push
```

---

## Rollback Procedure

```bash
# View deployment history
heroku releases

# Rollback to previous version
heroku releases:rollback
```

---

## Cost Estimation (Heroku)

- Dyno (web): $7/month (hobby-dev free tier available)
- PostgreSQL: $9/month (hobby tier)
- **Total**: ~$16/month

---

Last Updated: June 28, 2026
