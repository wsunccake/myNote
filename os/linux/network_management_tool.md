# network management tool / 網路管理工具

## Distro

### Red Hat (RHEL / CentOS / Fedora / Rocky / Alma)

Red Hat 家族在 8.0 是一個重大分水嶺，正式全面摒棄了使用數十年的 Shell 腳本，改由事件驅動的 NetworkManager 獨佔。

1. Network Scripts 時代 (/etc/sysconfig/network-scripts/)
   1990s - RHEL 6
   純粹由 Init 開機腳本呼叫 ifconfig / route / ip 指令。設定檔為經典的 ifcfg-eth0 格式，開機透過 service network restart 載入，不支援動態熱插拔。

2. 過渡期 (NetworkManager + Network Scripts 並存)
   RHEL 7 / CentOS 7
   導入 NetworkManager (nmcli) 作為預設服務，但同時保留傳統 network.service 與 ifcfg-\* 腳本相容層，使用者可擇一或混合使用。

3. NetworkManager 獨佔時代
   RHEL 8 / 9 / 10+
   完全廢棄 network.service 與 initscripts 套件。

### Debian

Debian 堅持極簡與高穩定度，開創了經典的 ifupdown 架構，現代則針對伺服器與桌面進行了路線分流。

1. ifupdown 時代 (/etc/network/interfaces)
   1999 - Debian 10
   由 Debian 自行開發的 ifupdown 套件統一管理網路，搭配 ifup eth0 / ifdown eth0 指令控制，是 Linux 歷史上最為廣泛採用的設定檔架構之一。

2. 路線分流 (ifupdown2 / systemd-networkd / NetworkManager)
   Debian 11 (Bullseye) / 12 (Bookworm)+
   因應現代複雜網路架構，Debian 預設走向多元化

### Canonical Ubuntu

Ubuntu 經歷了從繼承 Debian 架構，到自行開發抽象層（Netplan）的重大演進。

1. 繼承 Debian interfaces 時代
   Ubuntu 4.10 - 17.04
   伺服器版完全沿用 Debian 的 /etc/network/interfaces；桌面版則從 6.06 起導入 NetworkManager 處理 Wi-Fi 與熱插拔需求。

2. Netplan YAML 統一抽象層
   Ubuntu 17.10 - 至今 (18.04 LTS ~ 26.04 LTS+)
   Canonical 推出自研的 Netplan，不再直接讀取舊版設定檔。

### SUSE (SLES / openSUSE)

SUSE 在企業級市場獨樹一格，早期使用類似 Red Hat 的語法，後期則自行開發了高穩定度的 Wicked 框架。

1. sysconfig ifcfg 腳本時代
   SLES 11 以前
   使用由 SUSE 維護的 /etc/sysconfig/network/ifcfg-\* 純文字設定檔，透過 rcnetwork 腳本控制。

2. Wicked 企業級框架
   SLES 12 / 15 / openSUSE Leap
   推出 Wicked 架構，取代傳統腳本。

3. NetworkManager 為主
   openSUSE Tumbleweed / 現代桌面
   在滾動更新版與桌面環境中，預設改用 NetworkManager；SLES 伺服器版則繼續以 Wicked 為主力。

### Alpine Linux (嵌入式與微型容器)

Alpine 完全不採用 systemd，而是基於 BusyBox 與 OpenRC 建構出極小化網路架構。

1. BusyBox ifupdown + OpenRC 時代
   創立至今 (Alpine 1.x ~ 3.x+)
   語法採用類似 Debian 的 /etc/network/interfaces，但底層由 BusyBox 的極輕量 ifup/ifdown 與 udhcpc 解析。開機由 OpenRC 的 networking 服務管理。

2. Daemonless 與 setup-interfaces
   Docker / Cloud 時代

---

## Tool

### SysVinit / Network Scripts

早期 Linux 最基礎的網路控制方式，完全仰賴 Shell 腳本在開機時呼叫 ifconfig、route 或 ip 指令。

- 運作機制：開機時由 Init 執行 /etc/init.d/network restart 等腳本，依序讀取設定檔並綁定網卡。
- 主要設定檔路徑：
  - RHEL / CentOS / Fedora：/etc/sysconfig/network-scripts/ifcfg-eth0
  - Debian / Early Ubuntu：/etc/network/interfaces
- 主要 Linux 發行版：Red Hat Enterprise Linux (RHEL 6/7 以前)、CentOS 6、Debian 8 以前、Early Ubuntu (17.10 以前)、Slackware。
- 優缺點與淘汰原因：
  - 優點：直覺、設定檔即腳本，對固定 IP 的伺服器非常穩定。
  - 缺點：無法處理「網路熱插拔」（例如插拔網線、切換 Wi-Fi）、不支援現代複雜事件驅動機制，且各發行版腳本語法不統一。

### NetworkManager

因應筆記型電腦與無線網路興起，由 Red Hat 於 2004 年發起，旨在提供動態、事件驅動（Event-driven）的網路管理。

- 運作機制：後台執行 NetworkManager Daemon，透過 D-Bus 管理網路。使用者可透過桌面 GUI、TUI（nmtui）或 CLI（nmcli）進行控制。
- 主要設定檔路徑：
    - 早期：/etc/sysconfig/network-scripts/ (RHEL)
    - 現代：/etc/NetworkManager/system-connections/ (Keyfile 格式 .nmconnection)
