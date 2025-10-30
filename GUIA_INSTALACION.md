# 🚀 GUÍA DE INSTALACIÓN - MUSIC ANALYSIS

## � RRepositorio GitHub
**URL:** https://github.com/Voinich26/music-analysis-app.git

## 🔽 Descarga del Proyecto

### Opción 1: Clonar con Git
```bash
git clone https://github.com/Voinich26/music-analysis-app.git
cd music-analysis-app
```

### Opción 2: Descargar ZIP
1. Ve a https://github.com/Voinich26/music-analysis-app
2. Haz clic en "Code" → "Download ZIP"
3. Extrae el archivo en tu carpeta deseada

## 📋 Requisitos del Sistema

### Software Necesario
- **Windows 10/11** (64-bit recomendado)
- **Python 3.8+** - [Descargar aquí](https://python.org/downloads/)
- **Go 1.19+** - [Descargar aquí](https://golang.org/dl/)
- **Git** (opcional) - [Descargar aquí](https://git-scm.com/)

### ✅ Verificar Instalaciones
Abre **Command Prompt** o **PowerShell** y ejecuta:
```bash
python --version    # Debe mostrar Python 3.8+
go version         # Debe mostrar Go 1.19+
```

## 🛠️ Instalación Automática (Recomendada)

### Opción 1: Instalación Completa
1. **Descarga o clona** el proyecto
2. **Haz doble clic** en: `INICIAR_APLICACION_COMPLETA.bat`
3. **Espera** a que se instalen las dependencias automáticamente
4. **¡Listo!** La aplicación se abrirá en tu navegador

### Opción 2: Instalación Manual

#### Paso 1: Preparar el Entorno
```bash
# Crear entorno virtual de Python
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\activate.bat
```

#### Paso 2: Instalar Dependencias Python
```bash
# Dependencias básicas
pip install flask flask-cors yt-dlp librosa numpy scipy soundfile

# Dependencias avanzadas (opcional)
pip install madmom openai-whisper music21 aubio
```

#### Paso 3: Instalar Dependencias Go
```bash
cd backend
go mod tidy
cd ..
```

#### Paso 4: Configurar FFmpeg (Recomendado)
```bash
# Opción A: Instalador automático
instalar_ffmpeg.bat

# Opción B: Manual desde https://ffmpeg.org/
```

#### Paso 5: Ejecutar Aplicación
```bash
INICIAR_APLICACION_COMPLETA.bat
```

## 🔍 Verificación de la Instalación

### ✅ Checklist de Verificación
1. **Frontend**: http://localhost:8081 - Debe cargar la interfaz
2. **Backend**: http://localhost:3001/api/health - Debe responder "ok"
3. **YouTube**: http://localhost:5005/api/health - Debe responder "ok"
4. **Subir archivo** - Debe analizar correctamente
5. **Vista previa YouTube** - Debe mostrar información del video

### 🧪 Prueba Rápida
1. Abre http://localhost:8081
2. Sube un archivo MP3 pequeño
3. Verifica que aparezcan los resultados del análisis
4. Prueba la vista previa de YouTube con cualquier URL

## 🐛 Solución de Problemas Comunes

### ❌ "Python no encontrado"
**Solución:**
1. Instala Python desde https://python.org/downloads/
2. **IMPORTANTE**: Marca "Add Python to PATH" durante la instalación
3. Reinicia Command Prompt
4. Verifica: `python --version`

### ❌ "Go no encontrado"
**Solución:**
1. Instala Go desde https://golang.org/dl/
2. Reinicia Command Prompt
3. Verifica: `go version`

### ❌ "Puerto ocupado" / "Address already in use"
**Solución:**
```bash
# Liberar puertos automáticamente
DETENER_APLICACION.bat

# O liberar manualmente
liberar_puertos.bat

# Luego reiniciar
INICIAR_APLICACION_COMPLETA.bat
```

### ❌ "Backend no está ejecutándose"
**Solución:**
```bash
# Diagnóstico completo
DIAGNOSTICO_APLICACION.bat

# Si hay errores, reiniciar todo
DETENER_APLICACION.bat
INICIAR_APLICACION_COMPLETA.bat
```

### ❌ "Error al descargar de YouTube"
**Solución:**
1. Verifica que la URL sea válida
2. Algunos videos pueden estar restringidos por región
3. Reinicia el servidor de YouTube:
```bash
# Cerrar ventana de YouTube server (Ctrl+C)
iniciar_servidor_youtube.bat
```

### ❌ "Dependencias faltantes"
**Solución:**
```bash
# Activar entorno virtual
.venv\Scripts\activate.bat

# Reinstalar dependencias
pip install --upgrade flask flask-cors yt-dlp librosa numpy scipy soundfile

# Para análisis avanzado
pip install madmom openai-whisper music21 aubio
```

## ⚙️ Configuración Avanzada

### 🔧 Cambiar Puertos
Si necesitas usar puertos diferentes:

**Backend Principal (3001):**
```go
// En backend/main.go, línea ~35
port := "3001"  // Cambiar aquí
```

**Frontend (8081):**
```python
# En servidor_frontend.py, línea ~10
PORT = 8081  # Cambiar aquí
```

**YouTube Server (5005):**
```python
# En backend_youtube.py, línea final
app.run(host='0.0.0.0', port=5005, debug=True)  # Cambiar puerto aquí
```

### 🔒 Habilitar HTTPS (Opcional)
Para uso en producción:
1. Genera certificados SSL
2. Configura en `servidor_frontend.py`
3. Actualiza URLs en `frontend/js/app.js`

### 📊 Configurar Análisis Avanzado
Para habilitar funciones de IA:
```bash
# Instalar dependencias avanzadas
pip install madmom openai-whisper music21 aubio

# Verificar instalación
python -c "import madmom, whisper; print('✅ IA disponible')"
```

## 🔄 Actualización del Sistema

### Actualizar Dependencias
```bash
# Python
pip install --upgrade flask flask-cors yt-dlp librosa

# Go
cd backend
go mod tidy
go get -u
cd ..
```

### Actualizar Código (si usas Git)
```bash
git pull origin main
DETENER_APLICACION.bat
INICIAR_APLICACION_COMPLETA.bat
```

## 🗑️ Desinstalación

### Desinstalación Completa
1. Ejecuta: `DETENER_APLICACION.bat`
2. Elimina la carpeta completa del proyecto
3. Opcional: Desinstala Python/Go si no los usas para otros proyectos

### Desinstalación Parcial (Solo dependencias)
```bash
# Eliminar entorno virtual
rmdir /s .venv

# Limpiar caché de Go
go clean -modcache
```

## 📞 Obtener Ayuda

### 🔍 Diagnóstico Automático
```bash
DIAGNOSTICO_APLICACION.bat
```

### 📋 Información del Sistema
- **Logs del Frontend**: Consola del navegador (F12)
- **Logs del Backend**: Ventanas de terminal
- **Archivos de configuración**: `backend/`, `frontend/`, raíz del proyecto

### 🆘 Soporte
- **GitHub Issues**: Para reportar bugs
- **Documentación**: Archivos `.md` en el proyecto
- **Logs**: Siempre incluye los logs al reportar problemas

---

**🎵 ¡Disfruta analizando tu música!**

*Si sigues teniendo problemas, ejecuta `DIAGNOSTICO_APLICACION.bat` y comparte el resultado.*