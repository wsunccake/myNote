# robotframework 5.x


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

## ref

[Robot Framework User Guide](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
