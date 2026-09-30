# Linux Network 診斷備忘

介面 **errors / drops** 與頻寬飽和是兩件事；**TcpRetransSegs** 高也不等於線路已打滿。先看連不連得上、再看丟包／錯誤、最後才看吞吐與 `%ifutil`。體感卡、但 `%idle` 低時先對 [processor.md](processor.md)；髒頁寫不回、本機 I/O 等網路檔案系統時對 [disk.md](disk.md) / [memory.md](memory.md)。

介面名稱用通用的 `enp0s3`（有的機器是 `eth0`）；不要把筆記裡的名字當成固定硬體型號。

---

## ip

ip 是看「位址、路由、介面計數」的第一站。連結層錯誤與丟包用 `ip -s link`；位址與路由用 `ip addr` / `ip route`。

```bash
linux:~$ ip -br addr
lo               UNKNOWN        127.0.0.1/8 ::1/128
enp0s3           UP             10.0.0.15/24 fe80::a00:27ff:fe8a:1/64
```

```bash
linux:~$ ip -s link show enp0s3
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:8a:00:01 brd ff:ff:ff:ff:ff:ff
    RX:  bytes packets errors dropped  missed  mcast
     128400000  182000      0     120       0   4100
    TX:  bytes packets errors dropped carrier collsns
      96400000  141000      0       0       0       0
```

```bash
linux:~$ ip route
default via 10.0.0.1 dev enp0s3 proto dhcp metric 100
10.0.0.0/24 dev enp0s3 proto kernel scope link src 10.0.0.15 metric 100
```

- **UP / LOWER_UP**：
  - 管理上啟用，且實體層認為有連結。只有 UP、沒有 LOWER_UP：常是網線／對端沒起來，不是應用程式問題。
- **mtu**：
  - 這條介面的最大傳輸單元。路徑 MTU 問題見 traceroute / tracepath，不要只在這裡猜。
- **RX/TX bytes、packets**：
  - 開機以來累計收／送。速率要自己對兩次取樣相減，或改看 `sar -n DEV` / iftop。
- **errors**：
  - 💡 驅動／硬體回報的錯誤（CRC、frame 等，細項常在 ethtool -S）。
  - 持續增加才有意義；單次快照的絕對值可能是很久以前累積的。
- **dropped**：
  - 核心或驅動丟棄的封包（緩衝不夠、過濾等）。
  - ⚠️ drops 高、同時 `%ifutil` 很低：比較像本機收／送佇列或設定問題，不是「線路已經塞滿」。
- **overrun / fifo**（部分輸出寫在 errors 細項或 ethtool -S）：
  - 接收端來不及從硬體搬到記憶體時常見。對照 [processor.md](processor.md) 的 `%soft` / `NET_RX` 是否打滿單顆邏輯 CPU。
- **carrier / collsns（TX）**：
  - carrier 錯誤與碰撞。現代全雙工交換環境 collsns 應接近 0；持續增加要查雙工／連線品質。
- **default via …**：
  - 預設路由。ping 外網失敗時先確認有沒有 default、以及 `dev` 是否指到預期介面。

`ip -s link` 的計數與 `/proc/net/dev` 同源；歷史趨勢交給後面的 `sar -n DEV`。

---

## ethtool

ethtool 讀網卡驅動回報的連線模式、 stat 計數與 offload。確認「協商到多少速度／是否 full duplex」，以及 errors 的細項名稱。

```bash
linux:~$ ethtool enp0s3
Settings for enp0s3:
	Supported link modes:   10baseT/Half 10baseT/Full
	                        100baseT/Half 100baseT/Full
	                        1000baseT/Full
	Speed: 1000Mb/s
	Duplex: Full
	Auto-negotiation: on
	Link detected: yes
```

```bash
linux:~$ ethtool -S enp0s3 | grep -E 'err|drop|over|fifo|miss|crc' | head
     rx_errors: 0
     tx_errors: 0
     rx_dropped: 120
     rx_fifo_errors: 0
     rx_missed_errors: 0
     rx_crc_errors: 0
```

- **Speed / Duplex**：
  - 💡 實際協商結果。預期千兆卻卡在 100Mb/s Half：吞吐天花板與碰撞行為會完全不同，看起來像「網路很慢」。
- **Link detected**：
  - `yes` / `no`。對應 ip 的 LOWER_UP。
- **ethtool -S**：
  - 驅動私有計數，名稱因驅動而異。
  - 優先盯 **rx_errors**、**rx_crc_errors**、**rx_dropped**、**rx_fifo_errors**、**rx_missed_errors**、**tx_errors**。
  - ⚠️ 這些是累計值。診斷時隔幾秒再跑一次，看誰在「這一分鐘」往上爬。

需要對該介面有權限（常要 root）。虛擬網卡上部分欄位會是固定或不支援。

---

## nmcli

nmcli 是 NetworkManager 的命令列。用來確認「NM 認為這條連線有沒有起來、拿到什麼 IP／DNS」，不是看每秒吞吐。

```bash
linux:~$ nmcli -t -f DEVICE,TYPE,STATE,CONNECTION device
enp0s3:ethernet:connected:Wired connection 1
lo:loopback:unmanaged:
```

```bash
linux:~$ nmcli -f GENERAL,IP4,IP6,DHCP4 device show enp0s3
GENERAL.DEVICE:                         enp0s3
GENERAL.STATE:                          100 (connected)
IP4.ADDRESS[1]:                         10.0.0.15/24
IP4.GATEWAY:                            10.0.0.1
IP4.DNS[1]:                             10.0.0.1
```

