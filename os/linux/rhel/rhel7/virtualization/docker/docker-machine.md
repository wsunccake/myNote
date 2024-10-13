# Dokcer Machine

因為 Linux 本身就支援 LXC, 所以 Dokcer 有支援. 而 Windows 和 Mac OS X 並沒支援, 要使用 Docker 需要透過 VM. 在此會先安裝 VirtualBox, 然後安裝 Linux VM (這步驟在安裝後第一次啟動會自動執行). 之後的 Container 皆是透過該 Linux VM 啟動.


## Command

Linux VM 的設定, 可以透過 docker-machine 操作

```bash
osx:~ $ docker-machine help
osx:~ $ docker-machine ls
osx:~ $ docker-machine env

osx:~ $ docker-machine start <docker_machine>
osx:~ $ docker-machine stop <docker_machine>
osx:~ $ docker-machine status <docker_machine>

osx:~ $ docker-machine ip <docker_machine>
osx:~ $ docker-machine ssh <docker_machine>
osx:~ $ docker-machine inspect <docker_machine>

osx:~ $ docker-machine kill <docker_machine>
osx:~ $ docker-machine rm <docker_machine>
```

