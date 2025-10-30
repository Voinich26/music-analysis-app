#!/usr/bin/env python3
"""
INTEGRACIÓN COMPLETA TIPO SHAZAM
- Identificación de canciones con múltiples APIs
- Búsqueda de letras automática
- Enlaces a plataformas de música
- Descarga de YouTube
"""

import requests
import json
import os
import re
import tempfile
from urllib.parse import quote_plus

class ShazamIntegration:
    def __init__(self):
        self.apis = {
            'audd': 'https://api.audd.io/',
            'acoustid': 'https://api.acoustid.org/v2/lookup',
            'musicbrainz': 'https://musicbrainz.org/ws/2/'
        }
        
    def identify_song_complete(self, audio_path):
        """Identificación completa de canción con múltiples métodos"""
        try:
            # Método 1: AudD API (más preciso)
            result = self._identify_with_audd(audio_path)
            if result.get('identified'):
                return self._enrich_song_data(result)
            
            # Método 2: ACRCloud (alternativo)
            result = self._identify_with_acrcloud(audio_path)
            if result.get('identified'):
                return self._enrich_song_data(result)
            
            # Método 3: Análisis local mejorado
            result = self._identify_local_enhanced(audio_path)
            if result.get('identified'):
                return self._enrich_song_data(result)
            
            return {
                'identified': False,
                'title': 'No identificado',
                'artist': 'No identificado',
                'confidence': 0.0
            }
            
        except Exception as e:
            print(f"Error en identificación: {e}")
            return {'identified': False}
    
    def _identify_with_audd(self, audio_path):
        """Identificar con AudD API"""
        try:
            # Verificar tamaño del archivo
            if os.path.getsize(audio_path) > 3 * 1024 * 1024:  # Max 3MB
                return {'identified': False}
            
            with open(audio_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'return': 'apple_music,spotify,lyrics,deezer',
                    'api_token': 'test'  # Usar token real en producción
                }
                
                response = requests.post(
                    self.apis['audd'], 
                    files=files, 
                    data=data, 
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('status') == 'success' and result.get('result'):
                        song = result['result']
                        return {
                            'identified': True,
                            'title': song.get('title', ''),
                            'artist': song.get('artist', ''),
                            'album': song.get('album', ''),
                            'release_date': song.get('release_date', ''),
                            'confidence': 0.95,
                            'source': 'AudD API',
                            'raw_data': song
                        }
            
            return {'identified': False}
            
        except Exception as e:
            print(f"Error AudD: {e}")
            return {'identified': False}
    
    def _identify_with_acrcloud(self, audio_path):
        """Identificar con ACRCloud (método alternativo)"""
        try:
            # Implementación básica - requiere configuración de API
            # En producción, usar credenciales reales de ACRCloud
            return {'identified': False}
            
        except Exception:
            return {'identified': False}
    
    def _identify_local_enhanced(self, audio_path):
        """Identificación local mejorada con base de datos expandida"""
        try:
            import librosa
            import numpy as np
            
            # Cargar audio
            y, sr = librosa.load(audio_path, sr=22050, duration=60)
            
            # Extraer características mejoradas
            features = self._extract_audio_features(y, sr)
            
            # Base de datos expandida
            songs_db = self._get_expanded_song_database()
            
            best_match = None
            best_score = 0
            
            for song_id, song_data in songs_db.items():
                score = self._calculate_similarity_score(features, song_data['features'])
                
                if score > best_score and score > 0.75:
                    best_score = score
                    best_match = {
                        'identified': True,
                        'title': song_data['title'],
                        'artist': song_data['artist'],
                        'album': song_data.get('album', ''),
                        'confidence': score,
                        'source': 'Base de datos local'
                    }
            
            return best_match or {'identified': False}
            
        except Exception as e:
            print(f"Error identificación local: {e}")
            return {'identified': False}
    
    def _extract_audio_features(self, y, sr):
        """Extraer características de audio mejoradas"""
        try:
            import librosa
            import numpy as np
            
            # Características básicas
            tempo = librosa.beat.beat_track(y=y, sr=sr)[0]
            chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=1)
            mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
            zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
            
            return {
                'tempo': float(tempo),
                'chroma': chroma.tolist(),
                'mfcc': mfcc.tolist(),
                'spectral_centroid': float(spectral_centroid),
                'spectral_rolloff': float(spectral_rolloff),
                'zero_crossing_rate': float(zero_crossing_rate)
            }
            
        except Exception:
            return {}
    
    def _get_expanded_song_database(self):
        """Base de datos expandida de canciones - CARGA DESDE ARCHIVO LOCAL"""
        try:
            # Cargar base de datos local si existe
            local_db_file = 'local_songs_database.json'
            if os.path.exists(local_db_file):
                with open(local_db_file, 'r', encoding='utf-8') as f:
                    local_db = json.load(f)
                
                # Convertir formato de base de datos local al formato esperado
                converted_db = {}
                for song_id, song_data in local_db.items():
                    converted_db[song_id] = {
                        'title': song_data['title'],
                        'artist': song_data['artist'],
                        'album': song_data.get('album', ''),
                        'features': song_data['features']
                    }
                
                print(f"✅ Cargadas {len(converted_db)} canciones de base de datos local")
                return converted_db
            
        except Exception as e:
            print(f"⚠️  Error cargando base de datos local: {e}")
        
        # Base de datos por defecto si no hay archivo local
        return {
            'what_a_fool_believes': {
                'title': 'What a Fool Believes',
                'artist': 'The Doobie Brothers',
                'album': 'Minute by Minute',
                'features': {
                    'tempo': 126.0,
                    'chroma': [0.8, 0.3, 0.6, 0.2, 0.7, 0.4, 0.5, 0.9, 0.3, 0.6, 0.2, 0.4],
                    'spectral_centroid': 2100.0
                }
            },
            'hotel_california': {
                'title': 'Hotel California',
                'artist': 'Eagles',
                'album': 'Hotel California',
                'features': {
                    'tempo': 75.0,
                    'chroma': [0.6, 0.8, 0.3, 0.7, 0.2, 0.5, 0.4, 0.6, 0.9, 0.3, 0.5, 0.2],
                    'spectral_centroid': 1800.0
                }
            },
            'bohemian_rhapsody': {
                'title': 'Bohemian Rhapsody',
                'artist': 'Queen',
                'album': 'A Night at the Opera',
                'features': {
                    'tempo': 72.0,
                    'chroma': [0.9, 0.4, 0.7, 0.3, 0.8, 0.5, 0.6, 0.7, 0.4, 0.8, 0.3, 0.6],
                    'spectral_centroid': 2300.0
                }
            }
        }
    
    def _calculate_similarity_score(self, features1, features2):
        """Calcular puntuación de similitud mejorada"""
        try:
            import numpy as np
            
            score = 0
            weights = {
                'tempo': 0.2,
                'chroma': 0.4,
                'spectral_centroid': 0.2,
                'mfcc': 0.2
            }
            
            # Comparar tempo
            if 'tempo' in features1 and 'tempo' in features2:
                tempo_diff = abs(features1['tempo'] - features2['tempo'])
                tempo_score = max(0, 1 - tempo_diff / 50)  # Normalizar
                score += tempo_score * weights['tempo']
            
            # Comparar chroma
            if 'chroma' in features1 and 'chroma' in features2:
                chroma1 = np.array(features1['chroma'])
                chroma2 = np.array(features2['chroma'])
                chroma_corr = np.corrcoef(chroma1, chroma2)[0, 1]
                if not np.isnan(chroma_corr):
                    score += max(0, chroma_corr) * weights['chroma']
            
            # Comparar centroide espectral
            if 'spectral_centroid' in features1 and 'spectral_centroid' in features2:
                centroid_diff = abs(features1['spectral_centroid'] - features2['spectral_centroid'])
                centroid_score = max(0, 1 - centroid_diff / 2000)
                score += centroid_score * weights['spectral_centroid']
            
            return min(1.0, score)
            
        except Exception:
            return 0
    
    def _enrich_song_data(self, song_data):
        """Enriquecer datos de la canción con letras y enlaces"""
        try:
            if not song_data.get('identified'):
                return song_data
            
            title = song_data.get('title', '')
            artist = song_data.get('artist', '')
            
            # Buscar letra
            lyrics = self._get_lyrics(title, artist)
            song_data['lyrics'] = lyrics
            
            # Generar enlaces
            links = self._generate_music_links(title, artist)
            song_data['music_links'] = links
            
            return song_data
            
        except Exception as e:
            print(f"Error enriqueciendo datos: {e}")
            return song_data
    
    def _get_lyrics(self, title, artist):
        """Obtener letra de la canción"""
        try:
            # Método 1: API de Lyrics.ovh
            lyrics = self._get_lyrics_from_api(title, artist)
            if lyrics:
                return lyrics
            
            # Método 2: Base de datos local
            lyrics = self._get_lyrics_local(title, artist)
            if lyrics:
                return lyrics
            
            return "Letra no disponible"
            
        except Exception:
            return "Letra no disponible"
    
    def _get_lyrics_from_api(self, title, artist):
        """Obtener letra desde API"""
        try:
            # API gratuita de lyrics.ovh
            url = f"https://api.lyrics.ovh/v1/{quote_plus(artist)}/{quote_plus(title)}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('lyrics', '').strip()
            
            return None
            
        except Exception:
            return None
    
    def _get_lyrics_local(self, title, artist):
        """Obtener letra de base de datos local"""
        lyrics_db = {
            ('What a Fool Believes', 'The Doobie Brothers'): """What a fool believes
He sees
No wise man has the power
To reason away
What seems to be
Is always better than nothing
And nothing at all keeps sending him

Somewhere back in her long ago
Where he can still believe there's a place in her life
Someday, somewhere, she will return

She had a place in his life
He never made her think twice
As he rises to her apology
Anybody else would surely know
He's watching her go

But what a fool believes he sees
No wise man has the power to reason away
What seems to be
Is always better than nothing
There's nothing at all
But what a fool believes he sees""",
            
            ('Hotel California', 'Eagles'): """On a dark desert highway, cool wind in my hair
Warm smell of colitas, rising up through the air
Up ahead in the distance, I saw a shimmering light
My head grew heavy and my sight grew dim
I had to stop for the night

There she stood in the doorway
I heard the mission bell
And I was thinking to myself
This could be Heaven or this could be Hell
Then she lit up a candle and she showed me the way
There were voices down the corridor
I thought I heard them say

Welcome to the Hotel California
Such a lovely place (Such a lovely place)
Such a lovely face
Plenty of room at the Hotel California
Any time of year (Any time of year)
You can find it here""",
            
            ('Bohemian Rhapsody', 'Queen'): """Is this the real life?
Is this just fantasy?
Caught in a landslide
No escape from reality
Open your eyes, look up to the skies and see
I'm just a poor boy, I need no sympathy
Because I'm easy come, easy go, little high, little low
Any way the wind blows doesn't really matter to me, to me

Mama, just killed a man
Put a gun against his head, pulled my trigger, now he's dead
Mama, life had just begun
But now I've gone and thrown it all away"""
        }
        
        key = (title, artist)
        return lyrics_db.get(key, None)
    
    def _generate_music_links(self, title, artist):
        """Generar enlaces a plataformas de música"""
        try:
            query = f"{artist} {title}".replace(' ', '+')
            
            links = {
                'youtube': f"https://www.youtube.com/results?search_query={query}",
                'spotify': f"https://open.spotify.com/search/{quote_plus(f'{artist} {title}')}",
                'apple_music': f"https://music.apple.com/search?term={quote_plus(f'{artist} {title}')}",
                'deezer': f"https://www.deezer.com/search/{query}",
                'amazon_music': f"https://music.amazon.com/search/{query}",
                'youtube_music': f"https://music.youtube.com/search?q={query}"
            }
            
            return links
            
        except Exception:
            return {}

