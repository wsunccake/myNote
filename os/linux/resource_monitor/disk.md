# Linux Disk 診斷備忘

`df` 的 Use% 與 `iostat` 的 `%util` 都很容易被讀成「磁碟不行」。容量滿和裝置忙是兩件事：寫不進檔案先看空間與 inode；變慢先看延遲與佇列。髒頁寫不回去時，對照 [memory.md](memory.md) 的 **kbdirty** / **Dirty**。

---

## df

df 是查看「檔案系統還剩多少空間」最快的工具。它看的是容量，不是磁碟忙不忙。

```bash
linux:~$ df -hT
Filesystem     Type  Size  Used Avail Use% Mounted on
/dev/nvme0n1p2 ext4  468G   82G  362G  19% /
```

```bash
linux:~$ df -ih
Filesystem     Inodes IUsed IFree IUse% Mounted on
/dev/nvme0n1p2    30M  480K   29M    2% /
```

- **Filesystem**：
  - 檔案系統所在的區塊裝置（或 tmpfs、overlay 等虛擬來源）。
- **Type**：
  - 檔案系統類型。`df -T` 才會出現。
- **Size**：
  - 檔案系統總容量。
- **Used**：
  - 已配置給檔案與中繼資料的區塊。
- **Avail**：
  - 非 root 還能用的空間。
  - ext 系列預設保留約 5% 給 root，所以 Used + Avail 會小於 Size。
- **Use%**：
  - 💡 容量是否用盡，看這個，不要看 iostat。
  - 計算是 `Used / (Used + Avail)`，分母不是 Size。保留區塊會讓 Use% 比「Used / Size」高。
  - ⚠️ 接近 100% 只代表這個檔案系統快沒空間。它可以很滿但完全閒置，也可以 Use% 很低但裝置已經忙到延遲升高。
- **IUse%**（`df -i`）：
  - inode 用掉的比例。
  - ⚠️ IUse% 100% 而 Use% 仍低：不是碟子滿了，是檔案「個數」用盡（大量小檔、郵件、快取）。此時還有很多 GB 也無法再建立新檔。

btrfs、ZFS、以及有 snapshot 的檔案系統，`df` 的 Used 不等於「目錄加總」。那種環境要改看該檔案系統自己的用量工具。

---

## du

du 回答「空間被哪個目錄吃掉」。df 只告訴你這個檔案系統滿了，不告訴你是誰。

```bash
linux:~$ du -xh --max-depth=1 /var
4.0K    /var/local
1.2G    /var/log
18G     /var/lib
19G     /var
```

- **-x**：
  - 不跨越檔案系統。沒加的話，`/var` 底下若有別的掛載點會被重複算進父目錄。
- **-h**：
  - 以 K/M/G 顯示。
- **--max-depth=1**：
  - 只展開一層，先找該往哪一層挖。
- **數字**：
  - 預設是實際配置的區塊，不是 `ls -l` 的表面大小。稀疏檔要加 `--apparent-size` 才會接近表面大小。

⚠️ du 加總常常小於 df 的 Used。常見原因是已刪除但仍被行程開著的檔案：目錄上看不到，區塊還沒還給檔案系統。用下面的 `lsof +L1` 對。

---

## lsblk

lsblk 看磁碟、分割區、LVM 的樹狀關係，以及有沒有掛上來。它不提供使用率與健康度。

```bash
linux:~$ lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,MODEL,TRAN
NAME          SIZE TYPE FSTYPE MOUNTPOINT MODEL            TRAN
nvme0n1       477G disk                            NVMe SSD NVMe
└─nvme0n1p2   468G part ext4   /            NVMe SSD NVMe
```

- **NAME**：
  - 核心現在給的裝置名稱。重開機後 `sda` / `sdb` 可能對調；NVMe 的 `nvme0n1` 相對穩，但仍不要寫進需要永久識別的設定，改用 UUID。
- **SIZE**：
  - 裝置或分割區容量，不是剩餘空間。
- **TYPE**：
  - `disk`、`part`、`lvm`、`rom`。效能與 df 要看你實際對到的那一層。
