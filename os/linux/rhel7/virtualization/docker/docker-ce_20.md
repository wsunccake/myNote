# docker-ce 20.x

## install

```bash
centos:~ # yum remove docker docker-client docker-client-latest docker-common \
    docker-latest docker-latest-logrotate docker-logrotate docker-engine
centos:~ # yum install -y yum-utils
centos:~ # yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
centos:~ # yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```


---

## service

```bash
centos:~ # systemctl enable docker.service --now
centos:~ # docker version
centos:~ # docker run hello-world
```