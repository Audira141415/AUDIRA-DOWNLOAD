@echo off
title AUDIRA Download Manager - Key Generator
echo ========================================================
echo  AUDIRA DOWNLOAD MANAGER (ADM) - GENERATOR LISENSI
echo  Author: Agus Dwi Rianto (AUDIRA MDA / ASM)
echo ========================================================
echo.

set /p OWNER="Masukkan Nama Pemilik (contoh: Agus Dwi Rianto): "
set /p EMAIL="Masukkan Email Pemilik (contoh: agus@audira.my.id): "
set /p TIER="Pilih Tipe Paket [LIFE / YEAR] (default: LIFE): "

if "%TIER%"=="" set TIER=LIFE

node scripts/generate-adm-license.mjs --name "%OWNER%" --email "%EMAIL%" --tier "%TIER%"

echo.
pause

