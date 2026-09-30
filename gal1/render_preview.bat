@echo off
REM Doble clic: vista previa RAPIDA (480p) de los 2 videos de GAL 1, para probar.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0render_all.ps1" -Mode preview
pause
