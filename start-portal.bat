@echo off
title AUDIRA Download Manager - Central Portal & Licensing Server
echo ========================================================
echo  AUDIRA DOWNLOAD MANAGER (ADM) - PORTAL & LICENSING
echo  Author: Agus Dwi Rianto (AUDIRA MDA / ASM)
echo  Website: https://audira.my.id
echo ========================================================
echo.
echo Starting Web Portal on http://localhost:5060 ...
echo [Landing Page] http://localhost:5060/
echo [Fleet Portal] http://localhost:5060/portal  (audira / Sigma1993)
echo [License API]  http://localhost:5060/api/v1/licenses
echo.

start "" "http://localhost:5060/"
python server/adm_portal.py --port 5060
pause

