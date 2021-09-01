# kubespray

## hardware requirement

```
OS:
  ubuntu 20.04 lts

HW:
  4 vcpu
  1 network interfaces
  8GB main memory
  100GB disk space

```


---

## network topology

```
deploy      master      worker
|           |           |
|           |           |
+-----------+-----------+
```


---

## prepare

### deploy node


```bash
[deploy01:~ ] # apt update
[deploy01:~ ] # apt install openssh-server sshpass
[deploy01:~ ] # apt install python3 python3-pip

# ssh key
[deploy01:~ ] $ ssh-keygen -N ""
[deploy01:~ ] $ ssh-copy-id master01
[deploy01:~ ] $ ssh-copy-id worker01

# hosts
[deploy01:~ ] # vi /etc/hosts
192.168.10.100  deploy01
192.168.10.101  master01
192.168.10.102  worker01
```


### k8s node

```bash
# firewall
[node:~ ] # ufw status
[node:~ ] # ufw disable
[node:~ ] # systemctl disable ufw

# br_netfilter
[node:~ ] # vi /etc/modules-load.d/br_netfilter.conf
br_netfilterroot

[node:~ ] # modprobe br_netfilter
echo '1' > /proc/sys/net/bridge/bridge-nf-call-iptables

# ip_forward
[node:~ ] # vi /etc/sysctl.conf
net.ipv4.ip_forward=1

[node:~ ] # sysctl -w net.ipv4.ip_forward=1
```


---

## install

```bash
# download
[deploy01:~ ] $ git clone https://github.com/kubernetes-sigs/kubespray.git
[deploy01:~ ] $ cd kubespray

# install python package
[deploy01:~/kubespray ] $ sudo pip3 install -r requirements.txt

# copy config
[deploy01:~/kubespray ] $ cp -rfp inventory/sample inventory/mycluster

# generate inventory
[deploy01:~/kubespray ] $ declare -a IPS=(192.168.10.101 192.168.10.102)
[deploy01:~/kubespray ] $ CONFIG_FILE=inventory/mycluster/hosts.yaml python3 contrib/inventory_builder/inventory.py ${IPS[@]}

# inverntory file
[deploy01:~/kubespray ] $ vi inventory/mycluster/hosts.yaml
all:
  hosts:
    master01:
      ansible_host: 192.168.10.101
      ansible_ssh_user: <user>
      ansible_ssh_pass: <password>
      ansible_become_pass: <password>
      ip: 192.168.10.101
      access_ip: 192.168.10.101
    worker01:
      ansible_host: 192.168.10.102
      ansible_ssh_user: <user>
      ansible_ssh_pass: <password>
      ansible_become_pass: <password>
      ip: 192.168.10.102
      access_ip: 192.168.10.102
  children:
    kube_control_plane:
      hosts:
        master01:
    kube_node:
      hosts:
        worker01:
    etcd:
      hosts:
        master01:
    k8s_cluster:
      children:
        kube_control_plane:
        kube_node:
    calico_rr:
      hosts: {}

# addons
[deploy01:~/kubespray ] $ vi inventory/mycluster/group_vars/k8s_cluster/addons.yml
...
# change value to true if want to use nginx-proxy as ingress
ingress_nginx_enabled: true

# k8s-cluster
[deploy01:~/kubespray ] $ vi inventory/mycluster/group_vars/k8s_cluster/k8s-cluster.yml
...
# change container runtime to use cri-o
container_manager: crio
 
# change value to match the environment if want to use MetaLB as loadbalancer
kube_proxy_strict_arp: true
...
metallb_enabled: true
metallb_speaker_enabled: true
metallb_ip_range:
   - "192.168.10.150-192.168.10.200"

[deploy01:~/kubespray ] $ vi inventory/mycluster/group_vars/etcd.yml
...
# change value if change container runtime to use cri-o
etcd_deployment_type: host

# start to deploy
[deploy01:~/kubespray ] $ ansible-playbook -i inventory/mycluster/hosts.yaml --become --become-user=root cluster.yml
```


---

## test

```bash
[master01:~ ] # kubectl cluster-info
[master01:~ ] # kubectl config get-contexts

[master01:~ ] # kubectl create namespace demo
[master01:~ ] # kubectl -n demo
[master01:~ ] # kubectl -n demo create deployment hello-node --image=k8s.gcr.io/echoserver:1.4
[master01:~ ] # kubectl -n demo expose deployment hello-node --type=LoadBalancer --port=8080

[master01:~ ] # kubectl -n demo get svc hello-node -o json
[master01:~ ] # kubectl -n demo get svc hello-node -o jsonpath='{@}'
[master01:~ ] # srv_ip=$(kubectl -n demo get svc hello-node -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
[master01:~ ] # srv_port=$(kubectl -n demo get svc hello-node -o jsonpath='{.spec.ports[0].targetPort}')

[master01:~ ] # curl $srv_ip:$srv_port

[master01:~ ] # kubectl delete namesapce demo
```
