# bind

## history

1. 前 DNS 時代：HOSTS.TXT

   在網際網路的早期（1980 年代初），電腦數量還很少。當時，要將主機名稱轉換為 IP 位址，使用的是一個名為 HOSTS.TXT 的文字檔。這個檔案由 SRI (Stanford Research Institute) 維護，包含所有已註冊主機的清單。每次有新電腦加入網路，網管員都需要從 SRI 下載最新版本的 HOSTS.TXT。
   隨著網路規模的指數級增長，HOSTS.TXT 的方法很快變得無法維護。檔案變得太大，同步作業也越來越頻繁。這個中心化的系統無法因應快速成長的網路。

2. DNS 的誕生 (1983-1985)：一個分散式的解決方案

   為了解決 HOSTS.TXT 的問題，Paul Mockapetris 在 1983 年設計了 DNS 系統，並在 RFC 882 和 883 中發布。DNS 的核心思想是分散式資料庫：

   - 階層式結構： 採用類似樹狀的階層結構，由根伺服器（Root Servers）、頂級網域名稱伺服器（TLD Servers）和授權名稱伺服器（Authoritative Name Servers）組成。
   - 委託管理： 將命名空間的控制權下放給各個組織。例如，com 網域由一個 TLD 伺服器管理，而 google.com 的具體記錄則委託給 Google 的授權伺服器。這使得網際網路能夠無限擴充。

3. 現代 DNS 的演進

   隨著網際網路的普及，DNS 面臨新的挑戰，主要是在安全性、效能與隱私方面。

   - DNSSEC (DNS Security Extensions)：為了解決 DNS 欺騙和緩存中毒攻擊，DNSSEC 在 2005 年被提出並逐漸推廣。它使用數位簽章來驗證 DNS 記錄的真實性，確保你查詢的結果沒有被惡意篡改。
   - EDNS (Extension Mechanisms for DNS)：早期的 DNS 協定有訊息大小限制，無法承載 DNSSEC 簽章等額外資訊。EDNS 擴展了 DNS 訊息的空間，使其能承載更多資料。
   - DNS over HTTPS (DoH) 和 DNS over TLS (DoT)：傳統的 DNS 查詢是未加密的純文字，容易被竊聽或審查。DoH 和 DoT 透過在 HTTPS 或 TLS 協定上傳輸 DNS 流量，對查詢進行加密，大大提升了使用者的隱私和安全性。

---

## software

DNS 伺服器軟體主要分為兩大類：授權伺服器 (Authoritative Server) 和遞迴解析器 (Recursive Resolver)。許多軟體同時提供這兩種功能。

1. BIND

   全名： Berkeley Internet Name Domain
   特色： BIND 是歷史最悠久、最廣泛使用的 DNS 伺服器軟體。它功能強大、穩定性高，幾乎所有類 UNIX 系統都支援。由於其複雜性和安全性歷史問題，通常被認為是需要專業知識才能管理的「工業級」軟體。

2. PowerDNS

   特色： 一個高效能、模組化的 DNS 伺服器。它的設計允許使用各種後端來儲存 DNS 記錄，例如資料庫（MySQL, PostgreSQL）而不是傳統的文字檔，這使得它特別適合大規模、動態的 DNS 應用場景。

3. Unbound

   特色： 專為遞迴查詢而設計的現代化解析器。它的主要優勢是效能快、安全且記憶體使用率低。Unbound 專注於提供安全的遞迴服務，不具備授權功能，因此常與其他授權伺服器搭配使用。

4. dnsmasq

   特色： 一個輕量級的 DHCP 和 DNS 服務組合。它的設計目標是簡單易用，特別適合家庭網路、小型辦公室或嵌入式設備。它通常用作本地網路的 DNS 轉發器和快取伺服器。

5. CoreDNS

   特色： 以 Go 語言編寫，具有極高的模組化和擴充性。CoreDNS 在雲端原生環境（特別是 Kubernetes）中變得非常流行，因為它的外掛程式架構可以與其他服務無縫整合。

---

## port

- dns: 53/udp, 53/tcp

---

## server

### server - package

```bash
dns:~ # zypper in bind
dns:~ # zypper in yast2-dns-server
```

### server - config

- method 1 - by yast

```bash
dns:~ # yast dns-server
```

- method 2 - by manual

```bash
# config
dns:~ # vi /etc/named.conf
dns:~ # ls /etc/named.d/

dns:~ # named-checkconf /etc/named.conf
dns:~ # named-checkzone example.com /var/lib/named/master/example.com
dns:~ # named-checkzone 0.168.192.in-addr.arpa /var/lib/named/master
```

```conf
; /etc/named.conf
options {
        stale-answer-enable no;
        directory "/var/lib/named";
        managed-keys-directory "/var/lib/named/dyn/";
        dump-file "/var/log/named/dump.db";
        statistics-file "/var/log/named/stats";
        listen-on { any; };
        listen-on-v6 { none; };
        notify no;
    disable-empty-zone "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.IP6.ARPA";
    geoip-directory none;
};

zone "." in {
   type hint;
   file "root.hint";
};

zone "localhost" in {
   type master;
   file "localhost.zone";
};

zone "0.0.127.in-addr.arpa" in {
   type master;
   file "127.0.0.zone";
};

zone "0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa" IN {
   type master;
   file "127.0.0.zone";
};

zone "example.com" in {
   file "master/example.com";
   type master;
};

zone "0.168.192.in-addr.arpa" in {
        allow-transfer { any; };
        file "master/0.168.192.in-addr.arpa";
        type master;
};
```

```conf
; /var/lib/named/master/example.com
$TTL 2D
@               IN SOA          s1.     root.s1. (
                                2025081900      ; serial
                                3H              ; refresh
                                1H              ; retry
                                1W              ; expiry
                                1D )            ; minimum

example.com.    IN NS           s1.
pc1     IN      A               192.168.0.11 ;
```

```conf
; /var/lib/named/master/0.168.192.in-addr.arpa
$TTL 2d
@               IN SOA          s1.     root.s1. (
                                2025081900      ; serial
                                3h              ; refresh
                                1h              ; retry
                                1w              ; expiry
                                1d )            ; minimum
@       IN NS                   s1.0.158.192.in-addr.arpa.
11      IN PTR                  pc1.example.com.
```

### server - firewall

```bash
dns:~ # systemctl start named
dns:~ # systemctl enable named
```

### server - firewall

```bash
dns:~ # firewall-cmd --permanent --add-service=dns
dns:~ # firewall-cmd --reload
```

### server - test

```bash
dns:~ # dig @<dns> pc1.example.com
dns:~ # dig @<dns> -x 192.168.0.11
```
