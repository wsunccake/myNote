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


---

## routing / multiplexer

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
	http.HandleFunc("/api1", apiHandler)
	http.HandleFunc("/api2/", apiHandler)
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

## cookie


---

## reference

[build-web-application-with-golang](https://github.com/astaxie/build-web-application-with-golang)
