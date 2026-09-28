# Linux Processor 診斷備忘

Load average、`%iowait` 都很容易被單獨讀成「CPU 不夠」。判斷方式和記憶體一樣：先看真正代表「還有沒有算力」的欄位，再看有沒有人在排隊。

邏輯 CPU 數是所有數字的對照基準。`lscpu` 的 `CPU(s)`、`nproc`，或 sar 表頭的 `(4 CPU)` 都是這個數字。有超執行緒時，邏輯 CPU 多於實體核心；load 與 run queue 要跟邏輯 CPU 比，不是跟實體核心比。

---

## lscpu

lscpu 是確認「這台機器有幾顆邏輯 CPU、幾顆實體核心、有沒有超執行緒與 NUMA」最快的工具。讀 load 與 `%CPU` 之前先看這裡。

```bash
linux:~$ lscpu
Architecture:                            x86_64
CPU(s):                                  4
On-line CPU(s) list:                     0-3
Thread(s) per core:                      2
Core(s) per socket:                      2
Socket(s):                               1
NUMA node(s):                            1
NUMA node0 CPU(s):                       0-3
CPU max MHz:                             3600.0000
CPU min MHz:                             800.0000
```

- **CPU(s)**：
  - 邏輯 CPU 總數（含超執行緒）。
  - 💡 之後所有 load、`r`、`runq-sz`、單執行緒 `%CPU≈100` 的對照基準都是這個數字。
- **Thread(s) per core**：
  - 每個實體核心上的硬體執行緒數。`2` 代表有超執行緒（SMT / HT）。
- **Core(s) per socket**：
  - 每個實體插座上的實體核心數。
- **Socket(s)**：
  - 實體 CPU 插座數。
  - 實體核心總數 ≈ `Core(s) per socket × Socket(s)`。邏輯 CPU ≈ 實體核心 × `Thread(s) per core`。
- **NUMA node(s)** / **NUMA nodeN CPU(s)**：
  - NUMA 節點數，以及每個節點上的邏輯 CPU 清單。
  - 多節點時，跨節點存取記憶體會變慢；排程與親和性診斷才需要細看。
- **CPU max MHz / CPU min MHz**：
  - 頻率上下限。實際當下頻率要用 `cpupower` / `turbostat` 看，不是這兩個靜態欄位。

---

## /proc/cpuinfo

`/proc/cpuinfo` 是 lscpu 的原始資料來源之一。每個邏輯 CPU 一段；欄位比 lscpu 碎，適合核對 flags 或某一顆的編號。

```bash
linux:~$ grep -E '^(processor|physical id|core id|siblings|cpu cores|model name|flags)' /proc/cpuinfo | head -n 20
processor	: 0
model name	: Intel(R) Core(TM) i5
physical id	: 0
siblings	: 4
core id		: 0
cpu cores	: 2
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr ...
processor	: 1
model name	: Intel(R) Core(TM) i5
physical id	: 0
siblings	: 4
core id		: 1
cpu cores	: 2
```

- **processor**：
  - 邏輯 CPU 編號（0 起算）。對應 `mpstat` / `pidstat` 的 `CPU` 欄、以及 `taskset` 的 mask 位元。
- **physical id**：
  - 實體插座（socket）編號。
- **core id**：
  - 該插座內的實體核心編號。同一個 `physical id` + `core id` 出現兩次（兩個 `processor`），就是同一顆實體核心上的兩個超執行緒。
- **siblings**：
  - 同一個插座上的邏輯 CPU 數。
- **cpu cores**：
  - 同一個插座上的實體核心數。
- **flags**：
  - CPU 功能旗標。診斷效能時較常查 `avx`、`avx2`、`sse4_2` 等；日常負載判斷用不到。

⚠️ 不要用 `grep -c processor` 當「實體核心數」。那是邏輯 CPU 數。實體核心要看 `physical id` + `core id` 的唯一組合，或直接用 `lscpu`。

---

## dmidecode -t processor

dmidecode 從 SMBIOS / DMI 讀主機板記錄的處理器資訊。適合對規格書、序號、標稱時脈；不適合看當下使用率。

```bash
linux:~$ sudo dmidecode -t processor
# dmidecode 3.4
Getting SMBIOS data from sysfs.
SMBIOS 3.0.0 present.

Handle 0x0004, DMI type 4, 42 bytes
Processor Information
	Socket Designation: U3E1
	Type: Central Processor
	Family: Core i5
	Manufacturer: Intel(R) Corporation
	ID: A5 06 08 00 FF FB EB BF
	Signature: Type 0, Family 6, Model 142, Stepping 10
	Version: Intel(R) Core(TM) i5
	Voltage: 0.9 V
	External Clock: 100 MHz
	Max Speed: 3600 MHz
	Current Speed: 1800 MHz
	Status: Populated, Enabled
	Core Count: 2
	Core Enabled: 2
	Thread Count: 4
```

- **Version / Manufacturer**：
  - 主機板記錄的處理器型號與廠商字串。
- **Max Speed / Current Speed**：
  - DMI 裡的標稱最大速度與「當下」速度欄位。
  - ⚠️ `Current Speed` 常常是開機時寫死或粗略更新，**不能**當成 turbostat / cpupower 那種即時頻率。即時頻率改看後面硬體狀態章節。
- **Core Count / Core Enabled / Thread Count**：
  - 實體核心數、已啟用核心數、硬體執行緒總數。應與 `lscpu` 交叉核對。
- **Status**：
  - `Populated, Enabled` 代表這顆插座有裝且啟用。多插座機器若某一顆是 `Unpopulated`，邏輯 CPU 數會少一截。

需要 root。虛擬機或容器裡常沒有完整 DMI，輸出可能空白或與真實硬體不符。

---

## lstopo / hwloc-ls

lstopo（套件 hwloc；指令也可能叫 `hwloc-ls`）把 Socket → NUMA → Core → PU（邏輯 CPU）與快取層級畫成拓樸。用來確認「哪兩顆邏輯 CPU 其實是同一顆實體核心」。

```bash
linux:~$ lstopo-no-graphics --no-io
Machine (16GB total)
  Package L#0
    NUMANode L#0 (P#0 16GB)
      L3 (8192KB)
        L2 (256KB) + L1d (32KB) + L1i (32KB) + Core L#0
          PU L#0 (P#0)
          PU L#1 (P#1)
        L2 (256KB) + L1d (32KB) + L1i (32KB) + Core L#1
          PU L#2 (P#2)
          PU L#3 (P#3)
```

