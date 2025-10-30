package main

import (
	"log"
	"os"

	"music-analysis/internal/controllers"
	"music-analysis/internal/routes"
	"music-analysis/internal/services"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	// Configurar Gin
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()

	// Configurar CORS para permitir comunicación con el frontend
	config := cors.DefaultConfig()
	config.AllowOrigins = []string{"*"} // Permitir todos los orígenes para desarrollo
	config.AllowMethods = []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"}
	config.AllowHeaders = []string{"Origin", "Content-Type", "Accept", "Authorization", "X-Requested-With"}
	config.AllowCredentials = true
	r.Use(cors.New(config))

	// Inicializar servicios
	audioService := services.NewAudioService()
	analysisService := services.NewAnalysisService()

	// Inicializar controladores
	audioController := controllers.NewAudioController(audioService, analysisService)
	healthController := controllers.NewHealthController()

	// Configurar rutas
	routes.SetupRoutes(r, audioController, healthController)

	// Obtener puerto del entorno o usar 3001 por defecto
	port := os.Getenv("PORT")
	if port == "" {
		port = "3001"
	}

	log.Printf("🚀 Servidor iniciado en puerto %s", port)
	log.Printf("📡 API disponible en http://localhost:%s", port)
	log.Printf("🎵 Music Analysis Web Application")

	// Iniciar servidor
	if err := r.Run(":" + port); err != nil {
		log.Fatal("Error al iniciar el servidor:", err)
	}
}
