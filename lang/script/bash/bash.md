# BASH

## bashrc, profile

| 檔案            | 主要用途                                                   | 何時讀取                                                                   |
| --------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------- |
| **\~/.profile** | 設定環境變數 (PATH、LANG、EDITOR...)，影響整個登入 session | **登入 shell** 時（login shell，例如 ssh、登入 TTY、顯示管理員登入）       |
| **\~/.bashrc**  | 設定互動 shell 的行為 (alias、prompt、function...)         | **互動式非登入 shell**（例如你在 GNOME Terminal、xterm 裡再開一個新 bash） |

當執行 bash 時，會依「登入 / 非登入」、「互動 / 非互動」決定讀哪些檔案。

1. 登入 shell (login shell)

- /etc/profile → 系統設定
- ~/.profile → 使用者設定
- （部分發行版會改用 ~/.bash_profile 或 ~/.bash_login，優先順序是：~/.bash_profile > ~/.bash_login > ~/.profile）

2. 非登入 shell (non-login shell, 例如開新終端分頁)

- /etc/bash.bashrc → 系統設定
- ~/.bashrc → 使用者設定

3. 互動 + 登入 shell（常見情況：ssh）

- 同時會讀取 profile 與 bashrc（但要注意：~/.profile 內通常會手動呼叫 ~/.bashrc，確保登入時也能套用 alias/function）

許多系統的 ~/.profile 會看到

```bash
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi
```

這樣一來，不管是登入 shell 還是非登入 shell，~/.bashrc 都會被執行，確保 alias / prompt 一致。

```text
                 ┌──────────────┐
                 │  啟動 Bash   │
                 └──────┬───────┘
                        │
          ┌─────────────┴─────────────┐
          │                           │
    [登入 shell]                 [非登入 shell]
 (Login shell, ssh, tty)       (Non-login shell, 開新終端機)

          │                           │
   ┌──────┴───────┐             ┌─────┴─────┐
   │              │             │           │
 [互動式]     [非互動式]     [互動式]    [非互動式]
(Interactive) (Non-interactive) (Interactive) (Non-interactive)

   │              │             │           │
   │              │             │           │
1. 讀取:         不會讀取互動設定    讀取:       不會讀取互動設定
   - /etc/profile                - /etc/bash.bashrc
   - ~/.bash_profile             - ~/.bashrc
     或 ~/.bash_login
     或 ~/.profile

   │
   │ (通常在 ~/.profile 裡面再加:)
   │   if [ -f ~/.bashrc ]; then
   │       . ~/.bashrc
   │   fi
   │
   ▼
完成初始化
```

---

## run

```bash
# method 1
linux:~ # chmod +x script.sh
linux:~ # ./script.sh

# method 2
linux:~ # sh script.sh

# method 3
linux:~ # export VAR=value
linux:~ # ./script.sh

# method 4
linux:~ # env VAR=value ./script.sh

# run with debug
linux:~ # sh -xv script.sh
```

---

## stdout, stderr

```bash
| Function                              | CSH             |  SH
| ------------------------------------- | --------------- | -----------------
| Send stdout to file                   | prog > file     |  prog > file
| Send stderr to file                   |                 |  prog 2> file
| Send stdout and stderr to file        | prog >& file    |  prog > file 2>&1
| Take stdin from file                  | prog < file     |  prog < file
| Send stdout to end of file            | prog >> file    |  prog >> file
| Send stderr to end of file            |                 |  prog 2>> file
| Send stdout and stderr to end of file | prog >>& file   |  prog >> file 2>&1
|                                       |                 |  prog &> file
|                                       |                 |  prog >& file
| Read stdin from keyboard until c      | prog <          |  prog <
| Pipe stdout to prog2                  | prog | prog2    |  prog | prog2
| Pipe stdout and stderr to prog2       | prog |& prog2   |  prog 2>&1 | prog2
```

---

## pipe example