- 主要 Linux 發行版：RHEL (8/9/10 預設)、CentOS Stream、Rocky Linux、AlmaLinux、Fedora、Ubuntu Desktop、Debian Desktop、Arch Linux (桌面首選)。
- 優缺點：
    - 優點：支援度最廣，熱插拔、Wi-Fi、VPN、Bonding/Teaming、Bridge 支援極佳，API 豐富。
    - 缺點：記憶體佔用較高，在極簡容器或輕量化伺服器中顯得過於龐大。

### Netplan

Canonical 開發的網路配置抽象層（Abstraction Layer），它本身「不是」網路 Daemon，不直接控制網卡。

- 運作機制：使用者撰寫統一格式的 YAML 設定檔，Netplan 在套用時，會將 YAML 自動編譯並轉換成目標「後端（Renderer）」的設定檔。
    - NetworkManager（常用於 Desktop）
    - systemd-networkd（常用於 Server）
- 主要設定檔路徑：/etc/netplan/*.yaml（套用指令：sudo netplan apply）
- 主要 Linux 發行版：Ubuntu (18.04 LTS 起預設為伺服器與桌面標準)、Canonical 微型雲端環境。
- 優缺點：
    - 優點：語法統一且簡潔（使用 YAML），消除了 Ubuntu 在 Server (systemd-networkd) 與 Desktop (NetworkManager) 設定格式不一致的問題。
    - 缺點：YAML 對縮排極度敏感，若底層轉換出錯時除錯較為曲折。

### systemd-networkd

作為 systemd 專案的一部分，提供輕量化、原生的系統級網路管理服務。

- 運作機制：由 systemd-networkd.service 管理，搭配 systemd-resolved 處理 DNS，使用 networkctl 指令進行檢視與管理。
- 主要設定檔路徑：/etc/systemd/network/*.network
- 主要 Linux 發行版：Debian (Server 常用)、Arch Linux (極簡設定)、CoreOS / Flatcar (雲端原生 OS)、Ubuntu Server (底層預設，透過 Netplan 操控)。
- 優缺點：
    - 優點：極度輕量、啟動極快、無須額外安裝套件，非常適合雲端 VM、Docker 宿主機與無頭伺服器。
    - 缺點：缺乏對複雜無線網路（Wi-Fi GUI 切換）的良好支援，主要鎖定有線網路與伺服器環境。

### Wicked

SUSE 團隊為了取代傳統 Network Scripts 所專門開發的企業級 DBus 網路管理架構。

- 運作機制：採用 Client/Server 架構（wickedd），透過 XML 或簡化的 Schema 描述網路狀態，使用 wicked 指令進行控制。
- 主要設定檔路徑：
    - /etc/wicked/
    - /etc/sysconfig/network/ifcfg-*（相容舊式 SUSE 語法）
- 主要 Linux 發行版：SUSE Linux Enterprise Server (SLES 12/15)、openSUSE Leap。
- 優缺點：
    - 優點：針對企業級大規模伺服器設計，對 VLAN、InfiniBand、Complex Bridging、Bonding 的動態配置與狀態檢查非常精準。
    - 缺點：生態系僅限於 SUSE 家族，學習曲線較高，其他發行版幾乎不使用。

---

## command


### static ip

- ip

`iproute2` 工具包，為目前所有 Linux 的標準。

```bash
ip addr add 192.168.1.100/24 dev eth0       # 設定 IP 與子網遮罩
ip link set dev eth0 up                     # 啟用網卡
ip route add default via 192.168.1.1        # 設定預設閘道
```

- ifconfig

`net-tools` 工具包，已漸被淘汰。在 Embedded Linux（嵌入式系統） 的領域裡，是主流與絕對的主力。

```bash
ifconfig eth0 192.168.1.100 netmask 255.255.255.0 up    # 設定 IP 與子網遮罩
route add default gw 192.168.1.1 eth0                   # 設定預設閘道
```

### dynamic ip / dhcp

- dhclient

```bash
dhclient eth0    # 向 DHCP 伺服器請求 IP
dhclient -r eth0 # 釋放目前的 IP
```

- dhcpcd

```bash
sudo dhcpcd eth0
```

- nmcli

```bash
nmcli device connect eth0
```

- udhcpc

```bash
udhcpc -i eth0
```

| 設定類別   | 主要指令          | 適用 Linux 發行版與情境                |
| ---------- | ----------------- | -------------------------------------- |
| Static IP  | ip addr, ip route | 所有 Linux 發行版（通用標準）          |
| Static IP  | ifconfig, route   | 舊版 Linux 或已安裝 net-tools 的系統   |
| Dynamic IP | dhclient          | Ubuntu, Debian, RHEL, Rocky Linux      |
| Dynamic IP | dhcpcd            | Arch Linux, Raspberry Pi OS            |
| Dynamic IP | nmcli             | 具備 NetworkManager 的桌面與伺服器系統 |
| Dynamic IP | udhcpc            | Alpine Linux, BusyBox 嵌入式環"        |
