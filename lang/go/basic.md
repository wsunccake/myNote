# go

## introduction


---

## install

```bash
centos:~ # yum install golang
centos:~ # go env
```


---

## hello

```bash
linux:~ # hello.go
package main

import "fmt"

func main() {
    fmt.Println("Hello Go")
}

# run
linux:~ # go run hello.go

# compile to binary
linux:~ # go build hello.go
linux:~ # ./hello
```


---

## project

### simple

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # vi main.go
package main

func main() {
	println("Hello go")
}

# run with source
linux:~/project # go run main.go

# build binary
linux:~/project # export GOBIN=~/project/bin
linux:~/project # go install
linux:~/project # ls $GOBIN

# run with binary
linux:~/project # ./bin/project

linux:~/project # tree
.
├── bin
│   └── project
└── main.go
```


### import

```bash
linux:~/project # mkdir -p src/hello
linux:~/project # vi src/hello/myFunc.go
package hello

func Hello() {
	println("Hello GO")
}

func Hi() string {
	return "Hi GO"
}

linux:~/project # vi main.go
package main

import "hello"

func main() {
    println("Hello go")
    hello.Hello()
}

# run with source
linux:~/project # export GOPATH=~/project
linux:~/project # go run main.go

# build binary
linux:~/project # export GOBIN=~/project/bin
linux:~/project # go install
linux:~/project # ls $GOBIN

# run with binary
linux:~/project # ./bin/project

linux:~/project # tree
.
├── bin
│   └── project
├── main.go
└── src
    └── hello
        └── myFunc.go
```


### test

```bash
linux:~/project # vi hello_test.go
package main

import "testing"
imrpot "hello"

func TestHello(t *testing.T) {
	if hello.Hi() != "Hi Go" {
		t.Error("fail")
	}
}

# test
linux:~/project # export GOPATH=~/project
linux:~/project # go test

linux:~/project # tree
.
├── bin
│   └── project
├── hello_test.go
├── main.go
└── src
    └── hello
        └── myFunc.go
```

---

## variable

```go
package main

import "fmt"

func main() {
    // var name type = expression
    var i int
    i = 1
    var j int = 1
    var k = 1

    // name := expression
    l := 1

    // const
    const PI = 3.14
    // PI = 3.0
	r := 10.0
	fmt.Printf("Circle are: %f\n", PI * r * r)
}
```

---

## data type

```go
package main

import "fmt"

func main() {
	var b bool
	var i int
	var f float32
	var s string

	fmt.Printf("default %T: %t\n", b, b)
	fmt.Printf("default %T: %d\n", i, i)
	fmt.Printf("default %T: %f\n", f, f)
	fmt.Printf("default %T: %s\n", s, s)
}
```


---

## condition


### if

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	fmt.Print("input m/f: ")
	reader := bufio.NewReader(os.Stdin)
	text, _ := reader.ReadString('\n')
	text = strings.TrimSuffix(text, "\n")

	if text == "m" {
		fmt.Println("Male")
	} else if text == "f" {
		fmt.Println("Female")
	} else {
		fmt.Println("Unknown")
	}
}
```

### switch


```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	fmt.Print("input m/f: ")
	reader := bufio.NewReader(os.Stdin)
	text, _ := reader.ReadString('\n')
	text = strings.TrimSuffix(text, "\n")

	switch text {
	case "m":
		fmt.Println("Male")
	case "f":
		fmt.Println("Female")
	default:
		fmt.Println("Unknown")
	}
}
```


---

## loop


### for

```go
package main

import (
	"fmt"
)

func main() {
	const MAX int = 5
	for i:=0; i < MAX; i++ {
		fmt.Println(i)
	}

	i := 0
	for true {
		fmt.Println(i)
		i++
		if i >= MAX {
			break
		}
    }
    
    for i, v := range [MAX]int{1, 4, 5, 9} {
		fmt.Println(i, v)
	}
}
```


### goto

```go
package main

import (
	"fmt"
)

func main() {
	const MAX int = 5
	i := 0
	LOOP: fmt.Println(i)
	i++
	if i < MAX {
		goto LOOP
	}
}
```


---

## function

