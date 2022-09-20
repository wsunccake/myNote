# robotframework 5.x - test data

## testcase

### setting

```
[Documentation]         Used for specifying a test case documentation.
[Tags]                  Used for tagging test cases.
[Setup], [Teardown]     Specify test setup and teardown.
[Template]              Specifies the template keyword to use. The test itself will contain only data to use as arguments to that keyword.
[Timeout]               Used for setting a test case timeout. Timeouts are discussed in their own section.
```

```robot
*** Test Cases ***
Test With Settings
    [Documentation]    Another dummy test
    [Tags]    dummy    owner-johndoe
    Log    Hello, world!
```


### argument

```robot
*** Keywords ***
Named Run Program
    [Arguments]    @{args}
    Run Process    program.py    @{args}    # Named arguments are not recognized from inside @{args}

Free Named Run Program
    [Arguments]    @{args}    &{config}
    Run Process    program.py    @{args}    &{config}

Named-Only Run Program
    [Arguments]    @{args}    ${shell}=False
    Run Process    program.py    @{args}    shell=${shell}

*** Test Cases ***
Positional argument
    Create Directory    ${TEMPDIR}/stuff
    Copy File    ${CURDIR}/file.txt    ${TEMPDIR}/stuff
    No Operation

Default value
    Create File    ${TEMPDIR}/empty.txt
    Create File    ${TEMPDIR}/utf-8.txt         Hyvä esimerkki
    Create File    ${TEMPDIR}/iso-8859-1.txt    Hyvä esimerkki    ISO-8859-1

Variable number of argument
    Remove Files    ${TEMPDIR}/f1.txt    ${TEMPDIR}/f2.txt    ${TEMPDIR}/f3.txt
    @{paths} =    Join Paths    ${TEMPDIR}    f1.txt    f2.txt    f3.txt    f4.txt

Named arguments
    Named Run Program    shell=True    # This will not come as a named argument to Run Process

Free named argument
    Free Named Run Program    arg1    arg2    cwd=/home/user
    Free Named Run Program    argument    shell=True    env=${ENVIRON}

Named-only Arguments
    Named-Only Run Program    arg1    arg2              # 'shell' is False (default)
    Named-Only Run Program    argument    shell=True    # 'shell' is True
```


### tag

```robot
*** Settings ***
Force Tags      req-42
Default Tags    owner-john    smoke

*** Variables ***
${HOST}         10.0.1.42

*** Test Cases ***
No own tags
    [Documentation]    This test has tags owner-john, smoke and req-42.
    No Operation

With own tags
    [Documentation]    This test has tags not_ready, owner-mrx and req-42.
    [Tags]    owner-mrx    not_ready
    No Operation

Own tags with variables
    [Documentation]    This test has tags host-10.0.1.42 and req-42.
    [Tags]    host-${HOST}
    No Operation

Empty own tags
    [Documentation]    This test has only tag req-42.
    [Tags]
    No Operation

Set Tags and Remove Tags Keywords
    [Documentation]    This test has tags mytag and owner-john.
    Set Tags    mytag
    Remove Tags    smoke    req-*
```


### setup & teardown

```robot
*** Settings ***
Test Setup       Open Application    App A
Test Teardown    Close Application

*** Test Cases ***
Default values
    [Documentation]    Setup and teardown from setting section
    Do Something

Overridden setup
    [Documentation]    Own setup, teardown from setting section
    [Setup]    Open Application    App B
    Do Something

No teardown
    [Documentation]    Default setup, no teardown at all
    Do Something
    [Teardown]

No teardown 2
    [Documentation]    Setup and teardown can be disabled also with special value NONE
    Do Something
    [Teardown]    NONE

Using variables
    [Documentation]    Setup and teardown specified using variables
    [Setup]    ${SETUP}
    Do Something
    [Teardown]    ${TEARDOWN}
```


---

## template

### basic syntax

```robot
*** Keywords ***
Expect Exactly Two Args
    [Arguments]  ${a1}  ${a2}
    Run Keyword and Continue on Failure  Should Be Equal  ${a1}  ${a2}

*** Test Cases ***
Template With Variable And Assign Mark (=)
    [Documentation]  FAIL    1= != 2=
    [Template]  Expect Exactly Two Args
    ${42} =    42 =
    ${42}=     42=
    ${1}=      ${2}=
    ${1}=      ${1}=
```


