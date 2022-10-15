# array

## [<n>]<type>

```go
package main

import (
	"fmt"
)

func main() {
    var arr1 = [3]int{1, 2, 3}
    var arr2 = []int {4, 5, 6}
    var arr3 [3]int
    arr3[0] = 7
    arr3[1] = 8
    arr3[2] = 9
    var i int

    for i, e := range(arr1) {
        fmt.Println(i, e)
    }

    for i := range arr2 {
        fmt.Println(i)
    }

    for i = 0; i < 3; i++ {
        fmt.Println(i, arr3[i])
    }
}
```


---

## function

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

func main() {
    var arr = []int {4, 5, 6}
    showArray(arr)
}
```


---

## 2d

```go
package main

import (
	"fmt"
)

func main() {
    var arr2d = [2][3]int{{1, 2, 3}, {4, 5, 6}}
    for i1, e1 := range(arr2d) {
        for i2, e2 := range e1 {
            fmt.Println(i1 ,i2, e2)
        }
    }
}
```


---

# slice

## []<type>

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

	// emptySlice1 = make([]int, 0)
	// emptySlice2 = []int{}

	// var nilSlice []int
}
```


---

## make, append

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

## array / slice to slice

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
