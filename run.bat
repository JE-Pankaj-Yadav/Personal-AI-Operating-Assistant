@echo off
setlocal
set "ROOT=%~dp0"
for %%I in ("%ROOT%.") do set "ROOT=%%~fI"
echo PA NEXUS root: %ROOT%
powershell -NoProfile -ExecutionPolicy Bypass -File "%ROOT%\run.ps1"
if errorlevel 1 (echo RUN FAILED. & exit /b %errorlevel%)
