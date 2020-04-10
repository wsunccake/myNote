# LXC


## Package

```
rhel:~ # yum install -y lxc lxc-templates lxc-extra
rhel:~ # repoquery --list lxc 
rhel:~ # repoquery --list lxc-template
rhel:~ # repoquery --list lxc-extra
```

## Template

```
rhel:~ # ls /usr/share/lxc/templates
```

#### create container from template

```
rhel:~ # /usr/share/lxc/templates/lxc-centos -h
rhel:~ # /usr/share/lxc/templates/lxc-centos
rhel:~ # /usr/share/lxc/templates/lxc-centos -n <lxc_name> -R <7> -p <lxc_path>

rhel:~ # lxc-create -n lxc_name -t centos

rhel:~ # ls /var/lib/lxc/<lxc_name>
```

## Usage

```
rhel:~ # lxc-ls
rhel:~ # lxc-info -n <lxc_name>
rhel:~ # lxc-start -d -n <lxc_name>
rhel:~ # lxc-stop -n <lxc_name>
rhel:~ # lxc-console -n <lxc_name>  (ctrl-a q)
rhel:~ # lxc-destroy -n 
```