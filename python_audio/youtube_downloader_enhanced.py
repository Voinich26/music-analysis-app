#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DESCARGADOR MEJORADO DE YOUTUBE
Basado en el script proporcionado por el usuario con mejoras adicionales
"""

import yt_dlp
import os
import json
import sys
import time
import subprocess
from pathlib import Path

def youtube_downloader(url, quality='720p', audio_only=False, output_format='mp3'):
    """
    Descargador completo de YouTube con opciones avanzadas
    
    Args:
        url: URL del video de YouTube
        quality: Calidad del video ('720p', '1080p', 'best')
        audio_only: Si True, descarga solo audio
        output_format: Formato de salida ('mp3', 'wav', 'm4a', 'flac')
    
    Returns:
        dict: Resultado de la descarga con información del archivo
    """
    
    # Crear directorio de descargas
    output_dir = './downloads/'
    os.makedirs(output_dir, exist_ok=True)
    
    # Configuración base mejorada
    ydl_opts = {
        'outtmpl': output_dir + '%(title)s.%(ext)s',
        'quiet': False,
        'no_warnings': False,
        'extract_flat': False,
        'writethumbnail': False,
        'writeinfojson': False,
    }
    
    if audio_only:
        # Configuración optimizada para audio
        ydl_opts['format'] = 'bestaudio/best'
        
        # Verificar si FFmpeg está disponible
        ffmpeg_available = check_ffmpeg_availability()
        
        if ffmpeg_available:
            # Usar FFmpeg para conversión de alta calidad
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': output_format,
                'preferredquality': '192' if output_format == 'mp3' else '0',  # 0 = mejor calidad para otros formatos
            }]
            
            # Configuraciones específicas por formato
            if output_format == 'flac':
                ydl_opts['postprocessors'][0]['preferredquality'] = '0'  # Sin compresión
            elif output_format == 'wav':
                ydl_opts['postprocessors'][0]['preferredquality'] = '0'  # Sin compresión
                
        else:
            print("⚠️ FFmpeg no disponible, descargando en formato nativo")
            # Intentar obtener el mejor formato de audio disponible
            if output_format == 'mp3':
                ydl_opts['format'] = 'bestaudio[ext=mp3]/bestaudio[ext=m4a]/bestaudio'
            else:
                ydl_opts['format'] = 'bestaudio'
    else:
        # Configuración para video con audio
        if quality == '720p':
            ydl_opts['format'] = 'best[height<=720]/best'
        elif quality == '1080p':
            ydl_opts['format'] = 'best[height<=1080]/best'
        elif quality == '480p':
            ydl_opts['format'] = 'best[height<=480]/best'
        elif quality == '360p':
            ydl_opts['format'] = 'best[height<=360]/best'
        else:
            ydl_opts['format'] = 'best'
    
    try:
        print(f"🎬 Iniciando descarga desde: {url}")
        print(f"📁 Directorio: {os.path.abspath(output_dir)}")
        print(f"🎵 Solo audio: {audio_only}")
        print(f"📺 Calidad: {quality}")
        print(f"🔧 Formato: {output_format}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extraer información del video primero
            print("📋 Obteniendo información del video...")
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Video Descargado')
            uploader = info.get('uploader', 'Desconocido')
            duration = info.get('duration', 0)
            view_count = info.get('view_count', 0)
            upload_date = info.get('upload_date', '')
            
            print(f"📺 Título: {title}")
            print(f"👤 Canal: {uploader}")
            print(f"⏱️ Duración: {format_duration(duration)}")
            print(f"👀 Visualizaciones: {format_number(view_count)}")
            print(f"📅 Fecha: {format_date(upload_date)}")
            
            # Verificar si el video es muy largo (más de 1 hora)
            if duration > 3600:
                print("⚠️ Video largo detectado (>1h), esto puede tomar tiempo...")
            
            # Iniciar descarga
            print("⬇️ Iniciando descarga...")
            start_time = time.time()
            
            ydl.download([url])
            
            download_time = time.time() - start_time
            print(f"⏱️ Tiempo de descarga: {format_duration(int(download_time))}")
            
            # Buscar archivo descargado
            downloaded_file = find_downloaded_file(output_dir, title, output_format if audio_only else 'mp4')
            
            if downloaded_file and os.path.exists(downloaded_file):
                file_size = os.path.getsize(downloaded_file)
                print(f"✅ Descarga completada: {format_file_size(file_size)}")
                
                # Información adicional del archivo
                file_info = get_file_info(downloaded_file)
                
                return {
                    'success': True,
                    'file_path': downloaded_file,
                    'title': clean_string(title),
                    'artist': clean_string(uploader),
                    'duration': duration,
                    'format': output_format if audio_only else 'mp4',
                    'file_size': file_size,
                    'audio_only': audio_only,
                    'quality': quality,
                    'view_count': view_count,
                    'upload_date': upload_date,
                    'download_time': download_time,
                    'file_info': file_info
                }
            else:
                return {
                    'success': False,
                    'error': 'Archivo descargado no encontrado en el directorio'
                }
                
    except yt_dlp.DownloadError as e:
        error_msg = str(e)
        print(f"❌ Error de descarga: {error_msg}")
        
        # Sugerir soluciones comunes
        if "Video unavailable" in error_msg:
            print("💡 Sugerencia: El video puede estar privado, eliminado o restringido geográficamente")
        elif "Sign in to confirm your age" in error_msg:
            print("💡 Sugerencia: El video requiere verificación de edad")
        elif "network" in error_msg.lower():
            print("💡 Sugerencia: Verifica tu conexión a internet")
            
        return {
            'success': False,
            'error': f'Error de descarga: {error_msg}'
        }
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return {
            'success': False,
            'error': f'Error inesperado: {str(e)}'
        }

def check_ffmpeg_availability():
    """Verificar si FFmpeg está disponible en el sistema"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, 
                      check=True, 
                      timeout=10)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False

