@echo off
echo ========================================
echo  MUSIC ANALYSIS - APLICACION AVANZADA
echo ========================================
echo.

echo [1/4] Verificando dependencias...
cd /d "%~dp0"

echo Verificando Go...
go version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Go no está instalado o no está en el PATH
    echo    Instala Go desde: https://golang.org/dl/
    pause
    exit /b 1
)

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo    Instala Python desde: https://python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Dependencias básicas verificadas
echo.

echo [2/4] Configurando análisis avanzado...
cd python_audio

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual Python...
    python -m venv venv
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar dependencias básicas
python -c "import librosa" >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias básicas...
    pip install librosa numpy scipy soundfile
)

REM Verificar dependencias avanzadas
python -c "import madmom, whisper" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo 🚀 ¿Instalar análisis avanzado con IA? (Recomendado)
    echo    - Detección de acordes con deep learning
    echo    - Reconocimiento de voz con Whisper AI
    echo    - Identificación musical tipo Shazam
    echo.
    set /p install_advanced="Instalar análisis avanzado? (s/n): "
    if /i "!install_advanced!"=="s" (
        echo Instalando dependencias avanzadas...
        pip install madmom openai-whisper music21 aubio
        echo ✅ Análisis avanzado instalado
    ) else (
        echo ⚠️  Continuando con análisis básico
    )
) else (
    echo ✅ Análisis avanzado disponible
)

cd ..
echo.

echo [3/4] Iniciando Backend (Puerto 3001)...
cd backend
start "Backend - Music Analysis Avanzado" cmd /k "echo 🎵 Servidor backend con IA iniciado && go run main.go"
cd ..

echo Esperando 5 segundos para que el backend se inicie...
timeout /t 5 /nobreak >nul

echo [4/4] Iniciando Frontend (Puerto 8081)...
start "Frontend - Music Analysis" cmd /k "python servidor_frontend.py"

echo.
echo ========================================
echo 🎉 APLICACIÓN AVANZADA INICIADA
echo ========================================
echo.
echo 🌐 Frontend: http://localhost:8081
echo 🔧 Backend:  http://localhost:3001
echo.
echo 🚀 Funcionalidades disponibles:
echo   ✓ Análisis de tonalidad con múltiples algoritmos
echo   ✓ Detección de acordes con IA (madmom)
echo   ✓ Identificación musical tipo Shazam
echo   ✓ Reconocimiento de voz con Whisper AI
echo   ✓ Análisis armónico completo
echo   ✓ Exportación en múltiples formatos
echo.
echo 💡 Consejos:
echo   • Usa archivos MP3/WAV de buena calidad
echo   • El análisis puede tomar 30-60 segundos
echo   • Para mejores resultados, usa música con instrumentos claros
echo.
echo Abriendo navegador en 3 segundos...
timeout /t 3 /nobreak >nul
start http://localhost:8081

echo.
echo Para instalar más funciones: instalar_dependencias_avanzadas.bat
echo Para probar el sistema: cd python_audio && python test_advanced_analysis.py
echo Para detener: Cierra las ventanas o ejecuta liberar_puertos.bat
echo.
pause