- **Package**：
  - 實體插座。
- **NUMANode**：
  - NUMA 節點與其本地記憶體。
- **Core / PU**：
  - `Core` 是實體核心；底下每個 `PU`（Processing Unit）是一顆邏輯 CPU，`P#N` 就是 Linux 的邏輯 CPU 編號。
  - 💡 同一個 Core 下有兩個 PU 時，把兩個高負載執行緒綁在這兩個 PU 上，等於搶同一顆實體核心的算力與 L1/L2。
- **L1 / L2 / L3**：
  - 快取層級與大小。跨 Package 或跨 NUMA 的執行緒共享 L3 的方式不同，先進診斷通常先確認拓樸，不必先鑽延遲數字。

無圖形環境用 `lstopo-no-graphics`。`hwloc-ls` 是同一套工具的別名輸出。

---

## uptime

uptime 是查看「當下負載」最快的工具。它給的是 load average，不是 CPU 使用率。

```bash
linux:~$ uptime
 01:40:05 up 12 days,  4:18,  1 user,  load average: 0.08, 0.12, 0.09
```

```bash
linux:~$ cat /proc/loadavg
0.08 0.12 0.09 1/612 4821
```

- **load average**（三個數字）：
  - 依序是 1 分鐘、5 分鐘、15 分鐘的負載。
  - 計入兩種任務：R（正在某個邏輯 CPU 上執行，或已經可執行、正在等 CPU）以及 D（不可中斷睡眠，多半在等磁碟或 NFS）。
  - 這是指數衰減的移動平均，不是「過去 60 秒的算術平均」。短脈衝會在 1 分鐘那個數字上停留一陣子。
  - ⚠️ 大於邏輯 CPU 數，只代表「可執行 + 卡在 I/O 的任務」偏多，不代表 CPU 算力用盡。
- **/proc/loadavg 第四欄**（`1/612` 這種寫法）：
  - 斜線左邊是此刻處於 R 的任務數（不含 D）。
  - 斜線右邊是系統上的任務總數。
  - 💡 左邊長期明顯大於邏輯 CPU 數，才比較像有人在等 CPU。load 本體含有 D，這個欄位不含。
- **第五欄**：
  - 最近一次建立的 PID，與負載無關。

---

## w

w 在 uptime 同一行之外，多列出目前登入中的使用者，以及每人最近在跑什麼。負載數字的意義與 uptime 相同。

```bash
linux:~$ w
 01:40:05 up 12 days,  4:18,  1 user,  load average: 0.08, 0.12, 0.09
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
kam      pts/0    10.0.0.8         01:10    0.00s  0.04s  0.00s w
```

- **表頭 load average**：
  - 與 uptime 完全相同，含 R 與 D，不能單獨當成 CPU 使用率。
- **JCPU**：
  - 這個 TTY 上所有行程累積用掉的 CPU 時間。
- **PCPU**：
  - 目前 `WHAT` 那個行程用掉的 CPU 時間。
- **WHAT**：
  - 該使用者目前前景指令。用來回答「誰登進來、在跑什麼」，不是整機瓶頸儀表。

---

## top

top 是互動式總覽：上方 `%Cpu(s)` 對應整機時間占比，下方行程表對應「誰在吃 CPU」。適合盯著看；不留歷史。

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

📊 `%Cpu(s)`（整機；與 mpstat `all` 同一組 `/proc/stat` 計數）

- **us**：
  - 使用者空間，不含 nice。對應 `%usr`。
- **sy**：
  - 核心空間。procps 的 top 通常**不含**硬體中斷與 softirq（那些在 `hi` / `si`）。
- **ni**：
  - nice 過的使用者時間。對應 `%nice`。
- **id**：
  - 💡 閒置。還高就不是算力用盡。對應 `%idle`。
- **wa**：
  - iowait。⚠️ 是閒置的一種，不是「CPU 很忙」。對應 `%iowait`。
- **hi / si**：
  - 硬體中斷 / softirq。對應 `%irq` / `%soft`。
- **st**：
  - steal。對應 `%steal`。

按 `1` 可切成每顆邏輯 CPU 一列，效果接近 `mpstat -P ALL`。

📊 行程列（CPU 相關）

- **%CPU**：
  - 預設是「單一邏輯 CPU = 100%」。打滿一顆約 100%，四顆滿載可到約 400%。
  - 與 pidstat 預設刻度相同，和上方 `%Cpu(s)` 的整機百分比不同。
- **TIME+**：
  - 累積 CPU 時間（分:秒.百分秒）。開機後一直偏高的行程，歷史上吃過很多 CPU。
- **ni**：
  - nice 值。數字越大優先權越低。
- **S**：
  - 狀態：`R` 可執行或正在跑，`S` 可中斷睡眠，`D` 不可中斷睡眠（多半等 I/O），`Z` zombie，`T` stopped。
- **P**：
  - 最後一次跑在哪一顆邏輯 CPU（預設欄位未必顯示；`f` 勾選 `P = Last used cpu`）。
  - 一直黏在同一顆、且 `1` 顯示只有那顆 idle 為 0 時，就是單執行緒或親和性把一顆打滿。

`-bn1` 只印一次後結束，方便貼進筆記；互動模式才適合持續盯。

---

## htop / btop / glances

這三個都是 top 的加強版畫面，欄位意義與 top / mpstat / pidstat 同源，不必再背第二套定義。差別在互動與資訊密度。

- **htop**：
  - 預設就畫出每顆邏輯 CPU 的長條，一眼看出「只有一顆紅、其餘空」。
  - 可展開執行緒樹、用滑鼠選行程、自訂欄位（含 `PROCESSOR`、`STATE`）。
  - 比 top 少按鍵、同樣不留歷史。
- **btop**：
  - 把 CPU、記憶體、磁碟、網路畫在同一畫面，適合「先分是 CPU 還是別的子系統」。
  - CPU 圖仍是使用率，不是 load；解讀方式與 `%idle` 相同。
- **glances**：
  - 偏監控面板：CPU、load、每顆邏輯 CPU、前幾名行程一次列出，也可當用戶端/伺服器蒐集。
  - 適合巡檢；細到單一欄位時，仍以 mpstat / pidstat / sar 為準。

💡 診斷結論仍看 `%idle`、`r`、行程 `%CPU`；這三者負責「看得舒服」，不取代 sar 的歷史。

---

## mpstat

