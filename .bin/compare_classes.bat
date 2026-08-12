@echo off
REM compare_classes.bat - Launch compare_classes.py (class/spell analyzer)
REM Usage:
REM   compare_classes.bat summary
REM   compare_classes.bat candidates --base Necromancer --secondary Magician --maxlevel 20
REM   compare_classes.bat shared --a Necromancer --b Magician

setlocal EnableDelayedExpansion
set "SCRIPT_DIR=%~dp0"
set "PYEXE=%SCRIPT_DIR%..\.venv\Scripts\python.exe"
if not exist "%PYEXE%" set "PYEXE=python"

"%PYEXE%" "%SCRIPT_DIR%compare_classes.py" %*
exit /b %errorlevel%
