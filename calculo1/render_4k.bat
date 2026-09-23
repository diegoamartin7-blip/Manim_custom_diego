@echo off
REM ============================================================
REM  Doble clic: los 3 videos FINALES de Calculo 1 en 4K 60fps, 16:9.
REM  Todas las escenas corren en paralelo y cada video se une solo.
REM  Requiere: pip install manim, MiKTeX, ffmpeg en el PATH.
REM  Mas lento de lectura:  set C1_PACE=1.2  antes de la linea powershell.
REM ============================================================
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0render_all.ps1" -Mode 4k
echo.
echo  Videos: C1_V1_Probabilidad_Muy_Alta_4k.mp4, C1_V2_Probabilidad_Alta_4k.mp4, C1_V3_Probabilidad_Media_4k.mp4
pause
