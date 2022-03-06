# kubeadm

## network topology

```
master      worker
|           |
|           |
+-----------+
```

---

## prepare

### hosts

```bash
[ubuntu:~ ] # vi /etc/hosts
192.168.31.200	master
192.168.31.201	worker1
192.168.31.202	worker2
192.168.31.203	worker3
...
```


### swap

```bash
[ubuntu:~ ] # swapoff -a
[ubuntu:~ ] # vi /etc/fstab
# remove swap
[ubuntu:~ ] # swapon
```


### firewall

```bash
[ubuntu:~ ] # ufw status
[ubuntu:~ ] # ufw disable
[ubuntu:~ ] # systemctl disable ufw
```


### bridge traffic

```bash
# kernel module
[ubuntu:~ ] # cat << EOF | tee /etc/modules-load.d/k8s.conf
br_netfilter
overlay
EOF
[ubuntu:~ ] # modprobe br_netfilter
[ubuntu:~ ] # modprobe overlay
[ubuntu:~ ] # lsmod | grep br_netfilter
[ubuntu:~ ] # lsmod | grep overlay

# sysctl
[ubuntu:~ ] # cat << EOF | tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

[ubuntu:~ ] # sysctl --system
[ubuntu:~ ] # sysctl --all | grep net.bridge.bridge-nf-call-ip6tables
[ubuntu:~ ] # sysctl --all | grep net.bridge.bridge-nf-call-iptables
[ubuntu:~ ] # sysctl --all | grep net.ipv4.ip_forward
[ubuntu:~ ] # sysctl --values net.bridge.bridge-nf-call-ip6tables
[ubuntu:~ ] # sysctl --values net.bridge.bridge-nf-call-iptables
[ubuntu:~ ] # sysctl --values net.ipv4.ip_forward
```


### container runtime interface

```
CRI             Path to Unix domain socket
Docker	        /var/run/dockershim.sock
containerd	    /run/containerd/containerd.sock
CRI-O	          /var/run/crio/crio.sock
```

cri 選一種安裝


[docker](./docker-ce.md)

kubernetes 1.23+ 後就不支援 docker


[cri-o](./crio.md)

* cri-o version 必須配合 kubeadm 版本


[containerd]


### kubeadm kubelet kubectl

```bash
[ubuntu:~ ] # apt update
[ubuntu:~ ] # apt install apt-transport-https ca-certificates curl
[ubuntu:~ ] # curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
[ubuntu:~ ] # echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list
[ubuntu:~ ] # apt update
[ubuntu:~ ] # apt install kubelet kubeadm kubectl kubernetes-cni
[ubuntu:~ ] # apt-mark hold kubelet kubeadm kubectl

[ubuntu:~ ] # systemctl status kubelet

[ubuntu:~ ] # kubeadm config print init-defaults
[ubuntu:~ ] # kubeadm config print join-defaults
```


---

## install

### master

```bash
[master:~ ] # kubeadm init --pod-network-cidr=10.244.0.0/16 --cri-socket /var/run/crio/crio.sock

# config
[master:~ ] # mkdir -p $HOME/.kube
[master:~ ] # cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
[master:~ ] # chown $(id -u):$(id -g) $HOME/.kube/config
[master:~ ] # export KUBECONFIG=/etc/kubernetes/admin.conf
[master:~ ] # kubectl get node

# auto-completion
[master:~ ] # apt install bash-completion
[master:~ ] # kubectl completion bash > /etc/bash_completion.d/kubectl

# network
# https://kubernetes.io/docs/concepts/cluster-administration/addons/
[master:~ ] # kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
[master:~ ] # kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/k8s-manifests/kube-flannel-rbac.yml

kubectl create -f https://projectcalico.docs.tigera.io/manifests/tigera-operator.yaml


# token
[master:~ ] # kubeadm token list
[master:~ ] # kubeadm token list -o json
[master:~ ] # kubeadm token list -o jsonpath="{$.token}"

# ca-cert-hash
[master:~ ] # openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex
[master:~ ] # openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'
```


### worker

```bash
[woker:~ ] # kubeadm join <master ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<ca-cert-hash>
```


---

## test

```bash
[master:~ ] # kubectl version --client

# create
[master:~ ] # kubectl create deployment hello-node --image=k8s.gcr.io/echoserver:1.4
[master:~ ] # kubectl get pod,deploy
[master:~ ] # kubectl scale deployment hello-node --replicas=2
[master:~ ] # kubectl get pod,deploy
[master:~ ] # kubectl expose deployment hello-node --type=NodePort --port=8080
[master:~ ] # kubectl get pod,deploy,svc
[master:~ ] # kubectl get svc -l app=hello-node
[master:~ ] # kubectl get svc -l app=hello-node -o jsonpath="{$.items[0].spec.ports[0].nodePort}"

# test
[master:~ ] # curl <node ip>:<node port>

# teardown
[master:~ ] # kubectl delete service/hello-node
[master:~ ] # kubectl delete deployment.apps/hello-node
```


---

## ref

[Installing kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)

[kubeadm join](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/)

[Hello Minikube](https://kubernetes.io/docs/tutorials/hello-minikube/)
