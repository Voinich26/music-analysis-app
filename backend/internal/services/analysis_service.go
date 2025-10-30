package services

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"sync"
	"time"
)

// AnalysisService maneja el procesamiento y análisis de audio
type AnalysisService struct {
	results map[int]*AnalysisResult
	nextID  int
	mutex   sync.RWMutex
}

// AnalysisResult representa el resultado de un análisis de audio
type AnalysisResult struct {
	ID                    int                    `json:"id"`
	Key                   string                 `json:"key"`
	KeyConfidence         float64                `json:"key_confidence"`
	BPM                   float64                `json:"bpm"`
	TempoClassification   string                 `json:"tempo_classification"`
	Progression           []string               `json:"progression"`
	Timeline              []TimelineEntry        `json:"timeline"`
	Notes                 []string               `json:"notes"`
	Lyrics                string                 `json:"lyrics,omitempty"`
	Duration              float64                `json:"duration"`
	ChordCount            int                    `json:"chord_count"`
	AvgChordConfidence    float64                `json:"average_chord_confidence"`
	SongIdentification    *SongIdentification    `json:"song_identification,omitempty"`
	HarmonicAnalysis      *HarmonicAnalysis      `json:"harmonic_analysis,omitempty"`
	CreatedAt             time.Time              `json:"created_at"`
	Status                string                 `json:"status"` // "processing", "completed", "error"
	Error                 string                 `json:"error,omitempty"`
}

// SongIdentification representa información de identificación de la canción
type SongIdentification struct {
	Identified      bool                   `json:"identified"`
	Confidence      float64                `json:"confidence"`
	Characteristics map[string]interface{} `json:"characteristics"`
}

// HarmonicAnalysis representa el análisis armónico avanzado
type HarmonicAnalysis struct {
	TotalChords        int      `json:"total_chords"`
	UniqueChords       int      `json:"unique_chords"`
	ChordVariety       float64  `json:"chord_variety"`
	DetectedPatterns   []string `json:"detected_patterns"`
	MostCommonChord    string   `json:"most_common_chord"`
	HarmonicRhythm     string   `json:"harmonic_rhythm"`
}

// TimelineEntry representa una entrada en la línea de tiempo
type TimelineEntry struct {
	Time       string  `json:"time"`
	Chord      string  `json:"chord"`
	Confidence float64 `json:"confidence,omitempty"`
}

// NewAnalysisService crea una nueva instancia del servicio de análisis
func NewAnalysisService() *AnalysisService {
	return &AnalysisService{
		results: make(map[int]*AnalysisResult),
		nextID:  1,
	}
}

// ProcessAudio procesa un archivo de audio usando Python
func (as *AnalysisService) ProcessAudio(audioPath string) (int, error) {
	as.mutex.Lock()
	id := as.nextID
	as.nextID++

	// Crear resultado inicial
	result := &AnalysisResult{
		ID:        id,
		Status:    "processing",
		CreatedAt: time.Now(),
	}
	as.results[id] = result
	as.mutex.Unlock()

	// Procesar en una goroutine para no bloquear
	go as.processAudioAsync(id, audioPath)

	return id, nil
}