### with embedded argument

```robot
*** Keywords ***
The result of ${a1} should be ${a2}
    Run Keyword and Continue on Failure  Should Be Equal  ${a1}  ${a2}

*** Test Cases ***
Template With Variable And Assign Mark (=)
    [Template]  The result of ${a1} should be ${a2}
    ${42} =    42 =
    ${42}=     42=
    ${1}=      ${2}=
    ${1}=      ${1}=
```


### with loop

```robot
*** Keywords ***
Expect Exactly Two Args
    [Arguments]  ${a1}  ${a2}
    Run Keyword and Continue on Failure  Should Be Equal  ${a1}  ${a2}

*** Test Cases ***
Template With Variable And Assign Mark (=)
    [Template]  Expect Exactly Two Args
    FOR    ${index}    IN RANGE    3
        ${1}    ${index}
    END
```


### with condition

```robot
*** Keywords ***
Expect Exactly Two Args
    [Arguments]  ${a1}  ${a2}
    Run Keyword and Continue on Failure  Should Be Equal  ${a1}  ${a2}

*** Test Cases ***
Template With Variable And Assign Mark (=)
    [Template]  Expect Exactly Two Args
    FOR    ${index}    IN RANGE    3
        IF  ${index} < 2
            ${1}    ${index}
        END
    END
```


### data-driven style

```robot
*** Settings ***
Test Template   Expect Exactly Two Args

*** Keywords ***
Expect Exactly Two Args
    [Arguments]  ${a1}  ${a2}
    Run Keyword and Continue on Failure  Should Be Equal  ${a1}  ${a2}

*** Test Cases ***
testcase1           ${42} =         42 =
testcase2           ${42} =         42=
testcase3           ${1} =          ${2}=
testcase4           ${2} =          ${1}=
```


---

## task

```robot
*** Tasks ***
Process invoice
    Read information from PDF
    Validate information
    Submit information to backend system
    Validate information is visible in web UI
```


---

## test suite

### initialization file

`__init__.robot`

```robot
*** Settings ***
Documentation    Example suite                  # document
Suite Setup      Do Something    ${MESSAGE}     # setup or teardown
Force Tags       example                        # tag
Library          SomeLibrary
Metadata         Version         2.0            # metadata

*** Variables ***
${MESSAGE}       Hello, world!

*** Keywords ***
Do Something
    [Arguments]    ${args}
    Some Keyword    ${arg}
    Another Keyword
```


---

## test library

### using `Library` in setting

```robot
*** Settings ***
Library    OperatingSystem
Library    my.package.TestLibrary
Library    MyLibrary    arg1    arg2
Library    ${LIBRARY}
```


### using `Import Library` keyword

```robot
*** Test Cases ***
Example
    Do Something
    Import Library    MyLibrary    arg1    arg2
    KW From MyLibrary
```


### using physical path to library

```robot
*** Settings ***
Library    PythonLibrary.py
Library    relative/path/PythonDirLib/    possible    arguments
Library    ${RESOURCES}/Example.class
```


### setting custom name to test library

```robot
*** Settings ***
Library    com.company.TestLib    WITH NAME    TestLib
Library    ${LIBRARY}             WITH NAME    MyName
Library    SomeLibrary    localhost        1234    WITH NAME    LocalLib
Library    SomeLibrary    server.domain    8080    WITH NAME    RemoteLib
```


### example - import library

```bash
linux:~ $ cat UserDefineRF.robot
*** Keywords ***
RobotFramework Say
    [Arguments]  ${words}
    Log  hey ${words}

linux:~ $ UserDefinePyFunc.py
def func_say(msg):
    print(f'hi {msg}')

linux:~ $ UserDefinePyCls.py
class ClsSay():
    def __init__(self, msg) -> None:
        self.msg = msg

    def hello(self):
        print(f'hello {self.msg}')

linux:~ $ test.robot
*** Settings ** *
Library     OperatingSystem
Resource    UserDefineRF.robot
Library     UserDefinePyFunc
Library     UserDefinePyCls.ClsSay  RobotFramework  WITH NAME  cls_say

*** Test Cases ** *
Say Somethings
    Log  Hi RF
    RobotFramework Say  RobotFramework
    func_say  RobotFramework
    cls_say.hello

linux:~ $ robot test.robot
```


