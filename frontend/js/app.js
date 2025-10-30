/**
 * Music Analysis Web Application - VERSIÓN RESTAURADA
 * JavaScript para manejo de interfaz y comunicación con API
 * SOLO se agregó funcionalidad de YouTube sin tocar el resto
 */

class MusicAnalysisApp {
    constructor() {
        this.apiBaseUrl = 'http://localhost:3001/api';  // API original para análisis (puerto correcto)
        this.youtubeApiUrl = 'http://localhost:5005/api';  // API separada para YouTube
        this.currentAnalysisId = null;
        this.currentFile = null;
        this.currentFileInfo = null;  // Información extraída del nombre del archivo
        this.mediaRecorder = null;
        this.recordingChunks = [];
        this.recordingStartTime = null;
        this.recordingTimer = null;
        this.isRecording = false;

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupDragAndDrop();
        this.setupFileUpload();
        this.checkApiHealth();
    }

    setupEventListeners() {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    setupDragAndDrop() {
        const uploadBox = document.getElementById('fileUploadBox');

        uploadBox.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadBox.classList.add('dragover');
        });

        uploadBox.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadBox.classList.remove('dragover');
        });

        uploadBox.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadBox.classList.remove('dragover');

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileUpload(files[0]);
            }
        });
    }

    setupFileUpload() {
        const fileInput = document.getElementById('audioFile');
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileUpload(e.target.files[0]);
            }
        });
    }

    async checkApiHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`, {
                method: 'GET',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            if (!response.ok) {
                throw new Error('API no disponible');
            }
            console.log('✅ API de análisis conectada correctamente');
        } catch (error) {
            console.error('❌ Error conectando con API de análisis:', error);
            this.showNotification('Error: No se puede conectar con el servidor de análisis. Asegúrate de que el backend esté ejecutándose en el puerto 3001', 'error');
        }

        // Verificar API de YouTube por separado
        try {
            const response = await fetch(`${this.youtubeApiUrl}/health`);
            if (response.ok) {
                console.log('✅ API de YouTube conectada correctamente');
            }
        } catch (error) {
            console.log('⚠️ API de YouTube no disponible (puerto 5005)');
        }
    }

    async handleFileUpload(file) {
        const validTypes = ['audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/flac', 'audio/webm', 'audio/ogg'];
        if (!validTypes.includes(file.type) && !file.name.match(/\.(mp3|wav|m4a|flac|webm|ogg)$/i)) {
            this.showNotification('Formato de archivo no soportado. Use MP3, WAV, M4A, FLAC, WebM u OGG.', 'error');
            return;
        }

        this.currentFile = file;

        // Extraer información del nombre del archivo
        const fileInfo = this.extractSongInfoFromFilename(file.name);

        this.showAudioPreview(file);
        await this.analyzeAudio(file, fileInfo);
    }

    extractSongInfoFromFilename(filename) {
        // Remover extensión
        const nameWithoutExt = filename.replace(/\.(mp3|wav|m4a|flac|webm|ogg)$/i, '');

        // Patrones comunes para extraer artista y título
        const patterns = [
            /^(.+?)\s*-\s*(.+)$/, // "Artista - Título"
            /^(.+?)\s*–\s*(.+)$/, // "Artista – Título" (guión largo)
            /^(.+?)\s*_\s*(.+)$/, // "Artista _ Título"
            /^(.+?)\s*\|\s*(.+)$/, // "Artista | Título"
        ];

        for (const pattern of patterns) {
            const match = nameWithoutExt.match(pattern);
            if (match) {
                return {
                    artist: match[1].trim(),
                    title: match[2].trim(),
                    identified: true,
                    confidence: 0.95, // Alta confianza porque viene del nombre del archivo
                    source: 'filename'
                };
            }
        }

        // Si no hay patrón reconocible, usar todo como título
        return {
            artist: 'Desconocido',
            title: nameWithoutExt.trim(),
            identified: nameWithoutExt.trim().length > 0,
            confidence: 0.7,
            source: 'filename'
        };
    }

    showAudioPreview(file) {
        const audioPreview = document.getElementById('audioPreview');
        const audioPlayer = document.getElementById('audioPlayer');
        const audioInfo = document.getElementById('audioInfo');

        const fileUrl = URL.createObjectURL(file);
        audioPlayer.src = fileUrl;

        audioPlayer.addEventListener('loadedmetadata', () => {
            const duration = audioPlayer.duration;
            const minutes = Math.floor(duration / 60);
            const seconds = Math.floor(duration % 60);
            const durationText = `${minutes}:${seconds.toString().padStart(2, '0')}`;

            audioInfo.innerHTML = `
                <div class="file-info">
                    <p><strong>Archivo:</strong> ${file.name}</p>
                    <p><strong>Tamaño:</strong> ${(file.size / 1024 / 1024).toFixed(2)} MB</p>
                    <p><strong>Tipo:</strong> ${file.type || 'Desconocido'}</p>
                    <p><strong>Duración:</strong> ${durationText}</p>
                </div>
            `;
        });

        audioPreview.style.display = 'block';
    }

    async analyzeAudio(file, fileInfo = null) {
        try {
            this.showLoadingState('Analizando audio...');

            const formData = new FormData();
            formData.append('audio', file);

            const response = await fetch(`${this.apiBaseUrl}/audio/upload`, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Error al procesar el audio');
            }

            this.currentAnalysisId = result.analysis_id;
            this.currentFileInfo = fileInfo; // Guardar info del archivo
            await this.pollAnalysisResults();

        } catch (error) {
            console.error('Error en análisis:', error);
            this.showErrorState(`Error al analizar audio: ${error.message}`);
        }
    }

    async pollAnalysisResults() {
        const maxAttempts = 60;
        let attempts = 0;

        const poll = async () => {
            try {
                attempts++;

                const response = await fetch(`${this.apiBaseUrl}/audio/${this.currentAnalysisId}`);
                const result = await response.json();

                if (!response.ok) {
                    throw new Error(result.error || 'Error al obtener resultados');
                }

                if (result.status === 'completed') {
                    this.displayResults(result);
                    this.hideLoadingState();
                } else if (result.status === 'error') {
                    throw new Error(result.error || 'Error en el análisis');
                } else if (attempts < maxAttempts) {
                    setTimeout(poll, 5000);
                } else {
                    throw new Error('Tiempo de espera agotado');
                }

            } catch (error) {
                console.error('Error en polling:', error);
                this.showErrorState(`Error: ${error.message}`);
            }
        };

        poll();
    }

    displayResults(results) {
        document.getElementById('resultKey').textContent = results.key || 'No detectado';
        document.getElementById('resultBPM').textContent = results.bpm || 'No detectado';
        document.getElementById('resultDuration').textContent = this.formatDuration(results.duration || 0);

        this.displayChordProgression(results.progression || []);
        this.displayTimeline(results.timeline || []);
        this.displayNotes(results.notes || []);

        if (results.lyrics && results.lyrics.trim()) {
            this.displayLyrics(results.lyrics);
        }

        // Usar información del archivo si no hay identificación del backend
        let songIdentification = results.song_identification;

        if ((!songIdentification || !songIdentification.identified) && this.currentFileInfo && this.currentFileInfo.identified) {
            songIdentification = {
                identified: true,
                title: this.currentFileInfo.title,
                artist: this.currentFileInfo.artist,
                album: '',
                confidence: this.currentFileInfo.confidence,
                source: 'filename'
            };
        }

        if (songIdentification) {
            this.displaySongIdentification(songIdentification);
        }

        // Siempre mostrar el botón de búsqueda de letras
        this.showLyricsSearchButton();

        document.getElementById('resultsContainer').style.display = 'block';
        document.getElementById('resultsContent').style.display = 'block';

        document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
    }

    displayChordProgression(progression) {
        const container = document.getElementById('chordProgression');
        container.innerHTML = '';

        progression.forEach(chord => {
            const chordElement = document.createElement('span');
            chordElement.className = 'chord-item';
            chordElement.textContent = chord;
            container.appendChild(chordElement);
        });
    }

    displayTimeline(timeline) {
        const container = document.getElementById('timeline');
        container.innerHTML = '';

        fullTimelineData = timeline;

        const displayItems = timeline.slice(0, 10);

        displayItems.forEach(item => {
            const timelineItem = document.createElement('div');
            timelineItem.className = 'timeline-item';
            timelineItem.innerHTML = `
                <span class="timeline-time">${item.time}</span>
                <span class="timeline-chord">${item.chord}</span>
                <span class="timeline-confidence">${item.confidence ? (item.confidence * 100).toFixed(0) + '%' : ''}</span>
            `;
            container.appendChild(timelineItem);
        });

        if (timeline.length > 10) {
            const moreItem = document.createElement('div');
            moreItem.className = 'timeline-more';
            moreItem.innerHTML = `<p><i class="fas fa-ellipsis-h"></i> Y ${timeline.length - 10} acordes más... <button onclick="toggleFullTimeline()" class="btn-link">Ver todos</button></p>`;
            container.appendChild(moreItem);
        }
    }

    displayNotes(notes) {
        const container = document.getElementById('notesList');
        container.innerHTML = '';

        notes.forEach(note => {
            const noteElement = document.createElement('span');
            noteElement.className = 'note-item';
            noteElement.textContent = note;
            container.appendChild(noteElement);
        });
    }

    displayLyrics(lyrics) {
        const lyricsCard = document.getElementById('lyricsCard');
        const lyricsContent = document.getElementById('lyricsContent');

        // Limpiar y formatear las letras
        const formattedLyrics = this.formatLyrics(lyrics);
        lyricsContent.innerHTML = `<pre>${formattedLyrics}</pre>`;
        lyricsCard.style.display = 'block';
    }

    formatLyrics(lyrics) {
        if (!lyrics) return '';

        // Limpiar solo marcadores de transcripción, mantener idioma original
        let formatted = lyrics
            .replace(/^\[Transcripción\]:\s*/gi, '')
            .replace(/^\[transcripción\]:\s*/gi, '')
            .replace(/^\[TRANSCRIPCIÓN\]:\s*/gi, '')
            .trim();

        // Dividir el texto en frases más naturales
        // Usar múltiples patrones para detectar finales de línea
        const sentences = formatted.split(/(?<=[.!?])\s+|(?<=\w)\s+(?=[A-Z][a-z])/);

        // Filtrar frases muy cortas y agrupar en versos
        const meaningfulSentences = sentences.filter(sentence =>
            sentence.trim().length > 15 &&
            !sentence.match(/^[A-Z]\s*$/) // Evitar letras sueltas
        );

        // Agrupar en versos de 2-3 líneas para mejor legibilidad
        const verses = [];
        for (let i = 0; i < meaningfulSentences.length; i += 2) {
            const verse = meaningfulSentences.slice(i, i + 2)
                .map(line => line.trim())
                .join('\n');

            if (verse.trim().length > 0) {
                verses.push(verse);
            }
        }

        return verses.length > 0 ? verses.join('\n\n') : formatted;
    }

    showLyricsSearchButton() {
        const lyricsCard = document.getElementById('lyricsCard');
        const lyricsActions = document.getElementById('lyricsActions');
        const lyricsContent = document.getElementById('lyricsContent');
        
        // Mostrar la tarjeta de letras y el botón de búsqueda
        if (lyricsCard && lyricsActions) {
            lyricsCard.style.display = 'block';
            lyricsActions.style.display = 'block';
            
            // Si no hay contenido de letras, mostrar mensaje informativo
            if (lyricsContent && (!lyricsContent.innerHTML || lyricsContent.innerHTML.trim() === '')) {
                lyricsContent.innerHTML = `
                    <div style="text-align: center; padding: 20px; color: var(--gray-600);">
                        <i class="fas fa-search" style="font-size: 24px; margin-bottom: 10px;"></i>
                        <p>Haz clic en el botón de arriba para buscar las letras de esta canción en diferentes plataformas web.</p>
                    </div>
                `;
            }
        }
    }

    openLyricsSearch(artist, title) {
        // Si no hay información específica, usar información del archivo actual
        if (!artist || artist === 'Unknown') {
            artist = this.currentFileInfo?.artist || 'Unknown Artist';
        }
        if (!title || title === 'Unknown') {
            title = this.currentFileInfo?.title || 'Unknown Song';
        }

        // Crear URLs para diferentes sitios de letras
        const searchQuery = encodeURIComponent(`${artist} ${title}`);
        const sites = [
            {
                name: 'Genius',
                url: `https://genius.com/search?q=${searchQuery}`,
                icon: 'fas fa-brain',
                description: 'Letras con anotaciones y significados'
            },
            {
                name: 'AZLyrics',
                url: `https://www.azlyrics.com/`,
                icon: 'fas fa-music',
                description: 'Busca manualmente en la base de datos'
            },
            {
                name: 'Google Search',
                url: `https://www.google.com/search?q=${searchQuery}+lyrics`,
                icon: 'fab fa-google',
                description: 'Búsqueda general de letras'
            },
            {
                name: 'Letras.com',
                url: `https://www.letras.com/`,
                icon: 'fas fa-quote-left',
                description: 'Sitio en español para letras'
            }
        ];

        // Mostrar opciones de búsqueda
        const lyricsCard = document.getElementById('lyricsCard');
        const lyricsContent = document.getElementById('lyricsContent');

        lyricsCard.style.display = 'block';
        lyricsContent.innerHTML = `
            <div style="text-align: center; padding: 25px;">
                <h5 style="margin-bottom: 20px; color: var(--gray-800); font-size: 18px;">
                    🎵 Buscar letras para "${title}"
                </h5>
                <p style="margin-bottom: 25px; color: var(--gray-600);">
                    Selecciona una opción para buscar las letras de <strong>"${artist} - ${title}"</strong>:
                </p>
                <div style="display: grid; grid-template-columns: 1fr; gap: 15px; max-width: 400px; margin: 0 auto;">
                    ${sites.map(site => `
                        <a href="${site.url}" target="_blank" 
                           style="display: flex; align-items: center; gap: 15px; padding: 18px; 
                                  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark)); 
                                  color: white; text-decoration: none; border-radius: 12px; 
                                  transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);"
                           onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 8px 25px rgba(99, 102, 241, 0.4)'"
                           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(99, 102, 241, 0.3)'">
                            <i class="${site.icon}" style="font-size: 20px; min-width: 20px;"></i>
                            <div style="text-align: left; flex: 1;">
                                <div style="font-weight: 600; font-size: 16px;">${site.name}</div>
                                <div style="font-size: 12px; opacity: 0.9;">${site.description}</div>
                            </div>
                            <i class="fas fa-external-link-alt" style="font-size: 14px;"></i>
                        </a>
                    `).join('')}
                </div>
                <p style="margin-top: 25px; font-size: 13px; color: var(--gray-500); line-height: 1.5;">
                    💡 <strong>Consejos:</strong><br>
                    • <strong>Genius:</strong> Búsqueda automática con explicaciones<br>
                    • <strong>AZLyrics:</strong> Busca manualmente "${artist}" en el sitio<br>
                    • <strong>Google:</strong> Encuentra múltiples fuentes<br>
                    🎯 Todos se abren en nueva pestaña
                </p>
            </div>
        `;

        this.showNotification(`🔍 Opciones de búsqueda abiertas para "${title}"`, 'info');
    }



    displaySongIdentification(identification) {
        const songCard = document.getElementById('songIdentificationCard');
        const songTitle = document.getElementById('songTitle');
        const songArtist = document.getElementById('songArtist');
        const songAlbum = document.getElementById('songAlbum');
        const confidenceFill = document.getElementById('confidenceFill');
        const confidenceText = document.getElementById('confidenceText');
        const musicLinks = document.getElementById('musicLinks');
        const lyricsCard = document.getElementById('lyricsCard');
        const lyricsContent = document.getElementById('lyricsContent');

        if (identification.identified) {
            songCard.style.display = 'block';

            songTitle.textContent = identification.title || 'Título no identificado';

            // Mostrar botón para buscar letras reales
            const lyricsActions = document.getElementById('lyricsActions');
            if (lyricsActions) {
                lyricsActions.style.display = 'block';
            }
            songArtist.textContent = identification.artist || 'Artista desconocido';
            songAlbum.textContent = identification.album || '';

            const confidence = Math.round((identification.confidence || 0) * 100);
            confidenceFill.style.width = `${confidence}%`;
            confidenceText.textContent = `${confidence}%`;

            if (identification.lyrics && identification.lyrics.trim() !== '') {
                lyricsCard.style.display = 'block';
                const formattedLyrics = this.formatLyrics(identification.lyrics);
                lyricsContent.innerHTML = `<pre>${formattedLyrics}</pre>`;
            }

            if (identification.music_links) {
                musicLinks.style.display = 'block';

                document.getElementById('youtubeLink').href = identification.music_links.youtube || '#';
                document.getElementById('spotifyLink').href = identification.music_links.spotify || '#';
                document.getElementById('appleMusicLink').href = identification.music_links.apple_music || '#';
                document.getElementById('deezerLink').href = identification.music_links.deezer || '#';
            }

            const sourceMessage = identification.source === 'filename' ?
                '📁 Información extraída del nombre del archivo' :
                '🎵 Canción identificada por análisis de audio';

            this.showNotification(`${sourceMessage}: ${identification.title} - ${identification.artist}`, 'success');
        } else {
            songCard.style.display = 'block';
            songTitle.textContent = 'Canción no identificada';
            songArtist.textContent = 'Intenta con mejor calidad de audio o agrega la canción a la base de datos';
            confidenceFill.style.width = '0%';
            confidenceText.textContent = '0%';

            this.showNotification('❌ No se pudo identificar la canción. Intenta con mejor calidad de audio.', 'warning');
        }
    }

    showLoadingState(message = 'Procesando...') {
        const loadingState = document.getElementById('loadingState');
        const loadingText = loadingState.querySelector('p');

        loadingText.textContent = message;
        loadingState.style.display = 'block';

        document.getElementById('resultsContainer').style.display = 'block';
        document.getElementById('resultsContent').style.display = 'none';
        document.getElementById('errorState').style.display = 'none';
    }

    hideLoadingState() {
        document.getElementById('loadingState').style.display = 'none';
    }

    showErrorState(message) {
        const errorState = document.getElementById('errorState');
        const errorMessage = document.getElementById('errorMessage');

        errorMessage.textContent = message;
        errorState.style.display = 'block';

        document.getElementById('resultsContainer').style.display = 'block';
        document.getElementById('loadingState').style.display = 'none';
        document.getElementById('resultsContent').style.display = 'none';
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    formatDuration(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }

    async exportResults(format) {
        if (!this.currentAnalysisId) {
            this.showNotification('No hay resultados para exportar', 'warning');
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/audio/${this.currentAnalysisId}/export?format=${format}`);

            if (!response.ok) {
                throw new Error('Error al exportar resultados');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `music_analysis_${this.currentAnalysisId}.${format}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

        } catch (error) {
            console.error('Error en exportación:', error);
            this.showNotification(`Error al exportar: ${error.message}`, 'error');
        }
    }
}

