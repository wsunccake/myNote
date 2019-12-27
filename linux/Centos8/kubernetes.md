# kubernetes 1.17


## prepare

### selinux

```bash
centos:~ # sed -i 's/SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
centos:~ # reboot
```


### hosts

```bash
centos:~ # vi /etc/hosts
192.168.31.200	master
192.168.31.201	node1
192.168.31.202	node2
192.168.31.203	node3
...
```


### ntp / chronyc

```bash
centos:~ # chronyc -a makestep
centos:~ # chronyc -a 'burst 4/4'
```


### firewall

```bash
centos:~ # firewall-cmd --permanent --add-port=6443/tcp
centos:~ # firewall-cmd --permanent --add-port=2379-2380/tcp
centos:~ # firewall-cmd --permanent --add-port=10250/tcp
centos:~ # firewall-cmd --permanent --add-port=10251/tcp
centos:~ # firewall-cmd --permanent --add-port=10252/tcp
centos:~ # firewall-cmd --permanent --add-port=10255/tcp
centos:~ # firewall-cmd --reload
```


### docker

```bash
centos:~ # dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
centos:~ # dnf install docker-ce --nobest
centos:~ # systemctl enable --now docker

# forwarding
centos:~ # vi /lib/systemd/system/docker.service
[Service]
...
ExecStartPost=/sbin/iptables -I FORWARD -s 0.0.0.0/0 -j ACCEPT

centos:~ # systemctl daemon-reload
centos:~ # systemctl restart docker
```


### kubernetes

```bash
centos:~ # cat << EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

centos:~ # dnf install iproute-tc ipvsadm
centos:~ # dnf install kubelet kubeadm kubectl --disableexcludes=kubernetes
centos:~ # systemctl enable --now kubelet

# sysctl
centos:~ # cat << EOF >  /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
vm.swappiness = 0
EOF

centos:~ # sysctl --system

# disable swap
centos:~ # swapoff -a
centos:~ # vi /etc/fstab
# remove swap
```


---

## config

### master

master 必須做過 prepare 步驟

```bash
# init kube
master:~ # kubeadm config images pull
master:~ # kubeadm init --pod-network-cidr 10.244.0.0/16
master:~ # mkdir -p $HOME/.kube
master:~ # cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
master:~ # chown $(id -u):$(id -g) $HOME/.kube/config

# other
## auto completion
master:~ # dnf install bash-completion
master:~ # echo "source <(kubectl completion bash)" >> ~/.bashrc

## token id
master:~ # kubeadm token list

## ca hash
master:~ # openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'

master:~ # kubectl -n kube-system get cm kubeadm-config -oyaml
```


### network

