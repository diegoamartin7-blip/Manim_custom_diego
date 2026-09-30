@echo off
REM ============================================================
REM  Doble clic: renderiza SOLO las 3 escenas que fallaron por memoria
REM  (de a 3, sin llenar la RAM) y une los 2 videos:
REM    GAL1_V1_Teoria_Aplicada_4k.mp4 y GAL1_V2_Ejercicios_Parcial_4k.mp4
REM ============================================================
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0render_all.ps1" -Mode 4k -Only V1_07_Rango,V1_08_Determinante,V2_10_Cierre -MaxParallel 3
echo.
echo  Listo. Los videos quedaron en esta carpeta.
pause
