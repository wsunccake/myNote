# windows command / batch

## basic

```batch
help
ver
cls

date
time

dir
dir /?
cd c:\
mkdir <dir>
md <dir>
rmdir <dir>
rd <dir>
move <old_name> <new_name>
copy <src> <dest>
del <file>

type <file> | more
findstr <pattern>

tasklist
tasklist | findstr <pattern>
taskkill /IM <cmd>
taskkill /PID <pid>

find

shutdown /r /t 0
shutdown /s /t 0
```

---

## variable

```batch
sysdm.cpl
:: 設定環境變數
```

### environment

```batch
echo %HOMEPATH%
set

set VAR=<val>
echo %VAR%
set VAR=
```

### value

```batch
@echo off
set message=Hello World
echo %message%

set /A a = 5
set /A b = 10
set /A c = %a% + %b%
echo %c%

rem global variable
set globalvar = 5

rem local variable
SETLOCAL
set var = 13145
set /A var = %var% + 5
echo %var%
echo %globalvar%
ENDLOCAL
```

---

## script

```batch
@ehco off
echo "hello windows"
rem  it is comment
::   it is comment too

echo %0
echo %1
echo %~d1
echo %~p1
echo %~n1
echo %~x1
```

```batch
C:\Users\user> hello.bat C:\Windows\notepad.exe
```

---

## return code

```bat
dir
echo %errorlevel%
dir > nul

cmd1 & cmd2
cmd1 | cmd2

cmd1 && cmd2  (%errorlevel% == 0)
cmd1 || cmd2  (%errorlevel% != 0)
```

---

## if

```bat
@echo off
if "ABC"=="ABC" echo "ABC"=="ABC"
if not "ABC"=="abc" echo "ABC"=="abc"
if /I "ABC"=="abc" echo "ABC"=="abc"

if "ABC"=="ABC" (echo yes) else (echo no)

if "ABC"=="ABC" (
  echo yes
) else (
  echo no
)
```

```
EQU – 等於
NEQ – 不等於
LSS – 小於
LEQ – 小於或等於
GTR – 大於
GEQ – 大於或等於
```

---

## for

```bat
@echo off
for %%f in (*.txt) do echo %%f

for /l %%x in (0, 1, 10) do (
   echo %%x
)
```

---

## network

```bat
C:\Users\user> ping <ip>
C:\Users\user> netstat -p tcp udp

C:\Users\user> ipconfig /all
C:\Users\user> ipconfig /renew
```

---

## other

```bat
C:\Users\user> whoami           # -> <DOMAIN>/<USER>

C:\Users\user> runas /user:Administrator cmd
C:\Users\user> runas /noprofile /user:Administrator cmd

C:\Users\user> net user
C:\Users\user> net user adminitstrator
C:\Users\user> net user administrator /active:yes

net accounts
net computer
net config
net continue
net file
net group
net help
net helpmsg
net localgroup
net name
net pause
net print
net send
net session
net share
net start
net statistics
net stop
net time
net use
net user
net view
```

---

## ref

[Windows 命令](https://docs.microsoft.com/zh-tw/windows-server/administration/windows-commands/windows-commands)
