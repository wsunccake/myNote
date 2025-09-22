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
