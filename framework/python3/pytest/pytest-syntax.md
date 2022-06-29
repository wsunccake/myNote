# pytest - syntax

## assert

`code`

```python
    t1 = Task('sit there', 'brain')
    t2 = Task('do something', 'ken')
    assert t1 == t2
```


---

## single

`code`

```python
def test_default():
    ...
```

`command`

```bash
linux:~/project # pytest src/tests/test_tasks.py::test_default
```


---

## match

`code`

```python
def test_default():
    ...
```

`command`

```bash
linux:~/project # pytest -k default
```


---

## marker

`code`

```python
@pytest.mark.run_replace
def test_replace():
    ...
```

`command`

```bash
linux:~/project # pytest -m run_replace
```


---

## skip

`code`

```python
@pytest.mark.skip(reason='misunderstood the api')
def test_unique_id_1():
    ...
```


---

## skipif

`code`

```python
@pytest.mark.skipif(tasks.__version__ < '0.2.0', reason='no support version')
def test_unique_id_2():
    ...
```


---

## xfail

`code`

```python
@pytest.mark.xfail()
def test_unique_id_is_a_duck():
    ...
```


---

## parametreize

`origin`

```python
def test_add_1():
    """tasks.get() use id"""
    task = Task('berathe', 'BRIAN', True)
    task_id = tasks.add(task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, task)
```

`method 1`

```python
@pytest.mark.parametrize('task',
                         [Task('sleep', done=True),
                          Task('wake', 'brain'),
                          Task('breathe', 'brain', True)])
def test_add_2(task):
    task_id = tasks.add(task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, task)
```

`method 2`

```python
task_data = [Task('sleep', done=True),
               Task('wake', 'brain'),
               Task('breathe', 'brain', True)]

@pytest.mark.parametrize('task', task_data)
def test_add_3(task):
    task_id = tasks.add(task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, task)
```

`method 3`

```python
task_ids = ['Task({}, {}, {})'.format(t.summary, t.owner, t.done) for t in task_data]

@pytest.mark.parametrize('task', task_data, ids=task_ids)
def test_add_4(task):
    task_id = tasks.add(task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, task)
```


---

## fixture - auto use

`code - test_*.py`

```python
@pytest.fixture(autouse=True)
def initialized_tasks_db(tmpdir):
    """connect db"""
    # SETUP
    tasks.start_tasks_db(str(tmpdir), 'tiny')

    # this is where testing happen
    yield

    # TEARDOWN
    tasks.stop_tasks_db()

def test_add_return_valid_id():
    """tasks.add() should return integer"""
    # GIVEN initialize db
    # auto run initialized_tasks_db

    # WHEN new task id
    new_task = Task('do something')
    task_id = tasks.add(new_task)

    # THEN check return type
    assert isinstance(task_id, int)
```

`command`

```bash
linux:~/project # pytest
linux:~/project # pytest --setup-show --tb=no -v
linux:~/project # pytest --fixtures -q
```


---

## fixture - conftest.py

`code - conftest.py`

```python
import pytest
import tasks

@pytest.fixture()
def tasks_db(tmpdir):
    """connect db"""
    # SETUP
    tasks.start_tasks_db(str(tmpdir), 'tiny')

    # this is where testing happen
    yield

    # TEARDOWN
    tasks.stop_tasks_db()
```

`code - test_*.py`

```python
import tasks
from tasks import Task

def test_add_return_valid_id(tasks_db):
    """tasks.add() should return integer"""
    # GIVEN initialize db
    # auto run initialized_tasks_db

    # WHEN new task id
    new_task = Task('do something')
    task_id = tasks.add(new_task)

    # THEN check return type
    assert isinstance(task_id, int)
```


---

## fixture - data

`code - conftest.py`

```python
@pytest.fixture()
def tasks_with_multi_per_owner():
    """several owner with each task"""
    return (Task('make a cookie', 'raphael'),
            Task('use an emoji', 'raphael'),
            Task('move to Berlin', 'raphael'),

            Task('create', 'michelle'),
            Task('inspire', 'michelle'),
            Task('encourage', 'michelle'),

            Task('do a handstand', 'daniel'),
            Task('write some books', 'daniel'),
            Task('eat ice cream', 'daniel'))
```

`code - test_*.py`

```python
def test_acc(tasks_with_multi_per_owner):
    """send data from fixture"""
    assert len(tasks_with_multi_per_owner) > 0
```


---

## fixture - mulit fixture

`code - conftest.py`

```python
@pytest.fixture()
def db_with_multi_per_owner(tasks_db, tasks_with_multi_per_owner):
    """connect db with several tasks"""
    for t in tasks_with_multi_per_owner:
        tasks.add(t)
```

`code - test_*.py`

```python
def test_multi_fixture(db_with_multi_per_owner):
    """multi fixture"""
    assert tasks.count() > 0
```


---

## fixture - scope

function, class, module, session

`code`

```python
@pytest.fixture(scope='function')
def func_scope():
    """function scope"""

@pytest.fixture(scope='module')
def mod_scope():
    """module scope"""

@pytest.fixture(scope='session')
def sess_scope():
    """session scope"""

def test_scope_1(sess_scope, mod_scope, func_scope):
    """test scope 1"""

def test_scope_2(sess_scope, mod_scope, func_scope):
    """test scope 2"""

@pytest.fixture(scope='class')
def cls_scope():
    """class scope"""

@pytest.mark.usefixtures('cls_scope')
class TestSomething:
    """test class scope"""

    def test_scope_3(self):
        """test scope 3"""

    def test_scope_4(self):
        """test scope 4"""
```


---

# fixture - name

`code`

```python
@pytest.fixture(name='ua')
def ultimate_answer():
    """return answer"""
    return 42

def test_ultimate_answer(ua):
    """use short name"""
    assert ua == 42
```


---

# fixture - param

`code`

```python
task_data = [Task('sleep', done=True),
             Task('wake', 'brain'),
             Task('breathe', 'brain', True)]

@pytest.fixture(params=task_data)
def a_task(request):
    """task data"""
    return request.param

def test_add_3(tasks_db, a_task):
    task_id = tasks.add(a_task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, a_task)


task_ids = ['Task({}, {}, {})'.format(t.summary, t.owner, t.done) for t in task_data]

@pytest.fixture(params=task_data, ids=task_ids)
def b_task(request):
    """task data"""
    return request.param

def test_add_4(tasks_db, b_task):
    task_id = tasks.add(b_task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, b_task)


def ids_func(fixture_value):
    """generate ids"""
    return 'Task({}, {}, {})'.format(fixture_value.summary, fixture_value.owner, fixture_value.done)

@pytest.fixture(params=task_data, ids=ids_func)
def c_task(request):
    """task data"""
    return request.param

def test_add_5(tasks_db, c_task):
    task_id = tasks.add(c_task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, c_task)
```
