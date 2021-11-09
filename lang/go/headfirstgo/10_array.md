# array

## basic

```go
var a [5]int
fmt.Println("emp:", a)          // [0 0 0 0 0]

a[4] = 100
fmt.Println("set:", a)          // [0 0 0 0 100]
fmt.Println("get:", a[4])       // 100
fmt.Println("len:", len(a))     // 5

b := [5]int{1, 2, 3, 4, 5}
fmt.Println("dcl:", b)          // [1 2 3 4 5]

c := [...]int{1, 2, 3, 4, 5}
fmt.Println(reflect.TypeOf(c))	// [5]int

var twoD [2][3]int
for i := 0; i < 2; i++ {
	for j := 0; j < 3; j++ {
		twoD[i][j] = i + j
	}
}
fmt.Println("2d: ", twoD)       // [[0 1 2] [1 2 3]]
fmt.Println(twoD[0][1])         // 1
```


---

## for range

```go
twoD := [...][3]int{{0, 1, 2}, {3, 4, 5}}
for i, e := range twoD {
	fmt.Println(i, e)
}
fmt.Println(reflect.TypeOf(twoD))
```


---

## row major

```go
const M = 10000
startTime := time.Now()

var rowMajor [M][M]int
for i := 0; i < M; i++ {
	for j := 0; j < M; j++ {
		rowMajor[i][j] = i + j
	}
}

endTime := time.Now()
diffTime := endTime.Sub(startTime)
fmt.Println("rowMajor: ", diffTime)
```


---

## column major

```go
const M = 10000
startTime := time.Now()

var columnMajor [M][M]int
for j := 0; j < M; j++ {
	for i := 0; i < M; i++ {
		columnMajor[i][j] = i + j
	}
}

endTime := time.Now()
diffTime := endTime.Sub(startTime)
fmt.Println("columnMajor: ", diffTime)
```


---

## function

```go
func doubleValue(a [3]int) {
	for i, v := range a {
		a[i] = v * 2
	}
}

func doublePointer(a *[3]int) {
	for i, v := range a {
		a[i] = v * 2
	}
}

func main() {
	a := [...]int{1, 2, 3}
	fmt.Println(a)

	doubleValue(a)
	fmt.Println(a)

	doublePointer(&a)
	fmt.Println(a)
}
```


---

## os.Open

```bash
linux:~ $ echo 1 > tmp.txt
linux:~ $ echo 2 >> tmp.txt
linux:~ $ echo 3 >> tmp.txt
```


```go
file, err := os.Open("tmp.txt")
if err != nil {
	log.Fatal(err)
}
defer file.Close()

scanner := bufio.NewScanner(file)
for scanner.Scan() {
	fmt.Println(scanner.Text())
}
if scanner.Err() != nil {
	log.Fatal(scanner.Err())
}
```