- **FSTYPE / MOUNTPOINT**：
  - 檔案系統類型與掛載點。空的代表沒掛或沒有檔案系統。
- **TRAN**：
  - 匯流排：`nvme`、`sata`、`usb`、`iscsi`。USB 外接碟變慢時，瓶頸常常在這裡而不是在檔案系統。

---

## blkid

blkid 讀超級區塊上的 UUID、TYPE、LABEL。掛載與 fstab 用這些識別，不用會變的裝置名稱。

```bash
linux:~$ blkid
/dev/nvme0n1p2: UUID="0d2c1a44-7b31-4e0a-9f55-6c1e8a0b1234" TYPE="ext4"
```

- **UUID**：
  - 檔案系統識別。`/etc/fstab` 與下面的 `/dev/disk/by-uuid/` 都用它。
- **TYPE**：
  - 檔案系統類型。決定檢查時要叫 `e2fsck` 還是 `xfs_repair`。
- **LABEL**：
  - 人可讀的標籤，不一定有設。

---

## /dev/disk/by-uuid/

udev 依檔案系統 UUID 做的符號連結，指向目前的裝置節點。

```bash
linux:~$ ls -l /dev/disk/by-uuid/
lrwxrwxrwx 1 root root 15 09/22 01:40 0d2c1a44-7b31-4e0a-9f55-6c1e8a0b1234 -> ../../nvme0n1p2
```

- 連結目標是這一刻的裝置名稱。名稱若在下次開機改變，這條連結仍指向同一個檔案系統。
- 同目錄還有 `by-id/`（硬體序號）、`by-path/`（接在哪個埠）。診斷「這顆物理碟是誰」用 `by-id`；fstab 用 `by-uuid`。

---

## findmnt

findmnt 把掛載樹與掛載選項列清楚，比直接讀 `/proc/mounts` 容易對。

```bash
linux:~$ findmnt -D
SOURCE         FSTYPE  SIZE  USED AVAIL USE% TARGET
/dev/nvme0n1p2 ext4    468G   82G  362G  19% /
```

```bash
linux:~$ findmnt /var -o TARGET,SOURCE,FSTYPE,OPTIONS
TARGET SOURCE         FSTYPE OPTIONS
/var   /dev/nvme0n1p2 ext4   rw,relatime
```

- **-D**：
  - 模仿 df 的容量欄。解讀與 df 相同。
- **SOURCE**：
  - 裝置或虛擬檔案系統。
- **OPTIONS**：
  - 核心實際生效的掛載選項，來源是 mountinfo，不一定等於 `/etc/fstab` 裡寫的那一行（預設值會被補上）。
- **TARGET**：
  - 掛載點。

沒加 `-D` 時是樹狀清單，用來確認 bind mount、嵌套掛載有沒有讓 du 重複計算。

---

## mount

mount 不帶參數時，列出目前掛載，內容來自分區表的核心視圖。

```bash
linux:~$ mount | grep nvme0n1p2
/dev/nvme0n1p2 on / type ext4 (rw,relatime)
```

- 診斷時把它當成 findmnt 的簡表即可。要看剩餘空間用 df，要看選項用 findmnt。
- `/etc/mtab` 在多數系統上是指向 `/proc/self/mounts` 的符號連結，不是一份獨立紀錄。

---

## /proc/mounts

`/proc/mounts` 是核心公布的掛載表。`mount` 讀它；findmnt 讀的是資訊更完整的 `/proc/self/mountinfo`（含掛載 ID、父子關係、bind 傳播）。

```bash
linux:~$ cat /proc/mounts
/dev/nvme0n1p2 / ext4 rw,relatime 0 0
```

欄位依序是：

- **裝置**：
  - 來源。可與 blkid、by-uuid 對。
- **掛載點**：
  - 路徑。空白會以八進位跳脫。
- **檔案系統類型**。
- **選項**：
  - 核心眼中的選項。
- **dump / pass**：
  - 最後兩欄對應 fstab 的 dump 與 fsck 順序，在這份核心表裡通常是 `0 0`，不要拿來判斷開機時會不會跑 fsck。

---

## umount

