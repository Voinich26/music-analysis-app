package services

import (
	"fmt"
	"io"
	"mime/multipart"
	"os"
	"path/filepath"
	"time"
)

// AudioService maneja operaciones relacionadas con archivos de audio
type AudioService struct {
	tempDir string
}

// NewAudioService crea una nueva instancia del servicio de audio
func NewAudioService() *AudioService {
	// Crear directorio temporal si no existe
	tempDir := "./temp_audio"
	if err := os.MkdirAll(tempDir, 0755); err != nil {
		panic(fmt.Sprintf("No se pudo crear directorio temporal: %v", err))
	}

	return &AudioService{
		tempDir: tempDir,
	}
}

// SaveTemporaryFile guarda un archivo de audio temporalmente
func (as *AudioService) SaveTemporaryFile(file *multipart.FileHeader) (string, error) {
	// Generar nombre único para el archivo
	timestamp := time.Now().UnixNano()
	filename := fmt.Sprintf("audio_%d%s", timestamp, filepath.Ext(file.Filename))
	filePath := filepath.Join(as.tempDir, filename)

	// Abrir archivo de destino
	dst, err := os.Create(filePath)
	if err != nil {
		return "", fmt.Errorf("error al crear archivo temporal: %v", err)
	}
	defer dst.Close()

	// Abrir archivo fuente
	src, err := file.Open()
	if err != nil {
		return "", fmt.Errorf("error al abrir archivo fuente: %v", err)
	}
	defer src.Close()

	// Copiar contenido
	if _, err := io.Copy(dst, src); err != nil {
		return "", fmt.Errorf("error al copiar archivo: %v", err)
	}

	return filePath, nil
}

// CleanupTemporaryFile elimina un archivo temporal
func (as *AudioService) CleanupTemporaryFile(filepath string) error {
	if err := os.Remove(filepath); err != nil {
		return fmt.Errorf("error al eliminar archivo temporal: %v", err)
	}
	return nil
}

// GetTempDir retorna el directorio temporal
func (as *AudioService) GetTempDir() string {
	return as.tempDir
}
