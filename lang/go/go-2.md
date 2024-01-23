# oop

## content

- [struct](#struct)
  - [method](#method)
  - [tag](#tag)
  - [pointer](#pointer)
- [interface](#interface)

---

## struct

```go
package main

import (
	"fmt"
	"reflect"
)

type Person struct {
	name string
	age  int
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

### method

```go
package main

import "fmt"

type Person struct {
	name string
	age  int
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

### tag

```go
package main

import (
	"fmt"
	"reflect"
)

type User struct {
	id   int
	name string `max:"10"`
}

func main() {
	u := User{1, "Jane Doe"}
	t := reflect.TypeOf(u)
	for i := 0; i < t.NumField(); i++ {
		f := t.Field(i)
		if _, ok := f.Tag.Lookup("max"); ok {
			fmt.Println("Tag found")
		} else {
			fmt.Println("Tag not found")
		}

		fmt.Println(t.Field(i).Name)
		fmt.Println(t.Field(i).Tag.Get("max"))
	}
}
```

### pointer

```go
package main

import "fmt"

type Student struct {
	id   int
	name string
}

func main() {
	var s_1 *Student = new(Student)
	s_1.id = 100
	s_1.name = "cat"
	var s_2 Student = Student{id: 1, name: "tom"}
	fmt.Println(s_1, s_2)
}
```

```go
package main

import "fmt"

type Student struct {
	id    int
	name  string
	score int
}

func createStudent1(id int, name string) Student {
	return Student{id: id, name: name}
}

func createStudent2(id int, name string) *Student {
	return &Student{id: id, name: name}
}

func createStudents1(students []Student, name ...string) {
	for i, v := range name {
		students = append(students, Student{id: i, name: v})
	}
	fmt.Println(students)
}
func createStudents2(students []*Student, name ...string) {
	for i, v := range name {
		students = append(students, &Student{id: i, name: v})
	}
	fmt.Println(students)
}

func createStudents3(students *[]Student, name ...string) {
	for i, v := range name {
		*students = append(*students, Student{id: i, name: v})
	}
	fmt.Println(students)
}
func updateScore(student Student, score int) {
	student.score = score
}

func updateScorePtr(student *Student, score int) {
	student.score = score
}

func main() {
	s1 := createStudent1(1, "tom")
	s2 := createStudent2(2, "jerry")
	fmt.Println(s1, s2)

	updateScore(s1, 100)
	updateScore(*s2, 100)
	fmt.Println(s1, s2)

	updateScorePtr(&s1, 100)
	updateScorePtr(s2, 100)
	fmt.Println(s1, s2)

	ss1 := []Student{}
	createStudents1(ss1, "tom", "jerry")
	fmt.Println(ss1)

	ss2 := []*Student{}
	createStudents2(ss2, "tom", "jerry")
	fmt.Println(ss2)

	ss3 := []Student{}
	createStudents3(&ss3, "tom", "jerry")
	fmt.Println(ss3)

	ss4 := new([]Student)
	createStudents3(ss4, "tom", "jerry")
	fmt.Println(ss4)
}
```

---

## interface
