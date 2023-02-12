# redis

## install

`method1`

```bash
centos:~ # dnf install redis
```

`method2`

```bash
centos:~ # docker pull redis
centos:~ # docker run -d [-p 6379:6379] \
    --name redis \
    [-v /myredis/conf:/usr/local/etc/redis] \
    redis
linux:~ # docker exec -it redis redis-cli
```

`test`

```bash
centos:~ # redis-cli -h <host> -p <port> -a <password> [--raw]

centos:~ # redis-cli -h 127.0.0.1
127.0.0.1:6379> PING
```

default host: 127.0.0.1

default port: 6379

---

## config

```bash
# get config
127.0.0.1:6379> CONFIG GET <CONFIG_SETTING_NAME>

# example
127.0.0.1:6379> CONFIG GET *
127.0.0.1:6379> CONFIG GET loglevel


# set config
127.0.0.1:6379> CONFIG SET CONFIG_SETTING_NAME NEW_CONFIG_VALUE

# example
127.0.0.1:6379> CONFIG SET loglevel "notice"

# auth
127.0.0.1:6379> CONFIG SET requirepass <password>
127.0.0.1:6379> AUTH <password>
```

---

## keysapce / database

```bash
127.0.0.1:6379> CONFIG GET databases
127.0.0.1:6379> INFO Keyspace
127.0.0.1:6379> SELECT <database>
```

---

## key

```bash
127.0.0.1:6379> SET <KEY> <VALUE>
127.0.0.1:6379> GET <KEY>
127.0.0.1:6379> KEYS <pattern>
127.0.0.1:6379> DEL <KEY>
127.0.0.1:6379> DUMP <KEY>
127.0.0.1:6379> TYPE <KEY>
127.0.0.1:6379> EXISTS <KEY>

127.0.0.1:6379> TTL <KEY>
127.0.0.1:6379> PTTL <KEY>
127.0.0.1:6379> EXPIRE <KEY> <second>
127.0.0.1:6379> EXPIREAT <KEY> <timestamp>
127.0.0.1:6379> PEXPIRE <KEY> <millisecond>
127.0.0.1:6379> PEXPIREAT <KEY> <timestamp>
127.0.0.1:6379> PERSIST <KEY>

127.0.0.1:6379> RANDOMKEY
127.0.0.1:6379> RENAME <OLD_KEY> <NEW_KEY>
127.0.0.1:6379> RENAMENX <OLD_KEY> <NEW_KEY>

127.0.0.1:6379> MOVE <KEY> <DATABASE>

# example
127.0.0.1:6379> SET name 'redis'
127.0.0.1:6379> GET name
127.0.0.1:6379> KEYS *
127.0.0.1:6379> DEL name
127.0.0.1:6379> DUMP name
127.0.0.1:6379> TYPE name
127.0.0.1:6379> EXISTS name

127.0.0.1:6379> SET name 'redis'
127.0.0.1:6379> TTL name
127.0.0.1:6379> PTTL name
127.0.0.1:6379> EXPIRE name 5
127.0.0.1:6379> EXPIREAT name 1293840000
127.0.0.1:6379> PEXPIRE name 1500
127.0.0.1:6379> PEXPIREAT name 1293840000
127.0.0.1:6379> PERSIST name

127.0.0.1:6379> RANDOMKEY
127.0.0.1:6379> RENAME name nickname
127.0.0.1:6379> RENAMENX name nickname

127.0.0.1:6379> MOVE name 3
127.0.0.1:6379> SELECT 3
127.0.0.1:6379> GET name
```

---

## data

### string

```bash
127.0.0.1:6379> SET <KEY> <VALUE>
127.0.0.1:6379> GET <KEY>

127.0.0.1:6379> SETNX <KEY> <VALUE>
127.0.0.1:6379> SETEX <KEY> <TIMEOUT, second> <VALUE>
127.0.0.1:6379> PSETEX <KEY> <TIMEOUT, millisecond> <VALUE>

127.0.0.1:6379> MSET <KEY1> <KEY2> ... <KEYN>
127.0.0.1:6379> MGET <KEY1> <KEY2> ... <KEYN>
127.0.0.1:6379> MSETNX <KEY1> <KEY2> ... <KEYN>

127.0.0.1:6379> GETRANGE <KEY> <start> <end>
127.0.0.1:6379> GETSET <KEY> <VALUE>

127.0.0.1:6379> GETBIT <KEY> <OFFSET>
127.0.0.1:6379> SETBIT <KEY> <OFFSET> <VALUE>

127.0.0.1:6379> STRLEN <KEY>
127.0.0.1:6379> SETRANGE <KEY> <OFFSET> <VALUE>

127.0.0.1:6379> INCR <KEY>
127.0.0.1:6379> INCRBY <KEY> <increment>
127.0.0.1:6379> DECR <KEY>
127.0.0.1:6379> DECRBY <KEY> <decrement>

127.0.0.1:6379> APPEND <KEY> <VALUE>

# example
127.0.0.1:6379> SET name "redis"
127.0.0.1:6379> GET name

127.0.0.1:6379> EXISTS job
127.0.0.1:6379> SETNX job "programmer"
127.0.0.1:6379> SETNX job "code-farmer"
127.0.0.1:6379> GET job

127.0.0.1:6379> MSET key1 "Hello" key2 "World"
127.0.0.1:6379> MGET key1 key2
127.0.0.1:6379> MSETNX rmdbs "MySQL" nosql "MongoDB" key-value-store "redis"

127.0.0.1:6379> EXISTS mykey
127.0.0.1:6379> SETEX mykey 60 redis
127.0.0.1:6379> TTL mykey
127.0.0.1:6379> GET mykey
127.0.0.1:6379> PSETEX mykey 1000 redis
127.0.0.1:6379> PTTL mykey
127.0.0.1:6379> GET mykey

127.0.0.1:6379> SET mykey "This is my test key"
127.0.0.1:6379> GETRANGE mykey 0 3
127.0.0.1:6379> GETRANGE mykey 0 -1

127.0.0.1:6379> GETSET mynewkey "This is my test key"
127.0.0.1:6379> GETSET mynewkey "This is my new value to test getset"

127.0.0.1:6379> EXISTS bit
127.0.0.1:6379> GETBIT bit 10086
127.0.0.1:6379> SETBIT bit 10086 1
127.0.0.1:6379> GETBIT bit 10086

127.0.0.1:6379> SET mykey "Hello world"
127.0.0.1:6379> STRLEN mykey
127.0.0.1:6379> SETRANGE mykey 6 "Redis"
127.0.0.1:6379> GET mykey

127.0.0.1:6379> SET page_view 20
127.0.0.1:6379> INCR page_view
127.0.0.1:6379> GET page_view
127.0.0.1:6379> INCRBY page_view 30

127.0.0.1:6379> SET failure_times 10
127.0.0.1:6379> DECR failure_times
127.0.0.1:6379> GET failure_times
127.0.0.1:6379> DECRBY failure_times 4

127.0.0.1:6379> EXISTS myphone
127.0.0.1:6379> APPEND myphone "nokia"
127.0.0.1:6379> APPEND myphone " - 1110"
127.0.0.1:6379> GET myphone
```

