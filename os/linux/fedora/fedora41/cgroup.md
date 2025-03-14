# cgroup

## cgroup v2

### install

```bash
linux:~ # dnf install stress                # for rhel / fedora
linux:~ # apt install                       # for debian / ubuntu

# valid cgroup v2
linux:~ # test -f /sys/fs/cgroup/cgroup.controllers && echo "cgroup v2"
linux:~ # cat /sys/fs/cgroup/cgroup.controllers
cpuset cpu io memory hugetlb pids rdma
linux:~ # mount -t cgroup2
```

### usage

#### control group

```bash
linux:~ # ls -l /sys/fs/cgroup

# enable the desired controllers.
linux:~ # echo "+cpu" >> /sys/fs/cgroup/cgroup.subtree_control
linux:~ # echo "+cpuset" >> /sys/fs/cgroup/cgroup.subtree_control

linux:~ # mkdir -p /sys/fs/cgroup/Example
linux:~ # tree /sys/fs/cgroup/Example
/sys/fs/cgroup/Example
├── cgroup.controllers
├── cgroup.events
├── cgroup.freeze
├── cgroup.kill
├── cgroup.max.depth
├── cgroup.max.descendants
├── cgroup.pressure
├── cgroup.procs
├── cgroup.stat
├── cgroup.subtree_control
├── cgroup.threads
├── cgroup.type
├── cpu.idle
├── cpu.max
├── cpu.max.burst
├── cpu.pressure
├── cpuset.cpus
├── cpuset.cpus.effective
├── cpuset.cpus.exclusive
├── cpuset.cpus.exclusive.effective
├── cpuset.cpus.partition
├── cpuset.mems
├── cpuset.mems.effective
├── cpu.stat
├── cpu.stat.local
├── cpu.uclamp.max
├── cpu.uclamp.min
├── cpu.weight
├── cpu.weight.nice
├── io.bfq.weight
├── io.latency
├── io.max
├── io.pressure
├── io.prio.class
├── io.stat
├── io.weight
├── irq.pressure
├── memory.current
├── memory.events
├── memory.events.local
├── memory.high
├── memory.low
├── memory.max
├── memory.min
├── memory.numa_stat
├── memory.oom.group
├── memory.peak
├── memory.pressure
├── memory.reclaim
├── memory.stat
├── memory.swap.current
├── memory.swap.events
├── memory.swap.high
├── memory.swap.max
├── memory.swap.peak
├── memory.zswap.current
├── memory.zswap.max
├── memory.zswap.writeback
├── pids.current
├── pids.events
├── pids.events.local
├── pids.max
└── pids.peak

1 directory, 63 files

linux:~ # echo "+cpu +cpuset" >> /sys/fs/cgroup/Example/cgroup.subtree_control
linux:~ # echo "50000 100000" > /sys/fs/cgroup/Example/cpu.max
linux:~ # while true; do echo > /dev/null ; done &
linux:~ # echo $! > /sys/fs/cgroup/Example/cgroup.procs
linux:~ # echo <PID> > /sys/fs/cgroup/Example/cgroup.procs

linux:~ # find /sys/fs/cgroup/ -name cgroup.procs -exec cat {} \;

linux:~ # rmdir /sys/fs/cgroup/Example
```

#### child control group

```bash
# create control group
linux:~ # mkdir -p /sys/fs/cgroup/Example
# create child control group
linux:~ # mkdir -p /sys/fs/cgroup/Example/{g1,g2,g3}
# adjust CPU weight
linux:~ # echo "150" > /sys/fs/cgroup/Example/g1/cpu.weight
linux:~ # echo "100" > /sys/fs/cgroup/Example/g2/cpu.weight
linux:~ # echo "50" > /sys/fs/cgroup/Example/g3/cpu.weight
# setup pid
linux:~ # echo "<pid1>" > /sys/fs/cgroup/Example/g1/cgroup.procs
linux:~ # echo "<pid2>" > /sys/fs/cgroup/Example/g2/cgroup.procs
linux:~ # echo "<pid3>" > /sys/fs/cgroup/Example/g3/cgroup.procs
```

