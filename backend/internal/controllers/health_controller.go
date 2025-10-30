package controllers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// HealthController maneja las peticiones de salud del servidor
type HealthController struct{}

// NewHealthController crea una nueva instancia del controlador de salud
func NewHealthController() *HealthController {
	return &HealthController{}
}

// HealthCheck verifica el estado del servidor
func (hc *HealthController) HealthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "ok",
		"message": "Music Analysis API está funcionando correctamente",
		"version": "1.0.0",
	})
}

