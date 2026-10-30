@echo off
setlocal
title AUDIRA Download Manager - Web Portal Preview

echo ======================================================================
echo           AUDIRA DOWNLOAD MANAGER - Official Web Portal                
echo           Created by Agus Dwi R (AUDIRA)                             
echo ======================================================================
echo.
echo [*] Menjalankan server lokal di http://localhost:5050 ...
echo [*] Membuka browser default secara otomatis...
echo.

start "" "http://localhost:5050"

python server\adm_portal.py --port 5050
if %errorlevel% neq 0 (
    python -m http.server 5050 --directory "%~dp0web"
)
pause

