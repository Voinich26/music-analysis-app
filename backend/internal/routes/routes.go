package routes

import (
	"github.com/gin-gonic/gin"
	"music-analysis/internal/controllers"
)

// SetupRoutes configura todas las rutas de la aplicación
func SetupRoutes(r *gin.Engine, audioController *controllers.AudioController, healthController *controllers.HealthController) {
	// Grupo de rutas API
	api := r.Group("/api")
	{
		// Rutas de audio
		audio := api.Group("/audio")
		{
			audio.POST("/upload", audioController.UploadAudio)
			audio.GET("/:id", audioController.GetAnalysis)
			audio.GET("/:id/export", audioController.ExportAnalysis)
			audio.POST("/identify", audioController.IdentifySong)
			audio.POST("/youtube-download", audioController.DownloadFromYouTube)
		}

		// Ruta de salud del servidor
		api.GET("/health", healthController.HealthCheck)
	}

	// Servir archivos estáticos del frontend
	r.Static("/static", "./frontend")
	r.StaticFile("/", "./frontend/index.html")
}
