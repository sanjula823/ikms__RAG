#!/bin/bash
# Setup script for IKMS Multi-Agent RAG

set -e

echo "=========================================="
echo "IKMS Multi-Agent RAG - Setup Script"
echo "=========================================="

# Check Python installation
echo "Checking Python installation..."
python --version || { echo "Python 3.11+ is required"; exit 1; }

# Create virtual environment
echo "Creating Python virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f venv/Scripts/activate ]; then
    source venv/Scripts/activate  # Windows Git Bash
elif [ -f venv/bin/activate ]; then
    source venv/bin/activate  # Linux/Mac
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - PINECONE_API_KEY"
    echo "   - PINECONE_ENVIRONMENT"
fi

# Create data and logs directories
echo "Creating data and logs directories..."
mkdir -p data logs

echo ""
echo "=========================================="
echo "✅ Setup completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Update .env with your API credentials"
echo "2. Run: python -m uvicorn src.app.api:app --reload"
echo "3. Frontend: cd frontend && npm install && npm start"
echo ""