- **STATE / connected**：
  - NM 層的連線狀態。`disconnected` 或 `unavailable` 時，先別往應用層挖。
- **IP4.ADDRESS / GATEWAY / DNS**：
  - 目前生效的位址、閘道、DNS。可與 `ip addr`、`resolvectl` 交叉核對。
- 未跑 NetworkManager 的機器（純 systemd-networkd、或手寫 ifupdown）上 nmcli 會失敗或資訊不完整，改看 networkctl / `ip`。

---

## networkctl

networkctl 是 systemd-networkd 一側的狀態總覽。有跑 networkd 時用來確認 Link / Network / Address 是否 configured。

```bash
linux:~$ networkctl status enp0s3
● 2: enp0s3
                   Link File: /usr/lib/systemd/network/99-default.link
                Network File: /etc/systemd/network/10-enp0s3.network
                        Type: ether
                       State: routable (configured)
                        Path: pci-0000:00:03.0
                      Driver: e1000
            Hardware Address: 08:00:27:8a:00:01
                         MTU: 1500
                       QDisc: fq_codel
  IPv4 Address: 10.0.0.15/24
       Gateway: 10.0.0.1
           DNS: 10.0.0.1
```

- **State: routable (configured)**：
  - 💡 有位址且認為可路由。`degraded`、`failed`、`linger` 等要先讀 journal 與 `.network`，不是先抓包。
- **Network File**：
  - 實際套用到的 unit 檔路徑。改錯檔、或被另一個管理器搶走時，這裡會對不上預期。
- 與 nmcli 互斥管理同一介面時，以「誰真正在管」為準；兩個都改最容易出現位址閃爍。

---

## ss

ss 取代舊的 netstat，用來看「現在有哪些 socket、各狀態有多少」。查連線數與監聽埠用它；看介面錯誤用 ip / ethtool。

```bash
linux:~$ ss -s
Total: 412
TCP:   128 (estab 24, closed 80, orphaned 0, timewait 72)

Transport Total     IP        IPv6
RAW	  1         0         1
UDP	  12        8         4
TCP	  128       100       28
INET	  141       108       33
FRAG	  0         0         0
```

```bash
linux:~$ ss -tan state established | head
Recv-Q Send-Q Local Address:Port    Peer Address:Port
0      0      10.0.0.15:22         10.0.0.8:51234
0      0      10.0.0.15:443        10.0.0.20:49821
```

```bash
linux:~$ ss -lntup
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:Port Process
tcp   LISTEN 0      128        0.0.0.0:22           0.0.0.0:*     users:(("sshd",pid=812,fd=3))
tcp   LISTEN 0      511        0.0.0.0:443          0.0.0.0:*     users:(("nginx",pid=1204,fd=8))
udp   UNCONN 0      0        127.0.0.53%lo:53      0.0.0.0:*     users:(("systemd-resolve",pid=640,fd=13))
```

- **estab**：
  - 已建立的 TCP 數。對照應用預期的連線規模。
- **timewait**：
  - 💡 處於 TIME-WAIT 的 socket 數。
  - ⚠️ TIME-WAIT **本身不是連線洩漏**。短連線很頻繁（HTTP 短請求、健康檢查）時，TIME-WAIT 偏高是正常收尾。真正要查的是 **estab** 是否單調漲到異常、或 Recv-Q/Send-Q 長期堆高。
- **orphaned**：
  - 已無對應行程的 socket。持續升高才值得查行程異常退出。
- **Recv-Q / Send-Q**：
  - 已建立連線上，尚未被應用讀走／尚未送出的位元組。
  - LISTEN 上意義不同：Recv-Q 是已完成交握、等 `accept` 的連線數；Send-Q 是 backlog 上限。這不是 SYN 半開佇列。
  - ⚠️ 已建立連線的 Recv-Q 長期很大：應用讀太慢。Send-Q 長期很大：對端或路徑收太慢。這和介面 drops 要分開看。
- **State**：
  - `LISTEN`、`ESTAB`、`TIME-WAIT`、`SYN-SENT`、`CLOSE-WAIT` 等。
  - `CLOSE-WAIT` 堆很多：本端應用沒關掉 socket（常見於程式沒讀完就不管 fd）。
  - `SYN-SENT` 堆很多：連出去沒回應（防火牆、對端沒聽、路由黑洞）。
- **-lntup**：
  - 聽哪些埠、哪個行程（`-p` 常要 root）。確認服務有沒有真的 bind 到預期位址。

---

## lsof

lsof 在網路場景回答「哪個行程握著哪個埠／連線」。ss `-p` 做不到或要對檔案描述符時用它。

```bash
linux:~$ sudo lsof -iTCP:443 -sTCP:LISTEN
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nginx   1204 root    8u  IPv4  32100      0t0  TCP *:https (LISTEN)
```

```bash
linux:~$ sudo lsof -iTCP -sTCP:ESTABLISHED | head
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 4821 kam    5u  IPv4  88421      0t0  TCP linux:52310->10.0.0.20:5432 (ESTABLISHED)
```

- **-iTCP:埠**：
  - 只列該埠。`-sTCP:LISTEN` / `ESTABLISHED` 過濾狀態。
- **NAME**：
  - 本端與對端。`*:https` 表示聽所有位址的 443。
- **COMMAND / PID**：
  - 對到行程。磁碟那份用 `lsof +L1` 查已刪檔；這裡用 `-i` 查網路。

需要 root 才能看齊別人的 socket。只是數連線狀態時優先 `ss -s`，比較輕。

---

## ping

