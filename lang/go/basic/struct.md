# struct

## struct

```go
package main

import (
	"fmt"
	"reflect"
)

type Person struct {
	name string
	age int
}

type Employee struct {
	Person
	salary int
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
	fmt.Println(e1.name, e1.age, e1.salary)

	p1TypeOf := reflect.TypeOf(p1)
	p1ValueOf := reflect.ValueOf(p1)
	fmt.Printf("p1 TypeOf: %v, ValueOf: %v\n", p1TypeOf, p1ValueOf)

	for i := 0; i < p1TypeOf.NumField(); i++ {
		fmt.Println(p1TypeOf.Field(i))
	}

	switch p1TypeOf.Kind() {
	case reflect.Int:
		fmt.Println("int:")
	case reflect.String:
		fmt.Println("string:")
	case reflect.Struct:
		fmt.Println("struct:")
	default:
		fmt.Println("no match")
	}
	fmt.Println(p1TypeOf.Kind() == reflect.Struct)
}
```


---

## method

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
