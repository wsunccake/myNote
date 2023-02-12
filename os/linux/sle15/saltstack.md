# SaltStack

```
master ---  minion1
            minion2
            ...
```

master port: 4505 (publish_port), 4506(ret_port)

---

## master

### install

```bash
# package
master:~ # zypper install salt-master

# service
master:~ # systemctl enable salt-master
master:~ # systemctl start salt-master

# port
master:~ # ss -lutnp | grep 4505
master:~ # ss -lutnp | grep 4506

# firewall
master:~ # firewall-cmd --add-port=4505/tcp --add-port=4506/tcp --permanent
master:~ # firewall-cmd --reload
```

### config

```bash
master:~ # vi /etc/salt/master
interface: 0.0.0.0


master:~ # systemctl restart salt-master
```

### admin

```bash
# list key
master:~ # salt-key -h
master:~ # salt-key -L

# accept minion
master:~ # salt-key -a <minion>
master:~ # salt-key -A

# delet minion
master:~ # salt-key -d <minion>
master:~ # salt-key -D

# test
master:~ # salt [options] '<target>' <function> [arguments]
master:~ # salt '*' test.ping
master:~ # salt '*' cmd.run 'date'

# other
master:~ # salt-run manage.status
```

[EXECUTION MODULES](https://docs.saltstack.com/en/latest/ref/modules/all/index.html)

---

## minion

### install

```bash
minion:~ # zypper install salt-minion
minion:~ # systemctl enable salt-minion
minion:~ # systemctl start salt-minion
```

### config

```bash
minion:~ # vi /etc/salt/minion
master: <master>


minion:~ # systemctl restart salt-minion
```

---

## salt state

```bash
# config
master:~ # vi /etc/salt/master
file_roots:
  base:
    - /srv/salt


# restart service
master:~ # systemctl restart salt-master


# top file
master:~ # vi /srv/salt/top.sls
base:
  '*':
    - base.vim


# state file
master:~ # mkdir /srv/salt/base
master:~ # vi /srv/salt/base/top.sls
vim:
  pkg.installed


# usage
master:~ # salt '*' state.highstate
master:~ # salt '*' state.sls base.vim [saltenv='base']
```

[HOW DO I USE SALT STATES?](https://docs.saltstack.com/en/latest/topics/tutorials/starting_states.html)

---

## grains

attribute on minion

### config minion

```bash
minion:~ # vi /etc/salt/minion.d/grains.conf
grains:
  roles:
    - compute
    - backend
  dc_location: datecenter1


minion:~ # systemctl restart salt-minion
```

### usage master

```bash
master:~ # salt '*' grains.ls
master:~ # salt '*' grains.items
master:~ # salt '*' grains.item os

master:~ # salt '*' grains.item roles
master:~ # salt '*' grains.item dc_localtion
```

[GRAINS](https://docs.saltstack.com/en/latest/topics/grains/)

---

## pillar

attribute on master

### config master

```bash
# config
master:~ # vi /etc/salt/master
...
pillar_roots:
  base:
    - /srv/pillar
...


master:~ # vi /srv/pillar/top.sls
base:
  '*'
    - package
    - service


master:~ # vi /srv/pillar/package.sls
http:
  package-name: nginx
  version: 1.14.0

ftp:
  package-name: vsftpd
  version: 3.0.3


master:~ # vi /srv/pillar/service.sls
http:
  port:
    - 80
    - 8080


master:~ # systemctl restart salt-master
master:~ # salt '*' saltutil.refresh_pillar
```

### usage master

```bash
master:~ # salt '*' sys.doc pillar
master:~ # salt '*' sys.list_functions pillar

master:~ # salt '*' pillar.ls
master:~ # salt '*' pillar.items
```

[STORING STATIC DATA IN THE PILLAR](https://docs.saltstack.com/en/latest/topics/pillar/)

---

## mine

```bash
master:~ # salt '*' mine.get '*' network.interfaces
```

---

## ref

[SALT IN 10 MINUTES](https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough.html)
