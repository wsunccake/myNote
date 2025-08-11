# slurm

## introduction

佇列系統 (Queuing System) 在高效能運算 (HPC, High Performance Computing) 領域扮演著至關重要的角色, 負責管理和排程計算資源, 確保多個使用者提交的任務能夠有條不紊地執行.
從早期簡單的批次系統到現代功能豐富的資源管理器, 佇列系統的演進反映 HPC 需求的增長和技術的進步.

- IBM LoadLeveler
  時間: 可追溯至 1986 年
  說明: IBM 在 HPC 領域的作業排程器, LoadLeveler 的技術起源相當早. 根據其早期版本的文件版權資訊, 其開發可追溯至 1986 年. 主要在管理 IBM 大型機和叢集環境中的批次作業, 提供資源分配和作業排程功能.

- DQS (Distributed Queuing System)
  時間: 1990 年代初期 (具體年份較難精確考證, 但普遍認為是早期分散式佇列系統的代表)
  說明: 早期廣泛使用的分散式佇列系統之一, 為研究機構和大學提供了一種管理多個計算節點上任務的方式. 它實現了任務的分散式提交和執行, 為後來的更複雜系統奠定了基礎.

- PBS (Portable Batch System)
  時間: 1990 年代初期 (由 NASA Ames Research Center 開發)
  說明: PBS 是在 DQS 之後出現的一個里程碑式系統, 主要提供更強大的功能和更好的可移植性. 引入了作業腳本, 多個佇列和資源管理器等概念, 成為 HPC 領域的標準之一, 並衍生出多個版本, 如 OpenPBS 和 PBS Pro.

  - 作業腳本 (Job Scripts):允許使用者定義作業的資源需求（如 CPU 時間, 記憶體, 節點數量）和執行指令.
  - 佇列 (Queues):支援多個佇列, 每個佇列可以有不同的優先級和資源限制, 以滿足不同類型的作業需求.
  - 資源管理器 (Resource Manager):負責監控節點狀態和資源利用率, 以便更有效地調度作業.

- CODINE / GRD (Sun Grid Engine 的前身)
  時間: 1993 年 (由德國 Gridware 公司開發)
  說明: CODINE (Computing in Distributed Networked Environments) 和 GRD (Global Resource Director) 是 Sun Grid Engine 的核心技術來源. 它們在 1990 年代中期開始發展, 旨在提供網格計算環境下的資源管理和作業排程功能.

- OpenPBS
  時間: 1998 年
  說明: OpenPBS 是從 NASA 的 PBS 專案中衍生出來的開源版本. 它的發布使得 PBS 的技術能夠更廣泛地被社群使用和改進, 為後續的 TORQUE 等系統鋪平了道路.

- Sun Grid Engine (SGE)
  時間: 2000 年 (Sun Microsystems 收購 Gridware 後, 將 CODINE/GRD 重新命名並推廣)
  說明: 雖然其技術根源可追溯至 1993 年, 作為一個廣為人知的產品, Sun Grid Engine (SGE) 是在 Sun Microsystems 於 2000 年收購 Gridware 後才正式推出並開源 (2001 年). 它在當時的網格計算和叢集管理領域佔有重要地位.

- TORQUE (Terascale Open-source Resource and QUEue Manager)
  時間: 2000 年代初期 (從 OpenPBS 分支出來)
  說明: TORQUE 是從 OpenPBS 專案中分支出來的, 旨在提供一個更活躍維護和功能更豐富的開源解決方案. 它繼承了 PBS 的基本架構, 並在效能, 穩定性和可擴展性方面進行了改進.

- Slurm (Simple Linux Utility for Resource Management)
  時間: 2002-2003 年 (開始開發)
  說明: Slurm 是目前 HPC 領域最流行和廣泛使用的開源佇列系統之一. 它從零開始設計, 旨在提供高度可擴展, 容錯且功能豐富的資源管理和作業排程系統. Slurm 以其靈活的排程策略和強大的功能, 成為許多頂級超級電腦和 HPC 中心的標準配置.
  - 高度可擴展性:能夠管理從小型叢集到數十萬個核心的大型超級電腦.
  - 靈活的排程策略:支援多種排程演算法, 如優先級排程, 公平分享排程, 回填排程等, 以最大化資源利用率和滿足使用者需求.
  - 豐富的功能:提供精細的資源分配（如 CPU, 記憶體, GPU）, 作業依賴性, 陣列作業, 互動式作業等.
  - 模組化設計:易於擴展和整合第三方工具.
  - 強大的社群支援:擁有活躍的開發者社群和大量的使用者.

