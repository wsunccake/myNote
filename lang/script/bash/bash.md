# BASH

## history

Shell 的演進歷史與兩大陣營

Unix Shell 的發展主要分為兩大陣營：Bourne Shell 家族和 C Shell 家族。

- Thompson Shell (sh)：這是第一代的 Unix Shell，由 Ken Thompson 在 1971 年開發。它的功能非常簡單，僅支援基本的指令執行。
- Bourne Shell (sh)：由 Stephen Bourne 在 1977 年開發，並隨著 UNIX V7 發布。它引入了更強大的腳本編程功能，例如流程控制（if, for）、變數、命令替換等，為現代 Shell 奠定了基礎。這個 sh 與 Thompson Shell 同名但功能截然不同，它開創了 Bourne Shell 家族。
- C Shell (csh)：由 Bill Joy 在 1978 年開發，最初是為 BSD Unix 設計。它的語法類似於 C 語言，引入了許多用於互動式操作的功能，例如命令歷史記錄、別名（aliases）和工作控制（job control）。這開創了 C Shell 家族。

接下來的 Shell 大多是這兩個家族的後繼者，它們在各自的基礎上增強了功能，但腳本語法大多保持著家族內的兼容性。

1. `sh` (`Bourne Shell`)

- 時間點： 1977 年左右，由 Stephen Bourne 在貝爾實驗室開發。
- 介紹：最初的 Bourne Shell，也是許多現代 Shell 的基礎。它是一個輕量且符合 POSIX 標準的 Shell。由於其廣泛的兼容性，sh 通常作為腳本執行時的預設 Shell (#!/bin/sh)，以確保腳本能在各種 Unix-like 系統上運行。在許多 Linux 發行版中，sh 實際上是指向 bash 或 dash 的一個符號連結（symbolic link）。
- 優點：
  - 高可攜性（Portability）：腳本幾乎可以在任何 Unix-like 系統上執行，兼容性極佳。
  - 輕量且快速：資源消耗少，啟動速度快。
- 缺點：
  - 缺乏互動式功能：沒有命令補全、行編輯等便利功能。
  - 腳本語法較為簡潔：缺少許多現代 Shell 的進階功能。
- 常用/適用系統：任何 Unix-like 系統，特別是用於需要高度可攜性的腳本。

2. `csh` (`C Shell`)

- 時間點： 1978 年由 Bill Joy 在加州大學柏克萊分校開發。
- 介紹：C Shell 的語法類似 C 語言，特別適合 C 語言開發者。它引入了命令歷史記錄、行編輯和工作控制等重要的互動功能，是早期 BSD 系統的預設 Shell。
- 優點：
  - 強大的互動式功能：命令歷史記錄和別名功能在當時非常先進。
  - 語法與 C 語言相似：對 C 語言開發者來說更容易上手。
- 缺點：
  - 腳本編程不推薦：存在許多語法陷阱和不一致性，例如處理變數和引號時的複雜性。
  - 兼容性較差：腳本可攜性不如 Bourne Shell 家族。
- 常用/適用系統：傳統的 BSD 系統，但現在通常不作為日常使用的首選。

3. `ksh` (`Korn Shell`)

- 時間點：1983 年由 David Korn 在貝爾實驗室開發。
- 介紹：由 David Korn 在 AT&T Bell Labs 開發，旨在結合 sh 的腳本功能和 csh 的互動式功能。ksh 被認為是 Bourne Shell 家族中最嚴謹和強大的成員之一。
- 優點：
  - 高效能：腳本執行速度通常比 Bash 快。
  - 進階腳本功能：支援浮點數運算、關聯陣列（associative arrays）等，更適合複雜的腳本開發。
  - 優異的行編輯能力：支援 vi 和 emacs 模式的行編輯。
- 缺點：
  - 授權問題：早期的版本是專有軟體，雖然現在已開源，但普及度仍不如 Bash。
  - 可讀性較低：部分進階語法對新手來說較難理解。
  - 常用/適用系統：企業級 Unix 系統（如 AIX, Solaris），也適用於需要高效能、複雜腳本的場景。

4. `ash` (`Almquist Shell`) 和 `dash` (`Debian Almquist Shell`)

- 時間點：1989 年由 Kenneth Almquist 開發。
- 介紹：ash 是由 Kenneth Almquist 開發的 Bourne Shell 克隆，以其輕量和快速著稱。dash 是 ash 的 Debian 版本。
- 優點：
  - 極致的輕量與速度：其二進制文件非常小，啟動和執行速度極快。
  - 符合 POSIX 標準：確保腳本的高度兼容性。
- 缺點：
  - 功能極少：只包含最基本的腳本功能，缺乏許多互動式和進階的特性。
  - 常用/適用系統：dash 是許多 Debian 和 Ubuntu 系統中 sh 的預設實現，特別適用於系統啟動腳本和輕量級嵌入式系統（如路由器）。

5. `tcsh` (`TENEX C Shell`)

- 時間點：在 1980 年代末期出現。
- 介紹：tcsh 是 csh 的增強版本，增加了命令補全、拼寫檢查等功能。它是 C Shell 家族最受歡迎的成員。
- 優點：
  - 強大的互動式功能：提供了更完善的命令補全和歷史記錄功能。
- 缺點：
  - 腳本問題依舊存在：與 csh 相同，腳本編程的限制和語法不一致性使其不適合用於複雜任務。
- 常用/適用系統：FreeBSD 的預設 Shell，部分老舊的 Unix 系統。

6. `bash` (`Bourne Again Shell`)

- 時間點：1989 年由 Brian Fox 為 GNU Project 開發。
- 介紹：由 GNU 項目開發，旨在取代 sh，同時兼容 sh 和 ksh 的大部分功能。bash 引入了許多強大的互動式和腳本功能，並因其易用性和 GNU/Linux 的普及而成為最廣泛使用的 Shell。
- 優點：
  - 功能豐富：支援陣列、命令補全、行編輯、命令歷史記錄等。
  - 廣泛普及：幾乎所有 Linux 發行版和 macOS 的預設 Shell，資源豐富且社群龐大。
  - 腳本兼容性高：大部分 sh 腳本都可以在 bash 中運行。
- 缺點：
  - 腳本執行效率：相較於 dash 或 ksh，bash 在執行腳本時可能稍慢，體積也較大。
- 常用/適用系統：幾乎所有 Linux 發行版和 macOS，是日常命令列操作和腳本編程的首選。

7. `zsh` (`Z Shell`)

- 時間點：1990 年由 Paul Falstad 開發。
- 介紹：zsh 是一個高度可配置的 Shell，融合了 bash、ksh 和 tcsh 的優點。它以強大的命令補全和豐富的主題插件系統（例如 Oh My Zsh）而聞名。
- 優點：
  - 無與倫比的命令補全：可以補全命令、參數、路徑甚至變數。
  - 豐富的客製化：支援主題、插件，可以打造個性化的命令列介面。
  - 腳本兼容性：在保持自己特色的同時，也能兼容大部分 bash 腳本。
- 缺點：
  - 配置複雜：雖然框架簡化了過程，但完全手動配置對新手來說較為困難。
  - 啟動速度：由於需要加載許多插件和設定，啟動速度可能稍慢。
- 常用/適用系統：macOS Ventura 之後的預設 Shell，以及大多數 Linux 發燒友和需要強大互動式功能的開發者。

8. `fish` (`Friendly Interactive SHell`)

- 時間點：2005 年左右。
- 介紹：fish 是一個特別為互動式使用設計的現代 Shell。它的目標是開箱即用，提供友善且智能的功能，無需複雜配置。
- 優點：
  - 智能與友善：即時的語法高亮、命令建議（根據歷史記錄和手冊頁）和命令補全。
  - 簡單的腳本語法：語法比傳統 Shell 更加簡潔和直觀。
  - 開箱即用：許多實用功能無需額外配置。
- 缺點：
  - 不兼容 POSIX 標準：這是 fish 最大的缺點。它的腳本語法與 Bourne Shell 家族完全不同，這意味著 sh 或 bash 腳本無法在 fish 中直接運行。
  - 不適合腳本編程：由於其語法不兼容，不適合編寫需要跨系統運行的腳本。
  - 常用/適用系統：需要高效、視覺化和友善命令列體驗的日常使用者和開發者。

| Shell    | 家族    | 特點                           | 適用情境                           |
| -------- | ------- | ------------------------------ | ---------------------------------- |
| sh       | Bourne  | 輕量、POSIX 標準、高可攜性     | 系統腳本、嵌入式系統               |
| csh      | C Shell | 語法似 C、強大互動式功能       | 老舊的 BSD 系統（不推薦腳本編程）  |
| ksh      | Bourne  | 高效能、進階腳本功能、嚴謹     | 企業級 Unix、複雜腳本              |
| ash/dash | Bourne  | 極致輕量、快速、POSIX 標準     | 嵌入式系統、系統啟動腳本           |
| tcsh     | C Shell | csh 增強版、更好的互動體驗     | 部分老舊 Unix 系統                 |
| bash     | Bourne  | 功能豐富、普及度最高、兼容性佳 | 日常使用、通用腳本編程             |
| zsh      | Bourne  | 強大客製化、智能補全、插件豐富 | 進階使用者、追求高效體驗的開發者   |
| fish     | 獨立    | 開箱即用、智能建議、友善介面   | 日常互動、不編寫可攜性腳本的使用者 |

---

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

# method 4s
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
