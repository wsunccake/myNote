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
linux:~ # reboot
```

### user

unconfined_u: unconfined SELinux user

```bash
# selinux user map
semanage login -l

# selinux user
seinfo -u
seinfo -r
seinfo -t

id -Z
```

user_u: Is the SELinux user.
user_r: Is the SELinux role.
user_t: Is the SELinux type.

### semanage

```bash
semanage <argument>
```

**argument**

- `import`: 匯入 (Import) 本地化客製設定。 使用 semanage export 匯出的本地策略自訂設定檔案，匯入到系統中，通常用於還原或跨系統遷移設定。
- `export`: 匯出 (Output) 本地化客製設定。 輸出目前 SELinux 策略中所有本地化（非預設）的變更（例如 fcontext、port、login 等設定）到一個檔案，便於備份或遷移。
- `login`: 管理登入映射 (Login Mapping)。 管理 Linux 使用者名稱與 SELinux 使用者身份之間的映射關係。這是控制使用者登入後獲得初始安全上下文的關鍵。
- `user`: 管理 SELinux 使用者 (SELinux User)。 管理 SELinux 策略中定義的 SELinux 身份（例如 user_u、sysadm_u），以及這些身份可以擁有的角色 (Roles) 和 MLS/MCS 範圍 (Range)。
- `port`: 管理網路埠 (Network Port) 類型定義。 定義網路埠（如 TCP 或 UDP 埠）的安全上下文（type 欄位），允許特定的服務（如 httpd_t）綁定到非標準埠。
- `interface`: 管理網路介面 (Network Interface) 類型定義。 管理網路介面的 SELinux 上下文，通常用於網絡過濾和 MLS/MCS 系統。
- `module`: 管理 SELinux 策略模組 (Policy Module)。 載入、移除或啟用/禁用 SELinux 策略模組，用於動態地增加或移除特定的應用程式安全規則集。
- `node`: 管理網路節點 (Network Node) 類型定義。 管理網路主機或節點的 SELinux 上下文，通常用於 MLS/MCS 環境中為遠端連線設定標籤。
- `fcontext`: 管理檔案上下文 (File Context) 映射定義。 定義檔案路徑 (File Path) 與其應有的 SELinux 檔案類型 (File Type) 之間的映射規則，供 restorecon 命令使用以永久性地設定檔案標籤。
- `boolean`: 管理 SELinux 布林值 (Booleans)。 調整 SELinux 策略中的開關，這些布林值允許管理員在不修改核心策略的情況下，選擇性地啟用或禁用某些行為（例如 httpd_can_network_connect）。
- `permissive`: 管理寬容模式 (Permissive) 的領域。 將特定的程序領域 (Domain) 設置為寬容模式，意味著該程序發生的任何拒絕操作只會被記錄 (log) 而不會被強制執行 (enforce)。常用於除錯。
- `dontaudit`: 管理 dontaudit 規則。 禁用或啟用策略中的 dontaudit 規則。這些規則通常用於抑制大量不影響執行的存取拒絕訊息，但禁用它可以幫助更全面地查看所有拒絕事件。
- `ibpkey`: 管理 InfiniBand P_Key 類型定義。 專用於 InfiniBand 網路的策略管理，定義 P_Key 的 SELinux 上下文。
- `ibendport`: 管理 InfiniBand 終端埠類型定義。 專用於 InfiniBand 網路的策略管理，定義 InfiniBand 終端埠的 SELinux 上下文。

### file context

1. User (使用者)

- 格式範例： unconfined_u (不受限使用者)、system_u (系統服務)。
- 作用： 將 Linux 登入使用者映射到一個 SELinux 使用者身份。這通常用於限制登入使用者可以扮演的角色 (Role) 和可以執行的程序類型 (Type)。
- 常見情況： 對於大多數服務和檔案，您通常會看到 system_u 或 unconfined_u。一般使用者帳號登入後，其程序多半運行在 unconfined_u 下 (除非特別配置)。

```bash
# selinux user
linux:~ # seinfo -u [<user>] [-x]

