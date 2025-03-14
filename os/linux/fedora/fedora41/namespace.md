# namespace

## unshare

```bash
# check linux support "User Namespace"
# y: support, n: no support
linux:~ # grep CONFIG_USER_NS /boot/config-*

# check unshare permit
# for debian / ubuntu
linux:~ # echo 1 | sudo tee /proc/sys/kernel/unprivileged_userns_clone
# for rhel / fedora
linux:~ # setcap cap_sys_admin+ep /usr/bin/unshare

# run
linux:~ $ unshare -m -u -n -p --fork --mount-proc /bin/bash
```

```bash
# show namespace
linux:~ # lsns

# setns

# show process namespace
linux:~ # ls -l /proc/<pid>/ns/
```

### script

```bash
#!/bin/bash

set -e

if [ "$1" == "run" ]; then
    # 使用 unshare 建立新的 UTS、PID 和 Mount namespace
    unshare --uts --pid --mount-proc --fork --mount bash "$0" child "${@:2}"
elif [ "$1" == "child" ]; then
    # 確保 rootfs 存在
    if [ ! -d "rootfs" ]; then
        echo "Error: rootfs directory not found"
        exit 1
    fi

    # 掛載 rootfs
    mount --bind rootfs rootfs
    mkdir -p rootfs/oldrootfs
    pivot_root rootfs rootfs/oldrootfs
    cd /

    # 執行指定的指令
    exec "${@:2}"
else
    echo "Usage: $0 run <command> [args...]"
    exit 1
fi
```

```bash
linux:~ # docker create --name busybox busybox
linux:~ # mkdir rootfs
linux:~ # docker export busybox | tar -C rootfs -xvf -

linux:~ # bash main.sh run /bin/sh
```

## nsenter

```bash
linux:~ # lsns

linux:~ # nsenter --target <pid> --mount --pid --net --uts --ipc <cmd>
```
