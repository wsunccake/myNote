# quick start

```bash
linux:~ $ mkdir project
linux:~ $ cd $_
linux:~/project $ go mod init project
linux:~/project $ go mod tidy
linux:~/project $ go install github.com/gin-gonic/gin@latest
linux:~/project $ cat << EOF > main.go
package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})
	r.Run()
}
EOF

linux:~/project $ go run main.go

# test
linux:~ $ curl http://localhost:8080/ping
```