```bash
linux:~ # tar cf - *.log | gzip > file.tar.gz
linux:~ # gzip -dc file.tar.gz | tar xf -
linux:~ # tar cf - *.log | tar xf - -C backup_dir

linux:~ # curl http://download/file.tar.gz -o file.tar.gz && tar zxf file.tar.gz
linux:~ # curl http://download/file.tar.gz | tar zx

linux:~ # false | tee /dev/null; echo $?
linux:~ # false | tee /dev/null; echo ${PIPESTATUS[0]}

linux:~ # cp file.log file.$(date +%D).log && : > file.log && gzip file.$(date +%D).log

linux:~ # curl -o- https://github/install.sh | bash
linux:~ # wget -qO- https://github/install.sh | bash

# define file descriptor
linux:~ # exec 5>>config.log                        # open file descriptor
linux:~ # echo "This is the first message." >&5     # append to file descriptor
linux:~ # echo "This is the second message." >&5
linux:~ # cat config.log
linux:~ # exec 5>&-                                 # close file descriptor
```

---

## prefix and suffix

```bash
FILE_PATH=/usr/lib/python/site-package/xxx-1.0/yyy.zz
echo "raw:"
echo ${FILE_PATH}        # /usr/lib/python/site-package/xxx-1.0/yyy.zz

echo "prefix:"
echo ${FILE_PATH%.*}     # /usr/lib/python/site-package/xxx-1.0/yyy
echo ${FILE_PATH%%.*}    # /usr/lib/python/site-package/xxx-1

echo "suffix:"
echo ${FILE_PATH#*/}      # usr/lib/python/site-package/xxx-1.0/yyy.zz
echo ${FILE_PATH##*/}     # yyy.zz

# For bash 4.x
SENTENCE="That is a test."
echo "sentence:"
echo "${SENTENCE}"        # That is a test.

echo "reverse:"
echo "${SENTENCE~~}"      # tHAT IS A TEST.

echo "upper:"
echo "${SENTENCE^^}"      # THAT IS A TEST.

echo "lower:"
echo "${SENTENCE,,}"      # that is a test.

# define var operation
VAR="Hello Bash"
echo "define VAR: ${VAR}"
echo "\${VAR:=value}: ${VAR:=value}"
echo "VAR: ${VAR}"
echo

VAR="Hello Bash"
echo "define VAR: ${VAR}"
echo "\${VAR:-value}: ${VAR:-value}"
echo "VAR: ${VAR}"
echo

VAR="Hello Bash"
echo "define VAR: ${VAR}"
echo "\${VAR:+value}: ${VAR:+value}"
echo "VAR: ${VAR}"
echo

VAR="Hello Bash"
echo "define VAR: ${VAR}"
echo "\${VAR:?value}: ${VAR:?value}"
echo "VAR: ${VAR}"
echo

# undefine var operation
unset VAR
echo "undefine VAR: ${VAR}"
echo "\${VAR:=value}: ${VAR:=value}"
echo "VAR: ${VAR}"
echo

unset VAR
echo "undefine VAR: ${VAR}"
echo "\${VAR:-value}: ${VAR:-value}"
echo "VAR: ${VAR}"
echo

unset VAR
echo "undefine VAR: ${VAR}"
echo "\${VAR:+value}: ${VAR:+value}"
echo "VAR: ${VAR}"
echo

unset VAR
echo "undefine VAR: ${VAR}"
#echo "VAR:?value ${VAR:?value}"  # show err
echo "VAR: ${VAR}"
echo
```

1. 基本取值與預設值

```
語法                     說明
──────────────────────────────────────────────
${var}                  取變數值
${var:-word}            若 var 未設定或為空，取 word
${var:=word}            若 var 未設定或為空，設定為 word 並取值
${var:?msg}             若 var 未設定或為空，顯示錯誤 msg 並退出
${var:+word}            若 var 已設定且非空，取 word，否則空字串
```

```bash
#!/bin/bash

set -euo pipefail

${1:-help}
```

```bash
export HOST_IP=${HOST_IP:=127.0.0.1}
export PYTHONPATH=".:${WORK_DIR}${PYTHONPATH:+:$PYTHONPATH}"
```

2. 字串長度與子字串

```
語法                     說明
──────────────────────────────────────────────
${#var}                 變數字串長度
${var:offset}           從 offset 開始 (0-based) 的子字串
${var:offset:length}    從 offset 開始，長度 length 的子字串
```

