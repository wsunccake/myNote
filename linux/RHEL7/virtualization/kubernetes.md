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


## Hello World

```
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

master:~ # kubectl expose deployment hello-world [--external-ip=192.168.31.200] [--port=80] [--target-port=8080] [--type=NodePort]
# type: Cluster, LoadBalancer, NodePort
# Cluster 只能對內; LoadBalancer 是透過 IaaS 環境拿到 IP; NodePort 是手動指定 IP
# external-ip: 設定對外, ip 要在 kubernetes host 上 (master 或 node 都可)
master:~ # kubectl get service --all-namespaces -o wide
master:~ # curl `kubectl get service | awk '/hello/{print $2}'`:8080

master:~ # kubectl delete service hello-world
master:~ # kubectl delete deployment hello-world
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

