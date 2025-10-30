@echo off
title MUSIC ANALYSIS - DIAGNÓSTICO
color 0E

echo ========================================
echo   DIAGNÓSTICO MUSIC ANALYSIS
echo ========================================
echo.

echo [VERIFICANDO DEPENDENCIAS]
echo.
echo Go:
go version 2>nul && echo ✅ Go instalado || echo ❌ Go NO instalado

echo.
echo Python:
python --version 2>nul && echo ✅ Python instalado || echo ❌ Python NO instalado

echo.
echo [VERIFICANDO PUERTOS]
echo.
echo Puerto 3001 (Backend):
netstat -an | findstr :3001 >nul && echo ✅ Puerto 3001 en uso || echo ❌ Puerto 3001 libre

echo.
echo Puerto 5005 (YouTube):
netstat -an | findstr :5005 >nul && echo ✅ Puerto 5005 en uso || echo ❌ Puerto 5005 libre

echo.
echo Puerto 8081 (Frontend):
netstat -an | findstr :8081 >nul && echo ✅ Puerto 8081 en uso || echo ❌ Puerto 8081 libre

echo.
echo [VERIFICANDO SERVICIOS]
echo.
echo Backend Principal:
curl -s http://localhost:3001/api/health >nul 2>&1 && echo ✅ Backend funcionando || echo ❌ Backend NO responde

echo.
echo Servidor YouTube:
curl -s http://localhost:5005/api/health >nul 2>&1 && echo ✅ YouTube funcionando || echo ❌ YouTube NO responde

echo.
echo Frontend:
curl -s http://localhost:8081 >nul 2>&1 && echo ✅ Frontend funcionando || echo ❌ Frontend NO responde

echo.
echo [VERIFICANDO ARCHIVOS]
echo.
if exist "backend\main.go" (echo ✅ Backend encontrado) else (echo ❌ Backend NO encontrado)
if exist "frontend\index.html" (echo ✅ Frontend encontrado) else (echo ❌ Frontend NO encontrado)
if exist "backend_youtube.py" (echo ✅ YouTube server encontrado) else (echo ❌ YouTube server NO encontrado)

echo.
echo ========================================
echo   DIAGNÓSTICO COMPLETADO
echo ========================================
echo.
pause