# pid 1

## Systemd

```bash
# list all
systemctl list-units --type=service

# stop / disable
systemctl stop <service>
systemctl disable <service>
systemctl mask <service>

# status
systemctl status <service>

# start / enable
systemctl umask <service>
systemctl enable <service>
systemctl start <service>
```

## SysVinit

```bash
# lit all
service --status-all
ls /etc/init.d/

# stop / disable
service <service> stop
service <service> disable
/etc/init.d/<service> stop
/etc/init.d/<service> disable

# status
service <service> status
/etc/init.d/<service> status

# start / enable
service <service> enable
service <service> start
/etc/init.d/<service> enable
/etc/init.d/<service> start
```

## Upstart

```bash
# list all
initctl list

# stop / disable
stop <service>
echo manual > /etc/init/<service>.override

# status
status <service>

# start / enable
rm /etc/init/<service>.override
start <service>
```

## OpenRC

```bash
# list all
rc-service --list

# stop / disable
rc-service <service> stop
rc-update del <service> default

# status
rc-service <service> status

# start / enable
rc-update add <service> default
rc-service <service> start
```

## distro

- Systemd

Ubuntu 15.04~
Debian 8~
Fedora
CentOS 7~
RHEL / Red Hat Enterprise Linux 7~

- SysVinit

Slackware
Debian ~7
CentOS ~6
RHEL / Red Hat Enterprise Linux ~6

- Upstart

Ubuntu 9.10~14.10

- OpenRC

Gentoo
Alpine Linux
