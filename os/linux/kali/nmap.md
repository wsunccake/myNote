# [nmap](https://nmap.org/)

host discovery -> port scanning -> version detection -> os detection

## ip

```bash
# single ip
kali:~ # nmap 192.168.0.10

# multi ip
kali:~ # nmap 192.168.0.10 192.168.0.20

# ip range
kali:~ # nmap 192.168.0.10-20

# ip mask
kali:~ # nmap 192.168.0.0/24
```

---

## port

```bash
# single port
kali:~ # nmap -p 22 <ip>
kali:~ # nmap -p T:22 <ip>      # only tcp port

# multi port
kali:~ # nmap -p 21,23 192.168.0.1

# port range
kali:~ # nmap -p 20-23 192.168.0.1

# all port 1 ~ 65535
kali:~ # nmap -p- 192.168.0.1
```

---

## host discovery

```bash
# arp
kali:~ # nmap -sn <ip>      # ping scan

# icmp
kali:~ # nmap -PE <ip>      # ICMP echo
kali:~ # nmap -PP <ip>      # ICMP timestamp
kali:~ # nmap -PM <ip>      # ICMP netmask

# tcp / udp
kali:~ # nmap -PS <ip>      # TCP SYN ping
kali:~ # nmap -PA <ip>      # TCP ACK ping
kali:~ # nmap -PU <ip>      # UDP ping

kali:~ # nmap -Pn <ip>      # skip ping, assume target
```

---

## port scanning

```bash
# tcp
kali:~ # nmap -sT <ip>       # TCP connect scan
kali:~ # nmap -sS <ip>       # TCP SYN scan
kali:~ # nmap -sA <ip>       # TCP ACK scan
kali:~ # nmap -sN <ip>       # TCP NULL scan
kali:~ # nmap -sF <ip>       # TCP FIN scan
kali:~ # nmap -sX <ip>       # TCP Xmas (FIN, PSH, and URG) scan
kali:~ # nmap -sW <ip>       # TCP Window scan
kali:~ # nmap -sM <ip>       # TCP Maimon scan

# udp
kali:~ # nmap -sU <ip>       # UDP scan
```

| 參數 | 說明                | 特點                                                    |
| ---- | ------------------- | ------------------------------------------------------- |
| -sS  | TCP SYN 掃描 (預設) | 半開放掃描，速度快且相對隱蔽，不完成三次握手。          |
| -sT  | TCP 連線掃描        | 完成三次握手，易被日誌紀錄，但不需要 root 權限。        |
| -sU  | UDP 掃描            | 針對 DNS、DHCP、SNMP 等 UDP 服務，速度較慢。            |
| -sV  | 版本偵測            | 探測埠口上運行的軟體名稱與版本號。                      |
| -O   | 作業系統偵測        | 透過 TCP/IP 指紋辨識目標運行的 OS (Windows/Linux/iOS)。 |
| -A   | 進階綜合掃描        | 同時開啟 OS 偵測、版本偵測、腳本掃描與路徑追蹤。        |

---

## version detection

```bash
kali:~ # nmap -sV <ip>       # app/service version
```

---

## os detection

```bash
kali:~ # nmap -O <ip>        # app/service version
```

---

## nse - nmap script engine

```bash
kali:~ # ls /usr/share/nmap/scripts
kali:~ # grep categories /usr/share/nmap/scripts/*

kali:~ # nmap --script-help default
kali:~ # nmap --script-help ssh-run
kali:~ # nmap -sV -sC <ip>                                  # -sC = --script="default"

# script-file
kali:~ # nmap --script="http-title" <ip>                    # single
kali:~ # nmap --script="ssh-run,http-title"                 # multi

# script-category
kali:~ # nmap --script="default" <ip>                       # single
kali:~ # nmap --script="default,safe,brute,exploit" <ip>    # multi

# other
kali:~ # namp -Pn -p 80 --script="http-*" <ip>
kali:~ # namp -Pn -p 445 --script="smb-*" <ip>
kali:~ # namp --script="not intrusive" <ip>
kali:~ # namp --script="default or safe" <ip>
kali:~ # namp --script="default and safe" <ip>
```

| 類別 (Category) | 說明                                                          |
| --------------- | ------------------------------------------------------------- |
| default         | 即 -sC，預設執行，安全且實用。                                |
| auth            | 測試身份驗證，檢查是否有弱登入資訊或略過認證。                |
| vuln            | 最受歡迎！ 專門檢測目標是否有已知的 CVE 漏洞（如 MS17-010）。 |
| discovery       | 主動探測網域資訊、公開目錄、SNMP 資訊等。                     |
| brute           | "對各類協議（SSH, MySQL, Telnet）進行暴力破解。"              |
| intrusive       | 侵入性腳本，可能會導致目標服務不穩定或留下明顯日誌。          |

---

## output

```bash
kali:~ # namp -oN <file>        # normal
kali:~ # namp -oX <file>        # xml
kali:~ # namp -oS <file>        # script kiddle
kali:~ # namp -oG <file>        # grepable
kali:~ # namp -oA <file>        # all
```

---

## zenmap
