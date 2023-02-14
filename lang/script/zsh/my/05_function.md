# function

## define function

```zsh
# method 1
hi() {
    echo "hi"
}

# method 2
function hello() {
    echo "hello"
}

# call function
hi
hello

# unset function
unfuntion hello
hello
```

---

## argument

```zsh
foo() {
    echo "$1, $2, $3"
    echo "arg num: $#"

    # $*: 全部 argument
    for i ($*) {
        echo "arg: $i"
    }

    # if n arg exist
    (($+1)) && {
        echo "arg 1: $1"
    }
}

foo A z 1
# a, Z, 1
# arg num: 3
# arg: a
# arg: Z
# arg: 1
# arg 1: a

foo
# , ,
# arg num: 0

array=(A z 0)
foo $array
# A, z, 0
# arg num: 3
# arg: A
# arg: z
# arg: 0
# arg 1: A
```

---

## return

```zsh
foo() {

    (($+1)) && {
        return 0
    }
    return 1
}

foo && echo "good" || echo "bad"
foo abc && echo "good" || echo "bad"
# return 並非回傳值, 而是結束 function 的狀態
# 0: true, non-0: false
```

---

## local

```zsh
foo() {
    var=$1
    echo "foo var: $var"
    var+="!!"
}

var=abc
echo "before foo var: $var"     # before foo var: abc
foo $var                        # foo var: abc
echo "after foo var: $var"      # after foo var: abc!!

goo() {
    local var=$1
    echo "goo var: $var"
    var+="??"
}

var=ABC
echo "before goo var: $var"     # before goo var: ABC
goo $var                        # goo var: ABC
echo "after goo var: $var"      # after goo var: ABC
```

---

## getopts