```go
package main

import "fmt"

func max(x, y int) int{
	var temp int

	if x > y {
		temp = x
	} else {
		temp = y
	}
	
	return temp
}

func main() {
	fmt.Printf("max: %d\n", max(5, 10))
}
```

```go
package main

import "fmt"

func main() {
	a := 1
	b := 2

	fmt.Printf("before swap %d, %d\n", a, b)
	swap1(a, b)
	fmt.Printf("after swap %d, %d\n", a, b)

	fmt.Printf("before swap %d, %d\n", a, b)
	swap2(&a, &b)
	fmt.Printf("after swap %d, %d\n", a, b)
}

// call by value
func swap1(x, y int) {
	var temp int
	temp = x
	x = y
	y = temp
}

// call by address
func swap2(x, y *int) {
	var temp int
	temp = *x
	*x = *y
	*y = temp
}
```


### function variable / anonymous function

```go
package main

type add func(a int, b int) int

func addTemp() func(x, y int) int {
	f := func(x, y int) int {
		println(x, "+", y)
		return x + y
	}
	return f
}

func simple(c func(a, b int) int) {
	println("run function variable as argument", c(60, 7))
}

func main() {
	// first order function
	func (x, y int) int {
		println(x, "+", y)
		return x + y
	}(0, 3)

	add1 := func (x, y int) int {
		println(x, "+", y)
		return x + y
	}
	add1(1, 2)

	var add2 add = func (x, y int) int {
		println(x, "+", y)
		return x + y
	}
	add2(2, 4)

	add3 := addTemp()
	add3(1, 9)

    // high order function
	simple(func (x, y int) int {
		println(x, "+", y)
		return x + y
	})
	simple(add1)
	simple(add2)
	simple(add3)
}
```


---

## string

```go
package main

import (
	"fmt"
	"reflect"
	"strings"
)

func main() {
	var str string = "Hello Go"
	fmt.Println(str)
	fmt.Println("type: ", reflect.TypeOf(str))
	fmt.Println("length: ", len(str))
	fmt.Println("A ascii: ", "A"[0])

	fmt.Println("upper: ", strings.ToUpper(str))
	fmt.Println("lower: ", strings.ToLower(str))
	fmt.Println("has prefix: ", strings.HasPrefix(str,"hello"))
	fmt.Println("has suffix: ", strings.HasSuffix(str,"go"))

	lang := []string{"C", "C++", "Go"}
	fmt.Println(lang)
	fmt.Println("join: ", strings.Join(lang, ","))

	csvStr := "C,C++,Go"
	fmt.Println(csvStr)
	fmt.Println("split", strings.Split(csvStr, ","))
}
```


---

## regex

```go
package main

import (
	"fmt"
	"regexp"
)

func main() {
	str := "/usr/lib/python2.6/site-packages/gtk-2.0/gconf.so"

	re1, _ := regexp.Compile(`(.*)\.(.*?)$`)
	res1 := re1.FindAllStringSubmatch(str, -1)
	fmt.Printf("%+v\n", res1)
	for _, e := range res1 {
		fmt.Println("match: ", e[0])
		fmt.Println("group1: ",e[1])
		fmt.Println("group2: ",e[2])
	}

	re2, _ := regexp.Compile(`(.*?)\.(.*)`)
	res2 := re2.FindAllStringSubmatch(str, -1)
	fmt.Printf("%+v\n", res2)
	for _, e := range res2 {
		fmt.Println("match: ", e[0])
		fmt.Println("group1: ",e[1])
		fmt.Println("group2: ",e[2])
	}

	re3, _ := regexp.Compile(`(.*?)/(.*)`)
	res3 := re3.FindAllStringSubmatch(str, -1)
	fmt.Printf("%+v\n", res3)
	for _, e := range res3 {
		fmt.Println("match: ", e[0])
		fmt.Println("group1: ",e[1])
		fmt.Println("group2: ",e[2])
	}

	re4, _ := regexp.Compile(`(.*)/(.*)`)
	res4 := re4.FindAllStringSubmatch(str, -1)
	fmt.Printf("%+v\n", res4)
	for _, e := range res4 {
		fmt.Println("match: ", e[0])
		fmt.Println("group1: ",e[1])
		fmt.Println("group2: ",e[2])
	}

	re5, _ := regexp.Compile(`/python.*/`)
	res5 := re5.FindString(str)
	fmt.Println("greedy: ", res5)

	re6, _ := regexp.Compile(`/python.*?/`)
	res6 := re6.FindString(str)
	fmt.Println("lazy: ", res6)

}
```


