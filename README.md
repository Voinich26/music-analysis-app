# 🎵 Music Analysis - Análisis Musical Profesional

Una aplicación web completa para análisis musical avanzado con capacidades de descarga de YouTube, identificación de canciones, análisis armónico y transcripción de letras.

![Music Analysis](https://img.shields.io/badge/Version-2.0-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Características Principales

### 🎼 Análisis Musical Completo
- **Detección de Tonalidad** - Identifica la clave musical automáticamente
- **Análisis de Acordes** - Reconoce progresiones armónicas con IA
- **Detección de BPM** - Calcula el tempo con precisión
- **Timeline Musical** - Visualiza cambios armónicos en tiempo real
- **Notas Principales** - Extrae las notas más relevantes

### 🎬 Descarga de YouTube Avanzada
- **Audio en múltiples formatos**: MP3, WAV, M4A, FLAC
- **Video en múltiples calidades**: 360p, 480p, 720p, 1080p, Best
- **Vista previa** de información antes de descargar
- **Gestión de descargas** con lista de archivos
- **Identificación automática** de canciones descargadas

### 🎤 Identificación de Canciones (Shazam-like)
- **Grabación desde micrófono** para identificar música en vivo
- **Extracción automática** de información desde nombres de archivo
- **Búsqueda de letras** en múltiples fuentes web
- **Enlaces a plataformas** musicales (Spotify, Apple Music, etc.)

### 📊 Exportación y Análisis
- **Múltiples formatos**: JSON, TXT, PDF
- **Análisis detallado** con confianza estadística
- **Interfaz moderna** y responsive
- **Transcripción de letras** con Whisper AI

## 🚀 Instalación Rápida

### Prerrequisitos
- **Windows 10/11**
- **Python 3.8+** - [Descargar](https://python.org/downloads/)
- **Go 1.19+** - [Descargar](https://golang.org/dl/)
- **Git** - [Descargar](https://git-scm.com/)

### Instalación Automática

1. **Clona el repositorio:**
```bash
git clone https://github.com/tu-usuario/music-analysis.git
cd music-analysis
```

2. **Ejecuta el instalador automático:**
```bash
INICIAR_APLICACION_COMPLETA.bat
```

¡Eso es todo! La aplicación se abrirá automáticamente en tu navegador.

## 📖 Uso de la Aplicación

### 🎵 Análisis de Audio Local

1. **Arrastra y suelta** un archivo MP3/WAV en la zona de subida
2. **O haz clic** en "Seleccionar Archivo" para elegir manualmente
3. **Espera el análisis** (30-60 segundos)
4. **Revisa los resultados** completos con visualizaciones

### 🎬 Descarga desde YouTube

1. **Pega la URL** de YouTube en el campo correspondiente
2. **Haz clic en "Vista Previa"** para ver información del video
3. **Selecciona el tipo**: Solo Audio o Video Completo
4. **Elige formato/calidad** según tus necesidades
5. **Descarga** y analiza automáticamente

### 🎤 Identificación en Vivo

1. **Reproduce la canción** que quieres identificar
2. **Mantén presionado** el botón de grabación (mínimo 10 segundos)
3. **Suelta para procesar** - Se identificará automáticamente
4. **Obtén letras y enlaces** a plataformas musicales

## 🛠️ Arquitectura del Sistema

### Backend
- **Go + Gin** - API REST principal para análisis musical
- **Python + Flask** - Servidor especializado para YouTube
- **yt-dlp** - Descarga avanzada de YouTube
- **librosa** - Procesamiento de señales de audio
- **Whisper AI** - Transcripción de voz a texto

### Frontend
- **HTML5 + CSS3** - Interfaz moderna y responsive
- **JavaScript ES6+** - Lógica de aplicación
- **Font Awesome** - Iconografía profesional
- **CSS Grid/Flexbox** - Layout adaptativo

### Puertos y Servicios
- **Frontend**: http://localhost:8081
- **Backend Principal**: http://localhost:3001
- **Servidor YouTube**: http://localhost:5005

## 📁 Estructura del Proyecto

```
music-analysis/
├── 📁 backend/                 # API principal en Go
│   ├── main.go                # Servidor principal
│   └── internal/              # Lógica de negocio
├── 📁 frontend/               # Interfaz web
│   ├── index.html            # Página principal
│   ├── js/app.js             # Lógica JavaScript
│   └── styles/main.css       # Estilos CSS
├── 📁 python_audio/          # Procesamiento de audio
│   ├── youtube_simple_downloader.py
│   ├── youtube_downloader_enhanced.py
│   └── advanced_chord_detection.py
├── 📁 downloads/             # Archivos descargados
├── backend_youtube.py        # Servidor Flask para YouTube
├── servidor_frontend.py      # Servidor web estático
└── 📄 Scripts de ejecución (.bat)
```

## 🎯 Scripts de Administración

### Ejecución
- `INICIAR_APLICACION_COMPLETA.bat` - Inicia toda la aplicación
- `DETENER_APLICACION.bat` - Detiene todos los servicios
- `iniciar_servidor_youtube.bat` - Solo servidor de YouTube

### Diagnóstico
- `DIAGNOSTICO_APLICACION.bat` - Verifica estado del sistema
- `liberar_puertos.bat` - Libera puertos ocupados

### Instalación
- `instalar_ffmpeg.bat` - Instala FFmpeg para conversión
- `instalar_youtube_downloader.bat` - Instala dependencias de YouTube

## 🔧 Configuración Avanzada

### Formatos de Audio Soportados
- **MP3** - Comprimido, 192kbps (recomendado para música)
- **WAV** - Sin compresión (mejor para análisis)
- **M4A** - Formato Apple, buena calidad
- **FLAC** - Sin pérdida, máxima calidad

### Calidades de Video
- **360p** - Básica, menor tamaño (móviles)
- **480p** - Estándar (conexiones lentas)
- **720p** - HD, recomendado (balance calidad/tamaño)
- **1080p** - Full HD, máxima calidad
- **Best** - Mejor disponible automáticamente

## 🐛 Solución de Problemas

### Problemas Comunes

**❌ "Backend no está ejecutándose"**
```bash
# Solución:
DETENER_APLICACION.bat
INICIAR_APLICACION_COMPLETA.bat
```

**❌ "Error al descargar de YouTube"**
- Verifica que la URL sea válida
- Algunos videos pueden estar restringidos
- Ejecuta: `iniciar_servidor_youtube.bat`

**❌ "No se puede analizar el audio"**
- Verifica que el archivo sea MP3/WAV
- Tamaño máximo recomendado: 50MB
- Duración máxima recomendada: 10 minutos

### Logs y Diagnóstico
- **Consola del navegador** (F12) - Errores de frontend
- **Ventanas de terminal** - Logs de backend
- **DIAGNOSTICO_APLICACION.bat** - Estado completo del sistema

## 🤝 Contribución

### Desarrollo Local
1. Fork del repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Realiza cambios y pruebas
4. Commit: `git commit -m "Agrega nueva funcionalidad"`
5. Push: `git push origin feature/nueva-funcionalidad`
6. Crea Pull Request

### Reportar Bugs
- Usa el sistema de Issues de GitHub
- Incluye logs y pasos para reproducir
- Especifica tu versión de Windows y navegador

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **yt-dlp** - Descarga de YouTube
- **librosa** - Análisis de audio
- **OpenAI Whisper** - Transcripción de voz
- **Gin Framework** - API REST en Go
- **Flask** - Servidor Python

## 📞 Soporte

- **Documentación**: Ver archivos `.md` en el proyecto
- **Issues**: GitHub Issues para bugs y sugerencias
- **Email**: [tu-email@ejemplo.com]

---

**🎵 Desarrollado con ❤️ para músicos y compositores**

*Versión 2.0 - Última actualización: Octubre 2024*