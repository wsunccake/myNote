# function

## func

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


---

## function variable / anonymous function

```go
package main

import "fmt"

type add func(a int, b int) int

func addTemp() func(x, y int) int {
	f := func(x, y int) int {
		println(x, "+", y)
		return x + y
	}
	return f
}

func simple(c func(a, b int) int) {
	fmt.Println("run function variable as argument", c(60, 7))
}

func main() {
	// first order function
	func (x, y int) int {
		fmt.Println(x, "+", y)
		return x + y
	}(0, 3)

	add1 := func (x, y int) int {
		fmt.Println(x, "+", y)
		return x + y
	}
	add1(1, 2)

	var add2 add = func (x, y int) int {
		fmt.Println(x, "+", y)
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