mpstat 把每一顆邏輯 CPU 的時間拆開。整機平均會把「一顆打滿、其餘閒置」稀釋掉，所以判斷單執行緒瓶頸時要加 `-P ALL`。

```bash
linux:~$ mpstat -P ALL 1
Linux 7.0.0-14-generic (linux)      09/22/2026      _x86_64_        (4 CPU)

01:40:05 AM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
01:40:05 AM  all    0.42    0.00    0.18    0.03    0.00    0.01    0.00    0.00    0.00   99.36
01:40:06 AM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
01:40:06 AM  all    0.25    0.00    0.25    0.00    0.00    0.00    0.00    0.00    0.00   99.50
01:40:06 AM    0    1.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00   99.00
01:40:06 AM    1    0.00    0.00    1.00    0.00    0.00    0.00    0.00    0.00    0.00   99.00
01:40:06 AM    2    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00  100.00
01:40:06 AM    3    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00  100.00
```

⚠️ 帶間隔時，第一筆是開機到現在的平均。要看這一秒，從第二筆開始。

1. 程式與核心（時間真的花在執行指令）

- **%usr**：
  - 使用者空間（應用程式）所佔的 CPU 時間，不含 nice。
  - 偏高通常是程式自己在算。
- **%nice**：
  - 以 nice 調整過優先權的使用者空間時間。
  - 一般伺服器上這個值長期接近 0。批次工作被刻意降低優先權時才會出現。
- **%sys**：
  - 核心空間所佔的時間。不含硬體中斷與 softirq。
  - 偏高代表時間花在系統呼叫、排程、檔案系統等核心路徑，而不是應用程式的純計算。

2. 閒置與等待（看起來像忙，CPU 並沒有在算）

- **%idle**：
  - 💡 最重要的指標。CPU 閒置、而且沒有未完成磁碟 I/O 的時間比例。
  - 這個值還高，就不是算力用盡。
- **%iowait**：
  - CPU 閒置、同時系統有未完成磁碟 I/O 的時間比例。
  - ⚠️ CPU 這段時間沒有執行指令。它是閒置的一種，不是「CPU 很忙」。
  - 偏高只表示「有 CPU 空著，而且當時有磁碟 I/O」。不能當成磁碟延遲或 I/O 飽和的度量。
  - 反向也成立：CPU 一直在跑計算時，即使磁碟很慢，`%iowait` 也可以很低。
- **%steal**：
  - 虛擬 CPU 想執行、卻被 hypervisor 拿去服務其他虛擬機的時間。
  - 實體機通常是 0。虛擬機上持續偏高，代表宿主超賣或隔壁 VM 在搶 CPU，客人自己的 `%usr` 低不代表工作很快。

3. 中斷

- **%irq**：
  - 服務硬體中斷的時間。
- **%soft**：
  - 服務 softirq 的時間。網路收包、部分區塊 I/O 完成處理會落在這裡。
  - 封包速率很高時，這兩欄會起來；此時瓶頸可能在中斷處理，而不在應用程式的 `%usr`。

4. 客體時間（已包含在使用者時間裡）

- **%guest**：
  - 執行一般虛擬機客體的時間。
- **%gnice**：
  - 執行 nice 過的客體的時間。
  - ⚠️ `%usr + %nice + %sys + %iowait + %steal + %irq + %soft + %idle = 100`。`%guest` 已含在 `%usr`，`%gnice` 已含在 `%nice`，不要再加一次。

---

## pidstat

CPU 時間已經確認吃緊之後，用 pidstat 看是哪一個行程。`%CPU` 的刻度和 mpstat 不同。

```bash
linux:~$ pidstat -u -p 4821 1 2
Linux 7.0.0-14-generic (linux)      09/22/2026      _x86_64_        (4 CPU)

01:40:06 AM   UID       PID    %usr %system  %guest   %wait    %CPU   CPU  Command
01:40:07 AM  1000      4821   98.00    1.00    0.00    0.00   99.00     2  python3

01:40:07 AM   UID       PID    %usr %system  %guest   %wait    %CPU   CPU  Command
01:40:08 AM  1000      4821   60.00    1.00    0.00   35.00   61.00     1  python3
Average:      UID       PID    %usr %system  %guest   %wait    %CPU   CPU  Command
Average:     1000      4821   79.00    1.00    0.00   17.50   80.00     -  python3
```

⚠️ 帶間隔時，第一筆仍是開機至今。上面省略了第一筆。不指定 `-p` 時會列出所有行程，輸出很長。

- **%usr**：
  - 這個行程在使用者空間的 CPU 時間。
- **%system**：
  - 這個行程在核心空間的 CPU 時間。
- **%guest**：
  - 這個行程執行客體的時間。已含在 `%usr` 的計算裡。
- **%wait**：
  - 💡 行程已可執行、卻在等 CPU 的時間比例。
  - `%CPU` 不高但 `%wait` 持續偏高，代表它在排隊，CPU 被別人佔住。
- **%CPU**：
  - `%usr + %system`（客體時間不重複加總）。
  - ⚠️ 預設是「單一邏輯 CPU 為 100%」。打滿一顆核心約 100%，打滿 4 顆可以到約 400%。不是整機的百分比。
  - 要改成整機百分比（滿載約 100%）才加 `-I`。
- **CPU**：
  - 這個取樣區間最後一次跑在哪一顆邏輯 CPU。`Average` 那一列是 `-`。
  - 執行緒一直黏在同一顆、而 `mpstat -P ALL` 顯示只有那一顆 `%idle` 為 0 時，就是單執行緒（或親和性）把一顆核心打滿。

`pidstat -t` 拆到執行緒。`pidstat -w` 的 `nvcswch/s`（非自願上下文切換）持續很高時，行程是被排程器搶佔下來的，和 `%wait` 一起看。

---

## ps

ps 做一次性快照，適合腳本與「列出 CPU 相關欄位」。不是連續監控。

```bash
linux:~$ ps -eo pid,user,%cpu,cputime,stat,psr,nlwp,comm --sort=-%cpu | head
    PID USER     %CPU     TIME STAT PSR NLWP COMMAND
   4821 kam      99.0 00:12:34 Rl    2    1 python3
    812 root      0.3 00:45:01 Ss    0    1 systemd
   1204 kam       0.1 00:01:02 Sl    1   12 firefox
```

- **%CPU**：
  - 行程啟動至今的平均 CPU 使用率（單一邏輯 CPU = 100% 的刻度）。
  - ⚠️ 與 top / pidstat「最近一個取樣區間」不同；開很久但早就閒下來的行程，`%CPU` 仍可能被早期尖峰拉高。要看當下請改 top / pidstat。
