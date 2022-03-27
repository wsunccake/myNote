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