# pointer

## * / &

```go
package main

import "fmt"

func main() {
	var v1 int = 20
	var p1 *int
	p1 = &v1
	var p2 *int = &v1
	p3 := &v1
	p4 := new(int)
	p4 = &v1
	fmt.Printf("value v1: %d, *p1: %d, *p2: %d, *p3: %d, *p4: %d\n", v1, *p1, *p2, *p3, *p4)
	fmt.Printf("addres &v1: %x, p1: %x, p2: %x, p3: %x, p4: %x\n", &v1, p1, p2, p3, p4)
}
```