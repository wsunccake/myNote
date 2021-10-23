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
