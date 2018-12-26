# openstack

## cli

```bash
# project
op:~ # openstack project list
op:~ # openstack project show <project>
op:~ # openstack project create --enable <project>
op:~ # openstack project set --disable <project>
op:~ # openstack project delete <project>

# user
op:~ # openstack user list
op:~ # openstack user show <user>
op:~ # openstack user create --project <project> <user>
op:~ # openstack user set --password-prompt <user>
op:~ # openstack user set --enable <user>
op:~ # openstack user delete <user>

# network
op:~ # openstack network list
op:~ # openstack network show <network>
op:~ # openstack network create --project <project> <network>             # neutron net-create
op:~ # openstack network set --enable <network>
op:~ # openstack network delete <network>

# subnet
op:~ # openstack subnet list
op:~ # openstack subnet show <subnet>
op:~ # openstack subnet create --name <subnet> <network> 172.16.1.0/24    # neutron subnet-create
```


---

# other

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

