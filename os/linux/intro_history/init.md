# init

##　 history

Init（Initialization）是 Linux 核心啟動後在使用者空間（User Space）中執行的第一個程序（PID 1），它負責啟動系統中的所有其他服務、程序和資源，是系統正常運作的基石。隨著 Linux 應用場景的擴展（從伺服器到桌面、行動裝置、嵌入式），Init 系統也經歷了兩次重大演進。

1. `SysVinit` (System V init)

- 年代： 1980 年代（源自 UNIX System V），長期以來是大多數 Linux 發行版的標準。
- 設計理念： 簡單、可靠，完全依賴 Shell Script 來啟動和停止服務。
- 執行方式： 串行啟動（Sequential）：服務依賴性處理簡單，通常是依次啟動。必須等到前一個服務完全啟動後，才能啟動下一個服務。
- 配置文件： 服務的啟動和停止邏輯寫在 /etc/init.d/ 下的 Shell Script 中。
- 運行模式： 使用 Runlevel（運行級別） 來定義系統的狀態（例如：級別 3 是多使用者文字模式，級別 5 是圖形介面模式）。
- 主要優點： 成熟穩定、相容性高、邏輯清晰易懂（就是腳本）。
- 主要缺點： 開機速度慢（串行啟動）、缺乏彈性、難以處理服務之間的複雜相依性（需要手動維護腳本中的順序）。
- 代表發行版： 早期絕大多數的 Linux 發行版（如 Red Hat、Debian、SuSE、Slackware）。

2. `Upstart`

- 年代： 2006 年左右（由 Ubuntu 開發），作為 SysVinit 的改良替代品。
- 設計理念： 解決 SysVinit 啟動慢和事件處理能力不足的問題，轉向事件驅動。
- 執行方式： 事件驅動（Event-driven）：服務的啟動和停止不再是固定的順序，而是依賴於特定的系統事件（如：網路卡被偵測到、檔案系統掛載完成）。
- 平行化： 允許部分平行啟動服務，提高了開機速度。
- 配置文件： 使用專門的 .conf 配置文件（通常在 /etc/init/），而不是 Shell Script，來定義服務及其觸發事件。
- 程序追蹤： 使用 strace 等工具間接追蹤服務產生的子程序。
- 主要優點： 顯著改善了開機速度；能夠動態響應系統運行時的事件（例如：熱插拔設備）；與 SysVinit 腳本有一定向下相容性。
- 主要缺點： 事件定義不夠完善，對複雜服務相依性的處理仍有侷限性；無法可靠地追蹤服務進行二次 fork 後產生的所有程序。
- 代表發行版： Ubuntu (6.10 到 15.04)、早期 Fedora、RHEL 6。

3. `systemd`

- 年代： 2010 年至今（由 Red Hat 開發），目前是主流 Linux 發行版的標準 Init 系統。
- 設計理念： 提供一套完整、高效的系統和服務管理解決方案，致力於統一 Linux 系統的啟動和管理流程。
- 執行方式： 高度平行化：透過 Socket 啟用（Socket Activation）和 D-Bus 啟用等技術，服務可以同時啟動，極大縮短開機時間。
- 配置文件： 使用專門的 Unit 文件（例如 .service, .target, .mount, .timer 等）來定義系統資源。
- 程序追蹤： 採用 Linux 核心的 cgroups（控制群組）功能，可以精確追蹤服務產生的所有子程序，確保完全停止和資源控制。
- 核心工具： 使用 systemctl 集中管理所有服務和系統狀態；使用 journalctl 內建日誌管理系統。
- 主要優點： 極速開機；強大的程序追蹤和資源管理能力；功能高度整合（包含日誌、網路配置、時間同步等）；Target 取代了 Runlevel。
- 主要缺點： 體系龐大複雜，導致部分使用者認為其設計過於「臃腫」；與傳統 UNIX 哲學（單一程式做好一件事）有所背離。
- 代表發行版： 目前絕大多數主流發行版，包括 Fedora、RHEL 7+、CentOS 7+、Debian 8+、Ubuntu 15.04+、Arch Linux 等。

---

## `systemd`

`systemd` 將所有它管理的系統資源和任務都抽象化為一個基本單位，稱為 Unit（單位）。每個 Unit 都由一個特定的**配置文件（Unit File）**來定義，並以其文件擴展名（後綴）來區分其類型和功能。

```bash
linux:~ # systemctl -t help
```

