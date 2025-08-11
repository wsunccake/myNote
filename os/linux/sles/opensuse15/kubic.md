# kubkic (Kubernetes for opensuse)

## install kubic

[openSUSE Kubic](https://kubic.opensuse.org/)

download image and install os, select kubeadm Node


---

## atomic system

```bash
kubic:~ # transactional-update --help
kubic:~ # transactional-update pkg install <pkg>

kubic:~ # findmnt
```


### btrfs

```bash
kubic:~ # btrfs help
kubic:~ # btrfs filesystem --help
kubic:~ # btrfs filesystem show

kubic:~ # btrfs filesystem df /
kubic:~ # btrfs filesystem du /
kubic:~ # btrfs subvolume list /
kubic:~ # btrfs subvolume get-default /
kubic:~ # btrfs device usage /
kubic:~ # btrfs stats usage /
```


### snapper

```bash
# list
kubic:~ # snapper --help

# config folder
kubic:~ # ls /etc/snapper
kubic:~ # ls <path>/.snapper

# snapper config
kubic:~ # snapper list-configs                                 # list
kubic:~ # snapper -c <snapper_config> create-configs <path>    # create
kubic:~ # snapper [-c <snapper_config>] delete-config          # delete
kubic:~ # snapper [-c <snapper_config>] get-config
kubic:~ # snapper [-c <snapper_config>] set-config "NUMBER_CLEANUP=yes NUMBER_LIMIT=10"

# snapshot
kubic:~ # snapper -c <snapper_config> create [-t pre] [-d <description>]      # create
kubic:~ # snapper -c <snapper_config> create [-t post --pre-number <pre_id>] [-d <description>]
kubic:~ # snapper -c <snapper_config> modify <snapper_id> -d <description>    # modify 
kubic:~ # snapper -c <snapper_config> delete <snapper_id>                     # delete
kubic:~ # snapper [-c <snapper_config>] list|ls                               # list
kubic:~ # snapper [-c <snapper_config>] status 1..5
kubic:~ # snapper [-c <snapper_config>] diff 1..5

# rollback
kubic:~ # snapper [-c <snapper_config>] rollback <snapper_id>
kubic:~ # snapper [-c <snapper_config>] undochange 5..2 [file]
```


---

## master

```bash
master:~ # kubeadm init --pod-network-cidr 10.244.0.0/16 [--service-cidr 10.96.0.0/12] [--token 1234]

# config
master:~ # mkdir -p $HOME/.kube
master:~ # cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
master:~ # chown $(id -u):$(id -g) $HOME/.kube/config

# network
master:~ # kubectl apply -f /usr/share/k8s-yaml/flannel/kube-flannel.yaml

# network policy
master:~ # kubectl apply -f /usr/share/k8s-yaml/cilium/quick-install.yaml

# token id
master:~ # kubeadm token list

# ca hash
master:~ # openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'
```

config folder:

/var/lib/kubelet

/etc/kubernetes

port: 6443


--- 

## node

```bash
node:~ # kubeadm join <master_ip>:6443 --token <token_id> --discovery-token-ca-cert-hash sha256:<ca_hash>
```


---


## container

```bash
node:~ # crictl ps
```


## kube cluster

```bash
master:~ # kubectl get node [-o wide] [--all-namespaces]
master:~ # kubectl get pod
master:~ # kubectl get deployment
master:~ # kubectl get service
master:~ # kubectl get replicaset
master:~ # kubectl describe node
master:~ # kubectl describe pod
master:~ # kubectl describe deployment
master:~ # kubectl describe service
master:~ # kubectl describe replicaset

# create app
master:~ # kubectl run hello-world --image=gcr.io/google-samples/node-hello:1.0 --port=8080

# create service
master:~ # kubectl expose deployment hello-world --external-ip=<mater_ip>|<node_ip> --port=80 --target-port=8080 --type=NodePort

# delete service
master:~ # kubectl delete service hello-world

# delete service
master:~ # kubectl delete deployment hello-world
```
