# pdsh

## run

```bash
# install
sle:~ # zypper in pdsh

# config
sle:~ # ssh-keygen
sle:~ # ssh-copyid <host>

# setup RCMD
sle:~ # export PDSH_RCMD_TYPE=ssh

# run
sle:~ # pdsh -w <host>[,...] [-R ssh] <command>
# -R: exec, ssh, mrsh
```

---

## plugin

### pdsh-machines

```bash
sle:~ # zypper in pdsh-machines

sle:~ # mkdir -p /etc/pdsh
sle:~ # vi /etc/pdsh/machines
nfs1
nas1
xeon1
xeon2
xeon3

sle:~ # pdsh -a [-x <host>[,...]] <command>
```

### pdsh-genders

```bash
sle:~ # zypper in pdsh-genders

sle:~ # vi /etc/genders
nfs1,nas1  storages
xeon[1-10] xeon,nodes
xeon[11-20] amd,nodes
gpu[21-30] gpu,nodes

# use gender attr
sle:~ # pdsh -g <gender_attr>[,...] <command>
sle:~ # pdsh -a [-X <gender_attr>[,...]] <command>
```

ps: pdsh-machines & pdsh-genders conflict, 只能選一個

### pdsh-slurm

```bash
sle:~ # zypper in pdsh-slurm

sle:~ # vi /etc/slurm/slurm.conf

# use slurm partition
sle:~ # pdsh -p <slurm_partition> <command>
```
