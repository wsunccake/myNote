# Introduction #

RobotFramework 是一套基於 Python 以驗收測試及 ATDD (Acceptance Test-Driven Development) 功能為主而開發的自動化測試框架 (以下簡稱 RF). 

## 安裝 / Installtion ##

安裝前需先安裝 Python 及 pip

	linux:~ $ sudo pip install robotframework # for Linux
	osx:~ $ sudo pip install robotframework # for Mac OS X


## Plugin or IDE ##

`vim`

`sublime text`

`ride`

`PyCharm` / `IntelliJ IDEA`

-----------------------------

## 檔案格式 / Support Format ##

[Robot Framework User Guide](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html) 是一份簡易使用手冊, 有介紹如何使用 Robot Framework

* HTML (hypertext markup language)
* TSV (tab-separated values)
* TXT/ROBOT (plain text)
* reST (reStructuredText)

以下為 plain text 的範例

```
*** Settings ***
Library     OperatingSystem
Library     SSHLibrary  WITH NAME  SSH

*** Variables ***
${HOST}  127.0.0.1
${USERNAME}  test
${PASSWORD}  test
*** Keywords ***

SSH Login
    [Arguments]    ${host}=${HOST}  ${username}=${USERNAME}  ${password}=${PASSWORD}
    Open Connection  ${host}
    Login  ${username}  ${password}

*** Test Cases ***
Show Hostname
    SSH Login
    Write  hostname
    ${stdout}=  Read
    Log  ${stdout}
    Close Connection
```

RF 檔案分四個部分 Settings, Variables, Keywords 和 Test Cases.

`Setttings`

載入使用的 RF 或 Python 檔案.

`Variables`

設定參數

`Keywords`

使用者自訂關鍵字

`Test Cases`

要執行的測試


## 執行 / Run ##

`Python`

| function | command | run as module           | run as script           |
| -------  | ------- | ----------------------- | ----------------------- |
| test     | pybot   | python -m robot.run     | python robot/run.py     |
| report   | rebot   | python -m robot.rebot   | python robot/rebot.py   |
| libdoc   |         | python -m robot.libdoc  | python robot/libdoc.py  |
| testdoc  |         | python -m robot.testdoc | python robot/testdoc.py |
| tidy     |         | python -m robot.tidy    | python robot/tidy.py    |


`Jython`

| function | command | run as module           | run as script           |
| -------  | ------- | ----------------------- | ----------------------- |
| test     | jybot   | jython -m robot.run     | jython robot/run.py     |
| report   | jyrebot | jython -m robot.rebot   | jython robot/rebot.py   |
| libdoc   |         | jython -m robot.libdoc  | jython robot/libdoc.py  |
| testdoc  |         | jython -m robot.testdoc | jython robot/testdoc.py |
| tidy     |         | jython -m robot.tidy    | jython robot/tidy.py    |


`IronPython`

| function | command | run as module        | run as script        |
| -------  | ------- | -------------------- | -------------------- |
| test     | ipybot  |                      |                      |
| report   | ipyebot |                      |                      |
| libdoc   |         | ipy -m robot.libdoc  | ipy robot/libdoc.py  |
| testdoc  |         | ipy -m robot.testdoc | ipy robot/testdoc.py |
| tidy     |         | ipy -m robot.tidy    | ipy robot/tidy.py    |


執行 RF, 執行完 RF 會產生 report, 分別為 log.html, output.xml 和 report.html. 一般可以瀏覽器看 log.html

	linux:~ $ pybot test.robot # 使用 pybot 
	linux:~ $ python -m robot.run test.robot # 使用 python
	linux:~ $ pybot -V var.py -d output -t 'case1' test.robot # -V: 指定變數檔, -d: 指定輸出目錄, -t: 指定執行 test case

產生 report, 只要有 output.xml 就可以重新產生 log.html

	linux:~ $ rebot output.xml
	linux:~ $ python -m robot.rebot output.xml

檔案格式轉換

	linux:~ $ python -m robot.tidy -f html test.robot test.html 


-----------------------------

# Syntax #


## 變數 / Variable ##

RF 變數命名是不區分大小寫, 一個空格 兩個空格

```
${1}, ${2}, ${3}, ... # 整數
${Null}, ${None}, ${False}, ${True}
${null}, ${none}, ${false}, ${true}
${SPACE}, ${SPACE * 4} # 空格
${EMPTY}

${int1}=  Set Variable  ${1}    # 設定 int1 為 整數 1
${int1}=  Set Variable  1       # 設定 int1 為 字串 1

@{list1}=  Create List  A  B  C # 設定 array
Log  ${list1[0]}                # 顯示第一個 element
Log  ${list1[-1]}               # 顯示最後一個 element
Append To List  ${list1}  D     # 新增 element
Remove From List  ${list1}  0   # 移除 element
Log  ${list1}
${content}=  Catenate  SEPARATOR=\n  @{list1}  # 轉成字串

${dic1}=  Create Dictionary  Jun=1  Feb=2  # 設定 dictionary
Log  ${dic1['Jun']}
Set To Dictionary  ${dic1}  Mar  3         # 新增 key / value
Remove From Dictionary  ${dic1}  Jun       # 移除 key / value
Log  ${dic1}
```