umount 本身不提供診斷數字。它失敗時的訊息才是線索。

```bash
linux:~$ umount /mnt/data
umount: /mnt/data: target is busy.
```

- **target is busy**：
  - 仍有行程把該掛載點當工作目錄，或開著裡面的檔案。
  - 接著用 `lsof` 或 `fuser -vm /mnt/data` 找是誰，而不是先拆掛載。
- **lazy unmount（-l）**：
  - 路徑會先從命名空間消失，已開啟的 I/O 仍可能繼續。看起來卸掉了，裝置卻還在忙。

---

## lsof

df 與 du 對不上、或 umount 說 busy 時，用 lsof 看誰還握著檔案。

```bash
linux:~$ lsof +L1
COMMAND  PID USER   FD   TYPE DEVICE    SIZE/OFF NLINK   NODE NAME
python3 4821 kam     3w   REG  259,2  1073741824     0  18432 /var/tmp/big.dat (deleted)
```

- **+L1**：
  - 💡 列出連結數小於 1、仍被開啟的檔案，也就是已刪除但未關閉。
  - **SIZE/OFF** 仍算在 df 的 Used 裡，du 不會把它算進任何目錄。行程結束或關掉這個 fd 後，空間才回到 Avail。
- **FD**：
  - 檔案描述符。`cwd` 代表行程的工作目錄還在這個掛載點上，umount 會因此 busy。
- **DEVICE**：
  - `major,minor`。可對 `/proc/diskstats` 與 lsblk。

某個掛載點被誰佔用：`lsof +f -- /mnt/data`。

---

## iostat

iostat 把「裝置有多忙、延遲多少」拆開。整段時間的平均會把尖峰稀釋掉，所以排查當下要加間隔。

```bash
linux:~$ iostat -x 1
Linux 7.0.0-14-generic (linux)      09/22/2026      _x86_64_        (4 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           0.25    0.00    0.25    0.00    0.00   99.50

Device            r/s     rkB/s   rrqm/s  %rrqm r_await rareq-sz     w/s     wkB/s   wrqm/s  %wrqm w_await wareq-sz     d/s     dkB/s   drqm/s  %drqm d_await dareq-sz     f/s f_await  aqu-sz  %util
nvme0n1        12.40    480.00     0.00   0.00    0.15    38.71    8.20    336.00     1.10  11.83    0.42    40.98    0.00     0.00     0.00   0.00    0.00     0.00    0.40    0.80    0.01    0.40
```

⚠️ 帶間隔時，第一筆是開機到現在的平均。看這一秒要從第二筆開始。數字來自 `/proc/diskstats` 的差值。

1. 吞吐（做了多少）

- **r/s、w/s**：
  - 每秒完成的讀、寫請求數（合併之後）。
- **rkB/s、wkB/s**：
  - 每秒讀、寫的資料量。
- **rareq-sz、wareq-sz**：
  - 平均請求大小（KB）。很小代表大量細碎 I/O，同樣的 rkB/s 會比循序讀更累。

2. 延遲與佇列（💡 忙不忙看這裡）

- **r_await、w_await**：
  - 讀或寫從發出到完成的平均毫秒，含在佇列裡等待的時間。
  - 💡 體感慢不慢，優先看這兩欄，不要只看 %util。
- **aqu-sz**：
  - 平均佇列長度（含正在服務的請求）。
  - 它和 await 一起升高，代表請求堆起來了。await 高但 aqu-sz 接近 0，比較像單次 I/O 本身就慢（裝置、路徑、遠端檔案系統），不是本地佇列打爆。

3. 使用率（容易誤讀）

- **%util**：
  - 取樣區間內，裝置至少有一個 I/O 在處理的時間比例。
  - ⚠️ 傳統單顆磁碟、請求大致串行時，長期接近 100% 可以當成飽和。
  - NVMe、SSD、RAID 能並行處理多個請求。%util 100% 只表示「一直有 I/O 在飛」，不表示頻寬或 IOPS 已經到硬體上限。這種裝置要同時看 await 有沒有變長、rkB/s 與 w/s 有沒有到這顆碟該有的水準。
