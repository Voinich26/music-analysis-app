@echo off
echo ========================================
echo    LIMPIEZA DEL PROYECTO MUSICAL
echo ========================================
echo.

echo Eliminando archivos innecesarios...

REM Eliminar archivos de prueba y temporales
if exist "test.py" del "test.py"
if exist "abrir_aplicacion.sh" del "abrir_aplicacion.sh"
if exist "verificar_proyecto.sh" del "verificar_proyecto.sh"
if exist "ejecutar_aplicacion.bat" del "ejecutar_aplicacion.bat"
if exist "ejecutar_aplicacion_corregido.bat" del "ejecutar_aplicacion_corregido.bat"

REM Eliminar archivos compilados de Go
if exist "backend\music-analysis" del "backend\music-analysis"
if exist "backend\*.exe" del "backend\*.exe"

REM Limpiar directorio temporal de audio
if exist "backend\temp_audio\*" del /q "backend\temp_audio\*"

echo.
echo ✅ Limpieza completada
echo.
echo Archivos principales del proyecto:
echo   - ejecutar_aplicacion_completa.bat (script principal)
echo   - servidor_frontend.py (servidor frontend)
echo   - test_conexion.py (pruebas de conectividad)
echo   - backend/main.go (servidor backend)
echo   - frontend/index.html (interfaz web)
echo.
pause

