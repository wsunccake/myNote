# NFS

## content

- [server](#server)
  - [server - package](#server---package)
  - [server - config](#server---config)
  - [server - daemon](#server---daemon)
  - [server - other](#server---other)
- [client](#client)
  - [client - package](#client---package)
  - [client - config](#client---config)
  - [client - other](#client---other)

---

## server

### server - package

```bash
nfs:~ # zypper in nfs-kernel-server
nfs:~ # zypper in yast2-nfs-server
```

### server - config

```bash
# config by yast
nfs:~ # yast nfs_server

# config file
nfs:~ # vi /etc/export
/fs1	*(ro,root_squash,sync,subtree_check)
/fs2	192.168.1.0/24(rw,no_root_squash,async,no_subtree_check)
```

ro/rw, sync/async, root_squash/no_root_squash, all_squash

### server - daemon

```bash
nfs:~ # systemctl start nfs-server
nfs:~ # systemctl enable nfs-server

# test
nfs:~ # showmount -e <nfs_ip>
```

### server - other

```bash
nfs:~ # cat /proc/fs/nfs/exports
nfs:~ # cat /var/lib/nfs/rmtab
```

---

## client

### client - package

```bash
fs:~ # zypper in nfs-client
fs:~ # zypper in yast2-nfs-client
```

### client - config

```bash
# config by yast
fs:~ # yast nfs

# config file
fs:~ # vi /etc/fstab
...
<nfs>:/fs                    /fs   nfs   defaults  0  0

# mount nfs
fs:~ # mount -a
fs:~ # mount -t nfs -o proto=tcp,port=2049 <nfs_ip>:/fs /fs
```

### client - other

```bash
fs:~ # cat /proc/mounts
```
