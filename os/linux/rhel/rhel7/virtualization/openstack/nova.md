# nova

## cli

```bash
# help
controller:~ # nova help
controller:~ # nova help <command>

# image
controller:~ # nova image-list
controller:~ # nova image-show <img_id>|<img_name>
controller:~ # nova image-create <vm_id>|<vm_name> <snapshot_name>   # create snapshot from instance
controller:~ # nova image-delete <img_id>|<img_name>

# flavor
controller:~ # nova flavor-list
controller:~ # nova flavor-show <flv_id>|<flv_name>
controller:~ # nova [--ephemeral <ephemeral>] [--swap <swap>] [--is-public <is-public>] <name> <id> <ram> <disk> <vcpus>
controller:~ # nova flavor-delete <flv_id>|<flv_name>

# network
controller:~ # nova network-list
controller:~ # nova network-show <net_id>|<net_name>
controller:~ # nova network-create
controller:~ # nova network-delete <net_id>|<net_name>

# instance
controller:~ # nova list
controller:~ # nova diagnostics <vm_id>|<vm_name>
controller:~ # nova show <vm_id>|<vm_name>
controller:~ # nova boot --image <img_name> --flavor <fv_name> --file /root/.ssh/authorized_keys=<pub_key> --nic net-id=<net_id> [--availability-zone ZONE:HOST] <vm_name>
controller:~ # nova delete <vm_id>|<vm_name>
controller:~ # nova start <vm_id>|<vm_name>
controller:~ # nova stop <vm_id>|<vm_name>
controller:~ # nova reboot [--hard] <vm_id>|<vm_name>
controller:~ # nova suspend <vm_id>|<vm_name>  # save to disk
controller:~ # nova resume <vm_id>|<vm_name>
controller:~ # nova pause <vm_id>|<vm_name>    # save to cache
controller:~ # nova unpause <vm_id>|<vm_name>

controller:~ # nova ssh <vm_id>|<vm_name>
controller:~ # nova quota-show

# service
controller:~ # nova service-list
controller:~ # nova service-enable <host> <binary>
controller:~ # nova service-disable <host> <binary>
controller:~ # nova service-delete

# hyperviror
controller:~ # nova hypervisor-list
controller:~ # nova hypervisor-servers <hv_id>|<hv_name>   # chcek vm on hyperviror
controller:~ # nova hypervisor-show <hv_id>|<hv_name>

# security group
controller:~ # nova secgroup-list
controller:~ # nova secgroup-list-rules <security_group_id>

# other
controller:~ $ nova availability-zone-list
```

---

# nova-manage

```bash
controller:~ # nova-manage service list
controller:~ # nova-manage host list
controller:~ # nova-manage fixed list
```


---

# compute node resource overcommit

`(OR*PC)/VC`

OR: CPU overcommit ratio (virtual cores per physical core)

PC: Number of physical cores

VC: Number of virtual cores per instance

```bash
controller:~ # vi /etc/nova/nova.conf
...
cpu_allocation_ratio=8.0
ram_allocation_ratio=1.0
disk_allocation_ratio=1.0

controller:~ # systemctl restart nova-scheduler
```
