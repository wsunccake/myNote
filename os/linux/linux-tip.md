# Tip and Troubleshoot

## System

```bash
linux:~ # ps aux
linux:~ # ps axf
linux:~ # ps fww -p <pid>
linux:~ # ps -ejf
```

```bash
linux:~ # grep VmSwap /proc/<pid>/cmdline
linux:~ # grep VmSwap /proc/<pid>/status
linux:~ # grep VmSwap /proc/*/status | sort -n -k2
```

### Common

#### 忘記 root 密碼

在 grub2 的 kerenl 後面加上 init=/bin/sh

```sh
sh-4.2# mount -oremount,rw /
sh-4.2# mount -oremount,rw /proc
sh-4.2# password
sh-4.2# touch /.autorelabel       # 因為 selinux 關係, 所以須使用次步驟, 之後要多重開機一次; 若無 selinux 可略過次步驟
sh-4.2# sync
sh-4.2# /sbin/reboot -f
```

### CPU

### Memory

### HD

使用  smartctl 確認 SSD 使用狀況, Raw_Read_Error_Rate, Read_Soft_Error_Rate, Soft_Read_Error_Rate

```bash
linux:~ # smartctl -i /dev/sda
linux:~ # smartctl -s on|off /dev/sd
linux:~ # smartctl -x|-a /dev/sda
linux:~ # smartctl -d sat+megaraid,0 -x /dev/sda 
```

MegaCli

```
linux:~ # rpm -ivh MegaCli-8.07.14-1.noarch.rpm
linux:~ # alias megacli='/opt/MegaRAID/MegaCli/MegaCli64'
linux:~ # megacli -AdpAllInfo -aALL | grep Disks
linux:~ # megacli -ldinfo -lALL -aALL
linux:~ # megacli -pdlist -aALL | grep state
linux:~ # megacli -AdpEventLog -GetLatest 100 -f events.log -aALL
```

#### 清除 MBR

```bash
linux:~ # dd if=/dev/zero of=/dev/sda bs=512 count=1
```

### CD/DVD

#### 掛載 image/iso

```bash
linux:~ # mount -oloop image.iso /mnt
```

#### 光碟燒錄

wodim -> cdrecord (symbol link)

```bash
linux:~ # wodim -v -dao dev=/dev/cdrw image.iso

linux:~ # wodim --devices dev=/dev/sr0
linux:~ # wodim -scanbus dev=/dev/sr0
linux:~ # wodim -prcap
```

#### 建立 image/iso

genisoimage -> mkisofs (symbol  link)

```bash
linux:~ # genisoimage -r -joliet-long -V "cd_name" -o image.iso dir
```

### Desktop


#### GNOME 3 Menu 設定

GNOME3 app 檔副檔名為 `*.desktop`, 存放目錄為, /usr/share/applications/, /usr/local/share/applications/, ~/.local/share/applications

```bash
Linux:~/.local/share/applications # vi app.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=IntelliJ IDEA
Icon=/opt/idea-IU-143.1821.5/bin/idea.sh/idea.png
Exec="/opt/idea-IU-143.1821.5/bin/idea.sh" %f
Comment=Develop with pleasure!
Categories=Development;IDE;
Terminal=false
StartupWMClass=jetbrains-idea
```

#### GNOME 3 Startup 設定


```bash
linux:~ # gnome-session-properties

linux:~ # vi ~/.config/autostart/app.desktop
Type=Application
Exec=java -jar /usr/local/bin/selenium-server-standalone-3.4.0.jar
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_US]=Selenium RC
Name=Selenium RC
Comment[en_US]=Run Selenium RC
Comment=Run Selenium RC
```

### Other

stty 設定終端機顯示行列字數

```bash
linux:~ # stty
linux:~ # stty -a
linux:~ # stty columns 200
```


complete 自動補齊

```bash
# list all completion
linux:~ # complete -p

# completion all command
linux:~ # complete -c which == complete -A command which 
linux:~ # which [TAB] [TAB]
# completion all command
# completion

# customed definition completion
linux:~ # complete -W 'host1' ssh
linux:~ # ssh [TAB] [TAB]
```


----

## Network


----

## Service

```bash
ubuntu:~ $ sudo service avahi-daemon stop
ubuntu:~ $ sudo sh -c "echo manual > /etc/init/avahi-daemon.override"
```


----

## Regex

### grep

#### 不顯示 空行 跟 \# 開頭

```bash
linux:~ # grep -Ev '^$|^#'
```

### sed

```bash
// remove ansi color code
linux:~ # sed 's/\x1b\[[0-9;]*m//g'  file.log
```

#### 跨行搜尋

顯示特定內容

```bash
linux:~ # sed -n "/<\!--/,/-->/p" index.html
```

不顯示特定內容

```bash
linux:~ # sed  "/<\!--/,/-->/d" index.html
```


---

## Compile


### make

```bash
# method 1: 在 configure 時指定安裝路徑
Linux:~/pkg # ./configure --prefix=/install_dir
Linux:~/pkg # make
Linux:~/pkg # make install

# method 2: 在 make install 時指定安裝路徑
Linux:~/pkg # ./configure
Linux:~/pkg # make
Linux:~/pkg # make install DESTDIR=/install_dir
```


---

## Ineternet


### SSH

```bash
# forwarding port
linux:~ # ssh -L <local_port>:<remote_ip>:<remote_port> <forwarding_host>
linux:~ # ssh -L 9000:192.168.0.1:5901 <forwarding_host>
linux:~ # vncviewer 127.0.0.1 ::9000

# dynamic forwarding port
linux:~ # ssh -D <local_port> <forwarding_host>
linux:~ # ssh -D 9999 <forwarding_host>

# browser set proxy is socket5 127.0.0.1:9000
```

### SFTP

```bash
linux:~ # sftp 192.168.0.1
# 下載續傳
sftp> get -ar <remote_file>
sftp> reget <remote_file>
# 上傳續傳
sftp> put -ar <local_file>
sftp> reput <local_file>
```


### Chrome

在 Chrome Dev Tool 中, 輸入以下程式碼, 可直接 import javascript

```javascript
var jq = document.createElement('script');
jq.src = "https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js";
document.getElementsByTagName('head')[0].appendChild(jq);

$("#lst-ib").val("python");
```


### firefox

url 輸入 about:config

搜尋 network.http.max-persistent-connections-per-server 設定下載數量
