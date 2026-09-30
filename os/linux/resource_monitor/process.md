# Linux Process / Task 診斷備忘

整機 `%idle` 低、Use% 高、await 高，只說明「系統某一層忙」。要對到「是哪一個行程、卡在什麼狀態」，才用這份。CPU 時間刻度見 [processor.md](processor.md)；記憶體數字見 [memory.md](memory.md)；誰在讀寫磁碟見 [disk.md](disk.md) 的 iotop / `lsof +L1`。

Linux 的排程單位是 task（執行緒）。同一個 PID 底下可以有多個 LWP（`nlwp`）；`ps -L`、`pidstat -t`、`/proc/<PID>/task/` 看的是執行緒層。

---

## ps

ps 做一次性快照，適合腳本與「列出這個行程現在長什麼樣」。不是連續監控。

```bash
linux:~$ ps -eo pid,ppid,user,stat,ni,psr,nlwp,%cpu,%mem,rss,vsz,etime,cputime,comm --sort=-%cpu | head
    PID    PPID USER     STAT  NI PSR NLWP %CPU %MEM   RSS    VSZ     ELAPSED     TIME COMMAND
   4821    2801 kam      Rl     0   2    1 99.0  0.2 98432 812344       12:34 00:12:34 python3
    812       1 root     Ss     0   0    1  0.3  0.0 12288 185000    12-04:18 00:45:01 systemd
   1204    2801 kam      Sl     0   1   12  0.1  0.4 198000 2500000    03:22:01 00:01:02 firefox
```

📊 身份與樹

- **PID / PPID**：
  - 行程 ID 與父行程。孤兒會被 init / systemd（PID 1）收養，PPID 變成 1。
- **USER**：
  - 有效使用者。真正啟動時的 uid 要用 `ps -o ruser` 或 `/proc/<PID>/status` 的 Uid。

📊 狀態與排程（💡 行程「卡在哪」先看這裡）

- **STAT**：
  - 第一個字母最重要：
  - `R`：可執行或正在跑。
  - `S`：可中斷睡眠（等事件、鎖、網路、timer）。多數閒置行程是 S，正常。
  - `D`：不可中斷睡眠，多半在等磁碟或 NFS。⚠️ load average 會把 D 算進去；整機 `%idle` 仍可能很高。
  - `Z`：zombie。本體已結束，父行程還沒 `wait`。它幾乎不佔 CPU / 記憶體，但 PID 號還佔著。
  - `T` / `t`：被停止（SIGSTOP / 除錯器）。
  - 常見修飾：`l` 多執行緒、`s` session leader、`+` 前景行程群組、`<` 高優先權、`N` 低 nice。
- **NI**：
  - nice。數字越大，相對優先權越低（越「禮讓」）。對應後面的 `nice` / `renice`。
- **PSR**：
  - 最後（或目前）跑在哪一顆邏輯 CPU。對應 processor.md 的 top `P`、pidstat `CPU`。
- **NLWP**：
  - 這個行程的 LWP（執行緒）數。`1` 是單執行緒；很大時 `%CPU` 可以遠超過 100。

📊 資源占用

- **%CPU**：
  - ⚠️ 行程啟動至今的**平均**使用率（單一邏輯 CPU = 100%）。開很久但早就閒下來的行程，仍可能被早期尖峰拉高。要看「這一秒」改 top / pidstat。
- **%MEM / RSS**：
  - RSS 是常駐實體記憶體（KB）。`%MEM` ≈ RSS / 總實體記憶體。
  - 不含被換出的部分；共享函式庫會被多個行程各自算進 RSS，加總會高估。
- **VSZ**：
  - 虛擬位址空間大小。含未真正碰到的映射，通常遠大於 RSS。不能當成「用了多少 RAM」。
- **ELAPSED / TIME（cputime）**：
  - 牆鐘活了多久 / 累積 CPU 時間。TIME 對應 top 的 `TIME+`。

