# buildroot

## package

```bash
debian:~ # apt install rsync

debian:~ # tar zxf buildroot-2023.02.tar.gz
debian:~ # cd buildroot-2023.02
debian:~/buildroot-2023.02 # ls configs
```

---

## arm

```bash
debian:~/buildroot-2023.02 # make qemu_arm_vexpress_defconfig
debian:~/buildroot-2023.02 # make menuconfig
debian:~/buildroot-2023.02 # make [-j <cpu number>]

# exec
debian:~/buildroot-2023.02 # /output/images/start-qemu.sh
```
