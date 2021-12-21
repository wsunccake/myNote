# type

## type

```go
type Liter float64
type Gallon float64
type Milliliter float64

func GallonToLiter(g Gallon) Liter {
	return Liter(g * 3.785)
}

func LiterToGallon(l Liter) Gallon {
	return Gallon(l * 0.264)
}

func MilliliterToGallon(ml Milliliter) Gallon {
	return Gallon(ml * 0.000264)
}

func MilliliterToLiter(ml Milliliter) Liter {
	return Liter(ml * 0.001)
}

func main() {
	var carFuel Gallon
	carFuel = 10.0
	// carFuel = Gallon(10.0)
	busFuel := Liter(240.0)
	soda := Milliliter(300.0)

	fmt.Printf("car fuel: %f g ~ %f l \n", carFuel, Liter(carFuel*3.785))
	fmt.Printf("bus fuel: %f g ~ %f l \n", Gallon(busFuel*0.264), busFuel)
	fmt.Printf("soda    : %f g ~ %f l \n", Gallon(soda*0.000264), soda*0.001)
	// carFuel + busFuel

	fmt.Printf("car fuel: %f g ~ %f l \n", carFuel, GallonToLiter(carFuel))
	fmt.Printf("bus fuel: %f g ~ %f l \n", LiterToGallon(busFuel), busFuel)
	fmt.Printf("soda    : %f g ~ %f l \n", MilliliterToGallon(soda), MilliliterToLiter(soda))
}
```


---

## method

```go
type Liter float64
type Gallon float64
type Milliliter float64

func (g Gallon) ToLiter() Liter {
	return Liter(g * 3.785)
}

func (l Liter) ToGallon() Gallon {
	return Gallon(l * 0.264)
}

func (ml Milliliter) ToGallon() Gallon {
	return Gallon(ml * 0.000264)
}

func (ml Milliliter) ToLiter() Liter {
	return Liter(ml * 0.001)
}

func main() {
	var carFuel Gallon = 10.0
	// carFuel = Gallon(10.0)
	busFuel := Liter(240.0)
	soda := Milliliter(300.0)

	fmt.Printf("car fuel: %f g ~ %f l \n", carFuel, Liter(carFuel*3.785))
	fmt.Printf("bus fuel: %f g ~ %f l \n", Gallon(busFuel*0.264), busFuel)
	fmt.Printf("soda    : %f g ~ %f l \n", Gallon(soda*0.000264), soda*0.001)
	// carFuel + busFuel

	fmt.Printf("car fuel: %f g ~ %f l \n", carFuel, carFuel.ToLiter())
	fmt.Printf("bus fuel: %f g ~ %f l \n", busFuel.ToGallon(), busFuel)
	fmt.Printf("soda    : %f g ~ %f l \n", soda.ToGallon(), soda.ToLiter())
}
```
