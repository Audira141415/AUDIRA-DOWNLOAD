@echo off
setlocal
title AUDIRA Download Manager - Web Portal

echo [*] Menjalankan server static web di http://localhost:5050 ...
start "" "http://localhost:5050"
python -m http.server 5050
pause

