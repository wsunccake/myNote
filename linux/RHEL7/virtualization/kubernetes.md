# Kubernetes


## Install

Kubernetes 安裝可使用 source code, binary 或是執行 container 的方式

### Binary


####  all hosts

`install basic package`

```
centos:~ # yum install -y epel-release
centos:~ # yum install -y bash-completion
centos:~ # yum install -y ntp
```


`resovle host`

```
centos:~ # vi /etc/hosts
192.168.31.200	master
192.168.31.201	node1
192.168.31.202	node2
192.168.31.203	node3
```


`stop firewall`

```
centos:~ # systemctl stop firewalld
centos:~ # systemctl disable firewalld
```


`enable ntp`

```
centos:~ # systemctl start ntpd
centos:~ #systemctl enable ntpd
```


`disable selinux`

```
centos:~ # vi /etc/selinux/conf
SELINUX=disabled

centos:~ # reboot
```

----


#### master

`install package`

```
master:~ # yum -y install etcd kubernetes
```


`setup etcd`

```
master:~ # vi /etc/etcd/etcd.conf
ETCD_NAME=default
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379"
ETCD_ADVERTISE_CLIENT_URLS="http://localhost:2379"
```


`setup api server`

```
master:~ # vi /etc/kubernetes/apiserver
KUBE_API_ADDRESS="--address=0.0.0.0"
KUBE_API_PORT="--port=8080"
KUBELET_PORT="--kubelet_port=10250"
KUBE_ETCD_SERVERS="--etcd_servers=http://master:2379"
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"
KUBE_ADMISSION_CONTROL="--admission_control=NamespaceLifecycle,NamespaceExists,LimitRanger,SecurityContextDeny,ResourceQuota"
KUBE_API_ARGS=""
```


`restart service`

```
master:~ # systemctl restart etcd
master:~ # systemctl enable etcd

master:~ # systemctl restart kube-apiserver
master:~ # systemctl enable kube-apiserver

master:~ # systemctl restart kube-controller-manager
master:~ # systemctl enable kube-controller-manager

master:~ # systemctl restart kube-scheduler
master:~ # systemctl enable kube-scheduler
```


`set kubenetes network`

```
master:~ # etcdctl mkdir /kube-centos/network
master:~ # etcdctl mk /kube-centos/network/config '{"Network":"172.17.0.0/16"}'
master:~ # etcdctl mk /kube-centos/network/config '{"Network": "172.30.0.0/16", "SubnetLen": 24, "Backend": {"Type": "vxlan"} }'
master:~ # etcdctl ls /kube-centos/network/config
master:~ # etcdctl get /kube-centos/network/config
master:~ # etcdctl rm /kube-centos/network/config 
```

----


#### node

`install package`

```
node:~ # yum -y install flannel kubernetes
```


`setup flannel`

```
node:~ # vi /etc/sysconfig/flanneld
FLANNEL_ETCD_ENDPOINTS="http://master:2379"
FLANNEL_ETCD_PREFIX="/kube-centos/network"
```


`setup kubelet`

```
node:~ # vi /etc/kubernetes/config
KUBE_MASTER="--master=http://master:8080"

node:~ # vi /etc/kubernetes/kubelet
KUBELET_ADDRESS="--address=0.0.0.0"
KUBELET_PORT="--port=10250"
# change the hostname to this host’s IP address
KUBELET_HOSTNAME="--hostname_override=node1"
KUBELET_API_SERVER="--api_servers=http://master:8080"
KUBELET_ARGS=""
```


`restart service`

```
node:~ # systemctl restart kube-proxy
node:~ # systemctl enable kube-proxy

node:~ # systemctl restart kubelet
node:~ # systemctl enable kubelet

node:~ # systemctl restart docker
node:~ # systemctl enable docker

node:~ # systemctl restart flanneld
node:~ # systemctl enable flanneld
```

`check node network`

