# chapter 04

## calendar

```python
import calendar

print(calendar.month(2019, 5))

print(calendar.isleap(2020))
```


---

## datetime

```python
import datetime

print(datetime.date.today())

print(datetime.datetime.now())

d = datetime.datetime.now()
print(d.hour)
print(d.minute)
print(d.second)

today = datetime.date.today()
birth = datetime.date(1971,2,2)
print(today-birth)
```


---

## random

```python
import random

r = random.random()
print(r)

r = random.randint(1, 6)
print(r)

jan = random.choice(["石頭", "剪刀", "布"])
print(jan)

cnt = 0
while True:
    r = random.randint(1, 100)
    print(r)
    cnt = cnt + 1
    if r == 77:
        break
print("於第"+str(cnt)+"次抽中超稀有角色")
```
