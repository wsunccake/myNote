# nova

## cli

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