3. 前後綴刪除

```
語法                     說明
──────────────────────────────────────────────
${var#pattern}          從頭刪掉最短符合 pattern 的部分
${var##pattern}         從頭刪掉最長符合 pattern 的部分
${var%pattern}          從尾刪掉最短符合 pattern 的部分
${var%%pattern}         從尾刪掉最長符合 pattern 的部分
```

4. 字串取代

```
語法                     說明
──────────────────────────────────────────────
${var/pat/repl}          取代第一個符合 pat 的部分為 repl
${var//pat/repl}         全部取代
${var/#pat/repl}         若開頭符合 pat，則取代
${var/%pat/repl}         若結尾符合 pat，則取代
```

5. 大小寫轉換

```
語法                     說明
──────────────────────────────────────────────
${var^}                 把第一個字元轉大寫
${var^^}                全部字元轉大寫
${var,}                 把第一個字元轉小寫
${var,,}                全部字元轉小寫
```

6. 預設值

```
name=""
echo ${name:-Guest}   # name 為空，輸出 Guest
echo ${name:=Guest}   # name 為空，設定 name=Guest 並輸出
echo ${name:?Empty}   # name 為空，錯誤訊息 "Empty"
unset name
echo ${name:+Set}     # name 未設定，輸出空
```

---

## if

```bash
if [ "x$SEX" == "xmale" ]; then
  echo "Hi male"
else
  echo "Hi Female"
fi

[ "x$SEX" == "xmale" ] && echo "Hi male" || echo "Hi Female"

dividend=10
divisor=3
result=$((dividend % divisor == 0 ? divisor : dividend % divisor))

```

---

## for

```bash
for ((i=1; i<=3; i++)); do
  echo $i
done

for E in "1 2 3"; do
  echo "index: $E"
done

for E in 1 2 3; do
  echo "index: $E"
done

for E in `echo -e "1\n2\n3"`; do
  echo "index: $E"
done

for E in `seq 3`; do
  echo "index: $E"
done

for f in /etc/*.conf; do
  echo $f
done

seq 3 | xargs -i echo "{}"
```

---

## while

```bash
i=0
while [ $i -lt 3 ]; do
  i=`expr $i + 1`
  echo "$i"
done

i=0
while true; do
  i=`expr $i + 1`
  echo "$i"
  if [ $i -ge 3 ]; then
    break
  fi
done

while read -r line; do
  username=`echo $line | awk -F: '{print $1}'`
  home=`echo $line | awk -F: '{print $6}'`
  echo "username: $username, home: $home"
done < /etc/passwd
```

---

## until

```bash
i=0
until [ $i -eq 3 ]; do
  i=`expr $i + 1`
  echo "$i"
done

i=0
until false; do
  i=`expr $i + 1`
  echo "$i"
  [ $i -ge 3 ] && break
done
```

---

## case

```bash
case $SHELL in
  "/bin/bash")
    echo "BASH"
    ;;

  "/bin/tcsh")
    echo "TCSH"
    ;;

  *)
    echo "UNKNOWN"
    ;;
esac
```

---

## select

```bash
select V in a b q; do
  echo "select: $V"
  [ "$V" == "q" ] && break
done
```

---

## heredoc

```bash
cat > tmp.txt << EOF
echo "hello bash"
EOF

cat >> tmp.txt << EOF
echo "hi bash"
EOF

mysql -u root << EOF
  USE nova;
  SELECT id hypervisor_hostname FROM compute_nodes WHERE hypervisor_hostname = "$HOST";
  DELETE FROM compute_nodes WHERE hypervisor_hostname = "$HOST";
EOF

mongo << EOF
use $DB
print("$COLLECTION")
db.getCollection("$COLLECTION").findOne()
EOF
```

---

## array

