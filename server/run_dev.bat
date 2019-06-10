@echo off
echo Setting up Flask Server in development mode...
set FLASK_APP=server.py
pause
python -m flask run