## 判斷 / Condition ##

RF 判斷

```
Run Keyword If  '${status}' == '${True}'  Log  status is true

Run Keyword If  ${i < 2}
...    Log  i < 2
...  ELSE
...    Log  i >= 2

Run Keyword If  ${has_android} or ${has_ios}  Log  Wireless Device
```

## 迴圈 / Loop ##

RF 迴圈使用 :FOR 開頭作為迴圈迭代變數設定, 下一行以 \ 開頭作為重複執行內容 (相當是 block)

```
# loop for list
${lists}=  Create List  A  B  C
:FOR  ${element}  IN  @{lists}
\  Log  ${element}

# loop for dictionary
${dic}=  Create Dictionary  Jun=1  Feb=2
${items}=  Get Dictionary Items  ${dic}
:FOR  ${key}  ${value}  IN  @{items}
\  Log  ${key}->${value}
```

## 函數 / Function ##

RF 基本上沒有函數只有關鍵字(Keyword), 所有 Keyword 都定義在 Keyword section


```
*** Keywords ***
My Keyword1
    Log  Hi RF

My Keyword2
[Arugment]  ${arg}
    Log  Hi, ${arg}

My Keyword3 ${who}
    Log  Hi ${who}

My Keyword4
    Log  Hi RF
    [Return]  Hi RF
```

Keyword 帶參數 (argument) 有兩種方式, 一種是在 keyword 內使用 [Arugment] 宣告變數 (範例 My Keyword2); 另一種在宣告 keyword 名稱時就將參數當名稱 (範例 My Keyword3), 但是該參數名稱不能在 keyword name 開頭.

Keyword 回傳值 (return) 只需要在結尾處使用 [Return] 即可 (範例 My keyword4).

`Loop and keyword example`


```
*** Settings ***
Library     Collections

*** Variables ***
${var1}=  ${False}
${var2}  ${True}
@{lists}   A  B  C  D

*** Keywords ***
String Join
    ${exclude_tags}=  Create List
    Run Keyword IF  ${var1} == ${True}  Append To List  ${exclude_tags}  string1
    Run Keyword IF  ${var2} == ${True}  Append To List  ${exclude_tags}  string2
    ${tag}=  Set Variable  ${None}
    :FOR  ${var}  IN  @{exclude_tags}
    \  ${tag}=  Run Keyword IF  '${tag}' == '${None}'  Set Variable  ${var}
       ...  ELSE  Set Variable  ${tag} OR ${var}
    ${tag}=  Run Keyword IF  '${tag}' != '${None}'  Set Variable  -e '${tag}'
    ...  ELSE  Set Variable  \ \
    [Return]  ${tag}

*** Test Cases ***
Test1
   ${arg}=  String Join
   Log  run cmd ${arg}
```

\ \ 表示 white space (空白字元), ... 表示連接前面 statement 的換行


## 範例 / Example ##

以下為一個簡單的執行範例, 主要的測試檔案為 test.robot, 但是會另外載入 RF 格式的使用者定義 Keywords `UserDefineRF.robot`, Python 格式的使用者定義 module `UserDefinePython.py` 和 RF 格式的變數檔案 Variables `RFVar.txt`. 在執行是會讀取以 Python 格式訂的變數檔案.

[`UserDefineRF.robot`](./example/rf1/UserDefineRF.robot)

```
*** Keywords ***
RF Say
    [Arguments]  ${words}
    Log  ${words}
```

[`UserDefinePython.py`](./example/rf1/UserDefinePython.py)

```
def py_say(words):
    print words
```

[`RFVar.txt`](./example/rf1/RFVar.txt)

```
*** Variables ***
${rf_words}=  Hello Robotframework
```

[`var.py`](./example/rf1/var.py)

```
py_words = 'Hello Python'
```

[`test.robot`](./example/rf1/test.robot)

```
*** Settings ***
Library     OperatingSystem
Library     UserDefinePython
Resource    UserDefineRF.robot
Resource    RFVar.txt

*** Test Cases ***
Say Somethings
    Log  Hi
    RF Say  Hi Robotframe
    RF Say  ${rf_words}
    Py Say  Hi Python
    Py Say  ${py_words}
```

run RF

	linux:~ $ pybot -V var.py test.robot


-----------------------------

# Library #


## Run Command ##

