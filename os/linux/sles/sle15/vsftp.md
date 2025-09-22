# vsftp

## port

- ftp control: 21
- ftp data (active mode): 20

---

## server

### server - package

```bash
ftp:~ # zypper in vsftpd
ftp:~ # zypper in yast2-ftp-server
```

### server - config

- method 1 - by yast

```bash
ftp:~ # yast ftp-server
```

- method 2 - by manual

```bash
# config
ftp:~ # vi /etc/vsftpd.conf
```

```conf
# /etc/vsftpd.conf
write_enable=NO
dirmessage_enable=YES
nopriv_user=ftpsecure
local_enable=YES
anonymous_enable=YES
anon_world_readable_only=YES
syslog_enable=YES
connect_from_port_20=YES
ascii_upload_enable=YES
pam_service_name=vsftpd
listen=YES
listen_ipv6=NO
ssl_enable=NO
dsa_cert_file=
anon_mkdir_write_enable=NO
anon_root=/srv/ftp
anon_upload_enable=NO
chroot_local_user=NO
ftpd_banner=Welcome message
idle_session_timeout=900
log_ftp_protocol=YES
max_clients=10
max_per_ip=3
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=40100
# pasv_address=<nat ip>
ssl_tlsv1=YES
xferlog_enable=YES
```

### server - daemon

```bash
ftp:~ # systemctl start vsftpd
ftp:~ # systemctl enable vsftpd
```

### server - firewall

```bash
ftp:~ # firewall-cmd --permanent --add-service=ftp
ftp:~ # firewall-cmd --zone=public --permanent --add-port=40000-40100/tcp
ftp:~ # firewall-cmd --reload
```

---

## client

```bash
sle:~ $ ftp <ftp>
```
