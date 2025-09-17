# zsh

## zsh 啟動檔案

zsh 有多種啟動檔案，依不同情境載入：

| 檔案           | 何時執行                                  | 用途                                            |
| -------------- | ----------------------------------------- | ----------------------------------------------- |
| **`zshenv`**   | 每次啟動 Zsh 都會執行（最先）             | 設定環境變數（`PATH`），不要放 alias 或互動設定 |
| **`zprofile`** | login shell 讀取，類似 bash 的 `.profile` | 設定登入時需要的環境                            |
| **`zshrc`**    | interactive shell 讀取                    | 常用設定：alias、prompt、自訂 function          |
| **`zlogin`**   | login shell，`zprofile` 後讀取            | 類似歡迎訊息或登入後的動作                      |
| **`zlogout`**  | login shell 結束時                        | 登出時要做的清理                                |

## zsh script

1. 執行方式

```sh
# 直接執行
linux:~ $ chmod +x script.zsh
linux:~ $ ./script.zsh

# 指定解譯器
linux:~ $ zsh script.zsh

# 內嵌執行
linux:~ $ source script.zsh   # 或 . script.zsh
```

2. 變數

```bash
# declare
os="Linux"
echo $os

# array
arr=(apple banana cherry)
echo $arr[1]     # apple (Zsh index 從 1 開始!)
echo $arr[-1]    # cherry (倒數)

# hash map
typeset -A info
info=(os Linux platform x86)
echo $info[os]
```

- bash 從 $arr[0]， zsh 從 $arr[1] 開始。
- hash map 需要 typeset -A 宣告。

3. 判斷與迴圈

```sh
# if
if [[ -f "file.txt" ]]; then
  echo "檔案存在"
else
  echo "檔案不存在"
fi

# for
for i in {1..3}; do
  echo "第 $i 次"
done

# while
count=1
while [[ $count -le 3 ]]; do
  echo "計數 $count"
  ((count++))
done
```

- 推薦用 [[]] 而不是 [ ]，因為支援更多字串與模式比對。

4. 函數

```sh
# define
hello() {
  echo "Hello, $1"
}
hello Linux

# return
add() {
  echo $(($1 + $2))
}
result=$(add 5 3)
echo $result   # 8
```

5. pipeline

1️⃣ 基本概念

把一個命令的 輸出 (stdout)，接到另一個命令的 輸入 (stdin)

```sh
# 指令
cmd1 | cmd2 | cmd3

# 資料流向
[stdout] ─► [stdin] ─► [stdout] ─► [stdin] …
```

```sh
cat /etc/passwd | grep "bash" | wc -l
```

2️⃣ stderr 與 stdout 差異

- stdout (1)：送到管線右邊
- stderr (2)：不會進管線，直接輸出到螢幕

```sh
ls /notfound | wc -l
```

3️⃣ 常見變體

(1) 同時傳 stdout + stderr

```sh
# 指令
cmd1 |& cmd2

# 等同於
cmd1 2>&1 | cmd2
```

```sh
make |& tee build.log
```

(2) tee 分流

```sh
ls | tee list.txt | grep ".txt"

echo "Hello" | tee >(tr 'a-z' 'A-Z') >(rev) >(wc -c)
```

(3) process substitution

```sh
diff <(ls dir1) <(ls dir2)
```

6. prefix / suffix

