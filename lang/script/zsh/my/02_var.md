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