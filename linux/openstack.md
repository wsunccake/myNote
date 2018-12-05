# glance

```bash
op:~ # glance image-list
op:~ # glance image-show ef647309-d560-44bb-a159-6b423dc824ca

op:~ # glance image-create --name 'vsz-5.0.0.0.123' \
  --container-format bare \
  --disk-format qcow2 \
  --is-public true \
  --copy-from http://192.168.0.1/vsz-5.1.0.0.123.qcow2

op:~ # glance image-create --name 'vsz-5.0.0.0.123' \
  --container-format bare \
  --disk-format qcow2 \
  --is-public true \
  --file vsz-5.1.0.0.123.qcow2

op:~ # glance image-create --name 'vsz-5.0.0.0.123' \
  --container-format bare \
  --disk-format qcow2 \
  --is-public true \
  --progress < vsz-5.1.0.0.123.qcow2

op:~ # glance image-delete <img_id>
```

## disable swift / enable file

```bash
# stop glance
op:~ # service glance-api
op:~ # service glance-registry stop
op:~ # service glance-glare stop

# stop swift
op:~ # initctl stop swift-proxy
op:~ # initctl stop swift-account
op:~ # initctl stop swift-account-auditor
op:~ # initctl stop swift-account-reaper
op:~ # initctl stop swift-account-replicator
op:~ # initctl stop swift-container
op:~ # initctl stop swift-container-auditor
op:~ # initctl stop swift-container-replicator
op:~ # initctl stop swift-container-reconciler
op:~ # initctl stop swift-container-sync
op:~ # initctl stop swift-container-updater
op:~ # initctl stop swift-object
op:~ # initctl stop swift-object-auditor
op:~ # initctl stop swift-object-replicator
op:~ # initctl stop swift-object-updater
op:~ # initctl stop swift-object-reconstructor

# disable swift
op:~ # echo "manual" | tee /etc/init/swift-proxy.override
op:~ # echo "manual" | tee /etc/init/swift-account.override
op:~ # echo "manual" | tee /etc/init/swift-account-auditor.override
op:~ # echo "manual" | tee /etc/init/swift-account-reaper.override
op:~ # echo "manual" | tee /etc/init/swift-account-replicator.override
op:~ # echo "manual" | tee /etc/init/swift-container.override
op:~ # echo "manual" | tee /etc/init/swift-container-auditor.override
op:~ # echo "manual" | tee /etc/init/swift-container-replicator.override
op:~ # echo "manual" | tee /etc/init/swift-container-sync.override
op:~ # echo "manual" | tee /etc/init/swift-container-updater.override
op:~ # echo "manual" | tee /etc/init/swift-object.override
op:~ # echo "manual" | tee /etc/init/swift-object-auditor.override
op:~ # echo "manual" | tee /etc/init/swift-object-replicator.override
op:~ # echo "manual" | tee /etc/init/swift-object-updater.override
op:~ # echo "manual" | tee /etc/init/swift-object-reconstructor.override

# update glance config
op:~ # vi /etc/glance/glance-api.conf
stores = glance.store.swift.Store,glance.store.http.Store  ->  stores = file,http
default_store = swift  ->  default_store = file
filesystem_store_datadir = /var/lib/glance/images
...

op:~ # vi /etc/glance/glance-glare.conf
default_store = swift  ->  default_store = file
...

# regenerate glance database
op:~ # grep connection /etc/glance/glance-api.conf
connection = mysql://glance:<glance_password>@10.0.0.1/glance?charset=utf8&read_timeout=60

op:~ # mysql -u glance -p
mysql> drop database glance;
mysql> create database glance;

op:~ # /bin/sh -c "glance-manage db sync" glance

# start glance
op:~ # service glance-api start
op:~ # service glance-registry start
op:~ # service glance-glare start
```


---

# nova

