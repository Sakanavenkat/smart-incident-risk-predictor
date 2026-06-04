@echo off
REM Run script for Windows development

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Starting FastAPI backend on port 8000...
echo.
echo Access the API at:
echo   - API Docs: http://localhost:8000/docs
echo   - Health: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn backend.app.main:app --reload --port 8000
