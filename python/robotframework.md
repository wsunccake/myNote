# RobotFramework #
RobotFramework 是一套 python 的測試框架 ( 以下簡稱 RF),

### 安裝 ###
	linux:~ $ sudo pip install robotframework # for Linux
	osx: ~ $ sudo pip install robotframework # for Mac OS X

-----------------------------

### 檔案格式 / Support Format: ###

* HTML (hypertext markup language)
* TSV (tab-separated values)
* TXT/ROBOT (plain text)
* reST (reStructuredText)

-----------------------------

### 變數 ###

robot 變數命名是不區分大小寫

${1}, ${2}, ${3},

${Null}, ${None}, ${False}, ${True}

${null}, ${none}, ${false}, ${true}
${SPACE}, ${SPACE * 4}
${EMPTY}

${int1}=  Set Variable  ${1}    # 設定 int1 為 整數 1
${int1}=  Set Variable  1       # 設定 int1 為 字串 1
@{list1}=  Create List  A  B  C
${dic1}=  Create Dictionary  Jun=1  Feb=2

