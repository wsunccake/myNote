# function

## def

```bash
linux:~ # cat myswap01.py
def change(arg1, arg2):             # define function
    print("before: arg1: ", arg1, "arg2: ", arg2)
    (arg1, arg2) = (arg2 ,arg1)
    print("after: arg1: ", arg1, "arg2: ", arg2)
    return (arg1, arg2)             # return value

if __name__ == "__main__":          # define main function
    change("A", "B")

linux:~ # cat mymain01.py
import sys
# sys.path.append('modulepath')       # 指定 module path, 定義 sys.path 即可
import myswap01                     # 載入 myswap01.py, myswap01.py 和 mymain01.py 同資料夾或是定義在 PYTHONPATH 或 sys.path

if __name__ == "__main__":
    A = 3
    B = 1
    print "A: ", A, ", B: ", B
    (C, D) = myswap01.change(A, B)  # 使用 myswap01.py 裡的 chnage 函式
    print "A: ", A, ", B: ", B
    print "C: ", C, ", D: ", D
```


---

## nest def

```python
def fn1(m):
    print(f"{fn1.__name__} {m}")

def fn2(m):
    print(f"{fn2.__name__} {m}")

    def fn3(n):
        print(f"{fn3.__name__} {m} -> {n} in {fn2.__name__}")

    return fn3

fn1("aaa")
ff = fn2("bbb")
ff('ccc')

gg = fn2("bbb")
gg.__name__ = "gg"
gg('ccc')
```


---

##  *args, **kwargs

```python
def person(name = "NoName", *desc , **data):    # name = "NoName" default value, *desc 是傳入 tuple, **data 則是傳入 dict
    print ("Name: %s" %name)
    for k in data.keys():
        print("%s: %s" %(k, data[k]))
    for s in desc:
        print(s)

if __name__ == "__main__":
    myStory='''I'm student.
I live in Taiei.'''.split('\n')
    myData = {"sex":"female", "age":"15"}

    person("May", *myStory, **myData)           # 參數使用方式
```


---

## lambda

```python
my_sum = lambda x, y: x + y
print(my_sum(1, 3))

my_greater_than = lambda x, y: x if x > y else y
print(my_greater_than(7, 3))

round_up = lambda x, y: int(x / y) + (x % y > 0)
round_down = lambda x, y: int(x / y)
round_half = lambda x, y: int(x / y + 0.5)
```

```python
x = 10
a = lambda y: x + y
x = 20
b = lambda y: x + y
a(10)
b(10)
```

```python
x = 10
a = lambda y, x=x: x + y
x = 20
b = lambda y, x=x: x + y
a(10)
b(10)
```


---

## decorator

`simple decorator`

```python
def greet(function):
    print('Hello')
    return function

def greet_someone1(someone):
    print(someone)
greet_someone1 = greet(greet_someone1)

@greet
def greet_someone2(someone):
    print(someone)

greet_someone1('John')
print(greet_someone1.__name__)
greet_someone2('Mary')
print(greet_someone2.__name__)
```

`decorator without argument`

```python
def greet(function):
    def wrapper(name):
        print('Hello')
        return function(name)
    return wrapper

def greet_someone1(someone):
    print(someone)
greet_someone1 = greet(greet_someone1)

@greet
def greet_someone2(someone):
    print(someone)

greet_someone1('John')
print(greet_someone1.__name__)
greet_someone2('Mary')
print(greet_someone2.__name__)
```

`decorator with argument`

```python
def greet(arg = 'Hello'):
    def decorator(function):
        def wrapper(name):
            print(arg)
            return function(name)
        return wrapper
    return decorator

@greet('Hi')
def greet_someone(someone):
    print(someone)

greet_someone('John')
print(greet_someone.__name__)
greet_someone('Mary')
print(greet_someone.__name__)
```

`functool decorator without argument`

```python
import functools

def greet(function):
    @functools.wraps(function)
    def wrapper(name):
        print('Hello')
        return function(name)
    return wrapper

@greet
def greet_someone(someone):
    print(someone)

greet_someone('John')
print(greet_someone.__name__)
```

`functool decorator with argument`

```python
import functools

def greet(arg = 'Hello'):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(name):
            print(arg)
            return function(name)
        return wrapper
    return decorator

@greet()
def greet_someone(someone):
    print(someone)

greet_someone('John')
print(greet_someone.__name__)
```


---

## comment

```python
def add1(x, y):
    return x + y

def add2(x:int, y:int) -> int:
    return x + y
```
