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

ro/rw, sync/async, root_squash/no_root_squash, all_squash

### server - daemon

```bash
nfs:~ # systemctl start nfs-server
nfs:~ # systemctl enable nfs-server
```

### firewall

```bash
nfs:~ # firewall-cmd --permanent --add-service=nfs
nfs:~ # firewall-cmd --reload
```

### test

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
