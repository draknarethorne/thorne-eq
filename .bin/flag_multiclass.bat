@echo off
REM flag_multiclass.bat - Launch flag_multiclass.py (Phase 1 multi-class spike helper)
REM Usage:
REM   flag_multiclass.bat list   --class Necromancer
REM   flag_multiclass.bat check  --class Necromancer --spells 1,2,3
REM   flag_multiclass.bat grant  --class Necromancer --spells 1..20 --from Magician
REM   flag_multiclass.bat revoke --class Necromancer

setlocal EnableDelayedExpansion
set "SCRIPT_DIR=%~dp0"
set "PYEXE=%SCRIPT_DIR%..\.venv\Scripts\python.exe"
if not exist "%PYEXE%" set "PYEXE=python"

"%PYEXE%" "%SCRIPT_DIR%flag_multiclass.py" %*
exit /b %errorlevel%
