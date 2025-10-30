#!/usr/bin/env python3
"""
DETECCIÓN AVANZADA DE ACORDES - ALGORITMO MODERNO
Usa múltiples técnicas para detectar acordes en TODA la canción
"""

import librosa
import numpy as np
from scipy import signal
import json

class AdvancedChordDetector:
    def __init__(self):
        self.chord_templates = self._create_chord_templates()
        
    def _create_chord_templates(self):
        """Crear plantillas de acordes más precisas"""
        templates = {}
        
        # Acordes mayores
        major_chords = {
            'C': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            'C#': [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            'D': [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            'D#': [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            'E': [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            'F': [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            'F#': [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            'G': [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            'G#': [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
            'A': [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            'A#': [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            'B': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        }
        
        # Acordes menores
        minor_chords = {
            'Cm': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            'C#m': [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            'Dm': [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            'D#m': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
            'Em': [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
            'Fm': [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            'F#m': [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            'Gm': [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
            'G#m': [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
            'Am': [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            'A#m': [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            'Bm': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        }
        
        templates.update(major_chords)
        templates.update(minor_chords)
        
        return templates
    
    def detect_chords_complete(self, y, sr):
        """Detectar acordes en TODA la canción con máxima precisión"""
        try:
            total_duration = len(y) / sr
            
            # Usar segmentos muy pequeños para máximo detalle
            segment_duration = 1.0  # 1 segundo por segmento
            hop_length = int(0.5 * sr)  # Overlap de 50%
            
            # Calcular número total de segmentos
            total_segments = int((len(y) - sr) / hop_length) + 1
            
            chords = []
            
            print(f"Analizando {total_segments} segmentos de {segment_duration}s cada uno...")
            
            for i in range(total_segments):
                start_sample = i * hop_length
                end_sample = min(start_sample + int(segment_duration * sr), len(y))
                
                if end_sample - start_sample < sr * 0.5:  # Al menos 0.5 segundos
                    break
                    
                segment = y[start_sample:end_sample]
                time_seconds = start_sample / sr
                
                # Detectar acorde en este segmento
                chord, confidence = self._detect_chord_in_segment(segment, sr)
                
                chords.append({
                    'chord': chord,
                    'time': time_seconds,
                    'confidence': confidence
                })
                
                if i % 10 == 0:  # Progress update
                    print(f"Procesado: {i}/{total_segments} segmentos")
            
            # Filtrar acordes repetidos consecutivos pero mantener cambios
            filtered_chords = self._filter_consecutive_chords(chords)
            
            print(f"Acordes detectados: {len(filtered_chords)}")
            return filtered_chords
            
        except Exception as e:
            print(f"Error en detección avanzada: {e}")
            return [{'chord': 'C', 'time': 0, 'confidence': 0.0}]
    
    def _detect_chord_in_segment(self, segment, sr):
        """Detectar acorde en un segmento específico"""
        try:
            # Extraer chroma con ventana más pequeña
            chroma = librosa.feature.chroma_stft(
                y=segment, 
                sr=sr, 
                hop_length=256,
                n_fft=2048
            )
            
            # Promedio del chroma
            chroma_mean = np.mean(chroma, axis=1)
            
            # Normalizar
            if np.sum(chroma_mean) > 0:
                chroma_norm = chroma_mean / np.sum(chroma_mean)
            else:
                return 'N', 0.0
            
            # Encontrar mejor coincidencia
            best_chord = 'N'
            best_score = 0.0
            
            for chord_name, template in self.chord_templates.items():
                template_norm = np.array(template) / np.sum(template)
                
                # Correlación coseno
                correlation = np.dot(chroma_norm, template_norm) / (
                    np.linalg.norm(chroma_norm) * np.linalg.norm(template_norm)
                )
                
                if correlation > best_score:
                    best_score = correlation
                    best_chord = chord_name
            
            # Solo devolver acordes con confianza mínima
            if best_score < 0.3:
                return 'N', best_score
                
            return best_chord, best_score
            
        except Exception as e:
            return 'N', 0.0
    
    def _filter_consecutive_chords(self, chords):
        """Filtrar acordes consecutivos pero mantener cambios importantes"""
        if not chords:
            return []
        
        filtered = [chords[0]]
        
        for i in range(1, len(chords)):
            current = chords[i]
            previous = filtered[-1]
            
            # Mantener si:
            # 1. Es diferente al anterior
            # 2. O si ha pasado suficiente tiempo (cada 4 segundos mínimo)
            # 3. O si la confianza es significativamente mayor
            
            time_diff = current['time'] - previous['time']
            confidence_diff = current['confidence'] - previous['confidence']
            
            if (current['chord'] != previous['chord'] or 
                time_diff >= 4.0 or 
                confidence_diff > 0.2):
                filtered.append(current)
        
        return filtered

def analyze_with_advanced_detection(audio_path):
    """Función principal para análisis avanzado"""
    try:
        detector = AdvancedChordDetector()
        
        # Cargar audio
        y, sr = librosa.load(audio_path, sr=22050)
        duration = len(y) / sr
        
        print(f"Analizando archivo: {audio_path}")
        print(f"Duración: {duration:.2f} segundos")
        
        # Detectar acordes
        chords = detector.detect_chords_complete(y, sr)
        
        # Crear timeline formateado
        timeline = []
        for chord_data in chords:
            time_seconds = chord_data['time']
            minutes = int(time_seconds // 60)
            seconds = int(time_seconds % 60)
            time_formatted = f"{minutes:02d}:{seconds:02d}"
            
            timeline.append({
                'time': time_formatted,
                'chord': chord_data['chord'],
                'confidence': chord_data['confidence']
            })
        
        return {
            'timeline': timeline,
            'total_chords': len(timeline),
            'duration': duration,
            'analysis_type': 'advanced'
        }
        
    except Exception as e:
        print(f"Error en análisis avanzado: {e}")
        return {
            'timeline': [{'time': '00:00', 'chord': 'C', 'confidence': 0.0}],
            'total_chords': 1,
            'duration': 0,
            'analysis_type': 'error'
        }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = analyze_with_advanced_detection(sys.argv[1])
        print(json.dumps(result, indent=2))