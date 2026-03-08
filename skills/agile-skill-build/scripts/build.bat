@echo off
cd /d "%~dp0.."
python scripts\build.py
if %errorlevel% neq 0 (
  echo.
  echo If you see "The file cannot be accessed" or "cannot execute":
  echo   Python from Windows Store often breaks. Install from https://python.org
  echo   and ensure it is checked "Add to PATH" during install.
  exit /b 1
)
exit /b 0