---

## array

```go
package main

func main() {
    var arr1 = [3]int{1, 2, 3}
    var arr2 = []int {4, 5, 6}
    var arr3 [3]int
    arr3[0] = 7
    arr3[1] = 8
    arr3[2] = 9
    var i int
    
    for i, e := range(arr1) {
        println(i, e)
    }

    for i := range arr2 {
        println(i)
    }

    for i = 0; i < 3; i++ {
        println(i, arr3[i])
    }
}
```


### function

```go
package main

func showArray(array []int) {
    for i, e := range array {
        println(i, e)
    }
}

func main() {
    var arr = []int {4, 5, 6}
    showArray(arr)
}
```


### 2d

```go
package main

func main() {
    var arr2d = [2][3]int{{1, 2, 3}, {4, 5, 6}}
    for i1, e1 := range(arr2d) {
        for i2, e2 := range e1 {
            println(i1 ,i2, e2)
        }
    }
}
```


### slice

```go
package main

import (
	"fmt"
)

func main() {
	odds := []int{2, 4, 6, 8, 10}
	o1 := odds[1:3]
	o2 := odds[:2]
	o3 := odds[3:]
	o4 := odds[3]
	fmt.Println(o1, o2, o3, o4)

	names := []string{"Finn", "LPJ", "Tino"}
	n1 := names[0]
	fmt.Println(n1, n1[2:], n1[:], n1[1:3])
```


### make, append

```go
package main

import (
	"fmt"
	"reflect"
)

func main() {
	a1 := []int{1, 2, 3}
	fmt.Println(reflect.TypeOf(a1), a1, len(a1), cap(a1))
	//a1[3] = 4
	a1 = append(a1, 4)
	fmt.Println(a1, len(a1), cap(a1))
	a1[3] = 1
	fmt.Println(a1, len(a1), cap(a1))

	a2 := [5]int{1, 2, 3}
	fmt.Println(reflect.TypeOf(a2), a2, len(a2), cap(a2))
	//a2[5] = 1
	//a2 = append(a2, 4)

	a3 := make([]int, 3, 10)
	fmt.Println(reflect.TypeOf(a3), a3, len(a3), cap(a3))
	//a3[3]=1
	a3 = append(a3, 3)
	fmt.Println(a3, len(a3), cap(a3))
}
```


### array / slice to slice

```go
package main

import (
	"fmt"
)

func main() {
	array1 := [5]int{1, 2, 3, 4, 5}
	slice1 := array1[2:4]

	fmt.Printf("array: %+v\n", array1)
	fmt.Printf("array len: %d, cap: %d\n", len(array1), cap(array1))
	fmt.Printf("slice: %+v\n", slice1)
	fmt.Printf("slice len: %d, cap: %d\n", len(slice1), cap(slice1))

	fmt.Println("change slice...")
	slice1[1] = 22
	fmt.Printf("array: %+v\n", array1)
	fmt.Printf("slice: %+v\n", slice1)

	fmt.Println("append slice...")
	slice1 = append(slice1, 33)
	fmt.Printf("array: %+v\n", array1)
	fmt.Printf("slice: %+v\n", slice1)
	fmt.Printf("slice len: %d, cap: %d\n", len(slice1), cap(slice1))

	fmt.Println("append slice...")
	slice1 = append(slice1, 44)
	fmt.Printf("array: %+v\n", array1)
	fmt.Printf("slice: %+v\n", slice1)
	fmt.Printf("slice len: %d, cap: %d\n", len(slice1), cap(slice1))

	fmt.Println("change slice...")
	slice1[1] = 2222
	fmt.Printf("array: %+v\n", array1)
	fmt.Printf("slice: %+v\n", slice1)
}
```

---

## map

