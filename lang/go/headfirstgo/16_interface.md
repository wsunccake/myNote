# interface

## interface

```go
type Cat struct {
	name string
}

func (c Cat) MakeSound() string {
	return "meow"
}

func (c Cat) String() string {
	return fmt.Sprintf("Cat: %s", c.name)
}

type Dog struct {
	name string
}

func (d Dog) MakeSound() string {
	return "woof"
}

func (d Dog) String() string {
	return fmt.Sprintf("Dog: %s", d.name)
}

// interface
type Sound interface {
	MakeSound() string
}

func MakeSound(s Sound) {
	fmt.Println(s.MakeSound())
}

func main() {
	cat := Cat{"kitty"}
	MakeSound(cat)		// meow
	fmt.Println(cat)	// Cat: kitty

	dog := Dog{"snoopy"}
	MakeSound(dog)		// woof
	fmt.Println(dog)	// Dog: snoopy
}
```


---

## anonymous interface

```go
type person struct {
	name string
	age  int
}

type employee struct {
	person
	salary int
}

// anonymous interface
func printInfo(p interface{ getName() string }) {
	fmt.Println("name: ", p.getName())
}

func (p person) getName() string {
	return p.name
}

func main() {
	bob := person{"Bob", 20}
	printInfo(bob)

	mary := employee{person{"Mary", 24}, 2000}
	printInfo(mary)
}
```


---

## type assertion

```go
type Cat struct {
	name string
}

func (c Cat) MakeSound() string {
	return "meow"
}

func (c Cat) String() string {
	return fmt.Sprintf("Cat: %s", c.name)
}

func (c Cat) Eat() string {
	return "fish"
}

type Dog struct {
	name string
}

func (d Dog) MakeSound() string {
	return "woof"
}

func (d Dog) String() string {
	return fmt.Sprintf("Dog: %s", d.name)
}

func (d Dog) Chase() string {
	return "chasing cat"
}

type Sound interface {
	MakeSound() string
}

func MakeSound(s Sound) {
	fmt.Println(s.MakeSound())
}

func CreateDogOrCat(s string, name string) Sound {
	var i Sound
	switch {
	case s == "dog":
		i = Dog{name}
	case s == "cat":
		i = Cat{name}
	}
	return i
}

func main() {
	cat := CreateDogOrCat("cat", "kitty")
	MakeSound(cat)
	fmt.Println(cat)
	c := cat.(Cat)
	fmt.Println(c.Eat())

	dog := CreateDogOrCat("dog", "snoopy")
	MakeSound(dog)
	fmt.Println(dog)
	fmt.Println(dog.(Dog).Chase())
}
```
