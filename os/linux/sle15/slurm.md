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

slurmdbd: 6819/tcp

```bash
# firewall config
linux:~ # firewall-cmd --add-port=6819/tcp --add-port=6818/tcp --add-port=6817/tcp --permanent
linux:~ # firewall-cmd --reload
```

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

setup [ntp](./ntp.md)

setup [nis](./nis.md)

setup nfs or [chrony](./chrony.md)

setup [munge](./munge.md)


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

ReturnToService=2
# 0: down -> idle*
# 1: down -> down
# 2: down -> idle

PrivateData=jobs                        # hidden regular users
SrunPortRange=60001-63000               # listening ports to communicate
LaunchParameters=use_interactive_step   # interactive mode

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


---

## Job

### list

`squeue`

```bash
controller:~ # squeue
controller:~ # squeue -la
controller:~ # squeue -j <job_id>
controller:~ # squeue -u <user>

# format
controller:~ # squeue -o "%.18i %.9P %.8j %.8u %.2t %.10M %.6D %R"        # default
controller:~ # squeue -o "%.18i %.9P %.8j %.8u %.8T %.10M %.9l %.6D %R"   # long, -l
controller:~ # squeue -o "%.15i %.8j %.9P %.8u %.9M %N"                   # step, -s
controller:~ # squeue -o "%8i %8u %15a %.10r %.10L %.5D %.10Q"
controller:~ # squeue -O jobid:8,name:8,username:8,account:15,partition:12,timeused:15,qos:8,prioritylong:.10
```


`smap`

```bash
controller:~ # smap
```


### submit

`srun`

```bash
controller:~ # srun -N 2 hostname
controller:~ # srun -w <node> hostname
controller:~ # srun env
controller:~ # srun -N 1 –pty bash -i  # interactive mode
controller:~ # srun -l -N1 -c2 sh -c "hostname && sleep 10" &
```


`salloc`

```bash
controller:~ # salloc
> srun <cmd>
> exit
```


`sbatch`

```bash
controller:~ # cat <job>.sh
#!/bin/sh
#SBATCH -J <job>               ## job Name
#SBATCH -o %j.out              ## stdout
#SBATCH -e %j.err              ## stderr
#SBATCH -p <parition>          ## partition
#SBATCH -t 24:00:00            ## time for 1 day
#SBATCH -N 1                   ## node
#SBATCH --ntasks-per-node=4    ## task/node

echo $SLURM_NODEID
sleep 5

# intel mpi
mpiexec.hydra -hosts-group $SLURM_JOB_NODELIST -n $SLURM_NTASKS -ppn $SLURM_NTASKS_PER_NODE <mpi_cmd>

controller:~ # sbatch <job>.sh
```


### cancal

`scancal`

```bash
controller:~ # scancel <job_id>
```

### other

`sstat`

```bash
controller:~ # sstat -e
controller:~ # sstat <job_id>
controller:~ # sstat -o JobID,Nodelist,Ntasks <job_id>
```

`scontrol`

```bash
controller:~ # scontrol show job
controller:~ # scontrol show job <job_id>
controller:~ # scontrol suspend <job_id>
controller:~ # scontrol resume <job_id>
controller:~ # scontrol hold <job_id>
controller:~ # scontrol release <job_id>
```


---

## Admin

### partition

`sinfo`

```bash
controller:~ # sinfo
controller:~ # sinfo -la
controller:~ # sinfo -Nla
```


### config

`scontrol`

```bash
controller:~ # scontrol show <ENTITY> [<ID>]  # ENTITY: config, node, partition, job

controller:~ # scontrol show config
controller:~ # scontrol show node [<node>]
controller:~ # scontrol update NodeName=<node> State=idle

controller:~ # vi /etc/slurm/slurm.conf
controller:~ # scontrol reconfigure
```


---

## MariaDB

`package`

```bash
controller:~ # zypper in mariadb

# setup mariadb root
controller:~ # /usr/bin/mysqladmin -u root password <new-password>
controller:~ # /usr/bin/mysqladmin -u root -h <hostname> password <new-password>
controller:~ # /usr/bin/mysql_secure_installation
```


