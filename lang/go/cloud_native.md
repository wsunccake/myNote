


## project

### environment

```bash
linux:~ # export GOPATH=~/go  # default GOPATH
linux:~ # go env GOPATH
linux:~ # cd `go env GOPATH`
linux:~/go # mkdir src
```


### import from local

```bash
linux:~/go # mkdir src/hello
linux:~/go # vi src/hello/hello.go
package hello

import "fmt"

func Hello() {
  fmt.Println("Hello Go")
}

linux:~/go # vi main.go
package main

import "hello"

func main() {
  hello.Hello()
}
```


### manage project by github

```bash
linux:~/go/src/hello # git init
linux:~/go/src/hello # git add hello.go
linux:~/go/src/hello # git commit -m
linux:~/go/src/hello # git remote add origin git@github.com:<user>/<repo>.git
linux:~/go/src/hello # git push -u origin master
linux:~/go/src/hello # git push
```


### import from github

```bash
linux:~/go # go get github.com/<user>/<repo>
linux:~/go # tree src/github.com/<user>/<repo>
.
└── hello.go

linux:~/go # vi main.go
package main

import "github.com/<user>/<repo>"

func main() {
  hello.Hello()
}
```
