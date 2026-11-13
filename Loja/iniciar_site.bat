@echo off
title NexusCore - Servidor Flask
echo ==============================================
echo   Iniciando o servidor Flask do NexusCore...
echo ==============================================
echo.
cd /d "%~dp0BackEndmes06"

if exist "C:\Users\Wendel\.local\bin\python3.15.exe" (
    "C:\Users\Wendel\.local\bin\python3.15.exe" app.py
) else if exist "C:\Users\Wendel\AppData\Local\Programs\Python\Python312\python.exe" (
    "C:\Users\Wendel\AppData\Local\Programs\Python\Python312\python.exe" app.py
) else (
    python app.py
)

pause
