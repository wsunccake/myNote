# map

## basic

```go
	m := make(map[string]int)
	m["k1"] = 7
	m["k2"] = 13
	fmt.Println("map:", m)          // map[k1:7 k2:13]

	v1 := m["k1"]
	fmt.Println("v1: ", v1)         // 7
	fmt.Println("len:", len(m))     // 2

	delete(m, "k2")
	fmt.Println("map:", m)          // map[k1:7]

	_, prs := m["k2"]
	fmt.Println("prs:", prs)        // false

	n := map[string]int{"foo": 1, "bar": 2}
	fmt.Println("map:", n)          // map[bar:2 foo:1]
```


---

## for range

```go
n := map[string]int{"foo": 1, "bar": 2}
for k, v := range n {
	fmt.Println(k, v)
}
```


---

## function

```go
func doubleValue(a map[string]int) {
	for k, v := range a {
		a[k] = v * 2
	}
}

func doublePointer(a *map[string]int) {
	for k, v := range *a {
		(*a)[k] = v * 2
	}
}

func main() {
	n := map[string]int{"foo": 1, "bar": 2}
	fmt.Println(n)

	doubleValue(n)
	fmt.Println(n)

	doublePointer(&n)
	fmt.Println(n)
}
```
