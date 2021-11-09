# slice

## basic

```go
s := make([]string, 3)
fmt.Println("emp:", s)          // []

s[0] = "a"
s[1] = "b"
s[2] = "c"
fmt.Println("set:", s)          // [a b c]
fmt.Println("get:", s[2])       // c
fmt.Println("len:", len(s))     // 3

s = append(s, "d")
s = append(s, "e", "f")
fmt.Println("apd:", s)          // [a b c d e f]

c := make([]string, len(s))
copy(c, s)
fmt.Println("cpy:", c)          // [a b c d e f]
fmt.Println(reflect.TypeOf(c))	// []int

l := s[2:5]
fmt.Println("sl1:", l)          // [c d e]
l = s[:5]
fmt.Println("sl2:", l)          // [a b c d e]
l = s[2:]
fmt.Println("sl3:", l)          // [c d e f]

t := []string{"g", "h", "i"}
fmt.Println("dcl:", t)          // [g h i]

twoD := make([][]int, 3)
for i := 0; i < 3; i++ {
	innerLen := i + 1
	twoD[i] = make([]int, innerLen)
	for j := 0; j < innerLen; j++ {
		twoD[i][j] = i + j
	}
}
fmt.Println("2d: ", twoD)       // [[0] [1 2] [2 3 4]]
```


---

## for range

```go
twoD := [][]int{{0, 1, 2}, {3, 4, 5}}
for i, e := range twoD {
	fmt.Println(i, e)
}
fmt.Println(reflect.TypeOf(twoD))
```


---

## array / slice to slice

```go
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
```


---

## function

```go
func doubleValue(a []int) {
	for i, v := range a {
		a[i] = v * 2
	}
}

func doublePointer(a *[]int) {
	for i, v := range *a {
		(*a)[i] = v * 2
	}
}

func main() {
	a := []int{1, 2, 3}
	fmt.Println(a)

	doubleValue(a)
	fmt.Println(a)

	doublePointer(&a)
	fmt.Println(a)
}
```


---

## os.Args

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println(os.Args)
}
```


```bash
linux:~ $ go run main.go 1 a Z
```
