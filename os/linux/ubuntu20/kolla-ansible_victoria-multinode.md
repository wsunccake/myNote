# kolla-ansible victoria - multinode

## hardware requirement

```
OS:
  ubuntu 20.04 lts

HW:
  2 network interfaces
  8GB main memory
  40GB disk space
```


---

## network topology

```
deploy     control       compute      storage
   |          |             |            |
   |          |             |            |
   +----------+-------------+------------+  br-mgmt    / api_interface                10.20.0.x/24
              |             |            |
              |             |            |
              +-------------+------------+  br-storage / storage_interface
              |             |
              |             |
              +-------------+               br-tun     / tunnel_interface
              |
              |
              +                             br-ex      / neutron_external_interface
              |
              |
           internet
```

```
                         deploy     control     compute
openstack management     eth0       eth0        eth0
neutron external                    eth1        eth1
provider network                    eth2
```


---

## deploy node

### prepare

```bash
# hostname
[deploy01:~ ] # vi /etc/hosts
10.20.0.100  deploy01
10.20.0.101  control01
10.20.0.102  computer01

# ssh key
deploy01:~ $ ssh-keygen
deploy01:~ $ ssh-copy-id control01
deploy01:~ $ ssh-copy-id computer01
```


### install

```bash
# package
[deploy01:~ ] # apt update
[deploy01:~ ] # apt install python3-dev libffi-dev gcc libssl-dev
[deploy01:~ ] # apt install python3-pip
[deploy01:~ ] # pip3 install -U pip

# ansible
[deploy01:~ ] # pip3 install -U 'ansible<2.10'
[deploy01:~ ] # ansible --version
[deploy01:~ ] # mkdir -p /etc/ansible
[deploy01:~ ] # vi /etc/ansible/ansible.cfg
[defaults]
host_key_checking=False
pipelining=True
forks=100

# kolla-ansible
deploy01:~ # pip3 install kolla-ansible
```


### config

```bash
[deploy01:~  ] # mkdir -p /etc/kolla
[deploy01:~  ] # cp -v /usr/local/share/kolla-ansible/etc_examples/kolla/* /etc/ansible/.
'/usr/local/share/kolla-ansible/etc_examples/kolla/globals.yml' -> '/etc/kolla/./globals.yml'
'/usr/local/share/kolla-ansible/etc_examples/kolla/passwords.yml' -> '/etc/kolla/./passwords.yml'
[deploy01:~  ] # cp -v /usr/local/share/kolla-ansible/ansible/inventory/*  /etc/ansible/.
'/usr/local/share/kolla-ansible/ansible/inventory/all-in-one' -> '/etc/kolla/./all-in-one'
'/usr/local/share/kolla-ansible/ansible/inventory/multinode' -> '/etc/kolla/./multinode'
[deploy01:~  ] # chown -R <user>:<group> /etc/kolla

[deploy01:~  ] # vi /etc/kolla/globals.yml
kolla_base_distro: "ubuntu"
kolla_install_type: "binary"
openstack_release: "victoria"
node_custom_config: "/etc/kolla/config"
kolla_internal_vip_address: "10.20.0.111"
kolla_external_vip_address: "{{ kolla_internal_vip_address }}"
enable_haproxy: "yes"
nova_compute_virt_type: "kvm"

[deploy01:~ ] # vi /etc/kolla/multinode
[control]
control01 network_interface=eth1 tunnel_interface=eth1 neutron_external_interface=eth2 ansible_become_pass=<password>

[network]
control01 network_interface=eth1 tunnel_interface=eth1 neutron_external_interface=eth2 ansible_become_pass=<password>

[compute]
compute01 network_interface=eth1 tunnel_interface=eth1 ansible_become_pass=<password>

[monitoring]
control01 network_interface=eth1 tunnel_interface=eth1 neutron_external_interface=eth2 ansible_become_pass=<password>

[storage]
control01 network_interface=eth1 tunnel_interface=eth1 neutron_external_interface=eth2 ansible_become_pass=<password>
...
```


### deploy

```bash
[deploy01:~ ] $ kolla-ansible -i /etc/kolla/multinode bootstrap-servers
[deploy01:~ ] $ kolla-ansible -i /etc/kolla/multinode prechecks
[deploy01:~ ] $ kolla-ansible -i /etc/kolla/multinode pull
[deploy01:~ ] $ kolla-ansible -i /etc/kolla/multinode deploy

# reconfigure
[deploy01:~ ] $ kolla-ansible -i /etc/kolla/multinode reconfigure

# destroy
[deploy01:~ ] $ kolla-ansible -i /etc/kolla/multinode --yes-i-really-really-mean-it destroy
```


### usage