ping 用 ICMP echo 確認「到對端 IP 這一跳路徑上，能不能來回」。它不測 TCP 埠，也不直接等於 HTTP 成功。

```bash
linux:~$ ping -c 5 10.0.0.1
PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.
64 bytes from 10.0.0.1: icmp_seq=1 ttl=64 time=0.412 ms
64 bytes from 10.0.0.1: icmp_seq=2 ttl=64 time=0.388 ms
64 bytes from 10.0.0.1: icmp_seq=3 ttl=64 time=0.401 ms
64 bytes from 10.0.0.1: icmp_seq=4 ttl=64 time=0.395 ms
64 bytes from 10.0.0.1: icmp_seq=5 ttl=64 time=0.410 ms

--- 10.0.0.1 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4089ms
rtt min/avg/max/mdev = 0.388/0.401/0.412/0.009 ms
```

- **packet loss**：
  - 💡 丟包率。持續 > 0% 才代表路徑或對端不穩。
  - ⚠️ 有的網路會限速或丟棄 ICMP，**ping 100% loss 仍可能 TCP 正常**。反過來 ICMP 通也不保證 443 有開。
- **rtt min/avg/max/mdev**：
  - 來回延遲與抖動（mdev）。
  - ⚠️ **高 RTT ≠ 丟包**。RTT 高但 0% loss：路徑遠或壅塞造成延遲；loss 高才是「封包沒回來」。兩者都差才是嚴重品質問題。
- **icmp_seq**：
  - 序號不連續代表中間有遺失（在有回覆的前提下）。
- **-c**：
  - 送幾包就停。診斷用固定次數，避免背景一直 ping。

先 ping 閘道、再 ping 外網 IP、最後才 ping 域名（域名失敗要先分是 DNS 還是路徑）。

---

## nmap

nmap 做埠／主機探測，確認「對端有沒有在聽、過濾還是關閉」。只做連通性診斷，不展開掃描策略或攻擊流程。

```bash
linux:~$ nmap -Pn -p 22,80,443 10.0.0.20
Starting Nmap 7.94 ( https://nmap.org ) at 2026-09-22 01:40 CST
Nmap scan report for 10.0.0.20
Host is up.
PORT    STATE    SERVICE
22/tcp  open     ssh
80/tcp  closed   http
443/tcp filtered https
```

- **open**：
  - 有應用在聽且探測收到接受回應。
- **closed**：
  - 主機有回應「沒人聽這個埠」（常見 RST）。路徑大致通，服務沒開。
- **filtered**：
  - 💡 沒有明確開／關回應，多半被防火牆丟掉或禁 ICMP／探測。
  - 與本機 `ss -lnt` 對照：本機有 LISTEN、對端看 filtered → 查中間或主機防火牆（iptables / nft / ufw / firewalld）。
- **-Pn**：
  - 跳過主機 ping 發現。對端禁 ICMP 時不加可能被当成 down。

⚠️ 只對你有權管理或已獲授權的主機做探測。輸出用來判 open/closed/filtered，不當成效能儀表。

---

## traceroute

traceroute 逐跳看「封包走到哪、在哪變慢或消失」。預設常走 UDP 或 ICMP（實作依系統），用來劃路徑，不測應用層。

```bash
linux:~$ traceroute -n 1.1.1.1
traceroute to 1.1.1.1 (1.1.1.1), 30 hops max, 60 byte packets
 1  10.0.0.1  0.412 ms  0.388 ms  0.401 ms
 2  203.0.113.1  2.104 ms  2.088 ms  2.095 ms
 3  * * *
 4  1.1.1.1  12.401 ms  12.388 ms  12.395 ms
```

- **每一跳的 RTT**：
  - 該跳回應所花時間。某一跳突然變大、之後又恢復，不一定是那一跳壞了（路由器可能降優處理探測）。
- *** * ***：
  - 該跳沒回應。⚠️ 常見於路由器不回 TTL exceeded / 過濾探測，**不代表路徑中斷**——若後面跳仍有回應，路徑其實是通的。
- **-n**：
  - 不反查 DNS，避免把「慢」誤判成名稱解析慢。

路徑最後一跳通但應用失敗：改查埠與防火牆（nmap / ss / nft）。最後幾跳都 `*` 且 ping 也失敗：才比較像中途黑洞或對端擋。

---

## tracepath

tracepath 偏重路徑 MTU 發現（PMTUD），同時也能看到大致跳數。不需要 root 的 UDP 探測（視核心／權限而定）。

```bash
linux:~$ tracepath -n 1.1.1.1
 1?: [LOCALHOST]                      pmtu 1500
 1:  10.0.0.1                                         0.401ms
 2:  203.0.113.1                                      2.095ms
 3:  203.0.113.1                                     asymm  2  2.088ms pmtu 1472
 4:  1.1.1.1                                         12.395ms reached
     Resume: pmtu 1472 hops 4 back 4
```

- **pmtu**：
  - 💡 目前探測到的路徑 MTU。
  - 介面 MTU 1500，但 Resume 顯示 1472：路徑中間有較小 MTU（常見 VPN／隧道）。大封包若設 DF 又沒收到需要分片的訊號，會變成「小 ping 通、大傳輸卡住」。
- **asymm**：
  - 去程與回程跳數估計不對稱，僅供參考。
- **reached**：
  - 抵達目標。

⚠️ traceroute 看「路徑與延遲」；tracepath 額外強調 **路徑 MTU**。兩者都不取代 ping 的 loss／RTT 統計。

---

## nc

