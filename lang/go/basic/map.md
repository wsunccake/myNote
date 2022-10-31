# map

## make[<type>]<type>

```go
package main

import "fmt"

func main() {
	var countryCapitalMap map[string]string
	countryCapitalMap = make(map[string]string)

	countryCapitalMap["France"] = "Paris"
	countryCapitalMap["Italy"] = "Rome"
	countryCapitalMap["Japan"] = "Tokyo"

	// check key exist
	if _, ok := countryCapitalMap["Taiwan"]; !ok {
		fmt.Println("no found Taiwan")
	}

	weekDay := map[string]string{
		"sun": "Sunday",
		"mon": "Monday",
		"tues": "Tuesday",
		"wed": "Wednesday",
		"thurs": "Thursday",
		"fri": "Friday",
		"sat": "Saturday"}

	delete(countryCapitalMap, "Italy")

	for k, v := range countryCapitalMap {
		fmt.Printf("%s -> %s\n", k, v)
	}


	k := "abc"
	v, ok := weekDay[k]
	if ok {
		fmt.Println(k, "->", v)
	} else {
		fmt.Println("no found", k)
	}

	// emptyMap1 := make(map[string]int)
	// emptyMap2 := map[string]int{}

	// var nilMap map[string]int
}
```
