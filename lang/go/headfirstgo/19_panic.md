# panic

## defer

```go
fmt.Println("a")
panic("oh no")
fmt.Println("b")
```

```go
fmt.Println("a")
panic("oh no")
defer fmt.Println("b")
```

```go
fmt.Println("a")
defer fmt.Println("a1")
panic("oh no")
fmt.Println("b")
```


---

## func

```go
func myFunction() {
	panic("oh no")
	fmt.Println("c")
}

func main() {
	fmt.Println("a")
	myFunction()
	fmt.Println("b")
}
```


---

## recover

```go
func myFunction() {
	defer func() {
		r := recover()
		if r != nil {
			fmt.Println("Recovered:", r)
		}
	}()

	panic("oh no")
}

func main() {
	fmt.Println("a")
	myFunction()
	fmt.Println("b")
}
```
