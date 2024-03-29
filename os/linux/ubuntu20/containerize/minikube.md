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
[ubuntu:~ ] # mv kubectl /usr/local/bin/
[ubuntu:~ ] # kubectl version -o json

[ubuntu:~ ] # apt-get install bash-completion
[ubuntu:~ ] # kubectl completion bash > /etc/bash_completion.d/kubectl

# for user
[ubuntu:~ ] $ echo 'source <(kubectl completion bash)' >>~/.bashrc
[ubuntu:~ ] $ echo 'alias k=kubectl' >>~/.bashrc
[ubuntu:~ ] $ echo 'complete -F __start_kubectl k' >>~/.bashrc
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
```

---

## setup

```bash
[ubuntu:~ ] $ virt-host-validate

[ubuntu:~ ] $ minikube config set vm-driver kvm2
[ubuntu:~ ] $ minikube config set memory 16384
[ubuntu:~ ] $ minikube config set cpus 2
[ubuntu:~ ] $ minikube config get vm-driver
[ubuntu:~ ] $ minikube config get memory 16384
[ubuntu:~ ] $ minikube config get cpus

[ubuntu:~ ] $ minikube start

# export minikube env to docker
[ubuntu:~ ] $ eval $(minikube -p minikube docker-env)
```

---

## test

```bash
# create deployment
[ubuntu:~ ] $ kubectl create deployment hello-node --image=k8s.gcr.io/echoserver:1.4
[ubuntu:~ ] $ kubectl get deployments
[ubuntu:~ ] $ kubectl get pods
[ubuntu:~ ] $ kubectl get events
[ubuntu:~ ] $ kubectl config view

# create service
[ubuntu:~ ] $ kubectl expose deployment hello-node --type=LoadBalancer --port=8080
[ubuntu:~ ] $ kubectl get services
[ubuntu:~ ] $ kubectl get services -o yaml
[ubuntu:~ ] $ kubectl patch svc/hello-node -p '{"spec": {"type": "LoadBalancer"}}'
[ubuntu:~ ] $ kubectl edit svc/hello-node
[ubuntu:~ ] $ minikube service hello-node   # serivce type must be LoadBalancer

# enable addons
[ubuntu:~ ] $ minikube addons list
[ubuntu:~ ] $ minikube addons enable metrics-server
[ubuntu:~ ] $ kubectl get pod,svc -n kube-system

# disable addons
[ubuntu:~ ] $ minikube addons disable metrics-server

# clean up
[ubuntu:~ ] $ kubectl delete service hello-node
[ubuntu:~ ] $ kubectl delete deployment hello-node
[ubuntu:~ ] $ minikube stop
[ubuntu:~ ] $ minikube delete
```

---

## addons

### dashboard

```bash
[ubuntu:~ ] $ minikube addons enable dashboard
[ubuntu:~ ] $ minikube dashboard [--url]
```

### ingress

```bash
[ubuntu:~ ] $ minikube addons enable ingress
[ubuntu:~ ] $ cat << EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: example
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$1
spec:
  rules:
  - host: <host name>
    http:
      paths:
      - path: /(.*|$)
        backend:
          serviceName: <service name>
          servicePort: 80
EOF
[ubuntu:~ ] $ kubectl get ing
```

### dns

```bash
[ubuntu:~ ] $ minikube addons enable ingress
[ubuntu:~ ] $ minikube addons enable ingress-dns
[ubuntu:~ ] $ kubectl edit configmap coredns -n kube-system
```