// processAudioAsync procesa el audio de forma asíncrona
func (as *AnalysisService) processAudioAsync(id int, audioPath string) {
	as.mutex.Lock()
	result := as.results[id]
	as.mutex.Unlock()

	// Usar el script DEFINITIVO y ROBUSTO
	scriptPath := filepath.Join("..", "python_audio", "analyze_audio_ultimate.py")
	
	// Verificar que el script existe
	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		as.mutex.Lock()
		result.Status = "error"
		result.Error = fmt.Sprintf("Script de análisis no encontrado: %s", scriptPath)
		as.mutex.Unlock()
		return
	}
	
	// Usar directamente el Python del entorno virtual
	venvPythonPath := filepath.Join("..", "python_audio", "venv", "Scripts", "python.exe")
	
	// Verificar que Python existe
	if _, err := os.Stat(venvPythonPath); os.IsNotExist(err) {
		as.mutex.Lock()
		result.Status = "error"
		result.Error = fmt.Sprintf("Python del entorno virtual no encontrado: %s", venvPythonPath)
		as.mutex.Unlock()
		return
	}
	
	// Convertir audioPath a ruta absoluta
	absAudioPath, err := filepath.Abs(audioPath)
	if err != nil {
		as.mutex.Lock()
		result.Status = "error"
		result.Error = fmt.Sprintf("Error al obtener ruta absoluta: %v", err)
		as.mutex.Unlock()
		return
	}
	
	// Ejecutar comando con ruta absoluta
	cmd := exec.Command(venvPythonPath, scriptPath, absAudioPath)
	cmd.Dir = filepath.Join("..", "python_audio")  // Establecer directorio de trabajo
	
	output, err := cmd.Output()
	if err != nil {
		// Capturar stderr también
		// Limpiar archivo temporal en caso de error
		os.Remove(audioPath)
		
		if exitError, ok := err.(*exec.ExitError); ok {
			stderr := string(exitError.Stderr)
			as.mutex.Lock()
			result.Status = "error"
			result.Error = fmt.Sprintf("Error en script Python: %s. Stderr: %s", string(output), stderr)
			as.mutex.Unlock()
			return
		} else {
			as.mutex.Lock()
			result.Status = "error"
			result.Error = fmt.Sprintf("Error al ejecutar comando: %v. Output: %s", err, string(output))
			as.mutex.Unlock()
			return
		}
	}

	// Parsear resultado JSON avanzado
	var analysisData struct {
		Key                   string                 `json:"key"`
		KeyConfidence         float64                `json:"key_confidence"`
		BPM                   float64                `json:"bpm"`
		TempoClassification   string                 `json:"tempo_classification"`
		Progression           []string               `json:"progression"`
		Timeline              []TimelineEntry        `json:"timeline"`
		Notes                 []string               `json:"notes"`
		Lyrics                string                 `json:"lyrics,omitempty"`
		Duration              float64                `json:"duration"`
		ChordCount            int                    `json:"chord_count"`
		AvgChordConfidence    float64                `json:"average_chord_confidence"`
		SongIdentification    *SongIdentification    `json:"song_identification,omitempty"`
		HarmonicAnalysis      map[string]interface{} `json:"harmonic_analysis,omitempty"`
		Error                 string                 `json:"error,omitempty"`
	}

	if err := json.Unmarshal(output, &analysisData); err != nil {
		as.mutex.Lock()
		result.Status = "error"
		result.Error = fmt.Sprintf("Error al parsear resultado: %v", err)
		as.mutex.Unlock()
		return
	}

	// Verificar si hubo error en el análisis
	if analysisData.Error != "" {
		as.mutex.Lock()
		result.Status = "error"
		result.Error = analysisData.Error
		as.mutex.Unlock()
		return
	}

	// Convertir análisis armónico
	var harmonicAnalysis *HarmonicAnalysis
	if analysisData.HarmonicAnalysis != nil {
		harmonicAnalysis = &HarmonicAnalysis{}
		if val, ok := analysisData.HarmonicAnalysis["total_chords"].(float64); ok {
			harmonicAnalysis.TotalChords = int(val)
		}
		if val, ok := analysisData.HarmonicAnalysis["unique_chords"].(float64); ok {
			harmonicAnalysis.UniqueChords = int(val)
		}
		if val, ok := analysisData.HarmonicAnalysis["chord_variety"].(float64); ok {
			harmonicAnalysis.ChordVariety = val
		}
		if val, ok := analysisData.HarmonicAnalysis["most_common_chord"].(string); ok {
			harmonicAnalysis.MostCommonChord = val
		}
		if val, ok := analysisData.HarmonicAnalysis["harmonic_rhythm"].(string); ok {
			harmonicAnalysis.HarmonicRhythm = val
		}
		if val, ok := analysisData.HarmonicAnalysis["detected_patterns"].([]interface{}); ok {
			patterns := make([]string, len(val))
			for i, p := range val {
				if str, ok := p.(string); ok {
					patterns[i] = str
				}
			}
			harmonicAnalysis.DetectedPatterns = patterns
		}
	}

	// Actualizar resultado
	as.mutex.Lock()
	result.Key = analysisData.Key
	result.KeyConfidence = analysisData.KeyConfidence
	result.BPM = analysisData.BPM
	result.TempoClassification = analysisData.TempoClassification
	result.Progression = analysisData.Progression
	result.Timeline = analysisData.Timeline
	result.Notes = analysisData.Notes
	result.Lyrics = analysisData.Lyrics
	result.Duration = analysisData.Duration
	result.ChordCount = analysisData.ChordCount
	result.AvgChordConfidence = analysisData.AvgChordConfidence
	result.SongIdentification = analysisData.SongIdentification
	result.HarmonicAnalysis = harmonicAnalysis
	result.Status = "completed"
	as.mutex.Unlock()
	
	// Limpiar archivo temporal después del análisis exitoso
	if err := os.Remove(audioPath); err != nil {
		// Log error but don't fail the analysis
		fmt.Printf("Warning: Could not remove temporary file %s: %v\n", audioPath, err)
	}
}