```
node:~ # ip a | grep flannel | grep inet
```


### Container


#### all hosts

流程同上 Install via Binary 的 all hosts 部分, 還需要另外安裝 docker 跟設定 kubernetes repository

`install docker and kubeadm`

```
centos:~ # vi /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg
       https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg

centos:~ # yum install -y docker kubelet kubeadm kubectl kubernetes-cni

centos:~ # systemctl restart docker
centos:~ # systemctl docker

centos:~ # vi /etc/sysctl.d/bridge-nf-call-iptables.conf
net.bridge.bridge-nf-call-iptables=1
net.bridge.bridge-nf-call-ip6tables=1
centos:~ # sysctl -p /etc/sysctl.d/bridge-nf-call-iptables.conf
centos:~ # cat /proc/sys/net/bridge/bridge-nf-call-iptables

centos:~ # systemctl restart kubelet
centos:~ # systemctl enable kubelet
```

----


#### master

`auto completion`

```
master:~ # echo "source <(kubectl completion bash)" >> ~/.bashrc
```

`setup master`

```
master:~ # kubeadm reset
master:~ # kubeadm init [--token 1234] [--pod-network-cidr 10.244.0.0/16] [--service-cidr 10.96.0.0/12]
master:~ # kubeadm token list
```

network module 使用 flannel, 需要設定 --pod-network-cidr, 否則 kube-dns 會有問題

`config file`

```
master:~ # mkdir -p $HOME/.kube
master:~ # cp /etc/kubernetes/admin.conf $HOME/.kube/config
```

`install flannel`

```
master:~ # kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
master:~ # kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel-rbac.yml

kubectl get pod --all-namespaces -o wide
```

#### node

`join master`

```
node:~ # echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables
node:~ # kubeadm reset
node:~ # kubeadm join --token 3a88f0.e98c25d025e85412 masater:6443
```


## PWK/Play With K8S

http://labs.play-with-k8s.com/


`master`

```
master:~ # kubeadm init --apiserver-advertise-address $(hostname -i)
master:~ # kubectl apply -n kube-system -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
master:~ # curl -L -s https://git.io/kube-dashboard  | sed 's/targetPort: 9090/targetPort: 9090\n  type: LoadBalancer/' | kubectl apply -f -

master:~ # kubectl run -it busybox --image=busybox --restart=Never

master:~ # kubectl run busybox --image=busybox --restart=Never --command -- sleep 3600
master:~ # kubectl exec -it busybox /bin/sh

master:~ # vi busybox.yaml
apiVersion: v1
kind: Pod
metadata:
  name: busybox
  namespace: default
spec:
  containers:
  - image: busybox
    command:
      - sleep
      - "3600"
    imagePullPolicy: IfNotPresent
    name: busybox
  restartPolicy: Always
master:~ # kubectl create -f busybox.yaml
```


`node`

```
node:~ # kubeadm join --token ba7efe.e1db8bd85e84f340 10.0.32.3:6443
```


## Hello World

```
# create app
master:~ # kubectl run hello-world --image=gcr.io/google-samples/node-hello:1.0 --port=8080
master:~ # kubectl get node
master:~ # kubectl get pod
master:~ # kubectl get deployment
master:~ # kubectl get service
master:~ # kubectl get replicaset
master:~ # kubectl describe node
master:~ # kubectl describe pod
master:~ # kubectl describe deployment
master:~ # kubectl describe service
master:~ # kubectl describe replicaset

master:~ # kubectl get pod --all-namespaces -o wide
master:~ # curl `kubectl get pod -o wide | awk '/hello/{print $6}'`:8080

# replica app
master:~ # kubectl scale deployments/hello-world --replicas=4

# expose app
master:~ # kubectl expose deployment hello-world [--external-ip=192.168.31.200] [--port=80] [--target-port=8080] [--type=NodePort]
# type: Cluster, LoadBalancer, NodePort
# Cluster 只能對內; LoadBalancer 是透過 IaaS 環境拿到 IP; NodePort 是手動指定 IP
# external-ip: 設定對外, ip 要在 kubernetes host 上 (master 或 node 都可)
master:~ # kubectl get service --all-namespaces -o wide
master:~ # curl `kubectl get service | awk '/hello/{print $2}'`:8080

# delete app
master:~ # kubectl delete service hello-world
master:~ # kubectl delete deployment hello-world
```