```go
package main

import "fmt"

func main() {
	var countryCapitalMap map[string]string
	countryCapitalMap = make(map[string]string)

	countryCapitalMap["France"] = "Paris"
	countryCapitalMap["Italy"] = "Rome"
	countryCapitalMap["Japan"] = "Tokyo"

	weekDay := map[string]string{
		"sun": "Sunday",
		"mon": "Monday",
		"tues": "Tuesday",
		"wed": "Wednesday",
		"thurs": "Thursday",
		"fri": "Friday",
		"sat": "Saturday"}

	delete(countryCapitalMap, "Italy")

	for k, v := range countryCapitalMap {
		fmt.Printf("%s -> %s\n", k, v)
	}


	k := "abc"
	v, ok := weekDay[k]
	if ok {
		fmt.Println(k, "->", v)
	} else {
		fmt.Println("no found", k)
	}
}
```


---

## pointer

```go
package main

import "fmt"

func main() {
	var v1 int = 20
	var p1 *int
	p1 = &v1
	var p2 *int = &v1
	p3 := &v1
	p4 := new(int)
	p4 = &v1
	fmt.Printf("value v1: %d, *p1: %d, *p2: %d, *p3: %d, *p4: %d\n", v1, *p1, *p2, *p3, *p4)
	fmt.Printf("addres &v1: %x, p1: %x, p2: %x, p3: %x, p4: %x\n", &v1, p1, p2, p3, p4)
}
```


---

## struct

```go
package main

import "fmt"

type Person struct {
	name string
	age int
}

type Employee struct {
	Person
	int
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
	fmt.Println(e1.name, e1.age, e1.int)
}
```


### function / method

```go
package main

import "fmt"

type Person struct {
	name string
	age int
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


---

## interface

```go
package main

import "fmt"

type vehicle interface {
	accelerate()
}

func describe(v vehicle)  {
	fmt.Printf("%+v\n", v)
	v.accelerate()
}

type Car struct {
	vendor string
	color string
}

func (c Car) accelerate() {
	fmt.Println("10 m/s")
}

type Toyota struct {
	Car
	model string
}

type BMW struct {
	Car
	model string
}

func (b BMW) accelerate() {
	fmt.Println("100 m/s")
}

func main() {
	c := Car{"unknown", "black"}
	describe(c)

	t := Toyota{Car{"toyota", "white"}, "ae86"}
	describe(t)

	b := BMW{Car{"bmw", "white"}, "m3"}
	describe(b)
}
```


### switch

```go
package main

import "fmt"

func do(i interface{}) {
	switch v := i.(type) {
	case int:
		fmt.Printf("Twice %v is %v\n", v, v*2)
	case string:
		fmt.Printf("%q is %v bytes long\n", v, len(v))
	default:
		fmt.Printf("I don't know about type %T!\n", v)
	}
}

func main() {
	do(21)
	do("hello")
	do(true)
}
```

---

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


### range

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


### select

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


### arg

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

## dynamic call

```go
package main

import (
	"fmt"
	"os"
)

var funcMap = map[string]interface{} {
	"hi":    hi,
	"hello": hello,
}

func hi() {
	fmt.Print("Hi Go")
}

func hello(name string) string{
	return fmt.Sprintf("hello %v", name)
}

func callDynamically(name string, args ...interface{}) {
	switch name {
	case "hi":
		funcMap["hi"].(func())()
	case "hello":
		sentence := funcMap["hello"].(func(string) string)(args[0].(string))
		fmt.Println(sentence)
	}

}

func main() {
	arg1 := os.Args[1]
	arg2 := ""
	if len(os.Args) > 2 {
		arg2 = os.Args[2]
	}

	fmt.Printf("arg1: %v, arg2: %v\n", arg1, arg2)
	callDynamically(arg1, arg2)
}
```

```bash
linux:~ # go run main.go hi
linux:~ # go run main.go heloo go
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


---

## reference

[Golang tutorial series](https://golangbot.com/learn-golang-series/)

[Go Tutorial](https://www.tutorialspoint.com/go/index.htm)

[Go Bootcamp](http://www.golangbootcamp.com/book/frontmatter)

[cyent/golang](https://cyent.github.io/golang/)
