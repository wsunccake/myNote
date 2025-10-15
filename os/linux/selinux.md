# selinux

## concept

SELinux 實施的是強制存取控制 (MAC, Mandatory Access Control)，這與傳統的 自由裁量存取控制 (DAC) 有根本區別：

| 特性     | DAC (傳統 Linux 權限)                 | MAC (SELinux)                                             |
| -------- | ------------------------------------- | --------------------------------------------------------- |
| 控制基礎 | 使用者和檔案所有權。                  | 安全上下文 (Context)。                                    |
| 誰決定   | 資源的擁有者可以自由決定 (自由裁量)。 | 系統管理員和安全策略決定，使用者無法更改。                |
| 安全性   | 容易被權限提升或應用程式漏洞繞過。    | 即使 root 或應用程式被攻破，其權限仍受 SELinux 策略限制。 |

🔒 要素

SELinux 的運作基於一套簡單的邏輯： Subject 能否對 Object 執行特定操作，取決於 Security Context 是否允許。

- Subject / 主體： 試圖存取資源的程序 (Process) 或使用者。
- Object / 客體： 被存取的資源，如檔案、目錄、網路端口等。
- Security Context / 安全上下文： 這是 SELinux 的靈魂。每個主體和客體都有一個標籤，稱為上下文。

例子： 網頁伺服器程序 (httpd) 的上下文可能是 httpd_t；網頁文件 (index.html) 的上下文可能是 httpd_sys_content_t。

策略 (Policy)： SELinux 決定 httpd_t 程序能否讀取 httpd_sys_content_t 檔案的規則集。

---

## usage

### mode

SELinux 有三種運作模式，您可以使用 getenforce 或 sestatus 指令來查看當前模式。

| values     | explain                                                                                |
| ---------- | -------------------------------------------------------------------------------------- |
| enforcing  | SELinux 完全運作，會禁止任何違反安全政策的行為。這是最安全的模式。                     |
| permissive | SELinux 運作，但不會禁止違反安全政策的行為。它只會將違規行為記錄在日誌中。常用於除錯。 |
| disabled   | 關閉 SELinux。不建議使用，因為會移除重要的安全防護。                                   |

```bash
linux:~ # getenforce
linux:~ # sestatus

linux:~ # setenforce 0    # Permissive
linux:~ # setenforce 1    # Enforcing

linux:~ # vi /etc/selinux/config
SELINUX=
```

### file context

1. User (使用者)

- 格式範例： unconfined_u (不受限使用者)、system_u (系統服務)。
- 作用： 將 Linux 登入使用者映射到一個 SELinux 使用者身份。這通常用於限制登入使用者可以扮演的角色 (Role) 和可以執行的程序類型 (Type)。
- 常見情況： 對於大多數服務和檔案，您通常會看到 system_u 或 unconfined_u。一般使用者帳號登入後，其程序多半運行在 unconfined_u 下 (除非特別配置)。

2. Role (角色)

- 格式範例： object_r (客體/檔案角色)、system_r (系統角色)。
- 作用： 限制一個程序可以存取的類型 (Type)。它作為一個中介層，限制了 SELinux 使用者可以採用的程序角色。
- 常見情況：
  - 檔案/客體 (Objects)： 都是 object_r。
  - 程序 (Processes)： 大多是 system_r。

3. Type (類型) / Domain (領域) (最重要的部分)

- 格式範例： httpd_t (Apache 程序的類型/領域)、httpd_sys_content_t (網頁檔案內容的類型)。
- 作用：
  - 程序 (Subject)： 稱為 Domain (領域)，定義了程序能做什麼。
  - 檔案 (Object)： 稱為 Type (類型)，定義了該資源的用途。
- 核心運作： SELinux 策略主要就是基於 Type 之間的規則運作。例如：
  - 策略會規定：httpd_t 領域的程序被允許 (allow) 讀取 (read) 標籤為 httpd_sys_content_t 類型的檔案。
  - 策略會規定：httpd_t 領域的程序被拒絕 (deny) 寫入 (write) 標籤為 etc_t 類型的檔案。

