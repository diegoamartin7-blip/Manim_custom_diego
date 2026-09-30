@echo off
REM ============================================================
REM  Doble clic: SOLO el video de teoria aplicada (GAL1_V1) en 4K.
REM  (El de ejercicios ya lo tenes; este no lo vuelve a hacer.)
REM  Si una escena se cuelga mas de 4 horas, se corta sola y te avisa.
REM ============================================================
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0render_all.ps1" -Mode 4k -Video 1
echo.
echo  Video: GAL1_V1_Teoria_Aplicada_4k.mp4
pause