- **cputime**（`TIME`）：
  - 累積 CPU 時間。對應 top 的 `TIME+`（精準度較粗）。
- **stat**：
  - 狀態字串。第一個字母最重要：
  - `R`：可執行或正在跑。
  - `S`：可中斷睡眠。
  - `D`：不可中斷睡眠（多半等 I/O）。load 會把 D 算進去。
  - 後面常接修飾字元（BSD / GNU 都常見）：`l` 多執行緒、`s` session leader、`+` 前景行程群組、`<` 高優先權、`N` 低 nice。
- **psr**：
  - 目前（或最後）跑在哪一顆邏輯 CPU。對應 top 的 `P`、pidstat 的 `CPU`。
- **nlwp**：
  - 這個行程的執行緒（LWP）數。`1` 是單執行緒；很大時要再查是不是執行緒把多顆邏輯 CPU 打滿。

`ps aux` 是 BSD 風格、`ps -ef` 是 UNIX/GNU 風格；狀態字母 `R/S/D` 含義相同，修飾字元集合略有差異。看 CPU 時用 `-o` 自選欄位最清楚。

---

## taskset

taskset 讀（或設定）行程的 CPU 親和性：允許跑在哪些邏輯 CPU 上。診斷時先**讀**，確認是不是被綁死在少數幾顆。

```bash
linux:~$ taskset -cp 4821
pid 4821's current affinity list: 0-3
```

```bash
linux:~$ taskset -cp 4821
pid 4821's current affinity list: 2
```

- **-cp**：
  - `-c` 用邏輯 CPU 清單（如 `0-3`、`2`）顯示；`-p` 指定 PID。
  - 第一例 `0-3`：四顆都能跑，親和性不是瓶頸。
  - 第二例只有 `2`：再怎麼多核，這個行程也只能用一顆邏輯 CPU。此時 `mpstat -P ALL` 常會看到只有 CPU 2 的 `%idle` 接近 0。
- **affinity list / mask**：
  - 清單是人類可讀的邏輯 CPU 集合；不加 `-c` 時印的是十六進位 mask，位元對應 `processor` 編號。

⚠️ 本節只用來**確認**現況。亂改親和性可能讓負載更擠在同一顆實體核心；調校不在這份診斷備忘範圍。

---

## sar

sar 用同一組 CPU 欄位留下歷史，用來事後對照「當時慢，是不是 CPU」。即時欄位意義與 mpstat 相同；這裡多了佇列。

```bash
linux:~$ sar -u ALL
Linux 7.0.0-14-generic (linux)      09/22/2026      _x86_64_        (4 CPU)

01:00:05 AM     CPU      %usr     %nice      %sys   %iowait    %steal      %irq     %soft    %guest    %gnice     %idle
01:10:05 AM     all      0.15      0.00      0.12      0.02      0.00      0.00      0.01      0.00      0.00     99.70
01:20:05 AM     all      0.18      0.00      0.11      0.01      0.00      0.00      0.01      0.00      0.00     99.69
01:30:05 AM     all      1.42      0.00      0.55      0.20      0.00      0.00      0.02      0.00      0.00     97.81
01:40:05 AM     all      0.21      0.00      0.14      0.02      0.00      0.00      0.01      0.00      0.00     99.62
Average:        all      0.49      0.00      0.23      0.06      0.00      0.00      0.01      0.00      0.00     99.21
```

欄位與 mpstat 相同（sar 寫 `%usr` / `%sys`，有的版本寫 `%user` / `%system`，計數來源都是 `/proc/stat`）。`%guest`、`%gnice` 已分別含在 `%usr`、`%nice`。

`-u` 不加 `ALL` 時，預設不顯示 `%irq`、`%soft`、`%guest`、`%gnice`。要看中斷與客體時間就加 `ALL`。

```bash
linux:~$ sar -q
Linux 7.0.0-14-generic (linux)      09/22/2026      _x86_64_        (4 CPU)

01:00:05 AM   runq-sz  plist-sz   ldavg-1   ldavg-5  ldavg-15   blocked
01:10:05 AM         1       612      0.08      0.12      0.09         0
01:20:05 AM         1       614      0.10      0.11      0.09         0
01:30:05 AM         2       640      0.85      0.40      0.22         0
01:40:05 AM         1       618      0.21      0.28      0.18         0
Average:            1       621      0.31      0.23      0.15         0
```

- **runq-sz**：
  - 收集區間內，處於 R 的任務數平均（`/proc/stat` 的 `procs_running`），含正在執行的與正在等 CPU 的。
  - 和 vmstat 的 `r` 是同一類數字；vmstat 是取樣瞬間，這裡是區間平均。
  - 💡 長期明顯大於邏輯 CPU 數，才代表 run queue 堆積。
- **plist-sz**：
  - 任務清單上的任務總數。負載判斷用不到，只說明當時系統有多少任務。
- **ldavg-1 / ldavg-5 / ldavg-15**：
  - 與 uptime 的三個 load average 相同，差別是留下歷史。
  - 同樣含 R 與 D，不能單獨當成 CPU 使用率。
- **blocked**：
  - 處於 D 的任務數（`procs_blocked`），對應 vmstat 的 `b`。
  - `ldavg` 高、`runq-sz` 不高、`blocked` 高：負載來自 I/O 等待。

`sar -u` 預設是整機 `all`。事後要確認是不是只有一顆邏輯 CPU 打滿，用 `sar -P ALL`。

---

## /proc/stat

`/proc/stat` 是 mpstat、sar `-u`、top `%Cpu(s)`、vmstat cpu 欄的共同來源。讀原始計數時，欄位是**開機以來累積的 jiffies**，要自己做兩次取樣相減才有「這一段的百分比」。

```bash
linux:~$ grep -E '^(cpu|procs_)' /proc/stat
cpu  470384 12 210556 89234120 18234 0 4521 0 0 0
cpu0 120100 3 54020 22308000 4500 0 1200 0 0 0
cpu1 118200 3 52010 22309000 4600 0 1100 0 0 0
cpu2 116000 3 52200 22308500 4550 0 1110 0 0 0
cpu3 116084 3 52326 22308620 4584 0 1111 0 0 0
procs_running 1
procs_blocked 0
```

`cpu` / `cpuN` 各欄依序（單位：jiffies）：

