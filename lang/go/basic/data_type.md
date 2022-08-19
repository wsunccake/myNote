# data type

## variable

```go
package main

import "fmt"

func main() {
    // var name type = expression
    var i int
    i = 1
    var j int = 1
    var k = 1

    // name := expression
    l := 1

    // const
    const PI = 3.14
    // PI = 3.0
	r := 10.0
	fmt.Printf("Circle are: %f\n", PI * r * r)
}
```


---

## primitive

```go
package main

import "fmt"

func main() {
	var b bool
	var i int
	var f float32
	var s string

	fmt.Printf("default %T: %t\n", b, b)
	fmt.Printf("default %T: %d\n", i, i)
	fmt.Printf("default %T: %f\n", f, f)
	fmt.Printf("default %T: %s\n", s, s)
}
```


---

## string

```go
package main

import (
	"fmt"
	"reflect"
	"strings"
)

func main() {
	var str string = "Hello Go"
	fmt.Println(str)
	fmt.Println("type: ", reflect.TypeOf(str))
	fmt.Println("length: ", len(str))
	fmt.Println("A ascii: ", "A"[0])

	fmt.Println("upper: ", strings.ToUpper(str))
	fmt.Println("lower: ", strings.ToLower(str))
	fmt.Println("has prefix: ", strings.HasPrefix(str,"hello"))
	fmt.Println("has suffix: ", strings.HasSuffix(str,"go"))

	lang := []string{"C", "C++", "Go"}
	fmt.Println(lang)
	fmt.Println("join: ", strings.Join(lang, ","))

	csvStr := "C,C++,Go"
	fmt.Println(csvStr)
	fmt.Println("split", strings.Split(csvStr, ","))
}
```


---

## type conversion / type casting

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	var x, y int = 3, 4
	var f float64 = math.Sqrt(float64(x*x + y*y))
	z := uint(f)
	fmt.Println(x, y, z)
}
```
