# apache2

## history

網頁伺服器的歷史，從最初的簡單工具發展到現在複雜且高效的軟體生態系統，是一部與網際網路演進緊密相連的歷史。這個過程可以大致分為幾個關鍵階段：

第一階段：草創期 (1990 年代初期)

網頁伺服器最初是為學術研究而生，功能極其單純，主要任務就是「傳輸靜態檔案」。

- 開端 (1990)：Tim Berners-Lee 在 CERN 建立了世界上第一個網頁伺服器軟體 CERN httpd。這款軟體與第一個網頁瀏覽器 WorldWideWeb 一起，奠定了 HTTP 協定與網頁傳輸的基礎。
- 早期發展 (1993-1995)：伊利諾大學國家超級電腦應用中心 (NCSA) 的 NCSA HTTPd 成為當時最受歡迎的伺服器之一。它的功能比 CERN httpd 更進一步，並開始支援伺服器端腳本（如 CGI），這為動態網頁內容的出現鋪平了道路。

第二階段：百家爭鳴與市場主導 (1990 年代中後期)

隨著網際網路商業化，網頁伺服器軟體的需求激增，市場進入了激烈競爭的時代。

- Apache 的崛起 (1995)：當 NCSA HTTPd 的開發者離開後，一群開發者將其修復並改進，創造了 Apache HTTP Server。這個名字來自於「a patchy server」（一個修補過的伺服器）。Apache 以其穩固、可靠、高度可配置的特性迅速佔領市場，並在很長一段時間內成為主導者。它的開放原始碼性質也推動了整個網頁技術的發展，成為 LAMP (Linux, Apache, MySQL, PHP) 堆棧的核心。
- 微軟的加入 (1995)：微軟推出了 Internet Information Services (IIS)，並將其與 Windows NT 系統捆綁銷售。這使得 IIS 在企業市場中佔有一席之地，並與 Apache 形成競爭。IIS 的優勢在於與微軟生態系（如 ASP.NET）的深度整合。

第三階段：高效能與高併發的挑戰 (2000 年代後)

隨著 Web 2.0 的興起，互動式應用程式、社群媒體、大量即時資料傳輸對伺服器的效能提出了更高的要求。傳統的「一次一個請求」處理模式開始顯得力不從心。

- Nginx 的誕生 (2004)：為了應對高流量網站的「C10K 問題」（如何同時處理 10,000 個以上連線），Igor Sysoev 開發了 Nginx。Nginx 的核心優勢在於其非同步、事件驅動的架構。它不像 Apache 那樣為每個請求都啟動一個新進程，而是使用少量的進程來處理大量的並發請求。這讓它在處理靜態檔案、作為反向代理伺服器、負載均衡器等方面表現出色。
- 輕量化伺服器：除了 Nginx，許多其他的輕量級伺服器也隨之出現，例如 Lighttpd，它們都以低資源消耗和高效率為主要賣點。

第四階段：容器化與微服務時代 (2010 年至今)

雲端計算、微服務架構和容器技術的普及，再次改變了網頁伺服器軟體的應用方式。

- 內建伺服器 (Node.js, Go 等)：現代的應用程式框架，例如 Node.js 和 Go，通常會內建一個輕量級的 HTTP 伺服器，讓開發者可以直接啟動應用程式而不需要額外安裝 Apache 或 Nginx。這使得應用部署更加簡單，也讓伺服器與應用程式的結合更緊密。
- 反向代理與邊緣運算：在現代架構中，Apache 或 Nginx 已經不再是唯一的選擇，它們更多地作為反向代理伺服器，將請求分發給後端的多個應用伺服器。而像 Cloudflare Workers 這樣的服務，則將部分伺服器邏輯推向網路邊緣，以極大地減少延遲。

| 軟體名稱      | 發布年代  | 主要特點                     | 扮演角色                           |
| ------------- | --------- | ---------------------------- | ---------------------------------- |
| CERN httpd    | 1990s 初  | 史上第一個網頁伺服器         | 奠基者，靜態內容傳輸               |
| Apache HTTPD  | 1995      | 模組化、可配置、高可靠性     | 穩定的市場領導者，通用網頁伺服器   |
| Microsoft IIS | 1995      | 與 Windows 系統深度整合      | 企業級解決方案，Windows 環境首選   |
| Nginx         | 2004      | 非同步、事件驅動、高效能     | 反向代理、負載均衡，高併發網站首選 |
| Node.js/Go    | 2009/2012 | 內建伺服器，輕量化、部署簡單 | 應用伺服器、API 服務               |