`ps aux` 是 BSD 風格、`ps -ef` 是 UNIX/GNU 風格；狀態字母 `R/S/D/Z` 含義相同。看診斷欄位時用 `-o` 自選最清楚。

`ps -Lp <PID>` 列出該行程底下每個 LWP（TID）。

---

## pstree

pstree 把父子關係畫成樹。適合找「這個服務是誰拉起來的、zombie 的父行程是誰」。

```bash
linux:~$ pstree -ap 2801
bash,2801
  └─python3,4821
```

```bash
linux:~$ pstree -ap 1 | head
systemd,1
  ├─sshd,812
  │   └─sshd,2800
  │       └─bash,2801
  │           └─python3,4821
```

- **-a**：
  - 顯示命令列參數（截斷過長時仍比光看 comm 有用）。
- **-p**：
  - 顯示 PID。要對 kill、`/proc/<PID>/` 必須加。
- **-n**：
  - 同層依 PID 排序，方便腳本比對。

💡 看到 `Z` 時，用 pstree 往上找還沒 `wait` 的父行程；殺 zombie 本身無效，要處理父行程（或等它結束，讓 PID 1 收養並回收）。

---

## top

top 是互動式總覽：上方是整機，下方是「誰在吃資源」。適合盯著看；不留歷史。整機 `%Cpu(s)` 的欄位意義見 [processor.md](processor.md) 的 top / mpstat。

```bash
linux:~$ top -bn1 | head -n 20
top - 01:40:05 up 12 days,  4:18,  1 user,  load average: 0.08, 0.12, 0.09
Tasks: 612 total,   1 running, 611 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.4 us,  0.2 sy,  0.0 ni, 99.3 id,  0.1 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :  47104.0 total,  22528.0 free,   1843.2 used,  22732.8 buff/cache
MiB Swap:   8192.0 total,   8192.0 free,      0.0 used.  45056.0 avail Mem

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   4821 kam       20   0  812344  98432   9216 R  99.0   0.2   12:34.56 python3
    812 root      20   0  185000  12288   8192 S   0.3   0.0   45:01.20 systemd
```

📊 Tasks 列

- **running / sleeping / stopped / zombie**：
  - 對應狀態 `R` / `S`（含部分其他可中斷等待）/ `T` / `Z` 的計數。
  - 💡 zombie 數持續增加：有父行程沒在回收子行程。

📊 行程列（這份要盯的）

- **PID / USER / COMMAND**：
  - 身份。互動模式下 `c` 可切成完整命令列。
- **PR / NI**：
  - 優先權顯示值與 nice。`RT` 代表即時排程類。
- **VIRT / RES / SHR**：
  - 虛擬大小 / 常駐 / 可共享。診斷「吃 RAM」看 **RES**，不要看 VIRT。
- **S**：
  - 狀態，同 ps 的第一個字母。
- **%CPU**：
  - 💡 最近一個取樣區間的使用率（單一邏輯 CPU = 100%）。與 ps 的「啟動至今平均」不同。
  - 多執行緒可超過 100；四顆邏輯 CPU 滿載可到約 400%。
- **%MEM / TIME+**：
  - 記憶體占比與累積 CPU 時間。

按 `H` 展開執行緒；按 `1` 看每顆邏輯 CPU。`-bn1` 只印一次後結束，方便貼進筆記。

---

## pidstat

確認整機吃緊之後，用 pidstat 看**哪一個**行程（或執行緒）在忙，以及它是在跑還是在等。

