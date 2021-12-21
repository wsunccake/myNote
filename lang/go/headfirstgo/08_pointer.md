# pointer

## variable

```go
var val int
var ptr *int
fmt.Println(val)
fmt.Println(ptr)
fmt.Println(*ptr)
```


```go
v := 1
val := v
ptr := &v
fmt.Println(v)
fmt.Println(val)
fmt.Println(ptr)
fmt.Println(*ptr)

v = 3
fmt.Println(v)
fmt.Println(val)
fmt.Println(ptr)
fmt.Println(*ptr)
```


```go
v := 1
ptr := new(int)
ptr = &v
fmt.Println(v)
fmt.Println(ptr)
fmt.Println(*ptr)
```


---

## function

```go
// call by value
func zeroval(ival int) {
    ival = 0
}

// call by address
func zeroptr(iptr *int) {
    *iptr = 0
}

func main() {
    i := 1
    fmt.Println("initial:", i)      // 1
    zeroval(i)
    fmt.Println("zeroval:", i)      // 1

    zeroptr(&i)
    fmt.Println("zeroptr:", i)      // 0

    fmt.Println("pointer:", &i)
}
```
