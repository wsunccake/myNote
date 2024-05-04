# go - ready

## content

- [prepare](#prepare)
  - [install](#install)
  - [gvm](#gvm)
- [editor](#editor)
- [command](#command)
- [hello](#hello)
  - [start](#start)
  - [add external package](#add-external-package)
- [module](#module)
  - [start](#start-1)
  - [test](#test)
  - [call from anther](#call-from-anther)
- [multi-module](#multi-module)
  - [start](#start-2)
  - [create workspace](#create-workspace)
  - [download and modify external module](#download-and-modify-external-module)
- [other command](#other-command)

---

## prepare

### install

```bash
# for rhel / centos / fedora
linux:~ # yum install golang
linux:~ # dnf install golang

# for debian / ubuntu
linux:~ # apt install golang

# for binary
linux:~ # curl -OL https://go.dev/dl/go1.21.4.linux-amd64.tar.gz
linux:~ # tar -xzf go1.21.4.linux-amd64.tar.gz -C /usr/local
linux:~ # ln -s /usr/local/go/bin/go /usr/local/bin/.
```

### gvm

go version management

```bash
# for rhel / centos / fedora
linux:~ # yum install bison
linux:~ # dnf install bison

# for debian / ubuntu
linux:~ # apt install bison

linux:~ $ bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
linux:~ $ source /home/$(whoami)/.gvm/scripts/gvm
```

```bash
linux:~ $ gvm help
linux:~ $ gvm install go1.21.1 [--binary]
linux:~ $ gvm uninstall go1.21.1

linux:~ $ gvm list
linux:~ $ gvm use go1.21.1 [--default]
```

---

## editor

---

## command

```text
go help
go version
go install
go run <file>.go
go build
go test
go env [-w <GO_VAR>=<value> | -w <GO_VAR>]
```

---

## hello

require go version >= 1.11

### start

```go
// hello.go
package main

import "fmt"

func main() {
    fmt.Println("Hello Go")
}
```

```bash
linux:~ $ mkdir hello
linux:~ $ cd $_

# init module
linux:~/hello $ go mod init example/hello
linux:~/hello $ cat go.mod
linux:~/hello $ vi hello.go

# compile and run
linux:~/hello $ go run hello.go

# compile
linux:~/hello $ go build -o hello hello.go
linux:~/hello $ ./hello
```

### add external package

```go
// hello.go
package main

import "fmt"
import "rsc.io/quote"

func main() {
	fmt.Println("Hello Go")
    fmt.Println(quote.Go())
}
```

```bash
linux:~/hello $ go mod tidy
linux:~/hello $ cat go.mod

linux:~/hello $ go run .
```

---

## module

### start

```go
// greetings.go
package greetings

import "fmt"

func Hello(name string) string {
    message := fmt.Sprintf("Hi, %v. Welcome!", name)
    return message
}
```

```bash
linux:~ $ mkdir greetings
linux:~ $ cd $_

linux:~/greetings $ go mod init example.com/greetings
linux:~/greetings $ vi greetings.go
```

### test

```go
// greetings_test.go
package greetings

import (
    "testing"
    "regexp"
)

func TestHelloName(t *testing.T) {
    name := "Gladys"
    want := regexp.MustCompile(`\b`+name+`\b`)
    msg, err := Hello("Gladys")
    if !want.MatchString(msg) || err != nil {
        t.Fatalf(`Hello("Gladys") = %q, %v, want match for %#q, nil`, msg, err, want)
    }
}
```

```bash
linux:~/greetings $ vi greetings.go
linux:~/greetings $ go test
```

### call from anther

```go
// hello.go
package main

import (
    "fmt"
    "example.com/greetings"
)

func main() {
    message := greetings.Hello("Gladys")
    fmt.Println(message)
}
```

```bash
linux:~ $ mkdir hello
linux:~ $ cd $_

linux:~/hello $ go mod init example.com/hello
linux:~/hello $ vi hello.go
linux:~/hello $ go mod edit -replace example.com/greetings=../greetings
linux:~/hello $ go mod tidy

linux:~/hello $ go run .

linux:~/hello $ go build

linux:~/hello $ go list
linux:~/hello $ go list -f '{{.Target}}'
linux:~/hello $ go env -w GOBIN=<path>
linux:~/hello $ go env -w GOPATH=<path>
linux:~/hello $ export GOPATH=<path>

linux:~/hello $ go install

linux:~/hello $ ls $GOBIN
linux:~/hello $ ls $GOPATH/bin
```

---

## multi-module

require go version >= 1.18

## start

```go
// hello.go
package main

import (
    "fmt"
    "golang.org/x/example/hello/reverse"
)

func main() {
    fmt.Println(reverse.String("Hello"))
}
```

```bash
linux:~ $ mkdir workspace
linux:~ $ cd $_

linux:~/workspace $ mkdir hello
linux:~/workspace $ cd $_
linux:~/workspace/hello $ go mod init example.com/hello
linux:~/workspace/hello $ go get golang.org/x/example/hello/reverse
linux:~/workspace/hello $ vi hello.go

linux:~/workspace/hello $ go run .
```

### create workspace

```bash
linux:~/workspace $ go work init ./hello
linux:~/workspace $ go run ./hello
```

### download and modify external module

```go
// int.go
package reverse

import "strconv"

func Int(i int) int {
    i, _ = strconv.Atoi(String(strconv.Itoa(i)))
    return i
}
```

```go
// hello.go
package main

import (
    "fmt"
    "golang.org/x/example/hello/reverse"
)

func main() {
    fmt.Println(reverse.String("Hello"), reverse.Int(24601))
}
```

```bash
linux:~/workspace $ git clone https://go.googlesource.com/example
linux:~/workspace $ go work use ./example/hello

linux:~/workspace $ vi example/hello/reverse/int.go
linux:~/workspace $ vi hello/hello.go

linux:~/workspace $ go run ./hello
```

---

## other command

```bash
linux:~/project $ go mod edit -go=1.17
linux:~/project $ go mod edit -print
linux:~/project $ go mod edit -require github.com/gorilla/context@v1.1.1
linux:~/project $ go mod edit -replace example.com/student=../example.com/student

linux:~/project $ go list
linux:~/project $ go list all
linux:~/project $ go list -m all
linux:~/project $ go list -m -versions github.com/gorilla/mux

linux:~/project $ go mod why golang.org/x/text/language golang.org/x/text/encoding
```

- [Go Modules Reference](https://go.dev/ref/mod)
