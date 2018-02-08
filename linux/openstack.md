# glance

```
glance image-list
glance image-show ef647309-d560-44bb-a159-6b423dc824ca
glance image-create --name 'vsz35_446' --disk-format qcow2 \ --container-format bare --progress < vscg-3.5.0.0.446.qcow2
glance image-delete ef647309-d560-44bb-a159-6b423dc824ca
```


---

# nova

```
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

```
nova-manage service list
nova-manage host list
nova-manage fixed list
```


---

# ovs

```
op:~ # ovs-vsctl show | grep -E 'Port|Bridge'
```


---

# neutron

```
neutron security-group-list
neutron security-group-rule-list
neutron security-group-rule-delete b5373b9f-3980-4e6d-87ac-6b95dd87f709
neutron security-group-rule-create --protocol icmp --direction ingress \ --ethertype IPv6 --remote-ip-prefix ::/0 b5373b9f-3980-4e6d-87ac-6b95dd87f709
neutron security-group-rule-create --protocol tcp --direction ingress \ --ethertype IPv4 --port_range_min 8443 --port-range-max 8443 \ --remote-ip-prefix 0.0.0.0/0 b5373b9f-3980-4e6d-87ac-6b95dd87f709

neutron net-list
neutron net-show <neutron_id>
ip netns | grep <neutron_id>
ip netns exec qdhcp-<neutron_id> ip addr show
neutron quota-show
neutron quota-update --port 500
```