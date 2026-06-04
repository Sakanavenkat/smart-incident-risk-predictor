@echo off
REM Frontend installation script for Windows

echo Installing Frontend Dependencies...
echo.

cd /d "%~dp0frontend"

if not exist "node_modules\" (
    echo [1/2] Installing npm packages...
    call npm install
    if errorlevel 1 (
        echo ERROR: npm install failed
        exit /b 1
    )
)

echo.
echo [2/2] Installation complete!
echo.
echo To start the frontend development server, run:
echo   frontend-run.bat
echo.
pause
