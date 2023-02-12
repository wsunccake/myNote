# alma 9

## system

```bash
# epel
alma:~ # dnf clean all
alma:~ # dnf install epel-release -y
alma:~ # dnf update -y

# disable selinux
alma:~ # vi /etc/selinux/config
SELINUX=disabled
alma:~ # grubby --update-kernel ALL --args selinux=0 # update /etc/default/grub
alma:~ # reboot
```

---

## develop

```bash
# zsh
alma:~ # dnf install zsh -y

# java
alma:~ # dnf -y install java-1.8.0-openjdk-devel
alma:~ # dnf -y install java-11-openjdk-devel
alma:~ # dnf -y install java-17-openjdk-devel

# sdk
alma:~ # curl -s "https://get.sdkman.io" | bash

sdk install groovy 4.0.6
sdk install gradle 7.6
```

---

## vm / container

```bash
# docker
alma:~ # dnf -y remove podman runc
alma:~ # curl https://download.docker.com/linux/centos/docker-ce.repo -o /etc/yum.repos.d/docker-ce.repo
alma:~ # sed -i -e "s/enabled=1/enabled=0/g" /etc/yum.repos.d/docker-ce.repo
alma:~ # dnf --enablerepo=docker-ce-stable -y install docker-ce
```
