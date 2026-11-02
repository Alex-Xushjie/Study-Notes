@echo off
cd /d "%~dp0"
if not exist ".venv312\Scripts\python.exe" (
 echo Python environment not found. Please read README.md.
 pause
 exit /b 1
)
".venv312\Scripts\python.exe" -m gui.main
if errorlevel 1 pause