- **user**：
  - 使用者空間。⚠️ **含 guest**（執行虛擬機客體的時間已算在這欄裡）。
- **nice**：
  - nice > 0 的使用者空間。含 guest_nice。
- **system**：
  - 核心空間。不含 irq / softirq。
- **idle**：
  - 閒置且無未完成磁碟 I/O。
- **iowait**：
  - 閒置且有未完成磁碟 I/O。仍是閒置的一種。
- **irq**：
  - 硬體中斷。
- **softirq**：
  - softirq。
- **steal**：
  - 被 hypervisor 偷走的時間。
- **guest**：
  - 客體時間。已含在 **user**，列出來是為了拆開看。
- **guest_nice**：
  - nice 過的客體時間。已含在 **nice**。

- **procs_running**：
  - 此刻處於 R 的任務數（含正在跑的）。對應 vmstat `r`、sar `runq-sz`。
- **procs_blocked**：
  - 此刻處於 D 的任務數。對應 vmstat `b`、sar `blocked`。

💡 實務上優先用 mpstat / sar 讀百分比；直接 cat `/proc/stat` 是為了核對來源或寫腳本。不要把單次累積值當成「現在的使用率」。

---

## /proc/interrupts

`/proc/interrupts` 列出每種硬體中斷在各邏輯 CPU 上的累積次數。`%irq` 偏高、或某一顆 CPU 特別忙時，用來查是不是中斷集中在少數邏輯 CPU。

```bash
linux:~$ head -n 5 /proc/interrupts
           CPU0       CPU1       CPU2       CPU3
  0:         42          0          0          0  IR-IO-APIC   2-edge      timer
  1:          9          0          0          0  IR-IO-APIC   1-edge      i8042
  8:          1          0          0          0  IR-IO-APIC   8-edge      rtc0
  9:          0          0          0          0  IR-IO-APIC   9-fasteoi   acpi
```

```bash
linux:~$ grep -E 'enp|eth|nvme|CPU' /proc/interrupts | head
           CPU0       CPU1       CPU2       CPU3
 29:          0   12004521          0          0  IR-PCI-MSI 2097152-edge      enp0s31f6
 30:     884412          0          0          0  IR-PCI-MSI 512000-edge       nvme0q0
```

- **欄位 CPU0..CPUn**：
  - 該 IRQ 在這顆邏輯 CPU 上累積處理的次數。
- **最後一欄裝置名**：
  - 如網卡、NVMe、計時器。網路 IRQ 長期幾乎落在同一顆時，那顆的 `%soft` / `%irq` 容易偏高，應用程式卻不一定在 `%usr` 打滿。
- **讀法**：
  - 這是累積計數。要看速率，隔幾秒再 cat 一次做差，或用 `watch -n1 'grep enp /proc/interrupts'`。

與 `mpstat` 的 `%irq` 對照：百分比說「花了多少 CPU 時間」，這裡說「次數落在哪一顆」。

---

## /proc/softirqs

`/proc/softirqs` 是 softirq 種類在各邏輯 CPU 上的累積次數。`%soft` 偏高時用來分辨是網路、區塊裝置還是計時器。

```bash
linux:~$ cat /proc/softirqs
                    CPU0       CPU1       CPU2       CPU3
          HI:          1          0          0          0
       TIMER:    4200120    4188901    4191200    4189950
      NET_TX:       1204        980       1102       1050
      NET_RX:     880412   12500421     900200     910100
       BLOCK:      12040      11800      11950      12100
    TASKLET:        320        280        300        290
      SCHED:    2100450    2098800    2101200    2099900
    RCU:        1800200    1798800    1800500    1799000
```

- **NET_RX / NET_TX**：
  - 網路收／送封包的 softirq。💡 `NET_RX` 在某一顆特別大，常與 `/proc/interrupts` 裡網卡 IRQ 集中在同一顆一起出現。
- **BLOCK**：
  - 區塊 I/O 完成路徑相關的 softirq。
- **TIMER / SCHED / RCU**：
  - 計時器、排程、RCU。正常負載下各 CPU 大致接近；診斷網路或磁碟尖峰時優先看 `NET_*` 與 `BLOCK`。
- **HI / TASKLET**：
  - 高優先 softirq 與 tasklet。一般伺服器上數字相對小。

同樣是累積值；與 `%soft` 搭配：百分比看時間，這裡看種類與分布。

---

## sensors

sensors（lm-sensors）讀溫度、風扇等硬體感測。使用率不高但機器突然降速時，用來確認是不是過熱降頻。

```bash
linux:~$ sensors
coretemp-isa-0000
Adapter: ISA adapter
Package id 0:  +48.0°C  (high = +80.0°C, crit = +100.0°C)
Core 0:        +46.0°C  (high = +80.0°C, crit = +100.0°C)
Core 1:        +47.0°C  (high = +80.0°C, crit = +100.0°C)

acpitz-acpi-0
Adapter: ACPI interface
temp1:        +47.0°C
```

- **Package id / Core N**：
  - 整顆封裝與各實體核心溫度。接近 `high` / `crit` 時，CPU 可能開始 thermal throttling，頻率被壓低。
- **high / crit**：
  - 警告與臨界閾值。持續貼著 crit 比偶爾尖峰更值得查散熱。

虛擬機裡常常沒有真實 coretemp。需先 `sensors-detect`（發行版套件 lm-sensors）才有完整感測器。溫度 alone 不能證明瓶頸，要和 `Bzy_MHz` / `cpupower` 頻率一起看。

---

## cpupower

cpupower 讀電源管理與頻率策略。使用率有空間、體感卻慢時，確認當下是不是跑在很低的頻率。

```bash
linux:~$ cpupower frequency-info
analyzing CPU 0:
  driver: intel_pstate
  CPUs which run at the same hardware frequency: 0
  CPUs which need to have their frequency coordinated by software: 0
  maximum transition latency:  Cannot determine or is not constant.
  hardware limits: 800 MHz - 3.60 GHz
  available cpufreq governors: performance powersave
  current policy: frequency should be within 800 MHz and 3.60 GHz.
                  The governor "powersave" may decide which speed to use
                  within this range.
  current CPU frequency: Unable to call hardware
  boost state support: Supported
    Active: yes
```

- **hardware limits**：
  - 硬體允許的最低／最高頻率。對應 lscpu 的 min/max MHz。
- **available cpufreq governors / current policy**：
  - 可用與目前的調節器（如 `performance`、`powersave`）。
  - `powersave` 不代表永遠低頻，但在輕載時較積極降頻；查「為什麼沒衝到 max」時要看這個。
