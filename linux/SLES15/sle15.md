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
sle:~ # zypper in vim
sle:~ # zypper in mlocate
sle:~ # zypper in iputils
sle:~ # zypper in -t pattern yast2_basis

sle:~ # yast sw_single
```


`network`

```bash
sle:~ # yast lan

sle:~ # ls /etc/sysconfig/network/ifcfg-<nic>
```