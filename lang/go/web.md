## hello

```go
package main

import (
	"fmt"
	"net/http"
)

func handler(writer http.ResponseWriter, request *http.Request) {
	fmt.Fprint(writer, "Hello Go")
}

func main() {
	http.HandleFunc("/", handler)
	http.ListenAndServe(":8080", nil)
}
```

```bash
linux:~ # curl http://127.0.0.1:8080
```


---

## routing / multiplexer

```go
package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
)

func apiHandler(writer http.ResponseWriter, request *http.Request) {
	fmt.Fprint(writer, "Hello API")
}

func api1Handler(writer http.ResponseWriter, request *http.Request) {
	writer.Write([]byte("Hello API1"))
}

func api2Handler(writer http.ResponseWriter, request *http.Request) {
	io.WriteString(writer, "Hello API2")
}

func main() {
	http.HandleFunc("/", apiHandler)
	http.HandleFunc("/api1", api1Handler)
	http.HandleFunc("/api2/", api2Handler)
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
```

```bash
linux:~ # curl http://127.0.0.1:8080
linux:~ # curl http://127.0.0.1:8080/api1
linux:~ # curl http://127.0.0.1:8080/api1/
linux:~ # curl http://127.0.0.1:8080/api1/abc
linux:~ # curl http://127.0.0.1:8080/api2
linux:~ # curl http://127.0.0.1:8080/api2/
linux:~ # curl http://127.0.0.1:8080/api2/abc
```


### NewServeMux

```go
package main

import (
	"fmt"
	"log"
	"net/http"
)

func apiHandler(writer http.ResponseWriter, request *http.Request) {
	fmt.Fprint(writer, "Hello API")
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/api1", apiHandler)
	mux.HandleFunc("/api2/", apiHandler)

	server := &http.Server{
		Addr: "0.0.0.0:8080",
		Handler: mux,
	}

	if err := server.ListenAndServe(); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
```


---

## static


```bash
linux:~/project # cat main.go
package main

import (
	"fmt"
	"log"
	"net/http"
)


func main() {
	fs := http.FileServer(http.Dir("static"))
	http.Handle("/", fs)
	// http.Handle("/static/", http.StripPrefix("/static/", fs))

	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}

linux:~/project # cat example.html
<!DOCTYPE html>
<html lang="utf-8">
<head>
    <meta charset="UTF-8">
    <title>static page</title>
    <link rel="stylesheet" href="/stylesheets/main.css">
</head>
<body>
    <h1>Hello from a static page</h1>
</body>
</html>

linux:~/project # cat stylesheets/main.css
body {color: #c0392b}

linux:~/project # tree
.
├── static
│   ├── stylesheets
│   │   └── main.css
│   └ exmaple.html
└── main.go

linux:~ # curl http://127.0.0.1:8080
linux:~ # curl http://127.0.0.1:8080/example.html
```

---

## handler

### Handle & HandleFunc

```go
package main

import (
	"fmt"
	"net/http"
)

type HelloHandler struct{}

func (h *HelloHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello")
}

func hi(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hi")
}

func main() {
	// handler structure
	hello := HelloHandler{}
	http.Handle("/hello", &hello)
	
	// handler function
	http.HandleFunc("/hi", hi)

	server := http.Server{
		Addr: "0.0.0.0:8080",
	}
	server.ListenAndServe()
}
```


### chain handler

```go
package main

import (
	"fmt"
	"net/http"
	"reflect"
	"runtime"
)

func hello(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello")
}

func logger(h http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		name := runtime.FuncForPC(reflect.ValueOf(h).Pointer()).Name()
		fmt.Println("Handler function called - " + name)
		h(w, r)
	}
}

func main() {
	http.Handle("/hello", logger(hello))

	server := http.Server{
		Addr: "0.0.0.0:8080",
	}
	server.ListenAndServe()
}
```


---

## request

