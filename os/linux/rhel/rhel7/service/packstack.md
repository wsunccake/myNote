# PackStack


## Install

Condition: all in one

`prepare`

```bash
# 
centos:~ # /etc/environment
LANG=en_US.utf-8
LC_ALL=en_US.utf-8

centos:~ # systemctl disable firewalld
centos:~ # systemctl stop firewalld
centos:~ # systemctl disable NetworkManager
centos:~ # systemctl stop NetworkManager
centos:~ # systemctl enable network
centos:~ # systemctl start network
```


`repository`

```bash
#for rhel
centos:~ # yum install https://www.rdoproject.org/repos/rdo-release.rpm

# for centos
centos:~ # yum install centos-release-openstack-pike
```


`install`

```
centos:~ # yum update
centos:~ # yum install openstack-packstack
centos:~ # packstack --allinone
```

## Config

```bash
# config file
centos:~ # ls /root/packstack-answers*.txt

# rc file
centos:~ # cat /root/keystonerc_admin
unset OS_SERVICE_TOKEN
export OS_USERNAME=<USER>
export OS_PASSWORD=<PASSWORD>
export OS_AUTH_URL=http://<OPENASTACK_IP>:5000/v3

export OS_PROJECT_NAME=<PROJECT>
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_IDENTITY_API_VERSION=3

centos:~ # source /root/keystonerc_admin

# log
centos:~ # ls /var/tmp/packstack

# web
centos:~ # curl http://<ip>/dashboard
```

---

## CLI

`system`

```bash
# help
centos:~ # openstack command list

# host, hypervisor
centos:~ # openstack host list
centos:~ # openstack host show <host>
centos:~ # openstack host set [<arg>,...] <host>

centos:~ # openstack hypervisor list
centos:~ # openstack hypervisor show
centos:~ # openstack hypervisor stats show

# user, group, role
centos:~ # openstack user list
centos:~ # openstack user show <user>
centos:~ # openstack user create [<arg>,...] <user>
centos:~ # openstack user delete [<arg>,...] <user>
centos:~ # openstack user set [<arg>,...] <user>

centos:~ # openstack group list
centos:~ # openstack group show <group>
centos:~ # openstack group create [<arg>,...] <group>
centos:~ # openstack group delete [<arg>,...] <group>
centos:~ # openstack group set [<arg>,...] <group>
centos:~ # openstack group add user [<arg>,...] <group ><user>
centos:~ # openstack group remove user [<arg>,...] <group> <user>
centos:~ # openstack group contains user

centos:~ # openstack role list
centos:~ # openstack role show <role>
centos:~ # openstack role create [<arg>,...] <role>
centos:~ # openstack role delete [<arg>,...] <role>
centos:~ # openstack role set [<arg>,...] <role>
centos:~ # openstack role assignment list
centos:~ # openstack role add [<arg>,...] <gorup ><user>
centos:~ # openstack role remove [<arg>,...] <role> <user>
```


`serivce`

```bash
# project
centos:~ # openstack project list
centos:~ # openstack project show <project>
centos:~ # openstack project create [<arg>,...] <project>
centos:~ # openstack project delete [<arg>,...] <project>
centos:~ # openstack project set [<arg>,...] <project>
centos:~ # openstack project unset [<arg>,...] <project>

# service
centos:~ # openstack service list
centos:~ # openstack service show <service>
centos:~ # openstack service create [<arg>,...] <service>
centos:~ # openstack service delete [<arg>,...] <service>
centos:~ # openstack service set [<arg>,...] <service>
```


`instance`

```bash
# image
centos:~ # openstack image list
centos:~ # openstack image show <image>
centos:~ # openstack image create [<arg>,...] <image>
centos:~ # openstack image delete [<arg>,...] <image>
centos:~ # openstack image set [<arg>,...] <image>

# flavor
openstack flavor list
openstack flavor show <flavor>
openstack flavor create [<arg>,...] <flavor>
openstack flavor delete [<arg>,...] <flavor>
openstack flavor set [<arg>,...] <flavor>
openstack flavor unset [<arg>,...] <flavor>
```