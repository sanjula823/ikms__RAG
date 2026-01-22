@echo off
REM Setup script for IKMS Multi-Agent RAG (Windows)

echo.
echo ==========================================
echo IKMS Multi-Agent RAG - Setup Script
echo ==========================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python 3.11+ is required but not found
    exit /b 1
)

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo [WARNING] Please update .env with your API keys:
    echo    - OPENAI_API_KEY
    echo    - PINECONE_API_KEY
    echo    - PINECONE_ENVIRONMENT
)

REM Create data and logs directories
echo Creating data and logs directories...
if not exist data mkdir data
if not exist logs mkdir logs

echo.
echo ==========================================
echo Setup completed successfully!
echo ==========================================
echo.
echo Next steps:
echo 1. Update .env with your API credentials
echo 2. Run: python -m uvicorn src.app.api:app --reload
echo 3. Frontend: cd frontend ^&^& npm install ^&^& npm start
echo.
pause
