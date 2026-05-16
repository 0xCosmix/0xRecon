@echo off
title 0xRecon — Windows Installer
color 0A

echo.
echo   ██████╗ ██╗  ██╗██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
echo  ██╔═████╗╚██╗██╔╝██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
echo  ██║██╔██║ ╚███╔╝ ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
echo  ████╔╝██║ ██╔██╗ ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
echo  ╚██████╔╝██╔╝ ██╗██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
echo   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
echo.
echo   // OSINT Framework -- Windows Installer
echo   // by 0xCosmix
echo.

:: Check Python
echo [*] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found!
    echo [!] Download from https://python.org and rerun this script.
    echo [!] Make sure to check "Add Python to PATH" during install!
    pause
    exit /b 1
)
echo [OK] Python found

:: Upgrade pip
echo.
echo [*] Upgrading pip...
python -m pip install --upgrade pip -q

:: Install packages
echo.
echo [*] Installing dependencies...

python -m pip install PyQt6 -q
echo [OK] PyQt6

python -m pip install requests -q
echo [OK] requests

python -m pip install dnspython -q
echo [OK] dnspython

python -m pip install python-whois -q
echo [OK] python-whois

python -m pip install reportlab -q
echo [OK] reportlab

python -m pip install networkx -q
echo [OK] networkx

python -m pip install pillow -q
echo [OK] pillow

:: Create launcher
echo.
echo [*] Creating launcher...
set SCRIPT_DIR=%~dp0

echo @echo off > "%USERPROFILE%\Desktop\0xRecon.bat"
echo cd /d "%SCRIPT_DIR%" >> "%USERPROFILE%\Desktop\0xRecon.bat"
echo python 0xrecon_gui.py >> "%USERPROFILE%\Desktop\0xRecon.bat"

echo [OK] Desktop launcher created

echo.
echo ================================================
echo   Installation complete!
echo ================================================
echo.
echo   Launch options:
echo   1. Double-click 0xRecon.bat on Desktop
echo   2. Run: python 0xrecon_gui.py
echo.
echo   Only use on authorized systems.
echo.
pause
