# bind

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