```go
package main

import (
	"fmt"
	"log"
	"net/http"
	"strings"
)

func handler(writer http.ResponseWriter, request *http.Request) {
	fmt.Fprint(writer, "Hello Go")
	request.ParseForm()
	log.Println("Meothd: ", request.Method)
	log.Println("Form: ", request.Form)
	log.Println("URL.Path: ", request.URL.Path)
	log.Println("URL.Scheme: ", request.URL.Scheme)
	for k, v := range request.Form {
		log.Println("key:", k)
		log.Println("val:", strings.Join(v, ""))
	}
}

func main() {
	http.HandleFunc("/", handler)
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
```

```bash
linux:~ # curl http://127.0.0.1:8080
linux:~ # curl http://127.0.0.1:8080/action?id=12
```


### header & body

```go
package main

import (
	"fmt"
	"log"
	"net/http"
)

func headerHandler(writer http.ResponseWriter, request *http.Request) {
	h := request.Header
	writer.Header().Set("New-Attribute", "test")
	fmt.Fprintln(writer, h)
	fmt.Fprintln(writer, h["Accept"])
	fmt.Fprintln(writer, h.Get("Accept"))
}

func bodyHandler(writer http.ResponseWriter, request *http.Request) {
	len := request.ContentLength
	body := make([]byte, len)
	request.Body.Read(body)
	fmt.Fprintln(writer, string(body))
}

func main() {
	http.HandleFunc("/header", headerHandler)
	http.HandleFunc("/body", bodyHandler)
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
```

```bash
linux:~ # curl -v http://127.0.0.1:8080/header
linux:~ # curl -i http://127.0.0.1:8080/header
linux:~ # curl -i http://127.0.0.1:8080/body
linux:~ # curl -i -d "name=abc"http://127.0.0.1:8080/body
linux:~ # curl -i -d '{"name": "abc"}' http://127.0.0.1:8080/body
```


### form

```go
package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

type User struct {
	Username      string
	Password      string
}

func loginHandler(writer http.ResponseWriter, request *http.Request) {
	log.Println("method: ", request.Method)
	log.Println("Content-Type: ", request.Header.Get("Content-Type"))

	switch request.Method {
	case "POST":
		switch request.Header.Get("Content-Type") {
		case "application/x-www-form-urlencoded":
			request.ParseForm()
			fmt.Fprintf(writer, "username: "+request.Form.Get("username")+"\n")
			fmt.Fprintf(writer, "password: "+request.FormValue("password")+"\n")
		//case "multipart/form-data":
		case "application/json":
			var user User
			body, _ := ioutil.ReadAll(request.Body)
			json.Unmarshal(body, &user)
			fmt.Fprintf(writer,"%+v", user)
		default:
			len := request.ContentLength
			body := make([]byte, len)
			request.Body.Read(body)
			fmt.Fprintln(writer, string(body))
		}
	default:
		tmpl, _ := template.ParseFiles("login.html")
		tmpl.Execute(writer, nil)
	}
	log.Println("Form: ")
	log.Println(request.Form)
	log.Println("PostForm")
	log.Println(request.PostForm)
	log.Println("MultipartForm")
	log.Println(request.MultipartForm)
}

func uploadHandler(writer http.ResponseWriter, request *http.Request) {
	if request.Method == "GET" {
		tmpl, _ := template.ParseFiles("upload.html")
		tmpl.Execute(writer, nil)
	} else {
		request.ParseMultipartForm(32 << 20)
		file, handler, err := request.FormFile("uploadfile")
		if err != nil {
			log.Println(err)
			return
		}
		defer file.Close()
		fmt.Fprintf(writer, "%v", handler.Header)
		f, err := os.OpenFile("./tmp/"+handler.Filename, os.O_WRONLY|os.O_CREATE, 0666)
		if err != nil {
			log.Println(err)
			return
		}
		defer f.Close()
		io.Copy(f, file)
	}
}

func main() {
	http.HandleFunc("/login", loginHandler)
	http.HandleFunc("/upload", uploadHandler)
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
```