- **%iowait**（avg-cpu 那一列）：
  - CPU 閒置、同時有未完成磁碟 I/O 的時間。它不是磁碟使用率。CPU 一直在算時，磁碟很慢也可以幾乎沒有 iowait。

4. 合併、TRIM、flush

- **rrqm/s、wrqm/s、%rrqm、%wrqm**：
  - 送進裝置前被合併掉的相鄰請求。高代表核心在把細碎寫入併成較大的請求。
- **d/s、dkB/s**：
  - discard / TRIM。
- **f/s、f_await**：
  - flush（強制寫入穩定媒體）。f_await 高時，有程式在等資料真正落下，常見於資料庫的 commit。

舊版還有 **svctm**。那個欄位是用 `%util / 完成速率` 反推的，不是裝置回報的服務時間，新版 iostat 已拿掉。不要用它判斷磁碟快慢。

分割區與整顆碟會各有一列。飽和要看整顆碟（例如 `nvme0n1`）；df 的 Use% 則是檔案系統所在的那個分割區。

---

## /proc/diskstats

`/proc/diskstats` 是 iostat 與 `sar -d` 的計數來源。欄位是開機以來的累計值，不是每秒速率。

```bash
linux:~$ grep nvme0n1 /proc/diskstats
 259       0 nvme0n1 120000 0 9600000 18000 80000 8000 6400000 33600 0 48000 51600 0 0 0 0 400 320
```

每行開頭是 major、minor、裝置名稱，接著：

1. 讀完成次數
2. 被合併的讀
3. 讀取的 sector 數
4. 花在讀的毫秒
5. 寫完成次數
6. 被合併的寫
7. 寫入的 sector 數
8. 花在寫的毫秒
9. 目前進行中的 I/O
10. 裝置有 I/O 在處理的毫秒（%util 的原料）
11. 加權毫秒（aqu-sz 的原料：這段時間的差值 ÷ 毫秒）
12. discard 完成次數（核心 4.18+）
13. 被合併的 discard
14. discard 的 sector 數
15. 花在 discard 的毫秒
16. flush 完成次數（核心 5.5+）
17. 花在 flush 的毫秒

- ⚠️ 第 3、7、14 欄的 sector 固定是 512 bytes，即使這顆碟的邏輯區塊是 4096。
- 速率要自己對兩個時間點取差值。手算容易錯，即時看 iostat，歷史看 sar。
- 第 9 欄是此刻佇列裡的請求數，最接近「現在卡著幾個 I/O」。

---

## sar

sar -d 用同一組磁碟欄位留下歷史，用來事後對照「當時慢，是不是碟在忙」。即時欄位意義與 iostat 相同。

```bash
linux:~$ sar -d -p
Linux 7.0.0-14-generic (linux)      09/22/2026      _x86_64_        (4 CPU)

01:00:05 AM       DEV       tps     rkB/s     wkB/s     dkB/s   areq-sz    aqu-sz     await     %util
01:10:05 AM   nvme0n1     20.60    480.00    336.00      0.00     39.61      0.01      0.26      0.40
01:20:05 AM   nvme0n1     18.40    410.00    290.00      0.00     38.04      0.01      0.24      0.35
01:30:05 AM   nvme0n1     95.00  12000.00    420.00      0.00    130.74      0.08      0.84      6.10
01:40:05 AM   nvme0n1     22.10    520.00    300.00      0.00     37.10      0.01      0.28      0.42
Average:      nvme0n1     39.03   3352.50    336.50      0.00     94.50      0.03      0.41      1.82
```

- **-p**：
  - 印 `nvme0n1` 這種名稱。不加的話是 `dev259-0`（major-minor）。
- **tps**：
  - 每秒完成的傳輸數，約為讀加寫。
- **rkB/s、wkB/s、dkB/s**：
  - 讀、寫、discard 的吞吐。
- **areq-sz**：
  - 平均請求大小（KB）。
- **aqu-sz**：
  - 平均佇列長度。對應 iostat 的 aqu-sz。
- **await**：
  - 💡 平均延遲（毫秒），含排隊。事後判斷「慢不慢」以這欄為主。
