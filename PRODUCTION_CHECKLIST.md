# Project Aura - Production Readiness Checklist

Complete this checklist before deploying to production.

---

## Security

- [ ] **Secret Key**: Generate and set strong SECRET_KEY (32+ random characters)
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```

- [ ] **API Keys**: Add Claude API key to environment
  - [ ] ANTHROPIC_API_KEY configured
  - [ ] Key has proper permissions
  - [ ] Key is not in version control

- [ ] **Environment Variables**: All production vars set
  - [ ] FLASK_ENV=production
  - [ ] DATABASE_URL points to PostgreSQL
  - [ ] SESSION_COOKIE_SECURE=true
  - [ ] SESSION_COOKIE_HTTPONLY=true

- [ ] **Database**: Production database configured
  - [ ] PostgreSQL instance created
  - [ ] Database user with limited permissions
  - [ ] Backups enabled
  - [ ] SSL connections enabled

- [ ] **HTTPS**: SSL certificate configured
  - [ ] Domain has valid SSL cert
  - [ ] Heroku: Automatic (included)
  - [ ] Custom domain: Certificate installed
  - [ ] Redirect HTTP to HTTPS

- [ ] **File Uploads**: Secure upload handling
  - [ ] Max file size configured (10MB)
  - [ ] Allowed file types whitelisted
  - [ ] Upload directory permissions correct
  - [ ] Virus scanning (optional)

- [ ] **CORS & Headers**: Security headers configured
  - [ ] X-Frame-Options set
  - [ ] X-Content-Type-Options set
  - [ ] Content-Security-Policy configured

---

## Performance

- [ ] **Gunicorn Configuration**
  - [ ] Workers: (2 × CPU cores) + 1
  - [ ] Timeout: 120+ seconds
  - [ ] Worker class: sync or gevent (based on load)

- [ ] **Static Files**: Properly configured
  - [ ] CSS/JS files minified (optional)
  - [ ] CDN configured (optional)
  - [ ] Compression enabled
  - [ ] Cache headers set

- [ ] **Database**: Optimized
  - [ ] Indexes created
  - [ ] Connection pooling configured
  - [ ] Query optimization done
  - [ ] Slow query logging enabled

- [ ] **Caching**: Implemented where needed
  - [ ] Session caching configured
  - [ ] Redis/Memcached set up (optional)
  - [ ] Browser caching headers set

---

## Monitoring & Logging

- [ ] **Application Logging**
  - [ ] Logging level set to INFO
  - [ ] Logs written to file
  - [ ] Log rotation configured
  - [ ] Error tracking (Sentry) set up

- [ ] **Health Checks**
  - [ ] /health endpoint working
  - [ ] Uptime monitoring enabled
  - [ ] Response time monitoring
  - [ ] Error rate alerts configured

- [ ] **Database Monitoring**
  - [ ] Connection pool monitoring
  - [ ] Slow query logging
  - [ ] Disk space monitoring
  - [ ] Backup verification

- [ ] **Infrastructure Monitoring**
  - [ ] CPU usage monitoring
  - [ ] Memory usage monitoring
  - [ ] Disk space monitoring
  - [ ] Network monitoring

---

## Deployment

- [ ] **Code Quality**
  - [ ] No debug print statements
  - [ ] No TODO/FIXME comments
  - [ ] No hardcoded credentials
  - [ ] All tests passing

- [ ] **Version Control**
  - [ ] All code committed
  - [ ] No uncommitted changes
  - [ ] Git tags created for releases
  - [ ] CHANGELOG updated

- [ ] **Dependencies**
  - [ ] requirements.txt updated
  - [ ] All dependencies have versions
  - [ ] Security vulnerabilities checked
  - [ ] Python 3.11+ used

- [ ] **Configuration Files**
  - [ ] Procfile present
  - [ ] runtime.txt present (for Heroku)
  - [ ] .gitignore configured
  - [ ] .env.production configured

---

## Testing

- [ ] **Functional Testing**
  - [ ] Upload functionality works
  - [ ] Analysis generation works
  - [ ] Workbook download works
  - [ ] Form submissions work

- [ ] **Integration Testing**
  - [ ] Claude API integration works
  - [ ] Database operations work
  - [ ] File processing works
  - [ ] Error handling works

- [ ] **Security Testing**
  - [ ] No SQL injection vulnerabilities
  - [ ] No XSS vulnerabilities
  - [ ] CSRF protection enabled
  - [ ] Input validation works

- [ ] **Load Testing**
  - [ ] Application handles 10+ concurrent users
  - [ ] Database handles query load
  - [ ] File uploads process correctly
  - [ ] Response times acceptable

- [ ] **Browser Compatibility**
  - [ ] Chrome: ✓
  - [ ] Firefox: ✓
  - [ ] Safari: ✓
  - [ ] Edge: ✓
  - [ ] Mobile browsers: ✓

---

## Documentation

- [ ] **Code Documentation**
  - [ ] README.md complete
  - [ ] Code comments where needed
  - [ ] API endpoints documented
  - [ ] Setup instructions clear

- [ ] **Deployment Documentation**
  - [ ] DEPLOYMENT_GUIDE.md complete
  - [ ] Environment setup documented
  - [ ] Troubleshooting guide written
  - [ ] Rollback procedure documented

- [ ] **User Documentation**
  - [ ] User guide written
  - [ ] Video tutorials (optional)
  - [ ] FAQ section created
  - [ ] Support contact provided

---

## Pre-Launch

- [ ] **Stakeholder Approval**
  - [ ] Design approved
  - [ ] Functionality approved
  - [ ] Performance acceptable
  - [ ] Security reviewed

- [ ] **Backup & Recovery**
  - [ ] Database backups enabled
  - [ ] Backup tested & working
  - [ ] Recovery procedure documented
  - [ ] RTO/RPO defined

- [ ] **Incident Response**
  - [ ] On-call rotation established
  - [ ] Escalation procedure documented
  - [ ] Status page set up
  - [ ] Communication plan ready

- [ ] **Final Sign-off**
  - [ ] Product owner approval: [ ]
  - [ ] Security team approval: [ ]
  - [ ] Ops team approval: [ ]
  - [ ] Date approved: ___________

---

## Post-Launch

- [ ] **Launch Monitoring** (first 24 hours)
  - [ ] System metrics normal
  - [ ] Error rate low
  - [ ] No database issues
  - [ ] User feedback positive

- [ ] **Ongoing Maintenance**
  - [ ] Logs reviewed daily
  - [ ] Metrics tracked
  - [ ] Backups verified
  - [ ] Security updates applied

---

## Sign-Off

**Prepared by**: _____________________ **Date**: __________

**Reviewed by**: _____________________ **Date**: __________

**Approved by**: _____________________ **Date**: __________

---

Last Updated: June 28, 2026
