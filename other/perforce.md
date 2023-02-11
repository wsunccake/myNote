# Perforce

![perforce](https://www.perforce.com/perforce/doc.current/manuals/p4v-gs/images/01_p4v-gs.2.1.1.jpg)

## Client Configure

```bash
rhel:~ # cat ~/.bashrc
...
export P4CONFIG=~/.p4config

rhel:~ # cat ~/.p4config
P4PORT=perforce:1666
P4USER=user
P4ROOT=/$HOME/Perforce/user_host
P4CLIENT=user_host
```

---

## Client Command

### syntax

```bash
rhel:~ # p4 [-u <user>] [-P <password>] [-p perforce:1666] <command>
```

### help

```bash
rhel:~ # p4 help simple
rhel:~ # p4 help commands
rhel:~ # p4 help <command>

rhel:~ # p4 info
```

### login / logout

```bash
rhel:~ # p4 login
rhel:~ # p4 logout
```

### workspace / client

```bash
rhel:~ # p4 clients                             # list work space
rhel:~ # p4 client [-o] <WS>                    # create work space
rhel:~ # p4 client -d <WS>                      # delete work space

rhel:~ # p4 client -i                           # change work space config
Client: <WS>
Root:  /var
View:  //depot/release  /var/release
按 Ctrl D 結束

rhel:~ # echo -e "Client: <WS>\nRoot:  /var\nView:  //depot/release  /var/release" | p4 client -i
```

```bash
rhel:~ # p4 client -o
Client:	my-workspace

Update:	2022/04/28 20:32:02

Access:	2022/04/28 20:32:31

Owner:	p4user

Host:	myMachine

Description:
	Created by p4user.

Root:	/var/lib/workspace/app/

Options:	noallwrite noclobber nocompress unlocked nomodtime rmdir

SubmitOptions:	submitunchanged

LineEnd:	local

View:
	//depot/tools/app/... //my-workspace/app/...
	-//depot/tools/app/unittest/... //my-workspace/tools/app/unittest/...
	//depot/tools/app/config/... //my-workspace/tools/app/config/...

./p4 client -o | sed 's"//depot/tools/app/config/... //my-workspace/tools/app/config/..."-//depot/tools/app/config/... //my-workspace/tools/app/config/..."' | ./p4 client -i
```

### change list

```bash
rhle:~ # p4 changes[-u user]                    # show change list
rhel:~ # p4 changes -s shelved                  # show shevled in change list
rhel:~ # p4 describe -s <CL>                    # show shevled file in change list

rhel:~ # p4 change [-o <CL>]                    # create change list
rhel:~ # p4 change -d <CL>                      # delte change list
```

### file/dir

```bash
rhel:~ # p4 files //depot/*                     # show file on server
rhel:~ # p4 have //depot/*                      # show file on client

rhel:~ # p4 dirs //depot/*                      # show dir
```

### sync code

```bash
rhel:~ # p4 sync //depot/release/...#head          # sync code
rhel:~ # p4 sync -f //depot/release/...#head       # force sync

rhel:~ # p4 edit [-c <CL>] //depot/file            # add/edit code
rhel:~ # p4 shelve -f -c <CL> //depot/file         # shevle code

# sync code from shevle
rhel:~ # p4 unshelve -s <old CL> [-c <new CL>] [//depot/file]

rhel:~ # p4 revet //depot/file                     # revert/rollback code
```
