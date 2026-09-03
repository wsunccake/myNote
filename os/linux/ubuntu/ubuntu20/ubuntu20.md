# ubuntu 20

## network

netplan.io

```bash
[ubuntu:~ ] # dpkg -l netplan.io

[ubuntu:~ ] # vi /etc/netplan/00-installer-config.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens192:
      link-local:
        - ipv4
      dhcp4: no
      addresses:
        - 192.168.1.11/24
      gateway4: 192.168.1.1
      nameservers:
         addresses:
           - 192.168.1.1
           - 8.8.8.8
      routes:
        - to: 192.168.2.11 # default or 0.0.0.0/0
          via: 192.168.1.100

    ens172:
      dhcp4: yes
      dhcp4-overrides:
        use-routes: false
    ens2: {}
  vlans:
    vlan100:
      id: 100
      link ens2

[ubuntu:~ ] # netplan try
[ubuntu:~ ] # netplan apply
[ubuntu:~ ] # netplan ip leases ens172

[ubuntu:~ ] # ls /run/systemd/network/                  # auto generate systemd script
[ubuntu:~ ] # ls /usr/share/doc/netplan/examples/       # setup example
```

```bash
[ubuntu:~ ] # systemd-resolve --status

[ubuntu:~ ] # resolvectl status
[ubuntu:~ ] # resolvectl dns
```

---

## gui

### oxrg

```bash
[ubuntu:~ ] # apt install xorg
[ubuntu:~ ] # X -configure
[ubuntu:~ ] # mv xorg.conf.new /etc/X11/xorg.conf
```

### lightdm

```bash
[ubuntu:~ ] # systemctl start lightdm
[ubuntu:~ ] # systemctl enable lightdm
[ubuntu:~ ] # systemctl status lightdm
```

### xfce

```bash
[ubuntu:~ ] # apt install xfce4
[ubuntu:~ ] # startxfce4
```

### i3wm

```bash
[ubuntu:~ ] # apt install i3
[ubuntu:~ ] # startx /usr/bin/i3
```

$HOME/.config/i3

$mod + ENTER : open terminal

$mod + Shift + q : closing application window

$mod + Shift + e : exit i3

$mod + Shift + space : float window

$mod + j : left

$mod + k : down

$mod + l : up

$mod + ; : right

$mod + e : split vertical / horizontal

$mod + w : tab

$mod + s : stack

---

## development

### openjdk

```bash
[ubuntu:~ ] # apt install openjdk-11-jdk
```

---

## terminal

### zsh

```bash
[ubuntu:~ ] # apt install zsh
```

---

## timedate

```bash
[ubuntu:~ ] # timedatectl set-ntp true
[ubuntu:~ ] # timedatectl set-timezone UTC
[ubuntu:~ ] # vi /etc/systemd/timesyncd.conf
[Time]
NTP=clock.stdtime.gov.tw
FallbackNTP=ntp.ubuntu.com
RootDistanceMaxSec=5
PollIntervalMinSec=32
PollIntervalMaxSec=2048

[ubuntu:~ ] # systemctl restart systemd-timesyncd.service
```

1. systemd-timedated (系統時間管理服務)

這是一個設定與管理導向的服務。

- 核心作用：它是系統時間設定的「單一入口」。當你執行 timedatectl 指令（例如修改時區、手動改時間、開啟/關閉 NTP）時，timedatectl 就會發送訊號給 systemd-timedated 來執行修改。
- 按需啟動 (On-Demand)：為了節省系統資源，這個服務平時是關閉的（Inactive）。只有當有人執行 timedatectl 或有程式透過 D-Bus 請求修改時間設定時，它才會自動啟動，閒置一段時間後又會自動關閉。
- 管理範圍：
  - 管理系統時區（Timezone，對應 /etc/localtime）。
  - 管理硬體時鐘（RTC / Hardware Clock）是要使用 UTC 還是本地時間（Local Time）。
  - 控制是否啟用網路時間同步（NTP）。

2. systemd-timesyncd (網路時間同步服務)

這是一個執行導向的輕量級 NTP 用戶端 (Client)。

- 核心作用：它專職負責透過網路（NTP 協定）同步時間。它會定期向設定好的 NTP 伺服器（例如你日誌中的 10.206.96.100）發送請求，校正本機系統時間，防止時鐘變慢或變快（Time Drift）。
- 常駐執行 (Daemon)：只要你在 timedatectl 中開啟了 NTP 同步（set-ntp true），這個服務就會一直保持在後台運行（Active/Running）。
- 特殊機制（儲存時間點）：為了防止系統離線太久或突然斷電導致時間大倒退，它會定期把當前時間寫入硬碟（/var/lib/systemd/timesync/clock）。開機時如果連不上網路，它會先讀取這個檔案，確保系統時間「至少不會早於上一次關機的時間」。
- 定位：它只是一個用戶端，不是 NTP 伺服器，無法提供時間給區網內的其他電腦。

3. 兩者協同工作

輸入 timedatectl timesync-status 時

- 運作流程如下：
  1. 指令 → 觸發 systemd-timedated 啟動。
  2. systemd-timedated 透過系統 D-Bus 總線，向正在後台運行的 systemd-timesyncd 詢問：「目前的 NTP 同步詳細狀態（如延遲、抖動等）」。
  3. systemd-timesyncd 回傳資料 → systemd-timedated 整合後顯示在螢幕上。

4. 兩者狀態組合

| Service           | Status               | Why                                                       |
| ----------------- | -------------------- | --------------------------------------------------------- |
| systemd-timedated | disabled (or static) | 有人在背後呼叫 timedatectl 時才會短暫醒來，平時都在睡覺。 |
| systemd-timesyncd | enabled / running    | 必須 24 小時在背景不間斷地維護網路時間同步。              |
