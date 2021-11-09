# method

## basic

```go
type rect struct {
	width, height int
}

func (r *rect) area() int {
	return r.width * r.height
}

func (r rect) perim() int {
	return 2*r.width + 2*r.height
}

func main() {
	r := rect{width: 10, height: 5}

	fmt.Println("area: ", r.area())
	fmt.Println("perim:", r.perim())

	rp := &r
	fmt.Println("area: ", rp.area())
	fmt.Println("perim:", rp.perim())
}
```


---

## getter and setter

```go
// lib/person.go
type Person struct {
	name string
	age  int
}

// getter
func (p *Person) Age() int {
	return p.age
}

// setter
func (p *Person) SetAge(a int) error {
	if a < 0 {
		return errors.New("invalid age")
	}
	p.age = a
	return nil
}

func PersonNew(name string, age int) Person {
	p := Person{name, age}
	return p
}
```

```go
func main() {
	// p := lib.Person{}
	p := lib.PersonNew("john", 1)
	fmt.Printf("%v\n", p)

	// getter
	fmt.Printf("%v\n", p.Age())

	// setter
	if e := p.SetAge(-1); e != nil {
		fmt.Printf("%v\n", e)
	}

	// p.age = -2
	// fmt.Printf("%v\n", p)
}
```