### example - import variable

```bash
linux:~ $ cat var.robot
*** Variables ***
${rf_words}=  Hello Robotframework

linux:~ $ cat var.py
py_words = 'Hello Python'

linux:~ $ cat test.robot
*** Settings ** *
Library     OperatingSystem
Resource    var.robot

*** Test Cases ** *
Say Somethings
    Log  ${rf_words}
    Log  ${py_words}
    Log  ${words}

linux:~ $ robot -V var.py -v words:"Hello rf" test.robot
```


---

## variable

RF 變數命名是不區分大小寫

### scalar

```robot
${1}, ${2}, ${3}, ...                   # 整數
${Null}, ${None}, ${False}, ${True}
${null}, ${none}, ${false}, ${true}
${SPACE}, ${SPACE * 4}                  # 空格
${EMPTY}, ${/}, ${\}, ${\n}

${int1}=  Set Variable  ${1}            # 設定 int1 為 整數 1
${str1}=  Set Variable  1               # 設定 str1 為 字串 1
```


### list

```robot
${list1}=  Create List  A  B  C                 # 設定 list
Log  ${list1[0]}                                # 顯示第一個 element
Log  ${list1}[0]                                # 顯示第一個 element
Log  ${list1[-1]}                               # 顯示最後一個 element
# Log  @{list1[0]}                              # 錯誤
Append To List  ${list1}  D                     # 新增 element
Remove From List  ${list1}  0                   # 移除 element
Log  ${list1}
Log  ${list1[2:]}
# Log  @{list1}                                 # 錯誤 無法顯示
Log Many  ${list1}
Log Many  @{list1}

${content}=  Catenate  SEPARATOR=\n  @{list1}   # 轉成字串

@{list2}=  Create List  A  B  C                 # 設定 list 使用 @
${list3}=  Evaluate  ['A', 'B', 'C']            # 設定 list 使用 Evaluate

@{animals}=  Create List  cat  dog
FOR    ${e}    IN    @{list1}            # loop
    Log    ${e}
END
```


### dictionary

```robot
${dict1}=  Create Dictionary  Jun=1  Feb=2      # 設定 dictionary
Log  ${dict1['Jun']}
Set To Dictionary  ${dict1}  Mar  3             # 新增 key / value
Remove From Dictionary  ${dict1}  Jun           # 移除 key / value
Log  ${dict1}
# Log  &{dict1}                                 # 錯誤
Log Many  ${dict1}
Log Many  &{dict1}

&{dict2}=  Create Dictionary  Jun=1  Feb=2      # 設定 dictionary 使用 &
${dict3}=  Evaluate  {'Jun': '1', 'Feb': '2'}   # 設定 dictionary 使用 Evaluate

FOR    ${key}    ${value}    IN    &{dict1}
    Log    '${key}' -> '${value}'
END
```


### environment

```robot
Log  %{HOME}
```


### variables

```robot
*** Variables ***
# scalar
${NAME}         Robot Framework
${VERSION}      2.0
${ROBOT}        ${NAME} ${VERSION}
${EXAMPLE}      This value is joined
...             together with a space.
${MULTILINE}    SEPARATOR=\n
...             First line.
...             Second line.
...             Third line.

# list
@{NAMES}        Matti       Teppo
@{NAMES2}       @{NAMES}    Seppo
@{NOTHING}
@{MANY}         one         two      three      four
...             five        six      seven

# dictionary
&{USER 1}       name=Matti    address=xxx         phone=123
&{USER 2}       name=Teppo    address=yyy         phone=456
&{EVEN MORE}    &{USER 1}     first=override      empty=
...             =empty        key\=here=value
```


---

## control structure

### for loop