| Unit      | suffix     | 主要功能與特色                                                                                                     |
| --------- | ---------- | ------------------------------------------------------------------------------------------------------------------ |
| Service   | .service   | 最常見的類型。 用於啟動、停止、重啟和管理系統守護程序（Daemon）或應用程序。                                        |
| Target    | .target    | 同步點和分組。 用於將多個 Unit 組合在一起，定義系統要進入的狀態（類似於 SysV-init 的 Runlevel）。                  |
| Socket    | .socket    | 通訊端啟用。 用於監聽網路或 IPC 通訊端，當通訊端上有活動時，會按需啟動相關的 .service Unit。                       |
| Timer     | .timer     | 排程任務。 用於定義定時或週期性事件，功能類似於 cron，當時間到達時，會觸發相關的 .service Unit。                   |
| Path      | .path      | 路徑啟用。 用於監控特定的檔案或目錄路徑，當路徑狀態發生變化時，觸發相關的 .service Unit。                          |
| Mount     | .mount     | 檔案系統掛載。 用於定義和控制系統中的檔案系統掛載點（取代部分 /etc/fstab 功能）。                                  |
| Automount | .automount | 按需自動掛載。 用於配置延遲掛載點，只有當訪問該目錄時才進行實際掛載。                                              |
| Swap      | .swap      | 交換空間管理。 用於定義和管理系統中的交換設備或交換檔案。                                                          |
| Device    | .device    | 設備管理。 用於表示核心（Kernel）識別的設備，並實現基於設備的啟動（通常由 udev 自動生成）。                        |
| Slice     | .slice     | 資源控制。 用於在 Linux Control Group (cgroups) 樹中創建節點，對一組程序分層管理和限制系統資源（如 CPU、記憶體）。 |
| Scope     | .scope     | 外部程序容器。 用於組織和管理由 systemd 以外程序（例如登入管理器或容器）啟動的程序群組。                           |
| Busname   | .busname   | D-Bus 名稱。 用於追蹤和控制 D-Bus 系統匯流排上的名稱。                                                             |

### service

1. `[Unit]`：通用資訊與依賴關係

這些參數適用於所有 systemd Unit 類型，主要用於定義 Unit 的元數據以及與其他 Unit 的**啟動順序**和**相依性**。

| parameter     | type   | explain                                                                                           | value                                |
| ------------- | ------ | ------------------------------------------------------------------------------------------------- | ------------------------------------ |
| Description   | Single | Unit 的簡短描述，用於 systemctl status 輸出。                                                     | My Custom Web Server                 |
| Documentation | List   | 指向相關文件或手冊頁的 URL 或路徑。                                                               | https://example.com/docs             |
| Requires=     | List   | 強依賴：要求指定的 Unit 必須成功啟動，本 Unit 才能啟動。如果依賴的 Unit 失敗，本 Unit 也會停止。  | network.target                       |
| Wants=        | List   | 弱依賴：本 Unit 啟動時會嘗試啟動指定的 Unit。即使依賴的 Unit 啟動失敗，本 Unit 仍會繼續嘗試啟動。 | mysql.service                        |
| After=        | List   | 啟動順序：確保本 Unit 在指定的 Unit 之後才啟動。這只是排序，不強制拉起依賴 Unit。                 | network.target                       |
| Before=       | List   | 啟動順序：確保本 Unit 在指定的 Unit 之前完成啟動。                                                | multi-user.target                    |
| BindsTo=      |        | 連動相依性：與 Requires 類似，但如果被依賴的 Unit 停止或崩潰，本 Unit 也會被停止。                | dev-sda1.device                      |
| Conflicts=    | List   | 衝突關係：與指定的 Unit 不能同時運行。當本 Unit 啟動時，衝突 Unit 會被停止。                      | httpd.service（與 nginx 服務衝突時） |

2. `[Service]`：服務執行細節與生命週期管理

這些參數僅適用於 Service Unit，定義了服務程序如何**執行**、被**追蹤**以及在**失敗**時如何處理。

2-1. 執行指令

| parameter     | type   | explain                                                     |
| ------------- | ------ | ----------------------------------------------------------- |
| Type          | Single | 啟動模式。`simple`, `forking`, `oneshot`, `notify`, `dbus`  |
| ExecStart     | List   | 啟動服務的指令。 最核心的參數。                             |
| ExecStartPre  | List   | 在執行 ExecStart 之前執行的指令。可用於準備環境或檢查依賴。 |
| ExecStartPost | List   | 在執行 ExecStart 之後執行的指令。可用於後續設定或測試。     |
| ExecStop      | List   | 停止服務的指令。 覆蓋 systemd 預設的訊號處理。              |
| ExecReload    | List   | 重載設定檔的指令。 通常是發送 SIGHUP 訊號給主程序。         |