---

## port

- http: 80/tcp
- https: 443/tcp

---

## server

### server - package

```bash
http:~ # zypper in apache2 apache2-prefork
http:~ # zypper in yast2-http-server
```

### server - config

- method 1 - by yast

```bash
http:~ # yast http-server
```

- method 2 - by manual

```bash
# config
http:~ # ls /etc/apache2/
http:~ # vi /etc/apache2/httpd.conf
```

```conf
# /etc/apache2/httpd.conf
Include /etc/apache2/uid.conf
Include /etc/apache2/server-tuning.conf
ErrorLog /var/log/apache2/error_log
<IfDefine !SYSCONFIG>
  Include /etc/apache2/loadmodule.conf
</IfDefine>
Include /etc/apache2/listen.conf
Include /etc/apache2/mod_log_config.conf
<IfDefine !SYSCONFIG>
  Include /etc/apache2/global.conf
</IfDefine>
Include /etc/apache2/mod_status.conf
Include /etc/apache2/mod_info.conf
Include /etc/apache2/mod_reqtimeout.conf
Include /etc/apache2/mod_cgid-timeout.conf
Include /etc/apache2/mod_usertrack.conf
Include /etc/apache2/mod_autoindex-defaults.conf
TypesConfig /etc/apache2/mime.types
Include /etc/apache2/mod_mime-defaults.conf
Include /etc/apache2/errors.conf
Include /etc/apache2/ssl-global.conf
Include /etc/apache2/protocols.conf
<Directory />
    Options None
    AllowOverride None
    <IfModule !mod_access_compat.c>
        Require all denied
    </IfModule>
    <IfModule mod_access_compat.c>
        Order deny,allow
        Deny from all
    </IfModule>
</Directory>
AccessFileName .htaccess
<Files ~ "^\.ht">
    <IfModule !mod_access_compat.c>
        Require all denied
    </IfModule>
    <IfModule mod_access_compat.c>
        Order allow,deny
        Deny from all
    </IfModule>
</Files>
DirectoryIndex index.html index.html.var
Include /etc/apache2/default-server.conf
IncludeOptional /etc/apache2/vhosts.d/*.conf

http:~ # apache2ctl configtest
```

### server - daemon

```bash
http:~ # systemctl start httpd
http:~ # systemctl enable httpd
```

### server - firewall

```bash
http:~ # firewall-cmd --permanent --add-service=apache2
http:~ # firewall-cmd --permanent --add-service=apache2-ssl
http:~ # firewall-cmd --reload
```

### server - qa

常見問題與疑難排解

- 防火牆問題: 確保 80 埠（443 埠，如果使用 HTTPS）在您的 Web 伺服器上是開放的。
- DocumentRoot 設定錯誤: 檢查 httpd.conf 或虛擬主機設定檔中的 DocumentRoot 路徑是否正確，並且實際的網頁檔案位於該目錄中。
- 檔案權限問題: Apache 伺服器 (通常以 wwwrun 用戶運行) 需要對您的網頁檔案和目錄有讀取權限。如果 Apache 無法讀取檔案，您會看到 403 Forbidden 錯誤。
- 服務未啟動: 使用 sudo systemctl status apache2 查看服務狀態和日誌訊息，以獲取錯誤資訊。錯誤日誌通常在 /var/log/apache2/error_log。
- 虛擬主機設定問題: 如果您使用虛擬主機，請確保 ServerName 和 ServerAlias 與您的網域名稱匹配，並且您的 DNS 伺服器已將這些網域名稱解析到 Web 伺服器的 IP 位址。
- SELinux/AppArmor: 在某些安全性強化的 SUSE 環境中，SELinux 或 AppArmor 可能會阻止 Apache 存取某些目錄。如果遇到奇怪的權限問題，請檢查相關日誌（如 /var/log/audit/audit.log 或 journalctl -u apparmor）。通常，將內容放在 /srv/www/ 下會自動獲得正確的上下文。
- 日誌檔: 定期檢查 Apache 的錯誤日誌 (/var/log/apache2/error_log) 和訪問日誌 (/var/log/apache2/access_log)，它們是排除故障的重要工具。