- **%util**：
  - 與 iostat 相同。01:30 的 rkB/s 明顯升高，但 await 仍不到 1ms、%util 只有 6%：那是一次讀取尖峰，不是碟飽和。可對 memory.md 同一時段 kbcached 上升。

預設約 10 分鐘一筆，短脈衝會被平均掉。

---

## iotop

容量與延遲都指向磁碟之後，用 iotop 看是哪個行程在讀寫。

```bash
linux:~$ iotop -oP
Total DISK READ:         480.00 K/s | Total DISK WRITE:       336.00 K/s
Current DISK READ:       480.00 K/s | Current DISK WRITE:       0.00 B/s
    PID  PRIO  USER     DISK READ  DISK WRITE  SWAPIN     IO>    COMMAND
   4821 be/4 kam         480.00 K/s    0.00 B/s  0.00 %  0.12 % python3
```

- **-o**：
  - 只留目前真的有 I/O 的行程。
- **-P**：
  - 依行程加總，不拆執行緒。
- **DISK READ / DISK WRITE**：
  - 這個行程造成的讀寫量。
- **SWAPIN**：
  - 花在把頁從 Swap 讀回的時間比例。它高時，主因是記憶體不足，不是這顆碟的空間滿了。對照 memory.md 的 si。
- **IO>**：
  - 💡 行程花在等待 I/O 的時間比例（含 SWAPIN）。
  - Linux 5.14 起 delay accounting 預設常是關的，這欄會是 0 或 iotop 直接提示。需要時 `sysctl kernel.task_delayacct=1`（只影響之後新建立的行程）。

iotop 要 root。它沒有歷史。

---

## /proc/sys/vm/dirty_ratio

這組參數決定「髒頁累積到多少，核心才把它們寫回磁碟」。寫入突然變慢、memory.md 的 **kbdirty** 降不下來時，先確認不是被這組門檻卡住。

```bash
linux:~$ cat /proc/sys/vm/dirty_ratio /proc/sys/vm/dirty_background_ratio
20
10
```

- **dirty_background_ratio**：
  - 髒頁佔「可弄髒的記憶體」（空閒頁 + 可回收頁，不是 MemTotal）的百分比達到這裡，背景 flusher 開始寫回。預設約 10。
- **dirty_ratio**：
  - 達到這裡，產生寫入的行程自己會被拉去寫回，寫入呼叫變慢。預設約 20。
  - 💡 這是應用程式感到寫入停頓的門檻，不是磁碟 Use%。
- **dirty_bytes、dirty_background_bytes**：
  - 若非 0，會蓋過對應的 ratio，改成固定位元組數。ratio 與 bytes 同時看才不會誤判。

門檻很高時，髒頁可以堆很大，一旦刷出就變成一波陡的 wkB/s 與 await。門檻很低時，寫入會更頻繁地停下來等磁碟。

---

## smartctl

smartctl 看磁碟自己回報的健康狀態，不看檔案系統滿不滿。

```bash
linux:~$ smartctl -H /dev/nvme0n1
SMART overall-health self-assessment test result: PASSED
```

SATA 碟再看這幾個屬性（`smartctl -A`）：

- **Reallocated_Sector_Ct**：
  - 已被替換的壞磁區。持續增加代表媒體正在退化。
- **Current_Pending_Sector**：
  - 待確認的不穩定磁區。大於 0 就不要再把它當可靠的儲存。
- **Offline_Uncorrectable**：
  - 離線掃描也無法修正的磁區。
- **Temperature_Celsius**：
  - 溫度。過熱會降速，看起來像 await 變高。

- **PASSED** 只代表韌體自己的彙總判斷。Pending、Offline_Uncorrectable、Media Errors 大於 0 時，即使整體仍是 PASSED，也該備份。

---

## nvme

nvme-cli 讀 NVMe 的 SMART log。`percentage_used` 不是 df 的 Use%。

```bash
linux:~$ nvme smart-log /dev/nvme0n1
critical_warning                        : 0
temperature                             : 35 °C
available_spare                         : 100%
available_spare_threshold               : 10%
percentage_used                         : 1%
media_errors                            : 0
num_err_log_entries                     : 0
```

