# basic

## content

- [variable](#variable)
  - [declare](#declare)
  - [primitive](#primitive)
  - [string](#string)
  - [type conversion / type casting](#type-conversion--type-casting)
  - [built-in math](#built-in-math)
  - [const & enum](#const--enum)
- [decision](#decision)
  - [if](#if)
  - [switch](#switch)
- [loop](#loop)
  - [for](#for)
  - [goto](#goto)
- [func](#func)
  - [return](#return)
  - [argument](#argument)
  - [call by value and address](#call-by-value-and-address)
  - [function variable / anonymous function](#function-variable--anonymous-function)
- [pointer](#pointer)
- [array](#array)
  - [array - basic](#array---basic)
  - [array - function](#array---function)
  - [multi array](#multi-array)
- [slice](#slice)
  - [slice - basic](#slice---basic)
  - [make & append](#make--append)
  - [to slice](#to-slice)
- [map](#map)

---

## variable

### declare

```go
package main

import "fmt"

// global variable
var (
	str     = "hello world!"
	packInt = 1
)

func testVariable() {
	var a int
	var s string
	fmt.Printf("%d %q\n", a, s)
}

func testVariableInit() {
	var a, b int = 3, 4
	var s string = "fa q"
	fmt.Printf("%d %d %q\n", a, b, s)
}

func testVariableType() {
	var a, b, s = 1, 2, "van"
	fmt.Printf("%d %d %q\n", a, b, s)
}

func testVariableLocal() {
	a, b, s := 5, 6, "deep dark fantasty"
	fmt.Printf("%d %d %q\n", a, b, s)
}

func testVariableDeclare() {
	// var name type = expression
	var i int
	i = 1
	var j int = 1
	var k = 1
	fmt.Println("i: %d, j: %d, k: %d", i, j, k)

	// name := expression
	l := 1
	fmt.Println("l: %d", l)

	// const
	const PI = 3.14
	// PI = 3.0
	r := 10.0
	fmt.Printf("Circle are: %f\n", PI*r*r)
}

func main() {
	fmt.Printf("%d\n", packInt)
	fmt.Print(str + "\n")
	fmt.Print("hello world\n")
	testVariable()
	testVariableInit()
	testVariableType()
	testVariableLocal()
	testVariableDeclare()
}
```

### primitive

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

### string

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

### type conversion / type casting

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

### built-in math

```go
package main

import (
	"fmt"
	"math"
	"math/cmplx"
)

func euler() {
	c := 3 + 4i
	fmt.Printf("Abs(3+4i)=%f\n", cmplx.Abs(c))
	fmt.Println("e^i(Pi)+1=", cmplx.Pow(math.E, 1i*math.Pi)+1)
	fmt.Printf("e^i(Pi)+1=%.3f\n", cmplx.Exp(1i*math.Pi)+1)
}

func triangle() {
	var a, b int = 3, 4
	var c int
	c = int(math.Sqrt(float64(a*a + b*b)))
	fmt.Println(c)
}

func main() {
	euler()
	triangle()
}
```

### const & enum

```go
package main

import "fmt"

func consts() {
	const (
		Van  = "van darkholme"
		a, b = 1, 2
	)
	var c int
	c = a + b
	fmt.Println(Van)
	fmt.Println(c)
}

func enums() {
	const (
		cpp = iota
		java
		python
		golang
		javascript
		perl
		mysql
	)
	fmt.Println(cpp, java, python, golang, javascript, perl, mysql)

	const (
		b = 1 << (10 * iota) //自增表达式
		kb
		mb
		gb
		tb
		pb
	)
	fmt.Println(b, kb, mb, gb, tb, pb)
}

func main() {
	consts()
	enums()
}
```

---

## decision

### if

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func testIf() {
	fmt.Print("input m/f: ")
	var text string

	_, err := fmt.Scanf("%s", &text)
	if err != nil {
		fmt.Println(err)
	}

	if text == "m" {
		fmt.Println("Male")
	} else if text == "f" {
		fmt.Println("Female")
	} else {
		fmt.Println("Unknown")
	}
}

func testIfErr() {
	fmt.Print("file: ")
	reader := bufio.NewReader(os.Stdin)
	file, _ := reader.ReadString('\n')
	file = strings.TrimSuffix(file, "\n")

	if data, err := os.ReadFile(file); err == nil {
		fmt.Print(string(data))
	} else {
		fmt.Println(err)
	}

}

func main() {
	testIf()
	testIfErr()
}
```

### switch

```go
package main

import (
	"fmt"
)

func testSwitchString() {
	fmt.Print("input m/f: ")
	var text string

	_, err := fmt.Scanf("%s", &text)
	if err != nil {
		fmt.Println(err)
	}

	switch text {
	case "m":
		fmt.Println("Male")
	case "f":
		fmt.Println("Female")
	default:
		fmt.Println("Unknown")
	}
}

func testSwitchInt() {
	fmt.Print("input 0~100: ")
	var score int

	_, err := fmt.Scanf("%d", &score)
	if err != nil {
		fmt.Println(err)
	}

	result := ""
	switch {
	case score < 0 || score > 100:
		result = "error score range"
	case score < 60:
		result = "F"
	case score < 80:
		result = "C"
	case score < 90:
		result = "B"
	case score < 100:
		result = "C"
	case score == 100:
		result = "A+"
	}

	fmt.Printf("result: %s\n", result)
}

func testSwitchInt2() {
	fmt.Print("input 1~7 (weekday): ")
	dayOfWeek := 0

	_, err := fmt.Scanf("%d", &dayOfWeek)
	if err != nil {
		fmt.Println(err)
	}

	switch dayOfWeek {
	case 1:
		fmt.Println("Monday")
		fallthrough
	case 2:
		fmt.Println("Tuesday")
		fallthrough
	case 3:
		fmt.Println("Wednesday")
		fallthrough
	case 4:
		fmt.Println("Thursday")
		fallthrough
	case 5:
		fmt.Println("Friday")
		fallthrough
	case 6:
		fmt.Println("Saturday")
	case 7:
		fmt.Println("Sunday")
	default:
		fmt.Println("Invalid Day")
	}
}

func main() {
	testSwitchString()
	testSwitchInt()
	testSwitchInt2()
}
```

---

## loop

## for

```go
package main

import (
	"fmt"
)

func testFor1() {
	const MAX int = 5
	for i := 0; i < MAX; i++ {
		fmt.Println(i)
	}
}

func testFor2() {
	const MAX int = 5
	i := 0
	for i < MAX {
		fmt.Println(i)
		i++
	}
}

func testFor3() {
	for i, v := range []int{9, 8, 7, 6, 5} {
		fmt.Println(i, v)
	}
}

func main() {
	testFor1()
	testFor2()
	testFor3()
}
```

### goto

```go
package main

import (
	"fmt"
)

func testGoto() {
	const MAX int = 5
	i := 0
LOOP:
	fmt.Println(i)
	i++
	if i < MAX {
		goto LOOP
	}

}

func main() {
	testGoto()
}
```

---

## func

### return

```go
package main

import "fmt"

// no return
func funHello() {
	fmt.Println("hello")
}

// with return
func funMin(x, y int) int {
	var z int

	if z = y; x < y {
		z = x
	}

	return z
}

// return with name
func funMax(x, y int) (z int) {
	if z = y; x > y {
		z = x
	}

	return
}

// multi return
func funDiv(a, b int) (q, r int, err error) {
	if b == 0 {
		return q, r, fmt.Errorf("divisor cannot be 0")
	}

	q = a / b
	r = a % b
	return q, r, nil
}

func main() {
    funHello()

	fmt.Printf("min: %d\n", funMin(15, 10))
	fmt.Printf("max: %d\n", funMax(15, 10))

	for i, j := range []int{1, 1} {
		if a, b, err := funDiv(j, i); err == nil {
			fmt.Println(a, b)
		} else {
			fmt.Println(err)
		}
	}
}
```

### argument

```go
package main

import "fmt"

func sum(nums ...int) int {
	s := 0
	for i := range nums {
		s += nums[i]
	}
	return s
}

func main() {
	fmt.Println("sum: ", sum(1, 2, 3))
	fmt.Println("sum: ", sum([]int{1, 2, 3}...)) // unpack slice
}
```

### call by value and address

```go
package main

import "fmt"

// call by value
func swapByValue(x int, y int) {
	temp := x
	x = y
	y = temp
}

// call by address
func swapByAddress(x, y *int) {
	temp := *x
	*x = *y
	*y = temp
}

func main() {
	a := 1
	b := 2

	fmt.Printf("before swap %d, %d\n", a, b)
	swapByValue(a, b)
	fmt.Printf("after swap %d, %d\n", a, b)

	fmt.Printf("before swap %d, %d\n", a, b)
	swapByAddress(&a, &b)
	fmt.Printf("after swap %d, %d\n", a, b)
}
```

### function variable / anonymous function

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
	func(x, y int) int {
		fmt.Println(x, "+", y)
		return x + y
	}(0, 3)

	// anonymous function
	add1 := func(x, y int) int {
		fmt.Println(x, "+", y)
		return x + y
	}
	add1(1, 2)

	var add2 add = func(x, y int) int {
		fmt.Println(x, "+", y)
		return x + y
	}
	add2(2, 4)

	add3 := addTemp()
	add3(1, 9)

	// high order function
	simple(func(x, y int) int {
		println(x, "+", y)
		return x + y
	})
	simple(add1)
	simple(add2)
	simple(add3)
}
```

---

## pointer

```text
& address of operator
* indirection operator
```

```go
package main

import "fmt"

func testPointer() {
	var v1 int = 20

	// declare pointer
	var p1 *int
	p1 = &v1

	// declare pointer with initial value
	var p2 *int = &v1

	// short declare pointer with initial value
	p3 := &v1

	// declare pointer
	p4 := new(int)
	p4 = &v1

	fmt.Printf("value v1: %d, *p1: %d, *p2: %d, *p3: %d, *p4: %d\n", v1, *p1, *p2, *p3, *p4)
	fmt.Printf("addres &v1: %x, p1: %x, p2: %x, p3: %x, p4: %x\n", &v1, p1, p2, p3, p4)
}

func main() {
	testPointer()
}
```

---

## array

### array - basic

```go
package main

import "fmt"

func testArray() {
	var arr1 = [3]int{1, 2, 3}
	var arr2 = []int{4, 5, 6}
	var arr3 [3]int
	arr3[0] = 7
	arr3[1] = 8
	arr3[2] = 9

	for i, e := range arr1 {
		fmt.Println(i, e)
	}

	for i := range arr2 {
		fmt.Println(i)
	}

	for i := 0; i < 3; i++ {
		fmt.Println(i, arr3[i])
	}
}

func main() {
	testArray()
}
```

### array - function

```go
package main

import (
	"fmt"
)

func showArray(array []int) {
	for i, e := range array {
		fmt.Println(i, e)
	}
}

func changeArray(arr []int) {
	arr[0] = 100
}

func main() {
	var arr = []int{4, 5, 6}
	showArray(arr)

    fmt.Println(arr)
	changeArray(arr)
	fmt.Println(arr)
}
```

### multi array

```go
package main

import (
	"fmt"
)

func main() {
	var arr2d = [2][3]int{{1, 2, 3}, {4, 5, 6}}
	for i1, e1 := range arr2d {
		for i2, e2 := range e1 {
			fmt.Println(i1, i2, e2)
		}
	}
}
```

---

## slice

### slice - basic

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

	// emptySlice1 := make([]int, 0)
	// emptySlice2 := []int{}

	// var nilSlice []int
}
```

### make & append

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

### to slice

```go
package main

import (
	"fmt"
)

func main() {
	array1 := [5]int{1, 2, 3, 4, 5}
	slice1 := array1[2:4]

	fmt.Printf("array: %+v\n", array1)
	fmt.Printf("array len: %d, cap: %d\n", len(array1), cap(array1))
	fmt.Printf("slice: %+v\n", slice1)
	fmt.Printf("slice len: %d, cap: %d\n", len(slice1), cap(slice1))

	fmt.Println("change slice...")
	slice1[1] = 22
	fmt.Printf("array: %+v\n", array1)
	fmt.Printf("slice: %+v\n", slice1)

	fmt.Println("append slice...")
	slice1 = append(slice1, 33)
	fmt.Printf("array: %+v\n", array1)
	fmt.Printf("slice: %+v\n", slice1)
	fmt.Printf("slice len: %d, cap: %d\n", len(slice1), cap(slice1))

	fmt.Println("append slice...")
	slice1 = append(slice1, 44)
	fmt.Printf("array: %+v\n", array1)
	fmt.Printf("slice: %+v\n", slice1)
	fmt.Printf("slice len: %d, cap: %d\n", len(slice1), cap(slice1))

	fmt.Println("change slice...")
	slice1[1] = 2222
	fmt.Printf("array: %+v\n", array1)
	fmt.Printf("slice: %+v\n", slice1)
}
```

---

## map

```go
package main

import "fmt"

func main() {
	var countryCapitalMap map[string]string
	countryCapitalMap = make(map[string]string)

	countryCapitalMap["France"] = "Paris"
	countryCapitalMap["Italy"] = "Rome"
	countryCapitalMap["Japan"] = "Tokyo"

	// check key exist
	if _, ok := countryCapitalMap["Taiwan"]; !ok {
		fmt.Println("no found Taiwan")
	}

	weekDay := map[string]string{
		"sun": "Sunday",
		"mon": "Monday",
		"tues": "Tuesday",
		"wed": "Wednesday",
		"thurs": "Thursday",
		"fri": "Friday",
		"sat": "Saturday"}

	delete(countryCapitalMap, "Italy")

	for k, v := range countryCapitalMap {
		fmt.Printf("%s -> %s\n", k, v)
	}


	k := "abc"
	v, ok := weekDay[k]
	if ok {
		fmt.Println(k, "->", v)
	} else {
		fmt.Println("no found", k)
	}

	// emptyMap1 := make(map[string]int)
	// emptyMap2 := map[string]int{}

	// var nilMap map[string]int
}
```