// GetAnalysisResults obtiene los resultados de un análisis
func (as *AnalysisService) GetAnalysisResults(id int) (*AnalysisResult, error) {
	as.mutex.RLock()
	result, exists := as.results[id]
	as.mutex.RUnlock()

	if !exists {
		return nil, fmt.Errorf("análisis con ID %d no encontrado", id)
	}

	return result, nil
}

// GetAllAnalyses obtiene todos los análisis realizados
func (as *AnalysisService) GetAllAnalyses() []*AnalysisResult {
	as.mutex.RLock()
	defer as.mutex.RUnlock()

	results := make([]*AnalysisResult, 0, len(as.results))
	for _, result := range as.results {
		results = append(results, result)
	}

	return results
}

// ExportAnalysis exporta un análisis en diferentes formatos
func (as *AnalysisService) ExportAnalysis(id int, format string) ([]byte, string, error) {
	result, err := as.GetAnalysisResults(id)
	if err != nil {
		return nil, "", err
	}

	switch format {
	case "json":
		data, err := json.MarshalIndent(result, "", "  ")
		return data, "application/json", err
	case "txt":
		content := as.formatAsText(result)
		return []byte(content), "text/plain", nil
	case "pdf":
		// Implementar generación de PDF
		return nil, "", fmt.Errorf("exportación PDF no implementada aún")
	default:
		return nil, "", fmt.Errorf("formato no soportado: %s", format)
	}
}

// formatAsText formatea el resultado como texto
func (as *AnalysisService) formatAsText(result *AnalysisResult) string {
	content := fmt.Sprintf("🎵 ANÁLISIS MUSICAL AVANZADO\n")
	content += fmt.Sprintf("============================\n\n")
	content += fmt.Sprintf("ID: %d\n", result.ID)
	content += fmt.Sprintf("Fecha: %s\n", result.CreatedAt.Format("2006-01-02 15:04:05"))
	content += fmt.Sprintf("Estado: %s\n\n", result.Status)

	if result.Status == "completed" {
		// Información básica
		content += fmt.Sprintf("📊 INFORMACIÓN BÁSICA\n")
		content += fmt.Sprintf("Tonalidad: %s (Confianza: %.2f)\n", result.Key, result.KeyConfidence)
		content += fmt.Sprintf("BPM: %.1f (%s)\n", result.BPM, result.TempoClassification)
		content += fmt.Sprintf("Duración: %.2f segundos\n\n", result.Duration)

		// Identificación de canción
		if result.SongIdentification != nil {
			content += fmt.Sprintf("🎵 IDENTIFICACIÓN\n")
			if result.SongIdentification.Identified {
				content += fmt.Sprintf("Canción identificada (Confianza: %.2f)\n", result.SongIdentification.Confidence)
			} else {
				content += fmt.Sprintf("Canción no identificada en base de datos\n")
			}
			
			if chars, ok := result.SongIdentification.Characteristics["energy_level"].(string); ok {
				content += fmt.Sprintf("Nivel de energía: %s\n", chars)
			}
			if hints, ok := result.SongIdentification.Characteristics["genre_hints"].([]interface{}); ok && len(hints) > 0 {
				content += fmt.Sprintf("Pistas de género: ")
				for i, hint := range hints {
					if str, ok := hint.(string); ok {
						if i > 0 {
							content += ", "
						}
						content += str
					}
				}
				content += "\n"
			}
			content += "\n"
		}

		// Progresión armónica
		content += fmt.Sprintf("🎼 PROGRESIÓN ARMÓNICA\n")
		content += fmt.Sprintf("Acordes: %s\n", fmt.Sprintf("%v", result.Progression))
		content += fmt.Sprintf("Total de acordes detectados: %d\n", result.ChordCount)
		content += fmt.Sprintf("Confianza promedio: %.2f\n\n", result.AvgChordConfidence)

		// Análisis armónico
		if result.HarmonicAnalysis != nil {
			content += fmt.Sprintf("🔍 ANÁLISIS ARMÓNICO\n")
			content += fmt.Sprintf("Acordes únicos: %d\n", result.HarmonicAnalysis.UniqueChords)
			content += fmt.Sprintf("Variedad armónica: %.2f\n", result.HarmonicAnalysis.ChordVariety)
			content += fmt.Sprintf("Acorde más común: %s\n", result.HarmonicAnalysis.MostCommonChord)
			content += fmt.Sprintf("Ritmo armónico: %s\n", result.HarmonicAnalysis.HarmonicRhythm)
			
			if len(result.HarmonicAnalysis.DetectedPatterns) > 0 {
				content += fmt.Sprintf("Patrones detectados: %s\n", fmt.Sprintf("%v", result.HarmonicAnalysis.DetectedPatterns))
			}
			content += "\n"
		}

		// Línea de tiempo
		content += fmt.Sprintf("⏱️ LÍNEA DE TIEMPO\n")
		for _, entry := range result.Timeline {
			if entry.Confidence > 0 {
				content += fmt.Sprintf("  %s - %s (Confianza: %.2f)\n", entry.Time, entry.Chord, entry.Confidence)
			} else {
				content += fmt.Sprintf("  %s - %s\n", entry.Time, entry.Chord)
			}
		}

		// Notas principales
		content += fmt.Sprintf("\n🎹 NOTAS PRINCIPALES\n")
		content += fmt.Sprintf("Notas: %s\n", fmt.Sprintf("%v", result.Notes))

		// Letra
		if result.Lyrics != "" {
			content += fmt.Sprintf("\n🎤 LETRA\n")
			content += fmt.Sprintf("%s\n", result.Lyrics)
		}
	} else if result.Status == "error" {
		content += fmt.Sprintf("❌ Error: %s\n", result.Error)
	}

	return content
}

