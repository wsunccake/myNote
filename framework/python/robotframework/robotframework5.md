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

**robot**

實際執行測試腳本。

```bash
       robot
.robot ─────> output.xml  ───> log.html
                          └──> report.html
```

- 測試檔案: .robot
- 執行過程中，所有測試細節與結果即時寫入, outpu.xml
- 測試結束後，根據 output.xml 自動生成 log.html 與 report.html

```bash
# 刪除已通過（PASS）測試案例內的所有步驟細節，僅保留失敗案例的完整排錯資訊。
robot --removekeywords PASS testcase.robot

# 刪除 FOR 迴圈與重試機制（Wait Until...）中成功步驟的細節，大幅清理重複性雜訊。
robot --removekeywords FOR --removekeywords WUKS testcase.robot
```

**rebot**

不執行測試，僅對已存在的 output.xml 進行後處理或二次加工。

```bash
            rebot
output.xml ───────────> log.html
                  └───> report.html
```

```bash
# 讀取既有的 output.xml，生成 log.html 與 report.html 測試報告。
rebot output.xml

# 展平 FOR 迴圈的樹狀階層結構，不刪除任何資料，只優化網頁載入速度。
rebot --flattenkeywords FOR output.xml

# 刪除已通過（PASS）測試案例內的所有步驟細節，僅保留失敗案例的完整排錯資訊。
rebot --removekeywords PASS output.xml

# 刪除 FOR 迴圈與重試機制（Wait Until...）中成功步驟的細節，大幅清理重複性雜訊。
rebot --removekeywords FOR --removekeywords WUKS output.xml

# 刪除 FOR 迴圈與重試機制（Wait Until...）中成功步驟的細節後，將裁減過的結果另存為新的 XML 檔（output_clean.xml）並更新報告。
rebot --removekeywords FOR -o output_clean.xml output.xml
```

- **ALL**
  All: 移除所有 Keyword。不論 Test Case 是 PASS 或 FAIL，所有 Kw 內部的細節步驟通通清掉，只保留最頂層的結果統計。適合用在只需要高階報表、想把 log.html 檔案縮到極小的場景。

- **PASSED**
  Passed: 移除 PASS 測試裡面的 Keyword。若整個 Test Case 的結果是 PASS，則清空其內部 Kw；若 Test Case 是 FAIL，則完整保留內部所有 Kw 步驟。

- **FOR**
  For Loops: 只移除 FOR 迴圈中已通過的 Iteration。如果 FOR 迴圈跑了 1000 次，只有第 999 次失敗，它會清掉前 998 次 PASS 的迴圈步驟，僅保留 FAIL 的那一次以及最後一次。對付大數據量的迴圈非常有用。

- **WUKS**
  Wait Until Keyword Succeeds: 只移除重試機制中 PASS 的中間嘗試。當使用 Wait Until Keyword Succeeds 重試了 10 次才成功時，它會將前 9 次失敗/等待的過渡紀錄清掉，只保留最後一次成功的結果。避免 Log 被重試紀錄洗版。

- **NAME:<pattern>**
  Name Pattern: 依照 Keyword 名稱過濾。移除符合指定名稱（支援通配符 \*）的 Kw 內容。例如 --removekeywords NAME:BuiltIn.Log 會把所有 Log 關鍵字的內容清掉，減少印出過多重複 log。

- **TAG:<pattern>**
  Tag Pattern: 依照 Keyword 的 Tag 過濾。移除帶有指定 Tag 的 Kw 內容。常用於隱藏含有敏感資訊（如密碼）或步驟極度冗長的 Kw，例如 --removekeywords TAG:sensitive。

```bash
--removekeywords 的過濾機制
 ├── 1. 結果導向 (會保護 FAILED / 自動留底)
 │    ├── PASSED  ➔ 測試 PASS 才清；測試 FAIL 則「全留」
 │    ├── FOR     ➔ 迴圈 PASS 才清；迴圈 FAIL 則「保留該次」
 │    └── WUKS    ➔ 重試過渡期才清；最終結果「永遠保留」
 │
 └── 2. 標籤與名稱導向 (不管 FAILED / 一律照砍)
      ├── NAME    ➔ 名字中了就清 (無論 PASS/FAIL)
      └── TAG     ➔ 標籤中了就清 (無論 PASS/FAIL)
```

| 模式           | 觸發過濾的條件                     | 遇到 FAILED 時的行為                                | 核心設計目的 / 最佳實務場景                                                    |
| -------------- | ---------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------ |
| PASSED         | 整條 Test Case 結果為 PASS         | 🛡️ 完全保護(FAIL 的測試內部細節 100% 保留)          | 最常用。產出一份乾淨報告，成功的不佔空間，失敗的保留完整排錯 context。         |
| FOR            | FOR 迴圈中的單次 Iteration 為 PASS | 🛡️ 精準保護(只保留 FAIL 的那幾次，PASS 的迭代砍掉)  | 大數據迴圈。例如跑 1000 次測試資料，只留下出錯的那第 500 次細節。              |
| WUKS           | Wait Until... 重試過程中的過渡紀錄 | 🛡️ 結果保護(只刪除中間等待/失敗嘗試，留最終狀態)    | 消除重試噪音。重試 10 次才成功的 Keyword，只留最後一次成功，避免 Log 洗版。    |
| NAME:<pattern> | Keyword 名稱符合指定字樣           | 💥 照樣移除(即使該 Keyword 執行 FAIL，細節一樣被清) | 清理無害雜訊。如 NAME:BuiltIn.Log\*，專門清掉印出大篇幅無用純文字的 Kw。       |
| TAG:<pattern>  | Keyword Tag 符合指定標籤           | 💥 照樣移除(即使該 Keyword 執行 FAIL，細節一樣被清) | 資安防護與遮蔽。如 TAG:sensitive，無論成功失敗都不能把密碼/Token 留在 Log 裡。 |

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
