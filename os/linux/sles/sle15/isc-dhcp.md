# isc-dhcp

## history

DHCP 的誕生並非憑空而來，它是從更早期的協議演進而來的，主要是為了解決手動配置 IP 地址帶來的管理噩夢。

1. 早期：手動與 BOOTP 協議

   - 手動配置 (Manual Configuration)：在網際網路的早期，網路規模很小，IP 地址都是由網管員手動分配和配置的。這種方式效率低下，容易出錯，且當設備數量增加時，管理難度呈指數級增長。
   - RARP (Reverse Address Resolution Protocol)：1984 年，RARP 協議被提出，允許設備透過 MAC 地址向伺服器查詢 IP 地址，但其主要限制是必須在同一個網路區段內，且功能非常有限。
   - BOOTP (Bootstrap Protocol)：1985 年，BOOTP 協議出現，它改進了 RARP 的不足，可以跨越子網路提供 IP 地址和開機資訊給無硬碟的工作站，但它仍然是基於靜態配置的，無法動態分配 IP。

2. DHCPv4：動態配置的標準

   - DHCP 的誕生 (1993)：為了解決 BOOTP 的靜態分配問題，DHCP 協議在 1993 年正式被 RFC 1531 標準化。DHCP 是 BOOTP 的擴展，其最大革命在於引入了「IP 租約 (IP Lease)」的概念。
   - 動態 IP 租約：DHCP 伺服器可以從一個 IP 地址池中動態地分配地址給客戶端，並設定一個租約時間。租約到期後，IP 地址會被回收並重新分配給其他設備。這極大地優化了 IP 地址的使用效率。
   - DHCP 的完善：1997 年，RFC 2131 進一步完善了 DHCPv4 協議，使其成為現今 IPv4 網路的標準。

3. DHCPv6：為 IPv6 時代而生

   - DHCPv6 的誕生：隨著 IPv4 地址的耗盡，IPv6 協議被設計出來。DHCPv6（RFC 8415）不僅僅是 DHCPv4 的 IPv6 版本，它是一個完全不同的協議。
   - 與 SLAAC 的共存：IPv6 引入了 SLAAC (Stateless Address Autoconfiguration) 功能，允許設備自動配置 IP 地址而無需伺服器。DHCPv6 則用於提供更多配置資訊，例如 DNS 伺服器地址，並在需要狀態管理時提供服務。

DHCP 的演進，是從一個簡單的 IP 獲取工具，發展為一個能夠自動化管理 IP 地址、提供多樣化網路配置資訊的完整框架，成為現代網路不可或缺的一部分。

---

## software

DHCP 伺服器軟體

市面上有很多 DHCP 伺服器軟體，以下是幾種常見的開源和商業方案：

- ISC DHCP：這是最早、最廣泛使用的 DHCP 伺服器之一。它由網際網路系統協會 (ISC) 開發，是許多 Linux 發行版和網路設備的參考實作。它的功能非常完整且強大，但配置相對複雜。
- Kea DHCP：由 ISC 開發，旨在取代 ISC DHCP。Kea 是一個更現代、效能更高、配置更簡單的 DHCP 伺服器，它支援 JSON 格式的設定檔，更適合大型和雲端環境。
- Dnsmasq：這是一個輕量級的 DNS 轉發器和 DHCP 伺服器。它的設計初衷是為了家庭網路和小型企業，因此設定非常簡單，資源消耗低，非常適合嵌入式系統和路由器。
- Windows Server DHCP：微軟在 Windows Server 中提供了內建的 DHCP 服務，它與 Active Directory 緊密整合，提供圖形化介面，適合在 Windows 生態系中使用。
- DHCPd (Linux)：在大多數 Linux 系統中，DHCPd 是用於啟動和管理 DHCP 服務的標準 daemon。它通常與 ISC DHCP 軟體一起打包。

---

## port

- dhcp: 67/udp

---

## server

### server - package

```bash
dhcp:~ # zypper in dhcp-server
dhcp:~ # zypper in yast2-dhcp-server
```

### server - config

- method 1 - by yast

```bash
dhcp:~ # yast dhcp-server
```

- method 2 - by manual

```bash
# config
dhcp:~ # vi /etc/dhcpd.conf
```

```conf
# /etc/dhcpd.conf
option domain-name "domain";
option domain-name-servers 8.8.8.8;
option routers 192.168.0.1;
default-lease-time 14400;
ddns-update-style none;
subnet 192.168.0.0 netmask 255.255.255.0 {
  range dynamic-bootp 192.168.0.101 192.168.0.150;
  default-lease-time 14400;
  max-lease-time 172800;
  host hpc1 {
    fixed-address 192.168.0.11;
    hardware ethernet 52:54:00:93:fb:f4;
  }
}

dhcp:~ # dhcpd -t -cf /etc/dhcpd.conf
```

### server - daemon

```bash
dhcp:~ # systemctl start dhcp-server
dhcp:~ # systemctl enable dhcp-server
```

### server - firewall

```bash
dhcp:~ # firewall-cmd --permanent --add-service=dhcp
dhcp:~ # firewall-cmd --permanent --add-service=dhcpv6-client
dhcp:~ # firewall-cmd --reload
```

---

## client

### client - package

```bash
sle:~ # zypper in dhcp-client
```

### client - config

- method 1 - by yast

```bash
sle:~ # yast lan
```

- method 2 - by manual

```bash
# config
sle:~ # vi /etc/sysconfig/network/ifcfg-eth0
BOOTPROTO='dhcp'
STARTMODE='auto'
ZONE=public

sle:~ # wicked ifup eth0
sle:~ # wicked show eth0
sle:~ # dhclient -v -r eth0
```
