@echo off
echo ========================================
echo    LIBERAR PUERTOS - MUSIC ANALYSIS
echo ========================================
echo.

echo 🔍 Verificando puertos ocupados...

echo.
echo Puerto 3000:
netstat -ano | findstr :3000
if %errorlevel% equ 0 (
    echo ⚠️  Puerto 3000 está ocupado
    echo    Para liberarlo, ejecuta: taskkill /F /PID [PID_NUMBER]
) else (
    echo ✅ Puerto 3000 libre
)

echo.
echo Puerto 3001:
netstat -ano | findstr :3001
if %errorlevel% equ 0 (
    echo ⚠️  Puerto 3001 está ocupado
    echo    Para liberarlo, ejecuta: taskkill /F /PID [PID_NUMBER]
) else (
    echo ✅ Puerto 3001 libre
)

echo.
echo Puerto 8080:
netstat -ano | findstr :8080
if %errorlevel% equ 0 (
    echo ⚠️  Puerto 8080 está ocupado
    echo    Para liberarlo, ejecuta: taskkill /F /PID [PID_NUMBER]
) else (
    echo ✅ Puerto 8080 libre
)

echo.
echo 💡 Si necesitas liberar un puerto:
echo    1. Copia el PID del proceso que quieres cerrar
echo    2. Ejecuta: taskkill /F /PID [PID_NUMBER]
echo    3. O usa: netstat -ano | findstr :PUERTO
echo.
pause

