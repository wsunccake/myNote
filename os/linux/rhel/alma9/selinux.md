# selinux

## usage

```bash
# list selinux status
alma:~ # getenforce
alma:~ # sestatus

# switch Enforcing / Permissive
alma:~ # setenforce Enforcing
alma:~ # setenforce Permissive
```

---

## disable selinux

```bash
alma:~ # vi /etc/selinux/config
SELINUX=disabled
alma:~ # grubby --update-kernel ALL --args selinux=0 # update /etc/default/grub
alma:~ # reboot
```

---

## enable selinux

```bash
alma:~ # vi /etc/selinux/config
SELINUX=enforcing
alma:~ # grubby --update-kernel ALL --remove-args selinux # update /etc/default/grub
alma:~ # reboot
```
