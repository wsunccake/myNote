# condition

## if / else

```zsh
# number, 在 (()) 裡的變數可以省略 $
num=5
if (( $num > 3 && num + 3 < 10 )) {
    echo $num
}

# string, 在 [[]] 裡的變數可以省略 "
str=name
if [[ $str == "name" || "$str" == "value" ]] {
    echo "$str"
}

# shell
if { grep sd1 /etc/fstab } {
    echo good
}
```

---

## for

```zsh
# number
for ((i=0; i < 10; i++)) {
    echo $i
}

for i ({1..10}) {
    echo $i
}

# array
for i (aa bb cc) {
    echo $i
}

for i (*.txt) {
    echo $i
}

array=(aa bb cc)
for i ($array) {
    echo $i
}
```

---

## report

```zsh
repeat 5 {
    echo good
}
```

---

## while

##
