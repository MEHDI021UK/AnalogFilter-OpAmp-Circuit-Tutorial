@echo off
setlocal EnableExtensions
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo.
    echo Python was not found in PATH.
    echo Install it from https://www.python.org/downloads/ and tick "Add python.exe to PATH".
    echo.
    pause
    exit /b 1
)

echo.
echo Checking dependencies ^(requirments.txt^)...
python -m pip install -r "%~dp0requirments.txt"
if errorlevel 1 (
    echo.
    echo Could not install requirements. See errors above.
    pause
    exit /b 1
)

echo.
echo Starting Analog Tutorial...
python "%~dp0main.py"
set "EXITCODE=%ERRORLEVEL%"
if not "%EXITCODE%"=="0" (
    echo.
    echo The app exited with an error ^(code %EXITCODE%^).
    pause
)
exit /b %EXITCODE%