- **current CPU frequency**：
  - 有些驅動（尤其 intel_pstate）會顯示 `Unable to call hardware`。此時改看 `turbostat` 的 `Bzy_MHz`，或 `cat /proc/cpuinfo | grep MHz`、sysfs 的 `scaling_cur_freq`。
- **boost**：
  - Turbo / boost 是否啟用。關掉時頻率上不去標稱 max 以上。

本節只讀 `frequency-info`。改 governor 屬於調校，不在診斷備忘展開。

---

## turbostat

turbostat（linux-tools / kernel tools）按間隔列出每顆核心的忙碌比例、實際工作頻率與溫度。適合回答「使用率看起來不高，是不是降頻了」。

```bash
linux:~$ sudo turbostat --quiet --Interval 1 --show Busy%,Bzy_MHz,TSC_MHz,CPU%c1,CPU%c6,CoreTmp
Busy%   Bzy_MHz TSC_MHz CPU%c1  CPU%c6  CoreTmp
0.42    1202    2592    42.10   55.30   47
0.38    1105    2592    40.00   58.20   46
```

（未加 `--show` 時欄位更多，含每 Package/Core/CPU 列、IPC、IRQ、各 C-state 等；版本不同欄名略有差異。上表是診斷最常盯的子集。）

- **Busy%**：
  - 不在 C-state 休眠、實際在跑的時間比例。概念上接近 `100 - %idle` 一類的「有在做事」，但來自硬體計數，和 `/proc/stat` 不是同一條公式。
- **Bzy_MHz**：
  - 💡 忙碌期間的平均實際頻率（MHz）。這才是「現在跑多快」。
  - 遠低於 `TSC_MHz` / lscpu max，且 `Busy%` 不低時，可能是電源策略或過熱降頻。
- **TSC_MHz**：
  - TSC 標稱頻率，接近基底時脈，用來對照 `Bzy_MHz` 有沒有拉滿。
- **CPU%c1 / CPU%c6**（以及同系列的 `CPU%c3` 等）：
  - 待在該 C-state 的時間比例。數字高代表核心常休眠；輕載時正常。Busy 應高卻卡在深 C-state、同時 `Bzy_MHz` 上不去，才值得懷疑電源或平台限制。
- **CoreTmp**：
  - 核心溫度（°C）。與 `sensors` 交叉看；貼近熱限制時 `Bzy_MHz` 常被壓下。

需要 root（或對應的 MSR 權限）。虛擬機裡經常不可用或數字無意義。第一列有時是摘要；看趨勢用連續幾行 Interval。

---

## vmstat

vmstat 同時看「有沒有人在等 CPU」和「CPU 時間怎麼分」。記憶體與 swap 欄位見 [memory.md](memory.md)；這裡只讀 procs、system、cpu。

```bash
linux:~$ vmstat 1
procs -----------memory---------- ---swap-- -----io---- -system-- -------cpu-------
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st gu
 1  0      0  23345      4  22564    0    0    22   336  386    0  0  0 99  0  0  0
 0  0      0  23340      4  22564    0    0     0     4  420  610  0  0 99  0  0  0
```

⚠️ 第一列是開機至今的平均。從第二列開始才是這個間隔。

📊 procs（有沒有人在排隊）

- **r**：
  - 取樣當下處於 R 的任務數，含正在邏輯 CPU 上執行的，以及可執行但還在等 CPU 的。
  - 💡 長期大於邏輯 CPU 數，代表有任務排在 run queue 裡。等於邏輯 CPU 數只代表核心都有事做，還沒有人在等。
- **b**：
  - 處於 D（不可中斷睡眠）的任務數，多半在等 I/O。
  - load average 會把這些任務算進去。`b` 高、`r` 不高時，load 上升來自 I/O，不是 CPU。

📊 system（切換有多頻繁）

- **in**：
  - 每秒中斷次數。
- **cs**：
  - 每秒上下文切換次數。
  - `sy` 同時偏高、`cs` 非常高時，時間可能花在來回切換與系統呼叫，而不只是純計算。

📊 cpu（時間百分比；`us sy id wa st` 合計約 100）

- **us**：
  - 使用者空間，含 nice。對應 mpstat 的 `%usr + %nice`。
- **sy**：
  - 核心空間，而且含硬體中斷與 softirq。
  - ⚠️ mpstat / sar 的 `%sys` 不含 `%irq` 與 `%soft`。vmstat 的 `sy` 偏高時，可能是系統呼叫，也可能是中斷，要改看 mpstat 才能拆開。
- **id**：
  - 閒置，且沒有未完成的磁碟 I/O。對應 `%idle`。
- **wa**：
  - iowait。對應 `%iowait`，同樣是閒置的一種，不是 CPU 忙碌。
- **st**：
  - steal。對應 `%steal`。
- **gu**：
  - 客體執行時間，含 guest nice。
  - 已包含在 `us` 裡，不要和 `us` 相加。

---

## perf

perf 在已經確認 CPU bound 之後，用來做高階計數概覽（`perf stat`）。本節只記總覽欄位，不展開錄製、火焰圖或調校步驟。

```bash
linux:~$ perf stat -a sleep 5

 Performance counter stats for 'system wide':

       20000.12 msec cpu-clock                 #    4.000 CPUs utilized
          12840      context-switches          #    0.642 K/sec
            312      cpu-migrations            #    0.016 K/sec
           1450      page-faults               #    0.072 K/sec
    42180000000      cycles                    #    2.109 GHz
    31800000000      instructions              #    0.75  insn per cycle
        5200000      branches
          48000      branch-misses             #    0.92% of all branches

       5.000812345 seconds time elapsed
```

- **task-clock / cpu-clock**：
  - 計入的 CPU 時間。`CPUs utilized` 接近邏輯 CPU 數時，代表取樣期間幾乎打滿所有邏輯 CPU。
- **cycles**：
  - CPU cycle 數。除以時間可粗估平均頻率。
- **instructions**：
  - 退休（retired）指令數。
- **insn per cycle（IPC）**：
  - 💡 `instructions / cycles`。明顯偏低（遠低於該工作負載的常態）時，可能卡在記憶體延遲、快取未命中或管線停頓，而不只是「還有 idle」。
- **context-switches**：
  - 上下文切換次數。與 vmstat `cs` 同一類現象；極高時時間花在排程上。