```bash
# get dashboard password
[deploy01:~ ] $ grep keystone_admin_password /etc/kolla/passwords.yml

# generate openstack rc
[deploy01:~ ] $ sudo kolla-ansible post-deploy
[deploy01:~ ] $ ls /etc/kolla/admin-openrc.sh
[deploy01:~ ] $ sudo chown <user>:<group> /etc/kolla/admin-openrc.sh
[deploy01:~ ] $ source /etc/kolla/admin-openrc.sh

# install openstack client module
[deploy01:~ ] $ sudo pip3 install python-openstackclient
[deploy01:~ ] $ openstack service list

# create example
[deploy01:~ ] $ /usr/local/share/kolla-ansible/init-runonce
[deploy01:~ ] $ openstack server create \
  --image cirros \
  --flavor m1.tiny \
  --key-name mykey \
  --network demo-net \
  demo1

[deploy01:~ ] $ openstack server delete demo1
```


---

## provider network

### all openstack node

```bash
# setup openvswitch
[ubuntu:~ ] # docker exec -it openvswitch_vswitchd ovs-vsctl show
[ubuntu:~ ] # docker exec -it openvswitch_vswitchd ovs-vsctl add-br br0
[ubuntu:~ ] # docker exec -it openvswitch_vswitchd ovs-vsctl add-port br0 eth2
 
# list bridge and port
[ubuntu:~ ] # ip addr show dev br0
[ubuntu:~ ] # ip addr show dev eth2
[ubuntu:~ ] # docker exec -it openvswitch_vswitchd ovs-vsctl show
[ubuntu:~ ] # docker exec -it openvswitch_vswitchd ovs-vsctl list-ports br0
```


### control node

```bash
# setup neutron-openvswitch-agent
[control01:~  ] # vi /etc/kolla/neutron-openvswitch-agent/openvswitch_agent.ini
...
[ovs]
bridge_mappings = physnet1:br-ex,physnet3:br0
...
 
# setup neutron-server
[control01:~  ] # vi /etc/kolla/neutron-server/ml2_conf.ini
...
[ml2_type_flat]
flat_networks = physnet1,physnet3
...

[control01:~  ] # docker restart neutron_openvswitch_agent
[control01:~  ] # docker restart neutron_server
[control01:~  ] # reboot

# list bridge and port
[control01:~  ] # docker exec -it openvswitch_vswitchd ovs-vsctl show
[control01:~  ] # docker exec -it openvswitch_vswitchd ovs-vsctl list-ports br0
```


### compute node

```bash
# setup neutron-openvswitch-agent
[compute01:~ ] # vi /etc/kolla/neutron-openvswitch-agent/openvswitch_agent.ini
...
[ovs]
bridge_mappings = physnet3:br0
...
 
[compute01:~ ] # reboot

# list bridge and port
[compute01:~ ] # docker exec -it openvswitch_vswitchd ovs-vsctl show
[compute01:~ ] # docker exec -it openvswitch_vswitchd ovs-vsctl list-ports br0
```


### deploy node

```bash
# check network agent
[deploy01:~ ] # openstack network agent list

# create provider network
[deploy01:~ ] # openstack network create --share \
  --provider-physical-network physnet3 \
  --provider-network-type flat \
  provider_network

# create ipv4 subnet network
[deploy01:~ ] # openstack subnet create \
  --subnet-range 192.168.0.0/24 \
  --gateway 192.168.0.1 \
  --network provider_network \
  --allocation-pool start=192.168.0.100,end=192.168.0.200 \
  provider_subnet_v4

# create ipv6 subnet network
[deploy01:~ ] # openstack subnet create \
  --ip-version 6 \
  --ipv6-ra-mode slaac \
  --ipv6-address-mode slaac \
  --subnet-range 2001:192::/64 \
  --gateway 2001:192::1 \
  --network provider_network \
  --allocation-pool start=2001:192::100/64,end=2001:192::200/64 \
  provider_subnet_v6
```


---

## other


### quota port number

```bash
[deploy01:~ ] # openstack quota show
[deploy01:~ ] # openstack quota list --network
[deploy01:~ ] # openstack quota set --ports 5000 <project>
```


### resource overcommitting

```bash
[control01:~ ] # vi /etc/kolla/nova-scheduler/nova.conf
[DEFAULT]
...
cpu_allocation_ratio=1.0
ram_allocation_ratio=1.0
disk_allocation_ratio=1.0
...

[control01:~ ] # docker restart nova_scheduler
```


### glance image space

```bash
[control01:~ ] # docker volume inspect glance
[control01:~ ] # vi /etc/fstab
...
<nfs_ip>:<nfs_path>     /var/lib/docker/volumes/glance      nfs     defaults        0 0
...

[control01:~ ] # mount -a
[control01:~ ] # reboot
```

### nova compute hypervisor

```bash
[compute01:~ ] # cat /etc/kolla/nova-compute/nova.conf
...
[libvirt]
connection_uri = qemu+tcp://192.168.10.110/system
live_migration_inbound_addr = 192.168.10.110
virt_type = kvm
...

[compute01:~ ] # docker restart nova_compute
```
