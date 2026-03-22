@echo off
cd /d "%~dp0"
echo Starting Skin Disease Detection API...
py -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
pause
