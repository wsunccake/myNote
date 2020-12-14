# pytest-bdd

## install

```bash
linux:~ # pip install pytest-bdd
```


---

## sample

`sample.py `

```python
def add(a, b):
    return a + b
```


`test_sample.py `

```python
from pytest_bdd import scenario, given, when, then
from sample import add

global_vars = {}

@scenario('sample.feature',
          'correct answer',
          example_converters=dict(a=int, b=int, c=int)
)
def test_sample():
    pass


@given("initialize value <a> and <b>")
def initial_value(a, b):
    print(a)
    print(type(a))
    global_vars.update({'a': a, 'b': b})


@when("execute add")
def execute_add():
    c = add(global_vars['a'], global_vars['b'])
    global_vars.update({'c': c})


@then("check answer <c>")
def check_answer(c):
    assert c == global_vars['c']
```


`sample.feature `

```
Feature: sample

    Scenario: correct answer
        Given initialize value <a> and <b>
        When execute add
        Then check answer <c>

        Examples:
        | a   | b   | c   |
        | 1   | 1   | 2   |
        | 0   | 1   | 1   |
```

```bash
linux:~ # pytest
```
