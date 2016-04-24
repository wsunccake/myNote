l# Install

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
sh-4.3 # locale-gen
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

----


# Pakcage

## Upgrade

```
arch:~ # pacman -Syy
arch:~ # pacman -Su
```

## Remove package_group

```
arhc:~ # pacman -Qg | awk '/^package_group/{print $2}' | xargs -i pacman -Rs --noconfirm {}
```


## Essential Packages

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

rpm -ivh pkg = pacman -U pkg

rpm -ql pkg = pacman -Ql pkg


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

----


# Network

## netctl

```
arch:~ # cp /etc/netctl/examples/connect_profile /etc/netctl/my_interface_profile

arch:~ # netctl list
arch:~ # netctl start my_interface_profile
arch:~ # netctl enable my_interface_profile

arch:~ # netctl stop my_interface_profile
arch:~ # netctl disable my_interface_profile
```

# Sound

## ALSA

```
arch:~ # pacman -S alsa-utils 
arch:~ # alsamixer
```

## PulseAudio

```
arch:~ # pacman -S pulseaudio
arch:~ # pacman -S pulseaudio-alsa
```

----


# Service

## SSH

```
arch:~ # pacman -S openssh
arch:~ # systemctl enable sshd.service
```

----


# CLI

## gpm

```
arch:~ # pacman -S gpm
arch:~ # systemctl enable gpm.service
arch:~ # systemctl start gpm.service
```


## zsh

```
arhc:~ # pacman -S zsh zsh-completions

arhc:~ # yaourt oh-my-zsh-git
arhc:~ # cp /usr/share/oh-my-zsh/zshrc ~/.zshrc

arhc:~ # yaourt oh-my-zsh-powerline-theme-git
arhc:~ # vi ~/.zshrc
...
ZSH_THEME="powerline"
```

----

# CLI Application

## ScreenFetch

```
arch:~ # pacman -S screenfetch
arch:~ # echo /usr/bin/screenfetch >> /etc/bash.bashrc
```


----


# GUI

## X window

```
arch:~ # pacman -S xorg-server xorg-xinit xorg-utils xorg-server-utils mesa
arch:~ # pacman -S xorg-twm xterm xorg-xclock
arch:~ # pacman -S ttf-dejavu  ttf-droid  ttf-inconsolata
arch:~ # pacman -Ss xf86-video
arch:~ # pacman -S xf86-video-vesa
arch:~ # X -configure
arch:~ # cp xorg.conf.new /etc/X11/xorg.conf.d/xorg.conf

arch:~ # xdpyinfo
arch:~ # xrandr --output VGA-0 --mode 1024x768 --rate 60
```


## SDDM

```
arch:~ # pacman -S sddm
arch:~ # sddm --example-config > /etc/sddm.conf

arch:~ # pacman -S archlinux-themes-sddm
arch:~ # vi /etc/sddm.conf
...
[Theme]
# Current theme name
#Current=maui
Current=archlinux-soft-grey
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

## Chinese Font

```
arch:~ # locale-gen zh_TW
arch:~ # yaourt ttf-tw
```


## Chinese Input Method

```
arch:~ # pacman -S ibus
arch:~ # pacman -S ibus-chewing

arch:~ # ibus-daemon
arch:~ # ibus engine
arch:~ # ibus restart

arch:~ # cat ~/.bashrc
...
export GTK_IM_MODULE=ibus
export XMODIFIERS=@im=ibus
export QT_IM_MODULE=ibus
```

----


# GUI Application


## Cairo-Dock

```
arch:~ # pacman -S cairo-dock cairo-dock-plug-ins
```


## Guake

```
arch:~ # pacman -S guake
```


## Sublime Text

```
arch:~ # yaourt sublime-text-dev
```

## IntelliJ

```
arch:~ # yaourt intellij-idea-ultimate-edition
```


## VNC

```
arch:~ # yaourt tigervnc

arch:~ # vncserver   # start server
arch:~ # vncserver   # stop server

arch:~ # cat ~/.vnc/xstartup
#!/bin/sh

exec startxfce4
```

----


# VM

virtualbox-guest-utils:
pacman -S virtualbox-guest-utils virtualbox-guest-modules virtualbox-guest-modules-lts virtualbox-guest-dkms



http://www.cs.columbia.edu/~jae/4118-LAST/arch-setup-2015-1.html