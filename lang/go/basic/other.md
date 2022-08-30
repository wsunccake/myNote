# other

## dynamic call

```go
package main

import (
	"fmt"
	"os"
)

var funcMap = map[string]interface{} {
	"hi":    hi,
	"hello": hello,
}

func hi() {
	fmt.Print("Hi Go")
}

func hello(name string) string{
	return fmt.Sprintf("hello %v", name)
}

func callDynamically(name string, args ...interface{}) {
	switch name {
	case "hi":
		funcMap["hi"].(func())()
	case "hello":
		sentence := funcMap["hello"].(func(string) string)(args[0].(string))
		fmt.Println(sentence)
	}

}

func main() {
	arg1 := os.Args[1]
	arg2 := ""
	if len(os.Args) > 2 {
		arg2 = os.Args[2]
	}

	fmt.Printf("arg1: %v, arg2: %v\n", arg1, arg2)
	callDynamically(arg1, arg2)
}
```

```bash
linux:~ # go run main.go hi
linux:~ # go run main.go hello go
```
