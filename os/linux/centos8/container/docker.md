# docker

## install

```bash
[centos:~ ] # dnf autoremove podman runc docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-engine
[centos:~ ] # dnf autoremove podman runc containerd.io buildah skopeo runc

[centos:~ ] # dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
[centos:~ ] # dnf install docker-ce --nobest
[centos:~ ] # systemctl enable docker --now

# allow user run docker
[centos:~ ] # usermod -aG docker <user>
```


---

## config

```bash
[centos:~ ] # vi /etc/docker/daemon.json
{
        "bip": "10.253.42.1/16",

//  ipv6
//      "ipv6": true,

//  graph
//      "graph": "/home/docker",

//  for device mappe
//      "storage-opts":["dm.basesize=50G", "dm.loopdatasize=200G", "dm.loopmetadatasize=10G"],
}
```


---

## issue

### dns no working

centos 8 default firewall use nftables not iptables, docker 19 still not support.

`method 1`

```bash
[centos:~ ] # vi /etc/firewalld/firewalld.conf
FirewallBackend=nftables
->
FirewallBackend=iptables

[centos:~ ] # systemctl restart firewalld
```

`method 2`

```bash
[centos:~ ] # firewall-cmd --get-active-zones
[centos:~ ] # firewall-cmd --get-zone-of-interface=docker0

[centos:~ ] # firewall-cmd --permanent --zone=public --add-interface=docker0
[centos:~ ] # firewall-cmd --permanent --direct --add-rule ipv4 filter INPUT 4 -i docker0 -j ACCEPT
[centos:~ ] # firewall-cmd --permanent --direct --add-rule ipv6 filter INPUT 6 -i docker0 -j ACCEPT
[centos:~ ] # firewall-cmd --permanent --zone=public --add-masquerade

[centos:~ ] # firewall-cmd --reload

[centos:~ ] # systemctl restart docker

# if docker service start to fail, then firewall issue
[centos:~ ] # firewall-cmd --zone=trusted --change-interface=docker0 --permanent 
[centos:~ ] # firewall-cmd --zone=trusted --add-masquerade --permanent
[centos:~ ] # firewall-cmd --zone=docker --remove-interface=docker0
```
