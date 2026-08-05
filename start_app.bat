@echo off
title MediCare AI - Healthcare Chatbot
echo ========================================
echo   MediCare AI - Healthcare Chatbot
echo ========================================
echo.
echo Starting Streamlit server...
echo.
cd /d C:\Users\lenovo\healthcare-chatbot
call venv\Scripts\activate
echo Opening browser at http://localhost:8501
echo.
streamlit run app.py
pause
