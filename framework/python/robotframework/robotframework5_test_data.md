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

---

## ref

[Robot Framework User Guide](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)

[How to write good test cases using Robot Framework](https://github.com/robotframework/HowToWriteGoodTestCases/blob/master/HowToWriteGoodTestCases.rst)

