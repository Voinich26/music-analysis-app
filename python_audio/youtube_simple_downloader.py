#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DESCARGADOR SIMPLE DE YOUTUBE - SOLO UN VIDEO
Sin playlists, sin complicaciones, solo descarga el video específico
"""

import yt_dlp
import os
import json
import time

def download_single_youtube_video(url, format_type='mp3'):
    """
    Descarga SOLO un video específico de YouTube
    No playlists, no múltiples videos, solo el que se solicita
    """
    
    # Crear directorio de descargas
    output_dir = './downloads/'
    os.makedirs(output_dir, exist_ok=True)
    
    # Configuración SIMPLE para un solo video
    ydl_opts = {
        'outtmpl': output_dir + '%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'quiet': True,  # Menos verbose
        'no_warnings': True,
        'noplaylist': True,  # IMPORTANTE: No descargar playlists
        'extract_flat': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format_type,
            'preferredquality': '192',
        }],
    }
    
    try:
        print(f"🎬 Descargando SOLO: {url}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Obtener info del video específico
            info = ydl.extract_info(url, download=False)
            
            # Verificar que es un solo video
            if 'entries' in info:
                # Es una playlist, tomar solo el primer video
                info = info['entries'][0]
                print("⚠️ Detectada playlist, tomando solo el primer video")
            
            title = info.get('title', 'Video Descargado')
            uploader = info.get('uploader', 'Desconocido')
            duration = info.get('duration', 0)
            
            print(f"📺 Título: {title}")
            print(f"👤 Canal: {uploader}")
            print(f"⏱️ Duración: {duration}s")
            
            # Descargar SOLO este video
            start_time = time.time()
            ydl.download([url])
            download_time = time.time() - start_time
            
            # Buscar archivo descargado
            downloaded_file = None
            for file in os.listdir(output_dir):
                if file.endswith(f'.{format_type}') and title.replace('/', '_').replace('\\', '_')[:50] in file:
                    downloaded_file = os.path.join(output_dir, file)
                    break
            
            # Si no se encuentra, buscar el más reciente
            if not downloaded_file:
                files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) 
                        if f.endswith(f'.{format_type}')]
                if files:
                    downloaded_file = max(files, key=os.path.getctime)
            
            if downloaded_file and os.path.exists(downloaded_file):
                file_size = os.path.getsize(downloaded_file)
                print(f"✅ Descarga completada: {file_size} bytes")
                
                return {
                    'success': True,
                    'title': clean_string(title),
                    'artist': clean_string(uploader),
                    'duration': duration,
                    'format': format_type,
                    'file_size': file_size,
                    'file_path': downloaded_file,
                    'download_time': download_time
                }
            else:
                return {
                    'success': False,
                    'error': 'Archivo descargado no encontrado'
                }
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def clean_string(text):
    """Limpiar string para evitar problemas de encoding"""
    if not text:
        return ""
    return ''.join(c for c in text if ord(c) < 128 and c.isprintable())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
        format_type = sys.argv[2] if len(sys.argv) > 2 else 'mp3'
        
        result = download_single_youtube_video(url, format_type)
        print(json.dumps(result, ensure_ascii=True, indent=2))
    else:
        print("Uso: python youtube_simple_downloader.py <URL> [formato]")
        print("Ejemplo: python youtube_simple_downloader.py 'https://youtube.com/watch?v=...' mp3")