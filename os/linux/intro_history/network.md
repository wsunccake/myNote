# network

## history

Linux Network Management Services (網路管理服務) 發展，是從最原始的腳本驅動方式，逐步演變到現代自動化、彈性更高且與系統整合更緊密的服務。

1. 創始階段：靜態腳本與低階工具 (早期 Linux ~ 2000 年代初)

在這個階段，網路配置是`完全靜態`和`非自動化`的，主要依賴低階的指令和發行版特定的腳本。

| command / file                        | explain                                                                                                                                                          |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ifconfig, route, netstat (Net-tools)  | 核心指令工具。網路管理員直接使用它們來設定 IP 位址、路由等。                                                                                                     |
| networking / ifupdown (Debian/Ubuntu) | /etc/network/interfaces 配置檔案。ifup/ifdown 腳本根據此檔案來執行底層的 ifconfig/route。                                                                        |
| ifcfg / network (Red Hat/CentOS)      | /etc/sysconfig/network-scripts/ifcfg-ethX 獨立配置檔案。系統啟動時透過服務腳本讀取這些檔案並啟動網路。                                                           |
| iproute2 (ip, ss)                     | iproute2 套件在 90 年代中後期就出現，但全面取代 net-tools 成為主流則發生在 2000 年代中後期。為複雜的網路功能（如策略路由、流量控制）提供了現代化、更強大的介面。 |

2. 轉折點：自動化與桌面需求 (約 2004 年開始)

隨著筆記型電腦和無線網路的普及，手動編輯配置檔來切換網路變得不切實際。市場迫切需要一個可以`自動偵測`、`管理連線`、`處理 Wi-Fi` 和`漫遊`的網路服務。

`NetworkManager` (約 2004 年發布)

- 定位： 專為解決桌面環境的痛點而生。
- 特性： 提供連線檔 (Connection Profile) 概念，具備自動連線、故障排除、Wi-Fi 漫遊、VPN 支援等功能，並透過 GUI (GNOME/KDE)、TUI (`nmtui`) 和 CLI (`nmcli`) 介面進行管理。
- 影響： 迅速成為桌面 Linux 發行版（如 Fedora、Ubuntu）的標準。

3. 伺服器與發行版的分流 (約 2012 年開始)

隨著 `systemd` 成為主流初始化系統，新的網路管理解決方案開始出現，專注於高效能、輕量化或單一發行版的整合。

`systemd-networkd` (約 2012 年，隨 systemd 引入)

- 定位： 作為 `systemd` 服務套件的一部分，專注於伺服器、虛擬機和容器環境。
- 特性： 輕量級、高效能，基於 宣告式 (Declarative) 的 .network 檔案配置。它與 `systemd` 的其他組件（如 `systemd-resolved` 處理 DNS）緊密整合。
- 影響： 受到那些推崇 `systemd` 極簡主義和統一管理哲學的發行版（如 Arch Linux、CoreOS）青睞。

`wicked` (約 2012 年，SUSE/openSUSE)

- 定位： SUSE 為取代傳統 `ifup`/`ifdown` 腳本而開發的下一代網路配置服務。
- 特性： 強調在企業級伺服器環境中的可擴展性、靈活性和複雜網路配置的支援（如 Bonding, VLAN）。
- 影響： 成為 SUSE/openSUSE 發行版伺服器配置的標準。

4. 抽象層與統一配置 (約 2017 年開始)

網路管理服務眾多，配置檔格式各異 (ifcfg、.network、interfaces、NetworkManager Profile)，使得發行版之間的遷移或統一管理變得困難。這個階段的發展重點是建立一個抽象層。

`Netplan` (2017 年，Ubuntu 17.10 引入)

- 定位： 一個網路配置抽象渲染器 (Renderer)。
- 特性： 使用單一的、簡潔的 YAML 格式配置檔（位於 /etc/netplan/*.yaml）。使用者只須定義所需的網路狀態，`Netplan` 會自動將 YAML 轉換並「渲染」成底層網路服務（如 `NetworkManager` 或 `systemd-networkd`）所需的特定配置檔案。
- 影響： 成為 Ubuntu 伺服器和桌面版本的標準配置方法，將使用者與底層的網路服務解耦。