```bash
# Array
declare -a ARR
ARR=(eth0 em1)
ARR+=(en0)
echo "ARR Length: ${#ARR[@]}"

for ITEM in ${ARR[*]}; do
  echo "ITEM: $ITEM"
done

for ((i=0; i < ${#ARR[@]}; i++)); do
  echo "Index: $i, ITEM: ${ARR[$i]}"
done

# Array Append
A1=(1 2 3 X)
A2=(a b c X)
A3=(${A1[@]} ${A2[*]})

# String to Array
S=1,2,3,4
A=(`echo $S | sed 's/,/ /g'`)

# Associated Array
declare -A MAP
MAP=( [eth0]=192.168.0.1 [em1]=172.16.0.1 )

echo "MAP Length: ${#MAP[@]}"

for KEY in ${!MAP[@]}; do
  echo "KEY: $KEY, VALUE: ${MAP[$KEY]}"
done
```

```bash
###
### for bash 4.2-
###

# pass array to function
show_array() {
  eval "declare -A arr="${1#*=}

  for i in "${arr[@]}"; do
    echo "$i"
  done
}

arr=(one two three)
show_array "$(declare -p arr)"

# pass associative array to function
show_associative_array() {
  eval "declare -A ass_arr="${1#*=}

  for k in ${!ass_arr[@]}; do
    echo "key: $k -> val: ${ass_arr[$k]}"
  done
}

declare -A ass_arr
ass_arr=([eth0]=192.168.0.1 [em1]=172.16.0.1)
show_associative_array "$(declare -p ass_arr)"

###
### for bash 4.3+
###

# pass array to function
show_array() {
  local -n arr=$1

  for i in "${arr[@]}"; do
    echo "$i"
  done
}

ARRAY=(one two three)
show_array ARRAY

# pass associative array to function
show_associative_array() {
  local -n ass_arr=$1

  for k in ${!ass_arr[@]}; do
    echo "key: $k -> val: ${ass_arr[$k]}"
  done
}

declare -A MAP
MAP=([eth0]=192.168.0.1 [em1]=172.16.0.1)
show_associative_array MAP
```

---

## dollar sign

```bash
echo "script name: $0"
echo "first argument: $1"
echo "number of arguments: $#"
echo "all arguments (\$*): $*"
echo "all arguments (\$@): $@"
echo "process id: $$"
echo "last command status: $?"
echo "previous background pid: $!"
```

```bash
echo "#: $#, @: $@, *: $*, 1: $1"
shift
echo "#: $#, @: $@, *: $*, 1: $1"
```

---

## declare

在 BASH 中， `declare` 和 `typeset` 實際上是同一個指令。`typeset` 是為了相容舊的 KornShell (ksh) 而存在的，在 BASH 中，官方更推薦使用 `declare`。
這指令的作用是：聲明變數的屬性（如唯讀、整數、陣列等）或修改變數的定義。

**屬性設定選項 (Attributes)**

| Option | Attribute   | Explain                                                              |
| ------ | ----------- | -------------------------------------------------------------------- |
| -i     | Integer     | 將變數設為「整數」。進行賦值時會自動進行算術運算。                   |
| -a     | Array       | 宣告為「索引陣列」(Indexed Array)，下標為數字。                      |
| -A     | Associative | 宣告為「關聯陣列」(Associative Array)，下標為字串（類似 Hash/Map）。 |
| -r     | Read-only   | 設為「唯讀」。設定後無法修改值，也無法用 unset 刪除。                |
| -x     | Export      | 將變數標記為「環境變數」，效果等同於 export。                        |
| -l     | Lower       | 賦值時，自動將所有大寫字母轉換為小寫。                               |
| -u     | Upper       | 賦值時，自動將所有小寫字母轉換為大寫。                               |
| -n     | Nameref     | 建立「變數引用」（指標）。修改此變數會實際改動它所指向的變數。       |
| -t     | Trace       | 替變數加上追蹤屬性（較少用，通常用於函數）。                         |

**顯示與查詢選項 (Display)**

| Option | Attribute | Explain                                                                       |
| ------ | --------- | ----------------------------------------------------------------------------- |
| -p     | Print     | 顯示指定變數的屬性與值。如果不加名稱，則列出所有變數。                        |
| -f     | Function  | 列出所有已定義的函數內容。                                                    |
| -F     | Function  | name。僅列出函數名稱，不顯示原始碼。                                          |
| -g     | Global    | 在函數內部使用時，強制變數具備全域作用域（預設 declare 在函數內是區域變數）。 |

