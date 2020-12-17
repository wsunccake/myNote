# pytest

## install

```bash
linux:~ # pip install pytest
linux:~ # pytest --version
linux:~ # pytest --help
```


---

## sample

```bash
linux:~ # cat test_sample.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5

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
