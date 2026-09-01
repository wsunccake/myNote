# mount

## moude device

### mount / umount

`mount` 與 `umount` 是 Linux 最底層、最傳統的檔案系統掛載與卸載指令

```bash
umount /dev/sdb1
umount /mnt/usb
```

| 指令   | 作用                           | 基本語法 / 範例                     |
| ------ | ------------------------------ | ----------------------------------- |
| mount  | 將磁碟分割區掛載到指定的目錄   | mount /dev/sdb1 /mnt/usb            |
| umount | 斷開分割區與目錄的連結（卸載） | umount /dev/sdb1 或 umount /mnt/usb |

### udisksctl

`udisksctl` 是 Linux 桌面環境（如 GNOME、KDE、XFCE）用來管理儲存裝置（隨身碟、外接硬碟、SD卡）的命令列工具。

| 操作目標 | 命令範例                        | 說明                                                 |
| -------- | ------------------------------- | ---------------------------------------------------- |
| 查詢裝置 | udisksctl status                | 列出目前連接的所有儲存裝置與代號（如 sdb）           |
| 卸載目錄 | udisksctl unmount -b /dev/sdb1  | 斷開檔案系統（sdb1 為分割區名稱）                    |
| 掛載目錄 | udisksctl mount -b /dev/sdb1    | 自動掛載至 /media/使用者/隨身碟                      |
| 切斷電源 | udisksctl power-off -b /dev/sdb | 安全移除（sdb 為整體裝置名稱，會直接關閉隨身碟電源） |

---

## list device

### lsblk / (List Block Devices)

確認隨身碟代號（如 sdb1）及目前的掛載狀態。

```bash
lsblk
```

觀察最右側的 MOUNTPOINTS。若該分割區後面有路徑代表已掛載；若空白則代表已卸載。

### df / (Disk Free)

檢查隨身碟剩餘空間，或快速驗證是否還在掛載列表中。

```bash
df -h
```

如 df -h 的輸出中找不到 /dev/sdb1 或你的隨身碟名稱，就代表已經成功卸載。

### findmnt / (Find Mount)

精密檢查特定裝置或目錄的掛載詳情。

```bash
findmnt [/dev/sdb1]
```

如執行後完全沒有任何回應（空白輸出），代表該分割區目前完全沒有掛載到系統上。

| 工具    | 主要用途               | 資訊來源             | 特點與優勢                                                                                     |
| ------- | ---------------------- | -------------------- | ---------------------------------------------------------------------------------------------- |
| lsblk   | 顯示硬體結構與階層關係 | /sys 檔案系統        | 直觀顯示實體硬體、分割區（Partitions）與掛載點（Mountpoints）的樹狀 圖，未掛載的裝置也會顯示。 |
| df      | 顯示容量使用率         | /proc/mounts         | 專門查詢磁碟剩餘空間、已用空間與百分比，僅顯示已掛載的檔案系統。                               |
| findmnt | 顯示詳細掛載參數       | /proc/self/mountinfo | 顯示樹狀的掛載架構，能精確查詢特定裝置/目錄的掛載選項（如 rw/ro 讀寫權限）。                   |
