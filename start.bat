@echo off
REM Project Aura - Windows Startup Script

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║           PROJECT AURA - STARTUP SCRIPT                       ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ and add it to your PATH
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip list | findstr "Flask" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check .env file
if not exist .env (
    echo.
    echo WARNING: .env file not found
    echo Creating from .env.development...
    copy .env.development .env
    echo.
    echo Please edit .env and add your Claude API key:
    echo   ANTHROPIC_API_KEY=sk-ant-...
    echo.
    pause
)

REM Create necessary directories
if not exist uploads mkdir uploads
if not exist temp mkdir temp
if not exist workbooks mkdir workbooks

REM Set environment
set FLASK_ENV=development
set FLASK_APP=app.py

REM Display startup info
echo.
echo ═══════════════════════════════════════════════════════════════
echo Configuration:
echo ═══════════════════════════════════════════════════════════════
echo Flask Environment: %FLASK_ENV%
echo Python:
python --version
echo.

REM Start the server
echo Starting Project Aura...
echo.
echo ✓ Server running on http://localhost:5000
echo ✓ Press CTRL+C to stop
echo.

python app.py

pause