nc（netcat）對單一埠做「連不連得上」的快速探測，或聽一個測試埠。比 nmap 輕，一次一個目標。

```bash
linux:~$ nc -vz 10.0.0.20 443
Connection to 10.0.0.20 443 port [tcp/https] succeeded!
```

```bash
linux:~$ nc -vz 10.0.0.20 81
nc: connect to 10.0.0.20 port 81 (tcp) failed: Connection refused
```

- **-vz**：
  - 詳細＋只做掃描式連線（連上就關）。
- **succeeded**：
  - TCP 三次握手成功，對端有人聽（或中間有代理接受）。
- **Connection refused**：
  - 對端回 RST，路徑通但沒服務（或明確拒絕）。
- **timed out**：
  - 💡 多半被丟棄（防火牆 filtered），與 nmap 的 filtered 同一類現象。

UDP 模式（`-u`）沒有握手，成功／失敗語意較弱，解讀要保守。

---

## telnet

telnet 客戶端常被拿來手動試 TCP 埠（不是要你用明文遠端登入）。行為與 nc 類似，互動式較直覺。

```bash
linux:~$ telnet 10.0.0.20 443
Trying 10.0.0.20...
Connected to 10.0.0.20.
Escape character is '^]'.
```

```bash
linux:~$ telnet 10.0.0.20 81
Trying 10.0.0.20...
telnet: Unable to connect to remote host: Connection refused
```

- **Connected**：
  - TCP 已建立。對 TLS 埠會看到連上但後續是二進位亂碼——那只代表埠開著，不代表握手完成。
- **Connection refused / timed out**：
  - 意義同 nc。
- 許多發行版已不預裝；沒有就用 `nc -vz`。診斷埠用完即斷開（`Ctrl-]` 後 `quit`），不要拿 telnet 當正式管理通道。

---

## curl

curl 從應用層驗證 HTTP/HTTPS（或其它它支援的 URL 協定）：DNS、TCP、TLS、HTTP 狀態一次走完。

```bash
linux:~$ curl -sS -o /dev/null -w 'http=%{http_code} dns=%{time_namelookup}s connect=%{time_connect}s tls=%{time_appconnect}s ttfb=%{time_starttransfer}s total=%{time_total}s\n' https://example.com/
http=200 dns=0.012s connect=0.045s tls=0.120s ttfb=0.180s total=0.185s
```

- **http_code**：
  - HTTP 狀態。`200` 成功；`5xx` 是對端應用；連不上時這欄可能是 `000`。
- **time_namelookup**：
  - 💡 DNS 耗時。這裡偏高、connect 很短：問題在解析，改查 dig / resolvectl。
- **time_connect**：
  - TCP 連線完成時刻（相對開始）。減去 namelookup 可粗估 TCP 握手。
- **time_appconnect**：
  - TLS 握手完成（HTTPS）。偏高常見於 CPU／證書鏈／往返次數（對照 [processor.md](processor.md) 僅在本機 CPU 打滿時）。
- **time_starttransfer（TTFB）**：
  - 收到第一個位元組。TCP/TLS 都快、TTTFB 慢：多半是對端應用或後端慢，不是本機 NIC 錯誤。
- **-sS**：
  - 安靜但保留錯誤。`-o /dev/null` 丟掉內文，只量時間。

⚠️ curl 成功只代表這一條 URL 路徑通。介面 drops 仍可能在別的流量上發生。

---

## wget

wget 同樣拉 URL，偏下載／鏡像。診斷時用來對照 curl：同一個 URL 誰失敗、錯誤訊息是什麼。

```bash
linux:~$ wget -S -O /dev/null https://example.com/ 2>&1 | head
--2026-09-22 01:40:05--  https://example.com/
Resolving example.com (example.com)... 93.184.216.34
Connecting to example.com (example.com)|93.184.216.34|:443... connected.
HTTP request sent, awaiting response...
  HTTP/1.1 200 OK
...
```

- **Resolving …**：
  - DNS 步驟。卡在這裡 → dig / resolvectl。
- **Connecting … connected**：
  - TCP（與 TLS 客戶端）過了。
- **HTTP 狀態列**：
  - 與 curl 的 http_code 同類資訊。
- 預設會跟重新導向、寫檔；診斷加 `-O /dev/null` 或 `--spider` 減少副作用。

細分 DNS／TCP／TLS／TTFB 的毫秒值，curl `-w` 比較好讀；wget 適合「下載本身失敗」的訊息。

---

## tcpdump

tcpdump 在介面上做封包層級的**可讀診斷**：有沒有 SYN、有沒有回應、是否 RST／ICMP unreachable。只讀流量特徵，不記錄或還原帳密與憑證內容。

```bash
linux:~$ sudo tcpdump -ni enp0s3 host 10.0.0.20 and port 443 -c 20
01:40:05.001234 IP 10.0.0.15.52310 > 10.0.0.20.443: Flags [S], seq 101, win 64240, options [...], length 0
01:40:05.001456 IP 10.0.0.20.443 > 10.0.0.15.52310: Flags [S.], seq 202, ack 102, win 65535, options [...], length 0
01:40:05.001480 IP 10.0.0.15.52310 > 10.0.0.20.443: Flags [.], ack 203, win 502, length 0
```

- **-ni**：
  - 不反解域名、指定介面。避免 DNS 拖慢輸出。
- **-c**：
  - 抓滿幾包就停。診斷用短次數，避免整盤寫滿。
