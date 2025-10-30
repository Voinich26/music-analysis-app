#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BACKEND PARA DESCARGA DE YOUTUBE
Servidor Flask para manejar descargas de YouTube desde el frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import json
import tempfile
import shutil

# Agregar el directorio python_audio al path
sys.path.append('python_audio')

try:
    from youtube_simple_downloader import download_single_youtube_video
    from youtube_downloader_enhanced import get_video_info
    YOUTUBE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Error importando descargador de YouTube: {e}")
    YOUTUBE_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Permitir CORS para el frontend

# Configuración
DOWNLOAD_DIR = './downloads/'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar estado del servidor"""
    return jsonify({
        'status': 'ok',
        'youtube_available': YOUTUBE_AVAILABLE,
        'message': 'Backend de YouTube funcionando'
    })

@app.route('/api/audio/youtube-info', methods=['POST'])
def get_youtube_info():
    """Obtener información de un video de YouTube sin descargarlo"""
    try:
        if not YOUTUBE_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'Descargador de YouTube no disponible. Instala yt-dlp.'
            }), 500
        
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL requerida'
            }), 400
        
        print(f"📋 Obteniendo información de: {url}")
        
        # Obtener información del video
        info = get_video_info(url)
        
        if info['success']:
            return jsonify({
                'success': True,
                'title': info['title'],
                'uploader': info['uploader'],
                'duration': info['duration'],
                'duration_formatted': info['duration_formatted'],
                'view_count': info['view_count'],
                'view_count_formatted': info['view_count_formatted'],
                'upload_date_formatted': info['upload_date_formatted'],
                'thumbnail': info.get('thumbnail', ''),
                'description': info.get('description', '')
            })
        else:
            return jsonify({
                'success': False,
                'error': info['error']
            }), 400
            
    except Exception as e:
        print(f"❌ Error obteniendo información: {e}")
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500

@app.route('/api/audio/youtube-download', methods=['POST'])
def download_youtube_audio():
    """Descargar audio de YouTube"""
    try:
        if not YOUTUBE_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'Descargador de YouTube no disponible. Ejecuta: pip install yt-dlp'
            }), 500
        
        data = request.get_json()
        url = data.get('url')
        format_type = data.get('format', 'mp3')
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL requerida'
            }), 400
        
        print(f"🎬 Descargando desde YouTube: {url} (formato: {format_type})")
        
        # Descargar SOLO el video específico usando el descargador simple
        result = download_single_youtube_video(url, format_type)
        
        if result['success']:
            # Limpiar strings para JSON
            clean_result = {
                'success': True,
                'title': clean_string(result.get('title', 'Audio Descargado')),
                'artist': clean_string(result.get('artist', 'Desconocido')),
                'duration': result.get('duration', 0),
                'format': result.get('format', format_type),
                'file_size': result.get('file_size', 0),
                'file_path': result.get('file_path', ''),
                'download_time': result.get('download_time', 0),
                'view_count': result.get('view_count', 0),
                'upload_date': result.get('upload_date', ''),
                'quality': result.get('quality', '720p')
            }
            
            print(f"✅ Descarga exitosa: {clean_result['title']}")
            return jsonify(clean_result)
        else:
            print(f"❌ Error en descarga: {result['error']}")
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        print(f"❌ Error en descarga: {e}")
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500

@app.route('/api/audio/youtube-video', methods=['POST'])
def download_youtube_video():
    """Descargar video de YouTube"""
    try:
        if not YOUTUBE_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'Descargador de YouTube no disponible. Ejecuta: pip install yt-dlp'
            }), 500
        
        data = request.get_json()
        url = data.get('url')
        quality = data.get('quality', '720p')
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL requerida'
            }), 400
        
        print(f"🎬 Descargando video desde YouTube: {url} (calidad: {quality})")
        
        # Descargar video usando el descargador mejorado
        from youtube_downloader_enhanced import youtube_downloader
        result = youtube_downloader(
            url=url,
            quality=quality,
            audio_only=False
        )
        
        if result['success']:
            # Limpiar strings para JSON
            clean_result = {
                'success': True,
                'title': clean_string(result.get('title', 'Video Descargado')),
                'artist': clean_string(result.get('artist', 'Desconocido')),
                'duration': result.get('duration', 0),
                'format': 'mp4',
                'file_size': result.get('file_size', 0),
                'file_path': result.get('file_path', ''),
                'download_time': result.get('download_time', 0),
                'view_count': result.get('view_count', 0),
                'upload_date': result.get('upload_date', ''),
                'quality': result.get('quality', quality)
            }
            
            print(f"✅ Descarga de video exitosa: {clean_result['title']}")
            return jsonify(clean_result)
        else:
            print(f"❌ Error en descarga de video: {result['error']}")
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        print(f"❌ Error en descarga de video: {e}")
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500

@app.route('/api/downloads', methods=['GET'])
def list_downloads():
    """Listar archivos descargados"""
    try:
        downloads = []
        
        if os.path.exists(DOWNLOAD_DIR):
            for filename in os.listdir(DOWNLOAD_DIR):
                file_path = os.path.join(DOWNLOAD_DIR, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    downloads.append({
                        'filename': filename,
                        'size': stat.st_size,
                        'size_mb': round(stat.st_size / (1024 * 1024), 2),
                        'created': stat.st_ctime,
                        'modified': stat.st_mtime
                    })
        
        return jsonify({
            'success': True,
            'downloads': downloads,
            'total': len(downloads)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error listando descargas: {str(e)}'
        }), 500

def clean_string(text):
    """Limpiar string para evitar problemas de encoding"""
    if not text:
        return ""
    # Mantener solo caracteres ASCII seguros
    return ''.join(c for c in text if ord(c) < 128 and c.isprintable())

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500

if __name__ == '__main__':
    print("🚀 INICIANDO BACKEND DE YOUTUBE")
    print("=" * 50)
    print(f"📁 Directorio de descargas: {os.path.abspath(DOWNLOAD_DIR)}")
    print(f"🎵 YouTube disponible: {'✅ Sí' if YOUTUBE_AVAILABLE else '❌ No'}")
    print("🌐 Servidor corriendo en: http://localhost:5005")
    print("=" * 50)
    
    if not YOUTUBE_AVAILABLE:
        print("⚠️ ADVERTENCIA: yt-dlp no está disponible")
        print("   Ejecuta: pip install yt-dlp")
        print("=" * 50)
    
    app.run(host='0.0.0.0', port=5005, debug=True)