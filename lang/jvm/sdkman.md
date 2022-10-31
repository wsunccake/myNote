# sdkman

## install

```bash
# require
linux:~ # apt install zip unzip curl sed        # for ubuntu / debian
linux:~ # yum install zip unzip curl sed        # for centos
linux:~ # dnf install zip unzip curl sed        # for centos / fedora

# setup install dir
linux:~ $ export SDKMAN_DIR=$HOME/.sdkman

# instaall
linux:~ $ curl -s "https://get.sdkman.io" | bash                    # install
linux:~ $ curl -s "https://get.sdkman.io?rcupdate=false" | bash     # install and not change rc / profile

linux:~ $ source "$HOME/.sdkman/bin/sdkman-init.sh"
linux:~ $ sdk version
```


---

## usage

```bash
# help
linux:~ $ sdk help
linux:~ $ sdk help install

# search pkg
linux:~ $ sdk list
linux:~ $ sdk list groovy

# current
linux:~ $ sdk current

# install pkg
linux:~ $ sdk install groovy
linux:~ $ sdk install groovy 4.0.5

# uninstall pkg
linux:~ $ sdk uninstall groovy 4.0.5

# set pkg version
linux:~ $ sdk default groovy 4.0.5
linux:~ $ sdk use groovy 4.0.5
```


---

## uninstall

```bash
linux:~ $ tar zcvf ~/sdkman-backup_$(date +%F-%kh%M).tar.gz -C ~/ .sdkman
linux:~ $ rm -rf ~/.sdkman

# remove setup in rc
linux:~ $ vi ~/.bashrc
...
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
```


---

## ref

[SDKMAN](https://sdkman.io/)
