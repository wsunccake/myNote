# minikube

## install

install kvm

install [docker](./container/docker.md)


### kubectl

```bash
[centos:~ ] # curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl

[centos:~ ] # chmod +x kubectl
[centos:~ ] # mv kubectl  /usr/local/bin/
[centos:~ ] # kubectl version -o json 
```


### docker-machine

```bash
[centos:~ ] # curl -LO https://storage.googleapis.com/minikube/releases/latest/docker-machine-driver-kvm2

[centos:~ ] # chmod +x docker-machine-driver-kvm2
[centos:~ ] # mv docker-machine-driver-kvm2 /usr/local/bin/
[centos:~ ] # docker-machine-driver-kvm2 version
```


### minikube

```bash
[centos:~ ] # wget https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
[centos:~ ] # chmod +x minikube-linux-amd64
[centos:~ ] # mv minikube-linux-amd64 /usr/local/bin/minikube

[centos:~ ] # usermod -aG libvirt <user>
[centos:~ ] # minikube config set vm-driver kvm2

[centos:~ ] # su - <user>
[centos:~ ] $ minikube start
```


---

## usage

```bash
[centos:~ ] $ minikube start
[centos:~ ] $ cat $HOME/.minikube/machines/minikube/config.json
[centos:~ ] $ minikube stop
[centos:~ ] $ minikube delete
[centos:~ ] $ minikube ssh

[centos:~ ] $ minikube addons list
[centos:~ ] $ minikube dashboard
[centos:~ ] $ minikube dashboard --url

minikube config set memory 16384

```

```bash
[centos:~ ] $ kubectl cluster-info
[centos:~ ] $ kubectl config view
[centos:~ ] $ kubectl get nodes
[centos:~ ] $ kubectl get pods
[centos:~ ] $ kubectl get deployments
[centos:~ ] $ kubectl get services
[centos:~ ] $ kubectl get events
[centos:~ ] $ kubectl config view
```


---

## demo

```
[centos:~ ] $ kubectl create ns demo
[centos:~ ] $ kubectl -n demo create deployment hello-minikube --image=k8s.gcr.io/echoserver:1.4
[centos:~ ] $ kubectl -n demo expose deployment hello-minikube --type=NodePort --port=8080
[centos:~ ] $ kubectl -n demo get services hello-minikube
[centos:~ ] $ kubectl -n demo port-forward service/hello-minikube 7080:8080
[centos:~ ] $ curl http://localhost:7080/

[centos:~ ] $ kubectl delete ns demo
```
