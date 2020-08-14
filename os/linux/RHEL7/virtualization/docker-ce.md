# Docker CE

## install

docker-ce 為 docker 1.7+ 之後版本

```bash
# remove previous version
centos:~ # yum autoremove docker

# install
centos:~ # yum install -y yum-utils device-mapper-persistent-data lvm2
centos:~ # yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
centos:~ # yum makecache
centos:~ # yum list docker-ce --showduplicates | sort -r
centos:~ # yum install docker-ce

# user
centos:~ # usermod -aG docker <user>

# config file
# docker 1.7+ 之後使用 /etc/dokcer/daemon.json 去設定, 不使用 /etc/sysconfig/docker-xxx

centos:~ # vi /etc/docker/daemon.json
{
  "live-restore": true,
  "insecure-registries": ["172.16.1.123:5000"],
  "group": "docker",

  "bip": "192.168.1.5/24",
  "fixed-cidr": "192.168.1.5/25",
  "fixed-cidr-v6": "2001:db8::/64",
  "mtu": 1500,
  "default-gateway": "10.20.1.1",
  "default-gateway-v6": "2001:db8:abcd::89",
  "dns": ["10.20.1.2","10.20.1.3"]
}

# service
centos:~ # systemctl enable --now docker
```

## firewall

```bash
centos:~ # firewall-cmd --permanent --zone=public --add-masquerade
centos:~ # firewall-cmd --reload
```