- **Flags [S] / [S.] / [.] / [R] / [F]**：
  - SYN、SYN-ACK、ACK、RST、FIN。
  - 💡 只有不斷 `[S]` 沒有 `[S.]`：對端沒回應或中間丟掉（與 nc timeout、nmap filtered 一致）。
  - 立刻 `[R]`：對端或中間明確拒絕。
- **ICMP unreachable / fragmentation needed**：
  - 路由或 MTU 線索，可與 tracepath 的 pmtu 對照。

需要 root 或 `CAP_NET_RAW`。⚠️ 本節只用於確認握手與控制訊息是否出現；不要在備忘流程裡做內容還原或憑證擷取。

---

## tshark

tshark 是 Wireshark 的 CLI。欄位過濾與協定樹比 tcpdump 細，用途同樣是診斷「哪一層失敗」，不是蒐集憑證。

```bash
linux:~$ sudo tshark -i enp0s3 -f 'host 10.0.0.20 and port 443' -c 20 -T fields -e frame.time_relative -e ip.src -e ip.dst -e tcp.flags.str
0.000000000	10.0.0.15	10.0.0.20	······S·
0.000222000	10.0.0.20	10.0.0.15	·A····S·
0.000246000	10.0.0.15	10.0.0.20	·A······
```

- **-f**：
  - capture filter（與 tcpdump 相同語法，在抓之前過濾）。
- **-T fields -e …**：
  - 只印選定欄位，方便貼進筆記。
- **tcp.flags.str**：
  - 旗標字串，讀法同 tcpdump 的 Flags。
- **http / tls 握手失敗時**：
  - 可再看 `tls.handshake` 是否出現、是否有 alert；仍只解讀狀態，不匯出金鑰或應用資料。

tcpdump 夠判 SYN／RST 時不必上 tshark。需要依協定欄位過濾再換它。

---

## iftop

iftop 即時顯示「哪個對端 IP 佔用頻寬」。看當下誰在灌流量；不看 errors，也不留歷史。

```bash
linux:~$ sudo iftop -i enp0s3 -t -s 5
interface: enp0s3
...
          10.0.0.15                  => 10.0.0.20                 2.15Mb  2.10Mb  2.08Mb
                                     <=                           480Kb   470Kb   465Kb
...
Cumulative (5s): TX 1.25MB  RX 280KB
```

- **=> / <=**：
  - 送出／收入方向的速率（顯示單位依版本為 b 或 B，看畫面標題）。
- **三欄速率**：
  - 通常是 2 秒、10 秒、40 秒平均（互動模式）；`-t -s` 文字模式欄位依版本略有差異。
- 💡 某個對端佔滿接近 ethtool 的 Speed：才是頻寬層飽和。流量不高但 ip 的 dropped／errors 在爬：不是 iftop 能解釋的，回 ip / ethtool。

需要 root。對照歷史吞吐用 `sar -n DEV`，對照連線數用 ss。

---

## dig

dig 查 DNS 答案與耗時，把「名字解不開」從「網路不通」裡拆出來。

```bash
linux:~$ dig +stats example.com A
...
;; ANSWER SECTION:
example.com.		86400	IN	A	93.184.216.34

;; Query time: 12 msec
;; SERVER: 10.0.0.1#53(10.0.0.1)
;; WHEN: Tue Sep 22 01:40:05 CST 2026
;; MSG SIZE  rcvd: 56
```

- **ANSWER SECTION**：
  - 實際回傳的紀錄。沒有 ANSWER、只有錯誤碼：解析失敗。
- **Query time**：
  - 💡 這次查詢耗時。偏高時，curl 的 `time_namelookup` 也會高。
- **SERVER**：
  - 實際問了哪台解析器。與 resolvectl / `/etc/resolv.conf` 對照。
- **+trace**：
  - 從根往下追（輸出長）。只有懷疑委派問題時再用。

`dig @8.8.8.8 example.com` 可區分「系統指定的 DNS 壞了」還是「這台主機對外 53 都不通」。

---

## nslookup

nslookup 同樣做 DNS 查詢，互動或單次模式都有。欄位比 dig 少，許多環境預設仍在。

```bash
linux:~$ nslookup example.com 10.0.0.1
Server:		10.0.0.1
Address:	10.0.0.1#53

Non-authoritative answer:
Name:	example.com
Address: 93.184.216.34
```

- **Server / Address**：
  - 問的那台 DNS。
- **Name / Address**：
  - 答案。失敗時看 `NXDOMAIN`、`SERVFAIL`、timeout。
- 細部統計與追蹤優先 dig；nslookup 適合快速確認「有沒有 A 紀錄」。

---

## host

host 是最短的 DNS 查詢指令，適合腳本與一眼看答案。

```bash
linux:~$ host example.com
example.com has address 93.184.216.34
example.com has IPv6 address 2606:2800:220:1:248:1893:25c8:1946
example.com mail is handled by 0 .
```

- **has address**：
  - A 紀錄。
- **has IPv6 address**：
  - AAAA。雙棧環境下 curl 可能走 v6；v6 不通時會表現成「偶發很慢或失敗」。
- 沒有 Query time；要耗時用 dig。

---

## resolvectl

resolvectl（systemd-resolved）看本機「誰在解析、目前 DNS 伺服器、每條連線的 DNS」。NetworkManager / networkd 環境下比直接看 `resolv.conf` 準。

```bash
linux:~$ resolvectl status
Global
       Protocols: ...
Current DNS Server: 10.0.0.1
       DNS Servers: 10.0.0.1

Link 2 (enp0s3)
    Current Scopes: DNS
         Protocols: ...
Current DNS Server: 10.0.0.1
       DNS Servers: 10.0.0.1
```

