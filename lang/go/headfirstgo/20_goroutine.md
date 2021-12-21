# goroutine

## go

```go
	
func f(from string) {
    for i := 0; i < 3; i++ {
        fmt.Println(from, ":", i)
    }
}
go f("goroutine")

go func(msg string) {
    fmt.Println(msg)
}("go")
```

```go
func say(word string) {
	for i := 0; i < 10; i++ {
		time.Sleep(10 * time.Millisecond)
		fmt.Println(word)
	}
}
```

```go
func main() {
	say("hello")
	say("go")
	fmt.Println("end main()")
}
```

```go
func main() {
	go say("hello")
	say("go")
	fmt.Println("end main()")
}
```

```go
func main() {
	go say("hello")
	go say("go")
	fmt.Println("end main()")
}
```


---

### time.Sleep

```go
func say(word string) {
	for i := 0; i < 10; i++ {
		time.Sleep(10 * time.Millisecond)
		fmt.Println(word)
	}
}

func main() {
	go say("hello")
	go say("go")

    time.Sleep(2 * time.Second)

	fmt.Println("end main()")
}
```

---

### sync.WaitGroup

```go
func say(word string, wg *sync.WaitGroup) {
    defer wg.Done()

	for i := 0; i < 10; i++ {
		time.Sleep(10 * time.Millisecond)
		fmt.Println(word)
	}
}

func main() {
    wg := new(sync.WaitGroup)
    wg.Add(2)

    go say("world", wg)
    go say("go", wg)

    wg.Wait()

    fmt.Println("end main()")
}
```


---

### channel

```go
func say(word string, c chan struct{}) {
	for i := 0; i < 10; i++ {
		time.Sleep(10 * time.Millisecond)
		fmt.Println(word)
	}

	c <- struct{}{}
}

func main() {
	ch := make(chan struct{})

	go say("world", ch)
	go say("go", ch)

	<-ch
	<-ch

	fmt.Println("end main()")
}
```


---

## race condition

```go
total := 0
for i := 0; i < 1000; i++ {
	go func() {
		total++
	}()
}

time.Sleep(time.Second)
fmt.Println(total)
```

```bash
linux:~/hello $ go test -race
linux:~/hello $ go run -race
linux:~/hello $ go build -race
linux:~/hello $ go install -race
```


---

### sync.Mutex

```go
var mux sync.Mutex
total := 0
for i := 0; i < 1000; i++ {
	go func() {
		mux.Lock()
		total++
		mux.Unlock()
	}()
}

time.Sleep(time.Second)
fmt.Println(total)
```

```go
type SafeNumber struct {
	v   int
	mux sync.Mutex
}
total := SafeNumber{v: 0}

for i := 0; i < 1000; i++ {
	go func() {
		total.mux.Lock()
		total.v++
		total.mux.Unlock()
	}()
}

time.Sleep(time.Second)
fmt.Println(total.v)
```

---

### chan

```go
ch := make(chan int)
total := 0
sum := 0
for i := 0; i < 1000; i++ {
	go func() {
		total++
		ch <- total
	}()

	sum = <-ch
}

time.Sleep(time.Second)
fmt.Println(sum)
```

```go
total := 0
ch := make(chan int, 1)
ch <- total
for i := 0; i < 1000; i++ {
    go func() {
        ch <- <-ch + 1
    }()
}

time.Sleep(time.Second)
fmt.Println(<-ch)
```
