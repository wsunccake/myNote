# run

## install

```bash
centos:~ # yum install golang
centos:~ # go env
```


---

## hello

```bash
linux:~ $ hello.go
package main

import "fmt"

func main() {
    fmt.Println("Hello Go")
}

# run
linux:~ $ go run hello.go

# compile to binary
linux:~ $ go build hello.go
linux:~ $ ./hello
```


---

## project

### simple

```bash
linux:~ $ mkdir project
linux:~ $ cd project
linux:~/project $ vi main.go
package main

func main() {
	println("Hello go")
}

# run with source
linux:~/project $ go run main.go

# build binary
linux:~/project $ export GOBIN=~/project/bin
linux:~/project $ go install
linux:~/project $ ls $GOBIN

# run with binary
linux:~/project $ ./bin/project

linux:~/project $ tree
.
├── bin
│   └── project
└── main.go
```


### import

```bash
linux:~/project $ mkdir -p src/hello
linux:~/project $ vi src/hello/myFunc.go
package hello

func Hello() {
	println("Hello GO")
}

func Hi() string {
	return "Hi GO"
}

linux:~/project $ vi main.go
package main

import "hello"

func main() {
    println("Hello go")
    hello.Hello()
}

# set env
linux:~/project $ export GOPATH=~/project
linux:~/project $ export GOBIN=~/project/bin

# download package
linux:~/project $ go get

# run with source
linux:~/project $ go run main.go

# build binary
linux:~/project $ go install
linux:~/project $ ls $GOBIN

# run with binary
linux:~/project $ ./bin/project

linux:~/project $ tree
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
linux:~/project $ vi hello_test.go
package main

import "testing"
imrpot "hello"

func TestHello(t *testing.T) {
	if hello.Hi() != "Hi Go" {
		t.Error("fail")
	}
}

# test
linux:~/project $ export GOPATH=~/project
linux:~/project $ go test

linux:~/project $ tree
.
├── bin
│   └── project
├── hello_test.go
├── main.go
└── src
    └── hello
        └── myFunc.go
```
