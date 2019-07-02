# NIS

```
         +-------------------+
         ypserv         ypbind
         192.168.0.1    192.168.0.101
```


---

## Prepeare

`/etc/hosts`

```
192.168.0.1    server
192.168.0.101  client
```


---

## Server

### ypserv

```bash
# package
server:~ # yum install ypserv

# config
server:~ # vi /etc/sysconfig/network
NISDOMAIN=<nis_domain>
YPSERV_ARGS="-p 1011"

# nis domain command
server:~ # nisdomainname
server:~ # nisdomainname <nis_domain>

# config
server:~ # vi /etc/ypserv.conf
dns: no
# /etc/hosts

files: 30

xfr_check_port: yes
# master/slave, port < 1024

127.0.0.0/255.255.255.0     : * : * : none
192.168.0.0/255.255.255.0   : * : * : none
*                           : * : * : deny

# service
server:~ # systemctl enable ypserv
server:~ # systemctl start ypserv

# create nis database
server:~ # /usr/lib64/yp/ypinit -m

server:~ # cd /var/yp/
server:/var/yp # vi Makefile
server:/var/yp # make
```


### yppassword

```bash
server:~ # /etc/sysconfig/yppasswdd
...
YPPASSWDD_ARGS="--port 1012"

server:~ # systemctl enable yppasswdd
server:~ # systemctl start yppasswdd
```

### check

```bash
# check port
server:~ # ss
server:~ # ss -lutnp

# check rpc
server:~ # rpcinfo
server:~ # rpcinfo -s
server:~ # rpcinfo -p localhost
```


---

## Client

### ypbind

```bash
# package
client:~ # yum install ypbind

# config
server:~ # vi /etc/sysconfig/network
NISDOMAIN=<nis_domain>

# config
server:~ # vi /etc/yp.conf
ypserver 192.168.0.1

# config
server:~ # vi /etc/nsswitch.conf
...
passwd:     files nis sss
shadow:     files nis sss
group:      files nis sss

hosts:      files nis dns myhostname
netgroup:   files nis sss
automount:  files nis sss
...

# config via setup command
server:~ # setup
```


### check

```bash
# yptest
client:~ # yptest
client:~ # ypcat -x
client:~ # ypcat -t passwd.byname
client:~ # ypcat -kt hosts.byname

# check database
client:~ # getent passwd

# check account
cliend:~ # id <user>

# check port
client:~ # ss
client:~ # ss -lutnp

# check rpc
client:~ # rpcinfo
client:~ # rpcinfo -s
client:~ # rpcinfo -p localhost
```


### change passwd

in client, 使用者改變密碼, 系統會自動更新

```bash
client:~ $ yppasswd  # auto sync with server
```

in server 使用者改變密碼, 需管理員手動更新 db

```bash
server:~ $ passwd
server:/var/yp # make   # manual sync
```
