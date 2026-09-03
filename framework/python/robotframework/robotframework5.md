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
- [library](#library)
  - [python function](#python-function)
  - [python class](#python-class)
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

## Condition Syntax

1. Variable Expression

```robot
IF    $score >= 80
    Log    Pass
ELSE
    Log    Fail
END
```

- 運算機制：Python 物件直傳。變數直接以原生的 Python 物件型態傳入條件式中，不經過純文字替換。
- 安全性：🟢 高。保留變數原本型態（如 int、float），即便變數為 None 或空值也不會發生語法崩潰。
- 支援版本：Robot Framework 4.0+
- 綜合評估：🌟 最佳解（現代 RF 官方標準）。最精簡、最安全，徹底解決型態轉換與文字替換的潛在問題。

2. Inline Evaluation

```robot
IF    ${{ $score >= 80 }}
    Log    Pass
ELSE
    Log    Fail
END
```

- 運算機制：重複 Python 解析。在本身就具備 Python 評估能力的 IF 內，又多套了一層 ${{ ... }}。
- 安全性：🟡 中。運算邏輯雖然安全，但底層執行了不必要的二次解析。
- 支援版本：Robot Framework 4.0+
- 綜合評估：⚠️ 不推薦（語法冗餘）。屬於畫蛇添足的寫法，外層的 ${{ ... }} 完全可以省略。

3. Evaluate Keyword

```robot
${status}=    Evaluate    $score >= 80
IF    ${status}
    Log    Pass
ELSE
    Log    Fail
END
```

- 運算機制：兩階段處理。先透過 Evaluate 關鍵字將計算結果（True/False）存入臨時變數，再由 IF 進行讀取。
- 安全性：🟡 中。邏輯正確但流程繁瑣；若在 Evaluate 內使用 ${score} 仍會有純文字替換的風險。
- 支援版本：Robot Framework 2.9+
- 綜合評估：⚠️ 過時寫法。這是 RF 3.2 以前沒有原生 IF 時的過渡期寫法，增加了不必要的變數定義與代碼行數。

4. Normal IF

```robot
IF    ${score} >= 80
    Log    Pass
ELSE
    Log    Fail
END
```

- 運算機制：純文字巨集替換。在交給 Python 解析前，會先將 ${score} 的值直接以純文字方式填入條件式。
- 安全性：🔴 低（易崩潰）。若變數為空字串會引發 SyntaxError；若變數為字串型態會引發 TypeError。
- 支援版本：Robot Framework 4.0+
- 綜合評估：❌ 不建議使用。極易因變數型態不符合或變數為空值而導致測試腳本在中途直接崩潰。

5. Traditional

```robot
Run Keyword If    ${score} >= ${80}    Log    Pass
...    ELSE    Log    Fail
```

- 運算機制：關鍵字參數解析。透過 BuiltIn 關鍵字傳遞參數，使用 ... 進行換行與分支控制，並依賴 ${80} 強制做型態轉換。
- 安全性：🔴 低（已被棄用）。可讀性差、維護成本高，且非常依賴文字替換。
- 支援版本：Robot Framework 1.0 ~ 3.2（RF 4.0+ 已宣告棄用）
- 綜合評估：🛑 舊專案維護專用（已廢棄）。新專案切勿使用此寫法。

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
