# kolla-ansible train - all in one (aio)

## require

OS: centos 8

vCPU: 2

vRAM: 8GB

HD: 40GB

NIC: 2


---

## prepare

```bash
centos8:~ # dnf makecache
centos8:~ # dnf install epel-release
centos8:~ # dnf install git ansible

# disable selinux
centos8:~ # sed -i s/^SELINUX=.*/SELINUX=disabled/ /etc/selinux/config

# stop firewall
centos8:~ # systemctl stop firewalld
centos8:~ # systemctl disable firewalld

# install docker
centos8:~ # dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
centos8:~ # dnf install docker-ce --nobest
centos8:~ # systemctl enable docker --now

centos8:~ # reboot
```


---

## install

### kolla-ansible package

```bash
centos8:~ # pip3 install -U pip
centos8:~ # mkdir -p /etc/kolla

# binary
centos8:~ # pip3 install wheel
centos8:~ # pip3 install ansible
centos8:~ # pip3 install kolla-ansible

# source
centos8:~ # git clone https://github.com/openstack/kolla
centos8:~ # git clone https://github.com/openstack/kolla-ansible
centos8:~ # pip3 install ./kolla
centos8:~ # pip3 install ./kolla-ansible

# config
centos8:~ # cp -r /usr/local/share/kolla-ansible/etc_examples/kolla/* /etc/kolla/.
# globals.yml, passwords.yml 
centos8:~ # cp -r /usr/local/share/kolla-ansible/ansible/inventory/* .
# all-in-one, multinode
```


### ansible config

```bash
centos8:~ # vi /etc/ansible/ansible.cfg
[defaults]
host_key_checking=False
pipelining=True
forks=100

# test host
centos8:~ # ansible -i all-in-one -m ping

# /etc/kolla/passwords.yml
centos8:~ # kolla-genpwd
centos8:~ # ./kolla-ansible/tools/generate_passwords.py

# /etc/kolla/globals.yml
centos8:~ # vi /etc/kolla/globals.yml
kolla_base_distro: "centos"
kolla_install_type: "binary"
openstack_release: "train"
network_interface: "eth0"             # openstack management network
neutron_external_interface: "eth1"    # openstack external network
kolla_internal_vip_address: "192.168.100.123"
# kolla_external_vip_address: "192.168.100.123"

# deploy
centos8:~ # kolla-ansible -i ./all-in-one bootstrap-servers
centos8:~ # kolla-ansible -i ./all-in-one prechecks
centos8:~ # kolla-ansible -i ./all-in-one deploy
```


---

## usage

```bash
centos8:~ # grep keystone_admin_password /etc/kolla/passwords.yml

# generate openstack rc
centos8:~ # kolla-ansible post-deploy                          # binary
centos8:~ # ./kolla-ansible/tools/kolla-ansible post-deploy    # source

centos8:~ # ls /etc/kolla/admin-openrc.sh
centos8:~ # source /etc/kolla/admin-openrc.sh

# openstack client
centos8:~ # pip3 install python-openstackclient
centos8:~ # openstack service list

# create example
centos8:~ # /usr/local/share/kolla-ansible/init-runonce
```


---

## ref

[kolla-ansible](https://docs.openstack.org/kolla-ansible/latest/)