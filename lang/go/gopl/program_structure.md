# program structure

## declaration

```go
package main

import "fmt"

func main() {
    const freezingF, boilingF = 32.0, 212.0
    fmt.Printf("%g°F = %g°C\n", freezingF, fToC(freezingF)) // "32°F = 0°C"
    fmt.Printf("%g°F = %g°C\n", boilingF, fToC(boilingF))   // "212°F = 100°C"
}

func fToC(f float64) float64 {
    return (f - 32) * 5 / 9
}
```


---

## variable

### var declaration

```go
var s string       // ""
var i, j, k int    // int, int, int
var b, f, s = true, 2.3, "four"   // bool, float64, string
```


### short variable declaration

```go
i := 100                   // int
var boiling float64 = 100  // float64
i, j := 0, 1
```


### pointer

```go
// pointer
x := 1
p := &x  // p, of type *int, points to x
*p = 2   // equivalent to x = 2

// address
var x, y int
fmt.Println(&x == &x, &x == &y, &x == nil)   // "true false false"

var p = f()
func f() *int {
    v := 1
    return &v
}
fmt.Println(f() == f()) // "false"

func incr(p *int) int {
    *p++ // increments what p points to; does not change p
    return *p
}
v := 1
incr(&v)              // side effect: v is now 2
fmt.Println(incr(&v)) // "3" (and v is 3)
```

```bash
linux:~ $ cd `go env GOPATH`
linux:~/go $ mkdir -p src/echo4
linux:~/go $ vi src/echo4/main.go
package main

import (
    "flag"
    "fmt"
    "strings"
)

var n = flag.Bool("n", false, "omit trailing newline")
var sep = flag.String("s", " ", "separator")

func main() {
    flag.Parse()
    fmt.Print(strings.Join(flag.Args(), *sep))
    if !*n {
        fmt.Println()
    }
}

linux:~/go $ go build echo4
linux:~/go $ ./echo4 a bc def        # a bc def
linux:~/go $ ./echo4 -s / a bc def   # a/bc/def
linux:~/go $ ./echo4 -n a bc def     # a bc def
linux:~/go $ ./echo4 -help
Usage of ./echo4:
  -n    omit trailing newline
  -s string
        separator (default " ")
```


### new function

```go
p := new(int)    // p, of type *int, points to an unnamed int variable
fmt.Println(*p)  // 0
*p = 2           // sets the unnamed int to 2
fmt.Println(*p)  // 2

func newInt() *int {
    return new(int)
}

func newInt() *int {
    var dummy int
    return &dummy
}

p := new(int)
q := new(int)
fmt.Println(p == q) // "false"
```


### lifetime of variable

```go
for t := 0.0; t < cycles*2*math.Pi; t += res {
    x := math.Sin(t)
    y := math.Sin(t*freq + phase)
    img.SetColorIndex(size+int(x*size+0.5), size+int(y*size+0.5), blackIndex)
}

var global *int
func f() {
    var x int
    x = 1
    global = &x
}

func g() {
    y := new(int)
    *y = 1
}
```

---

## assignment

```go
x = 1
*p = true
person.name = "bob"
count[x] = count[x] * scale // array or slice or map element
count[x] *= scale

v := 1
v++ //sameasv=v+1;vbecomes2
v-- //sameasv=v-1;vbecomes1again
```


### tuple assignment

```go
x, y = y, x
a[i], a[j] = a[j], a[i]

func gcd(x, y int) int {
    for y != 0 {
        x, y = y, x%y
    }
return x
}

func fib(n int) int {
    x, y := 0, 1
    for i := 0; i < n; i++ {
        x, y = y, x+y
    }
    return x
}

i, j, k = 2, 3, 5
f, err = os.Open("foo.txt")  // function call returns two values
v, ok = m[key]               // map lookup
v, ok = x.(T)                // type assertion
v, ok = <-ch                 // channel receive
_, err = io.Copy(dst, src)   // discard byte count
_, ok = x.(T)                // check type but discard result
```


### assignability

```go
medals := []string{"gold", "silver", "bronze"}

medals[0] = "gold"
medals[1] = "silver"
medals[2] = "bronze"
```