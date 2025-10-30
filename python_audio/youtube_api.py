#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API SIMPLE PARA INTEGRAR CON FRONTEND
Funciones para usar desde JavaScript o otros scripts
"""

import json
import sys
from youtube_downloader_enhanced import youtube_downloader, get_video_info

def api_get_info(url):
    """API para obtener información del video"""
    try:
        result = get_video_info(url)
        return json.dumps(result, ensure_ascii=True)
    except Exception as e:
        return json.dumps({
            'success': False,
            'error': str(e)
        }, ensure_ascii=True)

def api_download_audio(url, format_type='mp3'):
    """API para descargar solo audio"""
    try:
        result = youtube_downloader(url, audio_only=True, output_format=format_type)
        
        # Limpiar strings para JSON
        if 'title' in result:
            result['title'] = ''.join(c for c in result['title'] if ord(c) < 128)
        if 'artist' in result:
            result['artist'] = ''.join(c for c in result['artist'] if ord(c) < 128)
            
        return json.dumps(result, ensure_ascii=True)
    except Exception as e:
        return json.dumps({
            'success': False,
            'error': str(e)
        }, ensure_ascii=True)

def api_download_video(url, quality='720p'):
    """API para descargar video"""
    try:
        result = youtube_downloader(url, quality=quality, audio_only=False)
        
        # Limpiar strings para JSON
        if 'title' in result:
            result['title'] = ''.join(c for c in result['title'] if ord(c) < 128)
        if 'artist' in result:
            result['artist'] = ''.join(c for c in result['artist'] if ord(c) < 128)
            
        return json.dumps(result, ensure_ascii=True)
    except Exception as e:
        return json.dumps({
            'success': False,
            'error': str(e)
        }, ensure_ascii=True)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python youtube_api.py <comando> <url> [opciones]")
        print("Comandos:")
        print("  info <url>                    - Obtener información")
        print("  audio <url> [formato]         - Descargar audio")
        print("  video <url> [calidad]         - Descargar video")
        sys.exit(1)
    
    comando = sys.argv[1]
    url = sys.argv[2]
    
    if comando == 'info':
        print(api_get_info(url))
    elif comando == 'audio':
        formato = sys.argv[3] if len(sys.argv) > 3 else 'mp3'
        print(api_download_audio(url, formato))
    elif comando == 'video':
        calidad = sys.argv[3] if len(sys.argv) > 3 else '720p'
        print(api_download_video(url, calidad))
    else:
        print(json.dumps({
            'success': False,
            'error': 'Comando no válido'
        }, ensure_ascii=True))