- **critical_warning**：
  - 0 表示韌體沒有亮起備用空間、溫度、可靠度、唯讀等警告位元。非 0 要逐位看，不能當成「還有幾個錯誤」的計數。
- **available_spare**：
  - 剩餘備用區塊百分比。低於 **available_spare_threshold** 時，碟子正在耗盡替換空間。
- **percentage_used**：
  - ⚠️ 廠商估計的壽命消耗（磨損），不是空間使用率。1% 表示磨損很少；它可以和 df Use% 100% 同時成立，也可以相反。
- **media_errors**：
  - 媒體錯誤次數。大於 0 要備份，並用 smartctl / nvme error-log 看細節，不是先跑會寫入的表面掃描。
- **temperature**：
  - 控制器回報的溫度。

---

## hdparm

hdparm -t 是一次循序讀的粗測，用來確認「這條路徑讀得到什麼等級的循序頻寬」。

```bash
linux:~$ hdparm -t /dev/nvme0n1

/dev/nvme0n1:
 Timing buffered disk reads: 6150 MB in  3.00 seconds = 2050.00 MB/sec
```

- **-t**：
  - 繞過頁面快取、做循序讀。數字是 MB/sec 等級的參考，不是 IOPS，也不是 await。
- **-T**：
  - ⚠️ 測的是從頁面快取讀的速度，幾乎不是磁碟。不要把 -T 的結果當成碟的效能。
- NVMe 上這個數字常常不能代表實際工作負載。延遲與小區塊隨機讀寫仍以 iostat 的 await、rareq-sz 為準。

---

## badblocks

badblocks 掃描媒體上讀不到的區塊。它是破壞力很高的工具，不是日常監控。

```bash
linux:~$ badblocks -v /dev/nvme0n1p2
```

不帶 `-w` 或 `-n` 時是唯讀掃描。

- **-w**：
  - ⚠️ 以測試圖樣覆寫整個裝置，上面的檔案系統與資料會消失。
- **-n**：
  - 非破壞模式仍是「讀出、寫測試圖樣、再寫回」。中途斷電或被中斷，該區塊的資料可能已經壞掉。不要對已掛載、有需要保留的資料的裝置跑。
- 現代 SSD / NVMe 會自己替換壞區塊。smartctl / `nvme smart-log` 的 media_errors、pending sector 比對整顆碟做寫入掃描合適。檔案系統層的唯讀檢查用下一節的 `-n`。

---

## fdisk

fdisk -l 只讀分割表：碟有多大、邏輯磁區多大、每個分割區從哪裡到哪裡。

```bash
linux:~$ fdisk -l /dev/nvme0n1
Disk /dev/nvme0n1: 476.94 GiB, 512110190592 bytes, 1000215216 sectors
Disk model: NVMe SSD
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
Disklabel type: gpt

Device           Start        End    Sectors  Size Type
/dev/nvme0n1p2  206848 1000214527 1000007680  477G Linux filesystem
```

- **logical/physical**：
  - 邏輯磁區與實體磁區大小。diskstats 的 sector 仍按 512 bytes 計，兩者不同時手算容量不要混用。
- **Disklabel type**：
  - `gpt` 或 `dos`（MBR）。
- **Type**：
  - 分割區類型，不是檔案系統類型。ext4 與否要看 blkid。

⚠️ 不加 `-l`、又指定裝置時，fdisk 會進入可寫入分割表的互動模式。看佈局只用 `-l`。

---

## parted

parted -l 同樣是讀分割表，單位可以直接是人類可讀的大小。

```bash
linux:~$ parted -l
Model: NVMe SSD (nvme)
Disk /dev/nvme0n1: 512GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt

Number  Start   End    Size   File system  Name  Flags
 2      106MB   512GB  512GB  ext4
```

- **File system**：
  - parted 偵測到的檔案系統，僅供對照；以 blkid 為準。
- **Flags**：
  - 例如 `boot`、`esp`、`raid`。和 df 的 Use%、iostat 的 await 無關。

不加 `-l` 的 `parted /dev/...` 是互動式，可以改分割表。診斷只用 `-l`。

