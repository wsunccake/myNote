# condition and loop

## if else

python 只提供 if else 判斷, 使用方式如下, 但有些時候會想使用 switch case 方式作條件式的判斷, 但 python 本身無此功能, 只能使用 elif 方式

```bash
sex = input('input your sex [m/f]: ')
if sex == 'm':
    print('Male')
elif sex == 'f':
    print('Female')
else:
    print('Unknown')

# 使用 dictionary 方法替代 switch/case
sex = {'m': 'Male', 'f': 'Female'}
print(sex.get('m', 'Unknown'))
```

當 statement 只有一行, 可以使用下面方式

```python
import platform

if platform.system() == "Linux":
    OS = "Linux"
else:
    OS = "Unknown"
print(OS)

# 另一種簡單方式的 if else 使用方式
OS = "Linux" if platform.system() else "Unknown"
print (OS)
```

and, or, not 的使用

```python
import os

# 兩個 condition 同時判斷檔案是否存在
if os.path.exists(os.path.join(os.getenv('HOME'), '.profile') ) or os.path.exists(os.path.join(os.getenv('HOME'), '.bash_profile') ) :
    print ".profile or .bashrc_profile exist"
```


---

## for

```python
list1 = ["ABC", 'xyz', 123]
# 顯示l ist 內容
for l in list1:
    print(l)

dict1 = {"A":"ABC", 'b':"xyz", "0":123}
# 顯示dictionary內容
for D in dict1.keys():
    print(dict1[D])

# 數值迴圈的使用方式
for i in range (5):
    print(i)
```


---

## list comprehension

```python
lines1 = []
for line in open('/etc/passwd'):
    lines1.append(line.rstrip())
f.close()
print(lines1)

lines2 = [line.rstrip() for line in open('/etc/passwd')]
print(lines2)

lines1 == lines2
```

配合 if

```python
S = [x**2 for x in range(10)]
V = [2**i for i in range(13)]
M = [x for x in S if x % 2 == 0]
print(S)
print(V)
print(M)

noprimes = [j for i in range(2, 8) for j in range(i*2, 50, i)]
primes = [x for x in range(2, 50) if x not in noprimes]
print(primes)
```


---

## dictionary comprehension

```python
l = [1, 2, 3]

dict1 = {}
for i in l:
    dict1[i] = i*i
print(dict1)

dict2 = {}
for i in l:
    dict2.update({i: i*i})
print(dict2)

dict3 = {i: i * i for i in l}
print(dict3)

dict4 = {k: v * v for k, v in enumerate(l)}
print(dict4)
```


---

## while

```
import sys

print("Input the word, [Quit]")
input1 = sys.stdin.readline().rstrip()

while input1 != "Quit":
    print("Your keyin: ", input1)
    input1 = sys.stdin.readline().rstrip()
```

```python
while True:
    word = input('Input the word, [Quit]')
    if word.lower() == 'quit':
        break
    elif word == '\n':
        continue
    else:
        print(word)
```


---

## match case

```python
status = 401

match status:
    case 400:
        print("bad request")
    case 401|403|404:
        print("not allow")
    case _:
        print("something else")
```

```python
point = (1, 2)

match point:
    case (0, 0):
        print("origin")
    case (0, y):
        print(f"Y={y}")
    case (x, 0):
        print(f"X={x}")
    case (x, y):
        print(f"X={x}, Y={y}")
    case _:
        raise ValueError("not a point")
```


class

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

point = Point(1, 2)

match point:
    case Point(x=0, y=0):
        print("Origin")
    case Point(x=0, y=y):
        print(f"Y={y}")
    case Point(x=x, y=0):
        print(f"X={x}")
    case Point(x=x, y=y):
        print(f"X={x}, Y={y}")
    case _:
        raise ValueError("not a point")
```

```python
from enum import Enum

class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

color = Color.RED

match color:
    case Color.RED:
        print("red")
    case Color.GREEN:
        print("green")
    case Color.BLUE:
        print("blues")
```


if

```python
score = 81

match score:
    case 100:
        print('good job')
    case score if score >= 80:
        print(f'high score {score}')
    case score if score >= 60:
        print('safe')
    case _:
        print('so sad')
```


list

```python
for thing in [[1, 2, 3], ['a', 'b', 'c'], "this won't be matched", 1, 4]:
    match thing:
        case [int(v1), int(v2), int()] as y:
            print(y, f'[1]=> {v2}')
        case [*x]:
            print(x)
        case _:
            print("unknown")
```


dict

```python
message = {'success': 'OK!'}
# message = {'failure': 'ERROR!'}

match message:
    case {'success': message}:
        print(f'success: {message}')
    case {'failure': message}:
        print(f'failure: {message}')
    case _:
        print('unknown')
```