```bash
linux:~$ resolvectl query example.com
example.com: 93.184.216.34
-- Information acquired via protocol DNS in 11.2ms.
```

- **Current DNS Server**：
  - 💡 此刻真正在用的伺服器。
- **Link … (enp0s3)**：
  - 每條介面自己的 DNS（VPN 常在這裡插入）。查錯介面的 DNS 會解到內網才能用的名字。
- **query … in Xms**：
  - 與 dig Query time 同類。
- `/etc/resolv.conf` 若指向 `127.0.0.53`，實際上游在 resolvectl，不要以為「只有本機 DNS」。

沒有 systemd-resolved 時指令不存在，改 dig / nslookup。

---

## iptables

iptables 讀傳統 filter／nat 表規則，確認封包有沒有被 **DROP/REJECT**。nft 後端系統上，iptables 可能是相容層，改規則前先搞清真正後端。

```bash
linux:~$ sudo iptables -L -n -v
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
 1200 72000 ACCEPT     all  --  lo     *       0.0.0.0/0            0.0.0.0/0
  800 48000 ACCEPT     all  --  *      *       0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
    0     0 DROP       tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:81
```

- **-L -n -v**：
  - 列出規則、不反解域名、顯示套用次數（pkts/bytes）。
- **policy**：
  - 鏈的預設策略。INPUT 預設 DROP 且沒有對應 ACCEPT 時，新連線會進不來。
- **pkts**：
  - 💡 這條規則命中次數。診斷「有沒有打到 DROP」看誰的 pkts 在增加。
- **DROP vs REJECT**：
  - DROP → 對端常是 timeout / filtered；REJECT → 常是 refused。可與 nc / nmap 狀態對照。

只讀診斷用 `-L`；改規則屬變更，不在本備忘展開。IPv6 看 `ip6tables`。

---

## nftables

nftables 是較新的核心封包過濾架構。`nft list ruleset` 看目前生效的整份規則。

```bash
linux:~$ sudo nft list ruleset
table inet filter {
	chain input {
		type filter hook input priority filter; policy accept;
		ct state established,related accept
		iif "lo" accept
		tcp dport 81 drop
	}
}
```

- **table / chain / hook**：
  - 表與掛在 input/output/forward 的鏈。policy 同樣是最後底線。
- **drop / reject / accept**：
  - 意義同 iptables。`counter` 若有寫在規則上，可看命中量。
- 💡 同一台機器請統一：要麼以 nft 為準，要麼搞清 iptables-nft 只是前端。兩邊各改一輪會無法解釋「規則明明開了卻不通」。

ufw / firewalld 往往在更高層產生這些規則；查應用意圖用 ufw/firewalld，查核心真正生效用 nft/iptables。

---

## ufw

ufw（Uncomplicated Firewall）是 Ubuntu 等常見的 iptables/nft 前端。看「對外政策與允許埠」最快。

```bash
linux:~$ sudo ufw status verbose
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
443/tcp                    ALLOW IN    Anywhere
```

- **Status: active / inactive**：
  - 沒啟用時，不通的原因不在 ufw。
- **Default: deny (incoming)**：
  - 💡 未明示允許的入站會被拒。nmap 顯示 filtered、本機 ss 有 LISTEN：先對這張表有沒有該埠。
- **ALLOW IN**：
  - 允許入站的埠／來源。
- `ufw status numbered` 方便對編號；本備忘只讀 status，不寫改規則步驟。

---

## firewalld

firewalld 以 zone 管理規則，常見於 RHEL／Fedora。看目前 zone 與開放的 service／port。

```bash
linux:~$ firewall-cmd --state
running

linux:~$ firewall-cmd --get-active-zones
public
  interfaces: enp0s3

linux:~$ firewall-cmd --list-all
public (active)
  target: default
  interfaces: enp0s3
  services: ssh https
  ports:
  forward-ports:
  ...
```

- **--state**：
  - running 才有在攔。
- **active zones / interfaces**：
  - 💡 介面落在哪個 zone。enp0s3 在 public、規則卻加在 home：等於沒放行。
- **services / ports**：
  - 目前允許的服務名與埠。對照 ss 的 LISTEN 與對端 nmap 結果。

改動屬營運變更；診斷先 `--list-all` 與 `--get-active-zones`。

---

## sar

sar `-n DEV` 留下每塊網卡的吞吐與利用率歷史，對應 memory 的 `sar -r`、disk 的 `sar -d`。即時錯誤計數仍以 `ip -s link` / ethtool 為準；sar 回答「當時流量有多高」。

```bash
linux:~$ sar -n DEV
Linux 7.0.0-14-generic (linux)      09/22/2026      _x86_64_        (4 CPU)

01:00:05 AM     IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s   %ifutil
01:10:05 AM    enp0s3     120.40     98.20     84.50     62.30      0.00      0.00      2.10      0.07
01:20:05 AM    enp0s3     118.00     95.10     80.20     58.40      0.00      0.00      1.80      0.06
01:30:05 AM    enp0s3   85200.00  41000.00  112400.00  52000.00      0.00      0.00     40.00     89.92
01:40:05 AM    enp0s3     130.20    101.50     90.10     66.80      0.00      0.00      2.00      0.07
Average:       enp0s3   21392.15  10323.70  28163.70  13046.88      0.00      0.00     11.48     22.53
```

- **IFACE**：
  - 介面名。略過 `lo` 除非在查本機回環異常。
- **rxpck/s、txpck/s**：
  - 每秒收／送封包數。小包極多時 pps 很高但 kB/s 未必高，CPU softirq 卻可能先爆（[processor.md](processor.md)）。
