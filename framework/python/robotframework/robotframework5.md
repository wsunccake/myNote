# robotframework 5.x


## instsall

```bash
linux:~ $ pip install robotframework
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


###

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

[Robot Framework User Guide](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)

[How to write good test cases using Robot Framework](https://github.com/robotframework/HowToWriteGoodTestCases/blob/master/HowToWriteGoodTestCases.rst)

