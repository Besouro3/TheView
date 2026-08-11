@echo off
title The View - Dashboard
cd /d "%~dp0.."
start "" http://localhost:8501
".venv\Scripts\python.exe" -m streamlit run app.py
