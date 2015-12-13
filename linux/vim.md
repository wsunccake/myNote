# VIM

## Level 1


### Mode / 模式

* normal mode

  進入 vim 就是處於 normal mode, 只能下按鍵指令, 不能輸入編輯文字. 這些指令可能是游標移動的指令, 也可能是編輯指令或尋找替換指令. 在任何非 normal mode 時, 可按 `Esc` 回到 normal mode

* insert mode

  進入 insert mode, 此時可鍵入文字, 編輯文章. 按 `i`, `a`, `o`, `O` 就會從 normal mode 進入 insert mode

* cmdline mode

  按 `:` 會進入 cmdline mode, 左下角會有一個冒號(:) 出現可下指令. 搜尋時的 `/` 及 `?` 按鍵也是屬於 cmdline mode


### Move / 移動

在 normal mode

  `h`, 向左移動一個字元

  `j`, 向下移動一個字元

  `k`, 向上移動一個字元

  `l`, 向右移動一個字元

  `Ctrl` ^ `f`, 向下 / 前翻頁（Forward）

  `Ctrl` ^ `b`, 向前 / 後翻頁（Backwad）


### Edit / 編輯

在 normal mode

  `x`, 刪除字元

  <i>n</i>`x`, 刪除 n 個字元

  `dd`, 刪除一整行文字

  `yy`, 複製一整行文字

  `p`, 貼上複製文字


### Opreate / 操作

在 cmdline mode

  :`h`[`elp`], 求助文件; :help

  :`e`[`edit`], 開啓檔案, :e!

  :`w`[`rite`], 儲存檔案, :w!

  :`q`[`uit`], 離開檔案, :q!, :wq, :qa

  :`r`[`ead`], 讀入檔案, :r !<i>cmd</i>, :r <i>file</i>


----


## Level 2


### Move / 移動

在 normal mode

  `0`, 移至行首（含空白字元）

  `^`, 移至行首第一個非空白字元

  `G`, 移至檔尾（全文最後一行的第一個非空白字元處）

  `gg`, 移至檔首（全文第一行之第一個非空白字元處）

  `w`, 移至次一個字（word）字首

  `W`, 同上，但會忽略一些標點符號

  `e`, 移至後一個字字尾

  `E`, 同上，但會忽略一些標點符號
  
  `b`, 移至前一個字字首

  `B`, 同上，但會忽略一些標點符號

  <i>n</i>`G`, 移至第 <i>n</i> 行

在 cmdline mode

  :<i>n</i>, 移動到第 <i>n</i> 行

  /<i>pattern</i>,

  ?<i>pattern</i>,


### Edit / 編輯

在 normal mode

  `D`, `d$`, 刪除至行尾

  `d0`, `d^`, 刪除至行首

  `dG`, 刪除至檔尾

  `dgg`, 刪除至檔首

  `d`</>n</i>`G`, 刪除至第 n 行

  <i>n</i>`dd`, , 刪除 n 行

  `y`</>n</i>`y`, 複製 n 行文字


在 cmdline mode


* :`d`[elete], 刪除; :[<i>range</i>]`d`

  :<i>n</i>`d`, 刪除第 n 行

  :.,<i>n</i>`d`, 刪除至第 n 行

  :.,+<i>n</i>`d`, 刪除 n 行

  :.,$`d`, 刪除至檔尾

  :0,.`d`, 刪除至檔首

  :%`d`, 刪除全部

* :`p`[`rint`], 顯示, :[<i>range</i>]`p`, 使用方式 `delete`

* :`m`[`ove`], 移動, :[<i>range</i>]`m`<i>address</i>, <i>range</i> 表示方式同 `delete`

  :<i>n</i>`m`<i>m</i>, 第 n 行移動到第 m 行

* :`co`[py], :[<i>range</i>]`m`<i>address</i>, 使用方式同 `move`


----


## Level 3


### Mode / 模式

* visual mode

  進入 visual mode, 此時才能反白選取文字, 按 `v`, `Ctrl` ^ `v`, 會從 norml mode 進入 visual mode


### Edit / 編輯

在 normal mode

  

在 cmdline mode

  :`reg`[isters], 顯示緩衝內容
