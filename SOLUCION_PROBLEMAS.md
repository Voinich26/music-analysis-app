# 🔧 SOLUCIÓN DE PROBLEMAS - MUSIC ANALYSIS

## 🚨 Problemas Comunes y Soluciones

### 1. ❌ "Backend no está ejecutándose"

**Síntomas:**
- Error de conexión en el navegador
- Mensaje "No se puede conectar con el servidor"
- API no responde

**Soluciones:**
```bash
# Diagnóstico automático
DIAGNOSTICO_APLICACION.bat

# Reiniciar aplicación completa
DETENER_APLICACION.bat
INICIAR_APLICACION_COMPLETA.bat

# Verificar puertos manualmente
netstat -an | findstr ":3001\|:5005\|:8081"
```

### 2. ❌ "Python no encontrado"

**Síntomas:**
- "python is not recognized as internal command"
- Error al ejecutar scripts de Python

**Soluciones:**
1. **Instalar Python** desde https://python.org/downloads/
2. **IMPORTANTE**: Marcar "Add Python to PATH" durante instalación
3. **Reiniciar** Command Prompt/PowerShell
4. **Verificar**:
   ```bash
   python --version
   pip --version
   ```

### 3. ❌ "Go no encontrado"

**Síntomas:**
- "go is not recognized as internal command"
- Error al compilar backend

**Soluciones:**
1. **Instalar Go** desde https://golang.org/dl/
2. **Reiniciar** terminal después de instalación
3. **Verificar**:
   ```bash
   go version
   ```

### 4. ❌ "Puerto ocupado" / "Address already in use"

**Síntomas:**
- Error al iniciar servidores
- "bind: address already in use"

**Soluciones:**
```bash
# Solución automática
liberar_puertos.bat

# Solución manual - encontrar proceso
netstat -ano | findstr ":3001"
netstat -ano | findstr ":5005"
netstat -ano | findstr ":8081"

# Terminar proceso específico
taskkill /PID [NUMERO_PID] /F
```

### 5. ❌ "Dependencias faltantes"

**Síntomas:**
- Error al importar módulos Python
- "ModuleNotFoundError"

**Soluciones:**
```bash
# Activar entorno virtual
.venv\Scripts\activate.bat

# Reinstalar dependencias básicas
pip install flask flask-cors yt-dlp librosa numpy scipy soundfile

# Dependencias avanzadas (opcional)
pip install madmom openai-whisper music21 aubio

# Verificar instalación
python -c "import flask, librosa; print('✅ Dependencias OK')"
```

### 6. ❌ "No se puede analizar el audio"

**Síntomas:**
- Archivo se sube pero no se procesa
- Error en análisis musical

**Soluciones:**
1. **Verificar formato**: Solo MP3, WAV, M4A, FLAC, WebM, OGG
2. **Verificar tamaño**: Máximo 50MB recomendado
3. **Verificar duración**: Máximo 10 minutos recomendado
4. **Probar archivo diferente**: Usar archivo conocido que funcione

### 7. ❌ "Error al descargar de YouTube"

**Síntomas:**
- "Video unavailable"
- "Sign in to confirm your age"
- Error de descarga

**Soluciones:**
1. **Verificar URL**: Debe ser válida de YouTube
2. **Probar video diferente**: Algunos están restringidos
3. **Reiniciar servidor YouTube**:
   ```bash
   # Cerrar ventana de YouTube server (Ctrl+C)
   iniciar_servidor_youtube.bat
   ```
4. **Actualizar yt-dlp**:
   ```bash
   pip install --upgrade yt-dlp
   ```

### 8. ❌ "FFmpeg no encontrado"

**Síntomas:**
- Error al convertir formatos de audio
- "FFmpeg not found"

**Soluciones:**
```bash
# Instalador automático
instalar_ffmpeg.bat

# Verificar instalación
ffmpeg -version

# Si no funciona, descargar manualmente:
# https://ffmpeg.org/download.html
```

### 9. ❌ Problemas de Rendimiento

**Síntomas:**
- Aplicación muy lenta
- Análisis toma demasiado tiempo
- Navegador se congela