// Instancia global de la aplicación
const app = new MusicAnalysisApp();

// Variable global para timeline completo
let fullTimelineData = [];

// FUNCIONES GLOBALES PARA EVENTOS DEL HTML

async function startRecording() {
    if (app.isRecording) return;

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        app.mediaRecorder = new MediaRecorder(stream);
        app.recordingChunks = [];
        app.isRecording = true;

        app.mediaRecorder.ondataavailable = (event) => {
            app.recordingChunks.push(event.data);
        };

        app.mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(app.recordingChunks, { type: 'audio/wav' });
            const audioFile = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });

            // Mostrar preview del audio grabado
            app.showAudioPreview(audioFile);

            // HACER EXACTAMENTE LO MISMO QUE CON UN ARCHIVO SUBIDO
            try {
                // Primero hacer análisis musical completo (igual que archivo subido)
                await app.analyzeAudio(audioFile);

                // Luego intentar identificar la canción
                setTimeout(async () => {
                    try {
                        await identifySongFromFile(audioFile);
                    } catch (error) {
                        console.log('No se pudo identificar la canción grabada:', error.message);
                    }
                }, 2000);

            } catch (error) {
                console.error('Error en análisis de grabación:', error);
                app.showErrorState(`Error al analizar grabación: ${error.message}`);
            }

            // Limpiar
            stream.getTracks().forEach(track => track.stop());
        };

        app.mediaRecorder.start();

        document.getElementById('recordText').textContent = 'Grabando... Suelta para parar';
        document.getElementById('recordingTimer').style.display = 'block';

        app.recordingStartTime = Date.now();
        app.recordingTimer = setInterval(() => {
            const elapsed = Math.floor((Date.now() - app.recordingStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            document.getElementById('recordingTimer').textContent =
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);

    } catch (error) {
        console.error('Error al iniciar grabación:', error);
        app.showNotification('Error al acceder al micrófono', 'error');
    }
}

function stopRecording() {
    if (!app.isRecording || !app.mediaRecorder) return;

    app.mediaRecorder.stop();
    app.isRecording = false;

    if (app.recordingTimer) {
        clearInterval(app.recordingTimer);
        app.recordingTimer = null;
    }

    document.getElementById('recordText').textContent = 'Mantén presionado para grabar';
    document.getElementById('recordingTimer').style.display = 'none';
}

// NUEVA FUNCIÓN PARA YOUTUBE - SEPARADA DEL RESTO
async function downloadFromYouTube() {
    const urlInput = document.getElementById('youtubeUrl');
    const progressDiv = document.getElementById('youtubeProgress');
    const progressFill = document.getElementById('youtubeProgressFill');
    const progressText = document.getElementById('youtubeProgressText');
    const downloadBtn = document.getElementById('youtubeDownloadBtn');

    const url = urlInput.value.trim();
    const downloadType = document.querySelector('input[name="downloadType"]:checked').value;

    console.log('🎬 Iniciando descarga de YouTube:', url, downloadType);

    if (!url) {
        app.showNotification('Por favor, ingresa una URL de YouTube válida', 'warning');
        return;
    }

    const youtubeRegex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
    if (!youtubeRegex.test(url)) {
        app.showNotification('Por favor, ingresa una URL de YouTube válida', 'error');
        return;
    }

    try {
        downloadBtn.disabled = true;
        downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Descargando...';
        progressDiv.style.display = 'block';
        progressText.textContent = '🔍 Analizando video de YouTube...';
        progressFill.style.width = '10%';

        // Verificar si el backend de YouTube está disponible
        try {
            const healthCheck = await fetch('http://localhost:5005/api/health');
            if (!healthCheck.ok) {
                throw new Error('Backend de YouTube no disponible');
            }
        } catch (error) {
            throw new Error('Backend de YouTube no está ejecutándose. Ejecuta: iniciar_servidor_youtube.bat');
        }

        let endpoint, requestBody;

        if (downloadType === 'audio') {
            const format = document.getElementById('audioFormat').value;
            console.log('🎵 Formato de audio seleccionado:', format);
            endpoint = '/api/audio/youtube-download';
            requestBody = { url: url, format: format };
            progressText.textContent = `⬇️ Descargando audio en ${format.toUpperCase()}...`;
        } else {
            const quality = document.getElementById('videoQuality').value;
            console.log('🎬 Calidad de video seleccionada:', quality);
            endpoint = '/api/audio/youtube-video';
            requestBody = { url: url, quality: quality };
            progressText.textContent = `⬇️ Descargando video en ${quality}...`;
        }

        console.log('📡 Endpoint:', endpoint);
        console.log('📦 Request body:', requestBody);

        progressFill.style.width = '30%';

        const response = await fetch(`http://localhost:5005${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        progressFill.style.width = '70%';

        const result = await response.json();

        console.log('📊 Resultado de descarga:', result);

        if (!response.ok) {
            throw new Error(result.error || 'Error al descargar desde YouTube');
        }

        if (!result.success) {
            throw new Error(result.error || 'Error en la descarga');
        }

        progressFill.style.width = '100%';
        progressText.textContent = '✅ Descarga completada';

        displayDownloadedFileInfo(result);

        // Mostrar gestión de descargas
        document.getElementById('downloadsCard').style.display = 'block';
        refreshDownloads();

        app.showNotification(`✅ Descarga exitosa: ${result.title}`, 'success');

        setTimeout(() => {
            progressDiv.style.display = 'none';
            progressFill.style.width = '0%';
        }, 3000);

    } catch (error) {
        console.error('❌ Error completo en descarga:', error);
        console.error('❌ Stack trace:', error.stack);

        // Mensajes de error más específicos
        let errorMessage = error.message;
        if (error.message.includes('Failed to fetch')) {
            errorMessage = 'No se puede conectar con el servidor de YouTube. Ejecuta: iniciar_servidor_youtube.bat';
        } else if (error.message.includes('Video unavailable')) {
            errorMessage = 'Video no disponible. Puede estar privado, eliminado o restringido geográficamente.';
        } else if (error.message.includes('Sign in to confirm')) {
            errorMessage = 'Este video requiere verificación de edad. Intenta con otro video.';
        }

        app.showNotification(`Error: ${errorMessage}`, 'error');
        progressText.textContent = `❌ Error: ${errorMessage}`;
        progressFill.style.width = '0%';

        setTimeout(() => {
            progressDiv.style.display = 'none';
        }, 5000);
    } finally {
        downloadBtn.disabled = false;
        const buttonText = downloadType === 'audio' ? 'Descargar Audio' : 'Descargar Video';
        downloadBtn.innerHTML = `<i class="fas fa-download"></i> <span id="downloadButtonText">${buttonText}</span>`;
    }
}

function displayDownloadedFileInfo(downloadResult) {
    const audioPreview = document.getElementById('audioPreview');
    const audioInfo = document.getElementById('audioInfo');

    audioPreview.style.display = 'block';

    audioInfo.innerHTML = `
        <div class="download-info">
            <h5><i class="fab fa-youtube"></i> Descargado desde YouTube</h5>
            <p><strong>Título:</strong> ${downloadResult.title || 'Título no disponible'}</p>
            <p><strong>Canal:</strong> ${downloadResult.artist || 'Canal no disponible'}</p>
            <p><strong>Duración:</strong> ${app.formatDuration(downloadResult.duration || 0)}</p>
            <p><strong>Formato:</strong> ${downloadResult.format || 'MP3'}</p>
            <p><strong>Tamaño:</strong> ${(downloadResult.file_size / 1024 / 1024).toFixed(2)} MB</p>
            <p><strong>Archivo:</strong> ${downloadResult.file_path || 'Descargado'}</p>
        </div>
    `;
}

async function identifySongFromFile(file) {
    try {
        app.showLoadingState('Identificando canción...');

        const formData = new FormData();
        formData.append('audio', file);

        const response = await fetch(`${app.apiBaseUrl}/audio/identify`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Error al identificar canción');
        }

        app.displaySongIdentification(result);
        app.hideLoadingState();

    } catch (error) {
        console.error('Error al identificar canción:', error);
        app.hideLoadingState();
        app.showErrorState(`Error al identificar canción: ${error.message}`);
    }
}

function toggleFullTimeline() {
    const timeline = document.getElementById('timeline');
    const timelineFull = document.getElementById('timelineFull');
    const toggleBtn = document.getElementById('toggleTimelineBtn');

    if (timelineFull.style.display === 'none') {
        timeline.style.display = 'none';
        timelineFull.style.display = 'block';
        toggleBtn.innerHTML = '<i class="fas fa-compress"></i> Ver Progresión Resumida';

        if (fullTimelineData.length > 0) {
            displayFullTimeline(fullTimelineData);
        }
    } else {
        timeline.style.display = 'block';
        timelineFull.style.display = 'none';
        toggleBtn.innerHTML = '<i class="fas fa-expand"></i> Ver Progresión Completa';
    }
}

function displayFullTimeline(timelineData) {
    const container = document.getElementById('timelineFull');
    container.innerHTML = '';

    timelineData.forEach((item, index) => {
        const timelineItem = document.createElement('div');
        timelineItem.className = 'timeline-item-full';
        timelineItem.innerHTML = `
            <span class="timeline-time">${item.time}</span>
            <span class="timeline-chord">${item.chord}</span>
            <span class="timeline-confidence">${item.confidence ? (item.confidence * 100).toFixed(0) + '%' : ''}</span>
        `;
        container.appendChild(timelineItem);
    });
}

function resetUpload() {
    document.getElementById('resultsContainer').style.display = 'none';
    document.getElementById('audioPreview').style.display = 'none';
    document.getElementById('youtubeUrl').value = '';
    document.getElementById('audioFile').value = '';
}

function exportResults(format) {
    app.exportResults(format);
}

// FUNCIONES MEJORADAS PARA YOUTUBE
async function previewYouTubeVideo() {
    const urlInput = document.getElementById('youtubeUrl');
    const url = urlInput.value.trim();

    if (!url) {
        app.showNotification('Por favor, ingresa una URL de YouTube', 'warning');
        return;
    }

    const youtubeRegex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
    if (!youtubeRegex.test(url)) {
        app.showNotification('Por favor, ingresa una URL de YouTube válida', 'error');
        return;
    }

    try {
        const response = await fetch('http://localhost:5005/api/audio/youtube-info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(result.error || 'Error al obtener información del video');
        }

        // Mostrar vista previa
        document.getElementById('videoTitle').textContent = result.title;
        document.getElementById('videoChannel').textContent = result.uploader;
        document.getElementById('videoDuration').textContent = `⏱️ ${result.duration_formatted}`;
        document.getElementById('videoViews').textContent = `👀 ${result.view_count_formatted}`;
        document.getElementById('videoDate').textContent = `📅 ${result.upload_date_formatted}`;

        document.getElementById('youtubePreview').style.display = 'block';

        app.showNotification(`✅ Video encontrado: ${result.title}`, 'success');

    } catch (error) {
        console.error('Error obteniendo información:', error);
        app.showNotification(`Error: ${error.message}`, 'error');
        document.getElementById('youtubePreview').style.display = 'none';
    }
}

function toggleDownloadOptions() {
    const downloadType = document.querySelector('input[name="downloadType"]:checked').value;
    const audioOptions = document.getElementById('audioOptions');
    const videoOptions = document.getElementById('videoOptions');
    const downloadButtonText = document.getElementById('downloadButtonText');

    if (downloadType === 'audio') {
        audioOptions.style.display = 'block';
        videoOptions.style.display = 'none';
        downloadButtonText.textContent = 'Descargar Audio';
    } else {
        audioOptions.style.display = 'none';
        videoOptions.style.display = 'block';
        downloadButtonText.textContent = 'Descargar Video';
    }
}

async function refreshDownloads() {
    try {
        const response = await fetch('http://localhost:5005/api/downloads');
        const result = await response.json();

        const downloadsList = document.getElementById('downloadsList');

        if (!result.success || result.downloads.length === 0) {
            downloadsList.innerHTML = `
                <div class="empty-downloads">
                    <i class="fas fa-folder-open"></i>
                    <p>No hay archivos descargados</p>
                </div>
            `;
            return;
        }

        downloadsList.innerHTML = result.downloads.map(download => `
            <div class="download-item">
                <div class="download-info">
                    <div class="download-name">${download.filename}</div>
                    <div class="download-details">
                        <span>📁 ${download.size_mb} MB</span>
                        <span>📅 ${new Date(download.created * 1000).toLocaleDateString()}</span>
                    </div>
                </div>
                <div class="download-actions">
                    <button onclick="openFile('${download.filename}')" title="Abrir archivo">
                        <i class="fas fa-play"></i>
                    </button>
                    <button onclick="deleteFile('${download.filename}')" title="Eliminar archivo">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error obteniendo descargas:', error);
        app.showNotification('Error al obtener lista de descargas', 'error');
    }
}

function openDownloadsFolder() {
    // En un entorno web, no podemos abrir carpetas directamente
    // Pero podemos mostrar la ubicación
    app.showNotification('📁 Archivos guardados en: ./downloads/', 'info');
}

function openFile(filename) {
    // Crear enlace de descarga
    const link = document.createElement('a');
    link.href = `http://localhost:5005/downloads/${filename}`;
    link.download = filename;
    link.target = '_blank';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function deleteFile(filename) {
    if (confirm(`¿Estás seguro de que quieres eliminar "${filename}"?`)) {
        // Aquí podrías implementar una API para eliminar archivos
        app.showNotification('Función de eliminación no implementada', 'warning');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎵 Music Analysis App - Versión Completa Cargada');

    // Inicializar opciones de descarga
    toggleDownloadOptions();
});