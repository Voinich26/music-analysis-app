#!/usr/bin/env python3
"""
Servidor web simple para el frontend de Music Analysis
Ejecuta el frontend en http://localhost:8080
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Configuración
PORT = 8081
FRONTEND_DIR = "frontend"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)
    
    def end_headers(self):
        # Agregar headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    # Cambiar al directorio del proyecto
    os.chdir(Path(__file__).parent)
    
    # Verificar que el directorio frontend existe
    if not os.path.exists(FRONTEND_DIR):
        print(f"❌ Error: El directorio '{FRONTEND_DIR}' no existe")
        return
    
    # Crear servidor
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🚀 Servidor frontend iniciado en http://localhost:{PORT}")
        print(f"📁 Sirviendo archivos desde: {os.path.abspath(FRONTEND_DIR)}")
        print(f"🌐 Abriendo navegador...")
        print(f"⏹️  Presiona Ctrl+C para detener el servidor")
        
        # Abrir navegador automáticamente
        try:
            webbrowser.open(f"http://localhost:{PORT}")
        except:
            print(f"⚠️  No se pudo abrir el navegador automáticamente")
            print(f"   Abre manualmente: http://localhost:{PORT}")
        
        # Iniciar servidor
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Servidor detenido")

if __name__ == "__main__":
    main()

