@echo off
echo ========================================
echo  INSTALANDO DEPENDENCIAS PARA SHAZAM
echo ========================================
echo.

echo [1/3] Activando entorno virtual...
cd python_audio
call venv\Scripts\activate.bat

echo [2/3] Instalando dependencias básicas para identificación...
pip install requests urllib3 beautifulsoup4

echo [3/3] Instalando dependencias para descarga de YouTube...
echo.
echo 🚀 ¿Instalar descargador de YouTube? (Recomendado)
echo    - yt-dlp: Descargador moderno y actualizado
echo    - pytube: Alternativa ligera
echo    - pydub: Conversión de formatos
echo.
set /p install_youtube="Instalar descargador de YouTube? (s/n): "
if /i "%install_youtube%"=="s" (
    echo Instalando yt-dlp...
    pip install yt-dlp
    
    echo Instalando pytube como alternativa...
    pip install pytube
    
    echo Instalando pydub para conversión...
    pip install pydub
    
    echo ✅ Descargador de YouTube instalado
) else (
    echo ⚠️  Continuando sin descargador de YouTube
)

echo.
echo ========================================
echo 🎉 DEPENDENCIAS INSTALADAS
echo ========================================
echo.
echo ✅ Funcionalidades disponibles:
echo   • Identificación de canciones tipo Shazam
echo   • Búsqueda de letras automática
echo   • Enlaces a plataformas de música
if /i "%install_youtube%"=="s" (
    echo   • Descarga desde YouTube
)
echo.
echo 💡 Para probar las funcionalidades:
echo   • Ejecuta: python test_shazam_integration.py
echo   • O usa la aplicación web normalmente
echo.
pause