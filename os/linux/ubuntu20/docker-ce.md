# docker-ce

## install

```bash
[ubuntu:~ ] # snap remove docker
[ubuntu:~ ] # apt remove docker docker-engine docker.io containerd runc
[ubuntu:~ ] # apt update
[ubuntu:~ ] # apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
[ubuntu:~ ] # curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
[ubuntu:~ ] # apt-key fingerprint 0EBFCD88
[ubuntu:~ ] # add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
[ubuntu:~ ] # apt update
[ubuntu:~ ] # apt install docker-ce docker-ce-cli containerd.io
```


---

## service

```bash
[ubuntu:~ ] # systemctl start docker
[ubuntu:~ ] # systemctl enable docker
[ubuntu:~ ] # systemctl status docker

[ubuntu:~ ] # vi /etc/docker/daemon.json
{
    "log-level": "error",
    "storage-driver": "overlay2",
    "bip": "192.168.10.0/24"
}
[ubuntu:~ ] # systemctl restart docker

[ubuntu:~ ] # usermod -aG docker <user>
```
