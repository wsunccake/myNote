# variable

## variable declaration

```go
//
var foo string
var bar int
foo = "go"
bar = 100

//
var foo string = "go"
var bar int = 100

//
var (
    foo string
    bar int
)
foo = "go"
bar = 100

//
var (
    foo string = "go"
    bar int = 100
)
```


---

## short declaration

```go
foo := "go"
bar := 100
```


---

```go
//
const (
    Monday = 1
    Tuesday = 2
    Wednesday = 3
)

//
const (
    Monday = iota + 1
    Tuesday
    Wednesday
)
```


---

## data type

```go
var b bool
var i int
var f float32
var s string

fmt.Printf("default %T: %t\n", b, b)
fmt.Printf("default %T: %d\n", i, i)
fmt.Printf("default %T: %f\n", f, f)
fmt.Printf("default %T: %s\n", s, s)
```


---

## scope

```go
foo := "go"

fmt.Println("begin outter: ", foo)
{
	fmt.Println("begin innter: ", foo)
	foo := "hello"
	fmt.Println("begin innter: ", foo)
}
fmt.Println("end outter: ", foo)
```
