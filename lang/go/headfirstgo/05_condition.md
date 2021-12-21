# condition

## if

```go
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
```

```go
f, err := os.OpenFile("access.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
if err != nil {
    log.Fatal(err)
}

if _, err := f.Write([]byte("appended some data\n")); err != nil {
    f.Close()
    log.Fatal(err)
}

if err := f.Close(); err != nil {
    log.Fatal(err)
}
```


---

## switch

```go
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
```

```go
// basic
i := 2
fmt.Print("Write ", i, " as ")
switch i {
case 1:
    fmt.Println("one")
case 2:
    fmt.Println("two")
case 3:
    fmt.Println("three")
}

// no condition
switch time.Now().Weekday() {
case time.Saturday, time.Sunday:
    fmt.Println("It's the weekend")
default:
    fmt.Println("It's a weekday")
}

// condition
t := time.Now()
switch {
case t.Hour() < 12:
    fmt.Println("It's before noon")
default:
    fmt.Println("It's after noon")
}

whatAmI := func(i interface{}) {
    switch t := i.(type) {
    case bool:
        fmt.Println("I'm a bool")
    case int:
        fmt.Println("I'm an int")
    default:
        fmt.Printf("Don't know type %T\n", t)
    }
}
whatAmI(true)
whatAmI(1)
whatAmI("hey")
```
