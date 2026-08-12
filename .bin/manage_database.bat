@echo off
REM manage_database.bat - Launch manage_database.py (Thorne-EQ DB operator)
REM Usage:
REM   manage_database.bat status
REM   manage_database.bat import --dump server\utils\sql\database_full\quarm_<date>.tar.gz
REM   manage_database.bat backup
REM   manage_database.bat gm --account <name>
REM   manage_database.bat query "SELECT COUNT(*) FROM spells_new"

setlocal EnableDelayedExpansion
set "SCRIPT_DIR=%~dp0"
set "PYEXE=%SCRIPT_DIR%..\.venv\Scripts\python.exe"
if not exist "%PYEXE%" set "PYEXE=python"

"%PYEXE%" "%SCRIPT_DIR%manage_database.py" %*
exit /b %errorlevel%
