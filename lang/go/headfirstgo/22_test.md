# test

```bash
linux:~/hello $ go mod init hello
linux:~/hello $ go mod tidy
linux:~/hello $ tree
.
├── go.mod
├── lib
│   └── lib.go
├── test
│   └── lib_test.go
└── main.go
```

```go
// lib.go
// package description ...
package lib

// func description ...
func Plus(a int, b int) int {
	return a + b
}

func Multiply(a int, b int) int {
	return a * b
}
```

```go
// main.go
package main

import (
	"fmt"
	"hello/lib"
)

func main() {
	a := 1
	b := 2
	c := lib.Plus(a, b)
	fmt.Println(c)
}
```

```go
package test

import (
	"fmt"
	"hello/lib"
	"testing"
)

func TestPlus(t *testing.T) {
	if lib.Plus(1, 2) != 3 {
		t.Error("fail")
	}
}

func TestMultiply(t *testing.T) {
	if lib.Multiply(1, 2) != 2 {
		t.Error("fail")
	}
}

func BenchmarkPlus(b *testing.B) {
	for i := 0; i < b.N; i++ {
		lib.Plus(1, 2)
	}
}

func TestMain(m *testing.M) {
	fmt.Println("setup")
	m.Run()
	fmt.Println("teardown")
}
```

```bash
linux:~/hello $ go test ./...
linux:~/hello $ go test -v test/lib_test.go
linux:~/hello $ go test -v --run ^TestPlus$ test/lib_test.go

linux:~/hello $ go test -timeout 30s -run ^TestPlus$ hello/test

linux:~/hello $ go test -benchmem -run=^$ -bench BenchmarkPlus hello/test
linux:~/hello $ go test -v -bench BenchmarkPlus -benchtime=5s hello/test

linux:~/hello $ go test -timeout 30s -run ^TestMain$ hello/test
```
