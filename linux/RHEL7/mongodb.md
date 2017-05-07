# mongoDB

![mongodb](https://webassets.mongodb.com/_com_assets/global/mongodb-logo-white.png)


----

## Install

```
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

# run mongo client
centos:~ # monogo
```


----