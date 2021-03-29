# SLE15

## Validate

```bash
sle:~ # ls SLE-15-SP2-Full-x86_64-GM-Media1.iso SLE-15-SP2-Full-x86_64-GM-Media2.iso

sle:~ # vi sle15sp2_sha256.txt
938dd99becf3bf29d0948a52d04bcd1952ea72621a334f33ddb5e83909116b55  SLE-15-SP2-Full-x86_64-GM-Media1.iso
c4c9393c35feffd3ffaea4a8860ae7428fe7bf996d202c4582a3abc1c4228604  SLE-15-SP2-Full-x86_64-GM-Media2.iso

sle:~ # sha256sum -c sle15sp2_sha256.txt
sle:~ # sha256sum SLE-15-SP2-Full-x86_64-GM-Media1.iso
```


---

## Install

安裝時, 預設 filesystem 為 btrfs, 建議使用 xfs (效能較佳)


---

## Setup


`repository`

```bash
# on local
sle:~ # mount /dev/sr0 /mnt
sle:~ # zypper rr -a
sle:~ # zypper ar /mnt/Module-Basesystem Basesystem
sle:~ # ls -d /mnt/{M,P}* | xarg -i zypper ar {} `basename {}`
sle:~ # zypper lr
sle:~ # ls /etc/zypp/repos.d/
sle:~ # yast repositories


# on http for apache2
sle:~ # zypper in apache2
sle:~ # systecmctl enable apache2
sle:~ # systecmctl start apache2
sle:~ # vi /etc/apache2/conf.d/repo.conf
Alias "/repo" "/mnt/"
<Directory "/mnt/">
	Options Indexes

	<IfModule !mod_access_compat.c>
		Require all granted
	</IfModule>
	<IfModule mod_access_compat.c>
		Order allow,deny
		Allow from all
	</IfModule>
</Directory>

sle:~ # systecmctl restart apache2
sle:~ # curl http://127.0.0.1/repo/
sel:~ # zypper ar http://127.0.0.1/repo/Module-Basesystem/ Module-Basesystem


# on http for nginx
sle:~ # zypper in ngin
sle:~ # systecmctl enable nginx
sle:~ # systecmctl start nginx
sle:~ # vi /etc/nginx/conf.d/repo.conf
server {
        listen 8080;
        listen [::]:8080;

        server_name .example.com;
        root /mnt;

        location / {
                autoindex on;
        }
}

sle:~ # systecmctl restart nginx
sle:~ # curl http://127.0.0.1:8080/
sle:~ # zypper ar http://127.0.0.1/Module-Basesystem/ Module-Basesystem


# on ftp
# on nfs
```


`firewall`

```bash
sle:~ # firewall-cmd --add-service=ssh,http --permament
sle:~ # firewall-cmd --add-ports=8080/tcp --permament
sle:~ # firewall-cmd --reload

sle:~ # yast firewall
```


`package`

```bash
sle:~ # zypper in vim mlocate
sle:~ # zypper in iputils psmisc
sle:~ # zypper in -t pattern yast2_basis

sle:~ # yast sw_single
```


`network`

```bash
sle:~ # yast lan

sle:~ # ls /etc/sysconfig/network/ifcfg-<nic>

sle:~ # ifup eth0
sle:~ # ifdown eth0
sle:~ # ifstatus eth0
sle:~ # ifprobe eth0
```


`sys log`

```bash
sle:~ # zypper in rsyslog
sle:~ # systemctl enable rsyslog
sle:~ # systemctl start rsyslog

sle:~ # vi /etc/systemd/journald.conf
ForwardToSyslog=yes
...

sle:~ # systemctl restart systemd-journald

sle:~ # journalctl -f
sle:~ # journalctl -n 100 -f
# log level: "emerg" (0), "alert" (1), "crit" (2), "err" (3), "warning" (4), "notice" (5), "info" (6), "debug" (7)
sle:~ # journalctl -p err
sle:~ # journalctl -p 3
```

`fs`

```bash
sle:~ # vi /etc/fstab
sle:~ # mount -a
sle:~ # mount /dev/sda1 <mnt>
sle:~ # mount -oloop image.iso <mnt>
sle:~ # mount -oremount,rw <mnt>
sle:~ # mount -oremount,ro <mnt>
sle:~ # mount -t iso9660 /dev/sr0 <mnt>
sle:~ # cat /etc/mtab
sle:~ # cat /proc/mounts
sle:~ # umount <mnt>
sle:~ # fuser -l
sle:~ # fuser -mv <mnt>
sle:~ # fuser -mk <mnt>
sle:~ # fusermount /dev/sda1 <mnt>
sle:~ # fusermount -u <mnt>

sle:~ # lsblk [-fs|-p]
sle:~ # df -h
sle:~ # du -hs [.|*]
sle:~ # cat /proc/partitions

sle:~ # fdisk [-l] /dev/sda
sle:~ # gdisk [-l] /dev/sda
sle:~ # parted [-l] /dev/sda
sle:~ # partprobe

sle:~ # mkfs -t xfs /dev/sda1
sle:~ # mkfs.xfs /dev/sda1
sle:~ # mkswap  /dev/sda2
```


---

## security

### fail2ban

```bash
sle:~ # zypper addrepo https://download.opensuse.org/repositories/network:utilities/SLE_15_SP2/network:utilities.repo
sle:~ # zypper refresh
sle:~ # zypper install python-pyinotify

sle:~ # zypper addrepo https://download.opensuse.org/repositories/security/SLE_15_SP2/security.repo
sle:~ # zypper refresh
sle:~ # zypper install fail2ban

sle:~ # systemctl enable fail2ban --now
```