```html
<!-- login.html -->
<!DOCTYPE html>
<html lang="utf-8">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <form action="/login" method="post">
        username: <input type="text" name="username" /><br />
        password: <input type="password" name="password" /><br />
        <input type="submit" value="submit" />
    </form>

    <form action="/login" method="post" enctype="application/x-www-form-urlencoded">
        username: <input type="text" name="username" /><br />
        password: <input type="password" name="password" /><br />
        <input type="submit" value="submit" />
    </form>

    <form action="/login" method="post" enctype="multipart/form-data">
        username: <input type="text" name="username" /><br />
        password: <input type="password" name="password" /><br />
        <input type="submit" value="submit" />
    </form>
</body>
</html>
```

```html
<!-- upload.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload</title>
</head>
<body>
    <form enctype="multipart/form-data" action="/upload" method="post">
        <input type="file" name="uploadfile" />
        <input type="submit" value="upload" />
    </form>
</body>
</html>
```

```bash
linux:~ # curl -X GET http://127.0.0.1:8080/login
linux:~ # curl -X POST -d "username=go&password=123" http://127.0.0.1:8080/login?api=v1
linux:~ # curl -X POST -d "username=go" -d "password=123" http://127.0.0.1:8080/login?api=v1

linux:~ # date >> tmp.txt
linux:~ # curl -X POST --form uploadfile=@tmp.txt http://127.0.0.1:8080/upload
```


### cookie

```go
package main

import (
	"fmt"
	"net/http"
)

func indexHandle(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Cookie Operation")
}

func cookieSetHandle(w http.ResponseWriter, r *http.Request) {
	c := http.Cookie{
		Name: "testCookie",
		Value: "1234",
		MaxAge: 300,
	}
	http.SetCookie(w, &c)
	fmt.Fprintf(w, "Set Cookie")
}

func cookieGetHandle(w http.ResponseWriter, r *http.Request) {
	if c, err := r.Cookie("testCookie"); err != nil {
		fmt.Fprintf(w, "Fail To Get Cookie")
	} else {
		fmt.Fprintf(w, "Get Cookie:, ", c.Value)
	}
}

func cookieDeleteHandle(w http.ResponseWriter, r *http.Request) {
	c := http.Cookie{
		Name: "testCookie",
		MaxAge: -1,
	}
	http.SetCookie(w, &c)
	fmt.Fprintf(w, "Delete Cookie")
}

func main() {
	http.HandleFunc("/", indexHandle)
	http.HandleFunc("/set", cookieSetHandle)
	http.HandleFunc("/get", cookieGetHandle)
	http.HandleFunc("/delete", cookieDeleteHandle)
	
	server := http.Server{
		Addr: "0.0.0.0:8080",
	}
	server.ListenAndServe()
}
```

```bash
linux:~ # curl -b tmp.cookie http://127.0.0.1:8080/set
linux:~ # cat tmp.cookie
linux:~ # curl http://127.0.0.1:8080/get
linux:~ # curl -c tmp.cookie http://127.0.0.1:8080/get
linux:~ # curl -c tmp.cookie http://127.0.0.1:8080/delete
```


---

## template

### Parse

```go
package main

import (
	"html/template"
	"log"
	"os"
)

func main() {
	name := "Go"
	tpl0 := template.New("example")
	tpl0, _ = tpl0.Parse("Hello {{.}} !")
	if err := tpl0.Execute(os.Stdout, name); err != nil {
		log.Fatalln("error: ", err)
	}

	days := []string{"Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"}
	tpl1 := template.New("example")
	tpl1, _ = tpl1.Parse(`
{{range $index, $element := .}}
	{{$index}} -> {{$element}}
{{end}}
`)
	if err := tpl1.Execute(os.Stdout, days); err != nil {
		log.Fatalln("error: ", err)
	}

	weekDay := map[string]string{
		"sun": "Sunday",
		"mon": "Monday",
		"tues": "Tuesday",
		"wed": "Wednesday",
		"thurs": "Thursday",
		"fri": "Friday",
		"sat": "Saturday"}
	tpl2 := template.New("example")
	tpl2, _ = tpl2.Parse(`
{{range $key, $value := .}}
	{{$key}} -> {{$value}}
{{end}}
`)
	if err := tpl2.Execute(os.Stdout, weekDay); err != nil {
		log.Fatalln("error: ", err)
	}

	type Person struct {
		UserName string
	}
	p := Person {UserName: "Go"}
	tpl3 := template.New("example")
	tpl3, _ = tpl3.Parse(`Hello {{.UserName}}`)
	if err := tpl3.Execute(os.Stdout, p); err != nil {
		log.Fatalln("error: ", err)
	}
}
```


