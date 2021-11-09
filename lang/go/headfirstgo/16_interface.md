# interface

```go
type person struct {
	name string
	age  int
}

type employee struct {
	person
	salary int
}

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