---

## fsck

fsck 是前端。它依檔案系統類型轉去叫 `e2fsck` 或 `xfs_repair` 等。

- ⚠️ 對 XFS，`fsck` / `fsck.xfs` 預設幾乎不檢查就成功結束。XFS 要明確用 `xfs_repair -n`。
- 修復（會改檔案系統的那一種）只在卸載之後做。先用 `-n` 看有沒有問題。

---

## e2fsck

ext2/ext3/ext4 的檢查工具。`-n` 只報告，不修改。

```bash
linux:~$ e2fsck -n /dev/nvme0n1p2
e2fsck 1.47.0 (5-Feb-2023)
/dev/nvme0n1p2: clean, 480000/31457280 files, 21500000/122000000 blocks
```

- **-n**：
  - 以唯讀方式開啟，回答全部當成 No。已掛載時結果可能因為檔案系統仍在變而不準，但不會寫入。
- **files**：
  - 已用 inode / inode 總數。可對 df -i。
- **blocks**：
  - 已用區塊 / 總區塊。可對 df 的 Used 與 Size。
- **clean**：
  - 日誌認為上次卸載是乾淨的。不是 SMART 健康，也不是 Use% 很低。

不帶 `-n` 的修復會改中繼資料，物件必須先 umount。

---

## xfs_repair

XFS 的檢查與修復。檢查用 `-n`。

```bash
linux:~$ xfs_repair -n /dev/nvme0n1p2
Phase 1 - find and verify superblock...
Phase 2 - using internal log
        - zero log...
        - scan filesystem freespace and inode maps...
...
No modify flag set, skipping filesystem flush and exiting.
```

- **-n**：
  - 不修改。輸出末行應看到 no modify。
- 不加 `-n`：
  - 會試圖修復，而且要求檔案系統未掛載。不要對 `/` 這種掛載中的 XFS 直接跑。
- 它不報告 Use% 或 await。空間用 df，速度用 iostat。

---

## dmidecode

dmidecode 讀 SMBIOS。磁碟容量、掛載、SMART、延遲都不在這裡。

- 記憶體條、處理器、主機板用它（記憶體見 memory.md 那一類規格工具）。
- 這顆碟的型號與匯流排用 `lsblk -d -o NAME,SIZE,MODEL,TRAN`，健康用 smartctl 或 `nvme smart-log`。

---

## 🔍 判斷是空間滿、還是磁碟忙

**df**

1. 空間夠：Use% 不高，Avail 還大，而且 `df -i` 的 IUse% 也不高。
2. 容量用盡：Use% 接近 100%。再跑 du 找目錄。
3. inode 用盡：IUse% 接近 100%，Use% 仍低。刪的是檔案個數，不是大檔。
4. Use% 高不解釋變慢。變慢改看 iostat 的 await。

**du 對 df**

1. 兩者接近：目錄加總就是空間的去向。
2. df 的 Used 明顯大於 du：優先 `lsof +L1`，找已刪除仍開啟的檔。

**iostat /proc/diskstats**

1. 閒：%util 低、await 在這顆碟的正常範圍（NVMe 常常遠小於 1ms）、aqu-sz 接近 0。
2. 佇列堆高：aqu-sz 與 await 一起上升。傳統單磁碟上 %util 會同時接近 100%。
3. 並行裝置（NVMe、SSD）：%util 100% 仍要看 await 有沒有變差、吞吐有沒有到該裝置的水準。%util 單獨不能判定飽和。
4. await 高、但 rkB/s 與 wkB/s 都很低：延遲問題。再分是本地媒體（smartctl、溫度）還是路徑（USB、網路檔案系統）。

**iotop**

1. 找出 DISK READ / DISK WRITE 最大的行程。
2. SWAPIN 高：記憶體不足造成的讀碟，先回到 memory.md，不是先換碟。

**sar -d**

1. 事後先看 await 與 aqu-sz，不要只看 %util。
2. rkB/s 或 wkB/s 有尖峰、await 仍低：有過流量，但沒有飽和。

**SMART / nvme**

