# apache2

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
