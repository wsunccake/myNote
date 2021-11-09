# run

## hello

```bash
linux:~/project $ cat << EOF > hello.go
package main

import "fmt"

func main() {
    fmt.Println("hello go")
}
EOF

# run
linux:~/project $ go run hello.go

# compile to binary
linux:~/project $ go build hello.go
linux:~/project $ ./hello
```
