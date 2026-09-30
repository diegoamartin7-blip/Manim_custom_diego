@echo off
REM ============================================================
REM  Doble clic: los 2 videos de GAL 1 en 4K 60fps, 16:9.
REM  Todas las escenas corren en paralelo y cada video se une solo.
REM  Requiere: pip install manim, MiKTeX, ffmpeg en el PATH.
REM  Mas lento de lectura:  set G1_PACE=1.2  antes de la linea powershell.
REM ============================================================
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0render_all.ps1" -Mode 4k
echo.
echo  Videos: GAL1_V1_Teoria_Aplicada_4k.mp4 y GAL1_V2_Ejercicios_Parcial_4k.mp4
pause
