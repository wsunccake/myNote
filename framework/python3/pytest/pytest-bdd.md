# pytest-bdd 5.x

## install

```bash
linux:~ $ pip install pytest-bdd
```


---

## example

`sample.py`

```python
def add(a, b):
    return a + b
```


`test_sample.py`

```python
from pytest_bdd import scenario, given, when, then
from sample import add

global_vars = {}

@scenario('sample.feature', 'correct answer')
def test_sample():
    pass

@given("initialize value")
def initial_value():
    global_vars.update({'a': 1, 'b': 1})

@when("execute add")
def execute_add():
    c = add(global_vars['a'], global_vars['b'])
    global_vars.update({'c': c})

@then("check answer")
def check_answer():
    assert 2 == global_vars['c']
```


`sample.feature`

```
Feature: sample

    Scenario: correct answer
        Given initialize value
        When execute add
        Then check answer
```


可安裝 [allure-pytest-bdd](./allure-pytest.md#allure-pytest-bdd) 產生 report


`command`

```bash
linux:~ $ pytest --alluredir=result --clean-alluredir test_sample.py
linux:~ $ allure serve result
```


---

## step

### alias

```python
@given("init value")
@given("initialize value")
def initial_value():
    global_vars.update({'a': 1, 'b': 1})
```

### argument

`test_sample.py`

```python
from pytest_bdd import scenario, given, when, then, parsers
from sample import add

@scenario('sample.feature', 'correct answer')
def test_sample():
    pass

# cfparse
@given(parsers.cfparse("initialize value {a:Number} and {b:Number}",
                       extra_types=dict(Number=int)),
       target_fixture="global_vars",
       )
def initial_value(a, b):
    return dict(a=a, b=b)

# target_fixture
@ when("execute add")
def execute_add(global_vars):
    c = add(global_vars['a'], global_vars['b'])
    global_vars.update({'c': c})

# re
@ then(parsers.re(r"check answer (?P<c>\d+)"),
       converters=dict(c=int)
       )
def check_answer(global_vars, c):
    assert c == global_vars['c']

# parse
@then(parsers.parse("check value {c:d}"))
def check_value(global_vars, c):
    assert c == global_vars['c']
```

`sample.feature`

```
Feature: sample

    Scenario: correct answer
        Given initialize value 1 and 1
        When execute add
        Then check answer 2
        And check value 2
```


---

## scenario - outline

`sample.feature`

```
Feature: sample

    Scenario: correct answer
        Given initialize value <a> and <b>
        When execute add
        Then check answer <c>

        Examples:
        | a  | b  | c  |
        | 1  | 1  | 2  |
        | 1  | -1  | 0  |
```


or vertical

```
Feature: sample

    Scenario: correct answer
        Given initialize value <a> and <b>
        When execute add
        Then check answer <c>

        Examples: Vertical
        | a  | 1  | 1  |
        | b  | 1  | -1  |
        | c  | 2  | 0  |
```


or feature

```
Feature: sample

    Examples:
    | a  | b  | c  |
    | 1  | 1  | 2  |
    | 1  | -1  | 0  |

    Scenario: correct answer
        Given initialize value <a> and <b>
        When execute add
        Then check answer <c>
```


or feature vertical

```
Feature: sample

    Examples: Vertical
    | a  | 1  | 1  |
    | b  | 1  | -1  |
    | c  | 2  | 0  |

    Scenario: correct answer
        Given initialize value <a> and <b>
        When execute add
        Then check answer <c>
```


---

## ref

[Welcome to Pytest-BDD’s documentation!](https://pytest-bdd.readthedocs.io/en/stable/)
