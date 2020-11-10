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
                                    eth2        eth2
```

---

## non deploy node

control, compute, storage


### all


```bash
# setup hostname
centos:~ # hostnamectl set-hostname <hostname>

# install package by dnf
centos:~ # dnf makecache
centos:~ # dnf install epel-release

# install docker
centos:~ # dnf autoremove podman
centos:~ # dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
centos:~ # dnf install docker-ce --nobest
centos:~ # systemctl enable docker --now

# setup private registry
centos:~ # vi /etc/docker/daemon.json
{
  "insecure-registries": ["<deploy_ip>:5000"]
}
centos:~ # systemctl daemon-reload
centos:~ # curl -X GET http://<deploy_ip>:5000/v2/_catalog
centos:~ # docker pull kolla/centos-binary-chrony:ussuri

# disable firewall
centos:~ # systemctl disable firewalld --now

# disable selinux
centos:~ # sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
centos:~ # reboot
```


### storage

```bash
storage:~ # dnf install lvm2
storage:~ # lsblk -fp

# pv
storage:~ # pvs
storage:~ # pvcreate /dev/sdb

# vg
storage:~ # vgs
storage:~ # vgcreate cinder-volumes /dev/sdb
```


---

## deploy node


### prepare

```bash
# setup hostname
deploy:~ # hostnamectl set-hostname deploy

# install package by dnf
deploy:~ # dnf makecache
deploy:~ # dnf install epel-release
deploy:~ # dnf install python3
deploy:~ # dnf install ansible

# install package by pip
deploy:~ # pip3 install -U pip
deploy:~ # pip3 install wheel
deploy:~ # pip3 install ansible            # ansible (2.8 ~ 2.9)
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


#### network configuration

network_interface - While it is not used on its own, this provides the required default for other interfaces below.

api_interface - This interface is used for the management network. The management network is the network OpenStack services uses to communicate to each other and the databases. There are known security risks here, so it’s recommended to make this network internal, not accessible from outside. Defaults to network_interface.

kolla_external_vip_interface - This interface is public-facing one. It’s used when you want HAProxy public endpoints to be exposed in different network than internal ones. It is mandatory to set this option when kolla_enable_tls_external is set to yes. Defaults to network_interface.

storage_interface - This is the interface that is used by virtual machines to communicate to Ceph. This can be heavily utilized so it’s recommended to put this network on 10Gig networking. Defaults to network_interface.

cluster_interface - This is another interface used by Ceph. It’s used for data replication. It can be heavily utilized also and if it becomes a bottleneck it can affect data consistency and performance of whole cluster. Defaults to network_interface.

tunnel_interface - This interface is used by Neutron for vm-to-vm traffic over tunneled networks (like VxLan). Defaults to network_interface.

neutron_external_interface - This interface is required by Neutron. Neutron will put br-ex on it. It will be used for flat networking as well as tagged vlan networks. Has to be set separately.


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

deploy:~ # kolla-ansible -i /etc/kolla/multinode --yes-i-really-really-mean-it destroy
```


### usage

```bash
# get dashboard password
deploy:~ # grep keystone_admin_password /etc/kolla/passwords.yml

# generate openstack rc
deploy:~ # kolla-ansible post-deploy

deploy:~ # ls /etc/kolla/admin-openrc.sh
deploy:~ # source /etc/kolla/admin-openrc.sh

# install openstack client module
deploy:~ # pip3 install python-openstackclient
deploy:~ # openstack service list

# create example
deploy:~ # /usr/local/share/kolla-ansible/init-runonce
deploy:~ # openstack server create --image cirros --flavor m1.tiny --key-name mykey --network demo-net demo1
```


---

## provider network


### all openstack node

```bash
centos:~ # dnf install network-scripts
centos:~ # systemctl enable network --now
centos:~ # systemctl disable NetworkManager --now
 
# setup openvswitch
centos:~ # docker exec -it openvswitch_vswitchd ovs-vsctl show
centos:~ # docker exec -it openvswitch_vswitchd ovs-vsctl add-br br0
centos:~ # docker exec -it openvswitch_vswitchd ovs-vsctl add-port br0 eth2
 
# list bridge and port
centos:~ # ip addr show dev br0
centos:~ # ip addr show dev eth2
centos:~ # docker exec -it openvswitch_vswitchd ovs-vsctl show
centos:~ # docker exec -it openvswitch_vswitchd ovs-vsctl list-ports br0
```

NetworkManager do not support openvswitch


### control node

```bash
# setup neutron-openvswitch-agent
control:~ # vi /etc/kolla/neutron-openvswitch-agent/openvswitch_agent.ini
...
[ovs]
bridge_mappings = physnet1:br-ex,physnet3:br0
...
 
# setup neutron-server
control:~ # vi /etc/kolla/neutron-server/ml2_conf.ini
...
[ml2_type_flat]
flat_networks = physnet1,physnet3
...
 
control:~ # reboot

# list bridge and port
control:~ # docker exec -it openvswitch_vswitchd ovs-vsctl show
control:~ # docker exec -it openvswitch_vswitchd ovs-vsctl list-ports br0
```


### compute node

```bash
# setup neutron-openvswitch-agent
compute:~ # vi /etc/kolla/neutron-openvswitch-agent/openvswitch_agent.ini
...
[ovs]
bridge_mappings = physnet3:br0
...
 
compute:~ # reboot

# list bridge and port
compute:~ # docker exec -it openvswitch_vswitchd ovs-vsctl show
compute:~ # docker exec -it openvswitch_vswitchd ovs-vsctl list-ports br0
```


### deploy node

```bash
# check network agent
deploy:~ # openstack network agent list

# create provider network
deploy:~ # openstack network create --share \
  --provider-physical-network physnet3 \
  --provider-network-type flat \
  provider_network

# create subnet network
deploy:~ # openstack subnet create --subnet-range 192.168.0.0/24 \
  --gateway 192.168.0.1 \
  --network provider_network \
  --allocation-pool start=192.168.0.100,end=192.168.0.200 \
  provider_subnet_v4
```


---

## ref

[Welcome to Kolla-Ansible’s documentation!](https://docs.openstack.org/kolla-ansible/latest/)

