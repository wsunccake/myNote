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

## Port

slurmctld: 6817/tcp

slurmd: 6818/tcp

---

## Preparation

setup /etc/hosts or dns

```bash
suse:~ # vi /etc/hosts
192.168.0.1      controller  
192.168.0.101    node1
...

suse:~ # hostname -s controller
```

setup ntp

[setup nis](./nis.md)

setup nfs

[setup munge](./munge.md)


---

## Controller

`package`

```bash
controller:~ # zypper in slurm
```

`config`

```bash
controller:~ # vi /etc/slurm/slurm.conf
# cluster
ClusterName=<cluster>

# controller
ControlMachine=<server>

# node config
NodeName=DEFAULT Sockets=2 CoresPerSocket=4 ThreadsPerCore=1
NodeName=node[1-10]
NodeName=node[20-30] Sockets=2 CoresPerSocket=4 ThreadsPerCore=2 Feature=HyperThread

# partition config
PartitionName=DEFAULT State=UP
PartitionName=normal Nodes=node[0-10,25-30] Default=YES MaxTime=24:00:00 State=UP
```

[Slurm Version 17.11 Configuration Tool](https://slurm.schedmd.com/configurator.html)


`daemon`

```bash
controller:~ # systemctl start slurmctld.service
controller:~ # systemctl enable slurmctld.service
```

`check`

```bash
controller:~ # slurmd -C
```


---

## Compute Node


```bash
node:~ # zypper in slurm-node
```

`config`


```bash
controller:~ # scp /etc/slurm/slurm.conf root@<client>:/etc/slurm/.
```

`daemon`

```bash
node:~ # systemctl start slurmd.service
node:~ # systemctl enable slurmd.service
```

`check`

```bash
node:~ # slurmd -C
```

## Usage

`queue`

```
controller:~ # squeue
controller:~ # squeue -l
controller:~ # squeue -a
controller:~ # squeue -s
controller:~ # squeue -j <job_id>
controller:~ # squeue -u <user>
```

`status`

```bash
controller:~ # sinfo
controller:~ # sinfo -l
controller:~ # sinfo -a

controller:~ # smap
```

`job`

```bash
# run job
controller:~ # srun -N1 hostname

# cancel job
controller:~ # scancel <job_id>
```

`config`

```bash
controller:~ # scontrol show nodes
controller:~ # scontrol show jobs
controller:~ # scontrol update nodename=node1 state=resume
controller:~ # scontrol show config
```


---

## Job

`script`

```bash
controller:~ # cat test.slurm
#!/bin/sh
#SBATCH -J test
#SBATCH -N 1
#SBATCH -o test.out
#SBATCH -e test.err

echo $SLURM_NODEID
sleep 5

controller:~ # sbatch test.slurm
```

`smp`

`mpi`


---

## QoS


`check`

```bash
controller:~ # scontrol show config | grep SchedulerType
controller:~ # scontrol show config | grep PriorityType
```

SchedulerType: sched/wiki -> maui, sched/wiki2 -> moab, sched/builtin or sched/backfill -> slurm

PriorityType: priority/basic, priority/multifactor

```bash
controller:~ # sprio
```


---

## Accouting

`package`

```bash
controller:~ # zypper in slurm-slurmdbd
controller:~ # zypper in mariadb
```

### DB

`db config`

```bash
controller:~ # vi /etc/my.cnf
# increase pool size
innodb_buffer_pool_size = 128M
```

`daemon`

```bash
controller:~ # systemctl start mariadb.service
controller:~ # systemctl enable mariadb.service
```

`check config`

```bash
controller:~ # mysql -u root
-- check pool size
MariaDB> show variables like 'innodb_buffer_pool_size';

-- check db engine
MariaDB> show engines;

MariaDB> quit;
```

`db`

```sql
-- create db
MariaDB> create database slurm_acct_db;
MariaDB> show databases;
MariaDB> drop database slurm_acct_db;
```

`user`

```sql
-- create user
MariaDB> create user 'slurm'@'localhost' identified by 'password';
MariaDB> create user 'slurm'@'controller' identified by 'password';
MariaDB> select Host, User, Password from mysql.user;
MariaDB> drop user 'slurm'@'localhost';
MariaDB> drop user 'slurm'@'controller';

-- setup grant privilege
MariaDB> grant all on slurm_acct_db.* TO 'slurm'@'localhost';
MariaDB> grant all on slurm_acct_db.* TO 'slurm'@'controller';
MariaDB> show grants for slurm@localhost;
```



### SlurmDB Daemon

`slurm config`

```bash
controller:~ # vi /etc/slurm/slurm.conf
AccountingStorageHost=controller
AccountingStorageUser=slurm
AccountingStoragePass=/var/run/munge/munge.socket.2
AccountingStoragePort=6819
AccountingStorageType=accounting_storage/slurmdbd

JobAcctGatherType=jobacct_gather/cgroup

JobCompType=jobcomp/mysql
```

AccountingStorageType: accounting_storage/none, accounting_storage/filetxt, accounting_storage/slurmdbd

JobAcctGatherType: jobacct_gather/none, jobacct_gather/linux, jobacct_gather/cgroup

JobCompType: jobcomp/none, jobcomp/elasticsearch, jobcomp/filetxt, jobcomp/mysql, jobcomp/script

`slurmdbd config`

```bash
controller:~ # vi /etc/slurm/slurmdbd.conf
StorageType=accounting_storage/mysql
```

`daemon`

```bash
controller:~ # systemctl restart slurmctld.service

controller:~ # systemctl start slurmdbd.service
controller:~ # systemctl enable slurmdbd.service
```

`check db`

```bash
controller:~ # mysql -u root
MariaDB> show databases;
MariaDB> use slurm_acct_db;
MariaDB> show tables;
```

`add data`

```bash
controller:~ # sacctmgr list cluster
controller:~ # sacctmgr add cluster <cluster>       # map db table
controller:~ # sacctmgr delete cluster <cluster>

controller:~ # sacctmgr list account
controller:~ # sacctmgr add account <account> cluster=<cluster> Description="none" Organization="none"

controller:~ # sacctmgr list user
controller:~ # sacctmgr add user <user> account=<account>
```

`usage`

```bash
controller:~ # sacct
```

[Accounting and Resource Limits](https://slurm.schedmd.com/accounting.html)


---

## Other

change cluster name

```bash
controller:~ # rm /var/lib/slurm/clustername
```