---

## status

```
         +-------------------+
         controller     compute node
         192.168.0.1    192.168.0.101
service: munge          munge
         ypserv         ypbind
         slurmctld      slurmd
```

---

## port

- slurmctld: 6817/tcp
- slurmd: 6818/tcp
- slurmdbd: 6819/tcp

```bash
# firewall
sle:~ # firewall-cmd --add-port=6819/tcp --add-port=6818/tcp --add-port=6817/tcp --permanent
sle:~ # firewall-cmd --reload
```

---

## prepare

setup /etc/hosts or dns

```bash
sle:~ # vi /etc/hosts
192.168.0.1      controller
192.168.0.101    node1
...

sle:~ # hostname -s controller
```

- setup [nis](./nis.md) and [nfs](./nfs.md)
- setup [ntp](./ntp.md) or [chrony](./chrony.md)
- setup [munge](./munge.md)

---

## controller

### package

```bash
controller:~ # zypper in slurm
```

### config

```bash
controller:~ # vi /etc/slurm/slurm.conf
# cluster
ClusterName=<cluster>

# controller
# ControlMachine=<server> # deprecated, => SlurmctldHost
SlurmctldHost=contoller(192.168.0.1)

SlurmUser=root    # slurmctld daemon executes as user
SlurmctldPort=6817
SlurmctldPidFile=/var/run/slurm/slurmctld.pid
SlurmctldLogFile=/var/log/slurm/slurmctld.log

SlurmdUser=root   # slurmd daemon executes as user
SlurmdPort=6818
SlurmdPidFile=/var/run/slurm/slurmd.pid
SlurmdLogFile=/var/log/slurm/slurmd.log

AuthType=auth/munge

ReturnToService=2
# 0: down -> idle*
# 1: down -> down
# 2: down -> idle

PrivateData=jobs                        # hidden regular users
SrunPortRange=60001-63000               # listening ports to communicate
LaunchParameters=use_interactive_step   # interactive mode

# node config
## cpu
NodeName=DEFAULT Sockets=2 CoresPerSocket=4 ThreadsPerCore=1
NodeName=node[1-10]
NodeName=node[11-20] Sockets=2 CoresPerSocket=4 ThreadsPerCore=2 Feature=HyperThread

## gpu
GresTypes=gpu,mps
NodeName=node[21-30] State=idle Gres=gpu:4,mps:400 Sockets=1 CoresPerSocket=8
NodeName=node[31-40] State=idle Gres=gpu:4 Sockets=1 CoresPerSocket=8

# partition config
PartitionName=DEFAULT State=UP
PartitionName=normal Nodes=node[0-10,25-30] Default=YES MaxTime=24:00:00 State=UP
PartitionName=vip Nodes=node[40-50] State=UP AllowAccounts=VIP
```

```
lscpu
Architecture:             x86_64
  CPU op-mode(s):         32-bit, 64-bit
  Address sizes:          45 bits physical, 48 bits virtual
  Byte Order:             Little Endian
CPU(s):                   2             <-- CPUs
  On-line CPU(s) list:    0,1
Vendor ID:                GenuineIntel
  Model name:             12th Gen Intel(R) Core(TM) i5-1245U
    CPU family:           6
    Model:                154
    Thread(s) per core:   1             <-- ThreadsPerCore
    Core(s) per socket:   1             <-- CoresPerSocket
    Socket(s):            2             <-- Sockets
```

- Socket(s):
  主機上有多少個物理 CPU 插槽。
  Slurm 配置中的 Sockets。
- Core(s) per socket:
  每個物理 CPU 插槽上有多少個物理核心。
  Slurm 配置中的 CoresPerSocket 數量。
- Thread(s) per core:
  Slurm 配置中的 ThreadsPerCore 數量。
  每個物理核心有多少個執行緒（Thread）。
  如果支援超執行緒（Hyper-threading），通常會大於 1（例如 2）；如果沒有，則為 1。
- CPU(s):
  所有邏輯 CPU 總數，等於 Sockets x CoresPerSocket x ThreadsPerCore。

