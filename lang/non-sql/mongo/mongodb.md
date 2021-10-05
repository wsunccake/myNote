# MongoDB

![mongodb](https://webassets.mongodb.com/_com_assets/global/mongodb-logo-white.png)


---

## Install

```bash
# install package
centos:~ # vi /etc/yum.repos.d/mongodb-org.repo
[mongodb-org]
baseurl = https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.2/x86_64/
gpgcheck = 1
gpgkey = https://www.mongodb.org/static/pgp/server-3.2.asc
name = mongodb-org

centos:~ # yum install mongodb-org

# start service
centos:~ # systemctl start mongodb
centos:~ # systemctl enable mongodb

# default port
centos:~ # netstat -lutnp | grep 27017

# run mongo client
centos:~ # monogo -version
centos:~ # monogo
```


---

## Backup & Restore

```bash
# backup
centos:~ # mongodump [-h <hostname>[:<port>]
centos:~ # ls dump                # create dump folder to dump data

# restore
centos:~ # mongorestore           # load dump folder to database
```

---

## Usage

```sql
// basic
> help                  // show help
> show dbs              // show database
> use <database>        // use database
> db                    // show current database
> show collections      // after useing database, show collection/table

> db.help()
> db.stats()

// query
> db.<collection>.findOne()
> db.<collection>.find().limit(1).pretty()
```

```bash
# For command
centos:~ # echo -e "use master\nshow collections" | docker exec -i mongo mongo

# For script
centos:~ # cat ex.sh
#!/bin/sh

docker exec -i mongo mongo << EOF
use <databases>
db
show collections
db.<collection>.find().pretty()
db.<collection>.aggregate({"\$match": {"startTime": {\$gt: ISODate("2018-01-01"), \$lt: ISODate("2018-01-31")}}}, 
                          {"\$group": {"_id": "\$_id"}},
                          {"\$sort": {count: -1}}).
                limit(1).
                pretty()
EOF

centos:~ # sh ex.sh
```


---

## Drivers


### From Python

```bash
# install pymongo
centos:~ # pip install pymongo
centos:~ # python -c "import pymongo"
```

---

## Reference

[Getting Started with MongoDB](https://docs.mongodb.com/getting-started/python/)
