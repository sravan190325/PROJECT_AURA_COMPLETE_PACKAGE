#!/bin/bash

# Project Aura - Unix/Linux/Mac Startup Script

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           PROJECT AURA - STARTUP SCRIPT                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.11+ first"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python ${PYTHON_VERSION} found"

# Check if requirements are installed
echo "Checking dependencies..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

# Check .env file
if [ ! -f .env ]; then
    echo ""
    echo "WARNING: .env file not found"
    echo "Creating from .env.development..."
    cp .env.development .env
    echo ""
    echo "Please edit .env and add your Claude API key:"
    echo "  ANTHROPIC_API_KEY=sk-ant-..."
    echo ""
fi

# Create necessary directories
mkdir -p uploads temp workbooks

# Set environment
export FLASK_ENV=development
export FLASK_APP=app.py

# Display startup info
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Configuration:"
echo "═══════════════════════════════════════════════════════════════"
echo "Flask Environment: ${FLASK_ENV}"
echo "Python: $(python3 --version)"
echo ""

# Start the server
echo "Starting Project Aura..."
echo ""
echo "✓ Server running on http://localhost:5000"
echo "✓ Press CTRL+C to stop"
echo ""

python3 app.py
