# regex

## regexp

```go
package main

import (
	"fmt"
	"regexp"
)

func main() {
	str := "/usr/lib/python2.6/site-packages/gtk-2.0/gconf.so"

	re1, _ := regexp.Compile(`(.*)\.(.*?)$`)
	res1 := re1.FindAllStringSubmatch(str, -1)
	fmt.Printf("%+v\n", res1)
	for _, e := range res1 {
		fmt.Println("match: ", e[0])
		fmt.Println("group1: ",e[1])
		fmt.Println("group2: ",e[2])
	}

	re2, _ := regexp.Compile(`(.*?)\.(.*)`)
	res2 := re2.FindAllStringSubmatch(str, -1)
	fmt.Printf("%+v\n", res2)
	for _, e := range res2 {
		fmt.Println("match: ", e[0])
		fmt.Println("group1: ",e[1])
		fmt.Println("group2: ",e[2])
	}

	re3, _ := regexp.Compile(`(.*?)/(.*)`)
	res3 := re3.FindAllStringSubmatch(str, -1)
	fmt.Printf("%+v\n", res3)
	for _, e := range res3 {
		fmt.Println("match: ", e[0])
		fmt.Println("group1: ",e[1])
		fmt.Println("group2: ",e[2])
	}

	re4, _ := regexp.Compile(`(.*)/(.*)`)
	res4 := re4.FindAllStringSubmatch(str, -1)
	fmt.Printf("%+v\n", res4)
	for _, e := range res4 {
		fmt.Println("match: ", e[0])
		fmt.Println("group1: ",e[1])
		fmt.Println("group2: ",e[2])
	}

	re5, _ := regexp.Compile(`/python.*/`)
	res5 := re5.FindString(str)
	fmt.Println("greedy: ", res5)

	re6, _ := regexp.Compile(`/python.*?/`)
	res6 := re6.FindString(str)
	fmt.Println("lazy: ", res6)

}
```
