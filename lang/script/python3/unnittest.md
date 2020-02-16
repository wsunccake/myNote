# unittest

## in main

```python
# main.py
import unittest


def add(x: int, y: int) -> int:
    return x + y


class TestAdd(unittest.TestCase):
    def test_add(self):
        print('run test_add')
        self.assertEqual(add(1, 1), 2, '1 + 1 = 2')


class Person:
    def __init__(self, name):
        self._name = name
        self._age = 0

    def get_name(self):
        return self._name

    def set_age(self, age):
        self._age = age

    def get_age(self):
        return self._age


class TestPerson(unittest.TestCase):
    def setUp(self):
        print('initialize')
        self.person = Person('john')

    def tearDown(self) -> None:
        print('finalize')

    def test_name(self):
        print('run test_name')
        self.assertEqual(self.person.get_name(), 'john')


if __name__ == '__main__':
    unittest.main()
```

```bash
linux:~ # python -m unittest main
linux:~ # python -m unittest main.TestPerson
linux:~ # python -m unittest main.TestPerson.test_name
```


---

## other file

```python
# util.py
def add(x: int, y: int) -> int:
    return x + y
```

```python
# test_util.py
import util
import unittest

class TestUtil(unittest.TestCase):
    def test_add(self):
        print('run test_add')
        self.assertEqual(util.add(1, 1), 2, '1 + 1 = 2')

if __name__ == '__main__':
    unittest.main()

```

```bash
linux:~ # python -m unittest test_util
linux:~ # python -m unittest test_util.TestUtil
linux:~ # python -m unittest test_util.TestUtil.test_add
```


---

# mock

```python
# util.py
import time


def calc_pi(p=10 ** -10):
    '''
    pi/2 = 1 + 1/3 + 1/3 * 2/5 + 1/3 * 2/5 * 3/7 + ...
    :return: double
    '''
    x = 2.0
    z = 2.0
    a = 1
    b = 3
    while z > p:
        z = z * a / b
        x += z
        a += 1
        b += 2
    time.sleep(2)
    return x


def circle_area(radius):
    pi = calc_pi()
    return radius * radius * pi
```

```python
# test_util.py
import util
import unittest
import unittest.mock


class TestUtil(unittest.TestCase):
    def test_circle_area(self):
        print('run test_circle_area')
        area = round(util.circle_area(1), 2)
        self.assertEqual(area, 3.14)

    @unittest.mock.patch('util.calc_pi')
    def test_circle_area_decorator_mock(self, mock_calc_pi):
        print('run test_circle_area')
        mock_calc_pi.return_value = 3.14
        area = round(util.circle_area(1), 2)
        self.assertEqual(area, 3.14)

    def test_circle_area_with_mock(self):
        print('run test_circle_area')
        with unittest.mock.patch('util.calc_pi') as mock_calc_pi:
            mock_calc_pi.return_value = 3.14
            area = round(util.circle_area(1), 2)
            self.assertEqual(area, 3.14)


if __name__ == '__main__':
    unittest.main()
```