def find_downloaded_file(directory, title, expected_format):
    """Buscar el archivo descargado en el directorio"""
    # Limpiar título para búsqueda
    clean_title = clean_filename(title)
    
    # Buscar archivos en el directorio
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        
        # Verificar si es un archivo (no directorio)
        if not os.path.isfile(file_path):
            continue
            
        # Buscar por título limpio
        if clean_title.lower() in file.lower():
            return file_path
            
        # Buscar por extensión esperada
        if file.endswith(f'.{expected_format}'):
            return file_path
    
    # Si no se encuentra, devolver el archivo más reciente
    files = [os.path.join(directory, f) for f in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, f))]
    
    if files:
        return max(files, key=os.path.getctime)
    
    return None

def get_file_info(file_path):
    """Obtener información adicional del archivo"""
    try:
        stat = os.stat(file_path)
        return {
            'created': time.ctime(stat.st_ctime),
            'modified': time.ctime(stat.st_mtime),
            'size_mb': round(stat.st_size / (1024 * 1024), 2)
        }
    except:
        return {}

def clean_string(text):
    """Limpiar string para evitar problemas de encoding"""
    if not text:
        return ""
    # Mantener solo caracteres ASCII seguros
    return ''.join(c for c in text if ord(c) < 128 and c.isprintable())

def clean_filename(filename):
    """Limpiar nombre de archivo para búsqueda"""
    if not filename:
        return ""
    # Remover caracteres problemáticos para nombres de archivo
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename.strip()

def format_duration(seconds):
    """Formatear duración en formato legible"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def format_number(num):
    """Formatear números grandes"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return str(num)

def format_file_size(size_bytes):
    """Formatear tamaño de archivo"""
    if size_bytes >= 1_073_741_824:  # GB
        return f"{size_bytes/1_073_741_824:.2f} GB"
    elif size_bytes >= 1_048_576:  # MB
        return f"{size_bytes/1_048_576:.2f} MB"
    elif size_bytes >= 1024:  # KB
        return f"{size_bytes/1024:.2f} KB"
    else:
        return f"{size_bytes} bytes"

def format_date(date_str):
    """Formatear fecha de upload"""
    if not date_str or len(date_str) != 8:
        return "Desconocida"
    
    try:
        year = date_str[:4]
        month = date_str[4:6]
        day = date_str[6:8]
        return f"{day}/{month}/{year}"
    except:
        return "Desconocida"

# Funciones de conveniencia para compatibilidad
def download_youtube_audio(url, format_type='mp3'):
    """Función específica para descargar solo audio"""
    return youtube_downloader(url, audio_only=True, output_format=format_type)

