# other

## PYTHONAPTH

在 bash env 設定 PYTHONPATH

```bash
linux:~ $ export PYTHONPATH=$(pwd):$PYTHONPATH
linux:~ $ echo $PYTHONPATH
```


在 python code 設定 PYTHONPATH

```python
import os
import sys

print(f'os.getcwd: {os.getcwd()}')
print(f"os.getenv: {os.getenv('PYTHONPATH')}")
### if no set PYTHONPATH env var, run os.environ to show KeyError
# print(f"os.environ: {os.environ['PYTHONPATH']}")

# append PYTHONPATH
sys.path.append(os.getcwd())
print(f"os.getenv: {os.getenv('PYTHONPATH')}")

import xxx
...
```


---

## globals

顯示所以以定義的 variable

```python
def add(x, y):
    return x+y

print(globals())
for k, v in dict(globals()).items():
    print(f'{k} -> {v}, {type(v)}')
```


動態宣告變數

```python
globals()['var'] = 'var'
print(var)
```


---

## inspect

```python
import inspect

def add(x, y):
    return x+y

max_value = lambda x, y: x if x > y else y

for k, v in dict(globals()).items():
    if inspect.isfunction(v):
        print(k)
        print(inspect.getsource(v))
```


---

## timestamp

```python
import datetime
import time

now = datetime.datetime.now()
now_timestamp = datetime.datetime.timestamp(now)
print(now, now_timestamp)
```


---

## infinite

```python
positive_infinity = float('inf')
negative_infinity = float('-inf')
```

```python
import math

positive_infinity = math.inf
negative_infinity = -math.inf
```

```python
from decimal import Decimal

positive_infinity = Decimal('Infinity')
negative_infinity = Decimal('-Infinity')
```

```python
import numpy as np

positive_infinity = np.inf
negative_infinity = -np.inf
```


---

## class

```python
class Shark():
    # class attribute / class member / class variable
    age = 0
    location = ['ocean']

    def __init__(self, name='') -> None:
        # instance attribute / instance member / instance variable
        self.name = name

    def pass_year(self, y=1):
        self.age = y + self.age


if '__main__' == __name__:
    s1 = Shark('s1')
    s2 = Shark('s2')

    print(f'Shark: {Shark.age} {Shark.location}')
    print(f's1: {s1.name}  {s1.age} {s1.location}')
    print(f's2: {s2.name} {s2.age} {s2.location}')

    print(f'Shark: {dir(Shark)} {Shark.__dict__}')
    print(f's1: {dir(s1)} {s1.__dict__}')
    print(f's2: {dir(s2)} {s2.__dict__}')

    s1.pass_year()
    s1.location.append('aquarium')
    s2.age = 3

    print(f'Shark: {Shark.age} {Shark.location}')
    print(f's1: {s1.name}  {s1.age} {s1.location}')
    print(f's2: {s2.name} {s2.age} {s2.location}')

    print(f'Shark: {dir(Shark)} {Shark.__dict__}')
    print(f's1: {dir(s1)} {s1.__dict__}')
    print(f's2: {dir(s2)} {s2.__dict__}')
```

instance attribute 會存在 <instance>.__dict__['variable']

clas attribute 會存在 <class>.__dict__['variable']

先找 instance attribute 沒有再找 class attribute

example:

s1.age -> s1.__dict__['age']

s1.location -> s1.__dict__['location'] -> Shark.__dict__['location']
