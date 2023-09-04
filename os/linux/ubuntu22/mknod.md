# mknod

---

## content

- [syntax](#syntax)
- [pipeline](#pipeline)
- [device](#device)
  - [character](#character)
  - [block](#block)
- [ref](#ref)

---

## syntax

```bash
linux:~ # mknod [-m 664] <device> b|c <major> <minor>    # craete block / character device
linux:~ # mknod [-m 664] <device> p                      # craete pipeline
```

---

## pipeline

```bash
linux:~ # mknod /tmp/my-pipe p
linux:~ # ls -l /tmp/my-pipe
prw-r--r-- 1 root root ... my-pipe

# terminal 1
linux:~ # echo "date: $(date)" > /tmp/my-pipe

# terminal 2
linux:~ # cat /tmp/my-pipe
```

---

## device

### character

```bash
linux:~ # mknod /dev/my-char c 1 7
linux:~ # ls -l /dev/my-char
crw-r--r-- 1 root root 1, 7 ... /dev/my-char

linux:~ # echo "date: $(date)" > /dev/my-char
```

### block

```bash
linux:~ # mknod /dev/dvd-rom b 11 0
linux:~ # ls -l /dev/dvd-rom
brw-r--r-- 1 root root ... /dev/dvd-rom

linux:~ # mount /dev/dvd-rom /mnt
```

---

## ref

[devices](https://www.kernel.org/doc/Documentation/admin-guide/devices.txt)
