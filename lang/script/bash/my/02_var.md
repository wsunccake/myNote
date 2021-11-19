# var

## prefix and suffix

```bash
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

## sentence and word

```bash
# For bash 4.x
SENTENCE="That is a test."
echo "sentence:"
echo "${SENTENCE}"          # That is a test.

echo "reverse:"
echo "${SENTENCE~~}"        # tHAT IS A TEST.

echo "upper:"
echo "${SENTENCE^^}"        # THAT IS A TEST.

echo "lower:"
echo "${SENTENCE,,}"        # that is a test.
```


---

## define var operation

```bash
VAR="Hello Bash"
echo "define VAR: ${VAR}"               # define VAR: Hello Bash
echo "\${VAR:=value}: ${VAR:=value}"    # ${VAR:=value}: Hello Bash
echo "VAR: ${VAR}"                      # VAR: Hello Bash
```

```bash
VAR="Hello Bash"
echo "define VAR: ${VAR}"               # define VAR: Hello Bash
echo "\${VAR:-value}: ${VAR:-value}"    # ${VAR:-value}: Hello Bash
echo "VAR: ${VAR}"                      # VAR: Hello Bash
```

```bash
VAR="Hello Bash"
echo "define VAR: ${VAR}"               # define VAR: Hello Bash
echo "VAR:+value ${VAR:+value}"         # VAR:+value value
echo "VAR: ${VAR}"                      # VAR: Hello Bash
```

```bash
VAR="Hello Bash"
echo "define VAR: ${VAR}"               # define VAR: Hello Bash
echo "\${VAR:?value}: ${VAR:?value}"    # ${VAR:?value}: Hello Bash
echo "VAR: ${VAR}"                      # VAR: Hello Bash
```


---

## undefine var operation

```bash
unset VAR
echo "undefine VAR: ${VAR}"             # undefine VAR: 
echo "\${VAR:=value}: ${VAR:=value}"    # ${VAR:=value}: value
echo "VAR: ${VAR}"                      # VAR: value
```

```bash
unset VAR
echo "undefine VAR: ${VAR}"             # undefine VAR: 
echo "\${VAR:-value}: ${VAR:-value}"    # ${VAR:-value}: value
echo "VAR: ${VAR}"                      # VAR:
```

```bash
unset VAR
echo "undefine VAR: ${VAR}"             # undefine VAR: 
echo "\${VAR:+value}: ${VAR:+value}"    # ${VAR:+value}: 
echo "VAR: ${VAR}"                      # VAR:
```

```bash
unset VAR
echo "undefine VAR: ${VAR}"
#echo "VAR:?value ${VAR:?value}"  # show err
echo "VAR: ${VAR}"
echo
```


---

## array

```bash
declare -a ARR
ARR=(eth0 em1)
ARR+=(en0)
echo "ARR Length: ${#ARR[@]}"

# loop
for ITEM in ${ARR[*]}; do
  echo "ITEM: $ITEM"
done

for ((i=0; i < ${#ARR[@]}; i++)); do
  echo "Index: $i, ITEM: ${ARR[$i]}"
done

# append
A1=(1 2 3 X)
A2=(a b c X)
A3=(${A1[@]} ${A2[*]})

# string to array
S=1,2,3,4
A=(`echo $S | sed 's/,/ /g'`)

# function
show_array() {
  local -n arr=$1

  for i in "${arr[@]}"; do
    echo "$i"
  done
}
show_array ARR
```


---

## associative array

```bash
declare -A MAP
MAP=([eth0]=192.168.0.1 [em1]=172.16.0.1)
echo "MAP Length: ${#MAP[@]}"

# loop
for KEY in ${!MAP[@]}; do
  echo "KEY: $KEY, VALUE: ${MAP[$KEY]}"
done

# function
show_associative_array() {
  local -n ass_arr=$1

  for k in ${!ass_arr[@]}; do
    echo "key: $k -> val: ${ass_arr[$k]}"
  done
}
show_associative_array MAP
```
