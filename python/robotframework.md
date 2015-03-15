# RobotFramework #

RobotFramework 是一套基於 Python 以驗收測試及 ATDD (Acceptance Test-Driven Development) 功能為主而開發的自動化測試框架 (以下簡稱 RF). 

### 安裝 ###

安裝前需先安裝 Python 及 pip

	linux:~ $ sudo pip install robotframework # for Linux
	osx:~ $ sudo pip install robotframework # for Mac OS X

-----------------------------

### 檔案格式 / Support Format: ###

* HTML (hypertext markup language)
* TSV (tab-separated values)
* TXT/ROBOT (plain text)
* reST (reStructuredText)

以下為 plain text 的範例

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

RF 檔案分四個部分 Settings, Variables, Keywords 和 Test Cases.

* Setttings 載入使用的 RF 或 Python 檔案.
* Variables 設定參數
* Keywords 使用者自訂關鍵字
* Test Cases 要執行的測試

-----------------------------

### 執行 ###

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

### 變數 ###

robot 變數命名是不區分大小寫, 一個空格 兩個空格

	${1}, ${2}, ${3}, ... # 整數
	${Null}, ${None}, ${False}, ${True}
	${null}, ${none}, ${false}, ${true}
	${SPACE}, ${SPACE * 4} # 空格
	${EMPTY}
	${int1}=  Set Variable  ${1}    # 設定 int1 為 整數 1
	${int1}=  Set Variable  1       # 設定 int1 為 字串 1
	@{list1}=  Create List  A  B  C # 設定 array
	${dic1}=  Create Dictionary  Jun=1  Feb=2 # 設定 dictionary


-----------------------------

### 範例 ###

以下為一個簡單的執行範例, 主要的測試檔案為 test.robot, 但是會另外載入 RF 格式的使用者定義 Keywords `UserDefineRF.robot`, Python 格式的使用者定義 module `UserDefinePython.py` 和 RF 格式的變數檔案 Variables `RFVar.txt`. 在執行是會讀取以 Python 格式訂的變數檔案.

[`UserDefineRF.robot`](./example/rf1/UserDefineRF.robot)

	*** Keywords ***
	RF Say
	    [Arguments]  ${words}
	    Log  ${words}


[`UserDefinePython.py`](./example/rf1/UserDefinePython.py)

	def py_say(words):
	    print words


[`RFVar.txt`](./example/rf1/RFVar.txt)

	*** Variables ***
	${rf_words}=  Hello Robotframework


[`var.py`](./example/rf1/var.py)

	py_words = 'Hello Python'


[`test.robot`](./example/rf1/test.robot)

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


run RF

	linux:~ $ pybot -V var.py test.robot


-----------------------------

### Run Command ###

因為 RF 並不會確認執行指令的正確於否, 所以當指令有可能執行失敗, 最好使用 Return Code 去判斷. (在 Shell 中, RC=0 為執行成功, RC!=0 為執行失敗); 同理, 在判斷 Python 程式執行時, 除了 Exception 之外, 其餘都視為正常結果.

`UserDefined.py`

	def intAdd(a1, a2):
	    if type(a1) != type(a2):
	        raise TypeError('type different')
	    return a1 + a2

`test.robot`

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


-----------------------------

### SSH ###


-----------------------------

### Reference ###

[ROBOT FRAMEWORK](http://robotframework.org/)

[Robot Framework Docs Manager](http://rfdocs.org/)