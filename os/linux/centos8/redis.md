# redis

## install

`method1`

```bash
centos:~ # dnf install redis
```


`method2`

```bash
linux:~ # docker pull redis
linux:~ # docker run -d [-p 6379:6379] \
    --name redis \
    [-v /myredis/conf:/usr/local/etc/redis] \
    redis
linux:~ # docker exec -it redis redis-cli
```


`test`

```bash
linux:~ # redis-cli -h <host> -p <port> -a <password> [--raw]

linux:~ # redis-cli -h 127.0.0.1
127.0.0.1:6379> PING
```


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

127.0.0.1:6379> GETRANGE <KEY> <start> <end>
127.0.0.1:6379> GETSET <KEY> <VALUE>
127.0.0.1:6379> GETBIT <KEY> <OFFSET>
127.0.0.1:6379> MGET <KEY1> <KEY2> ... <KEYN>
127.0.0.1:6379> SETEX <KEY> <TIMEOUT> <VALUE>


# example
127.0.0.1:6379> SET name "redis"
127.0.0.1:6379> GET name

127.0.0.1:6379> SET mykey "This is my test key"
127.0.0.1:6379> GETRANGE mykey 0 3
127.0.0.1:6379> GETRANGE mykey 0 -1

127.0.0.1:6379> GETSET mynewkey "This is my test key"
127.0.0.1:6379> GETSET mynewkey "This is my new value to test getset"

127.0.0.1:6379> SET key1 "hello"
127.0.0.1:6379> SET key2 "world"
127.0.0.1:6379> MGET key1 key2

127.0.0.1:6379> SETEX mykey 60 redis
127.0.0.1:6379> TTL mykey
127.0.0.1:6379> GET mykey
```


### list

```bash
```



### hash

```bash
```



127.0.0.1:6379> KEYS *
TYPE <key>