**大小寫轉換 (-l, -u)**

```bash
declare -u upper_str="hello"
echo $upper_str   # HELLO

declare -l lower_str="WORLD"
echo $lower_str   # world
```

**強制整數運算 (-i)**

```bash
declare -i num
num=10+5
echo $num           # 15

# 如果不使用 -i，BASH 會把數字當成字串拼接。
text=10+5
echo $text          # 10+5
```

**唯讀變數 (-r)**

```bash
declare -r API_KEY="secret_123"
API_KEY="hacked"    # readonly variable
```

**關聯陣列 (-A)**

```bash
declare -A user_shells
user_shells=( ["amy"]="/bin/zsh" ["bob"]="/bin/bash" )

echo ${user_shells["amy"]}    # /bin/zsh
```

**檢查變數狀態 (-p)**

```bash
declare -p user_shells        # declare -A user_shells=( [bob]="/bin/bash" [amy]="/bin/zsh" )
```

**引用變數 (-n)**

```bash
target="real_value"
declare -n ref=target     # ref 指向 target
ref="new_value"           # 修改 ref 等於修改 target

echo $target              # new_value
```

**區域變數 (Local Variables)**

```bash
my_func() {
    declare local_var="I am hidden"   # local_var="I am hidden"
    echo $local_var
}

my_func
echo $local_var
```

---

## set

在 BASH 中，`set` 是一個極其強大的內建指令。它的核心功能有二：

1. 設定 Shell 的執行選項（Flags）
2. 管理位置參數（Positional Parameters）。

與 `declare` 不同，`set` 通常是用來改變 「Shell 運作的行為模式」。

**`set -o`**: 以「可讀列表」顯示所有選項及其開關狀態 (on 或 off)。用於快速檢查目前 errexit 或 xtrace 是否啟動。
**`set +o`**: 以「指令格式」輸出。印出一系列 set -o 或 set +o 的指令。用於環境備份。可將輸出存入變數，稍後執行還原 Shell 狀態。
**`set -o` <opt>**: 開啟特定功能，`-` 號是用來觸發（Enable）一個選項。
**`set +o` <opt>**: 關閉特定功能，`+` 號是用來停用（Disable）一個選項。

| Option | Option Name (-o) | Explain                                               | 常用場景                   |
| ------ | ---------------- | ----------------------------------------------------- | -------------------------- |
| -e     | errexit          | 出錯即停止。指令回傳非 0 時腳本立刻退出。             | 必用。防止錯誤擴大。       |
| -u     | nounset          | 未定義報錯。存取未聲明的變數時視為錯誤。              | 必用。防止拼錯變數名。     |
| -x     | xtrace           | 指令追蹤。執行前先印出該行指令（含變數展開）。        | 除錯 (Debug) 專用。        |
| -n     | noexec           | 語法檢查。讀取指令但不執行。                          | 測試腳本語法是否正確。     |
| -f     | noglob           | 停用通配符。禁止 \*、?、[] 的路徑展開。               | 處理包含特殊符號的檔名。   |
| -v     | verbose          | 詳細模式。在執行前印出讀取到的輸入列。                | 觀察腳本如何讀取源碼。     |
| -a     | allexport        | 自動導出。隨後定義的所有變數都會被 export。           | 快速將本地變數轉環境變數。 |
| -C     | noclobber        | 禁止覆蓋。使用 > 重導向時，若檔案已存在則報錯。       | 防止意外覆蓋重要檔案。     |
| -m     | monitor          | 作業控制。開啟後台作業報告與控制。                    | 交互式 Shell 預設開啟。    |
| -P     | physical         | 實體路徑。執行 cd 等指令時不跟隨符號連結 (symlinks)。 | 需要獲取真實硬碟路徑時。   |

```bash
linux:~ # set
linux:~ # set -o
linux:~ # set +o

linux:~ # set -e    # enable errexit
linux:~ # set -o
linux:~ # set +o

linux:~ # set +e    # disable errexit
linux:~ # set -o
linux:~ # set +o
```

```bash
set -e
foo
echo "bar"


set -eo pipefail
foo | echo "a"
echo "bar"


set -u
echo $a
echo "bar"
```

