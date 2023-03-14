# string

## basic

```zsh
str0=abc123XYZ

echo "raw: ${str0}"         # raw: abc123XYZ
echo "len: ${#str0}"        # len: 9
echo "upper: ${(U)str0}"    # upper: ABC123XYZ
echo "lower: ${(L)str0}"    # lower: abc123xyz
echo "cap: ${(C)str0}"      # cap: Abc123xyz

str1="hello ${str0}"
str0+="!"
echo "concat: $str1"                        # concat: hello abc123XYZ
echo "+=: $str0"                            # +=: abc123XYZ!

echo "slice: ${str0[1,3]}"                  # slice: abc
echo "slice: ${str0:1:3} (bash style)"      # slice: bc1 (bash style)
```

```zsh
str0=abc123XYZ
pattern=b
echo "raw: ${str0}"                                         # raw: abc123XYZ
echo "pattern: ${pattern}"                                  # pattern: b

s=${str0[(i)${patter}]}
S=${str0[(I)${patter}]}
echo "from left to right: \$str0[(i)\${patter}]} -> $s"     # from left to right: $str0[(i)${patter}]} -> 1
echo "from right to left: \$str0[(I)\${patter}]} -> $S"     # from right to left: $str0[(I)${patter}]} -> 10
```

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
