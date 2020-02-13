# snap

## install

```bash
centos:~ # yum install epel-release
centos:~ # yum install snapd
centos:~ # systemctl enable --now snapd.socket
centos:~ # ln -s /var/lib/snapd/snap /snap
```


---

## usage

```bash
centos:~ # snap version

centos:~ # snap list
centos:~ # snap find <pkg>
centos:~ # snap install <pkg>
centos:~ # snap remove <pkg>
```
