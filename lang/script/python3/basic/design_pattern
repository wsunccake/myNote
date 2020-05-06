# design pattern

## singleton

```python
class Singleton:
    _instance = None

    @staticmethod
    def get_instance():
        if Singleton._instance is None:
            SingleTon()
        return Singleton._instance

    def __init__(self):
        if Singleton._instance is not None:
            raise Exception('only one instance can exist')
        else:
            self._id = id(self)
            SingleTon._instance = self

    def get_id(self):
        return self._id

if __name__ == '__main__':
    s1 = Singleton.get_instance()
    s2 = Singleton.get_instance()
    print(id(s1))
    print(id(s2))
```

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

if __name__ == '__main__':
    s1 = Singleton()
    s2 = Singleton()
    print(id(s1))
    print(id(s2))
```


---
