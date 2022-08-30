# condition

## if

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	fmt.Print("input m/f: ")
	reader := bufio.NewReader(os.Stdin)
	text, _ := reader.ReadString('\n')
	text = strings.TrimSuffix(text, "\n")

	if text == "m" {
		fmt.Println("Male")
	} else if text == "f" {
		fmt.Println("Female")
	} else {
		fmt.Println("Unknown")
	}
}
```


---

## switch

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	fmt.Print("input m/f: ")
	reader := bufio.NewReader(os.Stdin)
	text, _ := reader.ReadString('\n')
	text = strings.TrimSuffix(text, "\n")

	switch text {
	case "m":
		fmt.Println("Male")
	case "f":
		fmt.Println("Female")
	default:
		fmt.Println("Unknown")
	}
}
```


---

# loop

## for

```go
package main

import (
	"fmt"
)

func main() {
	const MAX int = 5
	for i:=0; i < MAX; i++ {
		fmt.Println(i)
	}

	i := 0
	for true {
		fmt.Println(i)
		i++
		if i >= MAX {
			break
		}
    }

    for i, v := range [MAX]int{1, 4, 5, 9} {
		fmt.Println(i, v)
	}
}
```


---

## goto

```go
package main

import (
	"fmt"
)

func main() {
	const MAX int = 5
	i := 0
	LOOP: fmt.Println(i)
	i++
	if i < MAX {
		goto LOOP
	}
}
```