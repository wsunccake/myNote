# the go programmign language


```bash
$ cd `go env GOPATH`
```

## program structure

### declaration

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

### variable


```go
// var declaration
var s string       // ""
var i, j, k int    // int, int, int
var b, f, s = true, 2.3, "four"   // bool, float64, string

// short variable declaration
i := 100                   // int
var boiling float64 = 100  // float64
i, j := 0, 1

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

## ref

[The Go Programming Language](http://www.gopl.io/)

[gopl](https://github.com/dreamrover/gopl-pdf)

[Go語言聖經](https://wizardforcel.gitbooks.io/gopl-zh/content/index.html)
