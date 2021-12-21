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
	fmt.Println(n)			// map[bar:2 foo:1]

	doubleValue(n)
	fmt.Println(n)			// map[bar:4 foo:2]

	doublePointer(&n)
	fmt.Println(n)			// map[bar:8 foo:4]
}
```


---

## map to map

```go
mm0 := make(map[string]map[string]string)
mm0["one"] = map[string]string{"o": "a"}
fmt.Println("mm0", mm0)
mm1 := map[string]map[string]string{"a": {"aa": "aaa"}}
mm1["b"] = map[string]string{"bb": "bbb"}
fmt.Println("mm1", mm1)
```


---

## map to slice

```go
as0 := make(map[string][]string)
as0["one"] = []string{"o", "a"}
fmt.Println("am1", as0)
as1 := map[string][]string{"a": {"a", "1"}}
as1["b"] = []string{"b", "2"}
fmt.Println("am1", as1)
```


---

## slice to map

```go
sm0 := make([]map[string]int, 1)
sm0[0] = map[string]int{"one": 1}
fmt.Println("sm0", sm0)
sm1 := [](map[string]int){map[string]int{"a": 1}}
sm1 = append(sm1, map[string]int{"b": 2})
fmt.Println("sm1", sm1)
```
