@echo off
chcp 65001 >nul
title DARK DOMINION – Launcher

echo.
echo  ╔══════════════════════════════════════╗
echo  ║   DARK DOMINION – Dark Expansion    ║
echo  ║           Launcher v1.0             ║
echo  ╚══════════════════════════════════════╝
echo.

:: Najdi Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo  [CHYBA] Python nebyl nalezen!
    echo  Nainstaluj Python 3.10+ z https://python.org
    pause
    exit /b 1
)

echo  [OK] Python nalezen: 
python --version

echo.
echo  [*] Instalace zavislosti...
python -m pip install --upgrade pip --quiet
python -m pip install colorama windows-curses --quiet 2>nul

echo  [OK] Zavislosti nainstalovany.
echo.
echo  [*] Spousteni hry...
echo  ══════════════════════════════════════════
echo.

python main.py

echo.
echo  ══════════════════════════════════════════
echo  [*] Hra ukoncena. Nashledanou!
pause
