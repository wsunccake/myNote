# tcsh

## 🔹 tcsh / csh 啟動邏輯

1. Login shell

用 ssh、su -、或登入終端機（如 tty）時，會啟動 login shell。

讀取順序為：

    1. /etc/csh.cshrc（系統全域）
    2. /etc/csh.login（系統全域）
    3. ~/.cshrc（使用者設定，通常放 alias、prompt、常用環境設定）
    4. ~/.login（使用者設定，通常放 PATH、環境變數、初始化工作）
    5. ~/.login_conf（部分系統會用）

📌 備註：在 tcsh 中 .tcshrc 會優先於 .cshrc，若存在 .tcshrc 就不會再讀 .cshrc。

2. Non-login shell

已經登入系統後，再開一個 shell（例如直接執行 csh 或 tcsh），則只會讀：

    - /etc/csh.cshrc
    - ~/.cshrc 或 ~/.tcshrc

3. Logout

login shell 結束時，會讀取：

    - ~/.logout

## 🔹 tcsh

1. set

- 用來設定 shell 變數 (local variable)，只在當前 shell 內有效。
- 不會自動繼承到子行程。

```sh
set os="Linux"
echo $os
```

2. setenv

- 設定 環境變數 (environment variable)，會被子行程繼承。
- 類似 bash 的 export。

```sh
setenv PATH "/usr/local/bin:$PATH"
echo $PATH
```

3. env

- 顯示目前環境變數，或在修改後的環境執行指令。

```sh
env
env VAR=123
```

4. printenv

```sh
printenv VAR
```

## 🔹 tcsh script

1. 執行方式

tcsh script 通常以 .csh 或 .tcsh 為副檔名，檔案第一行要宣告 shell：

```sh
#!/bin/tcsh
echo "Hello from tcsh"
```

```sh
# 指定 shell 執行
linux:~ $ tcsh myscript.csh

# 加上執行權限再執行
linux:~ $ chmod +x myscript.csh
linux:~ $ ./myscript.csh
```

2. 變數

```sh
# 設定變數
set name = "Alice"
echo "Hello $name"

# 環境變數
setenv PATH "$PATH:/usr/local/bin"
echo $PATH

# 陣列
set fruits = (apple banana cherry)
echo $fruits[1]        # apple (索引從 1 開始，不是 0)
echo $fruits           # 全部
echo $#fruits          # 陣列長度
```

- tcsh 不支援 關聯式陣列
- 陣列索引從 1 開始，這和 bash 不一樣

3. 判斷 & 迴圈

```sh
# if 判斷
set x = 5
if ( $x > 3 ) then
    echo "x 大於 3"
else
    echo "x 小於等於 3"
endif

set ans = "y"
if ( "$ans" == "y" ) then
    echo "Yes"
endif

# switch 判斷
set ans = "y"
switch ( $ans )
case y:
case Y:
    echo "Yes"
    breaksw
case n:
case N:
    echo "No"
    breaksw
default:
    echo "其他輸入"
    breaksw
endsw
```

```sh
# foreach 迴圈
foreach i ( 1 2 3 4 5 )
    echo "數字: $i"
end

# while 迴圈
set count = 1
while ( $count <= 3 )
    echo "次數: $count"
    @ count++
end
```

- if 條件必須用括號 ( ) 包住
- 遞增用 @，而不是 bash 的 (( ))

4. 函數

⚠️ tcsh 沒有 真正的 `函數` 概念，常用的做法有兩種：

4-1. 使用 alias 模擬

```sh
alias hello 'echo "Hello $1"'
hello Alice
```

4-2. 把程式寫成獨立檔案

```sh
# add.csh
#!/bin/tcsh
@ sum = $1 + $2
echo $sum
```

```sh
linux:~ $ ./add.csh 3 4
```

5. pipeline

```sh
echo "abc" | read line
echo $line
```

- bash：$line 會是空的
- tcsh：最後一個 read line 在 當前 shell，所以 $line = abc

6. prefix & suffix modifiers

```sh
$var:modifier
```

6-1. prefix modifier

- :h → head（路徑去掉最後一層）
- :t → tail（取最後一部分）
- :r → root（去掉副檔名）
- :e → extension（取副檔名）
- :q → quote（加引號）
- :x → expand（展開成參數）

```sh
set file = /usr/local/bin/test.sh

echo $file:h    # /usr/local/bin
echo $file:t    # test.sh
echo $file:r    # /usr/local/bin/test
echo $file:e    # sh
```

6-2. suffix modifier

```sh
set name = "hello_world.txt"

echo $name:r         # hello_world
echo $name:e         # txt
echo $name:gs/_/-/   # hello-world.txt
echo $name:u         # HELLO_WORLD.TXT
```

- :gs/old/new/ → 全域取代
- :as/old/new/ → 取代第一個
- :q → 加上引號（避免空白被展開）
- :x → 拆成多個參數
- :u → uppercase
- :l → lowercase
