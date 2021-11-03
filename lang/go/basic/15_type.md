# type

## type

```go
type Liter float64
type Gallon float64

func ToLiter(g Gallon) Liter {
	return Liter(g * 3.785)
}

func ToGallon(l Liter) Gallon {
	return Gallon(l * 0.264)
}

func main() {
	var carFuel Gallon
	carFuel = 10.0
	// carFuel = Gallon(10.0)
	busFuel := Liter(240.0)

	fmt.Printf("car fuel: %f g ~ %f l \n", carFuel, Liter(carFuel*3.785))
	fmt.Printf("bus fuel: %f g ~ %f l \n", Gallon(busFuel*0.264), busFuel)
	// carFuel + busFuel

	fmt.Printf("car fuel: %f g ~ %f l \n", carFuel, ToLiter(carFuel))
	fmt.Printf("bus fuel: %f g ~ %f l \n", ToGallon(busFuel), busFuel)
}
```


---

## struct

```go
```