**Soluciones:**
1. **Cerrar aplicaciones** que consuman CPU/RAM
2. **Usar archivos más pequeños** (< 10MB, < 5 minutos)
3. **Reiniciar aplicación**:
   ```bash
   DETENER_APLICACION.bat
   INICIAR_APLICACION_COMPLETA.bat
   ```
4. **Verificar recursos del sistema** (Task Manager)

### 10. ❌ "CORS Policy Error"

**Síntomas:**
- Error CORS en consola del navegador
- "Access to fetch blocked by CORS policy"

**Soluciones:**
1. **Usar localhost** (no 127.0.0.1)
2. **Verificar puertos** coincidan en frontend/backend
3. **Reiniciar navegador** y limpiar caché
4. **Verificar backend** tenga CORS habilitado

## 🔍 Comandos de Diagnóstico

### Verificar Estado Completo
```bash
# Diagnóstico automático completo
DIAGNOSTICO_APLICACION.bat

# Verificar procesos manualmente
tasklist | findstr "python.exe\|go.exe"

# Verificar puertos manualmente
netstat -an | findstr ":3001\|:5005\|:8081"
```

### Verificar Dependencias
```bash
# Verificar versiones
python --version
go version
pip --version

# Verificar módulos Python
python -c "import flask, librosa, yt_dlp; print('✅ Módulos básicos OK')"

# Verificar módulos avanzados
python -c "import madmom, whisper; print('✅ IA disponible')"
```

### Limpiar y Reiniciar
```bash
# Limpiar todo y reiniciar
DETENER_APLICACION.bat
liberar_puertos.bat
INICIAR_APLICACION_COMPLETA.bat

# Limpiar archivos temporales
del /q downloads\*
del /q python_audio\downloads\*
```

## 🧪 Pruebas de Funcionamiento

### Prueba Básica
1. **Abrir** http://localhost:8081
2. **Subir** archivo MP3 pequeño (< 5MB)
3. **Verificar** que aparezcan resultados
4. **Probar** exportación JSON

### Prueba YouTube
1. **Pegar URL** de YouTube conocida
2. **Hacer clic** en "Vista Previa"
3. **Verificar** información del video
4. **Probar descarga** en MP3

### Prueba Grabación
1. **Reproducir música** en otro dispositivo
2. **Mantener presionado** botón de grabación
3. **Grabar 10-15 segundos**
4. **Verificar** identificación automática

## 📋 Información para Reportar Problemas

### Datos Necesarios
- **Sistema Operativo**: Windows 10/11, versión
- **Versiones instaladas**:
  ```bash
  python --version
  go version
  pip --version
  ```
- **Mensaje de error completo**
- **Pasos para reproducir**
- **Archivos de prueba** (si es posible)

### Logs Útiles
- **Consola del navegador** (F12 → Console)
- **Ventanas de terminal** donde se ejecutan los servidores
- **Resultado de** `DIAGNOSTICO_APLICACION.bat`

## 🆘 Soluciones de Emergencia

### Si Nada Funciona
```bash
# 1. Detener todo
DETENER_APLICACION.bat

# 2. Limpiar completamente
rmdir /s .venv
del /q downloads\*

# 3. Reinstalar desde cero
INICIAR_APLICACION_COMPLETA.bat
```

### Reinstalación Completa
1. **Hacer backup** de archivos importantes en `downloads/`
2. **Eliminar** carpeta completa del proyecto
3. **Descargar** versión nueva del proyecto
4. **Ejecutar** `INICIAR_APLICACION_COMPLETA.bat`

## 📞 Obtener Más Ayuda

### Recursos Disponibles
- **README.md** - Información general del proyecto
- **GUIA_INSTALACION.md** - Instalación paso a paso
- **GUIA_USO.md** - Cómo usar todas las funciones

### Soporte Técnico
- **GitHub Issues** - Para reportar bugs
- **Documentación** - Archivos `.md` en el proyecto
- **Diagnóstico** - Siempre ejecutar `DIAGNOSTICO_APLICACION.bat` primero

---

**🔧 La mayoría de problemas se solucionan reiniciando la aplicación completa**

*Si el problema persiste, ejecuta `DIAGNOSTICO_APLICACION.bat` y comparte el resultado*