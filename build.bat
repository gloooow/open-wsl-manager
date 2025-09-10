@echo off
echo WSL Manager - Executable Builder
echo ================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Run the build script
python build.py

REM Pause to show results
pause
