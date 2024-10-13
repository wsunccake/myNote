# neutron

## cli

```bash
op:~ # neutron security-group-list
op:~ # neutron security-group-rule-list
op:~ # neutron security-group-rule-delete <security_group_id>
op:~ # neutron security-group-rule-create --protocol icmp --direction ingress \
  --ethertype IPv6 --remote-ip-prefix ::/0 <security_group_id>
op:~ # neutron security-group-rule-create --protocol tcp --direction ingress \
  --ethertype IPv4 --port_range_min <port> --port-range-max 8443 \
  --remote-ip-prefix 0.0.0.0/0 <security_group_id>
op:~ # neutron security-group-rule-create --direction egress --ethertype IPv4|IPv6 <security_group_id>
op:~ # neutron security-group-rule-create --direction ingress --ethertype IPv4|IPv6 <security_group_id>

op~: # neutron net-list
op~: # neutron net-show <neutron_id>
op~: # ip netns | grep <neutron_id>
op~: # ip netns exec qdhcp-<neutron_id> ip addr show
op~: # neutron quota-show
op~: # neutron quota-update --port 500

op:~ # neutron agent-list
```

---

## ovs

```bash
op:~ # ovs-vsctl show | grep -E 'Port|Bridge'
```


---

## conf

```bash
op:~ # vi /etc/neutron/plugins/ml2/openvswitch_agent.ini

[agent]
bridge_mappings = physnet1:br-floating,physnet2:br-prv,physnet3:br<xxx>
...


op:~ # vi /etc/neutron/plugins/ml2/ml2_conf.ini
[ml2]
physical_network_mtus = physnet1:1500,physnet2:1500,physnet3:1500
...

[ml2_type_vlan]
network_vlan_ranges = physnet1,physnet2:2141:2150,physnet3
...


op:~ # service neutron-plugin-openvswitch-agent restart
```