```bash
#!/bin/bash
set -euo pipefail   # Strict Mode
# set -e            => errexit
# set -u            => nounset
# set -o pipefail   => pipefail

set -x  # enable Debug mode
...
set +x  # disable Debug mode
```

---

## grep

---

## sed

```bash
linux:~ # echo "Hello BASH script" | sed 's/.//6g'              # Hello
linux:~ # echo "Hello BASH script" | sed 's/.\{6\}//'           # BASH script
linux:~ # echo "Hello BASH script" | sed 's/.\{6\}//;s/.//5g'   # BASH

linux:~ # echo /usr/lib/python/site-package/xxx-1.0/yyy.zz | sed 's/\(.*\)\..*$/\1/'    # /usr/lib/python/site-package/xxx-1.0/yyy
linux:~ # echo /usr/lib/python/site-package/xxx-1.0/yyy.zz | sed 's/\..*$//'            # /usr/lib/python/site-package/xxx-1
linux:~ # echo /usr/lib/python/site-package/xxx-1.0/yyy.zz | sed 's/\///'               # usr/lib/python/site-package/xxx-1.0/yyy.zz
linux:~ # echo /usr/lib/python/site-package/xxx-1.0/yyy.zz | sed 's/.*\///'             # yyy.zz

linux:~ # sed "s/\r//g" <file>    # remove ^M (windows carry return)
```

```bash
linux:~ # cat data.csv
Andy Jiang, ACA-4566, 10
Joe Hwang, M16-1226, 20
Tim Cheng, YKC-7725, 10
John Cheng, YKC-7722, 10
Kevin Lin, NI2-039, 100
David Lee, 2C-323, 200
Herry McGray Jr., 3C-123, 500
LeeLongDa, 3C-123, 500

linux:~ # sed -n 2,4p data.csv
linux:~ # sed -n '2p;4p' data.csv
linux:~ # sed -n '/Joe/,/Cheng/p' data.csv
linux:~ # sed -n '/Joe/p;/Cheng/p' data.csv
linux:~ # sed '/Tim/q' data.csv
```

[sed](./sed.md)

---

## awk

```bash
linux:~ # seq 5 | awk ' { sum = sum + $1 } END { print sum }'

# awk access shell variable
linux:~ # awk -v today="`date`" 'BEGIN {print today}'

# awk access environment variable
linux:~ # awk 'BEGIN {print ENVIRON["HOME"]}'

# awk argument
linux:~ # awk 'BEGIN {print ARGV[0], ARGV[1]}' "`date`"

# awk script
linux:~ # cat avg.awk
#!/usr/bin/awk -f

BEGIN {
  sum = 0
}

{
  sum = sum + $1
}

END {
  "count:", NR
  "sum: ", sum
  "average: %f\n", sum/NR
}

# regrex
linux:~ # awk '/<pattern>/{print $_}' <file>
linux:~ # awk '{if ($1 ~ /<pattern>/) print $_}' <file>
linux:~ # awk '{if ($1 == "<pattern>") print $_}' <file>
linux:~ # awk '$1 ~ /<pattern>/{print $_}' <file>
linux:~ # awk '$1 == "<pattern>"{print $_}' <file>

# double quote
linux:~ # awk "\$1 == \"<pattern>\" {printf \"$HOME %s\", \$_}" <file>

# NF: number fields (column), NR: number record (row), $_
linux:~ # awk '{if (NF < 3) {printf line %s, %s\n", NR, $_}}' <file>
```

[awk](./awk.md)

---

## find

```bash
# date
linux:~ # find . -maxdepth 1 -mindepth 1 -type d
linux:~ # find . -ctime +7 -type f
linux:~ # find . -ctime -7 -type f
linux:~ # find . -ctime  7 -type f

# hard link
linux:~ # find / -samefile <file>
linux:~ # find / -xdev -samefile <file>
```

---

## expect

```bash
#!/bin/bash
hostname=127.0.0.1
username=root
password=root

/usr/bin/expect << EOF

set time 30
spawn ssh $username@$hostname uptime
expect {
  "*yes/no" { send "yes\n"; exp_continue }
  "*password:" { send "$password\n" }
}
expect eof
EOF
```

