# 📖 GUÍA DE USO - MUSIC ANALYSIS

## 🎯 Cómo Usar la Aplicación

### 🚀 Inicio Rápido

1. **Ejecuta la aplicación**: `INICIAR_APLICACION_COMPLETA.bat`
2. **Abre tu navegador** en: http://localhost:8081
3. **¡Comienza a analizar música!**

## 🎵 Análisis de Audio Local

### Subir Archivos de Audio

#### Método 1: Arrastrar y Soltar
1. **Arrastra** un archivo MP3/WAV desde tu explorador
2. **Suéltalo** en la zona de "Subir Archivo"
3. **Espera** el análisis automático (30-60 segundos)

#### Método 2: Seleccionar Archivo
1. **Haz clic** en "Seleccionar Archivo"
2. **Navega** y elige tu archivo de audio
3. **Confirma** la selección

### Formatos Soportados
- ✅ **MP3** - Más común, buena compatibilidad
- ✅ **WAV** - Mejor calidad para análisis
- ✅ **M4A** - Formato Apple
- ✅ **FLAC** - Sin pérdida, máxima calidad
- ✅ **WebM** - Formato web
- ✅ **OGG** - Formato libre

### Resultados del Análisis

#### 📊 Información Básica
- **Tonalidad**: Clave musical detectada (ej: C Major, A Minor)
- **BPM**: Tempo en beats por minuto
- **Duración**: Tiempo total del archivo

#### 🎸 Progresión de Acordes
- **Acordes principales** identificados en la canción
- **Visualización** con chips de colores
- **Secuencia temporal** de cambios armónicos

#### ⏰ Línea de Tiempo
- **Timeline detallado** con cambios de acordes
- **Timestamps precisos** de cada cambio
- **Nivel de confianza** para cada detección
- **Vista expandida** para análisis completo

#### 🎼 Notas Principales
- **Notas más relevantes** en la composición
- **Frecuencias dominantes** identificadas

## 🎬 Descarga desde YouTube

### Vista Previa de Videos

1. **Pega la URL** de YouTube en el campo correspondiente
2. **Haz clic** en "Vista Previa"
3. **Revisa la información**:
   - Título del video
   - Canal/Artista
   - Duración
   - Número de visualizaciones
   - Fecha de publicación

### Tipos de Descarga

#### 🎵 Solo Audio
**Formatos disponibles:**
- **MP3** (Comprimido - 192kbps) - Recomendado para música
- **WAV** (Sin compresión) - Mejor para análisis profesional
- **M4A** (Apple - Buena calidad) - Balance calidad/tamaño
- **FLAC** (Sin pérdida - Máxima calidad) - Para audiófilos

#### 🎬 Video Completo
**Calidades disponibles:**
- **360p** (Básica - Menor tamaño) - Para conexiones lentas
- **480p** (Estándar) - Calidad decente, tamaño moderado
- **720p** (HD - Recomendado) - Balance perfecto
- **1080p** (Full HD - Mayor tamaño) - Máxima calidad
- **Mejor Disponible** - Automático según el video

### Proceso de Descarga

1. **Selecciona el tipo**: Audio o Video
2. **Elige formato/calidad** según tus necesidades
3. **Haz clic** en "Descargar Audio/Video"
4. **Espera** la descarga (puede tomar varios minutos)
5. **Revisa** el archivo en la sección de descargas

## 🎤 Identificación en Vivo (Shazam-like)

### Grabar desde Micrófono

1. **Reproduce la canción** que quieres identificar
2. **Mantén presionado** el botón de grabación
3. **Graba mínimo 10 segundos** para mejor precisión
4. **Suelta** para procesar automáticamente

### Qué Obtienes
- **Identificación automática** de la canción
- **Análisis musical completo** (tonalidad, acordes, BPM)
- **Búsqueda de letras** en múltiples fuentes
- **Enlaces** a plataformas musicales

## 🔍 Identificación Inteligente

### Desde Nombres de Archivo
La aplicación **automáticamente extrae** información de archivos con nombres como:
- "Artista - Título.mp3"
- "The Beatles - Hey Jude.wav"
- "Queen – Bohemian Rhapsody.flac"

