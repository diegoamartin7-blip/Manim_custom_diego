@echo off
REM ============================================================
REM  GAL 1 - Descarga lo ultimo del repo y renderiza los 2 videos en 4K.
REM  Ponelo en una carpeta vacia (ej: Documentos\GAL1) y doble clic.
REM ============================================================
setlocal
cd /d "%~dp0"
set "ZIP=%TEMP%\gal1_repo.zip"
set "TMPD=%TEMP%\gal1_repo"
echo Descargando el repo...
powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol='Tls12'; Invoke-WebRequest -UseBasicParsing -Uri 'https://github.com/diegoamartin7-blip/Manim_custom_diego/archive/refs/heads/claude/manim-test-video-2plus2-sdwryu.zip' -OutFile '%ZIP%'"
if errorlevel 1 ( echo No pude descargar. Revisa internet. & pause & exit /b 1 )
if exist "%TMPD%" rmdir /s /q "%TMPD%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Force '%ZIP%' '%TMPD%'"
for /d %%D in ("%TMPD%\*") do set "SRC=%%D"
robocopy "%SRC%\gal1" "%~dp0gal1" /E /NFL /NDL /NJH /NJS /XD media logs snaps >nul
robocopy "%SRC%\gal1_teoria" "%~dp0gal1_teoria" GAL1_teoria_1er_parcial.pdf verify.py /NFL /NDL /NJH /NJS >nul
echo Listo. El libro quedo en gal1_teoria\GAL1_teoria_1er_parcial.pdf
echo Arranca el render 4K (dejalo corriendo)...
call "%~dp0gal1\render_4k.bat"
endlocal
