# quick start

```bash
linux:~ $ mkdir project
linux:~ $ cd $_
linux:~/project $ go mod init project
linux:~/project $ go mod tidy
linux:~/project $ go install github.com/gin-gonic/gin@latest
linux:~/project $ go get github.com/gin-gonic/gin@latest
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

->

```go
package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func pingHandler(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"message": "pong",
	})
}

func main() {
	r := gin.Default()
	r.GET("/ping", pingHandler)
	r.Run()
}
```

---

## query parameter

```go
package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func hiHandler(c *gin.Context) {
	name := c.DefaultQuery("name", "Guest")
	age := c.Query("age")
	c.String(http.StatusOK, "Hi %s, age: %s", name, age)
}

func main() {
	r := gin.Default()
	r.GET("/hi", hiHandler)
	r.Run()
}
```

```bash
linux:~ $ curl http://localhost:8080/hi
linux:~ $ curl 'http://localhost:8080/hi?name=Man'
linux:~ $ curl 'http://localhost:8080/hi?name=Man&age=18'
```

---

## path paramter

```go
package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func helloHandler(c *gin.Context) {
	fmt.Println(c.FullPath())
	name := c.Param("name")
	c.String(http.StatusOK, "Hello %s", name)
}

func hello2Handler(c *gin.Context) {
	name := c.Param("name")
	action := c.Param("action")
	message := name + " is " + action
	c.String(http.StatusOK, message)
}

func main() {
	r := gin.Default()
	r.GET("/hello/:name", helloHandler)
	r.GET("/hello/:name/*action", hello2Handler)
	r.Run()
}
```

```bash
linux:~ $ curl http://localhost:8080/hello
linux:~ $ curl 'http://localhost:8080/hello/Man'
linux:~ $ curl 'http://localhost:8080/hello/Man/send'
```

---

## post form

```go
package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func heyHandler(c *gin.Context) {
	name := c.PostForm("name")
	c.String(http.StatusOK, "Hey %s", name)
}

func main() {
	r := gin.Default()
	r.POST("/hey", heyHandler)
	r.Run()
}
```

```bash
linux:~ $ curl curl -X POST -d name=Man http://localhost:8080/hey
```
