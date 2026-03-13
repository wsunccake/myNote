# exception

---

## content

- [try, except, finally](#try-except-finally)
- [raise](#raise)
- [defined exception](#defined-exception)

---

## try, except, finally

```python
try:
    a = int(input('input an integer number '))
    b = int(input('input an integer number '))
    if a > b:
        print(n)
except ValueError:
    print("Value Error, you don't input any character")
except:
    print("Other Error")
else:
    print("Normal finish")
finally:
    print("force action")
```

```python
try:
    a = int(input('input an integer number '))
    b = int(input('input an integer number '))
    if a > b:
        print(n)
except ValueError as e:
    print(f"Value Error, you don't input any character. {e}")
except Exception as e:
    print(f"Other Error. {e}")
else:
    print("Normal finish")
finally:
    print("force action")
```


---

## raise

```python
import math

anumber = int(input('input an integer number '))

if anumber < 0:
    # raise RuntimeError("You can't use a negative number")
    raise RuntimeError("You can't use a negative number") from None # no trace code
else:
    print(math.sqrt(anumber))
```

---

## defined exception

```python
class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

try:
    raise MyError(input("keyin any one: "))
except MyError as e:
    print('My exception occurred, value:', e.value)
```
