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

---

## nsenter

```bash
linux:~ # lsns

linux:~ # nsenter --target <pid> --mount --pid --net --uts --ipc <cmd>
```

---

## ip

### network namespace

```bash
linux:~ # ip netns list                                     # list namespace
linux:~ # ip netns add <net_ns>                             # create namespace
linux:~ # ip netns delete <net_ns>                          # delete namespace

linux:~ # ip link set <veth> netns <net_ns>                 # veth to namespace
linux:~ # ip netns exec <net_ns> <ip_cmd>                   # exec veth in namespace
```

### bridge

```bash
linux:~ # ip [-d] link show [type bridge|dev <br>]          # list bridge
linux:~ # ip link add <br> type bridge                      # create bridge
linux:~ # ip link delete <br>                               # delete bridge

linux:~ # ip link set <br> up                               # up bridge
linux:~ # ip link set <veth> master <br>                    # attach veth to bridge
linux:~ # ip link set <veth> nomaster                       # detach veth to bridge
```

### veth pair

```bash
linux:~ # ip link add veth0 type veth peer name veth1       # create veth pair
linux:~ # ip link delete veth0                              # delete veth pair
linux:~ # ip [-d] link show
...
4: veth1@veth0:
5: veth0@veth1:
# 在相同 namespace 裡, veth1@veth0 表示 veth0 <-> veth1

5: veth0@if11:
# 在不相同 namespace 裡, veth0@if12 表示 veth0 <-> if12

linux:~ # ip link set veth0 up
linux:~ # ip link set veth0 master br0                  # attach veth to bridge
linux:~ # ip link set veth0 nomaster                    # detach veth to bridge

linux:~ # ip link set veth1 up
linux:~ # ip link set veth1 netns ns                    # attach to namespace
linux:~ # ip netns exec ns ip link show                 # list in namespace
linux:~ # ip netns exec ns ip link set veth1 netns 1    # attch veth to default namespace
```