- **rxkB/s、txkB/s**：
  - 💡 每秒收／送 KB。估頻寬占用看這兩欄（再乘 8 與 ethtool Speed 比）。
- **%ifutil**：
  - 介面利用率估算：相對該介面速度的占用比例。
  - ⚠️ 速度來源若不對（協商錯、虛擬網卡報不實），`%ifutil` 會失真。先確認 ethtool 的 Speed。
  - 01:30 的 rxkB/s 與 `%ifutil` 同時衝高：那是頻寬層尖峰。若 `%ifutil` 很低但應用喊慢：去看 RTT、retransmit、drops、DNS，而不是「網卡打滿」。
- **Average**：
  - ⚠️ 會把尖峰稀釋。01:30 接近 90%、Average 只有 22%：不能拿 Average 說「當天都不忙」。
- 帶間隔的即時 `sar -n DEV 1 3`：與其它 sar 相同，**第一筆常是開機至今平均**，看當下從第二筆起。

相關：`sar -n EDEV` 看錯誤／丟包速率歷史；`sar -n TCP,ETCP` 看 TCP 區段與重傳速率（對應下方 snmp 計數的趨勢）。需要 sysstat 事先在蒐集。

原始累計也可對 `/proc/net/dev`（每介面 bytes/packets/errs/drop）與 `/proc/net/snmp`（如 **TcpRetransSegs**：開機以來 TCP 重傳段數）。

```bash
linux:~$ grep Tcp /proc/net/snmp
Tcp: RtoAlgorithm RtoMin RtoMax MaxConn ActiveOpens PassiveOpens AttemptFails EstabResets CurrEstab InSegs OutSegs RetransSegs InErrs OutRsts InCsumErrors
Tcp: 1 200 120000 -1 480012 120044 220 810 24 88001200 86400300 15200 12 6400 0
```

- **CurrEstab**：
  - 目前 ESTABLISHED 數，可與 `ss -s` 的 estab 對。
- **RetransSegs（TcpRetransSegs）**：
  - 💡 累計重傳段數。隔幾秒相減才有速率。
  - ⚠️ **重傳升高 ≠ 頻寬已飽和**。可能是丟包、延遲變大、對端窗小、無線品質差。先看 `%ifutil`／rxkB/s 是否同時貼近 Speed；若利用率很低卻一直重傳，優先查路徑品質與 loss，不是先加購頻寬。

---

## 🔍 判斷是連不通、丟包，還是頻寬打滿

**連線與設定（ip / nmcli / networkctl）**

1. 介面要有 LOWER_UP、有位址、有 default route。缺任一項，先別查應用。
2. nmcli / networkctl 顯示未 connected / 非 routable：先修連線管理器與設定檔。
3. `ip -s link` 的 errors、dropped 要看「是否持續增加」，不是看歷史絕對值。

**實體與驅動（ethtool）**

1. Speed／Duplex 是否符合預期；Link detected 是否為 yes。
2. `ethtool -S` 的 crc／fifo／missed 在短時間內爬升：連結品質或本機收包來不及，不是單純「網站慢」。

**socket 與行程（ss / lsof）**

1. 服務有沒有 LISTEN：`ss -lntup`。
2. TIME-WAIT 多、estab 穩定：通常正常。estab 或 CLOSE-WAIT 單調暴漲才像洩漏／應用沒關 fd。
3. Recv-Q／Send-Q 堆在已建立連線上：應用或對端慢，不是 NIC 名稱寫錯。

**路徑與埠（ping / traceroute / tracepath / nc / telnet / nmap）**

1. ping：先分 **loss** 與 **高 RTT**。只高 RTT 是慢，不是斷。
2. traceroute：中間 `*` 而後面仍通 → 常是路由器不回探測。tracepath 看 **pmtu** 是否小於介面 MTU。
3. nc／telnet／nmap：open／refused／timeout(filtered) 決定下一步是起服務還是查防火牆。

**應用與 DNS（curl / wget / dig / host / nslookup / resolvectl）**

1. curl 的 namelookup 大 → DNS；connect 大 → 路徑／防火牆；TTFB 大 → 對端應用。
2. resolvectl 確認真正上游 DNS；host／dig 確認有沒有答案。

**防火牆（iptables / nftables / ufw / firewalld）**

1. 本機有 LISTEN、外部 filtered／timeout：對 ufw status、firewalld zone、或 nft/iptables 的 DROP 計數。
2. REJECT 對 refused；DROP 對 timeout。

**流量與歷史（iftop / sar -n DEV / snmp）**

1. iftop：當下誰佔頻寬。
2. sar：`rxkB/s` `txkB/s` `%ifutil` 是否貼近 ethtool Speed。Average 會稀釋尖峰。
3. TcpRetransSegs 速率升、但 `%ifutil` 很低：品質／丟包問題，不是已經打滿線路。
4. drops／overrun 升、利用率低：本機收送路徑或 CPU softirq，可對 [processor.md](processor.md)。

💡 一分鐘快速診斷

1. `ip -br addr`、`ip route`：有位址、有預設路由、介面 UP。
2. `ip -s link` / `ethtool`：Link、Speed，以及 errors／dropped 是否在漲。
3. 不通：`ping` 閘道→對端 IP；再 `nc -vz` 或 nmap 看埠；filtered 就查 ufw／firewalld／nft。
4. 慢：`ping` 分清 loss 與 RTT；`tracepath` 看 pmtu；`curl -w` 分 DNS／TCP／TLS／TTFB。
5. 是否打滿：`sar -n DEV` 的 `%ifutil`／kB/s，對 ethtool Speed；IFTOP 看是誰。重傳高但利用率低 → 查品質，不是先加頻寬。
6. 連線數：`ss -s`；不要把 TIME-WAIT 單獨當成洩漏。

