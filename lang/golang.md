# Go

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