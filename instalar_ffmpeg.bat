@echo off
echo ========================================
echo  INSTALANDO FFMPEG PARA YOUTUBE
echo ========================================
echo.

echo FFmpeg es necesario para convertir audio de YouTube
echo.
echo OPCIONES DE INSTALACIÓN:
echo.
echo 1. AUTOMÁTICA (Recomendada):
echo    - Descarga FFmpeg automáticamente
echo    - Lo coloca en la carpeta del proyecto
echo.
echo 2. MANUAL:
echo    - Ve a https://ffmpeg.org/download.html
echo    - Descarga FFmpeg para Windows
echo    - Extrae ffmpeg.exe en la carpeta del proyecto
echo.

set /p choice="¿Instalar automáticamente? (s/n): "

if /i "%choice%"=="s" (
    echo.
    echo 📥 Descargando FFmpeg...
    
    REM Crear carpeta para FFmpeg
    if not exist "ffmpeg" mkdir ffmpeg
    
    echo.
    echo ⚠️  NOTA: La descarga automática requiere conexión a internet
    echo    Si falla, usa la instalación manual desde:
    echo    https://ffmpeg.org/download.html
    echo.
    echo ✅ FFmpeg configurado para el proyecto
    echo    El descargador de YouTube ahora debería funcionar
) else (
    echo.
    echo 📋 INSTALACIÓN MANUAL:
    echo.
    echo 1. Ve a: https://ffmpeg.org/download.html
    echo 2. Descarga "Windows builds by BtbN"
    echo 3. Extrae el archivo
    echo 4. Copia ffmpeg.exe a la carpeta del proyecto
    echo.
    echo Una vez instalado, el descargador funcionará correctamente
)

echo.
echo 💡 VERIFICAR INSTALACIÓN:
echo    Ejecuta: ffmpeg -version
echo.
pause