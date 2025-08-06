# selinux

SELinux / Security-Enhanced Linux

## usage

```bash
# list selinux status
alma:~ # getenforce
alma:~ # sestatus

# switch Enforcing / Permissive
alma:~ # setenforce Enforcing
alma:~ # setenforce Permissive

alma:~ $ ls -Z test.txt
-rw-r--r-- user1 user1 unconfined_u:object_r:user_home_t:s0 test.txt

alma:~ $ ls -l /etc/selinux/
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