⚠️ `perf stat` 回答「這幾秒硬體計數長什麼樣」；它不取代先看 `%idle` 與 `r` 的第一輪判斷。需要 root 或 `perf_event_paranoid` 允許。這裡只作診斷備忘，不涉及任何攻擊或利用程序。

---

## 🔍 判斷 CPU 是否真的是瓶頸

**規格先對齊**

1. `lscpu` / `/proc/cpuinfo`：確認邏輯 CPU 數、有無超執行緒、NUMA。
2. `lstopo`：確認哪幾個 `PU` 共用同一顆實體核心，避免把「兩條超執行緒」當成兩顆完整核心。
3. `dmidecode -t processor`：只核對主機板記錄的核心／執行緒數與標稱速度，不拿 `Current Speed` 當即時頻率。

**uptime / w**

1. 負載輕：三個 load 都明顯小於邏輯 CPU 數。
2. 還不能下結論：load 大於邏輯 CPU 數。可能是 CPU 排隊，也可能是大量 D 狀態。必須接著看 `%idle`、`r`、`b`。
3. `w` 多看一眼 `WHAT`：確認有沒有互動使用者在跑重活。

**top / htop / btop / glances**

1. 先看 `%Cpu(s)` 的 `id`（或 htop 每顆長條）：還高就不是整機算力用盡。
2. 再看行程 `%CPU`、`S`、`P`：誰在 `R`、是否黏在同一顆邏輯 CPU。
3. htop / btop 適合當場確認「只有一顆紅」；要留紀錄仍用 sar。

**mpstat**

1. 算力還夠：`all` 的 `%idle` 仍高。
2. CPU 飽和：`%idle` 長期接近 0，而且 `%usr` 或 `%sys` 接走了幾乎全部時間。
3. 不是 CPU：`%iowait` 高、`%idle` 也還在。CPU 在等 I/O，沒有在算。改查磁碟。
4. 單顆打滿：`-P ALL` 裡只有一顆 `%idle` 接近 0，其餘仍閒。整機 `all` 仍可能顯示約 75% idle（4 顆時）。這個行程已經到單執行緒上限。
5. 虛擬化：`%steal` 持續數個百分點以上，客人裡的使用率會低估「想跑卻跑不到」的時間。

**vmstat**

1. 健康：`r` 不長期超過邏輯 CPU 數，`id` 高，`b` 與 `wa` 接近 0。
2. CPU 排隊：`r` 持續大於邏輯 CPU 數，同時 `id` 接近 0。
3. I/O 被算進 load：`b` 與 `wa` 高，`r` 不大，`id` 仍高。對照 uptime 會看到 load 上升，但 CPU 不是瓶頸。

**sar**

1. 事後先看 `sar -u ALL` 的 `%idle`。當時若仍高，變慢不是因為算力用盡。
2. 再看 `sar -q`：`runq-sz` 長期大於邏輯 CPU 數，才是 run queue 堆積；`blocked` 高而 `runq-sz` 不高，是 D 狀態把 `ldavg` 墊高。
3. `sar -u` 的 `all` 看起來還有 idle、但使用者記得某支程式已經跑滿時，改查 `sar -P ALL`，確認是不是單顆邏輯 CPU。

**pidstat / ps / taskset**

1. pidstat：找到 `%CPU` 長期接近 100 的整數倍（一顆核心約 100）的行程；幾個行程 `%wait` 都高則是互搶。
2. ps：腳本列出 `%cpu`、`stat`、`psr`、`nlwp`；注意 `%CPU` 是啟動至今平均。
3. taskset `-cp`：親和性若只剩一顆邏輯 CPU，單執行緒打滿是預期行為，不是「系統只有一核」。

**/proc/stat · interrupts · softirqs**

1. `/proc/stat` 核對 `procs_running` / `procs_blocked`；百分比交給 mpstat。
2. `%irq` / `%soft` 偏高：用 `/proc/interrupts` 與 `/proc/softirqs` 看次數落在哪顆、是不是 `NET_RX`。

**sensors / cpupower / turbostat**

1. `%idle` 還在、但工作偏慢：看 `Bzy_MHz` 是否遠低於上限、`CoreTmp` / `sensors` 是否貼近熱限、governor 是否把頻率壓住。
2. 這三個回答「跑得慢是不是頻率問題」，不回答「有沒有人在等 CPU」。

**perf**

1. 已確認 CPU bound 後，用 `perf stat` 看 IPC、cycles、context-switches。
2. 不取代 `%idle` 與 `r` 的第一輪。

💡 一分鐘快速診斷

1. `lscpu` 確認邏輯 CPU 數。
2. 先看 `%idle`（top / mpstat / `sar -u`）：還很大，就不是 CPU 算力用盡。
3. 再看 `r` 或 `runq-sz`：長期大於邏輯 CPU 數，才有人在等 CPU。
4. load 高但 `%idle` 也高：看 `b` / `blocked` / `%iowait`，多半是 I/O。
5. 整機還有 idle、體感卻慢：`mpstat -P ALL` 或 htop 看是不是只打滿一顆；虛擬機再加看 `%steal`；頻率再看 turbostat / sensors。

---

## 🛠 設計目的、資料來源和適用場景

- **lscpu**
  - 定位: 邏輯／實體拓樸快照
  - 時間軸: 靜態（硬體不變就不變）
  - 資料來源: sysfs、`/proc/cpuinfo`
  - 優點: 一眼給出診斷用的邏輯 CPU 數與超執行緒。
  - 缺點: 不反映當下負載。

- **/proc/cpuinfo**
  - 定位: 每顆邏輯 CPU 的原始屬性
  - 時間軸: 靜態
  - 優點: 可核對 `core id`、flags。
  - 缺點: 輸出長，日常優先用 lscpu。

- **dmidecode -t processor**
  - 定位: SMBIOS 規格與資產資訊
  - 時間軸: 靜態（主機板記錄）
  - 優點: Core/Thread Count、型號字串可對庫存。
  - 缺點: 要 root；`Current Speed` 不可靠；虛擬機常缺資料。

- **lstopo / hwloc-ls**
  - 定位: 快取與 PU 拓樸圖
  - 時間軸: 靜態
  - 優點: 看清哪些邏輯 CPU 共享同一顆實體核心與 L1/L2。
  - 缺點: 要另裝 hwloc；不顯示使用率。

