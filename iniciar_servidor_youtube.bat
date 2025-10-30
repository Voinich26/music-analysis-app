@echo off
echo ========================================
echo 🎵 INICIANDO SERVIDOR YOUTUBE
echo ========================================
echo.

echo Verificando entorno virtual...
if not exist ".venv\Scripts\python.exe" (
    echo ❌ Entorno virtual no encontrado
    echo Ejecuta primero: python -m venv .venv
    pause
    exit /b 1
)

echo ✅ Entorno virtual encontrado

echo.
echo Verificando dependencias...
.\.venv\Scripts\python.exe -c "import flask, yt_dlp; print('✅ Dependencias OK')" 2>nul
if errorlevel 1 (
    echo ❌ Faltan dependencias, instalando...
    .\.venv\Scripts\pip.exe install flask flask-cors yt-dlp
)

echo.
echo 🚀 Iniciando servidor backend de YouTube...
echo 🌐 Servidor disponible en: http://localhost:5005
echo 📁 Descargas se guardan en: ./downloads/
echo.
echo ⚠️ Para detener el servidor, presiona Ctrl+C
echo.

.\.venv\Scripts\python.exe backend_youtube.py