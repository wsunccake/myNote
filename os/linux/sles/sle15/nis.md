# NIS

## rpc

```bash
sle:~ # rpcinfo [-p]
```

---

## daemon

- `ypserv`

  `ypserv` 是 NIS 伺服器最核心的服務。它的主要作用是提供 NIS 資料庫的查詢服務。當 NIS 客戶端（client）需要查詢使用者資訊、密碼、主機名稱等資料時，它會透過 RPC（Remote Procedure Call）連線到 NIS 伺服器上的 ypserv，由 ypserv 負責從 NIS 資料庫（通常是 /var/yp 目錄下的檔案）中找到所需的資訊並回傳給客戶端。簡單來說，ypserv 就是 NIS 的「總資料庫管理員」。

- `yppasswdd`

  `yppasswdd` 是一個輔助的服務，專門處理 NIS 使用者的密碼變更。當 NIS 客戶端的使用者執行 yppasswd 指令想要更改自己的密碼時，這個請求不會直接由 ypserv 處理，而是會傳送到 NIS 伺服器上的 yppasswdd。yppasswdd 接收到請求後，會負責：

  1. 驗證使用者的舊密碼。
  2. 修改 /etc/passwd 和 /etc/shadow 檔案中對應的密碼資訊。
  3. 重建 NIS 資料庫，使新的密碼生效。

  這個服務的目的是將密碼變更的作業從主要的 ypserv 分離出來，提供更安全且專職的密碼管理功能。

- `ypxfrd`

  `ypxfrd` 的作用是在 NIS 主伺服器與從屬伺服器 (slave server) 之間同步資料。在大型網路環境中，為了負載平衡或提高容錯性，通常會設置多台 NIS 從屬伺服器。ypxfrd 讓從屬伺服器能夠主動連線到主伺服器，將最新的 NIS 資料庫檔案傳輸過來，以確保主從伺服器之間的資料一致。

  簡單來說，它的功能就像是 NIS 資料庫的「資料傳輸員」，讓從屬伺服器能夠自動更新資料，而不需要管理員手動進行。

- `ypbind`

  `ypbind` 是一個 Network Information Service (NIS) 的客戶端（client）常駐程式，其主要功能是讓客戶端電腦能夠找到並連接到 NIS 伺服器。
  查詢 NIS 資料時，不知道 NIS 伺服器在哪裡。這時，ypbind 就會開始工作：

  1. 尋找伺服器： ypbind 會在網路上發出廣播，詢問「哪裡有 NIS 伺服器？」
  2. 建立連結： 當 NIS 伺服器回應時，ypbind 會記錄下伺服器的網路位址和埠號，並在客戶端和伺服器之間建立一個連結。
  3. 快取資訊： ypbind 會把這些連線資訊儲存在本地的 /var/yp/binding 目錄下，這樣之後客戶端需要查詢資料時，就可以直接使用這些快取資訊，而不用每次都重新廣播。

---

## port

- rpc / portmap : 111/tcp, 111/udp

---

## server

`package`

```bash
ypserv:~ # zypper in ypserv
ypserv:~ # zypper in yast2-nis-server
```

`config`

- method 1 - by yast

```bash
ypserv: # yast nis_server
```

- method 2 - by manual

```bash
ypserv:~ # vi /etc/ypserv.conf

ypserv:~ # vi /etc/sysconfig/ypserv
...
YPSERV_ARGS="--port 839"        # fix ypserv port for firewall
YPPASSWDD_ARGS="--port 854"     # fix yppasswdd port for firewall

ypserv:~ # vi /var/yp/securenets
255.0.0.0       127.0.0.0
255.255.255.0   192.168.0.0

ypserv:~ # vi /var/yp/Makefile
...
MINUID=1000              # set min uid
MINGID=100               # set min gid

ypserv:~ # cd /var/yp; make

ypserv:~ # nisdomainname <nisdomainname>
ypserv:~ # ypdomainname <nisdomainname>
ypserv:~ # domainname <nisdomainname>

ypserv:~ # nisdomainname > /etc/defaultdomain
```