[Installing Addons](https://kubernetes.io/docs/concepts/cluster-administration/addons/)

`flannel`

```bash
master:~ # kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
## config: /etc/cni/net.d/10-flannel.conflist,  /run/flannel/subnet.env
## container: kube-flannel
## nic: flannel

master:~ # wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
master:~ # 
kind: ConfigMap
apiVersion: v1
...
  net-conf.json: |
    { 
      "Network": "10.244.0.0/16",  # 可成自訂的 --pod-network-cidr
      "Backend": {
        "Type": "vxlan"
      }
    }
...

apiVersion: apps/v1
kind: DaemonSet
        command:
        - /opt/bin/flanneld
        args:
        - --ip-masq
        - --kube-subnet-mgr
        - --iface=<eth>  # 可指定 nic

# forwarding
master:~ # iptables -P FORWARD ACCEPT
node:~ # iptables -P FORWARD ACCEPT
```


`calico`

```bash
master:~ # wget https://docs.projectcalico.org/v3.8/manifests/calico.yaml
master:~ # sed -i 's@192.168.0.0/16@10.244.0.0/16@' calico.yaml
master:~ # kubectl apply -f calico.yaml
## config: /etc/cni/net.d/10-calico.conflist, /etc/cni/net.d/calico-kubeconfig
## container: calico
```


### node

node 必須做過 prepare 步驟

```bash
node:~ # kubeadm join <master_ip>:6443 --token <token_id> --discovery-token-ca-cert-hash sha256:<ca_hash>
```


### tip

```bash
# reset master
master:~ # rm -rf $HOME/.kube
master:~ # rm -rf /etc/cni/net.d/*
master:~ # kubeadm reset

# reset node
master:~ # kubectl delete node <node>
node:~ # rm -rf $HOME/.kube
node:~ # rm -rf /etc/cni/net.d/*
node:~ # kubeadm reset

# debug
master:~ # kubectl -n <namespace> describe pod <pod>
master:~ # kubectl -n <namespace> logs <pod> -c <container>
master:~ # kubectl -n <namespace> exec <pod> [-c <container>] -it <cmd>
```


### question

1. coredns READY,  是因為有可能是因為網路尚未設定, 只要將 network plugin 裝起來即可

```bash
master:~ # kubectl get pods --all-namespaces -o wide
NAMESPACE     NAME                           READY   STATUS
kube-system   coredns-6955765f44-dnmxh       0/1     ContainerCreating
kube-system   coredns-6955765f44-r56gm       0/1     ContainerCreating
kube-system   etcd-master                    1/1     Running
kube-system   kube-apiserver-master          1/1     Running
kube-system   kube-controller-manager-master 1/1     Running
kube-system   kube-proxy-wkqx9               1/1     Running
kube-system   kube-scheduler-master          1/1     Running

master:~ # journalctl -f
Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady messa>
Unable to update cni config: no networks found in /etc/cni/net.d
```


2. network plugin 會產生新的 nic, 所以在 reset 或 apple/delete 要去注意

```bash
master:~ # ip link show
1: lo: <LOOPBACK,UP,LOWER_UP>
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP>
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP>

# ie, flannel
master:~ # ip link show
1: lo: <LOOPBACK,UP,LOWER_UP>
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP>
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP>
4. flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> 
```


---

## app

```bash
# name space
master:~ # kubectl get namespace
master:~ # kubectl create namespace <namespace>
master:~ # kubectl delete namespace <namespace>

# list
master:~ # kubectl get nodes       [-o wide] [--all-namespaces]
master:~ # kubectl get pods        [-o wide] [--all-namespaces]
master:~ # kubectl get deployments [-o wide] [--all-namespaces]
master:~ # kubectl get services    [-o wide] [--all-namespaces]
master:~ # kubectl get replicasets [-o wide] [--all-namespaces]
master:~ # kubectl describe nodes        [--all-namespaces]
master:~ # kubectl describe pods         [--all-namespaces]
master:~ # kubectl describe deployments  [--all-namespaces]
master:~ # kubectl describe services     [--all-namespaces]
master:~ # kubectl describe replicasets  [--all-namespaces]

# create app
master:~ # kubectl run hello-world --image=gcr.io/google-samples/node-hello:1.0 --port=<container_port>
master:~ # kubectl expose deployment hello-world --external-ip=<mater_ip>|<node_ip> --port=<external_port> --target-port=<container_port> --type=NodePort

# delete app
master:~ # kubectl delete service hello-world
master:~ # kubectl delete deployment hello-world
```


### example

```bash
master:~ # kubectl create namespace demo
master:~ # kubectl -n demo run hello-world --image=gcr.io/google-samples/node-hello:1.0 --port=8080
master:~ # kubectl -n demo get pods
master:~ # kubectl -n demo get deployments

master:~ # kubectl -n demo expose deployment hello-world --external-ip=192.168.31.200 --port=80 --target-port=8080 --type=NodePort
master:~ # curl http://192.168.31.200
master:~ # kubectl -n demo exec hello-world -it bash

master:~ # kubectl -n demo delete service hello-world
master:~ # kubectl -n demo delete deployment hello-world
master:~ # kubectl delete namespace demo
```


---

## helm 2.16

```bash
# check kube info
master:~ # kubectl config current-context
master:~ # kubectl cluster-info
master:~ # cat ~/.kube/config

# prepare kube account and role
## serviceaccount
master:~ # kubectl get serviceaccount --all-namespaces
master:~ # kubectl -n kube-system create serviceaccount tiller
## clusterrole
master:~ # kubectl get clusterrole --all-namespaces
master:~ # kubectl create clusterrolebinding tiller-cluster-admin --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
## patch
master:~ # kubectl -n kube-system get clusterrole cluster-admin -o yaml
master:~ # kubectl -n kube-system patch deploy tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'


# install
master:~ # curl https://get.helm.sh/helm-v2.16.0-linux-amd64.tar.gz -o helm-v2.16.0-linux-amd64.tar.gz
master:~ # tar zxf helm-v2.16.0-linux-amd64.tar.gz
master:~ # mv linux-amd64/helm /usr/local/bin/

# init
master:~ # helm init --history-max 200
## config: $HOME/.helm
## conatienr: tiller-deploy
master:~ # helm reset

# repo
master:~ # helm repo update
master:~ # helm repo list
master:~ # helm repo add <repo> <url>
master:~ # helm repo remove <repo>
master:~ # helm search repo <pkg>

## ie
master:~ # helm repo add stable https://kubernetes-charts.storage.googleapis.com/

# environment variable
master:~ # kubectl -n kube-system describe pod tiller-deploy
# get the <helm_ip>, <helm_port>
# [env HELM_HOST=<helm_ip>:<helm_port>] 

# usage
master:~ # helm search <chart>
master:~ # helm list
master:~ # helm install <serivce>
master:~ #helm delete <serivce>

## ie
master:~ # kubectl create namespace demo
master:~ # helm search mysql
master:~ # helm install stable/mysql --namespace demo
master:~ # kubectl get services --all-namespaces
master:~ # helm delete --purge washed-squid-mysql
master:~ # kubectl delete namespace demo
```

---

## istio


```bash
master:~ # curl -L https://github.com/istio/istio/releases/download/1.4.2/istio-1.4.2-linux.tar.gz -o istio-1.4.2-linux.tar.gz
master:~ # tar zxf istio-1.4.2-linux.tar.gz
master:~ # mv istio-1.4.2/bin/istioctl /usr/local/bin/

master:~ # for psp in $(kubectl get psp -o jsonpath="{range .items[*]}{@.metadata.name}{'\n'}{end}"); do
  if [ $(kubectl auth can-i use psp/$psp --as=system:serviceaccount:default:default) = yes ]; then
    kubectl get psp/$psp --no-headers -o=custom-columns=NAME:.metadata.name,CAPS:.spec.allowedCapabilities
  fi
done

# create config
master:~ # istioctl manifest apply --set profile=demo
master:~ # kubectl -n istio-system get pods
master:~ # kubectl -n istio-system get services

# deploy app
master:~ # kubectl label namespace <namespace> istio-injection=enabled      # auto inject
master:~ # kubectl create -n <namespace> -f <app>.yaml
master:~ # istioctl kube-inject -f <app>.yaml | kubectl apply -f -          # manual inject

# ie
master:~ # kubectl create namespace bookinfo
master:~ # kubectl label namespace bookinfo istio-injection=enabled
master:~ # kubectl describe namespace bookinfo
master:~ # kubectl -n bookinfo apply -f istio-1.4.2/samples/bookinfo/platform/kube/bookinfo.yaml
master:~ # kubectl -n bookinfo get services
master:~ # kubectl -n bookinfo get pods

master:~ # kubectl -n bookinfo exec -it $(kubectl -n bookinfo get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}') -c ratings -- curl productpage:9080/productpage | grep -o "<title>.*</title>"

master:~ # kubectl -n bookinfo apply -f istio-1.4.2/samples/bookinfo/networking/bookinfo-gateway.yaml
master:~ # kubectl -n bookinfo get gateway

master:~ # kubectl -n istio-system get services istio-ingressgateway -o wide
master:~ # kubectl -n istio-system get services istio-ingressgateway -o json

master:~ # export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
master:~ # export INGRESS_HOST=<master_ip>
master:~ # curl -s http://$INGRESS_HOST:$INGRESS_PORT/productpage
```
