# chrony

## history

網路時間協定（NTP）的演進歷程反映了電腦對時間精確度的需求不斷提升，以及網路環境的變化。從早期的簡化版本到功能強大的現代實作，這段歷史可以分為三個主要階段：

1.  `NTP` (Network Time Protocol)：精準時間同步的基石

    NTP 是由美國特拉華大學的 David L. Mills 博士在 1980 年代初期開發的，旨在解決網路中電腦時間同步的問題。NTP 的設計非常複雜且強大，它不僅僅是簡單地將伺服器時間傳給客戶端，還包含了一套複雜的演算法來精確計算並補償網路延遲、抖動以及時鐘漂移。

    NTP 的核心特色包括：

         - 分層架構（Stratum）：NTP 伺服器被分為不同的層級，Stratum 0 是最精確的參考時鐘（如原子鐘或 GPS 時鐘），Stratum 1 伺服器直接與 Stratum 0 連接，依此類推。客戶端通常會連接到 Stratum 1、2 或 3 的伺服器。
         - 多伺服器冗餘：一個 NTP 客戶端可以同時向多個伺服器請求時間，並透過複雜的統計演算法來篩選出最可靠、最精確的時間來源，有效防止單一伺服器故障或惡意篡改。
         - 持續調整時鐘頻率（Clock Discipline）：NTP 不會粗暴地「跳躍」時間（除非時間差異過大），而是透過微調系統時鐘的頻率來緩慢修正時間偏差，確保時間平穩過渡，避免對應用程式造成不良影響。

    NTP 的強大功能使其成為企業、研究機構和網際網路基礎設施中不可或缺的標準，至今仍是絕大多數網路時間同步的基礎。

2.  `SNTP` (

## service

```bash
sle:~ # systemctl enable chronyd
sle:~ # systemctl start chronyd
```

## config

```bash
sle:~ # vi /etc/chrony.conf
sle:~ # ls /etc/chrony.d
```

## command

```bash
sle:~ # chronyc sources         # list ntp source
sle:~ # chronyc sources -v
sle:~ # chronyc sourcestats
sle:~ # chronyc tracking
sle:~ # chronyc activity

sle:~ # chronyc -a makestep
sle:~ # chronyc -a 'burst 4/4'       # sync time
```
