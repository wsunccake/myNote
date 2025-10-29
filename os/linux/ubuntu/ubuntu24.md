# ubuntu 24.04

---

## content

- [cli](#cli)
- [network](#network)
- [service](#service)
  - [ssh](#sshd)
  - [gnome-remote-desktop](#gnome-remote-desktop)

---

## cli

```bash
ubuntu:~ # apt install git
ubuntu:~ # apt install neovim
```

---

## gui

### DM

```bash
ubuntu:~ $ ps aux | grep -E 'gdm|lightdm|sddm|xdm'

# check tty / session
ubuntu:~ $ loginctl
ubuntu:~ $ loginctl show-session
ubuntu:~ $ loginctl show-session $(loginctl | grep tux | awk '{print $1}')
```

| COMMAND   | Display Manager | often      |
| --------- | --------------- | ---------- |
| `gdm3`    | GDM             | GNOME      |
| `lightdm` | LightDM         | XFCE, MATE |
| `sddm`    | SDDM            | KDE        |
| `xdm`     | XDM             | X-window   |

```bash
# restart display manager
ubuntu:~ # systemctl restart gdm3

ubuntu:~ # systemctl isolate multi-user.target
ubuntu:~ # systemctl isolate graphical.target
```

### GNOME setting

```bash
# 使用 GUI 設定
ubuntu:~ $ gnome-control-center [privacy]
Privacy & Security -> Screen Lock
```

```bash
# 使用 CLI 設定
ubuntu:~ $ gsettings list-recursively org.gnome.desktop.session
org.gnome.desktop.session idle-delay uint32 300
org.gnome.desktop.session session-name 'ubuntu'

ubuntu:~ $ gsettings list-recursively org.gnome.desktop.lockdown
org.gnome.desktop.lockdown disable-application-handlers false
org.gnome.desktop.lockdown disable-command-line false
org.gnome.desktop.lockdown disable-lock-screen false
org.gnome.desktop.lockdown disable-log-out false
org.gnome.desktop.lockdown disable-print-setup false
org.gnome.desktop.lockdown disable-printing false
org.gnome.desktop.lockdown disable-save-to-disk false
org.gnome.desktop.lockdown disable-show-password false
org.gnome.desktop.lockdown disable-user-switching false
org.gnome.desktop.lockdown mount-removable-storage-devices-as-read-only false
org.gnome.desktop.lockdown user-administration-disabled false
```

| item                                           | value    | description                                                         |
| ---------------------------------------------- | -------- | ------------------------------------------------------------------- |
| `idle-delay`                                   | `300`    | 在 **300 sec 不操作**後，會進入 **idle**，螢幕變暗或觸發螢幕鎖定。  |
| `session-name`                                 | `ubuntu` | 目前啟用的 session 名稱                                             |
| `disable-application-handlers`                 | `false`  | **應用程式** 處理程序運作（例如點選連結或檔案時呼叫預設處理程式）。 |
| `disable-command-line`                         | `false`  | **命令列工具** 或 **命令列相關功能**，不會禁用命令列操作。          |
| `disable-lock-screen`                          | `false`  | **螢幕鎖定** 功能運作，使用者在閒置時或手動啟動時，系統可鎖定螢幕。 |
| `disable-log-out`                              | `false`  | **使用者登出** ，目前未禁用登出功能。                               |
| `disable-print-setup`                          | `false`  | **使用者訪問** 及 **印表機和相關印表** 設定。                       |
| `disable-printing`                             | `false`  | **列印功能** ，使用者可以執行列印動作。                             |
| `disable-save-to-disk`                         | `false`  | **儲存檔案到磁碟** ，不會限制使用者儲存文件。                       |
| `disable-show-password`                        | `false`  | **顯示密碼內容** （例如在密碼欄位旁顯示明文選項），未被禁用。       |
| `disable-user-switching`                       | `false`  | **換使用者帳戶** ，未限制快速切換帳戶功能。                         |
| `mount-removable-storage-devices-as-read-only` | `false`  | **可攜式儲存設備** 以讀寫模式掛載，並非只讀。                       |
| `user-administration-disabled`                 | `false`  | **使用者管理動作** （如新增/刪除使用者），未限制這項功能。          |

```bash
#!/bin/bash

# unlock-screen.sh

enable() {
    gsettings set org.gnome.desktop.session idle-delay 0
    gsettings set org.gnome.desktop.screensaver idle-activation-enabled false
    gsettings set org.gnome.desktop.screensaver lock-enabled false
    gsettings set org.gnome.desktop.lockdown disable-lock-screen true
}

disable() {
    gsettings set org.gnome.desktop.session idle-delay 300
    gsettings set org.gnome.desktop.screensaver idle-activation-enabled true
    gsettings set org.gnome.desktop.screensaver lock-enabled true
    gsettings set org.gnome.desktop.lockdown disable-lock-screen false
}

$1
```

```bash
ubuntu:~ $ chmod +x unlock-screen.sh

ubuntu:~ $ ./lock-screen.sh enable
ubuntu:~ $ ./lock-screen.sh disable
```

```bash
# ~/.config/autostart/disable-lock.desktop
[Desktop Entry]
Type=Application
Exec=/home/$USER/unlock-screen.sh enable
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Disable Screen Lock
Comment=Disable idle lock and screensaver
```

---

## network

netplan.io

```bash
ubuntu:~ # dpkg -l netplan.io

ubuntu:~ # vi /etc/netplan/50-cloud-init.yaml
network:
    ethernets:
      ens192:
        dhcp4: no
        addresses:
          - 192.168.10.10/24
        nameservers:
          addresses:
            - 8.8.8.8
        routes:
          - to: 0.0.0.0/0
            via: 192.168.10.254
    version: 2

ubuntu:~ # netplan try
ubuntu:~ # netplan apply
ubuntu:~ # netplan ip leases ens192
```

---

## service

### sshd

```bash
ubuntu:~ # apt install openssh-server

ubuntu:~ # systemctl enable|disable ssh
ubuntu:~ # systemctl start|stop     ssh
ubuntu:~ # systemctl status         ssh
```

### gnome-remote-desktop

```bash
ubuntu:~ $ gnome-control-center [system]
System -> Remote Desktop
Enable
Desktop Share
Remote Control
```

---

## develop

### node

```bash
ubuntu:~ $ curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash
ubuntu:~ $ sudo apt-get install -y nodejs
```

### gemini cli

```bash
ubuntu:~ $ sudo npm install -g @google/gemini-cli

ubuntu:~ $ gemini
```