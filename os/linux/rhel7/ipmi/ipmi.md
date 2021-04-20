# ipmi

## install

```bash
centos:~ # yum install ipmitool

centos:~ # modprobe ipmi_msghandler
centos:~ # modprobe ipmi_ssif
centos:~ # lsmod | grep ipmi
```


---

## list

```bash
centos:~ # ipmitool user list [<channel number>]
centos:~ # ipmitool lan print [<channel number>]
centos:~ # ipmitool chassis status
centos:~ # ipmitool channel info
centos:~ # ipmitool sel list
centos:~ # ipmitool power status
```


---

## network

```bash
centos:~ # ipmitool lan set 1 ipsrc static|dhcp
centos:~ # ipmitool lan set 1 ipaddr <ipaddress>
centos:~ # ipmitool lan set 1 netmask <netmask>
centos:~ # ipmitool lan set 1 defgw ipaddr <gatewayip>
```


---

## power control

```bash
centos:~ # ipmitool power on|off|reset|cycle
```


---

## remote

RMCP/RMCP+: UDP port 623

```bash
centos:~ # netstat -lutnp | grep 623
centos:~ # ipmitool -I lan -H <ip> -U <user> -P <password> ...
```


---

## channel number

```
Dell: 1
HP: 2
SuperMicro: 1
```
