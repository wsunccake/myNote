# avahi

## install

```bash
fedora:~ # dnf in avahi avahi-tools
```

## service

```bash
fedora:~ # systemctl enable avahi-daemon
fedora:~ # systemctl start avahi-daemon
fedora:~ # systemctl status avahi-daemon
```

## config

```ini
[server] 控制 Avahi daemon 的全局設置。
host-name：設置設備的主機名（不包含 .local）。default 使用系統主機名。
domain-name：設置使用的域名，默認為 local。
use-ipv4：是否啟用 IPv4 支持（yes 或 no）。
use-ipv6：是否啟用 IPv6 支持（yes 或 no）。
allow-interfaces：限制 Avahi 僅在指定的網絡接口上工作（用逗號分隔）。
deny-interfaces：阻止 Avahi 在指定的網絡接口上工作。

[publish] 配置需要發佈的數據。
disable-publishing：禁用所有服務發佈（yes 或 no）。
disable-user-service-publishing：禁用用戶進程的服務發佈。
add-service-cookie：為每個服務添加隨機的 cookie，用於區分相同服務。
publish-addresses：發佈設備的 IP 地址。
publish-hinfo：發佈設備的主機信息（如操作系統和架構）。
publish-workstation：發佈工作站服務。

[reflector] 配置反射器行為（允許 Avahi 在多個網絡間轉發 mDNS）。
enable-reflector：啟用或禁用反射器功能。
reflect-ipv：是否反射 IPv4 或 IPv6 的多播數據。

[rlimits] 配置資源限制（如文件描述符數量）。
rlimit-nproc：設置允許的最大進程數。
rlimit-core：設置核心轉儲文件的大小限制。
rlimit-data：設置數據段大小限制。
```

```ini
# /etc/avahi/avahi-daemon.conf
[server]
#host-name=foo
#domain-name=local
#browse-domains=0pointer.de, zeroconf.org
use-ipv4=yes
use-ipv6=yes
#allow-interfaces=eth0
#deny-interfaces=eth1
#check-response-ttl=no
#use-iff-running=no
#enable-dbus=yes
#disallow-other-stacks=no
#allow-point-to-point=no
#cache-entries-max=4096
#clients-max=4096
#objects-per-client-max=1024
#entries-per-entry-group-max=32
ratelimit-interval-usec=1000000
ratelimit-burst=1000

[wide-area]
enable-wide-area=yes

[publish]
#disable-publishing=no
#disable-user-service-publishing=no
#add-service-cookie=no
#publish-addresses=yes
publish-hinfo=no
publish-workstation=no
#publish-domain=yes
#publish-dns-servers=192.168.50.1, 192.168.50.2
#publish-resolv-conf-dns-servers=yes
#publish-aaaa-on-ipv4=yes
#publish-a-on-ipv6=no

[reflector]
#enable-reflector=no
#reflect-ipv=no
#reflect-filters=_airplay._tcp.local,_raop._tcp.local

[rlimits]
#rlimit-as=
#rlimit-core=0
#rlimit-data=8388608
#rlimit-fsize=0
#rlimit-nofile=768
#rlimit-stack=8388608
#rlimit-nproc=3
```

## firewall

```bash
fedora:~ # firewall-cmd --add-service=mdns --permanent
fedora:~ # firewall-cmd --reload
```

## test

```bash
fedora:~ # ping $(hostname).local
fedora:~ # ssh $(hostname).local
```

```bash
fedora:~ # avahi-browse -a
fedora:~ # avahi-publish -s "My Service" _http._tcp 8080
```

## syslog

```bash
fedora:~ # journalctl -u avahi-daemon
```
