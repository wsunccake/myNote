# kali penetration testing

## passive reconnaissance

### google search / google hacking

site: oreilly filetype: pdf

inurl: oreilly.com intext: penetrantion


### SHODAN

country:tw city:taipei port:80 net:210.xxx.xxx.xxx/24

org:google isp:hinet hostname:noip version:4.2 geo:25,121 product:windows


### ZoomEye


### whois

web or cli

```bash
kali:~ # whois oreilly.com
kali:~ # whois 8.8.8.8
```


### theHarvester

```bash
kali:~ # theHarvester -d demo.testfire.net -b google -l 20
kali:~ # theHarvester -d testfire.net -b all -l 20
```


### recon-ng

```bash
kali:~ # recon-ng
[recon-ng][default] > marketplace refresh
[recon-ng][default] > marketplace search netblock
[recon-ng][default] > marketplace install recon/netblocks-hosts/reverse_resolve
```

[lanmaster53/recon-ng-marketplace](https://github.com/lanmaster53/recon-ng-marketplace/tree/master/modules/recon)


### maltego


### sn0int


### nslookup / dig


### dnsrecon


---

## active reconnaissance

### nmap
