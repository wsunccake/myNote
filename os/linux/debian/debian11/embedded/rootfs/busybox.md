# busybox

## package

```bash
# prepare
debian:~ # apt install libncurses-dev flex bison
debian:~ # apt install libssl-dev bc dwarves

# download
debian:~ # wget https://busybox.net/downloads/busybox-1.36.0.tar.bz2

debian:~ # tar jxf busybox-1.36.0.tar.bz2
debian:~ # cd busybox-1.36.0
```

---

## x86_64

```bash
debian:~ # ROOTFS_DIR=/home/rootfs

debian:~/busybox-1.36.0 # make menuconfig
settings  --->
  [ ] Enable compatibility for full-blown desktop systems (8kb)
  [*] Build static binary (no shared libs)
  (./_install) Destination path for 'make install'

# check flag
debian:~/busybox-1.36.0 # grep CONFIG_DESKTOP=n .config
debian:~/busybox-1.36.0 # grep CONFIG_STATIC=y .config
debian:~/busybox-1.36.0 # grep CONFIG_PREFIX= .config

# compile
debian:~/busybox-1.36.0 # make LDFLAGS=--static
debian:~/busybox-1.36.0 # make CONFIG_PREFIX=$ROOTFS_DIR install
```

---

## arm

---

## arm64
