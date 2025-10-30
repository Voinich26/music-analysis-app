@echo off
echo ========================================
echo  GESTOR DE BASE DE DATOS DE CANCIONES
echo ========================================
echo.

echo Activando entorno virtual...
cd python_audio
call venv\Scripts\activate.bat

echo.
echo 🎵 Iniciando gestor de base de datos...
echo.
echo INSTRUCCIONES:
echo 1. Usa opción 1 para agregar canciones individuales
echo 2. Usa opción 7 para agregar múltiples canciones desde una carpeta
echo 3. Coloca tus archivos MP3/WAV en una carpeta y usa la opción 7
echo 4. Después de agregar canciones, prueba la identificación en la web
echo.

python manage_song_database.py

echo.
echo Presiona cualquier tecla para continuar...
pause >nul