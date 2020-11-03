# kolla-ansible ussuri - multinode


## nic topology

```
        +----------+-------------+------------+  openstack management
        |          |             |            |
        |          |             |            |
 deploy		control       compute      storage
                   |
                   |neutron external
                   v 
                internet
```

```
                         deploy     control     compute
openstack management     eth0       eth0        eth0
neutron external                    eth1
```

---

## non deploy node

control, compute, storage


### prepare


```bash
# install docker
centos:~ # dnf autoremove podman
centos:~ # dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
centos:~ # dnf install docker-ce --nobest
centos:~ # systemctl enable docker --now

# update hosts
centos:~ # vi /etc/hosts
192.168.10.100  control01
192.168.10.110  compute01

# disable firewall
centos:~ # systemctl disable firewalld --now

# disable selinux
centos:~ # sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/onfig
centos:~ # reboot

# private registry
centos:~ # vi /etc/docker/daemon.json
{
  "insecure-registries": ["<deploy_ip>:5000"]
}

centos:~ # systemctl daemon-reload
centos:~ # curl -X GET http://<deploy_ip>:5000/v2/_catalog
centos:~ # docker pull kolla/centos-binary-chrony:ussuri
```

---

## deploy node


### prepare

```bash
# install package by dnf
deploy:~ # dnf makecache
deploy:~ # dnf install git
deploy:~ # dnf install epel-release
deploy:~ # dnf install python3-pip wget

# install package by pip
deploy:~ # pip3 install -U pip
deploy:~ # pip3 install wheel
deploy:~ # pip3 install ansible            # ansible (>= 2.9)
deploy:~ # pip3 install kolla-ansible

# install docker
deploy:~ # dnf autoremove podman
deploy:~ # dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
deploy:~ # dnf install docker-ce --nobest
deploy:~ # systemctl enable docker --now

# update hosts
deploy:~ # vi /etc/hosts
192.168.10.100  control01
192.168.10.110  compute01

# disable selinux
deploy:~ # sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
deploy:~ # reboot
```


### setup config

```bash
# copy ssh-key
deploy:~ # ssh-keygen -t rsa -f /root/.ssh/id_rsa -q -N "" <<< y
deploy:~ # ssh-copy-id control01
deploy:~ # ssh-copy-id compute01

# setup ansible
deploy:~ # vi /etc/ansible/ansible.cfg
[defaults]

forks = 100
host_key_checking = False
pipelining = True

deploy:~ # ansible all -i control01,compute01 -m ping


# setup kolla-ansible
deploy:~ # mkdir -p /etc/kolla
deploy:~ # cp -r /usr/local/share/kolla-ansible/etc_examples/kolla/* /etc/kolla/.    # globals.yml, passwords.yml 
deploy:~ # cp -r /usr/local/share/kolla-ansible/ansible/inventory/* /etc/kolla/.     # all-in-one, multinode

deploy:~ # vi /etc/kolla/globals.yml
kolla_base_distro: "centos"
kolla_install_type: "binary"
openstack_release: "ussuri"
node_custom_config: "/etc/kolla/config"
enable_haproxy: "no"
network_interface: "eth0"                       # openstack management network
neutron_external_interface: "eth1"              # openstack external network
kolla_internal_vip_address: "192.168.10.100"    # <ip> must openstack control management network 
nova_compute_virt_type: "kvm"                   # egrep -c '(vmx|svm)' /proc/cpuinfo > 0 => kvm, = 0 => qemu
                                                # kvm: hardware support, qemu: no hardware support


# update inventory
deploy:~ # vi /etc/kolla/multinode
[control]
control01  network_interface=eth0

[network]
control01  network_interface=eth0

[compute]
compute01  network_interface=eth0

[monitoring]
control01  network_interface=eth0

[storage]
#storage01  network_interface=eth0

[deployment]
control01  network_interface=eth0
...

deploy:~ # ansible -i /etc/kolla/multinode all -m ping

# update password
deploy:~ # kolla-genpwd
```


#### endpoint network configuration

kolla_internal_vip_address

network_interface

kolla_external_vip_address

kolla_external_vip_interface


#### openstack service configuration in kolla

node_custom_config


#### ip address constrained environment

enable_haproxy


### pull image

```bash
deploy:~ # kolla-ansible -i /etc/kolla/all-in-one bootstrap-servers
deploy:~ # kolla-ansible -i /etc/kolla/all-in-one pull
deploy:~ # docker images
```


### private registry

```bash
deploy:~ # docker run -d -p 5000:5000 --restart=always --name registry -v <data>:/var/lib/registry registry:2
deploy:~ # docker run -d -p 80:80 -e ENV_DOCKER_REGISTRY_HOST=<registry_ip> -e ENV_DOCKER_REGISTRY_PORT=5000 konradkleine/docker-registry-frontend:v2
```


### push image to private registry


```bash
deploy:~ # docker images | grep kolla | grep -v local | awk '{print $1,$2}' | while read -r image tag; do
    docker tag ${image}:${tag} localhost:5000/${image}:${tag}
    docker push localhost:5000/${image}:${tag}
done
```

```bash
deploy:~ # kolla-ansible -i /etc/kolla/multinode bootstrap-servers
deploy:~ # kolla-ansible -i /etc/kolla/multinode prechecks
deploy:~ # kolla-ansible -i /etc/kolla/multinode pull
deploy:~ # kolla-ansible -i /etc/kolla/multinode deploy
```

---

## ref

[Welcome to Kolla-Ansible’s documentation!](https://docs.openstack.org/kolla-ansible/latest/)

