@echo off
title MediCare AI - FastAPI Backend
echo ========================================
echo   MediCare AI - FastAPI Backend
echo ========================================
echo.
echo Starting FastAPI server...
echo.
cd /d C:\Users\lenovo\healthcare-chatbot
call venv\Scripts\activate
echo API docs at http://localhost:8000/docs
echo.
python api.py
pause
