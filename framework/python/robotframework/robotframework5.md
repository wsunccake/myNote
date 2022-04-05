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

## execution

### basic

```bash
linux:~ $ robot <file>.robot
linux:~ $ python -m robot <file>.robot
```


### simple pattern

glob-like patterns

```
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

```
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

---

## ref

[Robot Framework User Guide](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