def download_youtube_video(url, quality='720p'):
    """Función específica para descargar video"""
    return youtube_downloader(url, quality=quality, audio_only=False)

def get_video_info(url):
    """Obtener información del video sin descargar"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                'success': True,
                'title': clean_string(info.get('title', 'Sin título')),
                'uploader': clean_string(info.get('uploader', 'Desconocido')),
                'duration': info.get('duration', 0),
                'view_count': info.get('view_count', 0),
                'upload_date': info.get('upload_date', ''),
                'description': clean_string(info.get('description', ''))[:200] + '...' if info.get('description') else '',
                'thumbnail': info.get('thumbnail', ''),
                'formats_available': len(info.get('formats', [])),
                'duration_formatted': format_duration(info.get('duration', 0)),
                'view_count_formatted': format_number(info.get('view_count', 0)),
                'upload_date_formatted': format_date(info.get('upload_date', ''))
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': f'Error obteniendo información: {str(e)}'
        }

def test_downloader():
    """Función de prueba del descargador"""
    print("🧪 PROBANDO DESCARGADOR MEJORADO DE YOUTUBE")
    print("=" * 60)
    
    # URL de prueba (Rick Roll - video corto y siempre disponible)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("1. Verificando FFmpeg...")
    ffmpeg_ok = check_ffmpeg_availability()
    print(f"   FFmpeg disponible: {'✅ Sí' if ffmpeg_ok else '❌ No'}")
    
    print("\n2. Obteniendo información del video...")
    info = get_video_info(test_url)
    if info['success']:
        print(f"   Título: {info['title']}")
        print(f"   Canal: {info['uploader']}")
        print(f"   Duración: {info['duration_formatted']}")
        print(f"   Vistas: {info['view_count_formatted']}")
    else:
        print(f"   ❌ Error: {info['error']}")
        return
    
    print("\n3. Descargando audio de prueba...")
    result = download_youtube_audio(test_url, 'mp3')
    
    if result['success']:
        print(f"   ✅ Descarga exitosa!")
        print(f"   Archivo: {result['file_path']}")
        print(f"   Tamaño: {format_file_size(result['file_size'])}")
    else:
        print(f"   ❌ Error: {result['error']}")

if __name__ == "__main__":
    # Verificar si es modo de prueba
    if '--test' in sys.argv:
        test_downloader()
    elif len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        url = sys.argv[1]
        
        # Parsear argumentos adicionales
        audio_only = '--audio' in sys.argv or '-a' in sys.argv
        format_type = 'mp3'  # default
        quality = '720p'     # default
        
        # Buscar formato específico
        for i, arg in enumerate(sys.argv):
            if arg in ['--format', '-f'] and i + 1 < len(sys.argv):
                format_type = sys.argv[i + 1]
            elif arg in ['--quality', '-q'] and i + 1 < len(sys.argv):
                quality = sys.argv[i + 1]
        
        try:
            if audio_only:
                result = download_youtube_audio(url, format_type)
            else:
                result = download_youtube_video(url, quality)
            
            # Limpiar resultado para JSON
            if 'title' in result:
                result['title'] = clean_string(result['title'])
            if 'artist' in result:
                result['artist'] = clean_string(result['artist'])
                
            print(json.dumps(result, ensure_ascii=True, indent=2))
            
        except Exception as e:
            error_result = {
                'success': False,
                'error': clean_string(str(e))
            }
            print(json.dumps(error_result, ensure_ascii=True))
    else:
        # Mostrar ayuda
        print("Uso:")
        print("  python youtube_downloader_enhanced.py <URL> [opciones]")
        print("")
        print("Opciones:")
        print("  --audio, -a          Descargar solo audio")
        print("  --format, -f FORMAT  Formato de audio (mp3, wav, m4a, flac)")
        print("  --quality, -q QUAL   Calidad de video (360p, 480p, 720p, 1080p)")
        print("  --test               Ejecutar pruebas")
        print("")
        print("Ejemplos:")
        print("  python youtube_downloader_enhanced.py 'https://youtube.com/watch?v=...' --audio")
        print("  python youtube_downloader_enhanced.py 'https://youtube.com/watch?v=...' --audio --format flac")
        print("  python youtube_downloader_enhanced.py 'https://youtube.com/watch?v=...' --quality 1080p")