```robot
# simple loop
FOR    ${var}    IN    one    two    thtee    four    five
...    kuusi    7    eight    nine    last
    Log    ${var}
END

FOR    ${key}    ${value}    IN    a=1    d=4    g=7
        Log    '${key}' -> '${value}'
END

# multiple nesting loop
FOR    ${root}    IN    r1    r2
    FOR    ${child}    IN    c1   c2    c3
        FOR    ${grandchild}    IN    g1    g2
            Log Many    ${root}    ${child}    ${grandchild}
        END
    END
    FOR    ${sibling}    IN    s1    s2    s3
        IF    '${sibling}' != 's2'
            Log Many    ${root}    ${sibling}
        END
    END
END

# multiple loop variable
FOR    ${index}    ${english}    ${finnish}    IN
...    1           cat           kissa
...    2           dog           koira
...    3           horse         hevonen
    Add Translation    ${english}    ${finnish}    ${index}
END

# FOR - IN RANGE
FOR    ${index}    IN RANGE    10
    Log    ${index}
END

# FOR - IN ENUMERATE
FOR    ${index}    ${item}    IN ENUMERATE    dog   cat
    Log    ${index}: ${item}
END

FOR    ${index}     ${key}    ${value}    IN    a=1    d=4    g=7
        Log    ${index}: '${key}' -> '${value}'
END

${NUMBERS}=     Create List     ${1}    ${2}    ${5}
${NAMES}=       Create List     one     two     five
# FOR - IN ZIP
FOR    ${number}    ${name}    IN ZIP    ${NUMBERS}    ${NAMES}
    Log Many    ${number}    ${name}
END
```


### while loop

```robot
# simple
${rc}=  Set Variable    1
WHILE    ${rc} != 0
    ${rc}=  Generate Random String  1  [NUMBERS]
END

# limit as iteration count
WHILE    True    limit=100
    Log    This is run 100 times.
END

# limit as time
WHILE    True    limit=10 seconds
    Log    This is run 10 seconds.
END

# no limit
WHILE    True    limit=NONE
    Log    This must be forcefully stopped.
END

# nesting WHILE
${x} =   Set Variable    10
WHILE    ${x} > 0
    ${y} =   Set Variable    ${x}
    WHILE    ${y} > 0
        ${y} =    Evaluate    ${y} - 1
    END
    IF    ${x} > 5
        ${x} =    Evaluate    ${x} - 1
    ELSE
        ${x} =    Evaluate    ${x} - 2
    END
END
```

--expandkeywords name:<pattern>|tag:<pattern> *

--removekeywords all|passed|for|wuks|name:<pattern>|tag:<pattern> *

--flattenkeywords for|while|iteration|name:<pattern>|tag:<pattern> *


### break, continue

```robot
# BREAK with FOR
${text} =    Set Variable    zero
FOR    ${var}    IN    one    two    three
    IF    '${var}' == 'two'    BREAK
    ${text} =    Set Variable    ${text}-${var}
END
Should Be Equal    ${text}    zero-one

# CONTINUE with FOR
${text} =    Set Variable    zero
FOR    ${var}    IN    one    two    three
    IF    '${var}' == 'two'    CONTINUE
    ${text} =    Set Variable    ${text}-${var}
END
Should Be Equal    ${text}    zero-one-three
```


### if

```robot
# Number Compare
IF    ${rc > 0}
    Log  Positive
ELSE IF    ${rc < 0}
    Log  Negative
ELSE IF    ${rc == 0}
    Log  Zero
ELSE
    Fail    Unexpected rc: ${rc}
END

# String Compare
Run Keyword If  '${status}' == '${True}'  Log  status is true

# Inline IF/ELSE
IF    $condition    Keyword    argument    ELSE    Another Keyword

# Inline IF/ELSE IF/ELSE
IF    $cond1    Keyword 1    ELSE IF    $cond2    Keyword 2    ELSE IF    $cond3    Keyword 3    ELSE    Keyword 4

# Inline IF/ELSE with assignment
${var} =    IF    $condition    Keyword    argument    ELSE    Another Keyword

# Inline IF/ELSE with assignment having multiple variables
${host}    ${port} =    IF    $production    Get Production Config    ELSE    Get Testing Config

# Nested IF
IF    not ${items}
    Log to console    No items.
ELSE IF    len(${items}) == 1
    IF    ${log_values}
        Log to console    One item: ${items}[0]
    ELSE
        Log to console    One item.
    END
ELSE
    Log to console    ${{len(${items})}} items.
    IF    ${log_values}
        FOR    ${index}    ${item}    IN ENUMERATE    @{items}    start=1
            Log to console    Item ${index}: ${item}
        END
    END
END
```


---

## ref

[Robot Framework User Guide](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)

[How to write good test cases using Robot Framework](https://github.com/robotframework/HowToWriteGoodTestCases/blob/master/HowToWriteGoodTestCases.rst)
