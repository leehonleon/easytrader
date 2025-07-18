@echo off
echo %~dp0
cd /d %~dp0
call .\.venv\Scripts\activate
python main.py