`config`

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

`check`

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
MariaDB> create user 'slurm'@'localhost' identified by '<password>';
MariaDB> create user 'slurm'@'controller' identified by '<password>';
MariaDB> select Host, User, Password from mysql.user;
MariaDB> drop user 'slurm'@'localhost';
MariaDB> drop user 'slurm'@'controller';

-- change password
MariaDB> set PASSWORD FOR 'slurm'@'localhost' = PASSWORD('<password>');
MariaDB> set PASSWORD FOR 'slurm'@'controller' = PASSWORD('<password>');


-- setup grant privilege
MariaDB> grant all on slurm_acct_db.* TO 'slurm'@'localhost';
MariaDB> grant all on slurm_acct_db.* TO 'slurm'@'controller';
MariaDB> show grants for slurm@localhost;
```

`test`

```bash
controller:~ # mysql -u slurm
MariaDB> use slurm_acct_db;
```


---

## SlurmDB Daemon

```
         +-------------------+
         controller     compute node
         192.168.0.1    192.168.0.101
service: munge          munge
         ypserv         ypbind
         slurmctld      slurmd
         mariadb
         slurmddb
```

`package`

```bash
controller:~ # zypper in slurm-slurmdbd
```


`slurm config`

```bash
controller:~ # vi /etc/slurm/slurm.conf
AccountingStorageHost=controller
AccountingStorageUser=slurm
AccountingStoragePass=/var/run/munge/munge.socket.2
AccountingStoragePort=6819
AccountingStorageType=accounting_storage/slurmdbd

JobAcctGatherType=jobacct_gather/cgroup

JobCompType=jobcomp/none
```

AccountingStorageType: accounting_storage/none, accounting_storage/filetxt, accounting_storage/slurmdbd

JobAcctGatherType: jobacct_gather/none, jobacct_gather/linux, jobacct_gather/cgroup

JobCompType: jobcomp/none, jobcomp/elasticsearch, jobcomp/filetxt, jobcomp/mysql, jobcomp/script

`slurmdbd config`

```bash
controller:~ # vi /etc/slurm/slurmdbd.conf
StorageType=accounting_storage/mysql

StorageUser=slurm
StoragePass=<password>
StorageLoc=slurm_acct_db

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

```bash
controller: # sacct
```


---

## Accouting

`sacct`

```bash
controller:~ # sacct
```


`sacctmgr`

```bash
controller:~ # sacctmgr show configuration

controller:~ # sacctmgr list <ENTITY> [<SPECS>]
# <ENTITY>: account, association, cluster, configuration, coordinator,
#           event, federation, job, problem, qos, resource, reservation,
#           runawayjobs, stats,transaction, tres, user, wckey

# cluster
controller:~ # sacctmgr list cluster
controller:~ # sacctmgr add cluster <cluster>       # map db table
controller:~ # sacctmgr delete cluster <cluster>

# account
controller:~ # sacctmgr list account
controller:~ # sacctmgr add account <account> [Clusters=<cluster>] [Description="none"] [Organization="none"]
controller:~ # sacctmgr remove account <account> 

# user
controller:~ # sacctmgr list user
controller:~ # sacctmgr add user <user> [Account=<account>]
controller:~ # sacctmgr remove user <user> [where Account=<account>]
controller:~ # sacctmgr modify user set default=none where Account=<account>
```

