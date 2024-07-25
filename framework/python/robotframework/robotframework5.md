# robotframework 5.x

## content

- [instsall](#instsall)
- [hello](#hello)
- [execution](#execution)
  - [basic](#basic)
  - [simple pattern](#simple-pattern)
  - [tag pattern](#tag-pattern)
  - [argument file](#argument-file)
  - [stop](#stop)
  - [variable](#variable)
- [ref](#ref)

---

## instsall

```bash
linux:~ $ pip install robotframework
```

---

## hello

```robot
*** Settings ***
Library           OperatingSystem

*** Variables ***
${MESSAGE}        Hello, world!

*** Test Cases ***
My Test
    [Documentation]    Example test.
    My Keyword    ${MESSAGE}

*** Keywords ***
My Keyword
    [Arguments]    ${msg}
    Log    ${msg}
    Should Be Equal    ${msg}    Hello, world!
```

```bash
linux:~ $ robot hello.robot
linux:~ $ robot -v MESSAGE:"Hi RF" hello.robot
```

---

## execution

### basic

```bash
linux:~ $ robot <file>.robot
linux:~ $ python -m robot <file>.robot
```

### simple pattern

glob-like patterns

```text
* matches any string, even an empty string.
? matches any single character.
[abc] matches one character in the bracket.
[!abc] matches one character not in the bracket.
[a-z] matches one character from the range in the bracket.
[!a-z] matches one character not from the range in the bracket.
Unlike with glob patterns normally, path separator characters / and \ and the newline character \n are matches by the above wildcards.
Unless noted otherwise, pattern matching is case, space, and underscore insensitive.

--test Example*        # Matches tests with name starting 'Example'.
--test Example[1-2]    # Matches tests 'Example1' and 'Example2'.
--include f??          # Matches tests with a tag that starts with 'f' is three characters long.
```

### tag pattern

```text
AND / &
--include fooANDbar     # Matches tests containing tags 'foo' and 'bar'.
--exclude xx&yy&zz      # Matches tests containing tags 'xx', 'yy', and 'zz'.

OR
--include fooORbar      # Matches tests containing either tag 'foo' or tag 'bar'.
--exclude xxORyyORzz    # Matches tests containing any of tags 'xx', 'yy', or 'zz'.

NOT
--include fooNOTbar     # Matches tests containing tag 'foo' but not tag 'bar'.
--exclude xxNOTyyNOTzz  # Matches tests containing tag 'xx' but not tag 'yy' or tag 'zz'.
--include NOTfoo        # Matches tests not containing tag 'foo'
--include NOTfooANDbar  # Matches tests not containing tags 'foo' and 'bar'
```

```bash
linux:~ $ export ROBOT_OPTIONS="--outputdir results --tagdoc 'mytag:Example doc with spaces'"
linux:~ $ robot tests.robot

linux:~ $ export REBOT_OPTIONS="--reportbackground green:yellow:red"
linux:~ $ rebot --name example output.xml
```

### argument file

### stop

```bash
linux:~ $ kill -9 <robot pid> # force terminal, no report
linux:~ $ kill -2 <robot pid> # grace terminal, gen report
```

### variable

```robot
*** Settings ***
Variables         setup_var.py  foo_variables  bar_variables
Library           OperatingSystem

*** Variables ***
${MESSAGE}        Hello, world!

*** Test Cases ***
My Test
    [Documentation]    Example test.
    Log Variables
    My Keyword    ${MESSAGE}

*** Keywords ***
My Keyword
    [Arguments]    ${msg}
    Log    ${msg}
    Should Be Equal    ${msg}    Hello, world!
```

```python
# common_var.py
common_variables = {
    'version': '1.0.0',
}

foo_variables = common_variables | {
    'foo': 'foo',
}

bar_variables = common_variables | {
    'bar': 'bar',
}
```

```python
# setup_var.py
import sys
import common_var

def get_variables(*args):
    variables = {}

    m = globals().get("common_var")
    # v = m.__dict__.get("common_variables")
    for arg in args:
        v = m.__dict__.get(arg)
        variables.update(v)

    return variables

###
### main
###

if __name__ == "__main__":
    print("args:", sys.argv[1:])
    print(get_variables(*sys.argv[1:]))
```

```bash
linux:~ $ robot [-V <var.py>] [-v var:val] hello.robot
```

---

## library

### python function

```python
# lib/userFn.py
def add_two_number(a1, a2):
    if type(a1) != type(a2):
        raise TypeError('type different')
    return a1 + a2
```

```python
# lib/userFunc.py
def add_two_number(a1, a2):
    if type(a1) != type(a2):
        raise TypeError('type different')
    return a1 + a2
```

```
# test.robot
*** Settings ***
Library     OperatingSystem
Library     lib.userFn
Library     lib.userFunc  WITH NAME  func

*** Keywords ***
Run Without Check
    # convert robotframework keyword
    Add Two Number  4  9

    # call python function
    lib.userFn.add_two_number  4  9

    # call python function by alias
    func  4  9

Run With Check
    ${result}=  Add Two Number  ${4}  ${9}
    Should Be Equal As Integers  ${result}  ${13}

Run With Different Type
    Add Two Number  4  ${9}

*** Test Cases ***
Run Python Function Example
    Run Without Check
    Run With Check
    Run With Different Type
```

### python class

```python
# lib/userCls.py
class Calculator:
    def add(self, a1, a2):
        if type(a1) != type(a2):
            raise TypeError('type different')
        return a1 + a2


class Computer:
    def __init__(self, name) -> None:
        self.name = name

    def add(self, a1, a2):
        if type(a1) != type(a2):
            raise TypeError('type different')
        return a1 + a2
```

```
# test.robot
*** Settings ***
Library     OperatingSystem
Library     lib.userCls.Calculator
Library     lib.userCls.Computer   computer  WITH NAME  computer


*** Keywords ***
Run Without Check
    ${variable}=    lib.userCls.Calculator.add_two_number  ${1}  ${1}
    computer.add_two_number  ${1}  ${2}

*** Test Cases ***
Run Python Example
    Run  Without Check
```

---

## ref

[Robot Framework User Guide](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
