# nfs

## network topology

```
server          client
192.168.10.1    192.168.10.101
   |            |
   |            |
   +------------+                192.168.10.0/24
```

---

## server

### install

```bash
[server:~ ] # apt update
[server:~ ] # apt install nfs-kernel-server
[server:~ ] # cat /proc/fs/nfsd/versions

[server:~ ] # systemctl start nfs-kernel-server
[server:~ ] # systemctl enable nfs-kernel-server
[server:~ ] # systemctl status nfs-kernel-server
```

### config

```bash
[server:~ ] # cat /etc/default/nfs-kernel-server
[server:~ ] # cat /etc/default/nfs-common
```

### export fs

```bash
[server:~ ] # mkdir -p /data
[server:~ ] # vi /etc/exports
/data     192.168.10.0/24(rw,async,no_root_squash,no_subtree_check)

[server:~ ] # exportfs -ar
[server:~ ] # exportfs -v

[server:~ ] # showmount -e 192.168.10.1
```

---

## client

### install

```bash
[client:~ ] # apt update
[client:~ ] # apt install nfs-common
```

### mount

```bash
[client:~ ] # mkdir -p /data
[client:~ ] # showmount -e 192.168.10.1
[client:~ ] # mount -t nfs 192.168.10.1:/data /data
```

### fstab

```bash
[client:~ ] # vi /etc/fstab
192.168.10.1:/data /data nfs defaults,timeo=900 0 0

[client:~ ] # mount -a
```