### systemd

| 方法            | 適用場景      | 設定方式                            |
| --------------- | ------------- | ----------------------------------- |
| systemd.scope   | 單次/臨時進程 | systemd-run --scope -p CPUQuota=50% |
| systemd.service | 應用程式      | /etc/systemd/system/myapp.service   |
| systemd.slice   | 系統層級管理  | /etc/systemd/system/mygroup.slice   |

#### systemd.scope

```bash
linux:~ # systemd-run --scope -p CPUQuota=50% -p MemoryMax=500M stress --cpu 2
```

#### systemd.service

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My CGroup Limited Service
After=network.target

[Service]
ExecStart=/usr/bin/stress --cpu 2
CPUQuota=50%
MemoryMax=500M
IOWeight=100
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
linux:~ # vi /etc/systemd/system/myapp.service

linux:~ # systemctl daemon-reload
linux:~ # systemctl enable myapp.service
linux:~ # systemctl start myapp.service

linux:~ # systemctl status myapp.service
linux:~ # ls /sys/fs/cgroup/system.slice/myapp.service/
linux:~ # cat /sys/fs/cgroup/system.slice/myapp.service/cgroup.procs

linux:~ # systemctl set-property myapp.service CPUWeight=300
linux:~ # systemd-cgls
linux:~ # systemd-cgtop

linux:~ # systemctl stop myapp.service
linux:~ # systemctl disable myapp.service
linux:~ # rm /etc/systemd/system/myapp.service
linux:~ # systemctl daemon-reload
```

#### systemd.slice

```ini
# /etc/systemd/system/mygroup.slice
[Slice]
CPUQuota=50%
MemoryMax=500M
```

```bash
linux:~ # vi /etc/systemd/system/mygroup.slice

linux:~ # systemctl start mygroup.slice
linux:~ # systemctl enable mygroup.slice
linux:~ # systemctl status mygroup.slice

linux:~ # systemctl daemon-reexec
```

```ini
# /etc/systemd/system/mytask.service
[Unit]
Description=My CGroup Limited Service
After=network.target

[Service]
Slice=mygroup.slice
ExecStart=/usr/bin/stress --cpu 2
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
linux:~ # linux:~ # vi /etc/systemd/system/mytask.service

linux:~ # systemctl start mytask.slice
linux:~ # systemctl enable mytask.slice
linux:~ # systemctl status mytask.slice
```

---

## cgroup v1

### install

```bash
linux:~ # dnf install libcgroup-tools       # for rhel / fedora
linux:~ # apt install cgroup-tools          # for debian / ubuntu

linux:~ # dnf install stress                # for rhel / fedora
linux:~ # apt install                       # for debian / ubuntu
```

### command

```bash
# list cg
linux:~ # lscgroup

# create cg
linux:~ # cgcreate -g cpu,memory:/mygroup
linux:~ # ls /sys/fs/cgroup/mygroup

# detele cg
linux:~ # cgdelete -g cpu,memory:/mygroup

# set limit
linux:~ # cgset -r cgset -r cpu.max="50000 100000" mygroup

# set process
linux:~ # cgexec -g cpu:/mygroup stress --cpu 1
linux:~ # while true; do echo > /dev/null ; done &
linux:~ # cgclassify -g cpu:/mygroup $!
linux:~ # cgclassify -g cpu:/mygroup <PID>
linux:~ # cat /sys/fs/cgroup/mygroup/cgroup.procs
```

### cgconfig.service

```bash
linux:~ # systemctl enable --now cgconfig
linux:~ # systemctl status cgconfig
linux:~ # systemctl disable --now cgconfig

linux:~ # cat /etc/cgconfig.conf
```

```ini
# /etc/cgconfig.conf
group mygroup {
    cpu {
        cpu.weight = 100;
    }
}
```
