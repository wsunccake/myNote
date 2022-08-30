# goroutine

## channel

```go
package main

import (
	"fmt"
)

func chanFunc(n int, ch chan int) {
	for i := 0; i < n; i++ {
		ch <- i
		fmt.Printf("receive: channel <- %v\n", i)
		time.Sleep(time.Duration(10 * time.Millisecond))
	}
}

func main() {
	var chan1 chan int
	chan2 := make(chan int)
	fmt.Printf("chan1 type: %T, value: %v\n", chan1, chan1)
	fmt.Printf("chan2 type: %T, value: %v\n", chan2, chan2)

	// buffer
	chan3 := make(chan int, 1)

	// receive
	chan3 <- 1

	// send
	fmt.Println(<- chan3)

	chan4 := make(chan string)

	// chan4 <- "hello"

	// func () {
	// 	chan4 <- "hello"
	// }()

	go func () {
		chan4 <- "hello"
	}()

	val := <- chan4
	fmt.Println(val)

	chan5 := make(chan int)
	n := 5
	go chanFunc(n, chan5)
	for i:=0; i < n; i++ {
		fmt.Printf("send: %v <- channel\n", <- chan5)
	}
}
```


---

## range

```go
package main

import (
	"fmt"
)

func main() {}
	chan6 := make(chan int)
	go func() {
		for i:=0; i < 5; i++ {
			chan6 <- i
			fmt.Printf("recevei: channel <- %v\n", i)
		}
		close(chan6)
	}()

	for c := range chan6 {
		fmt.Println(c)
	}
}
```


---

## select

```go
package main

import (
	"fmt"
)

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


---

## arg

```go
package main

import (
	"fmt"
	"time"
)

func send(c chan<- int) {
	fmt.Printf("send: %T\n", c)
	c <- 1
}

func recv(c <-chan int) {
	fmt.Printf("recv: %T\n", c)
	fmt.Println(<-c)
}

func main() {
	c := make(chan int)
	fmt.Printf("%T\n", c)
	go send(c)
	go recv(c)
	time.Sleep(1 * time.Second)
}
```


---

## json

```go
package main

import (
	"encoding/json"
	"log"
	"os"
)

type Data struct {
	Id   int    `json:id`
	Name string `json: name`
}

func main() {
	arg1 := os.Args[1]
	data := Data{}

	if err := json.Unmarshal([]byte(arg1), &data); err == nil {
		log.Printf("data: %v", data)
		log.Print("id: ", data.Id, "name: ", data.Name)

		jsondata, _ := json.Marshal(data)
		log.Println(string(jsondata))
	} else {
		log.Print(err)
	}
}
```

```bash
linux:~ # go run main.go '{"id": 1, "name": "go"}'
```


---

## sync

```go
package main

import (
	"fmt"
	"sync"
	"time"
)

var wg = sync.WaitGroup{}

func f1() {
	for i := 0; i < 10; i++ {
		fmt.Println("f1,  ->", i)
		time.Sleep(time.Duration(5 * time.Millisecond))
	}
}

func f2() {
	for i := 0; i < 10; i++ {
		fmt.Println("f2,  ->", i)
		time.Sleep(time.Duration(10 * time.Millisecond))
	}
}

func f3() {
	for i := 0; i < 10; i++ {
		fmt.Println("f3,  ->", i)
		time.Sleep(time.Duration(5 * time.Millisecond))
	}
	wg.Done()
}

func f4() {
	for i := 0; i < 10; i++ {
		fmt.Println("f4,  ->", i)
		time.Sleep(time.Duration(10 * time.Millisecond))
	}
	wg.Done()
}

func main() {
	fmt.Println("no sync start")
	f1()
	f2()
	fmt.Println("no sync finish")

	fmt.Println("no sync start")
	go f1()
	f2()
	fmt.Println("no sync finish")
	fmt.Println("sync and delta: 1 start")
	wg.Add(1)
	go f3()
	go f4()
	wg.Wait()
	fmt.Println("sync and delta: 1 finish")

	fmt.Println("sync and delta: 2 start")
	wg.Add(2)
	go f3()
	go f4()
	wg.Wait()
	fmt.Println("sync and delta: 2 finish")
}
```

```go
package main

import (
	"fmt"
	"math/rand"
	"sync"
	"sync/atomic"
	"time"
)

var wait sync.WaitGroup
var count int64
var mutex sync.Mutex

func increment1(s string) {
	for i := 0; i < 10; i++ {
		x := count
		x++
		time.Sleep(time.Duration(rand.Intn(4)) * time.Millisecond)
		count = x
		fmt.Println(s, i, "Count: ", count)

	}
	wait.Done()
}

func increment2(s string) {
	for i := 0; i < 10; i++ {
		mutex.Lock()
		x := count
		x++
		time.Sleep(time.Duration(rand.Intn(4)) * time.Millisecond)
		count = x
		mutex.Unlock()
		fmt.Println(s, i, "Count: ", count)
	}
	wait.Done()
}

func increment3(s string) {
	for i := 0; i < 10; i++ {
		time.Sleep(time.Duration((rand.Intn(4))) * time.Millisecond)
		atomic.AddInt64(&count, 1)
		fmt.Println(s, i, "Count ->", count)
	}
	wait.Done()
}

func main() {
	count = 0
	wait.Add(2)
	go increment1("foo: ")
	go increment1("bar: ")
	wait.Wait()
	fmt.Println("Last Count:", count)

	count = 0
	wait.Add(2)
	go increment2("foo: ")
	go increment2("bar: ")
	wait.Wait()
	fmt.Println("Last Count:", count)

	count = 0
	wait.Add(2)
	go increment3("foo: ")
	go increment3("bar: ")
	wait.Wait()
	fmt.Println("Last Count:", count)
}
```
