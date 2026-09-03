# esxcli 7

```bash
# syntax
esxcli [options] {namespace}+ {cmd} [cmd options]

esxcli --help
esxcli --help network
esxcli --version
```

| Namespace | Explain                                           | 常用場景範例                                   |
| --------- | ------------------------------------------------- | ---------------------------------------------- |
| network   | 管理 vSwitch、NIC、IP、Firewall 及 DNS。          | 查詢 Port Group 名稱以利部署 OVA。             |
| storage   | 管理 storage、VMFS、PSP 及驅動。                  | 查詢 Datastore 剩餘空間或掛載新磁碟。          |
| system    | 管理系統版本、主機名、服務 (SSH/NTP) 及核心統計。 | 開啟/關閉 SSH 服務，或查詢系統組建版本。       |
| vm        | 控制虛擬機進程（非一般電源管理）。                | 當 VM 卡死且 Web UI 無法操作時，強制刪除進程。 |
| hardware  | 查詢與設定 CPU、Memory、PCI、IPMI 及平台資訊。    | 查詢伺服器序號 (SN) 或 CPU 型號。              |
| software  | 管理 ESXi VIBs、更新檔及軟體版本。                | 安裝新版驅動程式或確認系統補丁狀態。           |
| device    | 裝置管理器，管理硬體裝置的列舉與驅動關聯。        | 查詢特定硬體裝置的別名或狀態。                 |
| vsan      | 專用於 VMware vSAN 叢集的管理與疑難排解。         | 檢查 vSAN 儲存池狀態或磁碟組資訊。             |
| nvme      | 專門管理 NVMe 儲存裝置及其驅動操作。              | 查詢 NVMe SSD 的健康狀態與命名空間。           |
| iscsi     | 管理 iSCSI (HBA) 與 (Target) 連線。               | 設定 iSCSI 網路儲存掛載。                      |
| fcoe      | 管理 Fibre Channel over Ethernet。                | 查詢 FCoE 介面卡資訊。                         |
| rdma      | 管理遠端直接記憶體存取 (RDMA) 協定棧。            | 用於高效能網路（如 InfiniBand 或 RoCE）設定。  |
| graphics  | 管理 GPU 資源與圖形顯示設定。                     | 查詢虛擬桌面 (VDI) 環境中的顯卡分配。          |
| sched     | 管理核心排程、資源池與 CPU 分配策略。             | 調整特定的核心資源分配優先順序。               |
| daemon    | 控制使用 Daemon SDK (DSDK) 開發的後台服務。       | 進階開發者用於管理自定義插件。                 |
| esxcli    | 關於 esxcli 指令集本身的資訊與清單。              | 查詢 esxcli 支援的所有指令路徑。               |

---

## network

```bash
esxcli network

esxcli network ip interface ipv4 get

esxcli network vswitch standard portgroup list
esxcli network vm list
```

---

## storage


```bash
esxcli storage filesystem list
```

---

## vm

```bash
esxcli vm process list
```

---

## system

```bash
esxcli system version get
```