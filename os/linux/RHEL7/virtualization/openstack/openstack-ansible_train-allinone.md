# openstack-ansible (osa) train - all in one (aio)


## require

OS:   cento7

vCPU: 8
vRAM: 16GB 
HD:   80GB 
NIC:  1


## install

```bash
centos7:~ # yum makecache
centos7:~ # yum upgrade
centos7:~ # yum install git
centos7:~ # systemctl stop firewalld
centos7:~ # systemctl mask firewalld

centos7:~ # sed -i s/^SELINUX=.*/SELINUX=disabled/ /etc/selinux/config
centos7:~ # reboot
```

```bash
centos7:~ # git clone https://opendev.org/openstack/openstack-ansible /opt/openstack-ansible
centos7:~ # cd /opt/openstack-ansible

centos7:/opt/openstack-ansible # git tag -l
centos7:/opt/openstack-ansible # git checkout tags/19.1.0 -b stable/stein

centos7:/opt/openstack-ansible # git branch -a
centos7:/opt/openstack-ansible # git checkout stable/train

centos7:/opt/openstack-ansible # scripts/bootstrap-ansible.sh
centos7:/opt/openstack-ansible # [env BOOTSTRAP_OPTS="bootstrap_host_data_disk_device=sdb bootstrap_host_data_disk_fs_type=xfs"] scripts/bootstrap-aio.sh
centos7:/opt/openstack-ansible # cp etc/openstack_deploy/conf.d/{aodh,gnocchi,ceilometer}.yml.aio /etc/openstack_deploy/conf.d/
centos7:/opt/openstack-ansible # for f in $(ls -1 /etc/openstack_deploy/conf.d/*.aio); do mv -v ${f} ${f%.*}; done
```

```bash
centos7:~ # cd /opt/openstack-ansible/playbooks
centos7:/opt/openstack-ansible/playbooks # openstack-ansible setup-hosts.yml
centos7:/opt/openstack-ansible/playbooks # openstack-ansible setup-infrastructure.yml
centos7:/opt/openstack-ansible/playbooks # openstack-ansible setup-openstack.yml
```

```bash
centos7:~ # grep keystone_auth_admin_password /etc/openstack_deploy/user_secrets.yml
centos7:~ # lxc-attch -n <xxx>_utility_container-<yyy>
utility_container:~ # source /root/openrc
utility_container:~ # openstack help
``` 


---

## usage

### [flavor](https://docs.openstack.org/python-openstackclient/latest/cli/command-objects/flavor.html)

```bash
openstack flavor list
openstack show <flavor_name>|<flavor_id>
openstack flavor create --disk <disk_size> --vcpus <vcpu> --ram <ram_size> --public <flavor_name>
openstack delete <flavor_name>|<flavor_id>
```


### [image](https://docs.openstack.org/python-openstackclient/latest/cli/command-objects/image.html)

```bash
openstack image list
openstack image show <image_name>|<image_id>
openstack image create --disk-format <image_type> --file <image_file> --public <image_name>
openstack image delete <image_name>|<image_id>
```


### [network](https://docs.openstack.org/python-openstackclient/latest/cli/command-objects/network.html)

```bash
openstack network list
openstack network show <network_name>|<network_name>
openstack network create --provider-network-type <network_type> <network_name>
openstack network delete <network_name>|<network_name>
```


### [subnet](https://docs.openstack.org/python-openstackclient/latest/cli/command-objects/subnet.html)

```bash
openstack subnet list
openstack subnet show <subnet_name>|<subnet_name>
openstack subnet create --network <network_name> <subnet_name>
openstack subnet delete <subnet_name>|<subnet_name>
```


### [server](https://docs.openstack.org/python-openstackclient/latest/cli/command-objects/server.html)

```bash
openstack server list
openstack server show <server_name>|<server_name>
openstack server create --image <image_name> --flavor <flavor> --network <network_name> <server_name>
openstack server delete <server_name>|<server_name>
```


### example

```bash
utility_container:~ # wget http://download.cirros-cloud.net/0.5.1/cirros-0.5.1-x86_64-disk.img
utility_container:~ # openstack flavor create --disk 1 --vcpus 1 --ram 1024 --public  m1
utility_container:~ # openstack image create --disk-format qcow2 --file ./cirros-0.5.1-x86_64-disk.img --public cirros
utility_container:~ # openstack network create --provider-network-type vxlan n1
utility_container:~ # openstack subnet create --subnet-range 192.168.200.0/24 --network n1 s1
utility_container:~ # openstack server create --flavor m1 --network n1 --image cirros c1
```


---

## other

```bash
openstack service list
openstack hypervisor list
openstack host list
openstack compute agent list
openstack compute service list
openstack network agent list
```

