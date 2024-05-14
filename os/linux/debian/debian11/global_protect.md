# global protect

## install

```bash
debian:~ # tar zxf PanGPLinux-6.0.1-c6.tgz
debian:~ # dpkg -i GlobalProtect_deb-6.0.1.1-6.deb
```

---

## usage

```bash
debian:~ $ globalprotect connect -p <vpn server> -u <user>

debian:~ $ globalprotect
>> help
>> connect -p <vpn server> -u <user>

>> show --version
>> show --details
>> show --status
>> show --manual-gateway
>> show --host-state
>> show --notification

>> remove-user
>> disconnect
>> quit
```

---

## ui

```bash
debian:~ # tar zxf PanGPLinux-6.0.1-c6.tgz
debian:~ # dpkg -i GlobalProtect_UI_deb-6.0.1.1-6.deb

debian:~ $ globalprotect launch-ui [--recover]
```

---

## network device

```bash
debian:~ $ ip link show dev gpd0
debian:~ $ ip addr show dev gpd0
debian:~ $ ip route
```

---

## question

cannot connect to local gpd service.

```bash
debian:~ # systemctl restart gpd.service
debian:~ # systemctl status gpd.service
debian:~ # ps aux | grep Pan
```

error: default browser is not enabled

```bash
debian:~ # vi /opt/paloaltonetworks/globalprotect/pangps.xml
<GlobalProtect>
    ...
	<Settings>
		<default-browser>yes</default-browser>
        ...
	</Settings>
</GlobalProtect>
debian:~ # reboot

debian:~ # update-alternatives --config x-www-browser
debian:~ # export BROWSER=<browser path>
```
