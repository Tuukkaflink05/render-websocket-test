@echo off
REM Launches the chat server and two chat clients, each in its own cmd window.
REM Assumes server.py and client.py are in the same folder as this .bat file.

cd /d "%~dp0"

start "Server" cmd /k py server.py
timeout /t 1 /nobreak >nul

start "Client 1" cmd /k py client.py tuke
start "Client 2" cmd /k py client.py jeesbox
REM start "Client 3" cmd /k py client.py
