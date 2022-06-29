# new feature/syntax

## 3.4

###  ensurep module

include pip


---

## 3.5

### coroutines with async and await

```python
import asyncio

async def http_get(domain):
    reader, writer = await asyncio.open_connection(domain, 80)

    writer.write(b'\r\n'.join([
        b'GET / HTTP/1.1',
        b'Host: %b' % domain.encode('latin-1'),
        b'Connection: close',
        b'', b''
    ]))

    async for line in reader:
        print('>>>', line)

    writer.close()

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(http_get('example.com'))
finally:
    loop.close()
```

```python
import asyncio

async def coro(name, lock):
    print('coro {}: waiting for lock'.format(name))
    async with lock:
        print('coro {}: holding the lock'.format(name))
        await asyncio.sleep(1)
        print('coro {}: releasing the lock'.format(name))

loop = asyncio.get_event_loop()
lock = asyncio.Lock()
coros = asyncio.gather(coro(1, lock), coro(2, lock))
try:
    loop.run_until_complete(coros)
finally:
    loop.close()
```


### infix operator for matrix multiplication

```python
import numpy

x = numpy.ones(3)
x      # array([ 1., 1., 1.])

m = numpy.eye(3)
m      # array([[ 1., 0., 0.],
       #        [ 0., 1., 0.],
       #        [ 0., 0., 1.]])

x @ m  # array([ 1., 1., 1.])
```


### unpacking generalization

```python
print(*[1], *[2], 3, *[4, 5])                # 1 2 3 4 5

def fn(a, b, c, d):
    print(a, b, c, d)
fn(**{'a': 1, 'c': 3}, **{'b': 2, 'd': 4})   # 1 2 3 4

print(*[1], *[2], 3, *[4, 5])                # 1 2 3 4 5

def fn(a, b, c, d):
    print(a, b, c, d)
fn(**{'a': 1, 'c': 3}, **{'b': 2, 'd': 4})   # 1 2 3 4
```


## type hints

typing module

```python
def greeting(name: str) -> str:
    return 'Hello ' + name
```


---

# 3.6

### formatted string literal

f-strings or formatted string literals

```python
name = "Fred"
f"He said his name is {name}."    #'He said his name is Fred.'
width = 10
precision = 4
value = decimal.Decimal("12.34567")
f"result: {value:{width}.{precision}}"  # nested fields  'result:      12.35'

# binary
f"{0x3:b}"          # '11'
f"{0x3:8b}"         # '      11'
f"{0x3:08b}"        # '00000011'
```


### variable annotation

mypy, pytype module

```python
primes: List[int] = []

captain: str           # Note: no initial value

class Starship:
    stats: Dict[str, int] = {}
```


### underscores in numeric literal

```python
1_000_000_000_000_000        # 1000000000000000
0x_FF_FF_FF_FF               # 4294967295
'{:_}'.format(1000000)       # '1_000_000'
'{:_x}'.format(0xFFFFFFFF)   # 'ffff_ffff'
```


### asynchronous generator

```python
async def ticker(delay, to):
    """Yield numbers from 0 to *to* every *delay* seconds."""
    for i in range(to):
        yield i
        await asyncio.sleep(delay)
```

### asynchronous comprehension

```python
result = [i async for i in aiter() if i % 2]
result = [await fun() for fun in funcs if await condition()]
```


---

## 3.7

### ostponed Evaluation of Annotation

```python
from __future__ import annotations

class Foo:
    def make_foo() -> Foo:
        return Foo()
```


---

## 3.8


### assignment expressions

:= (walrus)

```python
if (n := len(a)) > 10:
    print(f"List is too long ({n} elements, expected <= 10)")

discount = 0.0
if (mo := re.search(r'(\d+)% discount', advertisement)):
    discount = float(mo.group(1)) / 100.0
```


### positional-only parameters

```python
def f(a, b, /, c, d, *, e, f):
    print(a, b, c, d, e, f)

f(10, 20, 30, d=40, e=50, f=60)
f(10, b=20, c=30, d=40, e=50, f=60)   # b cannot be a keyword argument
f(10, 20, 30, 40, 50, f=60)           # e must be a keyword argument
```

## f-strings

```python
user = 'eric_idle'
member_since = date(1975, 7, 31)
f'{user=} {member_since=}'                       # "user='eric_idle' member_since=datetime.date(1975, 7, 31)"

delta = date.today() - member_since
f'{user=!s}  {delta.days=:,d}'                   # 'user=eric_idle  delta.days=16,075'

print(f'{theta=}  {cos(radians(theta))=:.3f}')   # theta=30  cos(radians(theta))=0.866
```

---

## ref

[What’s New in Python](https://docs.python.org/3/whatsnew/index.html)

