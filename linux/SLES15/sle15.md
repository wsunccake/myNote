# SLE15

## Install

安裝時, 預設 filesystem 為 btrfs, 建議使用 xfs (效能較佳)


---

## Setup


`repository`


```bash
# on local
sel:~ # mount /dev/sr0 /mnt
sle:~ # zypper rr -a
sle:~ # zypper ar /mnt/Module-Basesystem Basesystem
sle:~ # ls -d /mnt/{M,P}* zypper ar {} `basename {}`
sle:~ # zypper lr

# on http
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

# on ftp
# on nfs
```

`firewall`

```bash
sle:~ # firewall-cmd --add-service=ssh --permament
sle:~ # firewall-cmd --reload
```

`package`

```bash
sle:~ # zypper in vim
sle:~ # zypper in mlocate
sle:~ # zypper in iputils
sle:~ # zypper in -t pattern yast2_basis
```


