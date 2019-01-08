# iSCSI initiator (client)

## install

```bash
initiator:~ # yum install iscsi-initiator-utils
```


---

## port

default port 3260

```bash
initiator:~ # nc -v <iscsi_taget_ip> 3260 < /dev/null
```


---

## usage

```bash
initiator:~ # iscsiadm -m discovery
initiator:~ # iscsiadm -m discovery -o show
initiator:~ # iscsiadm -m discovery -t sendtargets -p <iscsi_taget_ip:port>
initiator:~ # iscsiadm -m discovery -o delete -p <iscsi_taget_ip:port>

initiator:~ # iscsiadm -m node
initiator:~ # iscsiadm -m node -o show
initiator:~ # iscsiadm -m node -o delete -T <iqn>
initiator:~ # iscsiadm -m node --login
initiator:~ # iscsiadm -m node --logout

initiator:~ # iscsiadm -m session
initiator:~ # iscsiadm -m session -o show

initiator:~ # cat /proc/partitions
```
