# kernel panic

## content

- [boot option](#boot-option)
  - [recuse mode](#recuse-mode)
  - [recovery mode](#recovery-mode)
- [disk](#disk)
  - [status](#status)
  - [check or repair](#check-or-repair)
- [ram disk / initrd](#ram-disk--initrd)
  - [extract](#extract)
  - [rebuild](#rebuild)
- [boot loader - grub2](#boot-loader---grub2)
  - [config](#config)
  - [boot](#boot)
- [other](#other)

---

## boot option

```
Boot from Hard Disk   (可以進 hard disk 的 recovey mode)
Installation
Upgrade
More ...              (可以進 dvd 的 recuse mode)
```

```
Boot from Hard Disk
==>
xxx
Advanced option xxx -> recovery mode
==>
xxx
xxx (recovery ...)    (進入 recovery, 需要 root password, 盡可能 mount)
```

```
More ...
==>
Recuse System         (進入 recuse, 不需 root password)
Boot Linux System
Check Install Media
Memory Test
```

### recuse mode

```bash
# mount fs
recuse:~ # mount /dev/sda1 /mnt
recuse:~ # mount /dev/sda2 /mnt/boot

# change root
recuse:~ # chroot /mnt bash
```

### recovery mode

```bash
sles:~ # systemctl recuse | emergency
sles:~ # reboot
```

---

## disk

### status

```bash
recuse:~ # fdisk -l /dev/sd[X]
recuse:~ # parted -l /dev/sd[X]
recuse:~ # lsblk [-f|-l|-p]
recuse:~ # df -T
recuse:~ # bikid
```

### check or repair

```bash
recuse:~ # fsck -y -f /dev/sda1
recuse:~ # xfs_repair -L -v /dev/sda1
```

---

## ram disk / initrd

### extract

```bash
# show content
(chroot)recuse:~ # lsinitrd
(chroot)recuse:~ # lsinitrd -f /etc/ld.so.conf

# check initrd compress format
(chroot)recuse:~ # file /boot/initrd-<ver>
# gzip compressed data, ... -> gzip compressed
# XZ compressed data -> xz compressed
# LZ4 compressed data (v1.8+) -> lz4 compressed
# bzip2 compressed data, ... -> bzip2 compressed
# ASCII cpio archive (SVR4 with no CRC) -> uncompressed cpio archive:

# extract initrd
(chroot)recuse:~ # mkdir /tmp/intrd
(chroot)recuse:~ # cd /tmp/intrd
(chroot)recuse:/tmp/initrd #
(chroot)recuse:/tmp/initrd # zcat /boot/initrd-<ver> | cpio -idvm
(chroot)recuse:/tmp/initrd # xzcat /boot/initrd-<ver> | cpio -idvm
(chroot)recuse:/tmp/initrd # lz4 -d /boot/initrd-<ver> | cpio -idvm
(chroot)recuse:/tmp/initrd # cpio -idvm < /boot/initrd-<ver>
```

### rebuild

```bash
# rebuild init ramfs
(chroot)recuse:~ # dracut --force           # redhat / suse
(chroot)recuse:~ # update-initramfs -u      # debian / ubuntu
(chroot)recuse:~ # mkinitrd                 # old version
```

---

## boot loader - grub2

### config

```bash
(chroot)recuse:~ # grub2-mkconfig -o /boot/grub2/grub.cfg   # redhat / suse
(chroot)recuse:~ # update-grub                              # debian / ubuntu
(chroot)recuse:~ # reboot
```

```bash
grub> help
grub> set
grub> set pager=1       # less

grub> ls
grub> ls (hd0)          # (<disk>[, <partition name>])
grub> ls (hd0, gpt3)    # partition info
grub> ls (hd0, gpt3)/   #

grub> root (hd0, 1)     # set partition with /boot
```

### boot

```bash
# load module
grub> insmod xfs
grub> insmod lvm
grub> insmod btrfs

# on bios system
grub> set root=(hd0,gpt3)
grub> linux /vmlinuz-<ver> root=/dev/sda3 ro
grub> initrd /initrd-<ver>
# (hd0,gpt3) => /boot/vmlinuz-xxx, /boot/initrd-xxx,
# /dev/sda3  => /
grub> boot

# on uefi system
grub> set root=(hd0,gpt1)
grub> linux (hd0,gpt3)/vmlinuz-<ver> root=/dev/sda3 ro
grub> initrd (hd0,gpt3)/initrd-<ver>
# efi system partition => (hd0,gpt1)
# /dev/sda3  => /
grub> boot
```

---

## other

```bash
# detect bios or uefi system
recuse:~ # [ -d /sys/firmware/efi ] && echo UEFI || echo BIOS

# mount
recuse:~ # mount /dev/sd[X][n] /<mnt>
recuse:~ # umount [-lf] /<mnt>

# change root
recuse:~ # chroot <mnt> <cmd>

# remount to rw
recuse:~ # mount -o remount,rw /

# show journal / log
recuse:~ # journalctl -xb
```
