# chapter 05

## 猜猜看

```python
print("蠑螈太太的老公叫什麼名字？")
ans = input()
if ans == "鱒男":
    print("答對了")
else:
    print("答錯了")
```

->

```python
print("蠑螈太太的老公叫什麼名字？")
ans = input()
if ans == "鱒男" or ans == "masuo":
    print("答對了")
else:
    print("答錯了")
```

->

```python
QUESTION = [
"蠑螈太太的老公叫什麼名字？",
"磯野鰹的妹妹叫什麼名字？",
"鱈男是磯野鰹的誰？"]
R_ANS = ["鱒男", "磯野裙帶菜", "外甥"]
for i in range(3):
    print(QUESTION[i])
    ans = input()
    if ans == R_ANS[i]:
        print("答對了")
    else:
        print("答錯了")
```

->

```python
QUESTION = [
"蠑螈太太的老公叫什麼名字？",
"磯野鰹的妹妹叫什麼名字？",
"鱈男是磯野鰹的誰？"]
R_ANS = ["鱒男", "磯野裙帶菜", "外甥"]
R_ANS2 = ["masuo", "wakame", "oi"]

for i in range(3):
    print(QUESTION[i])
    ans = input()
    if ans == R_ANS[i] or ans == R_ANS2[i]:
        print("答對了")
    else:
        print("答錯了")
```


---

## 大富翁

```python
pl_pos = 6
def banmen():
    print("・"*(pl_pos-1) + "Ｐ" + "・"*(30-pl_pos))

banmen()
```

->

```python
pl_pos = 6
com_pos = 3
def banmen():
    print("・"*(pl_pos-1) + "Ｐ" + "・"*(30-pl_pos))
    print("・"*(com_pos-1) + "Ｃ" + "・"*(30-com_pos))
banmen()
```

->

```python
pl_pos = 1
com_pos = 1
def banmen():
    print("・"*(pl_pos-1) + "Ｐ" + "・"*(30-pl_pos))
    print("・"*(com_pos-1) + "Ｃ" + "・"*(30-com_pos))
while True:
    banmen()
    input("按下Enter就會前進")
    pl_pos = pl_pos + 1
    com_pos = com_pos + 2
```

->

```python
import random
pl_pos = 1
com_pos = 1
def banmen():
    print("・"*(pl_pos-1) + "Ｐ" + "・"*(30-pl_pos))
    print("・"*(com_pos-1) + "Ｃ" + "・"*(30-com_pos))
while True:
    banmen()
    input("按下Enter就會前進")
    pl_pos = pl_pos + random.randint(1,6)
    com_pos = com_pos + random.randint(1, 6)
```

->

```python
import random
pl_pos = 1
com_pos = 1
def banmen():
    print("・"*(pl_pos-1) + "Ｐ" + "・"*(30-pl_pos)+"Goal")
    print("・"*(com_pos-1) + "Ｃ" + "・"*(30-com_pos) +"Goal")

banmen()
print("大富翁開始！")
while True:
    input("按下Enter前進")
    pl_pos = pl_pos + random.randint(1,6)
    if pl_pos > 30:
        pl_pos = 30
    banmen()
    if pl_pos == 30:
        print("你獲勝了！")
        break
    input("按下Enter，換電腦前進")
    com_pos = com_pos + random.randint(1,6)
    if com_pos > 30:
        com_pos = 30
    banmen()
    if com_pos == 30:
        print("電腦獲勝！")
        break
```


---

## 缺少哪個字母

```python
ALP = ["A","B","C","D","E","F","G"]
for i in ALP:
    print(i)
```

->

```python
import random
ALP = ["A","B","C","D","E","F","G"]
r = random.choice(ALP)
alp = ""
for i in ALP:
    if i != r:
        alp = alp + i
print(alp)
```

->

```python
import random
ALP = ["A","B","C","D","E","F","G"]
r = random.choice(ALP)
alp = ""
for i in ALP:
    if i != r:
        alp = alp + i
print(alp)
ans = input("缺少哪個字母呢?")
if ans == r:
    print("答案正確")
else:
    print("答案錯誤")
```

->

```python
import random
import datetime
ALP = ["A","B","C","D","E","F","G"]
r = random.choice(ALP)
alp = ""
for i in ALP:
    if i != r:
        alp = alp + i
print(alp)
st = datetime.datetime.now()
ans = input("缺少哪個字母呢?")
if ans == r:
    print("答案正確")
    et = datetime.datetime.now()
    print((et-st).seconds)
else:
    print("答案錯誤")
```

->

```python
import random
import datetime
ALP = [
"A","B","C","D","E","F","G",
"H","I","J","K","L","M","N",
"O","P","Q","R","S","T","U",
"V","W","X","Y","Z"
]
r = random.choice(ALP)
alp = ""
for i in ALP:
    if i != r:
        alp = alp + i
print(alp)
st = datetime.datetime.now()
ans = input("缺少哪個字母呢?")
if ans == r:
    print("答案正確")
    et = datetime.datetime.now()
    print("總共花了"+str((et-st).seconds)+"秒喲")
else:
    print("答案錯誤")
```