### ParseFiles

```bash
linux:~/project # cat main.go
package main

import (
	"html/template"
	"log"
	"net/http"
)

type Todo struct {
	Title string
	Done  bool
}

type TodoPageData struct {
	PageTitle string
	Todos     []Todo
}

func main() {
	tmpl := template.Must(template.ParseFiles("template/layout.html"))

	mux := http.NewServeMux()
	mux.HandleFunc("/", func(writer http.ResponseWriter, request *http.Request) {
		data := TodoPageData{
			PageTitle: "My TODO list",
			Todos: []Todo{
				{Title: "Task 1", Done: false},
				{Title: "Task 2", Done: true},
				{Title: "Task 3", Done: true},
			},
		}
		if err := tmpl.Execute(writer, data); err != nil {
			log.Fatal("template execute: ", err)
		}
	})

	server := &http.Server{
		Addr:    "0.0.0.0:8080",
		Handler: mux,
	}

	if err := server.ListenAndServe(); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}

linux:~/project # cat template/layout.html
<!DOCTYPE html>
<html lang="utf-8">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>{{.PageTitle}}</h1>
    <ul>
        {{range .Todos}}
            {{if .Done}}
                <li class="done">{{.Title}}</li>
            {{else}}
                <li>{{.Title}}</li>
            {{end}}
        {{end}}
    </ul>
</body>
</html>

linux:~/project # tree
.
├── template
│   └ layout.html
└── main.go

linux:~ # curl http://127.0.0.1:8080
```


### ParseGlob

```go
// main.go
package main

import (
	"html/template"
	"log"
	"os"
)

func main() {
	tpl := template.Must(template.ParseGlob("*.html"))
	if err := tpl.ExecuteTemplate(os.Stdout, "header", nil); err != nil {
		log.Fatalln("error: ", err)
	}
	if err := tpl.ExecuteTemplate(os.Stdout, "footer", nil); err != nil {
		log.Fatalln("error: ", err)
	}
	if err := tpl.ExecuteTemplate(os.Stdout, "content", nil); err != nil {
		log.Fatalln("error: ", err)
	}
	if err := tpl.ExecuteTemplate(os.Stdout, "content", "Go"); err != nil {
		log.Fatalln("error: ", err)
	}
	if err := tpl.ExecuteTemplate(os.Stdout, "index", "Go"); err != nil {
		log.Fatalln("error: ", err)
	}
	if err := tpl.Execute(os.Stdout, "Go"); err != nil {
		log.Fatalln("error: ", err)
	}
}
```

```html
<!-- header.html -->
{{define "header"}}
    <h1>It's header</h1>
{{end}}
```

```html
<!-- footer.html -->
{{define "footer"}}
    <h3>It's footer</h3>
{{end}}
```

```html
<!-- content.html -->
{{define "content"}}
    <p>Hello {{.}} !"</p>
{{end}}
```

```html
<!-- index.html -->
{{define "index"}}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
{{template "header"}}
{{template "content" .}}
{{template "footer"}}
</body>
</html>
{{end}}
```

```bash
linux:~/project # tree
.
├── content.html
├── footer.html
├── header.html
├── inde.html
└── main.go

linux:~ # curl http://127.0.0.1:8080
```


---

## reference

[build-web-application-with-golang](https://github.com/astaxie/build-web-application-with-golang)
