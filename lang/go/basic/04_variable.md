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
