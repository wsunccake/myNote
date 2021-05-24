# minikube

## install

### update

```bash
[ubuntu:~ ] # apt-get update
[ubuntu:~ ] # apt-get install apt-transport-https
[ubuntu:~ ] # apt-get upgrade
```

install [kvm](./kvm.md)

install [docker-ce](./docker.md)


### kubectl

```bash
[ubuntu:~ ] # curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl

[ubuntu:~ ] # chmod +x kubectl
[ubuntu:~ ] # mv kubectl  /usr/local/bin/
[ubuntu:~ ] # kubectl version -o json 
```


### docker-machine

```bash
[ubuntu:~ ] # curl -LO https://storage.googleapis.com/minikube/releases/latest/docker-machine-driver-kvm2

[ubuntu:~ ] # chmod +x docker-machine-driver-kvm2
[ubuntu:~ ] # mv docker-machine-driver-kvm2 /usr/local/bin/
[ubuntu:~ ] # docker-machine-driver-kvm2 version
```

### minikube

```bash
[ubuntu:~ ] # wget https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
[ubuntu:~ ] # chmod +x minikube-linux-amd64
[ubuntu:~ ] # mv minikube-linux-amd64 /usr/local/bin/minikube

[ubuntu:~ ] # newgrp libvirt
[ubuntu:~ ] # usermod -aG libvirt <user>

[ubuntu:~ ] # minikube config set vm-driver kvm2
```
