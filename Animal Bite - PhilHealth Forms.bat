@echo off

REM ==== CHANGE THESE PATHS ====
set FLASK_APP=app.py
set FLASK_PORT=5000

REM ==== OPEN BROWSER ====
start http://127.0.0.1:%FLASK_PORT%

REM ==== RUN FLASK ====
flask run --host=0.0.0.0 --port=%FLASK_PORT%


