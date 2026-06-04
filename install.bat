@echo off
REM Setup script for Windows

echo Creating Python virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install --upgrade pip setuptools wheel
pip install -r backend/requirements.txt

echo Setup complete!
echo.
echo To start the backend, run:
echo   .venv\Scripts\activate.bat
echo   uvicorn backend.app.main:app --reload --port 8000
echo.
echo Backend API docs will be available at: http://localhost:8000/docs
