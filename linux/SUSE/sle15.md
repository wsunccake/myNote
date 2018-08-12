# SLE15

## Install

安裝時, 預設 filesystem 為 btrfs, 建議使用 xfs (效能較佳)


---

## Setup


`repository`

```bash
sel:~ # mount /dev/sr0 /mnt
sle:~ # zypper ar /mnt/Module-Basesystem Basesystem
```

`firewall`

```bash
sle:~ # firewall-cmd --add-service=ssh --permament
sle:~ # firewall-cmd --reload
```

`package`

```bash
sle:~ # zypper in vim
sle:~ # zypper in mlocate
sle:~ # zypper in iputils
sle:~ # zypper in -t pattern yast2_basis
```