[expect](./expect.md)

---

## xargs

```bash
linux:~ # seq 5 | xargs echo
linux:~ # seq 5 | xargs -t echo
linux:~ # seq 5 | xargs -t -n1 echo
linux:~ # seq 5 | xargs -I {} echo {}
linux:~ # seq 5 | xargs -i date
linux:~ # seq 5 | xargs -i sh -c 'expr {} + 1'
linux:~ # find . -type d | xargs -n1 ls -l
linux:~ # awk -F: '$7 !~/nologin/{print $1, $3}' /etc/passwd | xargs -n2  sh -c 'echo "uid: $1 user: $0"'

linux:~ # hi() {
  local h=$1
  echo "Hi $h"
}
linux:~ # export -f hi
linux:~ # awk -F: '{print $1}' /etc/passwd | xargs -i sh -c 'hi {}'
```

**深入理解 BASH `export -f`**

通常情況下，變量（variable）可通過 export 傳遞給子進程（sub-shell），但函數（function）不行。`-f` 選項打破了這個限制。

使用時機與場合：

- 平行運算： 使用 xargs 或 GNU Parallel 調用多個子進程來處理數據，且處理邏輯寫在一個函數裡時。
- 腳本拆分： main script 定義了通用工具函數，並希望被它調用的 sub script 直接使用。
- 自動化環境： 在複雜的 CI/CD 流程中，將一段邏輯「導出」到後續執行的 Shell 環境中。

---

## parallel

```bash
linux:~ # date && seq 5 | xargs -i sh -c "echo {} && sleep {}" && date
linux:~ # date && seq 5 | xargs -P 5 -i sh -c "echo {} && sleep {}" && date
linux:~ # date && seq 5 | parallel -j 5 "echo {} && sleep {}" && date
```

---

## compgen

```bash
# command
linux:~ # compgen -a  # alias
linux:~ # compgen -b  # builtin command
linux:~ # compgen -c  # command

# variable
linux:~ # compgen -e  # shell variable
linux:~ # compgen -v  # all variable

# file, directory
linux:~ # compgen -f  # file
linux:~ # compgen -d  # directory

# user, group
linux:~ # compgen -u  # user
linux:~ # compgen -g  # group

# wild list
linux:~ # compgen -W "aa ab Aa xyz abc123" -- a
```

---

## complete

```bash
linux:~ # complete -p   # list bash completion
linux:~ # complete -r   # remove bash completion

linux:~ # echo -e '#!/bin/bash\n\necho "ARG: $@"' > foo
linux:~ # chmod +x foo
linux:~ # touch a.foo b.foo c.foo

# filter pattern
linux:~ # complete -f -X '!*.foo' foo
linux:~ # ./foo <TAB><TAB>

# word list
linux:~ # complete -W 'abc xyz 123' foo
linux:~ # ./foo <TAB><TAB>

# function
linux:~ # function _foo_complete_() {
    local cmd="${1##*/}"
    local word=${COMP_WORDS[COMP_CWORD]}
    local line=${COMP_LINE}
    local xpat='!*.foo'

    echo
    echo "cmd: $cmd"
    echo "cur: ${cur}"
    echo "comp_cword: $COMP_CWORD"
    echo "comp_words: ${COMP_WORDS[*]}"
    echo "comp_line: ${COMP_LINE}"

    COMPREPLY=($(compgen -f -X "$xpat" -- "${cur}"))

    echo "compreply: ${COMPREPLY[*]}"

}
linux:~ # complete -F _foo_complete_ foo
linux:~ # ./foo <TAB><TAB>
```

---

## trap

```bash
linux:~ # trap "echo hello trap" SIGTERM
linux:~ # trap -p
linux:~ # kill -s SIGTERM `echo $$`
linux:~ # trap - SIGTERM

linux:~ # trap "echo hello trap" 15
linux:~ # trap -p
linux:~ # kill -15 `echo $$`
linux:~ # trap - 15

linux:~ # trap "echo hello trap" 2
linux:~ # trap
linux:~ # ctrl^c
linux:~ # trap 2
```