linux:~ # semanage user -l
linux:~ # semanage user -a -R <ROLE> [-L <LEVEL>] [-r <RANGER>]  <USER>
linux:~ # semanage user -d <USER>
```

```bash
# linux user map selinux user
linux:~ # useradd -Z <USER> <user>
linux:~ # usermod -Z <USER> <user>

linux:~ # id -Z

linux:~ # semanage login -l
linux:~ # ps auxZ
```

2. Role (角色)

- 格式範例： object_r (客體/檔案角色)、system_r (系統角色)。
- 作用： 限制一個程序可以存取的類型 (Type)。它作為一個中介層，限制了 SELinux 使用者可以採用的程序角色。
- 常見情況：
  - 檔案/客體 (Objects)： 都是 object_r。
  - 程序 (Processes)： 大多是 system_r。

`user_r`, `staff_r`, `sysadm_r`, 和 `unconfined_r` 是 SELinux 策略中定義的四個主要角色 (Roles)。目標是實現 RBAC (Role-Based Access Control)，即根據使用者當前的職責或任務來限制其權限。

| Role Name      | Privilege Level         | Intended Use                                                    | Key Restrictions                                                                                                                                                                                 |
| -------------- | ----------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `user_r`       | Confined / 基本使用者   | 標準的日常使用者、Web 瀏覽、文件編輯等非管理任務。              | 高度受限。 無法使用 su 或 sudo 切換使用者或提升權限。無法直接執行大多數系統管理任務。                                                                                                            |
| `staff_r`      | Confined / 具備管理潛力 | 具備系統管理能力，但預設在受限模式下運行的使用者。              | 受限，但允許使用 sudo。 登入後預設受限（類似 user_r），但策略允許其透過 sudo 過渡到更寬鬆的角色（如 sysadm_r 或 unconfined_r）來執行管理命令。                                                   |
| `sysadm_r`     | Confined / 系統管理員   | 專門用於執行全面系統配置、服務管理和根級別任務的管理員。        | 受限的管理員。 雖然權限很高，但其程序網域 (sysadm_t) 仍然受到 SELinux 策略的約束，這比 unconfined_r 更安全。例如，它可以管理系統文件，但可能被限制運行某些未被策略明確允許的應用程序。           |
| `unconfined_r` | Unconfined / 最寬鬆     | 幾乎不受 SELinux 限制的程序。通常用於相容性或特殊的高權限服務。 | 最小限制。 該角色允許程序運行在 unconfined_t 網域中，使其幾乎可以做任何事，等同於傳統 Linux 的 DAC 權限（User/Group/Other）。任何拒絕通常是由 Linux 自己的 DAC 或其他安全模組而非 SELinux 造成。 |

```bash
linux:~ # seinfo -r [<ROLE>] [-x]
```

3. Type (類型) / Domain (領域) (最重要的部分)

- 格式範例： httpd_t (Apache 程序的類型/領域)、httpd_sys_content_t (網頁檔案內容的類型)。
- 作用：
  - 程序 (Subject)： 稱為 Domain (領域)，定義了程序能做什麼。
  - 檔案 (Object)： 稱為 Type (類型)，定義了該資源的用途。
- 核心運作： SELinux 策略主要就是基於 Type 之間的規則運作。例如：
  - 策略會規定：httpd_t 領域的程序被允許 (allow) 讀取 (read) 標籤為 httpd_sys_content_t 類型的檔案。
  - 策略會規定：httpd_t 領域的程序被拒絕 (deny) 寫入 (write) 標籤為 etc_t 類型的檔案。

```bash
linux:~ # seinfo -t
```

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
linux:~ # getsebool ssh_sysadm_login

# temporary change
linux:~ # setsebool ssh_sysadm_login on

# permanent change
linux:~ # setsebool -P ssh_sysadm_login on

#               State   Default
# setsebool     V       X
# setsebool -N  V       X
# setsebool -P  V       V
# State: current
# Default: persistently, after reboot

linux:~ # semanage boolean -l | grep ssh_sysadm_login
linux:~ # semanage boolean -m --on|--off ssh_sysadm_login
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

linux:~ # sealert -l "*"

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
