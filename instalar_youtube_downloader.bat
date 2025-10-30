@echo off
echo ========================================
echo INSTALADOR DE DEPENDENCIAS YOUTUBE
echo ========================================
echo.

echo Activando entorno virtual...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Entorno virtual activado
) else (
    echo ⚠️ Entorno virtual no encontrado, usando Python global
)

echo.
echo Instalando dependencias de YouTube...
pip install --upgrade pip
pip install -r python_audio\requirements_youtube.txt

echo.
echo Verificando instalación de yt-dlp...
python -c "import yt_dlp; print('✅ yt-dlp instalado correctamente')" 2>nul || echo "❌ Error con yt-dlp"

echo.
echo Verificando instalación de pytube...
python -c "import pytube; print('✅ pytube instalado correctamente')" 2>nul || echo "❌ Error con pytube"

echo.
echo Probando descargador...
cd python_audio
python youtube_downloader_enhanced.py --test

echo.
echo ========================================
echo INSTALACIÓN COMPLETADA
echo ========================================
echo.
echo Para usar el descargador:
echo   cd python_audio
echo   python youtube_downloader_enhanced.py "URL_DE_YOUTUBE" --audio
echo.
pause