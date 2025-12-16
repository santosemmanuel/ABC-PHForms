@echo off
title Flask Project Launcher

REM === Change these paths to match your project ===
set PROJECT_DIR=C:\Users\Client-PC\Desktop\Animal Bite Philhealth Forms\ABC-PHForms
set VENV_DIR=%PROJECT_DIR%\venv
set FLASK_APP=app.py

REM === Go to project folder ===
cd /d %PROJECT_DIR%

REM === Activate Virtual Environment ===
call %VENV_DIR%\Scripts\activate

REM === (Optional) Open browser automatically ===
start "" http://127.0.0.1:5000

REM === Run Flask ===
flask run --host=0.0.0.0

pause