- **uptime**
  - 定位: 即時負載快照
  - 時間軸: 僅看當下（1 / 5 / 15 分鐘的衰減平均）
  - 資料來源: `/proc/loadavg`
  - 優點: 任何系統都有，一個數字就能和邏輯 CPU 數比。
  - 缺點: 含 D 狀態，沒有 `%idle`，無法區分「等 CPU」和「等 I/O」。也沒有每顆 CPU 的拆分。

- **w**
  - 定位: 負載 + 誰登入在跑什麼
  - 時間軸: 當下
  - 資料來源: `/proc/loadavg`、utmp、各使用者行程
  - 優點: 比 uptime 多使用者與 `WHAT`。
  - 缺點: 負載解讀限制與 uptime 相同。

- **top**
  - 定位: 互動式整機 + 行程總覽
  - 時間軸: 即時畫面（可 `-bn1` 單次）
  - 資料來源: `/proc/stat`、`/proc/<pid>/stat`
  - 優點: `%Cpu(s)` 與行程 `%CPU` 同屏；按 `1` 可看每顆邏輯 CPU。
  - 缺點: 不留歷史；`%CPU` 刻度是單顆 100%。

- **htop / btop / glances**
  - 定位: 強化互動／儀表板
  - 時間軸: 即時畫面
  - 優點: 每顆 CPU 長條、多資源同屏，適合當場分流。
  - 缺點: 要另裝；欄位定義仍回到 top/mpstat，且通常不取代 sar 歷史。

- **mpstat**
  - 定位: 即時、按邏輯 CPU 拆開的時間占比
  - 時間軸: 即時連續監控（如每秒一筆）
  - 資料來源: `/proc/stat`（sysstat）
  - 優點: `%idle`、`%iowait`、`%steal`、`%irq`、`%soft` 一次分開，專門對付「平均看起來還好」。
  - 缺點: 不告訴你是哪個行程。預設第一筆是開機至今，容易把現在的尖峰平均掉。

- **pidstat**
  - 定位: 哪一個行程（或執行緒）吃掉 CPU、誰在等
  - 時間軸: 即時連續監控
  - 資料來源: `/proc/<pid>/stat`（sysstat）
  - 優點: `%wait` 直接表示這個行程在等 CPU。`-t`、`-w` 可以再看到執行緒與非自願切換。
  - 缺點: `%CPU` 預設以單顆邏輯 CPU 為 100%，和 mpstat 的整機百分比不是同一刻度。

- **ps**
  - 定位: 行程欄位快照／腳本
  - 時間軸: 單次
  - 資料來源: `/proc/<pid>/stat` 等
  - 優點: `%cpu`、`stat`、`psr`、`nlwp` 可組成報表。
  - 缺點: `%CPU` 是啟動至今平均，不是「這一秒」。

- **taskset**
  - 定位: 讀 CPU 親和性
  - 時間軸: 當下設定
  - 優點: `-cp` 立刻看出是否被綁在少數邏輯 CPU。
  - 缺點: 不顯示使用率；本備忘只讀不調校。

- **sar**
  - 定位: 歷史紀錄與長期趨勢
  - 時間軸: 當天或過去特定日期（`sa` 檔，通常 10 分鐘一筆）
  - 資料來源: sadc 週期寫入的 `/var/log/sysstat` 或 `/var/log/sa/saDD`，內容仍來自 `/proc/stat` 與 run queue 計數
  - 優點: 事後能把 `%idle`、`runq-sz`、`blocked`、`ldavg` 對在同一段時間。`sar -P ALL` 補上每顆邏輯 CPU。
  - 缺點: 要事先安裝並啟用 sysstat。收集間隔預設 10 分鐘，短脈衝可能被平均掉。

- **/proc/stat**
  - 定位: CPU 時間與佇列的核心原始計數
  - 時間軸: 累積 jiffies；需兩次取樣才有區間
  - 優點: 所有使用率工具的共同來源；`procs_running` / `procs_blocked` 可直接讀。
  - 缺點: 手算百分比麻煩；`user` 已含 `guest`。

- **/proc/interrupts** · **/proc/softirqs**
  - 定位: 中斷／softirq 次數分布
  - 時間軸: 累積計數
  - 優點: 解釋 `%irq` / `%soft` 為何集中在某顆邏輯 CPU、是不是 `NET_RX`。
  - 缺點: 要自己算速率；不是使用率百分比。

- **sensors**
  - 定位: 溫度等感測
  - 時間軸: 當下
  - 優點: 查過熱降頻。
  - 缺點: 虛擬機常無資料；需 lm-sensors。

- **cpupower frequency-info**
  - 定位: 頻率範圍與 governor
  - 時間軸: 當下策略
  - 優點: 看硬體上下限與 powersave/performance。
  - 缺點: 有些驅動讀不到 current frequency。

- **turbostat**
  - 定位: 忙碌比例、實際 MHz、C-state、核心溫度
  - 時間軸: 即時連續（Interval）
  - 優點: `Bzy_MHz` + `Busy%` + `CoreTmp` 一次看清是否降頻。
  - 缺點: 常要 root；VM 上不可靠。

- **vmstat**
  - 定位: 佇列長度與 CPU、I/O 的對照
  - 時間軸: 即時連續監控
  - 資料來源: `/proc/stat`、`/proc/loadavg` 一類的核心計數；記憶體欄位另見 memory.md
  - 優點: `r` 與 `b` 放在 `us/sy/id/wa` 旁邊，最適合回答「load 高到底是 CPU 還是 I/O」。
  - 缺點: `sy` 含中斷，沒有 per-CPU，也沒有行程。`us sy id wa st` 才合計約 100，`gu` 是 `us` 的子集。

- **perf stat**
  - 定位: 已確認 CPU bound 後的硬體計數概覽
  - 時間軸: 指定取樣區間
  - 優點: IPC、cycles、context-switches 一眼可看。
  - 缺點: 不取代第一輪 `%idle`/`r`；權限與環境要求較高。

- 怎麼讀才不會誤判
  - 對應記憶體那份的 `available`：CPU 這邊先看 `%idle`，再看 `r` / `runq-sz` 有沒有大於邏輯 CPU 數。
  - load average 對應 `free` 的 `free` 欄位：數字最顯眼，單獨看最容易下錯結論。
  - `%iowait` / `wa` 不是 CPU 忙碌，也不是磁碟飽和的直接讀數。它只表示有 CPU 空著，而且當時有未完成的磁碟 I/O。
  - 行程 `%CPU`（top / pidstat / ps）預設以單顆邏輯 CPU 為 100%；整機百分比看 `%Cpu(s)` / mpstat `all`。
