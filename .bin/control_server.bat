@echo off
REM control_server.bat - Launch control_server.py (Thorne-EQ server orchestrator)
REM Usage:
REM   control_server.bat assemble          (build/refresh the run directory)
REM   control_server.bat start             (start shared_memory -> loginserver -> world -> zone)
REM   control_server.bat status            (show process/port status)
REM   control_server.bat stop              (stop all server processes)
REM   control_server.bat mariadb           (start portable MariaDB in the foreground)

setlocal EnableDelayedExpansion
set "SCRIPT_DIR=%~dp0"
set "PYEXE=%SCRIPT_DIR%..\.venv\Scripts\python.exe"
if not exist "%PYEXE%" set "PYEXE=python"

"%PYEXE%" "%SCRIPT_DIR%control_server.py" %*
exit /b %errorlevel%
