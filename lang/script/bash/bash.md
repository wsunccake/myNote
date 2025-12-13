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

## set

```bash
linux:~ # set
linux:~ # set -o
linux:~ # set -e
linux:~ # set +e
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
