## kql

---

## content

- [basic](#basic)

---

## basic

query is case insensitive

```csv
Date            Name            Age     City            Sex
2019-08-25      Bob             30      Austin          Male
2019-05-19      Sue             24      Dallas          Female
2019-08-20      Jerry           45      San Diego       Male
2019-04-20      Jennifer        32      Wichita         Female
```

```bash
# field exist
Name: *

# matching value
Name: "Bob"

# range value
Age >= 30

# using wildcard
Name: J*

# negating
not Name: J*
not Age >= 30

# combining
Age >= 25 and Age <= 40
Age >= 25 or Age <= 40
(Age >= 25) or (Age <= 40)

# timestamp
y: Years
M: Months
w: Weeks
d: Days
h: Hours
H: Hours
m: Minutes
s: Seconds
# timestamp: "yyyy-MM-dd hh:mm:ss"
# date: "yyyy[[-MM]-dd]"
# time: hh:mm:ss
@timestamp  > "2019-01" and @timestamp < "2019-12"
```

[Common options](#https://www.elastic.co/guide/en/elasticsearch/reference/8.10/common-options.html)
