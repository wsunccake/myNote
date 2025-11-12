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

## MASM

- [masm-dos](https://github.com/shiburaj/masm-dos)

```bash
Z:\> masm test.asm
Z:\> link test.obj
Z:\> test.exe
```
