# alpine

## apk

```bash
alpine:~ # cat /etc/apk/repositories

alpine:~ # apk update
alpine:~ # apk search <pkg>
alpine:~ # apk info [<pkg>]    # installed package
alpine:~ # apk list [<pkg>]    # available package
alpine:~ # apk stats

alpine:~ # apk add <pkg>       # install package
alpine:~ # apk del <pkg>       # uninstall package

# ie
alpine:~ # apk search mlocate
alpine:~ # apk add mlocate
alpine:~ # apk del mlocate
```


---

## openrc

```bash
# install openrc
alpine:~ # apk add openrc

# usage openrc
alpine:~ # rc-status [-a]
alpine:~ # rc-status -l        # list runlevel
alpine:~ # rc-service -l       # list service
alpine:~ # rc-service <service> start|stop|status|restart
alpine:~ # rc-update add|del <service> [<runlevel>]
alpine:~ # rc-update show [-v]

# ie
alpine:~ # apk add openssh-server
alpine:~ # rc-service --list
alpine:~ # rc-service sshd start
alpine:~ # rc-service sshd stop
alpine:~ # rc-service sshd status
alpine:~ # rc-update add sshd
alpine:~ # rc-update del sshd
alpine:~ # rc-status
```
