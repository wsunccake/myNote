# SLURM

## Status

```
         +-------------------+
         controller     compute node
         192.168.0.1    192.168.0.101
service: munge          munge
         ypserv         ypbind
         slurmctld      slurmd
```


---

## Port

slurmctld: 6817/tcp

slurmd: 6818/tcp


---

## Preparation

disable selinux

setup ntp or [chrony](./chrony.md)

[setup nis](./nis.md)

setup nfs

[setup munge](./munge.md)

```bash
centos:~ # cat /etc/login.defs

# create system group
centos:~ # groupadd -r slurm

# create system user
centos:~ # useradd -r -g slurm -s /usr/sbin/nologin slurm

# create spool folder
centos:~ # mkdir -p /var/spool/slurm
centos:~ # chown slurm:slurm /var/spool/slurm

# update hosts
centos:~ # vi /etc/hosts
192.168.0.1    controller
192.168.0.101  compute1
...
```


---

## Install

```bash
centos:~ # yum install pam-devel readline-devel perl-ExtUtils-MakeMaker munge-libs munge-devel
centos:~ # wget https://download.schedmd.com/slurm/slurm-19.05.0.tar.bz2
centos:~ # rpmbuild -ta slurm-19.05.0.tar.bz2
```


---

## Controller / Server

```bash
# package
controller:~ # yum install slurm-19.05.0-1.el7.x86_64.rpm slurm-slurmctld-19.05.0-1.el7.x86_64.rpm

# config
controller:~ # vi /etc/slurm/slurm.conf

# service
controller:~ # systemctl start slurmctld
controller:~ # systemctl enable slurmctld
```


---

## Compute / Client

```bash
# package
compute:~ # yum install slurm-19.05.0-1.el7.x86_64.rpm slurm-slurmd-19.05.0-1.el7.x86_64.rpm

# config
compute:~ # scp controller:/etc/slurm/slurm.conf /etc/slurm/slurm.conf

# service
compute:~ # systemctl start slurmd
compute:~ # systemctl enable slurmd
```


---

## Usage

```bash
# list queue
controller:~ $ squeue

# run job
controller:~ $ srun -N1 sleep 60

# submit job
controller:~ $ cat test.sbatch
#!/bin/sh
#SBATCH -J test
#SBATCH -N 1
#SBATCH -o test.out
#SBATCH -e test.err

echo $SLURM_NODEID
sleep 60

controller:~ $ sbatch test.sbatch

# cancel job
controller:~ $ scancel <job_id>
```

---

## Admin

```bash
controller:~ # sinfo
controller:~ # sinfo -N
controller:~ # sinfo -s
controller:~ # sinfo -l

controller:~ # scontrol
controller:~ # scontrol update NodeName=node10 State=DOWN Reason="undraining"
controller:~ # scontrol update NodeName=node10 State=RESUME
controller:~ # scontrol show node node10
controller:~ # scontrol show job 10

# syntax
scontrol: update <specification>
scontrol: show <entity> [<id>]
```