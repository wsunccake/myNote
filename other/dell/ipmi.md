# IPMI

## install

```bash
rocky:~ # dnf install ipmitool
```

---

## Usage

```bash
rocky:~ # ipmitool -I lanplus -H <hostname> -U <username> -P <password> <command>
rocky:~ # IPMI_CMD="ipmitool -I lanplus -H <hostname> -U <username> -P <password>"

rocky:~ # $IPMI_CMD fru [print [0]]
rocky:~ # $IPMI_CMD user list
rocky:~ # $IPMI_CMD lan print
```
