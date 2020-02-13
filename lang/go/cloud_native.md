


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

---

## serialize

### gob

`server`

```go
package main

import (
	"encoding/gob"
	"log"
	"net"
)

type User struct {
	Id      int
	Name    string
	Age     int
}

func handleConnection(conn net.Conn) {
	dec := gob.NewDecoder(conn)
	p := &User{}

	dec.Decode(p)
	log.Println("Hello ",p.Name,", Your Age is ",p.Age);

	conn.Close()
}


func main() {
	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		panic(err)
	}

	for {
		conn, err := ln.Accept()
		if err != nil {
			continue
		}
		go handleConnection(conn)
	}
}
```

`client`

```go
package main

import (
	"encoding/gob"
	"log"
	"net"
)

type User struct {
	Id      int
	Name    string
	Age     int
}

func main() {
	studentEncode := User{Id: 1, Name:"john", Age: 20}
	log.Println("start client");

	conn, err := net.Dial("tcp", "localhost:8080")
	if err != nil {
		log.Fatal("Connection error", err)
	}

	encoder := gob.NewEncoder(conn)
	encoder.Encode(studentEncode)

	conn.Close()
	log.Println("done")
}
```


### protocol buffers

`setup`

```bash
linux:~ # wget https://github.com/protocolbuffers/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip
linux:~ # unzip -l protoc-3.0.0-linux-x86_64.zip
linux:~ # unzip protoc-3.0.0-linux-x86_64.zip bin/protoc -d /usr/local

linux:~ # go get -u github.com/golang/protobuf/{proto,protoc-gen-go}
linux:~ # ls `go env GOPATH`/bin/protoc-gen-go
```

`protocol`

```bash
linux:~ # vi user.proto
syntax = "proto3";  
package protobuf;

message User {  
    int64  id   = 1;
    string name = 2;
    int32  age = 3;
}

linux:~ # protoc --go_out=. *.proto
linux:~ # ls user.pb.go
linux:~ # mkdir `go env GOPATH`/src/protobuf
linux:~ # mv user.pb.go `go env GOPATH`/src/protobuf
```

`server`

```go
package main

import (
    "github.com/golang/protobuf/proto"
    "net/http"
    "fmt"
    "io/ioutil"
    "protobuf"
)

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        user:= protobuf.User{}

        data, err := ioutil.ReadAll(r.Body)
        if err != nil {
            fmt.Println(err)
        }
        if err := proto.Unmarshal(data, &user); err != nil {
            fmt.Println(err)
        }
        fmt.Println(user.Id, ":", user.Name)
   })

    http.ListenAndServe(":3000", nil)
}
```

`client`

```go
package main

import (
    "github.com/golang/protobuf/proto"
    "net/http"
    "fmt"
    "bytes"
    "protobuf"
)

func main() {
	user := protobuf.User{Id: 1, Name: "joho", Age: 20}

    data, err := proto.Marshal(&user)
    if err != nil {
        fmt.Println(err)
        return
    }

    _, err = http.Post("http://localhost:3000", "", bytes.NewBuffer(data))

    if err != nil {
        fmt.Println(err)
        return
    }
}
```


---

## RPC

`server`

```go
package main

import (
	"log"
	"net"
	"net/rpc"
)

type Listener int

func (l *Listener) GetLine(line []byte, ack *bool) error {
	log.Println(string(line))
	return nil
}

func main() {
	addy, err := net.ResolveTCPAddr("tcp", "0.0.0.0:8080")
	if err != nil {
		log.Fatal(err)
	}

	inbound, err := net.ListenTCP("tcp", addy)
	if err != nil {
		log.Fatal(err)
	}

	listener := new(Listener)
	rpc.Register(listener)
	rpc.Accept(inbound)
}
```

`client`

```go
package main

import (
	"bufio"
	"log"
	"net/rpc"
	"os"
)

func main() {
	client, err := rpc.Dial("tcp", "localhost:8080")
	if err != nil {
		log.Fatal(err)
	}

	in := bufio.NewReader(os.Stdin)
	for {
		line, _, err := in.ReadLine()
		if err != nil {
			log.Fatal(err)
		}
		var reply bool
		err = client.Call("Listener.GetLine", line, &reply)
		if err != nil {
			log.Fatal(err)
		}
	}
}
```