class YouTubeDownloader:
    """Descargador de YouTube integrado"""
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def download_from_url(self, youtube_url, output_format='mp3'):
        """Descargar audio desde URL de YouTube"""
        try:
            # Verificar que sea URL válida de YouTube
            if not self._is_valid_youtube_url(youtube_url):
                return {
                    'success': False,
                    'error': 'URL de YouTube no válida'
                }
            
            # Usar yt-dlp para descarga
            result = self._download_with_ytdlp(youtube_url, output_format)
            
            if result['success']:
                return result
            
            # Método alternativo con pytube
            result = self._download_with_pytube(youtube_url, output_format)
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error en descarga: {str(e)}'
            }
    
    def _is_valid_youtube_url(self, url):
        """Verificar si es URL válida de YouTube"""
        youtube_patterns = [
            r'youtube\.com/watch\?v=',
            r'youtu\.be/',
            r'youtube\.com/embed/',
            r'youtube\.com/v/'
        ]
        
        return any(re.search(pattern, url) for pattern in youtube_patterns)
    
    def _download_with_ytdlp(self, url, format_type):
        """Descargar con yt-dlp - MEJORADO"""
        try:
            import yt_dlp
            import os
            
            # Crear nombre único para el archivo
            import time
            timestamp = int(time.time())
            output_filename = f'youtube_audio_{timestamp}'
            output_path = os.path.join(self.temp_dir, f'{output_filename}.{format_type}')
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.temp_dir, f'{output_filename}.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': format_type,
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Buscar el archivo descargado
                final_path = output_path
                if not os.path.exists(final_path):
                    # Buscar archivos con el nombre base
                    for file in os.listdir(self.temp_dir):
                        if file.startswith(output_filename) and file.endswith(f'.{format_type}'):
                            final_path = os.path.join(self.temp_dir, file)
                            break
                
                return {
                    'success': True,
                    'file_path': final_path,
                    'title': info.get('title', 'Audio descargado'),
                    'artist': info.get('uploader', 'Desconocido'),
                    'duration': info.get('duration', 0)
                }
                
        except ImportError:
            return {'success': False, 'error': 'yt-dlp no está instalado. Ejecuta: pip install yt-dlp'}
        except Exception as e:
            return {'success': False, 'error': f'Error descargando: {str(e)}'}
    
    def _download_with_pytube(self, url, format_type):
        """Descargar con pytube (método alternativo) - MEJORADO"""
        try:
            from pytube import YouTube
            import time
            
            yt = YouTube(url)
            
            # Obtener stream de audio de mejor calidad
            audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
            
            if not audio_stream:
                # Intentar con cualquier stream de audio
                audio_stream = yt.streams.filter(only_audio=True).first()
            
            if not audio_stream:
                return {'success': False, 'error': 'No se encontró stream de audio'}
            
            # Crear nombre único
            timestamp = int(time.time())
            filename = f'youtube_audio_{timestamp}'
            
            # Descargar
            output_path = audio_stream.download(
                output_path=self.temp_dir,
                filename=filename
            )
            
            # Convertir a formato solicitado si es necesario
            if format_type != 'mp4' and format_type != audio_stream.subtype:
                converted_path = self._convert_audio_format(output_path, format_type)
                if converted_path:
                    os.remove(output_path)  # Eliminar original
                    output_path = converted_path
            
            return {
                'success': True,
                'file_path': output_path,
                'title': yt.title,
                'artist': yt.author,
                'duration': yt.length
            }
            
        except ImportError:
            return {'success': False, 'error': 'pytube no está instalado. Ejecuta: pip install pytube'}
        except Exception as e:
            return {'success': False, 'error': f'Error pytube: {str(e)}'}
    
    def _convert_audio_format(self, input_path, output_format):
        """Convertir formato de audio - MEJORADO"""
        try:
            from pydub import AudioSegment
            
            # Cargar audio
            if input_path.lower().endswith('.mp4'):
                audio = AudioSegment.from_file(input_path, format="mp4")
            else:
                audio = AudioSegment.from_file(input_path)
            
            # Crear ruta de salida
            output_path = input_path.rsplit('.', 1)[0] + f'.{output_format}'
            
            # Exportar en formato solicitado
            audio.export(output_path, format=output_format, bitrate="192k")
            
            return output_path
            
        except ImportError:
            return None
        except Exception as e:
            print(f"Error convirtiendo audio: {e}")
            return None

# Funciones de utilidad para integración
def identify_and_enrich_song(audio_path):
    """Función principal para identificar y enriquecer canción"""
    shazam = ShazamIntegration()
    return shazam.identify_song_complete(audio_path)

def download_youtube_audio(youtube_url, format_type='mp3'):
    """Función principal para descargar audio de YouTube"""
    downloader = YouTubeDownloader()
    return downloader.download_from_url(youtube_url, format_type)

if __name__ == "__main__":
    # Prueba básica
    print("Módulo Shazam Integration cargado correctamente")