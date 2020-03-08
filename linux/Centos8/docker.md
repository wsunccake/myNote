# docker

## install

```bash
centos:~ # dnf autoremove podman

centos:~ # dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
centos:~ # dnf install docker-ce --nobest
centos:~ # systemctl enable docker --now
```


---

## config

```bash
centos:~ # vi /etc/docker/daemon.json
{
        "bip": "10.253.42.1/16",

//  graph
//      "graph": "/home/docker"

//  for device mappe
//      "storage-opts":["dm.basesize=50G", "dm.loopdatasize=200G", "dm.loopmetadatasize=10G"]
}
```
