# go

## introduction


---

## install

```bash
centos:~ # yum install golang
centos:~ # go env
```


---

## hello

```bash
linux:~ # hello.go
package main

import "fmt"

func main() {
    fmt.Println("Hello Go")
}

# run
linux:~ # go run hello.go

# compile to binary
linux:~ # go build hello.go
linux:~ # ./hello
```


---

## project

### simple

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # vi main.go
package main

func main() {
	println("Hello go")
}

# run with source
linux:~/project # go run main.go

# build binary
linux:~/project # export GOBIN=~/project/bin
linux:~/project # go install
linux:~/project # ls $GOBIN

# run with binary
linux:~/project # ./bin/project

linux:~/project # tree
.
├── bin
│   └── project
└── main.go
```


### import

```bash
linux:~/project # mkdir -p src/hello
linux:~/project # vi src/hello/myFunc.go
package hello

func Hello() {
	println("Hello GO")
}

func Hi() string {
	return "Hi GO"
}

linux:~/project # vi main.go
package main

import "hello"

func main() {
    println("Hello go")
    hello.Hello()
}

# run with source
linux:~/project # export GOPATH=~/project
linux:~/project # go run main.go

# build binary
linux:~/project # export GOBIN=~/project/bin
linux:~/project # go install
linux:~/project # ls $GOBIN

# run with binary
linux:~/project # ./bin/project

linux:~/project # tree
.
├── bin
│   └── project
├── main.go
└── src
    └── hello
        └── myFunc.go
```


### test

```bash
linux:~/project # vi hello_test.go
package main

import "testing"
imrpot "hello"

func TestHello(t *testing.T) {
	if hello.Hi() != "Hi Go" {
		t.Error("fail")
	}
}

# test
linux:~/project # export GOPATH=~/project
linux:~/project # go test

linux:~/project # tree
.
├── bin
│   └── project
├── hello_test.go
├── main.go
└── src
    └── hello
        └── myFunc.go
```

---

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

## data type

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

## condition


### if

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	fmt.Print("input m/f: ")
	reader := bufio.NewReader(os.Stdin)
	text, _ := reader.ReadString('\n')
	text = strings.TrimSuffix(text, "\n")

	if text == "m" {
		fmt.Println("Male")
	} else if text == "f" {
		fmt.Println("Female")
	} else {
		fmt.Println("Unknown")
	}
}
```

### switch


```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	fmt.Print("input m/f: ")
	reader := bufio.NewReader(os.Stdin)
	text, _ := reader.ReadString('\n')
	text = strings.TrimSuffix(text, "\n")

	switch text {
	case "m":
		fmt.Println("Male")
	case "f":
		fmt.Println("Female")
	default:
		fmt.Println("Unknown")
	}
}
```


### select


---

## loop


### for

```go
package main

import (
	"fmt"
)

func main() {
	const MAX int = 5
	for i:=0; i < MAX; i++ {
		fmt.Println(i)
	}

	i := 0
	for true {
		fmt.Println(i)
		i++
		if i >= MAX {
			break
		}
    }
    
    for i, v := range [MAX]int{1, 4, 5, 9} {
		fmt.Println(i, v)
	}
}
```


### goto

```go
package main

import (
	"fmt"
)

func main() {
	const MAX int = 5
	i := 0
	LOOP: fmt.Println(i)
	i++
	if i < MAX {
		goto LOOP
	}
}
```


---

## function

```go
package main

import "fmt"

func max(x, y int) int{
	var temp int

	if x > y {
		temp = x
	} else {
		temp = y
	}
	
	return temp
}

func main() {
	fmt.Printf("max: %d\n", max(5, 10))
}
```

```go
package main

import "fmt"

func main() {
	a := 1
	b := 2

	fmt.Printf("before swap %d, %d\n", a, b)
	swap1(a, b)
	fmt.Printf("after swap %d, %d\n", a, b)

	fmt.Printf("before swap %d, %d\n", a, b)
	swap2(&a, &b)
	fmt.Printf("after swap %d, %d\n", a, b)
}

// call by value
func swap1(x, y int) {
	var temp int
	temp = x
	x = y
	y = temp
}

// call by address
func swap2(x, y *int) {
	var temp int
	temp = *x
	*x = *y
	*y = temp
}
```


### function variable / anonymous function

```go
package main

type add func(a int, b int) int

func addTemp() func(x, y int) int {
	f := func(x, y int) int {
		println(x, "+", y)
		return x + y
	}
	return f
}

func simple(c func(a, b int) int) {
	println("run function variable as argument", c(60, 7))
}

func main() {
	// first order function
	func (x, y int) int {
		println(x, "+", y)
		return x + y
	}(0, 3)

	add1 := func (x, y int) int {
		println(x, "+", y)
		return x + y
	}
	add1(1, 2)

	var add2 add = func (x, y int) int {
		println(x, "+", y)
		return x + y
	}
	add2(2, 4)

	add3 := addTemp()
	add3(1, 9)

    // high order function
	simple(func (x, y int) int {
		println(x, "+", y)
		return x + y
	})
	simple(add1)
	simple(add2)
	simple(add3)
}
```


