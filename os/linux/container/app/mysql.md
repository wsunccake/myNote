# mysql

## install

```bash
[linux:~ ] # docker pull mysql
[linux:~ ] # docker run -d \
    -e MYSQL_ROOT_PASSWORD=<password> \
    -p 3306:3306 \
    -p 33060:33060 \
    [-v /data/db:/var/lib/mysql] \
    [-v /data/cnf:/etc/mysql/conf.d] \
    --name mysql \
    mysql

[linux:~ ] # docker exec -it mysql mysql -u root -p
```