因為 RF 並不會確認執行指令的正確於否, 所以當指令有可能執行失敗, 最好使用 Return Code 去判斷. (在 Shell 中, RC=0 為執行成功, RC!=0 為執行失敗); 同理, 在判斷 Python 程式執行時, 除了 Exception 之外, 其餘都視為正常結果.

[`UserDefined.py`](./example/rf2/UserDefined.py)

```
def intAdd(a1, a2):
    if type(a1) != type(a2):
        raise TypeError('type different')
    return a1 + a2
```

[`test.robot`](./example/rf2/test.robot)

```
*** Settings ***
Library     OperatingSystem
Library     UserDefined


*** Keywords ***
Run Error Command Without Check Return Code
    [Arguments]  ${cmd}=ls /abc
    ${result}=  Run  ls /abc
    Log  result:${result}

Run Error Command With Check Return Code
    [Arguments]  ${cmd}=ls /abc
    ${rc}  ${result}=  Run and Return RC and Output  ls /abc
    Log  result:${result} rc: ${rc}
    Should Be True  ${rc} == 0

Run Python Without Check
    intAdd  4  9

Run Python With Check
    ${result}=  intAdd  ${4}  ${9}
    Should Be Equal As Integers  ${result}  ${13}

Run Python With Different Type
    intAdd  4  ${9}


*** Test Cases ***
Run Shell Command Example
    Run Error Command Without Check Return Code
    Run Error Command With Check Return Code

Run Python Example
    Run Python Without Check
    Run Python With Check
    Run Python With Different Type
```


## SSHLibrary ##

RF 本身也提供 SSHLibary (底層使用 paramiko module), 方便開發使用 SSH 的 test case.
使用會載入 SSHLibrary, 需要先安裝 robotframework-sshlibrary (使用 pip 安裝即可). 注意不要安裝 2.0 之前的版本, 因為 keyword 差異.
[SSHLibrary](http://robotframework.org/SSHLibrary/latest/SSHLibrary.html) 有簡易的說明文件可以參考, 主要是說明 Keywords.

[`test.robot`](./example/rf3/test.robot)

```
*** Settings ***
Library     OperatingSystem
Library     SSHLibrary  WITH NAME  SSH

*** Variables ***
${HOST}  127.0.0.1
${USERNAME}  root
${PASSWORD}  password

*** Keywords ***
SSH Login
    [Arguments]    ${host}=${HOST}  ${username}=${USERNAME}  ${password}=${PASSWORD}
    Open Connection  ${host}
    Login  ${username}  ${password}

SSH Logout
    Close Connection

Run ${cmd} Command
    Write  ${cmd}
    ${stdout}=  Read
    Log  ${stdout}

Run ${cmd} Command With RC
    Start Command  ${cmd}
    ${stdout}  ${stderr}  ${rc}=  Read Command Output  return_stderr=True  return_rc=True
    Log  rc: ${rc}
    Log  stdout: ${stdout}
    Log  stderr: ${stderr}

*** Test Cases ***
Show Hostname
    SSH Login
    Run hostname Command
    Run ls abc Command
    Run ls abc Command With RC
    Run ls abc Command With RC
    SSH Logout
```

## Selenium ##

使用會載入 Selenium2Library, 需要先安裝 robotframework-selenium2library (使用 pip 安裝即可). 注意不要安裝 robotframework-seleniumlibrary, 因為 locator 語法有差異.
[Selenium2Library](http://rtomac.github.io/robotframework-selenium2library/doc/Selenium2Library.html) 有簡易的說明文件可以參考, 主要是說明 Keywords 和 Locators 使用, 而 Locators 可以參考 [Locators_table_1_0_2.pdf](http://www.cheat-sheets.org/saved-copy/Locators_groups_1_0_2.pdf) [Locators_table_1_0_2.pdf](http://www.cheat-sheets.org/saved-copy/Locators_table_1_0_2.pdf)

[`test.robot`](./example/rf4/test.robot)

```
*** Settings ***
Library        Selenium2Library

*** Variables ***
${delay}=  ${1}
${google_url}=  http://www.google.com
${browser}=  firefox

*** Test Cases ***
Test Google
    Open Browser  ${google_url}  ${browser}
    Capture Page Screenshot
    Set Selenium Speed  ${delay}
    Maximize Browser Window

    Input Text  id=lst-ib  robotframework\n
    Capture Page Screenshot

    Click Link  css=#rso > div:nth-child(2) > li:nth-child(1) > div > h3 > a
    Capture Page Screenshot

    Title Should Be  Robot Framework
    ${url}=  Get Location
    Log  ${url}
    Click Link  xpath=//*[@id="menu"]/div/ul/li[1]/a
    Click Link  css=#menu > div > ul > li:nth-child(2) > a
    Close Browser
```


-----------------------------

# Reference #

[ROBOT FRAMEWORK](http://robotframework.org/)

[Robot Framework Docs Manager](http://rfdocs.org/)