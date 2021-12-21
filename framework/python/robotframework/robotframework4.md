# robotframework 4

## run

```
linux:~ # robot <file>.robot

linux:~ # robot -V <var>.yaml -v <var>:<val> <file>.robot
linux:~ # robot -t <test_name> -d <output_dir> <file>.robot
linux:~ # robot -o <output>.xml -l <log>.html -r <report>.html <file>.robot
```


---

## loop

```robot
*** Settings ***
Library     OperatingSystem


*** Variables ***
@{langs}=  C  C++  Java  C#


*** Keywords ***
My List Keyword
    ${scripts}=  Create List  perl  javascript  php  python  ruby
    Length Should Be  ${scripts}  5
    Log  ${scripts}
    # Log  @{scripts}
    Log Many  @{scripts}

    Log  ${langs}
    Log Many  @{langs}

    # for 2.x
    Log  ${langs[0]}
    Log  ${langs[-1]}

    # for 4.x
    Log  ${langs}[0]
    Log  ${langs}[-1]

    # run each element
    FOR  ${script}  IN  @{scripts}
      Log  ${script}
    END

    # only run once
    FOR  ${script}  IN  ${scripts}
      Log  ${script}
    END


*** Test Cases ***
Test List
    My List Keyword
```
