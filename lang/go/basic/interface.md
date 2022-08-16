# interface

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
