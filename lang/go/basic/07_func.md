# func

## string format

```go
fmt.Printf("bool: %t\n", true)
fmt.Printf("int: %d\n", 123)
fmt.Printf("bin: %b\n", 14)
fmt.Printf("char: %c\n", 33)
fmt.Printf("hex: %x\n", 456)
fmt.Printf("float1: %f\n", 78.9)
fmt.Printf("float2: %e\n", 123400000.0)
fmt.Printf("float3: %E\n", 123400000.0)
fmt.Printf("str1: %s\n", "\"string\"")
fmt.Printf("str2: %q\n", "\"string\"")
fmt.Printf("str3: %x\n", "hex this")
fmt.Printf("pointer: %p\n", &p)
fmt.Printf("width1: |%6d|%6d|\n", 12, 345)
fmt.Printf("width2: |%6.2f|%6.2f|\n", 1.2, 3.45)
fmt.Printf("width3: |%-6.2f|%-6.2f|\n", 1.2, 3.45)
fmt.Printf("width4: |%6s|%6s|\n", "foo", "b")
fmt.Printf("width5: |%-6s|%-6s|\n", "foo", "b")

s := fmt.Sprintf("sprintf: a %s", "string")
fmt.Println(s)
fmt.Fprintf(os.Stderr, "io: an %s\n", "error")

type point struct {
	x, y int
}
p := point{1, 2}
fmt.Printf("struct1: %v\n", p)
fmt.Printf("struct2: %+v\n", p)
fmt.Printf("struct3: %#v\n", p)
fmt.Printf("type: %T\n", p)
```

---

## function

```go
func plus(a int, b int) int {
    return a + b
}

func plusPlus(a, b, c int) int {
    return a + b + c
}

func main() {
    res := plus(1, 2)
    fmt.Println("1+2 =", res)

res = plusPlus(1, 2, 3)
    fmt.Println("1+2+3 =", res)
}
```


---

## multiple return value

```go
func vals() (int, int) {
    return 3, 7
}

func main() {
    a, b := vals()
    fmt.Println(a)
    fmt.Println(b)

_, c := vals()
    fmt.Println(c)
}
```


---

## variadic function

```go
func sum(nums ...int) {
    fmt.Print(nums, " ")
    total := 0
    for _, num := range nums {
        total += num
    }
    fmt.Println(total)
}

func main() {
    sum(1, 2)
    sum(1, 2, 3)

    nums := []int{1, 2, 3, 4}
    sum(nums...)
}
```


---

## closure

```go
func intSeq() func() int {
    i := 0
    return func() int {
        i++
        return i
    }
}

func main() {
    nextInt := intSeq()

    fmt.Println(nextInt())
    fmt.Println(nextInt())
    fmt.Println(nextInt())

    newInts := intSeq()
    fmt.Println(newInts())
}
```


---

## recursion

```go
func fact(n int) int {
    if n == 0 {
        return 1
    }
    return n * fact(n-1)
}

func main() {
    fmt.Println(fact(7))

    var fib func(n int) int
    fib = func(n int) int {
        if n < 2 {
            return n
        }
        return fib(n-1) + fib(n-2)

    }
    fmt.Println(fib(7))
}
```


## pass function

```go
func plus(a int, b int) int {
	return a + b
}

func runFunc(a int, b int, f func(int, int) int) int {
	c := f(a, b)
	return c
}

func main() {
	a := 1
	b := 2
	c := runFunc(a, b, plus)
	fmt.Println(c)
}
```


```go
type plusFunc func(int, int) int

func plus(a int, b int) int {
	return a + b
}

func runFunc(a int, b int, f plusFunc) int {
	c := f(a, b)
	return c
}

func main() {
	a := 1
	b := 2
	c := runFunc(a, b, plus)
	fmt.Println(c)
}
```
