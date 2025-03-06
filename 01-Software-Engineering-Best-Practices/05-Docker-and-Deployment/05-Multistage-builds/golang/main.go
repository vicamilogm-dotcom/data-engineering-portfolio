package main

import "github.com/gin-gonic/gin"

func main() {
	r := gin.Default()
	r.SetTrustedProxies(nil)
	r.GET("/", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"App": "Running",
		})
	})
	r.Run()
}
