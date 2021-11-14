# error

## errors.New

```go
func hello(name string) (string, error) {
	if name == "" {
		return "", errors.New("empty name")
	}

	message := fmt.Sprintf("Hi, %v", name)
	return message, nil
}

func main() {
	message, err := hello("")
	if err != nil {
		fmt.Errorf(err)
	}
	fmt.Println(message)
}
```


---

## fmt.Errorf

```go
func hello(name string) (string, error) {
	if name == "" {
		return "", fmt.Errorf("empty name")
	}

	message := fmt.Sprintf("Hi, %v", name)
	return message, nil
}

func main() {
	message, err := hello("")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(message)
}
```


---

## type error

```go
type error interface {  
    Error() string
}
```

```go
type myError struct {
	msg string
}

func (m *myError) Error() string {
	return m.msg
}

func hello(name string) (string, error) {
	if name == "" {
		return "", &myError{"empty name"}
	}

	message := fmt.Sprintf("Hi, %v", name)
	return message, nil
}

func main() {
	message, err := hello("")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(message)
}
```
