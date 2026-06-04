@echo off
REM Frontend development server for Windows

echo Starting Frontend Development Server...
echo.
echo The dashboard will be available at: http://localhost:3000
echo API endpoint: http://localhost:8000/api
echo.
echo To stop the server, press Ctrl+C
echo.

cd /d "%~dp0frontend"

if not exist "node_modules\" (
    echo ERROR: Dependencies not installed
    echo Please run: frontend-install.bat
    pause
    exit /b 1
)

call npm run dev
