


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


---

## protocol buffers

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

const (
	serverPort = ":8080"
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

    http.ListenAndServe(serverPort, nil)
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

const (
	serverHost = "localhost"
	serverPort = ":8080"
)

func main() {
	user := protobuf.User{Id: 1, Name: "john", Age: 20}

    data, err := proto.Marshal(&user)
    if err != nil {
        fmt.Println(err)
        return
    }

    _, err = http.Post("http://" + serverHost + serverPort, "", bytes.NewBuffer(data))

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

const (
	serverProtocol = "tcp"
	serverPort = ":8080"
)

func main() {
	addy, err := net.ResolveTCPAddr(serverProtocol, "0.0.0.0" + serverPort)
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

const (
	serverProtocol = "tcp"
	serverHost = "localhost"
	serverPort = ":8080"
)

func main() {
	client, err := rpc.Dial(serverProtocol, serverHost + serverPort)
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

---

## gRPC

```

protoc --go_out=plugins=grpc:. *.proto
```


`setup`

```bash
linux:~ # wget https://github.com/protocolbuffers/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip
linux:~ # unzip -l protoc-3.0.0-linux-x86_64.zip
linux:~ # unzip protoc-3.0.0-linux-x86_64.zip bin/protoc -d /usr/local

linux:~ # go get -u github.com/golang/protobuf/{proto,protoc-gen-go}
linux:~ # ls `go env GOPATH`/bin/protoc-gen-go
linux:~ # go get -u google.golang.org/grpc
```

`protocol`

```bash
linux:~ # vi echo.proto
syntax = "proto3";

package protobuf;

service Echo {
    rpc GetUser (Id) returns(User){}
}

message Id {
    int64  id   = 1;
}

message User {
    int64  id   = 1;
    string name = 2;
    int32  age = 3;
}


linux:~ # protoc --go_out=plugins=grpc:. *.proto
linux:~ # ls echo.pb.go
linux:~ # mkdir `go env GOPATH`/src/protobuf
linux:~ # mv echo.pb.go `go env GOPATH`/src/protobuf
```

`server`

```go
package main

import (
	"context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
	"log"
	"net"
	"protobuf"
)

const (
	grpcProtocol = "tcp"
	grpcPort     = ":8080"
)

var allUsers = []protobuf.User{
	{Id: 0, Name: "", Age: 0},
	{Id: 1, Name: "john", Age: 20},
	{Id: 2, Name: "mary", Age: 18},
}

type EchoServer struct{}

func (e *EchoServer) GetUser(ctx context.Context, req *protobuf.Id) (resp *protobuf.User, err error) {
	log.Printf("receive client request: %d\n", req.Id)
	user := allUsers[req.Id]

	return &protobuf.User{
		Id: user.Id,
		Name: user.Name,
		Age: user.Age,
	}, nil
}

func main() {
	apiListener, err := net.Listen(grpcProtocol, grpcPort)
	if err != nil {
		log.Println(err)
		return
	}

	echoServer := &EchoServer{}
	grpcServer := grpc.NewServer()
	protobuf.RegisterEchoServer(grpcServer, echoServer)

	reflection.Register(grpcServer)
	if err := grpcServer.Serve(apiListener); err != nil {
		log.Fatal("gRPC Serve Error: ", err)
		return
	}
}
```

`client`

```go
package main

import (
	"context"
	"google.golang.org/grpc"
	"log"
	"protobuf"
)

const (
	grpcHost = "localhost"
	grpcPort = ":8080"
)

func main() {
	conn, err := grpc.Dial(grpcHost + grpcPort, grpc.WithInsecure())
	if err != nil {
		log.Fatalf("fail to connect： %v", err)
	}
	defer conn.Close()

	client := protobuf.NewEchoClient(conn)

	user, err := client.GetUser(context.Background(), &protobuf.Id{Id: 1})
	if err != nil {
		log.Fatalf("fail to run： %v", err)
	}
	log.Printf("name： %s, age: %d", user.Name, user.Age)
}
```


---

## docker

`app`

```bash
linux:~ # vi main.go
package main

import (
        "fmt"
        "net/http"
)

func handler(writer http.ResponseWriter, request *http.Request) {
        fmt.Fprint(writer, "Hello Go")
}

func main() {
        http.HandleFunc("/", handler)
        http.ListenAndServe(":8080", nil)
}

linux:~ # go build -o app main.go
linux:~ # ./app

linux:~ # curl 127.0.0.1:8080
```

`containerize 1`

```bash
linux:~ # vi dockerfile
FROM  golang

ADD  main.go /src/main.go
RUN  cd /src && go build -o /app/app main.go

WORKDIR /app/
EXPOSE 8080
ENTRYPOINT ./app


linux:~ # docker build -t go-app .
linux:~ # docker run -itd -p 8080:8080 go-app
```

`containerize 2`

```bash
linux:~ # vi dockerfile
FROM  golang:alpine

ADD  main.go /src/main.go
RUN  cd /src && go build -o /app/app main.go

WORKDIR /app/
EXPOSE 8080
ENTRYPOINT ./app


linux:~ # docker build -t go-app .
linux:~ # docker run -itd -p 8080:8080 go-app
```

`containerize 3`

```bash
linux:~ # vi dockerfile
# multi-stage
# build
FROM  golang:alpine  AS build-env

ADD  main.go /src/main.go
RUN  cd /src && go build -o /app/app main.go


# run
FROM alpine:latest

WORKDIR /app/
COPY --from=build-env /app/app /app/

EXPOSE 8080
ENTRYPOINT ./app


linux:~ # docker build -t go-app .
linux:~ # docker run -itd -p 8080:8080 go-app
```

`other`

```bash
linux:~ # docker pull golang
linux:~ # docker pull golang:alpine
linux:~ # docker pull alpine

linux:~ # curl https://registry.hub.docker.com/v2/repositories/library/golang/tags/
```
