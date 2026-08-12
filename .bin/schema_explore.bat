@echo off
REM schema_explore.bat - Launch schema_explore.py (read-only schema/data explorer)
REM Usage:
REM   schema_explore.bat --db --database quarm --user root
REM   schema_explore.bat --sql-dir server\utils\sql\database_full

setlocal EnableDelayedExpansion
set "SCRIPT_DIR=%~dp0"
set "PYEXE=%SCRIPT_DIR%..\.venv\Scripts\python.exe"
if not exist "%PYEXE%" set "PYEXE=python"

"%PYEXE%" "%SCRIPT_DIR%schema_explore.py" %*
exit /b %errorlevel%
