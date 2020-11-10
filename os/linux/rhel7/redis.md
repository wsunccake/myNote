# Redis

![redis](https://redis.io/images/redis-white.png)


---

## Install

```
# install package
centos:~ # yum install redis

# start service
centos:~ # systemctl start redis
centos:~ # systemctl enable redis

# test service
centos:~ # redis-cli ping
```

## Configure

```
centos:~ # vi /etc/redis.conf
```


---

## Command

```
cnetos:~ # redis-cli
127.0.0.1:6379>
```

### STRING

```
127.0.0.1:6379> SET hello world
127.0.0.1:6379> GET hello
127.0.0.1:6379> DEL hello
```


### SET

```
127.0.0.1:6379> SADD db-set mysql oracle
127.0.0.1:6379> SMEMBERS db-set
127.0.0.1:6379> SISMEMBER db-set mysql
127.0.0.1:6379> SREM db-set oracle
```


### LIST

```
127.0.0.1:6379> RPUSH db-list redis mongo 
127.0.0.1:6379> LPUSH db-list cassandra
127.0.0.1:6379> LRANGE db-list 0 -1
127.0.0.1:6379> LINDEX db-list 0
127.0.0.1:6379> LPOP db-list
```


### HASH

```
127.0.0.1:6379> HSET pl-hash perl 1
127.0.0.1:6379> HEXISTS pl-hash perl
127.0.0.1:6379> HGET pl-hash perl 
127.0.0.1:6379> HGETALL pl-hash 
127.0.0.1:6379> HDEL pl-hash pl-hash
```


### ZSET

```
127.0.0.1:6379> ZADD pl-zset 1 java 
127.0.0.1:6379> ZRANGE pl-zset 0 -1
127.0.0.1:6379> ZREM pl-zset java
```

---


## Test

```
centos:~ # pip install redis
centos:~ # pip install hiredis
centos:~ # cat hello.py
#!/usr/bin/env python

import redis

conn = redis.Redis()
conn.set('hello', 'world')
print (conn.get('hello'))

```