```
╔══════════════════╦══════════════════════════════╦════════════════════════════════╗
║     語法         ║        說明                  ║            範例輸出             ║
╠══════════════════╬══════════════════════════════╬════════════════════════════════╣
║ ${#var}          ║ 字串長度 / 陣列元素數量       ║ file="abc.txt" → 7             ║
║                  ║                              ║ arr=(a b c) → 3                ║
╠══════════════════╬══════════════════════════════╬════════════════════════════════╣
║ ${var%pattern}   ║ 從尾端移除最短符合的字串     ║ f=report.txt → ${f%.txt}=report║
║ ${var%%pattern}  ║ 從尾端移除最長符合的字串     ║ f=report.txt → ${f%%.*}=report ║
╠══════════════════╬══════════════════════════════╬════════════════════════════════╣
║ ${var#pattern}   ║ 從前端移除最短符合的字串     ║ f=report.txt → ${f#*.}=txt     ║
║ ${var##pattern}  ║ 從前端移除最長符合的字串     ║ f=report.txt → ${f##*.}=txt    ║
╠══════════════════╬══════════════════════════════╬════════════════════════════════╣
║ ${var:pos}       ║ 從字串位置擷取 (1-based)     ║ f=abcdef → ${f:2}=bcdef        ║
║ ${var:pos:len}   ║ 從字串擷取子字串 (指定長度)  ║ f=abcdef → ${f:2:3}=bcd        ║
╠══════════════════╬══════════════════════════════╬════════════════════════════════╣
║ ${arr[i]}        ║ 陣列元素 (1-based)           ║ arr=(a b c) → ${arr[2]}=b      ║
║ ${arr[-1]}       ║ 陣列倒數元素                  ║ arr=(a b c) → ${arr[-1]}=c     ║
║ ${arr[2,4]}      ║ 陣列切片                      ║ arr=(a b c d) → b c d         ║
╠══════════════════╬══════════════════════════════╬════════════════════════════════╣
║ ${var/pat/repl}  ║ 取代第一個符合               ║ f=a_b_c → ${f/_/-}=a-b_c      ║
║ ${var//pat/repl} ║ 全部取代                     ║ f=a_b_c → ${f//_/-}=a-b-c     ║
║ ${var/#pat/repl} ║ 只取代前綴符合               ║ f=abc → ${f/#a/A}=Abc         ║
║ ${var/%pat/repl} ║ 只取代後綴符合               ║ f=abc → ${f/%c/C}=abC         ║
╠══════════════════╬══════════════════════════════╬════════════════════════════════╣
║ ${var:u}         ║ 字串轉大寫                   ║ f=hello → HELLO                ║
║ ${var:l}         ║ 字串轉小寫                   ║ f=HELLO → hello                ║
╠══════════════════╬══════════════════════════════╬════════════════════════════════╣
║ ${var^}          ║ 首字母大寫 (單字)            ║ f=hello → Hello                ║
║ ${var^^}         ║ 全部大寫 (字元)              ║ f=hello → HELLO                ║
║ ${var,}          ║ 首字母小寫 (單字)            ║ f=Hello → hello                ║
║ ${var,,}         ║ 全部小寫 (字元)              ║ f=HELLO → hello                ║
╠══════════════════╬══════════════════════════════╬════════════════════════════════╣
║ ${var:q}         ║ 加引號避免空白展開           ║ f="a b" → "a b"                ║
║ ${var// /_}      ║ 把空白取代成底線             ║ f="a b c" → a_b_c              ║
╠══════════════════╬══════════════════════════════╬════════════════════════════════╣
║ ${var:-default}  ║ 若未定義或空字串 → 用預設值  ║ unset v → ${v:-hi}=hi          ║
║ ${var:=default}  ║ 若未定義或空字串 → 設為預設  ║ unset v → ${v:=hi} → v=hi      ║
║ ${var:+alt}      ║ 若已定義且非空 → 用替代值    ║ v=foo → ${v:+ok}=ok            ║
║ ${var:?msg}      ║ 若未定義或空 → 顯示錯誤訊息  ║ unset v → ${v:?error}          ║
╚══════════════════╩══════════════════════════════╩════════════════════════════════╝
```

1️⃣ 去掉前綴 / 後綴

```sh
原字串:   report.final.txt
           ^^^^^^^^^^^^^^^

去掉最短後綴 (%):      ${f%.txt}
           └───────╴     → report.final

去掉最長後綴 (%%):     ${f%%.*}
           └──────────╴ → report

去掉最短前綴 (#):      ${f#*.}
           ╶──┘         → final.txt

去掉最長前綴 (##):     ${f##*.}
           ╶────────┘   → txt
```

2️⃣ 取代 (pattern substitution)

```sh
原字串:   a_b_c

取代第一個:   ${f/_/-}
              a-b_c

取代全部:     ${f//_/-}
              a-b-c

取代前綴:     ${f/#a/A}
              A_b_c

取代後綴:     ${f/%c/C}
              a_b_C
```

3️⃣ 大小寫轉換

```sh
原字串:   hello world

${f:u}   → HELLO WORLD   (全部大寫)
${f:l}   → hello world   (全部小寫)

${f^}    → Hello world   (首字母大寫)
${f^^}   → HELLO WORLD   (全部字元大寫)

${f,}    → hello world   (首字母小寫)
${f,,}   → hello world   (全部字元小寫)
```

4️⃣ 預設值 / 錯誤處理

```sh
unset f

${f:-default}   → default   (沒定義就用 default，不改變 f)
${f:=default}   → default   (沒定義就用 default，並且 f=default)
${f:+alt}       → alt       (已定義就用 alt，否則空)
${f:?error}     → error     (未定義時輸出錯誤並中止)
```

5️⃣ 陣列展開

```sh
arr=(a b c d)

${arr[2]}     → b      (第 2 個元素)
${arr[-1]}    → d      (倒數第 1 個元素)
${arr[2,3]}   → b c    (區間)
${#arr}       → 4      (元素數量)
```
