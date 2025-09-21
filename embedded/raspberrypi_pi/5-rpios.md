# 5 - Raspberry Pi OS os 2025 03 15

## content

- [5 - Raspberry Pi OS os 2025 03 15](#5---raspberry-pi-os-os-2025-03-15)
  - [content](#content)
  - [install](#install)
  - [system](#system)
    - [config](#config)
    - [service](#service)
    - [apt](#apt)
  - [cli](#cli)
  - [python](#python)

---

## install

[Operating system images](https://www.raspberrypi.com/software/operating-systems/)

```bash
host:~ # lsblk                  # if sdX is sd card
host:~ # wipefs -a /dev/sdX
host:~ # xzcat raspios-arm64-full.img.xz | dd of=/dev/sdX bs=4M status=progress conv=fsync
host:~ # sync
```

```bash
rpios:~ # mount /dev/sdX1 /mnt
rpios:~ # touch /mnt/ssh

rpios:~ # vi /mnt/wpa_supplicant.conf
country=TW
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="ssid"
    psk="password"
}
```

```bash
rpios:~ # loginctl
rpios:~ # loginctl show-session <session_id> | grep -i type
# check x11 or wayland
rpios:~ # echo $XDG_SESSION_TYPE

# add hdmi sound card
rpios:~ # echo "hdmi_drive=2" >> /boot/firmware/config.txt
rpios:~ # reboot

rpios:~ # pactl list sinks
rpios:~ # alsamixer
```

```bash
rpios:~ # apt-get install fcitx5 fcitx5-configtool
rpios:~ # apt-get install fcitx5-chewing                              # 酷音輸入法
rpios:~ # apt-get install ttf-wqy-microhei ttf-wqy-zenhei xfonts-wqy  # 中文字型
rpios:~ # im-config
```

---

## system

### config

```bash
rpios:~ # raspi-config
# 於 Interface Options 中可以設定 ssh, rpi-connect, vnc
# 於 Advanced Options
```

```bash
rpios:~ # iwconfig wlan0
wlan0     IEEE 802.11  ESSID:"8DA0"
          Mode:Managed  Frequency:5.54 GHz  Access Point: 11:22:33:44:55:66
          Bit Rate=292.5 Mb/s   Tx-Power=31 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:on # 省電模式, 一段時間沒使用會自動停
          Link Quality=52/70  Signal level=-58 dBm
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:0  Invalid misc:0   Missed beacon:0

rpios:~ # iw dev wlan0 set power_save off

rpios:~ # nmcli device
rpios:~ # nmcli connect
rpios:~ # nmcli connection edit <connect_name>
nmcli> print
nmcli> set 802-11-wireless.powersave 2
# 0: default
# 1: ignore
# 2: disable
# 3: enable
nmcli> save
nmcli> quit
```

### service

```bash
rpios:~ # systemctl status ssh
rpios:~ # systemctl start ssh
rpios:~ # systemctl stop ssh
rpios:~ # systemctl enable ssh
rpios:~ # systemctl disable ssh

rpios:~ # systemctl status avahi-daemon
rpios:~ # systemctl start avahi-daemon
rpios:~ # systemctl stop avahi-daemon
rpios:~ # systemctl enable avahi-daemon
rpios:~ # systemctl disable avahi-daemon
```

### apt

```bash
# update software
rpios:~ # apt update
rpios:~ # apt full-upgrade

# search software
rpios:~ # apt search <pkg>
rpios:~ # apt-cache show <pkg>

# install / uninstall
rpios:~ # apt install <pkg>
rpios:~ # apt remove <pkg>

# manage disk usage
rpios:~ # apt clean
```

---

## cli

```bash
rpios:~ # apt install neovim
```

## python

```bash
rpios:~ # apt install python3-venv
rpios:~ # apt install python3-virtualenv
rpios:~ # apt install python3-virtualenvwrapper
```
