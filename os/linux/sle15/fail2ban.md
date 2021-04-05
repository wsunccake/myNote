# fail2ban

## install

```bash
sle:~ # zypper addrepo https://download.opensuse.org/repositories/network:utilities/SLE_15_SP2/network:utilities.repo
sle:~ # zypper refresh
sle:~ # zypper install python-pyinotify

sle:~ # zypper addrepo https://download.opensuse.org/repositories/security/SLE_15_SP2/security.repo
sle:~ # zypper refresh
sle:~ # zypper install fail2ban

sle:~ # systemctl enable fail2ban --now
```

---

## configuration

```bash
sle:~ # ls /etc/fail2ban
fail2ban.conf # global variable
jail.conf     # default jail rule
jail.local    # custom jail rule
paths-common.conf
paths-opensuse.conf
filter.d # 過濾符合條件的設定檔目錄
action.d # 指定執行方式的設定檔目錄

# default jail rule
sle:~ # vi /etc/fail2ban/jail.conf
[INCLUDES]
before = paths-opensuse.conf

[DEFAULT]                                 # global setting
bantime  = 10m
findtime  = 10m
maxretry = 3
...

filter = %(__name__)s[mode=%(mode)s]       # default filter

action_ = %(banaction)s[port="%(port)s", protocol="%(protocol)s", chain="%(chain)s"]
...
action = %(action_)s                       # default action
...

[sshd]
port    = ssh
logpath = %(sshd_log)s
backend = %(sshd_backend)s
...

# custom jail rule
sle:~ # vi /etc/fail2ban/jail.local
[DEFAULT]
ignoreip = 127.0.0.1/8 ::1
bantime  = 10m
findtime  = 10m
maxretry = 2

[sshd]
enabled = true
ignoreip = 192.168.1.0/24

sle:~ # grep -Ev '^$|^#' jail.conf         # show config
sle:~ # grep '^\[.*\]' jail.conf           # list all jail
```


---

## command

```bash
# fail2ban-server
sle:~ # fail2ban-server -b    # start server in background
sle:~ # fail2ban-server -f    # start server in background
sle:~ # fail2ban-server -v    # increase verbosity
sle:~ # fail2ban-server -d    # for debug
sle:~ # fail2ban-server --dp  # for debug

# fail2ban-client
sle:~ # fail2ban-client status
sle:~ # fail2ban-client status <jail>

sle:~ # fail2ban-client add <jail>
sle:~ # fail2ban-client create <jail>
sle:~ # fail2ban-client stop <jail>

# fail2ban-regex
sle:~ # fail2ban-regex /var/log/messages /etc/fail2ban/filter.d/sshd.conf  -v                                                   # Success: all regex match
sle:~ # fail2ban-regex systemd-journal   /etc/fail2ban/filter.d/sshd.conf  -v                                                   # Success: all regex match
sle:~ # fail2ban-regex /var/log/messages 'maximum authentication attempts exceeded for <F-USER>.*</F-USER> from <HOST>.*$' -v   # Success: the regex match
```
