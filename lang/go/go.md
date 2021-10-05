# go

## mod

```bash
linux:~ $ go help env
linux:~ $ go env GOPATH
linux:~ $ go env -w GO111MODULE=auto    # set go env
linux:~ $ cat $(go env GOENV)           # show go env
linux:~ $ go env -u GO111MODULE         # unset go env

linux:~ $ go build <go file>            # build
linux:~ $ go build ./...                # check all import, '...' wildcards
```


---

## practice

### internal package 

```bash
linux:~/gomp $ GO111MODULE=on go mod init gomp
linux:~/gomp $ cat go.mod
linux:~/gomp $ mkdir lib cli
linux:~/gomp $ touch lib/greeting.go cli/say.go
linux:~/gomp $ tree
.
├── cli
│   └── say.go
├── go.mod
└── lib
    └── greeting.go

linux:~/gomp $ cat << EOF > lib/greeting.go
package lib

import "fmt"

func Say(s string) {
    fmt.Println(s)
}
EOF

linux:~/gomp $ cat << EOF > cli/say.go
package main

import "gomp/lib"

func main() {
    lib.Say("Hello")
}
EOF

linux:~/gomp $ go build ./...
linux:~/gomp $ go build cli/say.go
```


### external package

```bash
linux:~/gomp $ go get github.com/fatih/color
linux:~/gomp $ go get github.com/fatih/color@v1.8.0
linux:~/gomp $ cat go.mod

linux:~/gomp $ cat << EOF > lib/greeting.go
package lib

import "fmt"
import "github.com/fatih/color"

func Say(s string) {
	fmt.Println(s)
}

func SayWithColor(s string) {
	color.Red(s)
}
EOF

linux:~/gomp $ cat << EOF > cli/say.go
package main

import "gomp/lib"

func main() {
	lib.Say("Hello")
	lib.SayWithColor("World")
}
EOF
```


### make utility

```bash
linux:~/gomp $ go get golang.org/x/lint/golint
linux:~/gomp $ go install golang.org/x/lint/golint

linux:~/gomp $ cat << EOF > makefile
.DEFAULT_GOAL := build

.PHONY: fmt
fmt:
	go fmt ./...

.PHONY: lint
lint:
	$(shell go env GOPATH)/bin/golint ./...

.PHONY: vet
vet: fmt
	go vet ./...

.PHONY: build
build: vet
	go build ./...
	go build cli/say.go
EOF

linux:~/gomp $ make lint
linux:~/gomp $ make
```


---

## import

```bash
linux:~/project $ mkdir lib
linux:~/project $ cat << EOF > lib/msg.go
package lib

import "fmt"

// func upper name export
func Hi() {
    fmt.Println("Hi")
}

// func lower name unexport or undefine
func hello() {
    fmt.Println("hello")
}
EOF

linux:~/project $ cat << EOF > main.go
package main

import (
    L "./lib"
    "./lib"
)

func main() {
    L.Hi()
//  L.hello()
    lib.Hi()
//  lib.hello()
}
EOF
linux:~/project $ go run main.go
```