### Nivel de Confianza
- **95%** - Información extraída del nombre del archivo
- **Variable** - Identificación por análisis de audio
- **0%** - No se pudo identificar

## 📝 Búsqueda de Letras

### Búsqueda Automática
Cuando se identifica una canción, aparece el botón:
**"Buscar Letras en Web"**

### Opciones de Búsqueda
- **Genius** - Letras con anotaciones y significados
- **AZLyrics** - Base de datos extensa (búsqueda manual)
- **Google Search** - Búsqueda general automática
- **Letras.com** - Opción en español

### Consejos para Mejores Resultados
- **Genius**: Búsqueda automática, mejores explicaciones
- **AZLyrics**: Busca manualmente el artista en el sitio
- **Google**: Encuentra múltiples fuentes automáticamente

## 📁 Gestión de Descargas

### Ver Archivos Descargados
La sección **"Archivos Descargados"** muestra:
- **Nombre** del archivo
- **Tamaño** en MB
- **Fecha** de descarga
- **Acciones** disponibles

### Acciones Disponibles
- **▶️ Abrir** - Reproduce/descarga el archivo
- **🗑️ Eliminar** - Borra el archivo (con confirmación)
- **🔄 Actualizar** - Refresca la lista
- **📁 Abrir Carpeta** - Muestra ubicación de descargas

## 📊 Exportación de Resultados

### Formatos Disponibles
- **JSON** - Para desarrolladores y análisis programático
- **TXT** - Texto plano, fácil de leer
- **PDF** - Documento profesional para imprimir

### Qué se Exporta
- Información básica (tonalidad, BPM, duración)
- Progresión completa de acordes
- Timeline detallado con timestamps
- Notas principales identificadas
- Información de identificación (si disponible)

## 🎯 Consejos para Mejores Resultados

### Para Análisis de Audio
- **Usa archivos de buena calidad** (320kbps MP3 o WAV)
- **Evita archivos muy largos** (máximo 10 minutos recomendado)
- **Música instrumental** da mejores resultados para acordes
- **Canciones con instrumentos claros** se analizan mejor

### Para Descarga de YouTube
- **Verifica que la URL sea correcta** antes de descargar
- **Algunos videos pueden estar restringidos** por región
- **Videos musicales** dan mejores resultados que conciertos en vivo
- **Calidad 720p** es el mejor balance calidad/tamaño

### Para Identificación en Vivo
- **Graba en ambiente silencioso** para mejor precisión
- **Acerca el micrófono** a la fuente de audio
- **Graba al menos 10-15 segundos** del coro o parte distintiva
- **Evita ruido de fondo** durante la grabación

## 🔧 Funciones Avanzadas

### Análisis Detallado
- **Timeline expandido** - Ver todos los cambios de acordes
- **Nivel de confianza** - Qué tan seguro está el análisis
- **Múltiples algoritmos** - Combina diferentes técnicas de análisis

### Personalización
- **Formatos preferidos** - Elige tus formatos por defecto
- **Calidades preferidas** - Configura calidades automáticas
- **Ubicación de descargas** - Archivos se guardan en `./downloads/`

## ❓ Preguntas Frecuentes

### ¿Por qué el análisis toma tanto tiempo?
- El análisis con IA es computacionalmente intensivo
- Archivos más largos requieren más tiempo
- La primera vez puede tomar más tiempo (carga de modelos)

### ¿Puedo analizar música en otros idiomas?
- Sí, el análisis musical funciona con cualquier idioma
- La identificación de letras depende de la disponibilidad online

### ¿Qué hago si no encuentra las letras?
- Usa el botón "Buscar Letras en Web"
- Prueba diferentes fuentes (Genius, Google, etc.)
- Algunas canciones pueden no tener letras disponibles

### ¿Los archivos se guardan en mi computadora?
- Sí, todo se procesa localmente
- Los archivos descargados se guardan en `./downloads/`
- No se envía información a servidores externos

---

**🎵 ¡Disfruta explorando y analizando tu música!**

*Para más ayuda técnica, consulta `GUIA_INSTALACION.md` o `SOLUCION_PROBLEMAS.md`*