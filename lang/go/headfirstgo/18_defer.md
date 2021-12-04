# defer

## defer

```go
func hello() {
	fmt.Println("hello1")
	defer fmt.Println("hello2")
	fmt.Println("Hello3")
}

func hi() {
	fmt.Println("hi1")
	defer fmt.Println("hi2")
	fmt.Println("hi3")
}

func goodbye() {
	defer fmt.Println("goodbye1")
	fmt.Println("goodbye2")
	defer fmt.Println("goodbye3")
}

func main() {
	defer hello()
	hi()
	goodbye()
}

// hi1
// hi3
// hi2
// goodbye2
// goodbye3
// goodbye1
// hello1
// Hello3
// hello2
```

---

## error

```go
func openFile(filename string) (*os.File, error) {
	fmt.Println("open file", filename)
	return os.Open(filename)
}

func closeFile(file *os.File) {
	fmt.Println("colse file")
	file.Close()
}

func main() {
	filename := "a.txt"
	file, err := openFile(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer closeFile(file)
}
```
