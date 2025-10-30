#!/usr/bin/env python3
"""
GESTOR DE BASE DE DATOS LOCAL DE CANCIONES
Permite agregar, eliminar y gestionar canciones en la base de datos local
"""

import os
import json
import librosa
import numpy as np
from shazam_integration import ShazamIntegration

class SongDatabaseManager:
    def __init__(self):
        self.db_file = 'local_songs_database.json'
        self.audio_folder = 'database_audio'
        self.shazam = ShazamIntegration()
        
        # Crear carpeta para audios si no existe
        if not os.path.exists(self.audio_folder):
            os.makedirs(self.audio_folder)
        
        # Cargar base de datos existente
        self.database = self.load_database()
    
    def load_database(self):
        """Cargar base de datos desde archivo JSON"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error cargando base de datos: {e}")
                return {}
        return {}
    
    def save_database(self):
        """Guardar base de datos en archivo JSON"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.database, f, indent=2, ensure_ascii=False)
            print("✅ Base de datos guardada correctamente")
        except Exception as e:
            print(f"❌ Error guardando base de datos: {e}")
    
    def add_song_from_file(self, audio_path, title=None, artist=None, album=None):
        """Agregar canción desde archivo de audio"""
        try:
            if not os.path.exists(audio_path):
                print(f"❌ Archivo no encontrado: {audio_path}")
                return False
            
            print(f"🎵 Procesando: {audio_path}")
            
            # Extraer características del audio
            features = self.extract_audio_features(audio_path)
            if not features:
                print("❌ No se pudieron extraer características del audio")
                return False
            
            # Obtener información de la canción
            if not title or not artist:
                print("📝 Información de la canción:")
                if not title:
                    title = input("  Título: ").strip()
                if not artist:
                    artist = input("  Artista: ").strip()
                if not album:
                    album = input("  Álbum (opcional): ").strip()
            
            if not title or not artist:
                print("❌ Título y artista son obligatorios")
                return False
            
            # Generar ID único
            song_id = f"{artist.lower().replace(' ', '_')}_{title.lower().replace(' ', '_')}"
            
            # Copiar archivo a carpeta de base de datos
            import shutil
            filename = f"{song_id}.{audio_path.split('.')[-1]}"
            dest_path = os.path.join(self.audio_folder, filename)
            shutil.copy2(audio_path, dest_path)
            
            # Crear entrada en base de datos
            song_entry = {
                'title': title,
                'artist': artist,
                'album': album or '',
                'file_path': dest_path,
                'features': features,
                'added_date': self.get_current_date()
            }
            
            self.database[song_id] = song_entry
            self.save_database()
            
            print(f"✅ Canción agregada: {title} - {artist}")
            return True
            
        except Exception as e:
            print(f"❌ Error agregando canción: {e}")
            return False
    
    def extract_audio_features(self, audio_path):
        """Extraer características de audio para identificación"""
        try:
            # Cargar audio
            y, sr = librosa.load(audio_path, sr=22050, duration=60)  # Primeros 60 segundos
            
            # Extraer características
            features = self.shazam._extract_audio_features(y, sr)
            
            # Agregar características adicionales para mejor identificación
            # Chroma fingerprint
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            chroma_mean = np.mean(chroma, axis=1).tolist()
            
            # Spectral features
            spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr), axis=1).tolist()
            
            # Tonnetz
            tonnetz = np.mean(librosa.feature.tonnetz(y=y, sr=sr), axis=1).tolist()
            
            features.update({
                'chroma_fingerprint': chroma_mean,
                'spectral_contrast': spectral_contrast,
                'tonnetz': tonnetz,
                'duration': len(y) / sr
            })
            
            return features
            
        except Exception as e:
            print(f"Error extrayendo características: {e}")
            return None
    
    def remove_song(self, song_id):
        """Eliminar canción de la base de datos"""
        try:
            if song_id not in self.database:
                print(f"❌ Canción no encontrada: {song_id}")
                return False
            
            song = self.database[song_id]
            
            # Eliminar archivo de audio
            if os.path.exists(song['file_path']):
                os.remove(song['file_path'])
            
            # Eliminar de base de datos
            del self.database[song_id]
            self.save_database()
            
            print(f"✅ Canción eliminada: {song['title']} - {song['artist']}")
            return True
            
        except Exception as e:
            print(f"❌ Error eliminando canción: {e}")
            return False
    
    def list_songs(self):
        """Listar todas las canciones en la base de datos"""
        if not self.database:
            print("📭 Base de datos vacía")
            return
        
        print(f"🎵 CANCIONES EN BASE DE DATOS ({len(self.database)} canciones)")
        print("=" * 60)
        
        for song_id, song in self.database.items():
            print(f"ID: {song_id}")
            print(f"  🎵 {song['title']} - {song['artist']}")
            if song['album']:
                print(f"  💿 Álbum: {song['album']}")
            print(f"  📅 Agregado: {song['added_date']}")
            print(f"  📁 Archivo: {song['file_path']}")
            print()
    
    def search_songs(self, query):
        """Buscar canciones por título o artista"""
        query = query.lower()
        results = []
        
        for song_id, song in self.database.items():
            if (query in song['title'].lower() or 
                query in song['artist'].lower() or 
                query in song.get('album', '').lower()):
                results.append((song_id, song))
        
        if results:
            print(f"🔍 RESULTADOS DE BÚSQUEDA: '{query}' ({len(results)} encontradas)")
            print("=" * 60)
            for song_id, song in results:
                print(f"  🎵 {song['title']} - {song['artist']}")
                if song['album']:
                    print(f"     💿 {song['album']}")
        else:
            print(f"❌ No se encontraron canciones con: '{query}'")
    
    def get_current_date(self):
        """Obtener fecha actual"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def export_database(self, export_path):
        """Exportar base de datos a archivo"""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.database, f, indent=2, ensure_ascii=False)
            print(f"✅ Base de datos exportada a: {export_path}")
        except Exception as e:
            print(f"❌ Error exportando: {e}")
    
    def import_database(self, import_path):
        """Importar base de datos desde archivo"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_db = json.load(f)
            
            # Fusionar con base de datos actual
            self.database.update(imported_db)
            self.save_database()
            
            print(f"✅ Base de datos importada desde: {import_path}")
            print(f"   Total de canciones: {len(self.database)}")
        except Exception as e:
            print(f"❌ Error importando: {e}")

