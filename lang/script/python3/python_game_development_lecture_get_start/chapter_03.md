# chapter 03

## variable

```python
score = 0
print(score)
score = score + 100
print(score)

job = "菜鳥劍士"
print("你的職業是："+job)
print("轉職了！")
job = "初出茅盧的勇者"
print("你的新職業是："+job)
```


---

## list

```python
enemy = ["史萊姆", "骷髏士兵", "魔法師"]
print(enemy[0])
print(enemy[1])
print(enemy[2])
```


---

## condition

```python
life = 0
if life <= 0:
    print("遊戲結束")
if life > 0:
    print("遊戲繼續")

gold = 100
if gold == 0:
    print("身上的錢是零元")
else:
    print("要買東西嗎？")
```


---

## loop

```python
for i in range(10):
    print(i)

for i in range(1, 5):
    print(i)

for i in range(10, 0, -2):
    print(i)

i = 0
while i < 5:
    print(i)
    i = i + 1
```


---

## function

```python
def win():
    print("你獲勝了！")

win()

def recover(val):
    print("你的體力")
    print(val)
    print("恢復了！")

recover(100)

def add(a, b):
    return a+b

c = add(1, 2)
print(c)
```
