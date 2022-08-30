# SOLID

## single-responsibility principle/ SRP / 單一職責原則

```python
class Modem
    def dial(self, number):
        pass

    def hangup():
        pass

    def send(self, data):
        pass

    def receive():
        pass
```

上述行為可以分為 connection, communication

->

```python
import abc

class Connection(abc.ABC):
    @abc.abstractmethod
    def dial(self, number):
        pass

    @abc.abstractmethod
    def hangup(self):
        pass

class Communication(abc.ABC):
    @abc.abstractmethod
    def send(self, data):
        pass

    @abc.abstractmethod
    def receive(self):
        pass

class Modem(Connection, Communication):
    def dial(self, number):
        pass

    def hangup(slef):
        pass

    def send(self, data):
        pass

    def receive(self):
        pass
```


---

## open–closed principle / OCP / 開放封閉原則

```python
class Payment:
    def pay(self):
        print(self.msg)

    def set_payment_type(self, payment_type):
        self.msg = ''
        if payment_type == 'cash':
            self.msg = 'pay cash'
        elif payment_type == 'credit':
            self.msg = 'pay credit card'
        elif payment_type == 'electronic':
            self.msg = 'pay electronic'
        else:
            self.msg = 'no pay method'

if __name__ == '__main__':
    p = Payment()
    p.set_payment_type('cash')
    p.pay()
```

->

```python
import abc

class Payment:
    def __init__(self):
        self.set_payment_type()

    def pay(self):
        print(self.msg)

    @abc.abstractmethod
    def set_payment_type(self):
        pass

class Cash(Payment):
    def set_payment_type(self):
        self.msg = 'pay cash'

class Credit(Payment):
    def set_payment_type(self):
        self.msg = 'pay credit'


if __name__ == '__main__':
    p = Cash()
    p.pay()
```


---

## Liskov substitution principle / LSP / 里氏替換原則

```python
class Square:
    def __init__(self, width):
        self.width = width

    def area(self):
        return self.width * self.width

class Rectangle(Square):
    def __init__(self, width, height):
        super().__init__(width)
        self.height = height

    def area(self):
        return self.width * self.height
```

不應該 override parenet class method

->

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, width):
        super().__init__(width, width)
```


---

## interface segregation principle / ISP / 介面隔離原則

```python
import abc

class Athlete(abc.ABC):
    @abc.abstractmethod
    def hit(self):
        pass

    def run(self):
        print('run')

    @abc.abstractmethod
    def pitch(self):
        pass

class BaseballPlayer(Athlete):
    def hit(self):
        print('hit baseball')

    def pitch(self):
        print('pitch baseball')

class TennisPlayer(Athlete):
    def hit(self):
        print('hit tennis')

    def pitch(self):
        print("can't pitch tennis")
```

TennisPlayer 不需要 pitch

->

```python
import abc

class Athlete(abc.ABC):
    @abc.abstractmethod
    def hit(self):
        pass

    def run(self):
        print('run')

class BaseballPlayerInterface(abc.ABC):
    @abc.abstractmethod
    def pitch(self):
        pass

class BaseballPlayer(Athlete, BaseballPlayerInterface):
    def hit(self):
        print('hit baseball')

    def pitch(self):
        print('pitch baseball')

class TennisPlayer(Athlete):
    def hit(self):
        print('hit tennis')
```

---

## dependency inversion principle / DIP / 依賴反向原則

```python
class Hamburger:
    def __str__(self) -> str:
        return 'Hamburger'

class Spaghetti:
    def __str__(self) -> str:
        return 'Spaghetti'

class Man:
    def __init__(self) -> None:
        self.food = Hamburger()

    def eat(self):
        print(f'eat {self.food}')


if __name__ == '__main__':
    m = Man()
    m.eat()
```

eat 雖接受 food, 但default always fix Hamburger

->

```python
class Hamburger:
    def __str__(self) -> str:
        return 'Hamburger'

class Spaghetti:
    def __str__(self) -> str:
        return 'Spaghetti'

class Man:
    def __init__(self, food) -> None:
        self.food = food

    def eat(self):
        print(f'eat {self.food}')


if __name__ == '__main__':
    m = Man(Spaghetti())
    m.eat()
```
