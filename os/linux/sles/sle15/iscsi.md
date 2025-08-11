# iscsi 0 lio

## target

`package`

```bash
target:~ # zypper in yast2-iscsi-lio-server
```

`device`

```bash
# virtual disk
target:~ # dd if=/dev/zero of=/iscsi/lun.img bs=500M count=1

# real disk
target:~ # lsblk /dev/vda
```

`config`

```bash
# config by yast
target:~ # yast iscsi-lio-server

# config by cli
target:~ # targetcli
/> ls

## config backstore
/> cd /backstores/fileio
/backstores/fileio> create <name> <dev_or_file>
/backstores/fileio> delete <name>
/backstores/fileio> create lun.img /iscsi/lun.img
/backstores/fileio> delete lun.img

/> /backstores/fileio create lun.img /iscsi/lun.img
/> /backstores/fileio delete lun.img

## config iscsi
### iqn: iscis qualified name
### wwn: world wide name
### iqn.yyyy-mm.<reversed domain name>:identifier
### iqn.年年-月.單位網域名的反轉寫法  :這個分享的target名稱
# create iqn
/> /iscsi create <iqn>
/> /iscsi create iqn.2019-09.com.example:3916f831af3a496db8bd
# create lun
/> /iscsi/<iqn>/tpg1/luns create /backstores/fileio/lun.img
# create portal
/> /iscsi/<iqn>/tpg1/portals create 0.0.0.0 3260
# set acl
## without auth
/> /iscsi/<iqn>/tpg1 set attribute authentication=0
/> /iscsi/<iqn>/tpg1 set attribute demo_mode_write_protect=0
/> /iscsi/<iqn>/tpg1 set attribute generate_node_acls=1
/> /iscsi/<iqn>/tpg1 set attribute cache_dynamic_acls=1

# create acl
/> /iscsi/<iqn>/tpg1/acls create <wwn>
/> /iscsi/<iqn>/tpg1/acls create iqn.2019-09.com.example:server1
## set acl with password
# authentication by target
/> /iscsi/<iqn>/tpg1/acls/<wwn> set auth userid=<user>
/> /iscsi/<iqn>/tpg1/acls/<wwn> set auth password=<password>
# authentication by initiator
/> /iscsi/<iqn>/tpg1/acls/<wwn> set auth mutual_userid=<user>
/> /iscsi/<iqn>/tpg1/acls/<wwn> set auth mutual_password=<password>

# save & exit
/> saveconfig
/> exit

# config file
target:~ # vi /etc/target/saveconfig.json
```

`daemon`

```bash
target:~ # systemctl enable targetcli
target:~ # systemctl start targetcli
```

---

## initiator

`package`

```bash
initiator:~ # zypper in open-iscsi
initiator:~ # zypper in yast2-iscsi-client
```

`config`

```bash
initiator:~ # yast iscsi-client
```

`usage`

```bash
initiator:~ # iscsiadm -m discovery
initiator:~ # iscsiadm -m discovery -o show
initiator:~ # iscsiadm -m discovery -t sendtargets -p <taget_ip:taget_port>
initiator:~ # iscsiadm -m discovery -o delete -p <taget_ip:taget_port>

initiator:~ # iscsiadm -m node
initiator:~ # iscsiadm -m node -o show
initiator:~ # iscsiadm -m node -o delete -T <iqn>
initiator:~ # iscsiadm -m node --login
initiator:~ # iscsiadm -m node --logout

initiator:~ # iscsiadm -m session
initiator:~ # iscsiadm -m session -o show

initiator:~ # cat /proc/partitions
initiator:~ # lsblk
```