[Slurm Version 17.11 Configuration Tool](https://slurm.schedmd.com/configurator.html)

### daemon

```bash
controller:~ # vi /usr/lib/systemd/system/slurmctld.service
[Service]
#PIDFile=/var/run/slurm/slurmctld.pid   # comment, SlurmctldPidFile in /etc/slurm/slurm.conf
#User=slurm                             # comment, SlurmUser in /etc/slurm/slurm.conf

controller:~ # systemctl daemon-reload
controller:~ # systemctl enable slurmctld.service --now
```

### check

```bash
controller:~ # slurmd -C
```

### tmpfile

```bash
controller:~ # cat /etc/tmpfiles.d/slurm.conf
d /var/run/slurm 0755 root root -
d /var/log/slurm 0755 root root -

controller:~ # systemd-tmpfiles --create
```

---

## compute node

### package

```bash
node:~ # zypper in slurm-node
```

### config

```bash
controller:~ # scp /etc/slurm/slurm.conf root@<client>:/etc/slurm/.
```

### daemon

```bash
node:~ # vi /usr/lib/systemd/system/slurmd.service
[Service]
#PIDFile=/var/run/slurm/slurmd.pid   # comment, SlurmdPidFile in /etc/slurm/slurm.conf
#User=slurm                          # comment, SlurmdUser in /etc/slurm/slurm.conf

node:~ # systemctl daemon-reload
node:~ # systemctl enable slurmd.service --now
```

### check

```bash
node:~ # slurmd -C
```

### tmpfile

```bash
node:~ # cat /etc/tmpfiles.d/slurm.conf
d /var/run/slurm 0755 root root -
d /var/log/slurm 0755 root root -

node:~ # systemd-tmpfiles --create
```

---

## job

### list

#### squeue

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

#### smap

```bash
controller:~ # smap
```

### submit

#### srun

```bash
controller:~ # srun -N 2 hostname
controller:~ # srun -w <node> hostname
controller:~ # srun env
controller:~ # srun -N 1 –pty bash -i  # interactive mode
controller:~ # srun -l -N1 -c2 sh -c "hostname && sleep 10" &
```

#### salloc

```bash
controller:~ # salloc
> srun <cmd>
> exit
```

#### sbatch

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

#### scancal

```bash
controller:~ # scancel <job_id>
```

### other

#### sstat

```bash
controller:~ # sstat -e
controller:~ # sstat <job_id>
controller:~ # sstat -o JobID,Nodelist,Ntasks <job_id>
```

#### scontrol

```bash
controller:~ # scontrol show job
controller:~ # scontrol show job <job_id>
controller:~ # scontrol suspend <job_id>
controller:~ # scontrol resume <job_id>
controller:~ # scontrol hold <job_id>
controller:~ # scontrol release <job_id>
```

```
scontrol show job(s): Admin, Operator, Coordinator
scontrol update job: Admin, Operator, Coordinator
scontrol requeue: Admin, Operator, Coordinator
scontrol show step(s): Admin, Operator, Coordinator
scontrol update step: Admin, Operator, Coordinator
scontrol show node: Admin, Operator
scontrol update node: Admin
scontrol show node: Admin, Operator
scontrol update node: Admin
scontrol create partition: Admin
scontrol show partition: Admin, Operator
scontrol update partition: Admin
scontrol delete partition: Admin
scontrol create reservation: Admin, Operator
scontrol show reservation: Admin, Operator
scontrol update reservation: Admin, Operator
scontrol delete reservation: Admin, Operator
scontrol reconfig: Admin
scontrol shutdown: Admin
scontrol takeover: Admin
```

---

## admin

### partition

#### sinfo

```bash
controller:~ # sinfo
controller:~ # sinfo -la
controller:~ # sinfo -Nla
```

### config

#### scontrol

```bash
controller:~ # scontrol show <ENTITY> [<ID>]  # ENTITY: config, node, partition, job

controller:~ # scontrol show config
controller:~ # scontrol show node [<node>]
controller:~ # scontrol update NodeName=<node> State=idle

controller:~ # vi /etc/slurm/slurm.conf
controller:~ # scontrol reconfigure
```

---

## mariadb

### package

```bash
controller:~ # zypper in mariadb
```

### config

```bash
controller:~ # vi /etc/my.cnf
# increase pool size
innodb_buffer_pool_size = 128M
```

### daemon

```bash
controller:~ # systemctl start mariadb.service
controller:~ # systemctl enable mariadb.service

# setup mariadb root
controller:~ # mariadb-admin -u root password <new-password>
controller:~ # mariadb-admin -u root -h <hostname> password <new-password>
controller:~ # mariadb_secure_installation
```

mysqladmin 可用 mariadb-admin 替代, 而 mysql_secure_installation 則用 mariadb_secure_installation

### check

```bash
controller:~ # mariadb -u root
-- check pool size
MariaDB> show variables like 'innodb_buffer_pool_size';

-- check db engine
MariaDB> show engines;

MariaDB> quit;
```

mysql 可用 mariadb 替代

### db

```sql
-- create db
MariaDB> create database slurm_acct_db;
MariaDB> show databases;
MariaDB> drop database slurm_acct_db;
```

### user

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

-- show grant
MariaDB> show grants for slurm@localhost;
```

### test

```bash
controller:~ # mariadb -u slurm -p
MariaDB> use slurm_acct_db;
```

---

## slurmdb daemon

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

### package

```bash
controller:~ # zypper in slurm-slurmdbd
```

### slurm config

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

[slurm.conf](https://slurm.schedmd.com/slurm.conf.html)

### slurmdbd config

```bash
controller:~ # vi /etc/slurm/slurmdbd.conf
StorageType=accounting_storage/mysql

StorageUser=slurm
StoragePass=<password>      # 設定密碼
StorageLoc=slurm_acct_db
```

[slurmdbd.conf](https://slurm.schedmd.com/slurmdbd.conf.html)

### daemon

```bash
controller:~ # systemctl restart slurmctld.service

controller:~ # systemctl start slurmdbd.service
controller:~ # systemctl enable slurmdbd.service
```

### check db

```bash
controller:~ # mariadb -u root
MariaDB> show databases;
MariaDB> use slurm_acct_db;
MariaDB> show tables;
```

```bash
controller: # sacct
```

---

## accouting

### sacct

```bash
controller:~ # sacct
```

### sacctmgr

```bash
controller:~ # sacctmgr help
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

## qos

### scontrol

```bash
controller:~ # scontrol show config
controller:~ # scontrol show config | grep SchedulerType
controller:~ # scontrol show config | grep PriorityType
controller:~ # scontrol show config | grep AccountingStorageEnforce
controller:~ # scontrol show config | grep PriorityWeightQOS
```

SchedulerType: sched/wiki -> maui, sched/wiki2 -> moab, sched/builtin or sched/backfill -> slurm

PriorityType: priority/basic -> fifo, priority/multifactor -> job priority factor

AccountingStorageEnforce: limits

PriorityWeightQOS: =0 don't use the qos factor, != 0 use the qos factor

### sacctmgr

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

[Resource Limits](https://slurm.schedmd.com/resource_limits.html)

### sprio

```bash
controller:~ # sprio
controller:~ # sprio -l
```

### example

```bash
# for qos
controller:~ # sacctmgr list configuration
controller:~ # sacctmgr list cluster
controller:~ # sacctmgr list qos format=name,priority,usagefactor
controller:~ # sacctmgr list qos format=name,maxsubmitjobsperuser,maxjob
controller:~ # sacctmgr list qos format=name,grpsubmitjob,grpjob
controller:~ # sacctmgr list account
controller:~ # sacctmgr list user
controller:~ # sacctmgr list association format=qos,account,user
controller:~ # sacctmgr list stats

controller:~ # sacctmgr add qos high_qos   priority=1000 usagefactor=1.0
controller:~ # sacctmgr add qos medium_qos priority=100  usagefactor=0.8
controller:~ # sacctmgr add qos low_qos    priority=10   usagefactor=0.5

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
controller:~ # sinfo -N -o "%.20N %.15C %.10t %.10m %.15P %.15G %.35E"

controller:~ # sprio
controller:~ # sprio -nl
controller:~ # sprio -nl

controller:~ # sshare
controller:~ # sshare -al

controller:~ # sstat -j <job_id>

# config
controller:~ # scontrol show node
controller:~ # scontrol show partition
controller:~ # scontrol show job

# repot
controller:~ # sreport cluster UserUtilizationByAccount
controller:~ # sreport user TopUsage
```

---

## ha

```bash
controller:~ # vi /etc/slurm/slurm.conf
# cluster
ClusterName=<cluster>

# controller
SlurmctldHost=<server>
SlurmctldHost=<ha_server>

controller:~ # scontrol ping
```

---

## question

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
