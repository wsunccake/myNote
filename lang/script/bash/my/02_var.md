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
