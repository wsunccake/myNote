# ubuntu 26.04

## network

### nic

```bash
ubuntu:~ # lspci -v
ubuntu:~ # ls -l /sys/class/net/
ubuntu:~ # ip link
```

### ip

`/etc/netplan/00-installer-config.yaml`

```yaml
network:
  ethernets:
    ens160:
      addresses:
        - 192.168.10.123/24
      match:
        macaddress: 00:11:22:33:44:55
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
        search: []
      routes:
        - to: default
          via: 192.168.10.254
      set-name: ens160
    ens192:
      dhcp4: true
      dhcp6: true
      accept-ra: true
    ens224:
      dhcp4: false
      dhcp6: false
      accept-ra: false
      link-local: []
  version: 2
```

- ens160: up nic, static ip
- ens192: up nic, dhcp / dynamic ip
- ens224: up nic, no ip

```bash
ubuntu:~ # netplan try
ubuntu:~ # netplan apply
ubuntu:~ # ip addr
```

### IPv4 & IPv6

- Disable IPv6 with Interface

`/etc/netplan/00-installer-config.yaml`

```yaml
#
network:
  version: 2
  renderer: networkd
  ethernets:
    ens160:
      addresses:
        - 192.168.10.123/24
      match:
        macaddress: 00:11:22:33:44:55
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
        search: []
      routes:
        - to: default
          via: 192.168.10.254
      set-name: ens160
      # === 以下為 ens160 新增的停用 IPv6 設定 ===
      dhcp6: false
      accept-ra: false
      link-local: [ipv4]

    ens192:
      dhcp4: true
      # === 以下為 ens192 修改的停用 IPv6 設定 ===
      dhcp6: false
      accept-ra: false
      link-local: [ipv4]

    ens224:
      dhcp4: false
      dhcp6: false
      accept-ra: false
      link-local: [ipv4] # 建議同步改成 [ ipv4 ]，防止產生 IPv6 本地網址
```

- Dsiable IPv6 with Sysctl

`/etc/sysctl.d/99-disable-ipv6.conf`

```ini
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
```

```bash
ubuntu:~ # sysctl --system
```

- Setup IPv4 High Priority

gai 是 GetAddrInfo 的縮寫。在 Linux 中，幾乎所有應用程式（例如 curl、wget、ssh 或您的瀏覽器）在連線前，都會呼叫系統底層一個叫做 getaddrinfo() 的函式，來決定要把網域名稱解析成 IPv4 還是 IPv6。

`/etc/gai.conf`

```bash
precedence ::ffff:0:0/96  100
```

### systemd-resolved

```bash
# package
ubuntu:~ # apt install systemd-resolved

# service
ubuntu:~ # systemctl status systemd-resolved
ubuntu:~ # systemctl enable systemd-resolved
ubuntu:~ # systemctl start  systemd-resolved

# config
ubuntu:~ # cat /etc/resolv.conf

# setup cache
ubuntu:~ # cat /etc/systemd/resolved.conf
[Resolve]
Cache=yes                         # 開啟快取功能（預設即為開啟，上限固定為 4096 筆）
DNSCacheSize=8192                 # 自訂快取數量上限（預設為 4096，最高可至 16777216）
                                  # 舊版 systemd 的快取數量固定為 4096 且無法調整。
                                  # systemd 261+，即可使用 DNSCacheSize= 自訂數量。
StaleResponsesSec=3600            # 當 DNS 伺服器壞掉時，允許使用過期 1 小時(3600秒)內的舊快取
MulticastDNS=no                   # 對外若已經找不到，就不要找對內
LLMNR=no                          # 對外若已經找不到，就不要找對內
DNSStubListenerExtra=172.17.0.1   # 讓 Docker 容器（透過 Gateway IP 172.17.0.1）可以使用 Host 的 DNS 快取

ubuntu:~ # resolvectl status
ubuntu:~ # resolvectl flush-caches
ubuntu:~ # resolvectl show-cache
ubuntu:~ # resolvectl statistics
ubuntu:~ # resolvectl query google.com
```