```bash
linux:~$ pidstat -u -r -d -p 4821 1 2
Linux 7.0.0-14-generic (linux)      09/22/2026      _x86_64_        (4 CPU)

01:40:07 AM   UID       PID    %usr %system  %guest   %wait    %CPU   CPU  Command
01:40:07 AM  1000      4821   98.00    1.00    0.00    0.00   99.00     2  python3

01:40:07 AM   UID       PID  minflt/s  majflt/s     VSZ     RSS   %MEM  Command
01:40:07 AM  1000      4821    120.00      0.00  812344   98432   0.20  python3

01:40:07 AM   UID       PID   kB_rd/s   kB_wr/s kB_ccwr/s iodelay  Command
01:40:07 AM  1000      4821      0.00      4.00      0.00       0  python3
```

⚠️ 帶間隔時，第一筆是開機至今。上面省略了第一筆。不指定 `-p` 會列出所有行程。

1. CPU（`-u`）

- **%usr / %system**：
  - 這個行程在使用者空間 / 核心空間的時間。
- **%wait**：
  - 💡 已可執行、卻在等 CPU 的時間比例。`%CPU` 不高但 `%wait` 高：它在排隊，CPU 被別人佔住。
- **%CPU**：
  - `%usr + %system`。預設單一邏輯 CPU = 100%；加 `-I` 改成整機百分比。
- **CPU**：
  - 這個區間最後跑在哪一顆邏輯 CPU。

2. 記憶體（`-r`）

- **minflt/s**：
  - 小缺頁（可從頁面快取或已映射頁滿足，不讀碟）。暴衝常代表在碰新地圖或擴堆。
- **majflt/s**：
  - 💡 大缺頁（要讀碟）。持續大於 0 常是記憶體壓力或冷啟動讀檔；對照 memory.md 的 si、disk.md 的 await。
- **RSS / %MEM**：
  - 常駐記憶體。

3. I/O（`-d`）

- **kB_rd/s、kB_wr/s**：
  - 這個行程造成的讀寫吞吐（task I/O accounting）。
- **kB_ccwr/s**：
  - 已寫入但後來被取消的（例如截斷）。真正落碟前被甩掉的量。
- **iodelay**：
  - 等待 I/O 的時鐘 tick。需要 delay accounting；沒開時可能一直是 0（見 disk.md iotop 對 `task_delayacct` 的說明）。

`pidstat -t` 拆到執行緒。`pidstat -w`：

- **cswch/s**：自願上下文切換（多半自己進入睡眠）。
- **nvcswch/s**：💡 非自願切換（被排程器搶佔）。與 `%wait` 一起升高 = 在搶 CPU。

---

## /proc/\<PID\>/

`/proc/<PID>/` 是 ps、top、pidstat、lsof 的共同來源。數字是當下快照；權限不足時部分檔案會 Permission denied。

```bash
linux:~$ tr '\0' ' ' < /proc/4821/cmdline; echo
python3 app.py --workers 4

linux:~$ grep -E '^(Name|State|PPid|Uid|Threads|voluntary_ctxt|nonvoluntary)' /proc/4821/status
Name:   python3
State:  R (running)
PPid:   2801
Uid:    1000    1000    1000    1000
Threads:        1
voluntary_ctxt_switches:        8421
nonvoluntary_ctxt_switches:     12033
```

常用檔：

- **cmdline**：
  - 完整命令列，參數以 `\0` 分隔。`ps` 的 COMMAND 截斷時來這裡。
- **environ**：
  - 環境變數（同樣 `\0` 分隔）。除錯「路徑、語言、代理」用。
- **status**：
  - 💡 人類可讀的狀態摘要。
  - **State**：同 ps 的 `R/S/D/Z/T`。
  - **PPid / Uid / Threads**：父行程、uid 四元組（real / effective / saved / fs）、執行緒數。
  - **VmRSS / VmSize**：對應 RSS / VSZ。
  - **voluntary_ctxt_switches / nonvoluntary_ctxt_switches**：累計切換次數，對應 pidstat `-w`。
- **stat**：
  - 同一組資料的機器可解析版（欄位很多）。腳本若自己 parse，注意 `comm` 欄位可能含括號與空格。
