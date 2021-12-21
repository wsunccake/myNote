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

## constant

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

fmt.Printf("default %T: %t\n", b, b)    // bool: false
fmt.Printf("default %T: %d\n", i, i)    // int: 0
fmt.Printf("default %T: %f\n", f, f)    // float32: 0.000000
fmt.Printf("default %T: %s\n", s, s)    // string: 

fmt.Println(reflect.TypeOf(0))          // int
fmt.Println(reflect.TypeOf(1.0))        // float64
fmt.Println(reflect.TypeOf(true))       // bool
fmt.Println(reflect.TypeOf("go"))       // string
fmt.Println(reflect.TypeOf('g'))        // int32
```


---

## scope

```go
foo := "go"

fmt.Println("begin outter: ", foo)          // gp
{
	fmt.Println("begin innter: ", foo)      // go
	foo := "hello"
	fmt.Println("begin innter: ", foo)      // hello
}
fmt.Println("end outter: ", foo)            // go
```


```go
foo := "go"

fmt.Println("begin outter: ", foo)          // go
{
	fmt.Println("begin innter: ", foo)      // go
	foo = "hello"
	fmt.Println("begin innter: ", foo)      // hello
}
fmt.Println("end outter: ", foo)            // hello
```


---

## convert

```go
i := 1
f := 1.5
fmt.Println(float64(i) + f)
```
