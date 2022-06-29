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


### host


### nslookup


### dig


### dnsrecon


---

## active reconnaissance

### [nmap](https://nmap.org/)


### masscan


### [dirb](http://dirb.sourceforge.net/)

```bash
kail:~ # dirb http://<ip>/<context>
```


### whatweb

```bash
kail:~ # whatweb http://<ip>/<context>
```


### amap


### smbmap


### telnet


### nc


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


### lynis


---

## remote


### [metasploit framework](https://www.metasploit.com/)


### sfuzz


---

## ref

[Kali Docs](https://www.kali.org/docs/)

[Kali Tools](https://www.kali.org/tools/)

[Nmap Network Scanning](https://nmap.org/book/toc.html)

[METASPLOIT UNLEASHED](https://www.offensive-security.com/metasploit-unleashed/)

[大学霸 Kali Linux 安全渗透教程](https://wizardforcel.gitbooks.io/daxueba-kali-linux-tutorial/content/index.html)
