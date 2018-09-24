# MySQL


## Install

`method1`

```bash
linux:~ # yum install mariadb
```


`method2`

```bash
linux:~ # docker pull mysql
linux:~ # docker run -d [-p 3306:3306] [-p 33060:33060] [-v /data/db:/var/lib/mysql] [-v /data/cnf:/etc/mysql/conf.d] --name mysql -e MYSQL_ROOT_PASSWORD=<password> mysql

linux:~ # docker exec -it mysql mysql -u root -p
```


## run


```bash
linux:~ # cat run.sh
#!/bin/sh

HOST="node-1.domain.tld"

mysql -u root << EOF
USE nova;
SELECT id, created_at, updated_at, hypervisor_hostname FROM compute_nodes;
-- SELECT id, created_at, updated_at, host FROM services;
SELECT id, created_at, updated_at, host FROM services WHERE host = "$HOST";
EOF

linux:~ # ./run.sh
```
