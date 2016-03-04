# Install

## partition

使用 fdisk/parted 分割硬碟


## install package

```
root@arhciso:~ # vi /etc/pacman.d/mirrorlist
root@arhciso:~ # pacstrap -i /mnt base
root@arhciso:~ # genfstab -U /mnt >> /mnt/etc/fstab
```

## chroot

```
root@arhciso:~ # arch-chroot /mnt /bin/bash
sh-4.3 # echo "LANG=en_US.UTF-8" > /etc/locale.conf
sh-4.3 # tzselect
sh-4.3 # ln -s /usr/share/zoneinfo/Asia/Taipei /etc/localtime
sh-4.3 # hwclock -w
sh-4.3 # mkinitcpio -p linux
sh-4.3 # pacman -S grub
sh-4.3 # grub-install /dev/sda
sh-4.3 # grub-mkconfig -o /boot/grub/grub.cfg
sh-4.3 # echo "arch" > /etc/hostname
sh-4.3 # password
sh-4.3 # exit
root@arhciso:~ # reboot
```

# Pakcage

## essential packages

```
arch:~ # pacman -S net-tools pkgfile base-devel
arch:~ # pacman -S vim emacs
arch:~ # pacman -S bash-completion
```

|function 		| 	yum 		| 	pacman 	|
|---------------| --------------| ----------|
|install 		| install pkg 	| -S pkg 	|
|search remote 	| search pkg 	| -Ss pkg 	|
|group list 	| grouplist 	| -Sg 		|
|uninstall 		| remove 		| -R pkg 	|
|installed 		| 				| -Qs 		|


# Service

## SSH

```
arch:~ # pacman -S openssh
arch:~ # systemctl enable sshd.service
```

# GUI

## X window

```
arch:~ # pacman -S xorg-server xorg-xinit xorg-utils xorg-server-utils mesa
arch:~ # pacman -S xorg-twm xterm xorg-xclock
arch:~ # pacman -S ttf-dejavu  ttf-droid  ttf-inconsolata
arch:~ # X -configure
arch:~ # cp xorg.conf.new /etc/X11/xorg.conf.d/xorg.conf

arch:~ # xdpyinfo
arch:~ # xrandr --output VGA-0 --mode 1024x768 --rate 60
```

## Xfce

```
arch:~ # pacman -S xfce4 xfce4-goodies
arch:~ # startxfce4
```


## KDE

```
arch:~ # pacman -S plasma  (DE)
arch:~ # pacman -R plasma-mediacenter
arch:~ # pacman -S kde-applications
arch:~ # pacman -S sddm    (DM)
arch:~ # systemctl enable sddm.service
arch:~ # systemctl start sddm.service

arch:~ # sddm --example-config > /etc/sddm.conf
# Maximum user id for displayed users
#MaximumUid=60000
MaximumUid=0

# Minimum user id for displayed users
#MinimumUid=1000
MinimumUid=0

arch:~ # echo "startkde" >> .xinitrc
```


# GUI Application


## Cairo-Dock

```
arch:~ # pacman -S cairo-dock cairo-dock-plug-ins
```


## Guake

```
arch:~ # pacman -S guake
```


# Package


## ABS (Arch Build System)

```
# install
arch:~ # pacman -S abs
arch:~ # abs   # /var/abs
arch:~ # vi /etc/abs.conf

# usage
arch:~ # cp -r /var/abs/core/pkg .
arch:~ # cd pkg
arch:~ # sudo -u nobody makepkg -s
arch:~ # makepkg -sri --skippgpcheck
arch:~ # pacman -U pkg.tar.xz
```

## AUR (Arch User Repository)

https://aur.archlinux.org


## Yaourt

```
# install
arch:~ # git clone https://aur.archlinux.org/package-query.git
arch:~ # cd package-query
arch:~ # makepkg -si

arch:~ # git clone https://aur.archlinux.org/yaourt.git
arch:~ # cd yaourt
arch:~ # makepkg -si

# usage
arch:~ # yaourt pkg     # search
arch:~ # yaourt -G pkg  # download PKGBUILD
arch:~ # yaourt -Sb pkg # download and compile
```

# VM

virtualbox-guest-utils:
pacman -S virtualbox-guest-utils virtualbox-guest-modules virtualbox-guest-modules-lts virtualbox-guest-dkms



http://www.cs.columbia.edu/~jae/4118-LAST/arch-setup-2015-1.html