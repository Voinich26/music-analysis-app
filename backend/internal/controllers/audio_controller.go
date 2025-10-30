package controllers

import (
	"fmt"
	"net/http"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
	"music-analysis/internal/services"
)

// AudioController maneja las peticiones relacionadas con audio
type AudioController struct {
	audioService    *services.AudioService
	analysisService *services.AnalysisService
}

// NewAudioController crea una nueva instancia del controlador de audio
func NewAudioController(audioService *services.AudioService, analysisService *services.AnalysisService) *AudioController {
	return &AudioController{
		audioService:    audioService,
		analysisService: analysisService,
	}
}

// UploadAudio maneja la subida de archivos de audio
func (ac *AudioController) UploadAudio(c *gin.Context) {
	// Obtener el archivo del formulario
	file, err := c.FormFile("audio")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "No se pudo obtener el archivo de audio",
			"details": err.Error(),
		})
		return
	}

	// Validar el tipo de archivo
	if !ac.isValidAudioFile(file.Filename) {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Formato de archivo no soportado. Use MP3 o WAV",
		})
		return
	}

	// Guardar el archivo temporalmente
	savedPath, err := ac.audioService.SaveTemporaryFile(file)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Error al guardar el archivo",
			"details": err.Error(),
		})
		return
	}

	// Procesar el audio usando Python (no eliminar archivo aún)
	analysisID, err := ac.analysisService.ProcessAudio(savedPath)
	if err != nil {
		// Si hay error, limpiar archivo
		ac.audioService.CleanupTemporaryFile(savedPath)
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Error al procesar el audio",
			"details": err.Error(),
		})
		return
	}

	// NO limpiar archivo temporal aquí - se limpiará después del análisis

	c.JSON(http.StatusOK, gin.H{
		"message": "Audio procesado exitosamente",
		"analysis_id": analysisID,
	})
}

// GetAnalysis obtiene los resultados de un análisis
func (ac *AudioController) GetAnalysis(c *gin.Context) {
	analysisID := c.Param("id")
	if analysisID == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "ID de análisis requerido",
		})
		return
	}

	// Convertir ID a entero
	id, err := strconv.Atoi(analysisID)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "ID de análisis inválido",
		})
		return
	}

	// Obtener resultados del análisis
	results, err := ac.analysisService.GetAnalysisResults(id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "Análisis no encontrado",
			"details": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, results)
}

// ExportAnalysis exporta los resultados de un análisis
func (ac *AudioController) ExportAnalysis(c *gin.Context) {
	analysisID := c.Param("id")
	format := c.DefaultQuery("format", "json")
	
	if analysisID == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "ID de análisis requerido",
		})
		return
	}

	// Convertir ID a entero
	id, err := strconv.Atoi(analysisID)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "ID de análisis inválido",
		})
		return
	}

	// Exportar resultados
	data, contentType, err := ac.analysisService.ExportAnalysis(id, format)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "Error al exportar análisis",
			"details": err.Error(),
		})
		return
	}

	// Configurar headers para descarga
	filename := fmt.Sprintf("music_analysis_%d.%s", id, format)
	c.Header("Content-Disposition", fmt.Sprintf("attachment; filename=%s", filename))
	c.Header("Content-Type", contentType)
	c.Data(http.StatusOK, contentType, data)
}

// isValidAudioFile valida si el archivo es un formato de audio soportado
func (ac *AudioController) isValidAudioFile(filename string) bool {
	// Obtener la extensión del archivo
	ext := strings.ToLower(filepath.Ext(filename))
	
	// Verificar si es un formato soportado
	supportedFormats := []string{".mp3", ".wav", ".m4a", ".flac", ".webm", ".ogg"}
	for _, format := range supportedFormats {
		if ext == format {
			return true
		}
	}
	
	return false
}

// IdentifySong identifica una canción usando funcionalidad tipo Shazam
func (ac *AudioController) IdentifySong(c *gin.Context) {
	// Obtener el archivo del formulario
	file, err := c.FormFile("audio")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "No se pudo obtener el archivo de audio",
			"details": err.Error(),
		})
		return
	}

	// Validar el tipo de archivo
	if !ac.isValidAudioFile(file.Filename) {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Formato de archivo no soportado",
		})
		return
	}

	// Guardar el archivo temporalmente
	savedPath, err := ac.audioService.SaveTemporaryFile(file)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Error al guardar el archivo",
			"details": err.Error(),
		})
		return
	}

	// Identificar la canción usando el nuevo módulo Shazam
	identification, err := ac.analysisService.IdentifySongWithShazam(savedPath)
	if err != nil {
		// Limpiar archivo temporal
		ac.audioService.CleanupTemporaryFile(savedPath)
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Error al identificar la canción",
			"details": err.Error(),
		})
		return
	}

	// Limpiar archivo temporal
	ac.audioService.CleanupTemporaryFile(savedPath)

	c.JSON(http.StatusOK, identification)
}

// DownloadFromYouTube descarga audio desde YouTube
func (ac *AudioController) DownloadFromYouTube(c *gin.Context) {
	var request struct {
		URL    string `json:"url" binding:"required"`
		Format string `json:"format"`
	}

	if err := c.ShouldBindJSON(&request); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "URL de YouTube requerida",
			"details": err.Error(),
		})
		return
	}

	// Formato por defecto
	if request.Format == "" {
		request.Format = "mp3"
	}

	// Descargar desde YouTube
	result, err := ac.analysisService.DownloadFromYouTube(request.URL, request.Format)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Error al descargar desde YouTube",
			"details": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, result)
}
