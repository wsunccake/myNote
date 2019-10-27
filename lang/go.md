# go

## introduction


---

## install

```bash
centos:~ # yum install golang
centos:~ # go env
```


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

// call by reference
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


---

## pointer


---

## reference

[Golang tutorial series](https://golangbot.com/learn-golang-series/)

[Go Tutorial](https://www.tutorialspoint.com/go/index.htm)
