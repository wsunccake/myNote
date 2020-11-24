# centos 8

## gnome3

after mini install, source from iso/image

```bash
centos:~ # mount -oloop CentOS-8.2.2004-x86_64-dvd1.iso /mnt
centos:~ # cp /mnt/media.repo /etc/yum.repos.d
centos:~ # vi /etc/yum.repos.d/media.repo
[AppStream]
name=AppStream
mediaid=None
metadata_expire=-1
gpgcheck=0
cost=500
baseurl=file:///mnt/AppStream

[BaseOS]
name=BaseOS
mediaid=None
metadata_expire=-1
gpgcheck=0
cost=500
baseurl=file:///mnt/BaseOS

centos:~ # yum makecache
centos:~ # yum repolist
centos:~ # dnf install @'Server with GUI'

centos:~ # systemctl set-default graphical
centos:~ # systemctl isolate graphical
```

## gnome3 tweak 

```bash
centos:~ # dnf install gnome-tweaks
```

[Tweaking GNOME Desktop Environment on CentOS 8](https://linuxhint.com/tweaking_gnome_desktop_centos8/)

[How to Show Desktop in GNOME](https://itsfoss.com/show-desktop-gnome-3/)


---

## software

```bash
centos:~ # dnf install epel-release

# openjdk
centos:~ # dnf install java-11-openjdk-devel

# git
centos:~ # dnf install git

# chrome
centos:~ # wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
centos:~ # dnf install google-chrome-stable_current_x86_64.rpm

# vscode
centos:~ # rpm --import https://packages.microsoft.com/keys/microsoft.asc
centos:~ # echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo
centos:~ # dnf check-update
centos:~ # dnf install code

# intellij idea
centos:~ # vi ~/.local/share/applications/idea.desktop
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

# /usr/share/applications/
# /usr/local/share/applications/
# ~/.local/share/applications
```
