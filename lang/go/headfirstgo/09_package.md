# package

## go doc

```go
// main.go
package main

import (
	"fmt"
	"hello/lib"
	// . "hello/lib"
	// helloLib "hello/lib"
)

func main() {
	a := 1
	b := 2
	c := lib.Plus(a, b)
	fmt.Println(c)
}
```


```go
// lib.go
// package description ...
package lib

// func description ...
func Plus(a int, b int) int {
	return a + b
}
```


```bash
linux:~ $ go doc lib
linux:~ $ go doc lib.Plus
```


---

## GOPATH

```bash
linux:~ $ go env GO111MODULE    # off | auto
linux:~ $ go env -w GO111MODULE=auto
linux:~ $ go env -w GO111MODULE=off

linux:~ $ ls $(go env GOPATH)/src/hello/lib/lib.go
linux:~/hello $ tree
.
└── main.go
```


---

## GO111MODULE

```bash
linux:~ $ go env GO111MODULE    # on | auto
linux:~ $ go env -w GO111MODULE=auto
linux:~ $ go env -w GO111MODULE=on

linux:~/hello $ go mod init hello
linux:~/hello $ go mod tidy
linux:~/hello $ tree
.
├── go.mod
├── lib
│   └── lib.go
└── main.go
```
