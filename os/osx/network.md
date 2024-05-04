# network

## networksetup

```bash
osx:~ # networksetup -listnetworkserviceorder                             # 顯示所有可連線裝置
osx:~ # networksetup -ordernetworkservices "Ethernet" "Wi-Fi" "" ...      # 設定連線裝置優先順序

osx:~ # networksetup -getairportpower en1             # 顯示裝置開關狀態
osx:~ # networksetup -setairportpower en1 on          # 開裝置
osx:~ # networksetup -setairportpower en1 off         # 關裝置

osx:~ # networksetup -getairportnetwork en1               # 顯示無線網路連線狀態
osx:~ # networksetup -setairportnetwork en1 ssid passwd   # 無線網路連線

osx:~ # networksetup -removeallpreferredwirelessnetworks en1        # 移除所有 prefer ssid
osx:~ # networksetup -removeallpreferredwirelessnetwork en1 <ssid>  # 移除特定 prefer ssid

osx:~ # networksetup -setdhcp en1

osx:~ # networksetup -setdnsservers <networkservice> 8.8.8.8 9.9.9.9     # 設定 DNS
```

---

## ping

```bash
osx:~ # ping [-S <src_addr>] [-c <n>] <dest_addr>
# 在 multi nic or multi subnet, 使用 -S 代替 -I 指定特地 interface/ip
# 避免出現 ping: invalid multicast interface: 訊息
```

---

## netstat

```bash
osx:~ # netstat -rn
osx:~ # netstat -an -f inet
osx:~ # netstat -an -p tcp
osx:~ # netstat -an -p udp
```

---

## route

顯示或設定 router

```bash
osx:~ # route -nv get <src_ip>                      # 顯示透過那個 router 連線到 <ip>
osx:~ # route -n flush                              # 清除所有 routing rule
osx:~ # route -n add -inet default <gw_ip>          # 設定 default gateway
osx:~ # route -n add <dest_ip>/<prefix> <src_ip>    # 增加特定 routing rule, from <src_ip> to <dest_ip>, 用於 multi nic
osx:~ # route -n del <dest_ip>/<prefix> <src_ip>    # 刪除特定 routing rule
```

---

## nc

```bash
# check port
osx:~ # nc -v -w1 <ip> <port> < /dev/null
osx:~ # nc -v -w1 <ip> <port1>-<port2> < /dev/null

# chat
server:~ # nc -l <port> # server listen port
client:~ # nc <server_ip> <server_port>

# file transfer
server:~ # nc -l <port> < file.txt
client:~ # nc <server_ip> <server_port> > file.txt

server:~ # nc -l <port> < file.txt
client:~ # nc <server_ip> <server_port> > file.txt

server:~ # tar -cvf – <dir> | nc -l <port>
client:~ # nc -n <server_ip> <server_port> | tar xvf -

server:~ # tar -cvf – <dir> | gzip |nc -l <port>
client:~ # nc -n <server_ip> <server_port> | gzip -d | tar xvf -

# shell
server:~ # nc -l <port> -e /bin/sh
client:~ # nc <server_ip> <server_port>
```

---

## pfctl

Packet Filter, 相當是 osx 使用的防火牆

```bash
osx:~ # pfctl -e                # 啟動 PF
osx:~ # pfctl -d                # 停用 PF
osx:~ # pfctl -f /etc/pf.conf   # 重新載入 pf.conf
osx:~ # pfctl -nf /etc/pf.conf  # 檢查 PF 語法是否正確 (未載入)

osx:~ # pfctl -sn   # 現階段 NAT 的規則 = pfctl -s nat
osx:~ # pfctl -sr   # 現階段過濾的規則 = pfctl -s rules
osx:~ # pfctl -ss   # 現階段封包運作狀態 = pfctl -s state
osx:~ # pfctl -si   # 現階段過濾封包的統計資料 = pfctl -s info
osx:~ # pfctl -sa   # 現階段所有統計的資料 = pfctl -s all
osx:~ # pfctl -sm = pfctl -s memory
osx:~ # pfctl -sq   # 目前佇列 = pfctl -s queue
osx:~ # pfctl -vsr  # 現階段過濾封包的統計資料 = pfctl -vs rules

osx:~ # pfctl -F nat    # 清空 NAT 規則
osx:~ # pfctl -F queue  # 清空佇列
osx:~ # pfctl -F rules  # 清空封包過濾規則
osx:~ # pfctl -F all    # 清空所有的規則
osx:~ # pfctl -F info   # 清空計數器
osx:~ # pfctl -F Tables
```

---

## airport

```bash
osx:~ # /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --scan
osx:~ # /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --getinfo
osx:~ # /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --disassociate
```
