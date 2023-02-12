# var

## prefix and suffix

```zsh
FILE_PATH=/usr/lib/python/site-package/xxx-1.0/yyy.zz
echo "raw:"
echo ${FILE_PATH}        # /usr/lib/python/site-package/xxx-1.0/yyy.zz

echo "prefix:"
echo ${FILE_PATH%.*}     # /usr/lib/python/site-package/xxx-1.0/yyy
echo ${FILE_PATH%%.*}    # /usr/lib/python/site-package/xxx-1

echo "suffix:"
echo ${FILE_PATH#*/}     # usr/lib/python/site-package/xxx-1.0/yyy.zz
echo ${FILE_PATH##*/}    # yyy.zz
```

---

## define var operation

```zsh
VAR="Hello Zsh"
echo "define VAR: ${VAR}"               # define VAR: Hello Zsh
echo "\${VAR:=value}: ${VAR:=value}"    # ${VAR:=value}: Hello Zsh
echo "VAR: ${VAR}"                      # VAR: Hello Zsh
```

```zsh
VAR="Hello Zsh"
echo "define VAR: ${VAR}"               # define VAR: Hello Zsh
echo "\${VAR:-value}: ${VAR:-value}"    # ${VAR:-value}: Hello Zsh
echo "VAR: ${VAR}"                      # VAR: Hello Zsh
```

```zsh
VAR="Hello Zsh"
echo "define VAR: ${VAR}"               # define VAR: Hello Zsh
echo "VAR:+value ${VAR:+value}"         # VAR:+value value
echo "VAR: ${VAR}"                      # VAR: Hello Zsh
```

```zsh
VAR="Hello Zsh"
echo "define VAR: ${VAR}"               # define VAR: Hello Zsh
echo "\${VAR:?value}: ${VAR:?value}"    # ${VAR:?value}: Hello Zsh
echo "VAR: ${VAR}"                      # VAR: Hello Zsh
```

---

## undefine var operation

```zsh
unset VAR
echo "undefine VAR: ${VAR}"             # undefine VAR:
echo "\${VAR:=value}: ${VAR:=value}"    # ${VAR:=value}: value
echo "VAR: ${VAR}"                      # VAR: value
```

```zsh
unset VAR
echo "undefine VAR: ${VAR}"             # undefine VAR:
echo "\${VAR:-value}: ${VAR:-value}"    # ${VAR:-value}: value
echo "VAR: ${VAR}"                      # VAR:
```

```zsh
unset VAR
echo "undefine VAR: ${VAR}"             # undefine VAR:
echo "\${VAR:+value}: ${VAR:+value}"    # ${VAR:+value}:
echo "VAR: ${VAR}"                      # VAR:
```

```zsh
unset VAR
echo "undefine VAR: ${VAR}"
#echo "VAR:?value ${VAR:?value}"  # show err
echo "VAR: ${VAR}"
echo
```

---

## array

```zsh
ARR=(a b c)
ARR+=d
ARR[2]=B
echo "ARR: $ARR"
echo "ARR type: ${(t)ARR}"
echo "ARR first: ${ARR[1]}"
echo "ARR last: ${ARR[-1]}"
echo "ARR slice: ${ARR[2,-2]}"
echo "ARR length: ${#ARR[@]}"
echo "ARR: ${ARR[@]}"
echo "ARR first: ${ARR[@][1]}"
echo "ARR: ${(@)ARR}"
echo "ARR first: ${(@)ARR[1]}"

# loop
for ITEM in ${ARR[*]}; do
  echo "ITEM: $ITEM"
done

for ((i=1; i <= ${#ARR[@]}; i++)); do
  echo "Index: $i, ITEM: ${ARR[$i]}"
done

# append
A1=(1 2 3 X)
A2=(a b c X)
A3=(${A1[@]} ${A2[*]})

# string to array
S=1,2,3,4
A=($(echo $S | sed 's/,/ /g'))
echo $A

# function
show_array() {
  local arr=$1

  for i in "${(P)${arr}[@]}"; do
    echo "$i"
  done
}
show_array ARR
```

---

## associative array

```zsh
declare -A MAP
MAP=([eth0]=192.168.0.1 [em1]=172.16.0.1)
echo "${MAP[eth0]}"
echo "MAP Length: ${#MAP[@]}"
echo "MAP type: ${(t)MAP}"

# typeset alias declare
typeset -A ASSOC
ASSOC=(one 1 two 2)
echo ${ASSOC[a]}
echo "ASSOC value: $ASSOC"
echo "ASSOC key: ${(k)ASSOC}"
echo "ASSOC key/value: ${(kv)ASSOC}"

# loop
for key val in "${(@kv)ASSOC}"; do
  echo "$key -> $val"
done

# function
show_assoc() {
  local assoc=$1

  for k v in "${(@Pkv)${assoc}}"; do
    echo "key: $k, val: $v"
  done
}
show_assoc ASSOC
```

## compare

```zsh
# number
num=123
((num == 123)) && echo good
((num == 1 || num == 2)) && echo good

# string
str=abc
[[ $str == abc ]] && echo good
[[ $str == "" || $str == 123 ]] && echo good
```
