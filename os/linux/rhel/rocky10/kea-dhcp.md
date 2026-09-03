# Kea DHCP

**ISC DHCP (經典時代)**

- 誕生： 1990 年代中期，目的是提供一個穩定、標準化的開源 DHCP 實作。
- 特點： 採用單體式架構 (Monolithic)。所有的功能（IPv4、IPv6、管理）全部封裝在一個進程中。
- 現況： ISC 已於 2022 年底正式宣布停止維護 (End of Life)。這意味著它不再獲得新功能，僅處理極其嚴重的安全性漏洞。

**Kea DHCP (雲端與自動化時代)**

- 誕生： 2014 年左右推出，是為了克服 ISC DHCP 的架構限制而重新編寫的「下一代」產品。
- 特點： 採用模組化架構，並引入了現代軟體工程的特性（如 REST API）。
- 現況： 目前開發非常活躍，是 ISC 官方推薦的替代方案。

| 特性               | ISC DHCP                                   | Kea DHCP                                    |
| ------------------ | ------------------------------------------ | ------------------------------------------- |
| 架構設計           | 單體式，啟動時需讀取完整設定檔。           | 模組化，IPv4、IPv6、控制代理分別運行。      |
| 配置動態性         | 修改設定通常需要重啟服務，會造成短暫中斷。 | 支援 REST API，可在不重啟的情況下修改設定。 |
| 資料儲存 (Backend) | 使用純文字檔 (dhcpd.leases)。              | 支援 MySQL、PostgreSQL、Cassandra。         |
| 效能               | 較慢，適合中小規模環境。                   | 極高，每秒可處理上萬次租約請求。            |
| 擴充性             | 需透過原始碼修改或複雜指令碼。             | 支援 Hooks 函式庫，方便開發者自定義功能。   |
| 維護狀態           | 已停止維護 (EOL)。                         | 持續更新與維護。                            |

---

## server - ipv4

```bash
rocky:~ # dnf install kea
rocky:~ # ls /etc/kea/

# config
rocky:~ # cp /etc/kea/kea-dhcp4.conf /etc/kea/kea-dhcp4.conf.org
rocky:~ # vi /etc/kea/kea-dhcp4.conf
rocky:~ # chown root:kea /etc/kea/kea-dhcp4.conf
rocky:~ # chmod 640 /etc/kea/kea-dhcp4.conf

# service
rocky:~ # systemctl enable --now kea-dhcp4

# firewall
rocky:~ # firewall-cmd --add-service=dhcp
rocky:~ # firewall-cmd --runtime-to-permanent

# leased ip
rocky:~ # ls /var/lib/kea/
rocky:~ # cat /var/lib/kea/kea-leases4.csv
```

```json
// /etc/kea/kea-dhcp4.conf
{
  "Dhcp4": {
    "interfaces-config": {
      "interfaces": ["eth1"]
    },

    "control-socket": {
      "socket-type": "unix",
      "socket-name": "kea4-ctrl-socket"
    },

    "lease-database": {
      "type": "memfile",
      "lfc-interval": 3600
    },

    "expired-leases-processing": {
      "reclaim-timer-wait-time": 10,
      "flush-reclaimed-timer-wait-time": 25,
      "hold-reclaimed-time": 3600,
      "max-reclaim-leases": 100,
      "max-reclaim-time": 250,
      "unwarned-reclaim-cycles": 5
    },

    "renew-timer": 900,
    "rebind-timer": 1800,
    "valid-lifetime": 3600,

    "option-data": [
      {
        // dns server
        "name": "domain-name-servers",
        "data": "8.8.8.8, 1.1.1.1"
      }
    ],

    "subnet4": [
      {
        "id": 1,
        "subnet": "192.168.61.0/24",
        "pools": [{ "pool": "192.168.61.101 - 192.168.61.200" }],
        // "interface": "eth0",
        "option-data": [
          {
            "name": "routers",
            "data": "192.168.61.254"
          }
        ],
        "reservations": [
          {
            "hw-address": "00:0c:29:e4:c9:a5",
            "ip-address": "192.168.61.43"
          }
        ]
      }
    ],

    "loggers": [
      {
        "name": "kea-dhcp4",
        "output-options": [
          {
            "output": "kea-dhcp4.log"
          }
        ],
        "severity": "INFO",
        "debuglevel": 0
      }
    ]
  }
  
}
```
