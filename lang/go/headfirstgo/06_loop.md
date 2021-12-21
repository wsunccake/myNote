# loop

## for

```go
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

for {
    fmt.Println("loop")
    break
}

for n := 0; n <= 5; n++ {
    if n%2 == 0 {
        continue
    }
    fmt.Println(n)
}
```


---

## goto

```go
const MAX int = 5

i := 0
LOOP: fmt.Println(i)
i++
if i < MAX {
	goto LOOP
}
```
