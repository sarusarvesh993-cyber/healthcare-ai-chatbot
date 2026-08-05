@echo off
title MediCare AI - Full Stack
echo ========================================
echo   MediCare AI - Healthcare Chatbot
echo   Starting Full Stack...
echo ========================================
echo.

cd /d C:\Users\lenovo\healthcare-chatbot
call venv\Scripts\activate

echo [1/2] Starting FastAPI Backend...
start "MediCare API" cmd /k "cd /d C:\Users\lenovo\healthcare-chatbot && call venv\Scripts\activate && python api.py"

timeout /t 5 /nobreak >nul

echo [2/2] Starting Streamlit Frontend...
echo.
echo ========================================
echo   Both services starting!
echo.
echo   Streamlit UI:  http://localhost:8501
echo   FastAPI Docs:  http://localhost:8000/docs
echo.
echo   Close this window to stop all services.
echo ========================================
echo.

streamlit run app.py
