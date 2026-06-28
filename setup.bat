@echo off
REM PROJECT AURA - Automated Setup Script (Windows)
REM This script sets up the complete Project Aura application

echo.
echo 🎉 PROJECT AURA - Setup Script (Windows)
echo ========================================
echo.

REM Check Python version
echo ✓ Checking Python version...
python --version
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+
    exit /b 1
)

REM Create virtual environment
echo.
echo ✓ Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo ✓ Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
echo.
echo ✓ Checking environment configuration...
if not exist .env (
    echo ⚠️  .env file not found
    echo Creating .env from .env.example...
    copy .env.example .env
    echo ❗ IMPORTANT: Edit .env and add your Claude API key!
    echo    ANTHROPIC_API_KEY=sk-ant-your-key-here
    echo.
)

REM Create required directories
echo ✓ Creating required directories...
if not exist uploads mkdir uploads
if not exist temp mkdir temp
if not exist workbooks mkdir workbooks

REM Show next steps
echo.
echo ✅ Setup Complete!
echo.
echo 📋 Next Steps:
echo   1. Edit .env and add your Claude API key
echo   2. Run: python app.py
echo   3. Visit: http://localhost:5000
echo.
echo 🚀 Happy planning!
pause