// IdentifySongWithShazam identifica una canción usando el módulo Shazam
func (as *AnalysisService) IdentifySongWithShazam(audioPath string) (map[string]interface{}, error) {
	// Usar el script de integración Shazam
	scriptPath := filepath.Join("..", "python_audio", "shazam_integration.py")
	
	// Verificar que el script existe
	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("script de Shazam no encontrado: %s", scriptPath)
	}
	
	// Usar Python del entorno virtual
	venvPythonPath := filepath.Join("..", "python_audio", "venv", "Scripts", "python.exe")
	
	// Verificar que Python existe
	if _, err := os.Stat(venvPythonPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("Python del entorno virtual no encontrado: %s", venvPythonPath)
	}
	
	// Convertir audioPath a ruta absoluta
	absAudioPath, err := filepath.Abs(audioPath)
	if err != nil {
		return nil, fmt.Errorf("error al obtener ruta absoluta: %v", err)
	}
	
	// Ejecutar comando Python para identificación
	cmd := exec.Command(venvPythonPath, "-c", fmt.Sprintf(`
import sys
sys.path.append('.')
from shazam_integration import identify_and_enrich_song
import json

result = identify_and_enrich_song('%s')
print(json.dumps(result, ensure_ascii=False))
`, absAudioPath))
	
	cmd.Dir = filepath.Join("..", "python_audio")
	
	output, err := cmd.Output()
	if err != nil {
		if exitError, ok := err.(*exec.ExitError); ok {
			stderr := string(exitError.Stderr)
			return nil, fmt.Errorf("error en identificación Shazam: %s. Stderr: %s", string(output), stderr)
		}
		return nil, fmt.Errorf("error al ejecutar identificación: %v", err)
	}
	
	// Parsear resultado JSON
	var result map[string]interface{}
	if err := json.Unmarshal(output, &result); err != nil {
		return nil, fmt.Errorf("error al parsear resultado de identificación: %v", err)
	}
	
	return result, nil
}

// DownloadFromYouTube descarga audio desde YouTube
func (as *AnalysisService) DownloadFromYouTube(youtubeURL, format string) (map[string]interface{}, error) {
	// Usar el script de integración Shazam para descarga de YouTube
	scriptPath := filepath.Join("..", "python_audio", "shazam_integration.py")
	
	// Verificar que el script existe
	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("script de descarga no encontrado: %s", scriptPath)
	}
	
	// Usar Python del entorno virtual
	venvPythonPath := filepath.Join("..", "python_audio", "venv", "Scripts", "python.exe")
	
	// Verificar que Python existe
	if _, err := os.Stat(venvPythonPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("Python del entorno virtual no encontrado: %s", venvPythonPath)
	}
	
	// Ejecutar comando Python para descarga
	cmd := exec.Command(venvPythonPath, "youtube_downloader_complete.py", youtubeURL, format)
	
	cmd.Dir = filepath.Join("..", "python_audio")
	
	output, err := cmd.Output()
	if err != nil {
		if exitError, ok := err.(*exec.ExitError); ok {
			stderr := string(exitError.Stderr)
			return nil, fmt.Errorf("error en descarga YouTube: %s. Stderr: %s", string(output), stderr)
		}
		return nil, fmt.Errorf("error al ejecutar descarga: %v", err)
	}
	
	// Parsear resultado JSON
	var result map[string]interface{}
	if err := json.Unmarshal(output, &result); err != nil {
		return nil, fmt.Errorf("error al parsear resultado de descarga: %v", err)
	}
	
	return result, nil
}