### hash

```bash
127.0.0.1:6379> HSET <KEY> <FIELD1> <VALUE1> [<FIELD2> <VALUE2> ...]
127.0.0.1:6379> HGET <KEY> <FIELD1> [<FIELD2> ...]
127.0.0.1:6379> HDEL <KEY> <FIELD1> [<FIELD2> ...]
127.0.0.1:6379> HEXISTS <KEY> <FIELD>
127.0.0.1:6379> HGETALL <KEY>
127.0.0.1:6379> HKEYS <KEY>
127.0.0.1:6379> HVALS <KEY>
127.0.0.1:6379> HLEN <KEY>

127.0.0.1:6379> HSETNX <KEY> <FIELD1> <VALUE1> [<FIELD2> <VALUE2> ...]

127.0.0.1:6379> HMSET <KEY> <FIELD1> <VALUE1> [<FIELD2> <VALUE2> ...]
127.0.0.1:6379> HMGET <KEY> <FIELD1> [<FIELD2> ...]

127.0.0.1:6379> HINCRBY <KEY> <FIELD> <increment>
127.0.0.1:6379> HINCRBYFLOAT <KEY> <FIELD> <increment>

# example
127.0.0.1:6379> HSET myhash rmdbs "MySQL" document-store "MongoDB" key-value-store "redis"
127.0.0.1:6379> HGET myhash rmdbs
127.0.0.1:6379> HDEL myhash rmdbs
127.0.0.1:6379> HEXISTS myhash rmdbs
127.0.0.1:6379> HGETALL myhash
127.0.0.1:6379> HKEYS myhash
127.0.0.1:6379> HVALS myhash
127.0.0.1:6379> HLEN myhash

127.0.0.1:6379> HSETNX myhash wide-column-store "Cassandra"
127.0.0.1:6379> HSETNX myhash nosql "non-sql"
127.0.0.1:6379> HSETNX myhash nosql "Cassandra"
```

### list

```bash
127.0.0.1:6379> LPUSH <KEY> <VALUE1> [<VALUE2> ...]
127.0.0.1:6379> LPOP <KEY>
127.0.0.1:6379> RPUSH <KEY> <VALUE1> [<VALUE2> ...]
127.0.0.1:6379> RPOP <KEY>
127.0.0.1:6379> LRANGE <KEY> <start> <stop>

127.0.0.1:6379> LLEN <KEY>
127.0.0.1:6379> LSET <KEY> <INDEX> <VALUE>
127.0.0.1:6379> LINDEX <KEY> <INDEX>
127.0.0.1:6379> LREM <KEY> <count> <VALUE>
# count > 0, from start to stop
# count < 0, from stop to start
# count = 0, all value
127.0.0.1:6379> LTRIM <KEY> <start> <stop>

127.0.0.1:6379> LPUSHX <KEY> <VALUE1> [<VALUE2> ...]
127.0.0.1:6379> RPUSHX <KEY> <VALUE1> [<VALUE2> ...]

# example
127.0.0.1:6379> LPUSH mylist redis
127.0.0.1:6379> LPUSH mylist mongodb memcache
127.0.0.1:6379> LRANGE mylist 0 10
127.0.0.1:6379> LPOP mylist

127.0.0.1:6379> RPUSH mylist mysql
127.0.0.1:6379> RPUSH mylist sqlite postgre
127.0.0.1:6379> LRANGE mylist 0 -1
127.0.0.1:6379> RPOP mylist

127.0.0.1:6379> LLEN mylist
127.0.0.1:6379> LSET mylist 0 cassandra
127.0.0.1:6379> LINDEX mylist 3
127.0.0.1:6379> LREM mylist 0 mongodb
127.0.0.1:6379> LTRIM mylist 1 -1

127.0.0.1:6379> LPUSHX mylist2 redis
127.0.0.1:6379> RPUSHX mylist2 redis
```

### set