4. Level (等級) / MLS/MCS (多層次/多類別安全)

- 格式範例： s0 (單一等級)、s0:c0.c1023 (多類別)。
- 作用： 這是用於實現 多層次安全 (MLS, Multi-Level Security) 和 多類別安全 (MCS, Multi-Category Security) 的可選機制。它提供了比 Type 更細緻的存取控制。
  - MLS： 用於軍事和政府環境，強制執行「不能向上寫入，不能向下讀取」的原則。
  - MCS： 常用於虛擬化和容器技術 (如 KVM, Docker)，用於隔離不同的工作負載，確保一個容器中的程序無法存取另一個容器的資源。
- 常見情況： 在大多數標準的 Linux 服務器上，預設只會看到 s0，這表示此功能沒有被主動使用。

```bash
linux:~ # ls -Z /srv/www/htdocs/index.html
unconfined_u:object_r:httpd_sys_content_t:s0 /srv/www/htdocs/index.html
# user:role:type:level

# temporary change
linux:~ # chcon -t httpd_sys_content_t /tmp/myweb.html
# -u: user
# -r: role
# -t: type
# -l: level

# permanent change
linux:~ # semanage fcontext -a -t httpd_sys_content_t "/srv/www(/.*)?"

# restore
linux:~ # restorecon -v /srv/www
```

### selinux boolean

```bash
linux:~ # getsebool -a
linux:~ # getsebool httpd_can_network_connect

# temporary change
linux:~ # setsebool httpd_can_network_connect on

# permanent change
linux:~ # setsebool -P httpd_can_network_connect on
```

### log

```bash
linux:~ # cat /var/log/audit/audit.log
```

### module

```bash
linux:~ # semodule -l           # list
linux:~ # semodule -i <module>  # install
linux:~ # semodule -r <module>  # remove

# generate SELinux policy
linux:~ # ausearch -c '(su)' --raw | audit2allow -M my-su

# add SELinux policy
linux:~ # semodule -X 300 -i my-su.pp
```

---

## config

### kernel policy file

SELinux 的核心規則被編譯成二進位格式，並載入到核心中

| 檔案/路徑                              | 作用                                                                                                                                                   |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| /etc/selinux/config                    | 主要配置文件。 決定 SELinux 運作模式 (SELINUX=enforcing/permissive/disabled) 和策略類型 (SELINUXTYPE=targeted/mls)。永久修改模式需要編輯此檔案後重啟。 |
| /etc/selinux/targeted/policy/policy.\* | 實際策略二進位檔案。 所有核心規則被編譯後結果，系統啟動時會載入此檔案。不應直接編輯它。                                                                |

### file context rules

定義規則路徑 (Path) 應該被標籤為特定的 Type (即 user:role:type:level)

| 檔案/路徑                                          | 作用                                                                                                                    |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| /etc/selinux/targeted/contexts/files/file_contexts | 靜態規則檔案。 包含系統預設的、基於正規表達式路徑的檔案上下文規則。restorecon 指令會參考此檔案。                        |
| semanage fcontext 資料庫                           | 使用 semanage fcontext -a 新增的自定義/本地端規則所儲存的位置。這些規則會覆寫靜態規則，並確保在 restorecon 時永久生效。 |

### booleans and modules

使用 setsebool -P 或 audit2allow 創建新規則時，它們被儲存在單獨的模組中

| 檔案/路徑                                           | 作用                                                                                        |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| /etc/selinux/targeted/modules/active/booleans.local | 布林值狀態檔案。 儲存 setsebool -P 永久設定的布林值狀態 (on/off)。                          |
| /etc/selinux/targeted/modules/active/modules/\*.pp  | 客製化策略模組。 使用 audit2allow 創建並載入新的規則時，會被編譯成一個 .pp 檔案儲存在此處。 |
