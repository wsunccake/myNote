# web

## server

```go
func helloHandler(writer http.ResponseWriter, request *http.Request) {
	fmt.Fprint(writer, "Hello Go")

	// reqeust
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
	http.HandleFunc("/hello", helloHandler)
	http.ListenAndServe(":8080", nil)
}
```

```bash
linux:~ $ curl -ksL 'http://localhost:8080'
linux:~ $ curl -ksL 'http://localhost:8080/hello'
linux:~ $ curl -ksL 'http://localhost:8080/hello?id=1'
linux:~ $ curl -ksL 'http://localhost:8080/hello?id=1&foo=bar'
```


---

## client

```go
func main() {
	resp, err := http.Get("http://localhost:8080/hello")
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	fmt.Println("Response status:", resp.Status)
	scanner := bufio.NewScanner(resp.Body)
	for i := 0; scanner.Scan() && i < 5; i++ {
		fmt.Println(scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		panic(err)
	}
}
```


---

## httptest
