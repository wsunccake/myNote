# NFS

## content

- [server](#server)
  - [server - package](#server---package)
  - [server - config](#server---config)
  - [server - daemon](#server---daemon)
  - [server - other](#server---other)
- [client](#client)
  - [client - package](#client---package)
  - [client - config](#client---config)
  - [client - other](#client---other)

---

## history

NFS (Network File System) 是一個分散式檔案系統協定，由 昇陽電腦 (Sun Microsystems) 於 1984 年開發。它的核心目的是讓客戶端電腦能夠像存取本地檔案一樣，透明地存取遠端伺服器上的檔案。

NFS 的演進主要分為幾個重要的版本，每個版本都針對前一版的弱點進行了改進。

- `NFSv2`：開創性的版本

  - 誕生： 於 1989 年正式發布，NFSv2 是第一個廣泛採用的版本。它為網路檔案共享奠定了基礎。
  - 優點：
    - 簡單且穩健： 協定設計簡單，易於實作。
    - 無狀態 (Stateless)： 伺服器不會追蹤客戶端的狀態，這使得伺服器發生故障後，恢復起來非常簡單，也增加了系統的容錯能力。
  - 缺點：
    - 缺乏安全性： 沒有內建的加密或強大的身分驗證機制。
    - 效能瓶頸： 對於大檔案傳輸效率不高，且檔案大小上限為 2GB。

- `NFSv3`：效能的重大提升

  - 誕生： 於 1995 年發布，NFSv3 的主要目標是解決 NFSv2 的效能和可擴充性問題。
  - 主要改進：
    - 支援大檔案： 突破了 2GB 的檔案大小限制，可以處理超過 64 位元大小的檔案。
    - 異步寫入： 允許伺服器在將資料寫入磁碟之前，就向客戶端確認寫入成功，大大提高了寫入效能。
    - 增強的錯誤處理： 引入了更詳細的錯誤報告機制，讓客戶端能更好地處理伺服器端發生的錯誤。

- `NFSv4`：邁向現代化的里程碑

  - 誕生： 於 2003 年發布，NFSv4 是一個具有里程碑意義的版本，它將 NFS 帶入了現代網路環境。
  - 主要改進：
    - 內建狀態： 改變了 NFSv2 和 v3 的無狀態設計，引入了狀態機制，允許更複雜的功能，如檔案鎖定。
    - 更強的安全性： 內建了 Kerberos 等更強大的身分驗證和加密機制，大大提高了安全性。
    - 單一協定： 將所有操作合併在一個協定中，使用一個單一的 UDP/TCP 埠號 2049。這解決了舊版本需要動態埠號的麻煩，極大地簡化了防火牆的設定。
    - 跨平台支援： 引入了 user@domain 格式的使用者識別方式，更好地支援跨 UNIX 和 Windows 環境的使用者管理。
    - 委託 (Delegation) 功能： 允許伺服器委託客戶端處理某些操作，從而減少網路流量並提高效能。

---

## port

- rpc / portmap : 111/tcp, 111/udp
- nfsv4: 2049/tcp

---

## rpc

```bash
sle:~ # rpcinfo [-p]
```

---

## server

### server - package

```bash
nfs:~ # zypper in nfs-kernel-server
nfs:~ # zypper in yast2-nfs-server
```

### server - config

- method 1 - by yast

```bash
nfs:~ # yast nfs_server
```

- method 2 - by manual

```bash
# config file
nfs:~ # vi /etc/export
/fs1	*(ro,root_squash,sync,subtree_check)
/fs2	192.168.1.0/24(rw,no_root_squash,async,no_subtree_check)
```

/etc/export option

- `ro` / `rw`:
  - `ro` (read-only): 允許客戶端只讀取共用的檔案系統，無法寫入。
  - `rw` (read-write): 允許客戶端讀取和寫入共用的檔案系統。
- `sync` / `async`:
  - `sync`: 這是預設選項。它要求 NFS 伺服器在將變更寫入磁碟之前，不回應客戶端的寫入請求。這確保了資料的完整性，但可能會犧牲一些效能。
  - `async`: 允許 NFS 伺服器在將變更寫入磁碟之前就回應客戶端的寫入請求。這可以提升效能，但有資料遺失或損壞的風險，特別是在伺服器意外重啟時。
- UID/GID Mapping:
  - `root_squash`: 這是預設選項。它將遠端客戶端的 root 使用者的 UID/GID 映射為伺服器上的匿名使用者（nfsnobody）。這能有效防止客戶端的 root 使用者在伺服器上擁有超級管理員權限，是一種重要的安全措施。
  - `no_root_squash`: 不進行 root 映射。這意味著客戶端的 root 使用者在 NFS 伺服器上也能保持 root 權限。除非是在可信任的內部網路環境中，否則強烈不建議使用此選項。
  - `all_squash`: 將所有遠端使用者（包括 root 和非 root）都映射為伺服器上的匿名使用者。
  - `anonuid`=<UID> / `anongid`=<GID>: 與 all_squash 一起使用，可以指定所有使用者和群組所映射的特定 UID 和 GID。
- `secure` / `insecure`:
  - `secure`: 這是預設選項。要求客戶端發起的請求必須來自小於 1024 的特權埠號。
  - `insecure`: 允許客戶端使用任何埠號。
- `subtree_check` / `no_subtree_check`:
  - `subtree_check`: 這是預設選項。當匯出一個子目錄時，NFS 伺服器會檢查客戶端請求的檔案是否真的存在於該子目錄中。這增加了安全性，但會降低效能。
  - `no_subtree_check`: 禁用子目錄檢查。在匯出整個檔案系統或效能是主要考量時非常有用。

mount option

- `soft` / `hard`:
  - `hard`: 這是預設選項。如果 NFS 伺服器沒有回應，客戶端會不斷重試直到伺服器恢復。這能確保資料完整性，但如果伺服器當機，客戶端程序可能會卡住。通常建議用於關鍵應用程式。
  - `soft`: 如果 NFS 伺服器在一定時間後仍沒有回應，客戶端會放棄請求並返回一個 I/O 錯誤。這可以防止程序卡住，但可能導致資料遺失。
- `rsize`=<size> / `wsize`=<size>:
  - `rsize` (read size): 設定 NFS 讀取資料區塊的大小（位元組）。
  - `wsize` (write size): 設定 NFS 寫入資料區塊的大小（位元組）。
  - `nolock`: 禁用檔案鎖定。在連接到不支援鎖定的舊版 NFS 伺服器時可能需要。
  - `nfsvers`=<version>: 選擇 NFS 協定版本，例如 nfsvers=3 或 nfsvers=4。如果沒有指定，系統會自動使用支援的最高版本。NFSv4 引入了許多改進，包括更好的安全性。
  - `nosuid`: 阻止 set-user-ID 或 set-group-ID 位元在掛載的檔案系統上生效。這是一種安全措施，可以防止使用者透過執行特權程式來提升權限。
  - `noexec`: 阻止執行掛載點上的任何二進制檔案。這對於只用於儲存資料的共用很有用。

### server - daemon

```bash
nfs:~ # systemctl start nfs-server
nfs:~ # systemctl enable nfs-server
```

### server - firewall

```bash
nfs:~ # firewall-cmd --permanent --add-service=nfs
nfs:~ # firewall-cmd --reload
```

### server - test

```bash
nfs:~ # showmount -e <nfs_ip>
```

### server - other

```bash
nfs:~ # cat /proc/fs/nfs/exports
nfs:~ # cat /var/lib/nfs/rmtab
```

---

## client

### client - package

```bash
fs:~ # zypper in nfs-client
fs:~ # zypper in yast2-nfs-client
```

### client - config

- method 1 - yast

```bash
fs:~ # yast nfs
```

- method 2 - by manual

```bash
fs:~ # vi /etc/fstab
...
<nfs>:/fs                    /fs   nfs   defaults  0  0

# mount nfs
fs:~ # mount -a
fs:~ # mount -t nfs -o proto=tcp,port=2049 <nfs_ip>:/fs /fs
```

### client - check nfs version

```bash
fs:~ # cat /proc/mounts
fs:~ # mount | grep nfs
fs:~ # nfsstat -m
```