- **io**：
  - `rchar`、`wchar`、`read_bytes`、`write_bytes` 等累計 I/O。`read_bytes` / `write_bytes` 才是真正對儲存裝置的量。
- **fd/**、**fdinfo/**：
  - 開啟的檔案描述符。`ls -l /proc/<PID>/fd` 常比裝 lsof 更快。
- **cwd / exe / root**：
  - 工作目錄、可執行檔、chroot。umount busy 時看 cwd。
- **limits**：
  - 這個行程的 rlimit 實際值。對應 `ulimit` / `prlimit`。
- **sched / cpuset / affinity**：
  - 排程與 CPU 集合。親和性也可用 `taskset -cp`。
- **stack**：
  - 核心堆疊（通常要 root）。`State: D` 時可看卡在哪個核心路徑。
- **task/<TID>/**：
  - 每個執行緒一份縮小版的 `/proc`。`pidstat -t`、`ps -L` 讀這裡。
- **smaps / smaps_rollup**：
  - 記憶體映射明細。RSS 裡多少是 private、多少是 shared，深查時用；日常先看 status 的 VmRSS。

行程結束後，整個目錄消失。腳本要容忍 `ENOENT`。

---

## lsof

lsof 列出行程開啟的檔案、socket、cwd。磁碟空間對不上時的 `+L1` 見 [disk.md](disk.md)；這裡偏「這個 PID 握著什麼」。

```bash
linux:~$ lsof -p 4821
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 4821 kam  cwd    DIR  259,2     4096  131072 /home/kam/app
python3 4821 kam  txt    REG  259,2  5550152  390001 /usr/bin/python3
python3 4821 kam    0u   CHR   136,0      0t0       3 /dev/pts/0
python3 4821 kam    3w   REG  259,2 1073741824  18432 /var/tmp/big.dat
python3 4821 kam    5u  IPv4  78421      0t0     TCP *:8080 (LISTEN)
```

- **FD**：
  - `cwd` / `txt` / `mem`：工作目錄、可執行檔、映射的函式庫。
  - 數字 + `r/w/u`：真正的檔案描述符與讀寫模式。
- **TYPE**：
  - `REG` 一般檔、`DIR` 目錄、`CHR`/`BLK` 裝置、`FIFO`、`unix`、`IPv4`/`IPv6`。
- **NAME**：
  - 路徑或 `host:port`。`(deleted)` 表示目錄項已刪、fd 仍開著。

依檔案反查誰開著：`lsof /var/log/app.log`。依埠：`lsof -i :8080`。

---

## fuser

fuser 用較短的輸出回答「這個檔案或掛載點被哪些 PID 用」。

```bash
linux:~$ fuser -vm /var/tmp/big.dat
                     USER        PID ACCESS COMMAND
/var/tmp/big.dat:    kam        4821 F....  python3
```

```bash
linux:~$ fuser -vm /mnt/data
                     USER        PID ACCESS COMMAND
/mnt/data:           kam        4821 ..c..  python3
```

- **-v**：
  - 顯示 USER / PID / ACCESS / COMMAND。
- **-m**：
  - 指定掛載點時，列出所有使用該檔案系統的行程（含 cwd、開檔、mmap）。
- **ACCESS**：
  - `c` cwd、`e` 可執行檔被執行、`f` 開檔、`r` root 目錄、`m` mmap、`s` 共享函式庫。大寫常表示對該物件有寫入意圖。

⚠️ `fuser -k` 會送 SIGKILL。診斷階段先只用查詢；殺行程用下面的 kill，並先試 TERM。

---

## ulimit

ulimit 是 shell 內建，顯示或調整**當前 shell** 的資源上限。行程真正生效的值在 `/proc/<PID>/limits`。

```bash
linux:~$ ulimit -a
...
open files                          (-n) 1024
max user processes                  (-u) 127568
virtual memory              (kbytes, -v) unlimited
core file size              (blocks, -c) 0
```

```bash
linux:~$ cat /proc/4821/limits
Limit                     Soft Limit           Hard Limit           Units
Max open files            1024                 1048576              files
Max processes             127568               127568               processes
Max cpu time              unlimited            unlimited            seconds
```

- **soft / hard**：
  - 行程可把自己的 soft 調到 hard 以下；超過 soft 會失敗（例如 `EMFILE`、`EAGAIN`）。
  - hard 通常只有 root 能再往上調。
- **-n（open files）**：
  - 💡 `Too many open files` 先對這個。lsof 計數接近 soft limit 就是撞上上限，不是磁碟滿。
- **-u（max user processes）**：
  - 該使用者能建立的行程/執行緒數上限。頻繁 fork 失敗時對一下。
- **-v / -m**：
  - 虛擬記憶體 / 常駐上限。設太小會讓本來該能跑的程式被殺或 mmap 失敗。

systemd 服務的 LimitNOFILE 等會寫進該服務行程的 limits，與你登入 shell 的 ulimit 無關。查服務要用那個 PID 的 `/proc/<PID>/limits`。

---

## strace

strace 追蹤系統呼叫。在「行程活著、CPU 不高、又好像卡住」時，用來看它卡在哪一個 syscall。

```bash
linux:~$ strace -p 4821 -f -tt -T 2>&1 | head
01:40:07.123456 openat(AT_FDCWD, "/no/such/file", O_RDONLY) = -1 ENOENT (No such file or directory) <0.000012>
01:40:07.123500 read(5, "hello\n", 4096) = 6 <0.000004>
01:40:07.123520 futex(0x7f8c..., FUTEX_WAIT_PRIVATE, 0, NULL
```

- **-p**：
  - 附加到已存在的 PID（通常要權限）。
- **-f**：
  - 跟隨 clone 出來的執行緒 / 子行程。多執行緒服務幾乎一定要加。
- **-tt / -T**：
  - 時間戳與每個呼叫花費的秒數。💡 某個呼叫的 `<...>` 特別長，就是卡點。
- **-e trace=...**：
  - 只看某類呼叫，例如 `network`、`file`、`desc`，減少噪音。
- **輸出末尾卡住、沒有 `=`**：
  - 行程正阻塞在這個 syscall 裡（上例的 `futex`）。對應 ps 的 `S` 或 `D`。

⚠️ 附加 strace 會明顯拖慢目標。確認卡點後就該停。它顯示的是系統呼叫，不是使用者空間函式名（那是 ltrace）。

統計模式：`strace -c -p <PID>` 跑一段時間再中斷，看哪個 syscall 累計時間最多。

---

## ltrace

ltrace 追蹤動態函式庫呼叫（預設對 libc）。卡在使用者空間、又很少進核心時才用得上。

```bash
linux:~$ ltrace -p 4821 -tt -T 2>&1 | head
01:40:07.200000 malloc(64) = 0x55a1c80e2a00 <0.000003>
01:40:07.200100 strlen("hello") = 5 <0.000001>
01:40:07.200150 pthread_mutex_lock(0x55a1c80d1010
```

- 解讀方式與 strace 類似：最後一個沒返回的呼叫，就是目前卡的函式。
- 靜態連結、或熱路徑完全在自有代碼裡時，ltrace 幾乎看不到東西；改用 `perf`（processor.md）或除錯器。
- 同樣會拖慢目標；`-e` 可過濾函式名。

---

## nice / renice

nice 影響 CPU 排程的相對優先權，不改變磁碟配額，也不保證「比較慢的程式比較省記憶體」。

```bash
linux:~$ nice -n 10 bash -c 'echo started'
started

linux:~$ renice -n 5 -p 4821
4821 (process ID) old priority 0, new priority 5
```

- **nice 值**：
  - 範圍通常 -20～19。數字**越大**越禮讓（越容易把 CPU 讓給別人）。
  - 一般使用者只能把自己的行程往「更大（更禮讓）」調；往更小（更急）通常要 root。
- **nice**：
  - 啟動時帶著指定 nice 建立新行程。
- **renice**：
  - 改已存在的 PID（或 `-g` 程序組、`-u` 使用者）。

💡 top / ps 的 `NI` 就是這個值。`%nice`（mpstat）偏高，代表時間花在這些被調低優先權的行程上，不是「系統壞了」。

---

## taskset

taskset 讀（或設定）CPU 親和性：允許跑在哪些邏輯 CPU。診斷時先**讀**。

```bash
linux:~$ taskset -cp 4821
pid 4821's current affinity list: 0-3
```

```bash
linux:~$ taskset -cp 4821
pid 4821's current affinity list: 2
```

- **-cp**：
  - `-c` 用清單顯示；`-p` 指定 PID。
  - `0-3`：四顆都能跑。
  - 只有 `2`：再多核也只能用一顆。此時 processor.md 的 `mpstat -P ALL` 常只看到 CPU 2 的 `%idle` 接近 0。
- 不加 `-c` 時印十六進位 mask，位元對應邏輯 CPU 編號。

⚠️ 本節用來確認現況。亂改親和性可能把負載擠在同一顆實體核心；調校不在這份診斷範圍。

---

## kill / pkill / killall

這三個都是送訊號，不是「保證立刻消失」。預設訊號是 `TERM`（15）。

```bash
linux:~$ kill -TERM 4821
linux:~$ kill -0 4821 && echo still_there
still_there

linux:~$ pkill -TERM -u kam python3
linux:~$ killall -TERM python3
```

- **kill PID**：
  - 對單一 PID。`kill -0 PID` 不送訊號，只測「能不能對它送訊號」（存在且有權限）。
- **pkill**：
  - 依名稱、使用者、完整命令列（`-f`）等選。先 `pkill -l` 看訊號名；先不加 `-9`。
- **killall**：
  - 依行程名。⚠️ 在某些 Unix 上語意不同；在 Linux 上是「同名行程都送」。名稱要夠準，避免誤殺。
- **常見訊號**：
  - `TERM`（15）：請行程自己清理後結束。💡 先試這個。
  - `INT`（2）：等同 Ctrl+C。
  - `HUP`（1）：許多守護行程用來重新載入設定，不一定會退出。
  - `KILL`（9）：無法被捕捉，核心直接拆掉任務。⚠️ 不會跑應用程式自己的清理；共享記憶體、暫存檔、子行程可能留下。`D` 狀態卡在不可中斷 I/O 時，KILL 也要等它離開 D 才真正消失。
  - `STOP` / `CONT`：暫停 / 繼續（對應狀態 `T`）。

順序建議：`TERM` → 等幾秒看 `/proc/<PID>` 是否還在 → 再考慮 `KILL`。zombie（`Z`）殺不掉，要處理父行程。

---

## 🔍 判斷行程出了什麼事

**狀態（ps / top / `/proc/<PID>/status`）**

1. `R` 且 `%CPU` 高：在算。對照 processor.md 是否整機或單顆飽和。
2. `S` 且 `%CPU` 接近 0：多半在等事件。用 strace / ltrace 看卡在哪個呼叫；不一定是故障。
3. `D`：等不可中斷 I/O。看 disk.md 的 await、是不是 NFS／壞碟；不要急著 KILL。
4. `Z`：找父行程（pstree / PPid），不是殺 zombie。
5. `T`：誰送了 STOP，或是不是在被除錯。

**CPU**

1. 當下誰在吃：top / `pidstat -u` 的 `%CPU`。
2. 在跑還是在排：`%wait`、`nvcswch/s`。
3. 只能用一顆：`taskset -cp`、`nlwp=1`、psr 固定。

**記憶體**

1. 看 RSS / `%MEM`，不看 VSZ。
2. `majflt/s` 持續大於 0：在讀碟補頁，對照 memory.md 是否 available 吃緊、是否在 swap。

**檔案與上限**

1. `Too many open files`：`/proc/<PID>/limits` 的 Max open files，對 lsof 計數。
2. umount busy / 空間不釋放：`fuser -vm`、`lsof +L1`（disk.md）。

**卡住**

1. strace：最後一個未返回的 syscall。
2. ltrace：卡在函式庫層且很少進核心時。
3. 仍不明：`/proc/<PID>/stack`（D 狀態）或 perf（已確定 CPU bound）。

💡 一分鐘快速診斷

1. `ps -p <PID> -o pid,stat,ni,psr,nlwp,%cpu,rss,etime,cmd` 看狀態與資源。
2. `R`+高 CPU → pidstat / taskset；`D` → disk；`S`+無進度 → strace；`Z` → pstree 找父行程。
3. 需要殺時先 `kill -TERM`，確認 `/proc/<PID>` 消失再考慮 `-KILL`。

---

## 🛠 設計目的、資料來源和適用場景

- **ps**
  - 定位: 行程快照與腳本取數
  - 時間軸: 僅看當下
  - 資料來源: `/proc/<PID>/stat`、`status`、`cmdline`
  - 優點: 欄位可自選；適合一次列出狀態、nice、RSS、NLWP。
  - 缺點: `%CPU` 是啟動至今平均；沒有每秒曲線。

- **pstree**
  - 定位: 父子關係
  - 時間軸: 當下
  - 優點: 一眼看出服務樹與 zombie 的父行程。
  - 缺點: 不顯示資源用量。

- **top**
  - 定位: 互動式「誰在吃」
  - 時間軸: 即時刷新
  - 資料來源: `/proc` 與 `/proc/stat`
  - 優點: `%CPU` 是最近區間；可切執行緒、每顆 CPU。
  - 缺點: 不留歷史；整機欄位細節以 processor.md 為準。

- **pidstat**
  - 定位: 單一行程的 CPU / 記憶體缺頁 / I/O / 切換
  - 時間軸: 即時連續（可加間隔）
  - 資料來源: `/proc/<PID>/...`（sysstat）
  - 優點: `%wait`、majflt、nvcswch 能區分「在跑 / 在排 / 在等碟」。
  - 缺點: 要 sysstat；第一筆是開機平均；預設 `%CPU` 刻度是單核 100%。

- **/proc/\<PID\>/**
  - 定位: 該行程的核心原始資料
  - 時間軸: 當下
  - 優點: cmdline、limits、fd、io、stack 等工具沒一次列完的都能查。
  - 缺點: 要自己拼；行程一結束路徑就沒有。

- **lsof / fuser**
  - 定位: 檔案與埠被誰握住
  - 優點: lsof 明細全；fuser 對「這個路徑／掛載點」回答短。
  - 缺點: lsof 在 fd 極多時慢；fuser `-k` 危險。

- **ulimit / limits**
  - 定位: 資源上限
  - 優點: 解釋 EMFILE、無法 fork，而不是「機器壞了」。
  - 缺點: shell 的 ulimit ≠ 服務行程的 limits。

- **strace / ltrace**
  - 定位: 卡住時看卡在哪一層
  - 優點: 直接看到阻塞中的 syscall / 函式庫呼叫。
  - 缺點: 明顯拖慢；ltrace 對靜態連結幾乎無用。

- **nice、taskset、kill**
  - 定位: 排程參數與訊號（診斷為主，調校為輔）
  - 讀 NI、affinity、試 TERM 屬於診斷；改親和性與 KILL 要有意為之。

- 和另外三份的分工
  - 整機還有沒有算力、單顆是否打滿：processor.md。
  - 整機還有沒有 RAM、是否在 swap：memory.md。
  - 整機碟是否在排隊、空間是否滿：disk.md。
  - 對到 PID、狀態、fd、limits、訊號：本份。
