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
