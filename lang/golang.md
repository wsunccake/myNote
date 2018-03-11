# Go

## Introduction


---

## Install

```bash
centos:~ # yum install golang
```


## Hello

```bash
centos:~ # hello.go
package main

import "fmt"

func main() {
    fmt.Println("Hello Go")
}

centos:~ # go run hello.go

centos:~ # go build hello.go
centos:~ # ./hello
```

---

## Variable

```
// var name type = expression
var i int = 1
var j = 100
var k int

// name := expression
l := 0
```

---

## Data Type

### String

```
var str1 string
str2 := "go"
```

---


## Reference

[Golang tutorial series](https://golangbot.com/learn-golang-series/)

[Go Tutorial](https://www.tutorialspoint.com/go/index.htm)