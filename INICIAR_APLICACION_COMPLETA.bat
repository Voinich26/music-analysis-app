@echo off
title MUSIC ANALYSIS - INICIADOR ROBUSTO
color 0A

echo ========================================
echo   MUSIC ANALYSIS - INICIADOR ROBUSTO
echo ========================================
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

echo [PASO 1] Limpiando procesos anteriores...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM go.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo [PASO 2] Verificando dependencias...
go version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Go no instalado
    echo    Descarga desde: https://golang.org/dl/
    pause
    exit /b 1
)

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no instalado
    echo    Descarga desde: https://python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Dependencias verificadas

echo [PASO 3] Configurando entorno Python...
if not exist ".venv" (
    echo Creando entorno virtual...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo [PASO 4] Instalando dependencias básicas...
pip install --quiet flask flask-cors yt-dlp librosa numpy scipy soundfile

echo [PASO 5] Iniciando Backend Principal (Puerto 3001)...
cd backend
start "BACKEND-MUSIC-ANALYSIS" /MIN cmd /c "echo Backend iniciado && go run main.go && pause"
cd ..
timeout /t 3 /nobreak >nul

echo [PASO 6] Iniciando Servidor YouTube (Puerto 5005)...
start "YOUTUBE-SERVER" /MIN cmd /c "call .venv\Scripts\activate.bat && python backend_youtube.py && pause"
timeout /t 3 /nobreak >nul

echo [PASO 7] Iniciando Frontend (Puerto 8081)...
start "FRONTEND-SERVER" /MIN cmd /c "call .venv\Scripts\activate.bat && python servidor_frontend.py && pause"
timeout /t 3 /nobreak >nul

echo [PASO 8] Verificando servicios...
:check_services
echo Verificando Backend Principal...
curl -s http://localhost:3001/api/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ⏳ Esperando Backend Principal...
    timeout /t 2 /nobreak >nul
    goto check_services
)

echo Verificando Servidor YouTube...
curl -s http://localhost:5005/api/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ⏳ Esperando Servidor YouTube...
    timeout /t 2 /nobreak >nul
    goto check_services
)

echo Verificando Frontend...
curl -s http://localhost:8081 >nul 2>&1
if %errorlevel% neq 0 (
    echo ⏳ Esperando Frontend...
    timeout /t 2 /nobreak >nul
    goto check_services
)

echo.
echo ========================================
echo 🎉 APLICACIÓN INICIADA CORRECTAMENTE
echo ========================================
echo.
echo 🌐 Frontend:        http://localhost:8081
echo 🔧 Backend:         http://localhost:3001
echo 🎵 YouTube Server:  http://localhost:5005
echo.
echo ✅ TODOS LOS SERVICIOS FUNCIONANDO
echo.
echo 🚀 Abriendo navegador...
start http://localhost:8081

echo.
echo 💡 INSTRUCCIONES:
echo   • La aplicación está lista para usar
echo   • Puedes subir archivos MP3/WAV
echo   • Puedes descargar de YouTube
echo   • Para cerrar: ejecuta DETENER_APLICACION.bat
echo.
echo ⚠️ NO CIERRES ESTA VENTANA
echo    (Se cerrará automáticamente en 10 segundos)
echo.

timeout /t 10 /nobreak >nul
exit