def main():
    """Interfaz de línea de comandos para gestionar la base de datos"""
    manager = SongDatabaseManager()
    
    while True:
        print("\n" + "=" * 60)
        print("🎵 GESTOR DE BASE DE DATOS DE CANCIONES")
        print("=" * 60)
        print("1. Agregar canción desde archivo")
        print("2. Listar todas las canciones")
        print("3. Buscar canciones")
        print("4. Eliminar canción")
        print("5. Exportar base de datos")
        print("6. Importar base de datos")
        print("7. Agregar múltiples canciones desde carpeta")
        print("0. Salir")
        print()
        
        try:
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '0':
                print("👋 ¡Hasta luego!")
                break
            
            elif choice == '1':
                audio_path = input("Ruta del archivo de audio: ").strip()
                if audio_path:
                    manager.add_song_from_file(audio_path)
            
            elif choice == '2':
                manager.list_songs()
            
            elif choice == '3':
                query = input("Buscar (título/artista/álbum): ").strip()
                if query:
                    manager.search_songs(query)
            
            elif choice == '4':
                manager.list_songs()
                song_id = input("ID de canción a eliminar: ").strip()
                if song_id:
                    manager.remove_song(song_id)
            
            elif choice == '5':
                export_path = input("Ruta para exportar (ej: backup.json): ").strip()
                if export_path:
                    manager.export_database(export_path)
            
            elif choice == '6':
                import_path = input("Ruta del archivo a importar: ").strip()
                if import_path:
                    manager.import_database(import_path)
            
            elif choice == '7':
                folder_path = input("Ruta de la carpeta con archivos de audio: ").strip()
                if folder_path and os.path.exists(folder_path):
                    add_songs_from_folder(manager, folder_path)
            
            else:
                print("❌ Opción no válida")
        
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def add_songs_from_folder(manager, folder_path):
    """Agregar múltiples canciones desde una carpeta"""
    audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
    
    audio_files = []
    for file in os.listdir(folder_path):
        if any(file.lower().endswith(ext) for ext in audio_extensions):
            audio_files.append(os.path.join(folder_path, file))
    
    if not audio_files:
        print("❌ No se encontraron archivos de audio en la carpeta")
        return
    
    print(f"📁 Encontrados {len(audio_files)} archivos de audio")
    
    for audio_file in audio_files:
        print(f"\n🎵 Procesando: {os.path.basename(audio_file)}")
        
        # Intentar extraer información del nombre del archivo
        filename = os.path.splitext(os.path.basename(audio_file))[0]
        
        # Formato común: "Artista - Título"
        if ' - ' in filename:
            parts = filename.split(' - ', 1)
            suggested_artist = parts[0].strip()
            suggested_title = parts[1].strip()
        else:
            suggested_artist = ""
            suggested_title = filename
        
        print(f"Sugerencias basadas en nombre de archivo:")
        print(f"  Artista: {suggested_artist}")
        print(f"  Título: {suggested_title}")
        
        title = input(f"Título [{suggested_title}]: ").strip() or suggested_title
        artist = input(f"Artista [{suggested_artist}]: ").strip() or suggested_artist
        album = input("Álbum (opcional): ").strip()
        
        if title and artist:
            manager.add_song_from_file(audio_file, title, artist, album)
        else:
            print("⏭️  Saltando archivo (título y artista requeridos)")

if __name__ == "__main__":
    main()