1. media_errors、Current_Pending_Sector、Offline_Uncorrectable 大於 0，或 available_spare 低於門檻：媒體不可靠。這和 df 是否還有空間無關。
2. percentage_used 是磨損，不是 Use%。

💡 一分鐘快速診斷

1. 寫不進去：`df -h` 與 `df -i`。滿了再用 du；df 比 du 大很多就看 `lsof +L1`。
2. 變慢：`iostat -x 1` 的第二筆以後，看 await 與 aqu-sz。%util 只在單顆傳統磁碟上大致等於飽和。
3. 知道是碟之後：iotop 看是哪個行程。SWAPIN 高就改查記憶體。
4. 事情已經過去：`sar -d -p` 看當時的 await。髒頁居高不下時同時看 memory.md 的 kbdirty 與 dirty_ratio。

---

## 🛠 設計目的、資料來源和適用場景

- **df**
  - 定位: 檔案系統容量快照
  - 時間軸: 僅看當下
  - 資料來源: `statfs`（檔案系統超級區塊的用量）
  - 優點: 一眼看出 Use% 與 Avail。`-i` 能抓到 inode 用盡。
  - 缺點: 看不到誰佔用、看不到延遲與速率，也沒有歷史。

- **du**
  - 定位: 目錄佔用
  - 時間軸: 僅看當下（掃描當下的目錄樹）
  - 資料來源: 走目錄讀到的檔案配置
  - 優點: 能指出下一層該刪哪裡。
  - 缺點: 慢；看不到已刪除仍開啟的檔；不跨越檔案系統時才不會重複計算。

- **iostat**
  - 定位: 即時吞吐、延遲、佇列
  - 時間軸: 即時連續監控
  - 資料來源: `/proc/diskstats`（sysstat）
  - 優點: await 與 aqu-sz 能判斷是不是真的在排隊。
  - 缺點: 第一筆是開機至今。%util 在 NVMe 上容易讀成飽和。不告訴你是哪個行程。

- **/proc/diskstats**
  - 定位: 區塊層累計計數
  - 時間軸: 開機以來的累計，速率要自己相減
  - 優點: 不依賴 sysstat，腳本可以直接讀。
  - 缺點: sector 固定 512 bytes；欄位多，沒有現成的每秒值。

- **sar -d**
  - 定位: 磁碟歷史
  - 時間軸: 當天或過去特定日期（通常 10 分鐘一筆）
  - 資料來源: sadc 寫入的 sa 檔，內容仍來自 `/proc/diskstats`
  - 優點: 事後能把 await、aqu-sz、吞吐對在同一段時間。對照 memory.md 的 sar -r 看當時是缺記憶體還是缺碟。
  - 缺點: 要事先啟用 sysstat。間隔太粗會吃掉短脈衝。

- **iotop**
  - 定位: 哪個行程在讀寫
  - 時間軸: 即時
  - 資料來源: task I/O accounting 與 delay accounting
  - 優點: 直接對到 PID。SWAPIN 能把「記憶體不夠」和「碟本身慢」分開。
  - 缺點: 要 root；新核心可能要打開 task_delayacct 才有 IO 時間。沒有歷史。

- 空間和忙碌不要混讀
  - 容量：df 的 Use% 與 `df -i`。這是磁碟上的 free。
  - 忙碌：iostat / sar 的 await 與 aqu-sz。這是磁碟上的「有沒有人在等」。
  - %util 像一個容易誤讀的彙總：單顆傳統磁碟上還能用，並行 SSD 上要退回 await。

- 裝置身份、掛載、健康
  - 佈局：lsblk、fdisk -l、parted -l。只讀，不進入會寫分割表的互動模式。
  - 識別：blkid 與 `/dev/disk/by-uuid/`。fstab 不要寫死會變的 sda。
  - 掛載：findmnt、`/proc/mounts`。umount busy 時用 lsof，不先做 lazy unmount。
  - 健康：smartctl、`nvme smart-log`。percentage_used 是磨損。badblocks 的寫入模式會毀掉資料，不是第一步。
  - 檔案系統結構：e2fsck -n、xfs_repair -n。`fsck` 對 XFS 不能代替 `xfs_repair -n`。
