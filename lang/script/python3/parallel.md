# thread


## function

```python
import threading
import random
import time
import datetime


def func(index):
    sleep_time = random.randint(1, 5)
    print("func call by thread {} and name {}, {}".format(index, threading.currentThread().getName(), datetime.datetime.now()))
    time.sleep(sleep_time)
    print("func call by thread {} and sleep {} second, {}".format(index, sleep_time, datetime.datetime.now()))


threads = []

for i in range(5):
    t = threading.Thread(target=func, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

threading.Thread().start(): 開始執行 thread

threading.Thread().join(): 等待 thread 結束


## class

```python
import threading
import random
import time
import datetime


class MyThread(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = index

    def run(self):
        sleep_time = random.randint(1, 5)
        print("class call by thread {} and name {}, {}".format(self.index, threading.currentThread().getName(), datetime.datetime.now()))
        time.sleep(sleep_time)
        print("class call by thread {} and sleep {} second, {}".format(self.index, sleep_time, datetime.datetime.now()))


threads = []

for i in range(5):
    t = MyThread(i)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

overwrite run()


## lock

```python
import threading
import datetime

resource_with_lock = 0
resource_without_lock = 0
COUNT = 1000000

lock = threading.Lock()


def increment_with_lock():
    global resource_with_lock
    for i in range(COUNT):
        lock.acquire()
        # print("increment_with_lock: {}, {}, {}".format(threading.currentThread().getName(), resource_with_lock,
        #                                                datetime.datetime.now()))
        resource_with_lock += 1
        lock.release()


def decrement_with_lock():
    global resource_with_lock
    for i in range(COUNT):
        lock.acquire()
        # print("decrement_with_lock: {}, {}, {}".format(threading.currentThread().getName(), resource_with_lock,
        #                                                datetime.datetime.now()))
        resource_with_lock -= 1
        lock.release()


def increment_without_lock():
    global resource_without_lock
    for i in range(COUNT):
        # print("increment_without_lock: {}, {}, {}".format(threading.currentThread().getName(), resource_without_lock,
        #                                                   datetime.datetime.now()))
        resource_without_lock += 1


def decrement_without_lock():
    global resource_without_lock
    for i in range(COUNT):
        # print("decrement_without_lock: {}, {}, {}".format(threading.currentThread().getName(), resource_without_lock,
        #                                                   datetime.datetime.now()))
        resource_without_lock -= 1


works = []
works.append(threading.Thread(target=increment_with_lock))
works.append(threading.Thread(target=decrement_with_lock))
works.append(threading.Thread(target=increment_without_lock))
works.append(threading.Thread(target=decrement_without_lock))

for work in works:
    work.start()

for work in works:
    work.join()

print(resource_with_lock)
print(resource_without_lock)
```

`unlocked`

```python
import threading


lock = threading.Lock()
lock.release()     # RuntimeError: release unlocked lock
```

`deadlock`

```python
import threading


lock = threading.Lock()
lock.acquire()
lock.acquire()     # block
lock.release()
```

threading.Lock().acquire()

threading.Lock().release()


## rlock

```python
import threading


lock = threading.RLock()
lock.acquire()
lock.acquire()
lock.release()
lock.release()
```


## semaphore

```python
import datetime
import random
import threading
import time

semaphore = threading.Semaphore(2)


def func(index):
    semaphore.acquire()
    sleep_time = random.randint(1, 5)
    print("func call by thread {} and name {}, {}".format(index, threading.currentThread().getName(), datetime.datetime.now()))
    time.sleep(sleep_time)
    print("func call by thread {} and sleep {} second, {}".format(index, sleep_time, datetime.datetime.now()))
    semaphore.release()


threads = []

for i in range(5):
    t = threading.Thread(target=func, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

threading.Semaphore(n), n >= 0

threading.Semaphore(n).acquire(), => -1

threading.Semaphore(n).release(), => +1



## condition

```python
import datetime
import random
import threading
import time

items = []
condition = threading.Condition()


class Producer(threading.Thread):
    global condition
    global items

    def __init__(self):
        # threading.Thread.__init__(self)
        super().__init__()

    def run(self):
        condition.acquire()
        for i in range(5):
            sleep_time = random.randint(1, 5)
            print("Producer: {}, sleep: {}, {}".format(threading.currentThread().getName(), sleep_time, datetime.datetime.now()))
            items.append(sleep_time)
        condition.notify()
        condition.release()


class Consumer(threading.Thread):
    global condition
    global items

    def __init__(self):
        # threading.Thread.__init__(self)
        super().__init__()

    def run(self):
        condition.acquire()
        if len(items) <= 0:
            condition.wait()
            condition.notify()
        condition.release()

        item = items.pop()
        print("Consumer: {}, {}".format(threading.currentThread().getName(), datetime.datetime.now()))
        time.sleep(item)
        print("Consumer: {}, sleep: {}, {}".format(threading.currentThread().getName(), item, datetime.datetime.now()))
        

workers = []

for i in range(5):
    c = Consumer()
    c.start()
    workers.append(c)

p = Producer()
p.start()
workers.append(p)

for worker in workers:
    worker.join()

print(items)
```

threading.Condition().acquire()

threading.Condition().wait()

threading.Condition().notify()

threading.Condition().release()


## event

```python
import datetime
import random
import threading
import time

items = []
event = threading.Event()


class Producer(threading.Thread):
    global items

    def __init__(self, event):
        threading.Thread.__init__(self)
        self.event = event

    def run(self):
        for i in range(10):
            sleep_time = random.randint(1, 5)
            print("Producer: {}, sleep: {}, {}".format(threading.currentThread().getName(), sleep_time, datetime.datetime.now()))
            items.append(sleep_time)
        self.event.set()
        self.event.clear()


class Consumer(threading.Thread):
    global items

    def __init__(self, event):
        threading.Thread.__init__(self)
        self.event = event

    def run(self):
        if len(items) <= 0:
            self.event.wait()

        item = items.pop()
        print("Consumer: {}, {}".format(threading.currentThread().getName(), datetime.datetime.now()))
        time.sleep(item)
        print("Consumer: {}, sleep: {}, {}".format(threading.currentThread().getName(), item, datetime.datetime.now()))


workers = []

for i in range(5):
    c = Consumer(event)
    c.start()
    workers.append(c)

p = Producer(event)
p.start()
workers.append(p)

for worker in workers:
    worker.join()

print(items)
```

threading.Event().set()

threading.Event().clear()

threading.Event().wait()


## with

with => acquire(), release()

`lock` or `rlock`

```python
import threading
import datetime

resource_with_lock = 0
COUNT = 1000000

lock = threading.Lock()


def increment_with_lock():
    global resource_with_lock
    for i in range(COUNT):
        with lock:
            resource_with_lock += 1


def decrement_with_lock():
    global resource_with_lock
    for i in range(COUNT):
        with lock:
            resource_with_lock -= 1


works = []
works.append(threading.Thread(target=increment_with_lock))
works.append(threading.Thread(target=decrement_with_lock))

for work in works:
    work.start()

for work in works:
    work.join()

print(resource_with_lock)
```

`semaphore`

```python
import datetime
import random
import threading
import time

semaphore = threading.Semaphore(2)


def func(index):
    with semaphore:
        sleep_time = random.randint(1, 5)
        print("func call by thread {} and name {}, {}".format(index, threading.currentThread().getName(), datetime.datetime.now()))
        time.sleep(sleep_time)
        print("func call by thread {} and sleep {} second, {}".format(index, sleep_time, datetime.datetime.now()))


threads = []

for i in range(5):
    t = threading.Thread(target=func, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

`condition`

```python
import datetime
import random
import threading
import time

items = []
condition = threading.Condition()


class Producer(threading.Thread):
    global condition
    global items

    def __init__(self):
        # threading.Thread.__init__(self)
        super().__init__()

    def run(self):
        with condition:
            for i in range(5):
                sleep_time = random.randint(1, 5)
                print("Producer: {}, sleep: {}, {}".format(threading.currentThread().getName(), sleep_time, datetime.datetime.now()))
                items.append(sleep_time)
            condition.notify()


class Consumer(threading.Thread):
    global condition
    global items

    def __init__(self):
        # threading.Thread.__init__(self)
        super().__init__()

    def run(self):
        with condition:
            if len(items) <= 0:
                condition.wait()
                condition.notify()
            
        item = items.pop()
        print("Consumer: {}, {}".format(threading.currentThread().getName(), datetime.datetime.now()))
        time.sleep(item)
        print("Consumer: {}, sleep: {}, {}".format(threading.currentThread().getName(), item, datetime.datetime.now()))


workers = []

for i in range(5):
    c = Consumer()
    c.start()
    workers.append(c)

p = Producer()
p.start()
workers.append(p)

for worker in workers:
    worker.join()

print(items)
```


## barrier

```python
import datetime
import random
import threading
import time

items = []
barrier = threading.Barrier(5+1)


class Producer(threading.Thread):
    global condition
    global items

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        for i in range(5):
            sleep_time = random.randint(1, 5)
            print("Producer: {}, sleep: {}, {}".format(threading.currentThread().getName(), sleep_time, datetime.datetime.now()))
            items.append(sleep_time)
        barrier.wait()


class Consumer(threading.Thread):
    global condition
    global items

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        if len(items) <= 0:
            barrier.wait()

        item = items.pop()
        print("Consumer: {}, {}".format(threading.currentThread().getName(), datetime.datetime.now()))
        time.sleep(item)
        print("Consumer: {}, sleep: {}, {}".format(threading.currentThread().getName(), item, datetime.datetime.now()))


workers = []

for i in range(5):
    c = Consumer()
    c.start()
    workers.append(c)

p = Producer()
p.start()
workers.append(p)

for worker in workers:
    worker.join()

print(items)
```

threading.Barrier(n)

threading.Barrier(n).wait


## queue

```python
import threading
import queue
import random
import time
import datetime


class Producer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        for i in range(5):
            sleep_time = random.randint(1, 5)
            print("Producer: {}, sleep: {}, {}".format(threading.currentThread().getName(), sleep_time, datetime.datetime.now()))
            self.queue.put(sleep_time)


class Consumer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        if self.queue.qsize() > 0:
            item = self.queue.get()
            print("Consumer: {}, {}".format(threading.currentThread().getName(), datetime.datetime.now()))
            time.sleep(item)
            print("Consumer: {}, sleep: {}, {}".format(threading.currentThread().getName(), item, datetime.datetime.now()))


q = queue.Queue()

p = Producer(q)
p.start()
p.join()

consumers = []

for i in range(5):
    c = Consumer(q)
    c.start()
    consumers.append(c)

for c in consumers:
    c.join()
```

queue.put(), queue.get()


## pool

```python
import threading
import random
import time
import datetime

import concurrent.futures


def func(index):
    sleep_time = random.randint(1, 5)
    print("func call by thread {} and name {}, {}".format(index, threading.currentThread().getName(), datetime.datetime.now()))
    time.sleep(sleep_time)
    print("func call by thread {} and sleep {} second, {}".format(index, sleep_time, datetime.datetime.now()))


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(func, i) for i in range(5)]

    for future in concurrent.futures.as_completed(futures):
        print(future.result())


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(func, range(5))
```

concurrent.futures.ThreadPoolExecutor().submit()

concurrent.futures.ThreadPoolExecutor().map()

concurrent.futures.ThreadPoolExecutor().shutdown()

concurrent.futures.as_completed()


---

# process

`function`

```python
import multiprocessing
import random
import time
import datetime


def func(index):
    sleep_time = random.randint(1, 5)
    print("func call by thread {} and name {}, {}".format(index, multiprocessing.current_process().name, datetime.datetime.now()))
    time.sleep(sleep_time)
    print("func call by thread {} and sleep {} second, {}".format(index, sleep_time, datetime.datetime.now()))


processes = []

for i in range(5):
    p = multiprocessing.Process(target=func, args=(i,))
    processes.append(p)
    p.start()

for p in processes:
    p.join()
```

---

# async

## type

```python
# function
def fun1():
    return 1

print(fun1)
print(fun1())

# generator
def fun2():
    yield 1

print(fun2)
print(fun2())

# generator
def fun3():
    yield from 1

print(fun3)
print(fun3())

# await
def fun4():
    await 1

print(fun4)
print(fun4())

# coroutine
async def afun1():
    return 1

print(afun1)
print(afun1())

# async_generator
async def afun2():
    yield 1

print(afun2)
print(afun2())

# yield from
async def afun3():
    yield from 1

print(afun3)
print(afun3())

# coroutine
async def afun4():
    await 1

print(afun4)
print(afun4())
```


## coroutine/future

```python
import asyncio
import datetime


async def async_hello(index='hello', sleep_time=1):
    print('{}, begin: {}'.format(index, datetime.datetime.now()))
    await asyncio.sleep(sleep_time)
    print('{}, finish: {}'.format(index, datetime.datetime.now()))

# run as task in event loop
async def loop_stop(loop, sleep_time=1):
    await asyncio.sleep(sleep_time)
    loop.stop()

print(async_hello())
```

`coroutine/future`

```python
print('begin: {}'.format(datetime.datetime.now()))
asyncio.run(async_hello('python', 2))
asyncio.run(async_hello('async', 2))
print('end: {}'.format(datetime.datetime.now()))
```

`coroutine/future in event loop`

```python
print('begin: {}'.format(datetime.datetime.now()))
event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(async_hello('python', 2))
event_loop.run_until_complete(async_hello('async', 2))
event_loop.close()
print('end: {}'.format(datetime.datetime.now()))
```


## task

`task`

```python
print('begin: {}'.format(datetime.datetime.now()))
event_loop = asyncio.get_event_loop()
tasks = [event_loop.create_task(async_hello('python', 2)), event_loop.create_task(async_hello('python', 2))]
event_loop.run_until_complete(asyncio.wait(tasks))
event_loop.close()
print('end: {}'.format(datetime.datetime.now()))
```

create_task (3.7) -> ensure_future (3.6)

`event status`


```python
print('begin: {}'.format(datetime.datetime.now()))
event_loop = asyncio.get_event_loop()
event_loop.create_task(async_hello('python', 2))
event_loop.create_task(async_hello('async', 2))
event_loop.create_task(loop_stop(event_loop, 2))
event_loop.run_forever()
event_loop.close()
print('end: {}'.format(datetime.datetime.now()))
```


## nested

```python
import asyncio
import datetime


async def async_hello(index='hello', sleep_time=1):
    print('{}, begin: {}'.format(index, datetime.datetime.now()))
    await asyncio.sleep(sleep_time)
    print('{}, finish: {}'.format(index, datetime.datetime.now()))


async def async_main():
    print('{}, begin: {}'.format('main', datetime.datetime.now()))
    await async_hello('hello')
    await async_hello('world')
    print('{}, finish: {}'.format('main', datetime.datetime.now()))


print('begin: {}'.format(datetime.datetime.now()))
asyncio.run(async_main())
print('end: {}'.format(datetime.datetime.now()))
```


---

# mpi


---

# mq


---

# ref

[Python Parallel Programming Cookbook - Second Edition](https://github.com/PacktPublishing/Python-Parallel-Programming-Cookbook-Second-Edition)

[python-parallel-programmning-cookbook](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/)

[平行處理](https://chenhh.gitbooks.io/parallel_processing/content/)
