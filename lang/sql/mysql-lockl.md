# mysql - lock

```sql
mysql> SELECT version();            -- version
mysql> STATUS;                      -- rmdbs status

mysql> SELECT CONNECTION_ID();      -- show connection id

mysql> SHOW OPEN TABLES;            -- list table lock status
mysql> SHOW PROCESSLIST;            -- list process
mysql> KILL <pid>                   -- kill connection

@@<var>                             -- System Vaiable
@<var>                              -- User Defined Variable
```


---

## transaction, commit, rollback

```sql
mysql> SET AUTOCOMMIT = 0;          -- manual commit and rollback
mysql> SET AUTOCOMMIT = OFF;

mysql> SET AUTOCOMMIT = 1;          -- auto commit, not rollback
mysql> SET AUTOCOMMIT = ON;

mysql> SELECT @@AUTOCOMMIT;         -- show current autocommit
```

```sql
mysql> SET AUTOCOMMIT = 0;

mysql> BEGIN;
mysql> DELETE FROM tutorials_tbl WHERE tutorial_title = "SQL%";
mysql> ROLLBACK;

mysql> START TRANSACTION;
mysql> DELETE FROM tutorials_tbl WHERE tutorial_title = "SQL%";
mysql> ROLLBACK;

mysql> BEGIN;
mysql> DELETE FROM tutorials_tbl WHERE tutorial_title = "SQL%";
mysql> COMMIT;

mysql> START TRANSACTION;
mysql> DELETE FROM tutorials_tbl WHERE tutorial_title = "SQL%";
mysql> COMMIT;
```

[START TRANSACTION, COMMIT, and ROLLBACK Statements](https://dev.mysql.com/doc/refman/8.0/en/commit.html)


---

## table lock

```sql
mysql> LOCK TABLES <table> [READ | WRITE]
...
mysql> UNLOCK TABLES;
```

```sql
mysql> CREATE TABLE IF NOT EXISTS LOCKTEST(
    ID   INTEGER PRIMARY KEY AUTO_INCREMENT,
    NAME TEXT NOT NULL
);
```


### write lock

```sql
session 1                           session 2
LOCK TABLES LOCKTEST WRITE;
                                    SELECT * FROM LOCKTEST;     -- pend
                                    INSERT INTO LOCKTEST (NAME) -- pend
                                        VALUES ('s20');
                                    LOCK TABLES LOCKTEST READ;  -- pend
                                    LOCK TABLES LOCKTEST WRITE; -- pend
UNLOCK TABLES;
```


### read lock

```sql
session 1                           session 2
LOCK TABLES LOCKTEST READ;
                                    SELECT * FROM LOCKTEST;     -- pass
                                    INSERT INTO LOCKTEST (NAME) -- pend
                                        VALUES ('s20');
                                    LOCK TABLES LOCKTEST WRITE; -- pend
                                    LOCK TABLES LOCKTEST READ;  -- pass, effect seesion to lock
INSERT INTO LOCKTEST (NAME) -- error
    VALUES ('s10');
                                    INSERT INTO LOCKTEST (NAME) -- pend
                                        VALUES ('s21');
                                    UNLOCK TABLES;
UNLOCK TABLES;
```

[LOCK TABLES and UNLOCK TABLES Statements](https://dev.mysql.com/doc/refman/8.0/en/lock-tables.html)


---

## lock read

```sql
mysql> SELECT ... FOR UPDATE [OF column_list][WAIT n|NOWAIT][SKIP LOCKED]; 

mysql> SELECT ... FOR UPDATE;
mysql> SELECT ... LOCK IN SHARE MODE;
```

```sql
mysql> BEGIN;

mysql> SELECT * FROM tutorials_tbl WHERE tutorial_id = 1 FOR UPDATE;        -- row lock, select primay key
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_id = -1 FOR UPDATE;       -- no lock, no find data
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_id > 3 FOR UPDATE;        -- table lock, no primay key

mysql> SELECT * FROM tutorials_tbl FOR UPDATE
mysql> SELECT * FROM tutorials_tbl FOR UPDATE NOWAIT
mysql> SELECT * FROM tutorials_tbl FOR UPDATE WAIT 5
mysql> SELECT * FROM tutorials_tbl FOR UPDATE SKIP LOCKED

mysql> COMMIT;
```