```bash
# help
op:~ # nova help
op:~ # nova help <command>

# image
op:~ # nova image-list
op:~ # nova image-show <img_id>|<img_name>
op:~ # nova image-create <vm_id>|<vm_name> <snapshot_name>   # create snapshot from instance
op:~ # nova image-delete <img_id>|<img_name>

# flavor
op:~ # nova flavor-list
op:~ # nova flavor-show <flv_id>|<flv_name>
op:~ # nova [--ephemeral <ephemeral>] [--swap <swap>] [--is-public <is-public>] <name> <id> <ram> <disk> <vcpus>
op:~ # nova flavor-delete <flv_id>|<flv_name>

# network
op:~ # network-list
op:~ # network-show <net_id>|<net_name>
op:~ # network-create
op:~ # network-delete <net_id>|<net_name>

# instance
op:~ # nova list
op:~ # nova diagnostics <vm_id>|<vm_name>
op:~ # nova show <vm_id>|<vm_name>
op:~ # nova boot --image <img_name> --flavor <fv_name> --file /root/.ssh/authorized_keys=<pub_key> --nic net-id=<net_id> [--availability-zone ZONE:HOST] <vm_name>
op:~ # nova delete <vm_id>|<vm_name>
op:~ # nova start <vm_id>|<vm_name>
op:~ # nova stop <vm_id>|<vm_name>
op:~ # nova reboot [--hard] <vm_id>|<vm_name>
op:~ # nova suspend <vm_id>|<vm_name>  # save to disk
op:~ # nova resume <vm_id>|<vm_name>
op:~ # nova pause <vm_id>|<vm_name>    # save to cache
op:~ # nova unpause <vm_id>|<vm_name>

op:~ # nova ssh <vm_id>|<vm_name>
op:~ # nova quota-show

# service
op:~ # nova service-list
op:~ # nova service-enable <host> <binary>
op:~ # nova service-disable <host> <binary>
op:~ # nova service-delete

# hyperviror
op:~ # nova hypervisor-list
op:~ # nova hypervisor-servers <hv_id>|<hv_name>   # chcek vm on hyperviror
op:~ # nova hypervisor-show <hv_id>|<hv_name>

# other
op:~ $ nova availability-zone-list
```

---

# nova-manage

```bash
op:~ # nova-manage service list
op:~ # nova-manage host list
op:~ # nova-manage fixed list
```


---

# ovs

```bash
op:~ # ovs-vsctl show | grep -E 'Port|Bridge'
```


---

# neutron

```bash
op:~ # neutron security-group-list
op:~ # neutron security-group-rule-list
op:~ # neutron security-group-rule-delete b5373b9f-3980-4e6d-87ac-6b95dd87f709
op:~ # neutron security-group-rule-create --protocol icmp --direction ingress \ --ethertype IPv6 --remote-ip-prefix ::/0 b5373b9f-3980-4e6d-87ac-6b95dd87f709
op:~ # neutron security-group-rule-create --protocol tcp --direction ingress \ --ethertype IPv4 --port_range_min 8443 --port-range-max 8443 \ --remote-ip-prefix 0.0.0.0/0 b5373b9f-3980-4e6d-87ac-6b95dd87f709

op~: # neutron net-list
op~: # neutron net-show <neutron_id>
op~: # ip netns | grep <neutron_id>
op~: # ip netns exec qdhcp-<neutron_id> ip addr show
op~: # neutron quota-show
op~: # neutron quota-update --port 500
```


---

# swift

```bash
# get token for swift
op:~ # vi /etc/swift/proxy-server.conf
[filter:authtoken]
log_name = swift
signing_dir = /var/cache/swift
paste.filter_factory = keystonemiddleware.auth_token:filter_factory

auth_uri = http://1.2.3.4:5000/
identity_uri = http://1.2.3.4:35357/
admin_tenant_name = services
admin_user = swift
admin_password = <swift_password>
delay_auth_decision = 1
cache = swift.cache
include_service_catalog = False

op:~ # swift --os-auth-url http://1.2.3.4:5000//v3 \
--auth-version 3 \
--os-project-name services \
--os-username swift \
--os-password <swift_password> \
auth

# get token for glance
op:~ # cat /etc/glance/glance-swift.conf
user = services:glance
key = <glance_password>
auth_version = 3
auth_address = http://1.2.3.4:5000//v3
user_domain_id=default
project_domain_id=default

op:~ # swift --os-auth-url http://1.2.3.4:5000//v3 \
--auth-version 3 \
--os-project-name services \
--os-username glance \
--os-password  <glance_password> \
auth
```


```bash
op:~ # swift stat
op:~ # swift list
op:~ # swift list --lh
```


---

# other operation

## remove nova compute

```bash
op:~ # nova hypervisor-list
op:~ # mysql -u root
mysql> USE nova;
mysql> SELECT id, created_at, updated_at, hypervisor_hostname FROM compute_nodes;
mysql> DELETE FROM compute_nodes WHERE hypervisor_hostname='node1;

op:~ # nova service-list
op:~ # mysql -u root
mysql> USE nova;
mysql> SELECT id, created_at, updated_at, host FROM services;
mysql> DELETE FROM services WHERE host='node1';

op:~ # neutron agent-list
op:~ # mysql -u root
mysql> USE neutron;
mysql> SELECT id, created_at, host FROM agents;
mysql> DELETE FROM agents WHERE host='node1';

op:~ # neutron port-list
op:~ # mysql -u root
mysql> USE neutron;
mysql> SELECT id, mac_address FROM ports;
mysql> DELETE FROM ports WHERE mac_address='node1';

op:~ # cinder service-list
op:~ # mysql -u root
mysql> USE cinder;
mysql> SELECT id, created_at, updated_at, host FROM services;
mysql> DELETE FROM services WHERE host='node1';
```