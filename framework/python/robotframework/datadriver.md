# robotframework-datadriver

## install

```bash
linux:~ $ pip install robotframework-datadriver
```


---

## sample

`test.robot`

```robot
*** Settings ***
Test Template   Expect Exactly Two Args
Library         DataDriver  file=data.csv  dialect=unix

*** Keywords ***
Expect Exactly Two Args
    [Arguments]  ${a1}  ${a2}
    Run Keyword and Continue on Failure  Should Be Equal  ${a1}  ${a2}

*** Test Cases ***
Two Args ${a1} ${a2}
```


`data.csv`

```csv
${a1},${a2}
42,42
1,2
1,1
```

```bash
linux:~ $ robot test.robot
linux:~ $ pabot --pabotlib --testlevelsplit test.robot
```


---

## ref

[DataDriver for Robot Framework®](https://github.com/Snooz82/robotframework-datadriver)
