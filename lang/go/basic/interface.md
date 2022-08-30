# interface

## interface

```go
package main

import "fmt"

type Vehicle interface {
	accelerate()
}

func describe(v Vehicle)  {
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

type Bicycle struct {
	vendor string
	color  string
}

func main() {
	c := Car{"unknown", "black"}
	describe(c)

	t := Toyota{Car{"toyota", "white"}, "ae86"}
	describe(t)

	b := BMW{Car{"bmw", "white"}, "m3"}
	describe(b)

	bi := Bicycle{"unknown", "black"}
	fmt.Printf("bicycle color: %s\n", bi.color)
}
```


---

## type assertion

```go
	var b0 interface{} = new(BMW)
	// b0.accelerate()
	// describe(b0)

	// 轉型 interface
	b0.(Vehicle).accelerate()
	describe(b0.(Vehicle))

	var b1 interface{ Vehicle } = new(BMW)
	b1.accelerate()
	describe(b1)
	b1.(Vehicle).accelerate()
	describe(b1.(Vehicle))

	// var b2 interface{} = new(Bicycle)
	// b2.accelerate()
	// describe(b2)
	// b2.(Vehicle).accelerate()
	// describe(b2.(Vehicle))

	// 判斷 type 是否包括 interface 需要的 method
	var _ Vehicle = (*BMW)(nil)
	// var _ Vehicle = (*Bicycle)(nil)
```


---

## switch

```go
package main

import "fmt"

func do(i interface{}) {
	switch v := i.(type) {
	case int:
		fmt.Printf("Twice %v is %v\n", v, v*2)
	case string:
		fmt.Printf("%q is %v bytes long\n", v, len(v))
	default:
		fmt.Printf("I don't know about type %T!\n", v)
	}
}

func main() {
	do(21)
	do("hello")
	do(true)
}
```