## Pod

```
master:~ # vi pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello
  labels:
    app: hello-world
spec:
  containers:
  - name: hello
    image: gcr.io/google-samples/node-hello:1.0
    ports:
    - containerPort: 8080

master:~ # kubectl create -f pod.yaml
master:~ # kubectl delete -f pod.yaml
```


## Namespace

```
# 使用 cli
master:~ # kubectl create namespace new-namespace

# 使用 config
master:~ # vi namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: new-namespace

mater:~ # kubectl create -f namespace.yaml

master:~ # kubectl get configmap  -n=kube-public
master:~ # kubectl delete namespaces new-namespace
```


## Deployment

```
# 使用 cli
master:~ # kubectl run hello-world --image=nginx:1.7.9 --port=80

# 使用 config
master:~ # vi deployment.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  template:
    metadata:
      labels:
        run: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80

mater:~ # kubectl create -f deployment.yaml
mater:~ # kubectl delete -f deployment.yaml

# scaling
master:~ # kubectl scale deployment nginx-deployment --replicas 10
master:~ # kubectl autoscale deployment nginx-deployment --min=10 --max=15 --cpu-percent=80

# rolling update
master:~ # kubectl set image deployment/nginx-deployment nginx=nginx:1.9.1
master:~ # kubectl rollout status deployment/nginx-deployment
master:~ # kubectl rollout history deployment/nginx-deployment
master:~ # kubectl rollout undo deployment/nginx-deployment [--to-revision=2]
master:~ # kubectl rollout pause deployment/nginx-deployment
master:~ # kubectl rollout resume deployment/nginx-deployment
```

## Service


ClusterIP, NodePort, LoadBalancer, ExternalName

```
# 使用 cli
master:~ # kubectl expose deployment nginx --port 8080 --target-port 80 [--external-ip 10.240.0.9]
# port: service external port
# target-port: container forwarding port
# external-ip: service external ip

# 使用 config
master:~ # vi service.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  template:
    metadata:
      labels:
        run: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  labels:
    run: nginx
  name: nginx
  namespace: default
spec:
#  externalIPs:
#  - 10.240.0.9
  ports:
  - port: 8080
    protocol: TCP
    targetPort: 80
  selector:
    run: nginx
# Service spec.selector.run must equal Deployment spec.template.labels.run
  sessionAffinity: None
  type: ClusterIP

mater:~ # iptable -L -nv -t nat
```



## Manage

`basic infomation`

```
master:~ # kubectl --help
master:~ # kubectl options
master:~ # kubectl version
master:~ # kubectl version --help

master:~ # kubectl cluster-info
```


`node`

```
master:~ # kubectl get nodes          # list nodes
master:~ # kubectl delete node node1  # remove node

node:~ # kubeadm join --token 3a88f0.e98c25d025e85412 masater:6443.  # join master
```


`pod`


## Reference

[Kubernetes指南](https://kubernetes.feisky.xyz/)

[Kubernetes學習筆記](https://gcpug-tw.gitbooks.io/kuberbetes-in-action/content/)

[Kubernetes 入門指南](http://kubernetes.kansea.com/docs/)

[kubectl-cheatsheet](https://kubernetes.io/docs/user-guide/kubectl-cheatsheet/)

[Installing Kubernetes Cluster with 3 minions on CentOS 7 to manage pods and services](https://severalnines.com/blog/installing-kubernetes-cluster-minions-centos7-manage-pods-services)
