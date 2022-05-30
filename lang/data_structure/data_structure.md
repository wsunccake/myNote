## Big-O

O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(n^3) < O(2^n) < O(n!) < O(n^n)

`O(n)`

```
for(i = 0; i < n; i++) {
    O(1)
}

count = 0
while (count < n) {
    count++
}
```


`O(log n)`

```
for (i = 1; i < n; i = i * 2){
    O(1)
}

count = 1
while (count < n) {
	count = count*2
}
```


`O(n^2)`

```
count = 0
for(i=0; i<n; i++) {
    for(j=0; j<n; j++) {
        count++
    }
}
```