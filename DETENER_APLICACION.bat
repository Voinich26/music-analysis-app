@echo off
title MUSIC ANALYSIS - DETENIENDO SERVICIOS
color 0C

echo ========================================
echo   DETENIENDO MUSIC ANALYSIS
echo ========================================
echo.

echo [1] Cerrando ventanas de servidores...
taskkill /F /FI "WINDOWTITLE eq BACKEND-MUSIC-ANALYSIS*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq YOUTUBE-SERVER*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq FRONTEND-SERVER*" >nul 2>&1

echo [2] Terminando procesos Python...
taskkill /F /IM python.exe >nul 2>&1

echo [3] Terminando procesos Go...
taskkill /F /IM go.exe >nul 2>&1

echo [4] Liberando puertos...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3001') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5005') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8081') do taskkill /F /PID %%a >nul 2>&1

timeout /t 2 /nobreak >nul

echo.
echo ✅ APLICACIÓN DETENIDA CORRECTAMENTE
echo.
echo 💡 Para volver a iniciar, ejecuta:
echo    INICIAR_APLICACION_COMPLETA.bat
echo.
pause