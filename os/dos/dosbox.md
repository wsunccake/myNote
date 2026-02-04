# DOSBox

## install

- [DOSBox Download](https://www.dosbox.com/download.php?main=1)

current last: 0.74-3

```bash
# for debian / ubuntu
ubuntu:~ # apt install dosbox
```

```bash
linux:~ $ dosbox -version
linux:~ $ dosbox -printconf
```

---

## conf

```powershell
PS C:\Users\user> dosbox -printconf
PS C:\Users\user> vi ${env:LOCALAPPDATA}\DOSBox\dosbox-0.74-3.conf
```

```bash
linux:~ $ dosbox -printconf
linux:~ $ vi ~/.dosbox/dosbox-0.74-3.conf
```

```ini
[sdl]
fullscreen=false
fulldouble=false
fullresolution=original
windowresolution=original
output=surface
autolock=true
sensitivity=100
waitonerror=true
priority=higher,normal
mapperfile=mapper-0.74-3.map
usescancodes=true

[dosbox]
language=
machine=svga_s3
captures=capture
memsize=16

[render]
frameskip=0
aspect=false
scaler=normal2x

[cpu]
core=auto
cputype=auto
cycles=auto
cycleup=10
cycledown=20

[mixer]
nosound=false
rate=44100
blocksize=1024
prebuffer=25

[midi]
mpu401=intelligent
mididevice=default
midiconfig=

[sblaster]
sbtype=sb16
sbbase=220
irq=7
dma=1
hdma=5
sbmixer=true
oplmode=auto
oplemu=default
oplrate=44100

[gus]
gus=false
gusrate=44100
gusbase=240
gusirq=5
gusdma=3
ultradir=C:\ULTRASND

[speaker]
pcspeaker=true
pcrate=44100
tandy=auto
tandyrate=44100
disney=true

[joystick]
joysticktype=auto
timed=true
autofire=false
swap34=false
buttonwrap=false

[serial]
serial1=dummy
serial2=dummy
serial3=disabled
serial4=disabled

[dos]
xms=true
ems=true
umb=true
keyboardlayout=auto

[ipx]

ipx=false

[autoexec]
```

## mount

使用指令掛載，每次開機完都要執行

```bash
# mount local folder to dosbox
Z:\> mount c /home/dosbox   # for linux
Z:\> mount c d:\dosbox      # for windows

# umount
Z:\> mount -u c

# path
Z:\> path                   # show path
Z:\> path %PATH%;c:\bin     # append path
```

寫在設定檔，開機完都會自動執行

```ini
[autoexe]
MOUNT C D:\data             # mount local folder
# PATH=Z:\;C:\BIN           # set PATH
# MOUNT D G:\ -t cdrom      # mount CD-ROM
PATH %PATH%;c:\bin

[sdl]
# windowresolution=original
windowresolution=1280x960
# output=surface
output=opengl
```

---

## command

- DIR：顯示當前目錄下的檔案和子目錄列表。
- CD <目錄名稱>：切換到指定的目錄。
- MD <目錄名稱> 或 MKDIR <目錄名稱>：建立一個新的目錄。
- RD <目錄名稱> 或 RMDIR <目錄名稱>：刪除一個空的目錄。
- COPY <來源> <目的地>：複製檔案。
- DEL <檔案名稱> 或 ERASE <檔案名稱>：刪除檔案。
- REN <舊檔案名稱> <新檔案名稱> 或 RENAME <舊檔案名稱> <新檔案名稱>：重新命名檔案。
- TYPE <檔案名稱>：顯示文字檔案的內容。
- EDIT：啟動 DOS 編輯器 (如果存在)。這是一個簡單的文字編輯器，可用於編寫程式碼或文字檔。
- CLS：清除螢幕上的所有內容。
- MEM：顯示記憶體使用情況。
- EXE、COM 或批次檔名稱：直接輸入可執行檔或批次檔的名稱來運行程式。

```bat
DIR /W (寬格式顯示)
CD MYPROG (進入 MYPROG 目錄)
CD .. (回到上一級目錄)
CD \ (回到根目錄)
MD GAMES
RD OLDDIR
COPY MYFILE.TXT A:\BACKUP\
DEL TEMP.BAK
REN OLDNAME.DOC NEWNAME.DOC
TYPE README.TXT

GAME.EXE
```

---

## DOSBox-X

1. DOSBox (標準版)

最廣為人知的版本，主要目標是讓 90 年代的經典遊戲（如《大富翁》、《仙劍奇俠傳》）能在現代電腦上跑。

- 優點：
  - 輕量、穩定： 只專注於遊戲所需的指令集。
  - 跨平台相容性極佳： 在各種系統（甚至手機、瀏覽器）上表現一致。
  - 操作簡單： 設定檔非常直觀，適合只想開遊戲的人。

- 缺點：
  - 開發功能殘缺： 就像你遇到的，它對 Input Redirection (<) 和 Pipe (|) 的支援很差，甚至會卡死。
  - 硬體模擬有限： 僅支援基本的 VGA/SoundBlaster，不支援較複雜的商用硬體環境。
  - 擴充性低： 很難模擬長檔名 (LFN) 或高解析度的顯示模式。

2. DOSBox-X (開發者加強版)

從 DOSBox 分支出來的「怪獸級」計畫，目標是成為一個完整的 DOS 模擬環境，而不僅僅是遊戲機。

- 優點：
  - 完美的腳本支援： 修正了重導向與管線的 Bug，非常適合跑 MASM、DEBUG 自動化。
  - 支援 Windows 3.x/9x： 它甚至可以讓你流暢地在裡面裝 Windows 98。
  - 功能極其強大： 支援打印機模擬、中文編碼 (TTF 字型)、長檔名、APM（電源管理）。
  - UI 選單： 視窗上方有一排選單（選單欄），可以直接切換磁碟、更改設定，不用去改 .conf 檔。

- 缺點：
  - 設定複雜： 因為功能太多，其設定檔 (dosbox-x.conf) 密密麻麻，新手容易看暈。
  - 體積較大： 相對於標準版，它的資源消耗稍微多一點點（但對於現代電腦來說沒差）。

| 功能                  | DOSBox               | DOSBox-X                   |
| --------------------- | -------------------- | -------------------------- |
| 主要定位              | 經典遊戲模擬         | 軟體開發、系統模擬、遊戲   |
| "自動化腳本 (<, \|)"  | 不穩定 (常卡死)      | 完美支援                   |
| 長檔名 (LFN)          | 不支援 (僅 8.3 格式) | 支援                       |
| 文字複製貼上          | 難以操作             | 支援選取與主機貼上         |
| 打印機/串列埠         | 基本模擬             | 完整模擬 (可導向 PDF/實體) |
| 即時存檔 (Save State) | 視版本而定           | 原生內建                   |

```bash
linux:~ $ dosbox-x -printconf
linux:~ $ vi ~/.config/dosbox-x/dosbox-x-2024.03.01.conf

# copy dosbox config to dosbox-x config
linux:~ $ cat `dosbox -printconf` > `dosbox-x -printconf`
```

---

## MASM

- [masm-dos](https://github.com/shiburaj/masm-dos)

```bash
Z:\> masm test.asm
Z:\> link test.obj
Z:\> test.exe
```
