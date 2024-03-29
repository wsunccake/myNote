# pytest 7.x

## install

```bash
linux:~ # pip install pytest
linux:~ # pytest --version
linux:~ # pytest --help
```


---

## editor or ide

### vscode

```json
// launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["${file}"],
            "environment": [{"PYTHONPATH": "${workspaceFolder}"}],
            "justMyCode": true
        }
    ]
}
```


---

## sample

```bash
linux:~ # cat test_sample.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5

class TestCase:
    def test_answer(self):
        assert func(3) == 7

linux:~ # python -m pytest test_sample.py

linux:~ # pytest test_sample.py
linux:~ # pytest -v test_sample.py
linux:~ # pytest -q test_sample.py
```

test file default name must be test_*.py or *_test.py

test function / test method default name must be test_*

test class default name must be Test*


---

## option

`tests/test_demo.py`

```python
import pytest
from collections import namedtuple

Task = namedtuple('Task', ['summary', 'owner', 'done', 'id'])
Task.__new__.__defaults__ = (None, None, False, None)

def test_default():
    '''check default value'''
    t1 = Task()
    t2 = Task(None, None, False, None)
    assert t1 == t2

def test_member_access():
    '''check member'''
    t = Task('buy milk', 'brain')
    assert t.summary == 'buy milk'
    assert t.owner == 'brain'
    assert (t.done, t.id) == (False, None)

def test_asdict():
    ''' asdict() return dict'''
    t_task = Task('do something', 'ken', True, 21)
    t_dict = t_task._asdict()
    expected = {'summary': 'do something',
                'owner': 'ken',
                'done': True,
                'id': 21}
    assert t_dict == expected

@pytest.mark.run_replace
def test_replace():
    '''replace'''
    t_before = Task('finish book', 'brain', False)
    t_after = t_before._replace(id=10, done=True)
    t_excepted = Task('finish book', 'brain', True, 10)
    assert t_after == t_excepted
```

```bash
linux:~/project # pytest
linux:~/project # pytest tests/test_demo.py::test_default
linux:~/project # pytest -v -k 'asdict or default'
linux:~/project # pytest -m run_replace
linux:~/project # pytest -v --tb=no
```

## folder


```bash
.
├── CHANGELOG.rst
├── LICENSE
├── MANIFEST.in
├── setup.py
├── src
│   └── tasks
│       ├── __init__.py
│       ├── ...
│       └── xxx.py
└── tests
    ├── conftest.py
    ├── func
    │   ├── __init__.py
    │   └── test_func.py
    ├── pytest.ini
    └── unit
        ├── __init__.py
        └── test_task.py
```

pytest.ini

conftest.py

## pybulder


```bash
linux:~/project # pip install pybuilder
linux:~/project # pyb --start-project
linux:~/project # vi build.py
...

# use_plugin("python.unittest")
# use_plugin("python.coverage")

use_plugin('python.pycharm')

use_plugin('pypi:pybuilder_pytest')
use_plugin('pypi:pybuilder_pytest_coverage')


@init
def set_properties(project):
    project.get_property("pytest_extra_args").append("-x")
    project.set_property('pytest_coverage_html', True)
    project.set_property('coverage_threshold_warn', 70)
    project.set_property('coverage_break_build', False)

linux:~/project # pyb pycharm_generate
```

`src/src/python/task.py`

```python
def add(x, y):
    return x + y
```

`src/unittest/python/test_sample.py`

```python
from task import add

def test_add():
    assert add(1, 2) == 3
```

`run`

```bash
linux:~/project # pyb
linux:~/project # pyb run_unit_tests
linux:~/project # pyb clean analyze
```


---

## setup & teardown

`def`

```python
def setup_module():
    print("setup module")

def teardown_module():
    print("teardown module")

def setup_function():
    print("setup function")

def teardown_function():
    print("teardown function")

def test_sample1():
    print("test sample1")

def test_sample2():
    print("test sample2")

###
### test process
###
# setup module
#
# setup function
# test sample1
# teardown function
#
# setup function
# test sample2
# teardown function
#
# teardown module
```


`class`

```python
class TestSample:
    @classmethod
    def setup_class(cls):
        print("setup class")

    @classmethod
    def teardown_class(cls):
        print("teardown class")

    def setup_method(self):
        print("setup method")

    def teardown_method(self):
        print("teardown method")

    def test_sample1(self):
        print("test sample1")

    def test_sample2(self):
        print("test sample2")

###
### test process
###
# setup class
#
# setup method
# test sample1
# teardown method
#
# setup method
# test sample2
# teardown method
#
# teardown class
```


---

## pytest.fixture

`def with pytest.fixture`

```python
import pytest

@pytest.fixture(scope="session")
def sess_scope():
    print("setup session")
    yield
    print("teardown session")

@pytest.fixture(scope="module")
def mod_scope():
    print("setup module")
    yield
    print("teardown module")

@pytest.fixture(scope="function")
def func_scope():
    print("setup function")
    yield
    print("teardown function")

def test_sample1(sess_scope, mod_scope, func_scope):
    print("test sample1")

@pytest.mark.usefixtures("func_scope", "mod_scope", "sess_scope")
def test_sample2():
    print("test sample2")

###
### test process
###
# setup session
# setup module
#
# setup function
# test sample1
# teardown function
#
# setup function
# test sample2
# teardown function
#
# teardown module
# teardown session
```


`class with pytest.fixture`

```python
import pytest

@pytest.fixture(scope="session")
def sess_scope():
    print("setup session")
    yield
    print("teardown session")

@pytest.fixture(scope="module")
def mod_scope():
    print("setup module")
    yield
    print("teardown module")

@pytest.fixture(scope="class")
def cls_scope():
    print("setup class")
    yield
    print("teardown class")

@pytest.fixture(scope="function")
def func_scope():
    print("setup function")
    yield
    print("teardown function")

@pytest.mark.usefixtures("cls_scope")
class TestSample:
    def test_sample1(self, sess_scope, mod_scope, func_scope):
        print("test sample1")

    def test_sample2(self, func_scope, mod_scope, sess_scope):
        print("test sample2")

###
### test process
###
# setup session
# setup module
# setup class
#
# setup function
# test sample1
# teardown function
#
# setup function
# test sample2
# teardown function
#
# teardown class
# teardown module
# teardown session
```

`return with pytest.fixture`

```python
@pytest.fixture
def di():
    return "di"

@pytest.mark.usefixtures("di")
def test_sample1():
    print(di)               # function di
    print("test sample1")

def test_sample2(di):
    print(di)               # call/run function di
    print("test sample2")

###
### test process
###
# <function di at 0x10e598700>
# test sample1
#
# di
# test sample1
```


---

## pytest.mark.parametrize

```python
import pytest

data = [("root", "1234"), ("root", "5678"),
        ("admin", "1234"), ("admin", "5678")]

@pytest.mark.parametrize('username,passworod', data)
def test_login(username, passworod):
    assert username == 'admin' and passworod == '1234'
```


```python
import pytest
usernames = ["root", "admin", "sys"]
passwords = ["1234", "5678", "abcd"]

@pytest.mark.parametrize('password', passwords)
@pytest.mark.parametrize('username', usernames)
def test_login(username, password):
    assert username == 'admin' and password == '1234'
```


---

## ref

[Full pytest documentation](https://docs.pytest.org/en/latest/contents.html)
