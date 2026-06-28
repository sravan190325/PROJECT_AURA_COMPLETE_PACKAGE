#!/bin/bash

# PROJECT AURA - Automated Setup Script
# This script sets up the complete Project Aura application

echo "🎉 PROJECT AURA - Setup Script"
echo "================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python --version
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.11+"
    exit 1
fi

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
python -m venv venv
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
echo ""
echo "✓ Checking environment configuration..."
if [ ! -f .env ]; then
    echo "⚠️  .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "❗ IMPORTANT: Edit .env and add your Claude API key!"
    echo "   ANTHROPIC_API_KEY=sk-ant-your-key-here"
    echo ""
fi

# Create required directories
echo "✓ Creating required directories..."
mkdir -p uploads temp workbooks

# Show next steps
echo ""
echo "✅ Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "  1. Edit .env and add your Claude API key"
echo "  2. Run: python app.py"
echo "  3. Visit: http://localhost:5000"
echo ""
echo "🚀 Happy planning!"
