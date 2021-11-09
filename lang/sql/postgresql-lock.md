# postgresql - lock

```sql
postgres=# SELECT version();            -- version

postgres=# \d pg_locks;                 -- list lock status
postgres=# SELECT * FROM pg_stat_activity WHERE datname = '<database>';
postgres=# SELECT pid FROM pg_stat_activity WHERE datname = '<database>' AND wait_event_type = 'Lock';
postgres=# SELECT pg_cancel_backend(<pid>);         -- cancel
postgres=# SELECT pg_terminate_backend(<pid>);      -- terminate

postgres=# SELECT txid_current();                   -- show connection id
```

```sql
postgres=# SELECT txid_current();      -- 123
postgres=# SELECT txid_current();      -- 124

postgres=# BEGIN;
postgres=# SELECT txid_current();      -- 125
postgres=# SELECT txid_current();      -- 125
postgres=# COMMIT;
```


---

## transaction, commit, rollback

```sql
BEGIN;
DELETE FROM DEPARTMENT WHERE ID = 1;
ROLLBACK;

BEGIN;
DELETE FROM DEPARTMENT WHERE ID = 1;
COMMIT;
```


---

## table lock

### lock mode

```
ACCESS EXCLUSIVE > EXCLUSIVE > SHARE ROW EXCLUSIVE > SHARE > SHARE UPDATE EXCLUSIVE > ROW EXCLUSIVE > ROW SHARE > ACCESS SHARE
```

```sql
postgres=# BEGIN;
postgres=# LOCK [ TABLE ] [ ONLY ] name [ * ] [, ...] [ IN <lock mode> MODE ] [ NOWAIT ]
...
postgres=# COMMIT|ROLLBACK;
```

```sql
postgres=# CREATE TABLE IF NOT EXISTS LOCKTEST(
    ID   SERIAL PRIMARY KEY,
    NAME TEXT NOT NULL
);
```

### ACCESS EXCLUSIVE

```sql
session 1                                           session 2
BEGIN;
LOCK TABLE LOCKTEST IN ACCESS EXCLUSIVE MODE;
                                                    BEGIN;                                          -- pass
                                                    LOCK TABLE LOCKTEST IN ACCESS EXCLUSIVE MODE;   -- pend
                                                    SELECT * FROM LOCKTEST;                         -- pend
COMMIT;
```


### EXCLUSIVE

### SHARE ROW EXCLUSIVE

### SHARE

### SHARE UPDATE EXCLUSIVE

### ROW EXCLUSIVE

### ROW SHARE

### ACCESS SHARE


---

## row lock

```
FOR UPDATE > FOR NO KEY UPDATE > FOR SHARE > FOR KEY SHARE
```

### FOR UPDATE

```sql
postgres=# BEGIN;

postgres=# SELECT * FROM DEPARTMENT WHERE ID = 1 FOR UPDATE;        -- row lock, select primay key
postgres=# SELECT * FROM DEPARTMENT WHERE ID = -1 FOR UPDATE;       -- no lock, no find data
postgres=# SELECT * FROM DEPARTMENT WHERE ID > 3 FOR UPDATE;        -- table lock, no primay key

postgres=# SELECT * FROM DEPARTMENT FOR UPDATE;
postgres=# SELECT * FROM DEPARTMENT FOR UPDATE NOWAIT;
postgres=# SELECT * FROM DEPARTMENT FOR UPDATE SKIP LOCKED;

postgres=# COMMIT;
```


### FOR NO KEY UPDATE

### FOR SHARE

### FOR KEY SHARE
