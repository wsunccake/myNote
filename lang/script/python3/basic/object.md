# object

---

## content

- [attr](#attr)
- [class](#class)
- [inheritance](#inheritance)
- [multi-inheritance](#multi-inheritance)
- [abstract class](#abstract-class)
- [staticmethod, classmethod](#staticmethod-classmethod)
- [getattr / setattr](#getattr--setattr)

---

## attr

```python
class Person:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

obj = Person('man')

print(dir(obj))

print([mthd for mthd in dir(obj) if callable(getattr(obj, mthd))])
print([mthd for mthd in dir(obj) if callable(getattr(obj, mthd)) and not mthd.startswith("__")])

print([attr for attr in vars(obj)])
print(vars(obj))
print(obj.__dict__)
```

---

## class

```python
class Animal:
    def __init__(self, name=None):
        self.__name = name
        self.__voice = 'a'
        self.__age = 0
        self.__sex = 'unknown'
        print("Construct Animal")

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def set_age(self, age):
        self.__age = age

    def get_age(self):
        return self.__age

    age = property(get_age, set_age, 'age')

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, sex):
        if sex.lower() == 'male' or sex.lower() == 'female':
            self.__sex = sex
        else:
            raise ValueError('Error sex value')

    @property
    def voice(self):
        return self.__voice

    def _set_voice(self, voice):
        self.__voice = voice

animal = Animal('animal')
print(animal.get_name())

animal.set_age(1)
print(animal.age)

print(animal.sex)
```

---

## inheritance

```python
class Felidae(Animal):
    def __init__(self, name):
        Animal.__init__(self, name)
        print('Construct Felidae, and inheritance Animal')


class Cat(Felidae):
    def __init__(self, name):
        super().__init__(name)
        self._set_voice('Meow')
        print('Construct Cat')

    def __str__(self):
        return 'Cat: {}'.format(self.get_name())

felidae = Felidae('felidae')
print(felidae.get_name())

cat = Cat('kitty')
print(cat.get_name())
print(cat.voice)
print(cat)
```

---

## multi-inheritance

```python
class Bird(Animal):
    def __init__(self):
        Animal.__init__(self)
        print("Construct Bird, and inheritance Animal")

    def fly(self):
        print("Flying in sky")

    def eat(self):
        print('Eat meat and fish')

class Griffin(Felidae, Bird):
    def __init__(self, name):
        super().__init__(name)
        print("Construct Felidae and Bird, and inheritance Animal")

    def eat(self):
        super(Felidae, self).eat()

griffin = Griffin('griffin')
griffin.walk()
griffin.fly()
griffin.eat()
```

---

## abstract class

```python
import abc

class AbcCar(metaclass=abc.ABCMeta):
    def __init__(self, volume):
        self._set_gasoline_volume(volume)
        self._gasoline = 0.0

    def _set_gasoline_volume(self, volume):
        self._volume = volume

    def get_volume(self):
        return self._volume

    def add_gasoline(self, volume):
        if self._gasoline + volume > self._volume:
            raise RuntimeError('add too much gasoline, max %f'.format(self._volume))
        self._gasoline += volume

    @property
    def gasoline(self):
        return self._gasoline

    def run(self, mileage):
        raise NotImplementedError()

    @abc.abstractmethod
    def turbo(self, mileage):
        pass

class Car(AbcCar):
    def run(self, mileage):
        if self._gasoline - mileage * 0.1 > 0:
            self._gasoline -= mileage * 0.1

    def turbo(self, mileage):
        if self._gasoline - mileage * 0.2 > 0:
            self._gasoline -= mileage * 0.2

car = Car(10)
car.add_gasoline(10)
print(car.gasoline)

car.turbo(10)
print(car.gasoline)

car.run(10)
print(car.gasoline)
```

---

## staticmethod, classmethod

```python
class Date(object):
    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year)
        return date1

    @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999

date2 = Date.from_string('11-09-2012')
print(date2.year, date2.day)

print(Date.is_date_valid('11-09-2012'))
```

---

## getattr / setattr

```python

def send(msg):
    print(f"send {msg}")

def speak(l, m):
    print(f"{l} -> {m}")

def say(l):
    print(f"hi {l.name}")

class Message:
    def __init__(self, name):
        self.name = name
        # dynamic set member
        setattr(self, "send", send)                     # assign functuin
        setattr(self, "hello", f"hello {self.name}")    # assign value

        # dynamic set method
        setattr(Message, "speak", speak)

    # dynamic set method / member
    def get_value(self, value):
        return getattr(self, value)

# dynamic set methed/member
setattr(Message, "say", say)
setattr(Message, "hi", "hi")

m = Message("python3")
m.send("learn python")
m.say()
m.speak("go python")
print(m.hello)
print(m.hi)
print(m.get_value("hello"))
print(m.get_value("send")("learning python"))

# dynamic get methed / member
getattr(m, "send")("learn python")
getattr(m, "say")()
getattr(m, "speak")("go python")
```