---

## 🛠 設計目的、資料來源和適用場景

- **ip**
  - 定位: 位址、路由、介面累計計數
  - 時間軸: 當下；`-s` 為開機以來累計
  - 資料來源: 核心網路堆疊、`/proc/net/dev`
  - 優點: 一條指令看到 UP、IP、路由與 RX/TX errors／drops。
  - 缺點: 無歷史速率；細項錯誤名不如 ethtool -S。

- **ethtool**
  - 定位: 連線模式與驅動統計
  - 時間軸: 當下；-S 為累計
  - 優點: Speed／Duplex／Link 與 crc、fifo、missed 細項。
  - 缺點: 要權限；欄位名因驅動而異；虛擬網卡常不全。

- **nmcli**
  - 定位: NetworkManager 連線狀態
  - 時間軸: 當下
  - 優點: 一眼看 connected 與 DNS／IP。
  - 缺點: 非 NM 環境無用。

- **networkctl**
  - 定位: systemd-networkd 狀態
  - 時間軸: 當下
  - 優點: routable／configured 與套用的 .network 檔。
  - 缺點: 未跑 networkd 時資訊有限。

- **ss**
  - 定位: socket 狀態與計數
  - 時間軸: 當下快照
  - 資料來源: 核心 sock_diag
  - 優點: estab／timewait、Recv-Q／Send-Q、LISTEN 與行程。
  - 缺點: 不看介面錯誤與頻寬；TIME-WAIT 易被誤讀。

- **lsof**
  - 定位: 哪個行程佔埠／連線
  - 時間軸: 當下
  - 優點: `-i` 對 PID 很直覺。
  - 缺點: 重；要 root 才看齊全；日常數狀態優先 ss。

- **ping**
  - 定位: ICMP 可達與 RTT／loss
  - 時間軸: 探測期間
  - 優點: 最快分清丟包與延遲。
  - 缺點: 不測 TCP 埠；ICMP 可能被擋。

- **nmap**
  - 定位: 埠狀態（open／closed／filtered）
  - 時間軸: 單次探測
  - 優點: 與防火牆現象對得起來。
  - 缺點: 非效能工具；僅能對授權目標使用。

- **traceroute**
  - 定位: 路徑跳點與大致延遲
  - 時間軸: 單次
  - 優點: 劃出走到哪。
  - 缺點: 中間 `*` 常被過度解讀。

- **tracepath**
  - 定位: 路徑 MTU
  - 時間軸: 單次
  - 優點: pmtu 對「小 ping 通、大傳輸死」。
  - 缺點: 不是 loss 統計工具。

- **nc** / **telnet**
  - 定位: 單埠 TCP 連通
  - 時間軸: 單次
  - 優點: 輕；refused／timeout 語意清楚。
  - 缺點: 一次一埠；UDP 語意弱。

- **curl** / **wget**
  - 定位: URL／HTTP(S) 應用層
  - 時間軸: 單次請求
  - 優點: curl `-w` 能拆 DNS／連線／TLS／TTFB。
  - 缺點: 不代表整機 NIC 健康。

- **tcpdump** / **tshark**
  - 定位: 封包層握手與控制訊息
  - 時間軸: 短時間擷取
  - 優點: 證實 SYN 有無回應、RST／ICMP。
  - 缺點: 要權限；本備忘不做內容／憑證還原。

- **iftop**
  - 定位: 即時誰佔頻寬
  - 時間軸: 即時
  - 優點: 對到對端 IP。
  - 缺點: 無歷史；不算 errors。

- **dig** / **nslookup** / **host** / **resolvectl**
  - 定位: DNS 答案與本機解析器
  - 時間軸: 當下查詢
  - 優點: 把「名字」從「網路」拆開；resolvectl 看真正上游。
  - 缺點: 不解 TCP 應用是否健康。

- **iptables** / **nftables** / **ufw** / **firewalld**
  - 定位: 過濾政策是否擋連線
  - 時間軸: 當下規則（計數為累計）
  - 優點: 對 filtered／timeout／refused。
  - 缺點: 多層前端並存時要先搞清誰生效。

- **sar -n DEV**（兼 `/proc/net/dev`、`/proc/net/snmp`）
  - 定位: 網卡吞吐與利用率歷史；snmp 提供 TCP 重傳等累計
  - 時間軸: 當天或指定日期（通常 10 分鐘一筆）；proc 為累計
  - 資料來源: sadc ← `/proc/net/dev` 等
  - 優點: 事後對 `%ifutil`、rxkB/s、txkB/s；可與 retransmit 分開談。
  - 缺點: 要啟用 sysstat；Average 與第一筆平均易誤導；`%ifutil` 依賴正確連線速度。

- 怎麼讀才不會誤判
  - 錯誤／丟包：ip `-s`、ethtool `-S`、`sar -n EDEV`。這是品質與本機佇列。
  - 頻寬飽和：rxkB/s、txkB/s、`%ifutil`、iftop，並對 ethtool Speed。
  - 重傳：TcpRetransSegs／`sar -n ETCP`——利用率低仍可能很高。
  - TIME-WAIT：ss 計數——短連線常態，不是洩漏的充分條件。
  - ping loss 對「丟」；高 RTT 對「慢」；traceroute 對「路徑」；tracepath 對「MTU」。
