# reflect

## reflect

```go
package main

import (
	"fmt"
	"reflect"
)

type Person struct {
	Name string
	Age  int `json:"type" id:"100"`
	money int
}

func (p Person) Show() {
	fmt.Printf("Hi, %s\n", p.Name)
}

func (p Person) Grow() {
	p.Age++
}

func (p Person) deposit() int {
	return p.money
}

func main() {
	var i int = 1
	var p Person = Person{"jo", 10, 100}
	field := "Age"

//
// type
//
	typeOfI := reflect.TypeOf(i)
	fmt.Printf("TypeOf i %v\n", typeOfI)
	fmt.Printf("TypeOf i Kind: %v, Name: %v\n", typeOfI.Kind(), typeOfI.Name())
	// TypeOf i int
	// TypeOf i Kind: int, Name: int

	typeOfP := reflect.TypeOf(p)
	fmt.Printf("TypeOf p %v\n", typeOfP)
	fmt.Printf("TypeOf p Kind: %v, Name: %v\n", typeOfP.Kind(), typeOfP.Name())
	// TypeOf p main.Person
	// TypeOf p Kind: struct, Name: Person
	if name, ok := typeOfP.FieldByName("Name"); ok {
		fmt.Printf("name: %v, .Name: %v, .Type: %v\n", name, name.Name, name.Type)
	}
	// name: {Name  string  0 [0] false}, .Name: Name, .Type: string
	if age, ok := typeOfP.FieldByName("Age"); ok {
		fmt.Printf("age.Tag.Get json: %v, id: %v\n", age.Tag.Get("json"), age.Tag.Get("id"))
	}
	// age.Tag.Get json: type, id: 100
	for i := 0; i < typeOfP.NumField(); i++ {
		fmt.Printf("Field %v: %v\n", i, typeOfP.Field(i))
	}
	// Field 0: {Name  string  0 [0] false}
	// Field 1: {Age  int json:"type" id:"100" 16 [1] false}
	// Field 2: {money main int  24 [2] false}
	for i := 0; i < typeOfP.NumMethod(); i++ {
		fmt.Printf("Method %v: %v\n", i, typeOfP.Method(i))
	}
	// Method 0: {Grow  func(main.Person) <func(main.Person) Value> 0}
	// Method 1: {Show  func(main.Person) <func(main.Person) Value> 1}

	var ptrI *int
	typeOfPtrI := reflect.TypeOf(ptrI)
	fmt.Printf("typeOf ptrI %v\n", typeOfPtrI)
	fmt.Printf("typeOf ptrI Kind: %v, Name: %v\n", typeOfPtrI.Kind(), typeOfPtrI.Name())
	// typeOf ptrI *int
	// typeOf ptrI Kind: ptr, Name:
	typeOfPtrIElem := reflect.TypeOf(ptrI).Elem()
	fmt.Printf("typeOf ptrI Elem %v\n", typeOfPtrIElem)
	fmt.Printf("typeOf ptrI Elem Kind: %v, Name: %v\n", typeOfPtrIElem.Kind(), typeOfPtrIElem.Name())
	// typeOf ptrI Elem int
	// typeOf ptrI Elem Kind: int, Name: int

//
// value
//
	valueOfI := reflect.ValueOf(i)
	fmt.Printf("valueOf i %v\n", valueOfI)
	fmt.Printf("valueOf i CanSet: %v, CanAddr: %v\n", valueOfI.CanSet(), valueOfI.CanAddr())
	// valueOf i 1
	// valueOf i CanSet: false, CanAddr: false

	valueOfPtrI := reflect.ValueOf(&i)
	fmt.Printf("valueOf &i %v\n", valueOfPtrI)
	fmt.Printf("valueOf &i CanSet: %v, CanAddr: %v\n", valueOfPtrI.CanSet(), valueOfPtrI.CanAddr())
	// valueOf &i 0xc00010c008
	// valueOf &i CanSet: false, CanAddr: false

	valueOfPtrIElem := valueOfPtrI.Elem()
	fmt.Printf("i: %v, valueOfI: %v, valueOfPtrIElem: %v\n", i, valueOfI, valueOfPtrIElem)
	valueOfPtrIElem.Set(reflect.ValueOf(3))
	fmt.Printf("i: %v, valueOfI: %v, valueOfPtrIElem: %v\n", i, valueOfI, valueOfPtrIElem)
	valueOfPtrIElem.SetInt(5)
	fmt.Printf("i: %v, valueOfI: %v, valueOfPtrIElem: %v\n", i, valueOfI, valueOfPtrIElem)
	// i: 1, valueOfI: 1, valueOfPtrIElem: 1
	// i: 3, valueOfI: 1, valueOfPtrIElem: 3
	// i: 5, valueOfI: 1, valueOfPtrIElem: 5

	valueOfP := reflect.ValueOf(p)
	fmt.Printf("valueOf p %v\n", valueOfP)
	fmt.Printf("valueOf p . %s %v\n", field, valueOfP.FieldByName(field))
	// valueOf p {jo 10 100}
	// valueOf p . Age 10
	valueOfP.MethodByName("Show").Call([]reflect.Value{})
	// Hi, jo
	valueOfP.MethodByName("Grow").Call([]reflect.Value{})
	fmt.Printf("valueOf p %v\n", valueOfP)
	// valueOf p {jo 10 100}
	for i := 0; i < valueOfP.NumMethod(); i++ {
		fmt.Printf("Method %v: %v\n", i, valueOfP.Method(i).String())
	}
	// Method 0: <func() Value>
	// Method 1: <func() Value>

	valueOfPtrP := reflect.ValueOf(&p)
	fmt.Printf("valueOf &p %v\n", valueOfPtrP)
	fmt.Printf("valueOf &p . %s %v\n", field, valueOfPtrP.Elem().FieldByName(field))
	// valueOf &p &{jo 10 100}
	// valueOf &p . Age 10

	fmt.Printf("p: %v, valueOfP: %v, valueOfPtrPElem: %v\n", p, valueOfP, valueOfPtrP.Elem())
	valueOfPtrP.Elem().FieldByName(field).SetInt(15)
	fmt.Printf("p: %v, valueOfP: %v, valueOfPtrPElem: %v\n", p, valueOfP, valueOfPtrP.Elem())
	// p: {jo 10 100}, valueOfP: {jo 10 100}, valueOfPtrPElem: {jo 10 100}
	// p: {jo 15 100}, valueOfP: {jo 10 100}, valueOfPtrPElem: {jo 15 100}
}
```
