# Firewalld #


## Package ##

```bash
rhel~: # yum install firewalld
```


## Serivce ##

RHEL 7 的防火牆有兩種可以選擇, 一個是 iptables (相容之前 RHEL 6), 另一個是 firewalld (RHEL 7 才提供), 只能使用一種

```bash
rhel:~ # systemctl start firewalld.service
rhel:~ # systemctl enable firewalld.service
rhel:~ # systemctl status firewalld.service
```


## Command ##

```bash
rhel:~ # firewall-cmd --permanent --zone=public --add-rich-rule="rule family=ipv4 accept source address=192.168.68.0/24"
```


### Zone ###

firewalld 使用 zone 去管理 rule

```bash
# 顯示 zone 設定
rhel:~ # firewall-cmd [--zone=public] --list-all

rhel:~ # firewall-cmd --get-default-zone
rhel:~ # firewall-cmd --get-active-zones
rhel:~ # firewall-cmd --get-zones
rhel:~ # firewall-cmd --set-default-zone=home  # 更改 default zone

# 更改 zone 設定

# 暫時性修改 (並不會寫入設定檔), 重開 serivce 就無效
rhel:~ # firewall-cmd --new-zone=test                    # 新增 zone
rhel:~ # firewall-cmd --delete-zone=test                 # 新增 zone

# 用久性修改 (會寫入設定檔), 剛設定完須重載設定檔才會生效
rhel:~ # firewall-cmd --permanent --new-zone=test        # 新增 zone
rhel:~ # firewall-cmd --permanent --delete-zone=test     # 新增 zone

rhel:~ # firewall-cmd --reload                           # 重載設定

rhel:~ # ls /etc/firewalld/zones/*.xml                   # 設定檔
```


### Interface ###

```bash
rhel:~ # firewall-cmd [--permanent] [--zone=internal] --change-interface=eth0
```


### Service ###

```bash
rhel:~ # firewall-cmd --list-services

rhel:~ # firewall-cmd --add-service=ssh                    # 新增 service
rhel:~ # firewall-cmd --remove-service=ssh                 # 移除 service

rhel:~ # firewall-cmd --add-service={http,https,dns}       # 一次設定多個 service
```


### Source ###

```bash
rhel:~ # firewall-cmd --zone=trusted --list-sources

rhel:~ # firewall-cmd --add-source=192.168.2.0/24          # 新增 source
rhel:~ # firewall-cmd --delete-source=192.168.2.0/24       # 移除 source
```


### Port ###

```bash
rhel:~ # firewall-cmd --zone=internal --list-ports

rhel:~ # firewall-cmd --add-port=443/tcp                   # 新增 port
rhel:~ # firewall-cmd --delete-port=443/tcp                # 移除 port

# port forwarding
rhel:~ # firewall-cmd --add-forward-port=port=22:proto=tcp:toport=3753
```


### Masquerade ###

```bash
rhel:~ # firewall-cmd --add-masquerade
rhel:~ # firewall-cmd –-remove-masquerade
rhel:~ # firewall-cmd -–query-masquerade
```


### Direct ###

```bash
rhel:~ # firewall-cmd --direct --get-all-rules

rhel:~ # firewall-cmd --direct --add-rule ipv4 filter INPUT 0 -p tcp --dport 9000 -j ACCEPT
rhel:~ # firewall-cmd --permanent --direct --add-rule ipv4 filter INPUT 0 -p tcp --dport 9000 -j ACCEPT 

rhel:~ # firewall-cmd --direct --add-rule ipv6 nat POSTROUTING 1 -s fc00:db8::1/112 -j MASQUERADE
rhel:~ # firewall-cmd --permanent --direct --add-rule ipv6 nat POSTROUTING 1 -s fc00:db8::1/112 -j MASQUERADE

rhel:~ # firewall-cmd --reload
```


## Configuration ##

```bash
rhel:~ # echo "net.ipv4.ip_forward=1" > /etc/sysctl.conf
rhel:~ # sysctl -p

rhel:~ # firewall-cmd --state
```


### File ###

/usr/lib/firewalld/services

/etc/firewalld/services


### Offline ###

```bash
rhel:~ # firewall-offline-cmd --direct --add-rule ipv4 filter INPUT 0 -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
```

### Backupt ###

```bash
rhel:~ # iptables -S > firewalld_rules_ipv4
rhel:~ # ip6tables -S > firewalld_rules_ipv6
```


---

# Iptables

```bash
# list all rule
rhel:~ # iptables -L -nv

# list FORWARD chain rule
rhel:~ # iptables -L FORWARD -nv


rhel:~ # iptables -S
```