[Accounting and Resource Limits](https://slurm.schedmd.com/accounting.html)


---

## QoS

`scontrol`

```bash
controller:~ # scontrol show config
controller:~ # scontrol show config | grep SchedulerType
controller:~ # scontrol show config | grep PriorityType
controller:~ # scontrol show config | grep AccountingStorageEnforce
controller:~ # scontrol show config | grep PriorityWeightQOS

```

SchedulerType: sched/wiki -> maui, sched/wiki2 -> moab, sched/builtin or sched/backfill -> slurm

PriorityType: priority/basic, priority/multifactor

AccountingStorageEnforce: limits

PriorityWeightQOS: != 0


`sacctmgr`

```bash
controller:~ # sacctmgr list qos [format=Name,Priority,GrpCPUs]
controller:~ # sacctmgr add qos <qos> [Priority=1000]
controller:~ # sacctmgr del qos <qos>
controller:~ # sacctmgr mod qos <qos> set GrpCPUs=-1 Flags=OverPartQOS # -1 is default, unlimited
controller:~ # sacctmgr mod qos <qos> set GrpJobs=<n>   # job number
controller:~ # sacctmgr mod qos <qos> set Priority=<n>  # job priority

# associate qos
controller:~ # sacctmgr mod account <account> set qos=<qos>
controller:~ # sacctmgr mod user <user> set qos=<qos>

controller:~ # sacctmgr list associations
```


`sprio`

```bash
controller:~ # sprio
controller:~ # sprio -l
```


### example

```bash
# for qos
controller:~ # sacctmgr list configuration
controller:~ # sacctmgr list cluster
controller:~ # sacctmgr list qos format=name,priority,grpjobs
controller:~ # sacctmgr list account
controller:~ # sacctmgr list user
controller:~ # sacctmgr list association format=qos,account,user
controller:~ # sacctmgr list stats

controller:~ # sacctmgr add qos high_qos   priority=1000
controller:~ # sacctmgr add qos medium_qos priority=100
controller:~ # sacctmgr add qos low_qos    priority=10

controller:~ # sacctmgr add account high_acc   cluster=mycluster qos=high_qos
controller:~ # sacctmgr add account medium_acc cluster=mycluster qos=medium_qos
controller:~ # sacctmgr add account low_acc    cluster=mycluster qos=low_qos

controller:~ # sacctmgr add user name=high_user   account=high_acc   cluster=mycluster
controller:~ # sacctmgr add user name=medium_user account=medium_acc cluster=mycluster
controller:~ # sacctmgr add user name=low_user    account=low_acc    cluster=mycluster

# for job
controller:~ # squeue
controller:~ # squeue -l

controller:~ # sinfo
controller:~ # sinfo -al
controller:~ # sinfo -Nal

controller:~ # sprio
controller:~ # sprio -nl
controller:~ # sprio -nl

controller:~ # sshare
controller:~ # sshare -al

controller:~ # sstat -j <job_id>
```

---

## HA

```bash
controller:~ # vi /etc/slurm/slurm.conf
# cluster
ClusterName=<cluster>

# controller
#ControlMachine=<server>
SlurmctldHost=<server>
SlurmctldHost=<ha_server>
```


---

## Question

1. change cluster name

```bash
controller:~ # rm /var/lib/slurm/clustername
```


2. munge didn't start when boot

```bash
node:~ # systemctld status systemd-tmpfile-setup
node:~ # systemctl status systemd-tmpfiles-clean
node:~ # cat /usr/lib/tmpfiles.d/munge.conf
node:~ # systemctld start systemd-tmpfile-setup

node:~ # systemctld stop ypbind
node:~ # zypepr in -f munge
node:~ # reboot
```


3. slurm didn't start when boot

```bash
node:~ # systemctld status systemd-tmpfile-setup
node:~ # systemctl status systemd-tmpfiles-clean
node:~ # cat /usr/lib/tmpfiles.d/slurm.conf
node:~ # systemctld start systemd-tmpfile-setup

node:~ # systemctld stop ypbind
node:~ # zypper in -f slurm-config
node:~ # reboot
```


4. job priority

```
Job_priority =
	site_factor +
	(PriorityWeightAge) * (age_factor) +
	(PriorityWeightAssoc) * (assoc_factor) +
	(PriorityWeightFairshare) * (fair-share_factor) +
	(PriorityWeightJobSize) * (job_size_factor) +
	(PriorityWeightPartition) * (partition_factor) +
	(PriorityWeightQOS) * (QOS_factor) +
	SUM(TRES_weight_cpu * TRES_factor_cpu,
	    TRES_weight_<type> * TRES_factor_<type>,
	    ...)
	- nice_factor
```
