# 5 - Raspberry Pi OS os 2025 03 15

## content

- [install](#install)
- [system](#system)
  - [config](#config)
  - [service](#service)
  - [apt](#apt)
- [cli](#cli)

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

---

## system

### config

```bash
rpios:~ # raspi-config
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
