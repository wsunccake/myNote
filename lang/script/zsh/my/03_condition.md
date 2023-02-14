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
if [[ "$str" == "name" || $str == "value" ]] {
    echo "$str"
}

# command
cmd="ls ."
if { eval $cmd >& /dev/null } {
    echo "success"
} else {
    echo "fail"
}


# simple
SEX=m
[[ "$SEX" == "m" ]] && echo "male"

NUM=5
(( $NUM < 10 )) && {
    for i ({1..$NUM}) {
        echo $i
    }
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

```zsh
i=0
while (( $i < 5 )) {
    echo "$i: hello zsh"
    i=$(( i + 1 ))
}
```

---

## until

```zsh
i=0
until (( $i > 5 )) {
    echo "$i: hello zsh"
    i=$(( i + 1 ))
}
```

---

## case

```zsh
i=hi
case $i {
    (go_on)
    echo "run it and next pattern"
    ;&
    # ;& 執行下一個 pattern

    (hi)
    echo "hi $USER"
    ;|
    # ;| 繼續匹配

    (bye)
    echo "bye"
    ;;
    # ;; 離開 case

    (hi)
    echo "pattern: $i"
    ;;

    (*)
    echo "other"
    ;;
}
```

---

## select

```zsh

select V  (a b q); do
  echo "select: $V"
  [[ "$V" == "q" ]] && break
done
```

---

## always

類似一般語言的 except

```zsh
always {
    echo "always"
}
```