---

## array

```go
package main

func main() {
    var arr1 = [3]int{1, 2, 3}
    var arr2 = []int {4, 5, 6}
    var arr3 [3]int
    arr3[0] = 7
    arr3[1] = 8
    arr3[2] = 9
    var i int
    
    for i, e := range(arr1) {
        println(i, e)
    }

    for i := range arr2 {
        println(i)
    }

    for i = 0; i < 3; i++ {
        println(i, arr3[i])
    }
}
```


### function

```go
package main

func showArray(array []int) {
    for i, e := range array {
        println(i, e)
    }
}

func main() {
    var arr = []int {4, 5, 6}
    showArray(arr)
}
```


### 2d

```go
package main

func main() {
    var arr2d = [2][3]int{{1, 2, 3}, {4, 5, 6}}
    for i1, e1 := range(arr2d) {
        for i2, e2 := range e1 {
            println(i1 ,i2, e2)
        }
    }
}
```


### slice

```go
package main

import (
	"fmt"
)

func main() {
	odds := []int{2, 4, 6, 8, 10}
	o1 := odds[1:3]
	o2 := odds[:2]
	o3 := odds[3:]
	o4 := odds[3]
	fmt.Println(o1, o2, o3, o4)

	names := []string{"Finn", "LPJ", "Tino"}
	n1 := names[0]
	fmt.Println(n1, n1[2:], n1[:], n1[1:3])
```


### make, append

```go
package main

import (
	"fmt"
	"reflect"
)

func main() {
	a1 := []int{1, 2, 3}
	fmt.Println(reflect.TypeOf(a1), a1, len(a1), cap(a1))
	//a1[3] = 4
	a1 = append(a1, 4)
	fmt.Println(a1, len(a1), cap(a1))
	a1[3] = 1
	fmt.Println(a1, len(a1), cap(a1))

	a2 := [5]int{1, 2, 3}
	fmt.Println(reflect.TypeOf(a2), a2, len(a2), cap(a2))
	//a2[5] = 1
	//a2 = append(a2, 4)

	a3 := make([]int, 3, 10)
	fmt.Println(reflect.TypeOf(a3), a3, len(a3), cap(a3))
	//a3[3]=1
	a3 = append(a3, 3)
	fmt.Println(a3, len(a3), cap(a3))
}
```

---

## pointer

```go
package main

import "fmt"

func main() {
	var v1 int = 20
	var p1 *int
	p1 = &v1
	var p2 *int = &v1
	p3 := &v1
	p4 := new(int)
	p4 = &v1
	fmt.Printf("value v1: %d, *p1: %d, *p2: %d, *p3: %d, *p4: %d\n", v1, *p1, *p2, *p3, *p4)
	fmt.Printf("addres &v1: %x, p1: %x, p2: %x, p3: %x, p4: %x\n", &v1, p1, p2, p3, p4)
}
```


---

## struct

```go
package main

import "fmt"

type Person struct {
	name string
	age int
}

type Employee struct {
	Person
	int
}

func main() {
	var p1 Person = Person{name: "LPJ", age: 20}
	var p2 Person
	p2 = Person{"Tino", 25}
	p3 := Person{"Finn", 20}
	fmt.Printf("p1: %+v, p2: %+v, p3: %+v\n", p1, p2, p3)
	fmt.Println(p1.name, p1.age)

	e1 := Employee{Person{"yoyo", 21}, 1}
	fmt.Printf("e1: %+v\n", e1)
	fmt.Println(e1.name, e1.age, e1.int)
}
```


### function / method

```go
package main

import "fmt"

type Person struct {
	name string
	age int
}

func (p Person) grow1() {
	p.age++
}

func (p *Person) grow2() {
	p.age++
}

func main() {
	p := Person{name: "LPJ", age: 20}
	fmt.Printf("p: %+v\n", p)
	p.grow1()
	fmt.Printf("p: %+v\n", p)
	p.grow2()
	fmt.Printf("p: %+v\n", p)
}
```


---

## interface

```go
package main

import "fmt"

type vehicle interface {
	accelerate()
}

func describe(v vehicle)  {
	fmt.Printf("%+v\n", v)
	v.accelerate()
}

type Car struct {
	vendor string
	color string
}

func (c Car) accelerate() {
	fmt.Println("10 m/s")
}

type Toyota struct {
	Car
	model string
}

type BMW struct {
	Car
	model string
}

func (b BMW) accelerate() {
	fmt.Println("100 m/s")
}

func main() {
	c := Car{"unknown", "black"}
	describe(c)

	t := Toyota{Car{"toyota", "white"}, "ae86"}
	describe(t)

	b := BMW{Car{"bmw", "white"}, "m3"}
	describe(b)
}
```

---

## reference

[Golang tutorial series](https://golangbot.com/learn-golang-series/)

[Go Tutorial](https://www.tutorialspoint.com/go/index.htm)
