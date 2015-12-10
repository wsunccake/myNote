# VIM

## Level 1


### Mode / 模式

* normal mode

  進入 vim 就是處於 normal mode, 只能下按鍵指令, 不能輸入編輯文字. 這些指令可能是游標移動的指令, 也可能是編輯指令或尋找替換指令. 在任何非 normal mode 時, 可按 `esc` 回到 normal mode

* insert mode

  進入 insert mode, 此時才可鍵入文字. 按 `i`, `a`, `o`, `O` 就會進入 normal mode, 此時才可鍵入文字, 編輯文章

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

  `dd`, 刪除一整行文字

  `yy`, 複製一整行文字

  `p`, 貼上複製文字


### Opreate / 操作

在 cmdline mode

  :`h`[`elp]`, 求助文件

  :`e`[`edit`], 開啓檔案

  :`w`[`rite`], 儲存檔案

  :`q`[`uit`], 離開檔案

  :`r`[`ead`], 讀入檔案


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

在 cmdline mode