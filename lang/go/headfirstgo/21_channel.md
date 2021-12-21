# channel

## chan

```go
messages := make(chan string)
go func() { messages <- "ping" }()
msg := <-messages
fmt.Println(msg)
```


---

## unbuffer 

unbuffer -> non blocking

```go
msg := make(chan string)
msg <- "0"
fmt.Println(<-msg)
msg <- "1"
fmt.Println(<-msg)
```

```go
msg := make(chan string)
fmt.Println(<-msg)
msg <- "0"
fmt.Println(<-msg)
msg <- "1"
```

```go
c := make(chan bool)
go func() {
	fmt.Println("GO GO GO")
	c <- true
}()
<-c
```

```go
c := make(chan bool)
go func() {
	fmt.Println("GO GO GO")
	<-c
}()
c <- true
```


---

## buffer

buffer -> blocking

buffer size = 1

```go
msg := make(chan string, 1)
msg <- "0"
fmt.Println(<-msg)
msg <- "1"
fmt.Println(<-msg)
```

```go
msg := make(chan string, 1)
msg <- "0"
msg <- "1"
fmt.Println(<-msg)
fmt.Println(<-msg)
```

```go
msg := make(chan string, 1)
fmt.Println(<-msg)
msg <- "0"
fmt.Println(<-msg)
msg <- "1"
```

```go
c := make(chan bool, 1)
go func() {
	fmt.Println("GO GO GO")
	c <- true
}()
<-c
```

```go
c := make(chan bool, 1)
go func() {
	fmt.Println("GO GO GO")
	<-c
}()
c <- true
```

buffer size = 2

```go
msg := make(chan string, 2)
msg <- "0"
fmt.Println(<-msg)
msg <- "1"
fmt.Println(<-msg)
```

```go
msg := make(chan string, 2)
msg <- "0"
msg <- "1"
fmt.Println(<-msg)
fmt.Println(<-msg)
```

```go
msg := make(chan string, 2)
fmt.Println(<-msg)
msg <- "0"
fmt.Println(<-msg)
msg <- "1"
```

```go
c := make(chan bool, 2)
go func() {
	fmt.Println("GO GO GO")
	c <- true
}()
<-c
```

```go
c := make(chan bool, 2)
go func() {
	fmt.Println("GO GO GO")
	<-c
}()
c <- true
```

---

## direction

```go
func ping(pings chan<- string, msg string) {
	pings <- msg
}

func pong(pings <-chan string, pongs chan<- string) {
	msg := <-pings
	pongs <- msg
}
func main() {
	pings := make(chan string, 1)
	pongs := make(chan string, 1)
	ping(pings, "passed message")
	pong(pings, pongs)
	fmt.Println(<-pongs)
}
```


---

## close

```go
msg := make(chan string)

go func() {
	result, isExist := <-msg
	fmt.Println("goroutine:", result, isExist)
}()

msg <- "hello go"
close(msg)
// msg <- "hello go"
// close(msg)

time.Sleep(2 * time.Second)
fmt.Println("end main()")
```

```go
jobs := make(chan int, 5)
done := make(chan bool)

go func() {
	for {
		j, more := <-jobs
		if more {
			fmt.Println("received job", j)
		} else {
			fmt.Println("received all jobs")
			done <- true
			return
		}
	}
}()

for j := 1; j <= 3; j++ {
	jobs <- j
	fmt.Println("sent job", j)
}
close(jobs)
fmt.Println("sent all jobs")

<-done
```


---

## range

```go
queue := make(chan string, 2)
queue <- "one"
queue <- "two"

for elem := range queue {
	fmt.Println(elem)
}
```

```go
queue := make(chan string, 2)
queue <- "one"
queue <- "two"
close(queue)

for elem := range queue {
	fmt.Println(elem)
}
```

```go
queue := make(chan string, 2)
queue <- "one"
queue <- "two"
close(queue)

for {
	res, ok := <-queue
	if is {
		fmt.Println("value:", res, ok)
	} else {
		fmt.Println("close:", res, ok)
		return
	}
}
```


---

## select

```go
func receive(ch1, ch2, ch3, quit chan int) {
	for i := 0; i < 2; i++ {
		fmt.Printf("receive %d from ch1\n", <-ch1)
		fmt.Printf("receive %d from ch2\n", <-ch2)
		fmt.Printf("receive %d from ch3\n", <-ch3)
	}
	quit <- 0
}

func send(ch1, ch2, ch3, quit chan int) {
	for i := 0; i < 10; i++ {
		select {
		case ch1 <- i:
			fmt.Printf("send %d to ch1\n", i)
		case ch2 <- i:
			fmt.Printf("send %d to ch2\n", i)
		case ch3 <- i:
			fmt.Printf("send %d to ch3\n", i)
		case <-quit:
			fmt.Println("quit")
			return
		}
	}
}

func main() {
	ch1 := make(chan int)
	ch2 := make(chan int)
	ch3 := make(chan int)
	quit := make(chan int)
	go receive(ch1, ch2, ch3, quit)
	send(ch1, ch2, ch3, quit)
}
```
