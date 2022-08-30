# coroutine

## yield

### next / send

```python
def producer():
    while True:
        data = random.randint(0, 9)
        print('produce', data)
        yield data

def consumer():
    while True:
        data = yield
        print('consume', data)

p = producer()
c = consumer()
c.__next__()        # __next__

jobs = 3
for i in range(jobs):
    data = next(p)  # next
    c.send(data)    # send
```


### yield from

```python
for v in g:
    yield v
-->
yield from g
```


```python
def reader():
    """A generator that fakes a read from a file, socket, etc."""
    for i in range(4):
        yield '<< %s' % i

def reader_wrapper(g):
    # Manually iterate over data produced by reader
    for v in g:
        yield v

wrap = reader_wrapper(reader())
for i in wrap:
    print(i)
# << 0
# << 1
# << 2
# << 3

def reader_wrapper2(g):
    yield from g

wrap2 = reader_wrapper2(reader())
for i in wrap2:
    print(i)
# << 0
# << 1
# << 2
# << 3
```


### async

```python
import random

def consumer(name):
    while True:
        data = yield
        print(f'{name} -> {data}')

def producer(consumers, n):
    [next(c) for c in consumers]

    for _ in range(n):
        [c.send(random.randint(0, 9)) for c in consumers]

con1 = consumer('j1')
con2 = consumer('j2')
cons = [con1, con2]
producer(cons, 5)
```


---

## greenlet

```python
from greenlet import greenlet

def test1():
    print("[gr1] main  -> test1")
    gr2.switch()
    print("[gr1] test1 <- test2")
    return 'test1 done'

def test2():
    print("[gr2] test1 -> test2")
    gr1.switch()
    print("This is never printed.")

gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr1.switch()
# [gr1] main  -> test1
# [gr2] test1 -> test2
# [gr1] test1 <- test2

print(gr1.dead)     # True
print(gr2.dead)     # False
```

```python
from greenlet import greenlet

def test1():
    gr1.parent = gr2
    print("[gr1] main  -> test1")
    gr2.switch()
    print("[gr1] test1 <- test2")
    return 'test1 done'

def test2():
    print("[gr2] test1 -> test2")
    gr1.switch()
    print("This is never printed.")

gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr1.switch()
# [gr1] main  -> test1
# [gr2] test1 -> test2
# [gr1] test1 <- test2
# This is never printed.

print(gr1.dead)     # True
print(gr2.dead)     # True
```


---

## gevent

```python
import random
import gevent

def play(name, n):
    print(f'start to play {name}, {n}')
    gevent.sleep(n)
    print(f'finsh to play {name}, {n}')

p1 = gevent.spawn(play, 'p1', random.randint(0, 9))
p2 = gevent.spawn(play, 'p2', random.randint(0, 9))
p1.join()
p2.join()
```


---

## asyncio

```python
import asyncio
import datetime
import random

async def hello(name, n):
    print(f'start to hello {name}, {n}')
    await asyncio.sleep(n)
    print(f'finsh to hello {name}, {n}')

# asyncio run
print('begin: {}'.format(datetime.datetime.now()))
asyncio.run(hello('python', random.randint(0, 9)))
asyncio.run(hello('async', random.randint(0, 9)))
print('end: {}'.format(datetime.datetime.now()))

# asyncio run with await / async
async def run():
    await hello('python', random.randint(0, 9))
    await hello('async', random.randint(0, 9))

print('begin: {}'.format(datetime.datetime.now()))
asyncio.run(run())
print('end: {}'.format(datetime.datetime.now()))

# event loop
print('begin: {}'.format(datetime.datetime.now()))
event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(hello('python', random.randint(0, 9)))
event_loop.run_until_complete(hello('async', random.randint(0, 9)))
event_loop.close()
print('end: {}'.format(datetime.datetime.now()))

# event loop with task
print('begin: {}'.format(datetime.datetime.now()))
event_loop = asyncio.get_event_loop()
tasks = [event_loop.create_task(hello('python', random.randint(0, 9))), event_loop.create_task(hello('async', random.randint(0, 9)))]
event_loop.run_until_complete(asyncio.wait(tasks))
event_loop.close()
print('end: {}'.format(datetime.datetime.now()))

# event loop with future
async def hello_future(name, n, fut):
    print(f'start to hello {name}, {n}')
    await asyncio.sleep(n)
    print(f'finsh to hello {name}, {n}')
    fut.set_result('stop hello')

async def run():
    loop = asyncio.get_running_loop()
    fut1 = loop.create_future()
    fut2 = loop.create_future()
    loop.create_task(hello_future('python', random.randint(0, 9), fut1))
    loop.create_task(hello_future('async', random.randint(0, 9), fut2))
    await fut1
    await fut2
    fut1.result()
    fut2.result()

asyncio.run(run())
```


---

# ref

[Python asyncio 從不會到上路](https://myapollo.com.tw/zh-tw/begin-to-asyncio/  # Coroutines-%EF%BC%88%E6%88%96%E7%A8%B1%E5%8D%94%E7%A8%8B%EF%BC%89)
