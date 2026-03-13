# tuned

## service

```bash
rocky:~ # systemctl status tuned
rocky:~ # systemctl enable --now tuned

```

```bash
rocky:~ # tuned-adm active     # current profile
rocky:~ # tuned-adm list          # show all profile
rocky:~ # tuned-adm profile <profile> # change <profile>
rocky:~ # tuned-adm recommend     # recommend profile
```

| Profile                | Situation            | 優化重點                             |
| ---------------------- | -------------------- | ------------------------------------ |
| balanced               | 一般桌面或通用伺服器 | 兼顧效能與省電（預設值）             |
| throughput-performance | 高負載伺服器         | 追求最大吞吐量，關閉節能模式         |
| latency-performance    | 資料庫、即時運算     | 降低延遲，CPU 始終保持高頻           |
| powersave              | 筆電、需極端省電環境 | 最大程度降低功耗                     |
| virtual-guest          | 虛擬機 (Guest OS)    | 針對虛擬化環境進行磁碟與記憶體優化   |
| mssql / oracle         | 特定資料庫           | 專為 SQL Server 或 Oracle 優化的參數 |
