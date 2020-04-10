# neutron

## cli

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

op:~ # neutron agent-list
```

---

## ovs

```bash
op:~ # ovs-vsctl show | grep -E 'Port|Bridge'
```

