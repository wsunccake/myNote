# lxc

## Create/Delete

```bash
debian:~ # ls /usr/share/lxc/templates

debian:~ # lxc-create -n container_name -t template
debian:~ # lxc-create -t download -n container_name

debian:~ # lxc-destroy -n container_name

debian:~ # lxc-ls
debian:~ # lxc-ls -f

debian:~ # lxc-info -n container_name

debian:~ # ls /var/lib/lxc
```

---

## Start/Stop

```bash
debian:~ # lxc-start -n container_name
debian:~ # lxc-start -n container_name -d

debian:~ # lxc-stop -n container_name

debian:~ # lxc-console -n container_name


debian:~ # lxc-attach -n u1 -- lsb_release -a
```

---

## Networking

### Bridge

```bash
debian:~ # cat /etc/network/interfaces.d/ifcfg-br0
auto br0
iface br0 inet dhcp
  bridge_ports eth0
  up /usr/sbin/brctl stp br0 off

debian:~ # cat /etc/network/interfaces.d/ifcfg-eth0
auto eth0
allow-hotplug eth0
iface eth0 inet manual
  pre-up ifconfig $IFACE up
  pre-down ifconfig $IFACE down

debian:~ # lxc-create -n container_name -t template
debian:~ # vi /var/lib/lxc/container_name/config
...
lxc.network.type = empty
->
lxc.network.type = veth
lxc.network.link = br0
lxc.network.flags = up
lxc.network.hwaddr = 00:16:3e:11:22:33

debian:~ # lxc-start -n container_name -d
```

### NAT

```bash
debian:~ # vi /etc/dnsmasq.d/lxc
bind-interfaces
except-interface=lxcbr0


debian:~ # vi /var/lib/lxc/container_name/config
...
lxc.network.type = empty
->
lxc.network.type = veth
lxc.network.link = br0
lxc.network.flags = up
lxc.network.hwaddr = 00:16:3e:xx:xx:xx


debian:~ # vi /etc/sysctl.conf
...
net.ipv4.ip_forward=1

debian:~ # sysctl -p

```

---

## Resource

```bash
debian:~ # lxc-checkconfig

debian:~ # lxc-cgroup -n container_name memroy.limit_in_bytes 256M
debian:~ # vi /var/lib/lxc/container_name/config
...
cpuset.cpus = 0,3
cpu.shares = 512
lxc.cgroup.memory.limit_in_bytes = 256M

# Autostart
lxc.start.auto = 1
lxc.start.delay = 5
lxc.start.order = 100
```