`simple`:（預設值） ExecStart 中的程序是主程序，且不會 Fork。systemd 視程序開始執行即為啟動完成。現代、簡單的服務程序。
`forking`: 傳統 Daemon 模式。ExecStart 中的程序會 Fork 出子程序後，父程序立即退出。systemd 視父程序退出為啟動完成。傳統的服務程序（如舊版 Apache、Nginx）。通常需要配合 PIDFile。
`oneshot`: 一次性任務。程序執行完畢後退出，systemd 視退出為完成。 | 執行單次腳本或系統配置任務。
`notify`: 類似 simple，但程序必須主動發送通知給 systemd（透過 sd_notify 函式）來宣告自己已準備就緒。複雜的現代服務，確保服務真正準備好才繼續啟動下一個 Unit。
`dbus`: 服務被視為已啟動，直到其在 D-Bus 系統匯流排上取得特定的名稱 (BusName=)。D-Bus 整合的服務，如 NetworkManager。

2-2. 程序管理與安全性

| parameter        | type   | explain                                                           |
| ---------------- | ------ | ----------------------------------------------------------------- |
| PIDFile          | Single | 指定服務主程序 PID 檔案的路徑。 /run/httpd.pid                    |
| User             | Single | 服務程序運行時使用的 Linux 使用者名稱。 nobody                    |
| Group            | Single | 服務程序運行時使用的 Linux 群組名稱。 www-data                    |
| WorkingDirectory | Single | 服務程序運行時的工作目錄。 /srv/my-app                            |
| Environment      | List   | 設置服務運行時的環境變數。 Environment="PORT=8080 API_KEY=abc"    |
| EnvironmentFile  | List   | 從指定的檔案中載入環境變數。 EnvironmentFile=-/etc/default/my-app |
| PrivateTmp       | Single | 安全性增強：預設為 `yes`, `no`                                    |

`yes`:（預設值）會創建一個私有的 /tmp 和 /var/tmp 目錄，與系統和其它服務隔離。

2-3. 錯誤處理與重啟

| parameter      | type   | explain                                                                                          |
| -------------- | ------ | ------------------------------------------------------------------------------------------------ |
| Restart        | Single | 重啟策略：定義在什麼條件下 systemd 應該自動重啟服務。 `no`, `always`, `on-failure`, `on-success` |
| RestartSec     | Single | 如果服務自動重啟，這是兩次嘗試啟動之間的間隔時間。 `1s` 或 `5 seconds`                           |
| TimeoutSec     | Single | 啟動或停止的總超時時間。如果服務在這個時間內未能達到目標狀態，systemd 將宣告失敗。 `30s`         |
| StandardOutput | Single | 標準輸出（STDOUT）的目標。systemd 建議所有日誌輸出到 journald。 `journal`, `null`, `inherit`     |

`no`：（預設值） 永不重啟。
`always`：無論退出狀態或原因如何，總是重啟。
`on-failure`：只有在程序以非零狀態碼退出、被非訊號 1/255 終止、或遇到超時時才重啟。
`on-success`：只有程序成功退出（狀態碼 0）時才重啟。
`journal`：（預設）
`null`
`inherit`

3. `[Install]`：啟用（Enable）設定

這些參數定義了執行 systemctl enable 命令時，Unit 如何被整合到系統的啟動過程中。

| parameter  | type | explain                                                                                                           |
| ---------- | ---- | ----------------------------------------------------------------------------------------------------------------- |
| WantedBy   | List | 指定本 Unit 應被哪個 Target Unit 所拉起（即在 Target 目錄下創建軟連結）。 `multi-user.target`, `graphical.target` |
| RequiredBy | List | 類似 WantedBy，但使用 強依賴 關係（Requires）。如果本 Unit 啟動失敗，拉起它的 Target 也會失敗。                   |
| Alias      | List | 為 Unit 定義一個或多個別名。當 Unit 被啟用時，這些別名也會被建立。                                                |

`multi-user.target`：在多使用者模式（伺服器常用狀態）下啟動。
`graphical.target`：在圖形介面模式下啟動。

4. example

```conf
[Unit]
Description=My Custom Python Web Server
Documentation=https://example.com/docs
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/mywebapp
ExecStart=/usr/bin/python3 app.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

```conf
Environment="Variable1=Value1"
Environment="Variable2=Value2"
# => 此時為 Variable1=Value1, Variable2=Value2

Environment="Variable1=Value1"
Environment=        # Environment 清空
Environment="Variable2=Value2"
# => 此時為 Variable2=Value2

EnvironmentFile=-file
# 如果 file 不存在也不會報錯誤
```