```conf
# /etc/ypserv.conf
#
# ypserv.conf   In this file you can set certain options for the NIS server,
#               and you can deny or restrict access to certain maps based
#               on the originating host.
#
#               See ypserv.conf(5) for a description of the syntax.
#

# Some options for ypserv. This things are all not needed, if
# you have a Linux net.

# How many map file handles should be cached ?
files: 30

# Should we register ypserv with SLP? Only available if SLP support
# is compiled in. Deprecated functionality.
slp: no
# After how many seconds we should re-register ypserv with SLP?
slp_timeout: 3600

# xfr requests are only allowed from ports < 1024
xfr_check_port: yes

# The following, when uncommented,  will give you shadow like passwords.
# Note that it will not work if you have slave NIS servers in your
# network that do not run the same server as you.
# IMPORTANT: this rules will be ignored for IPv6 connections!

# Host                     : Domain  : Map              : Security
#
# *                        : *       : passwd.byname    : port
# *                        : *       : passwd.byuid     : port

# Not everybody should see the shadow passwords, not secure, since
# under MSDOG everbody is root and can access ports < 1024 !!!
*                          : *       : shadow.byname    : port
*                          : *       : passwd.adjunct.byname : port

# If you comment out the next rule, ypserv and rpc.ypxfrd will
# look for YP_SECURE and YP_AUTHDES in the maps. This will make
# the security check a little bit slower, but you only have to
# change the keys on the master server, not the configuration files
# on each NIS server.
# If you have maps with YP_SECURE or YP_AUTHDES, you should create
# a rule for them above, that's much faster.
# *                        : *       : *                : none
```

`daemon`

```bash
ypserv:~ # systemctl start ypserv
ypserv:~ # systemctl enable ypserv
```

`firewall`

```bash
ypserv:~ # firewall-cmd --permanent --add-port=839/tcp
ypserv:~ # firewall-cmd --permanent --add-port=839/udp
ypserv:~ # firewall-cmd --permanent --add-port=854/udp
ypserv:~ # firewall-cmd --permanent --add-port=854/tcp
ypserv:~ # firewall-cmd --reload
```

---

## client

`package`

```bash
yp:~ # zypper in ypbind
yp:~ # zypper in yast2-nis-client
```

`config`

- method 1 - yast

```bash
ypserv: # yast nis
```

- method 2 - by manual

```bash
yp:~ # vi /etc/yp.conf
ypserver <ypserv_ip>
domain <nisdomainname> [broadcast]

yp:~ # tail -1 /etc/passwd
+::::::

yp:~ # tail -1 /etc/group
+:::

yp:~ # tail -1 /etc/shadow
+

yp:~ # vi /etc/nsswitch.conf
...
passwd: compat
group:  compat
shadow: compat
...

yp:~ # vi /etc/pam.d/common-account
account required        pam_unix.so     try_first_pass

yp:~ # vi /etc/pam.d/common-auth
auth    required        pam_env.so
auth    required        pam_unix.so     try_first_pass

yp:~ # vi common-password
password        requisite       pam_cracklib.so
password        required        pam_unix.so     use_authtok nullok shadow try_first_pass
# password        optional        pam_exec.so     seteuid /usr/bin/make -C /var/yp

yp:~ # vi common-session
session optional        pam_systemd.so
session required        pam_limits.so
session required        pam_unix.so     try_first_pass
session optional        pam_umask.so
session optional        pam_env.so

yp:~ # nisdomainname <nisdomainname>

yp:~ # nisdomainname > /etc/defaultdomain
```

```conf
### /etc/yp.conf is a symlink to /run/netconfig/yp.conf
### autogenerated by netconfig!
#
# Before you change this file manually, consider to define the
# static NIS configuration using the following variables in the
# /etc/sysconfig/network/config file:
#     NETCONFIG_NIS_STATIC_DOMAIN[_<number>]
#     NETCONFIG_NIS_STATIC_SERVERS[_<number>]
# or disable NIS configuration updates via netconfig by setting:
#     NETCONFIG_NIS_POLICY=''
#
# See also the netconfig(8) manual page and other documentation.
#
### Call "netconfig update -f" to force adjusting of /etc/yp.conf.
ypserver 192.168.100.1
```

`daemon`

```bash
yp:~ # systemctl start ypbind
yp:~ # systemctl enable ypbind
```

`test`

```bash
yp:~ # getent passwd
```
