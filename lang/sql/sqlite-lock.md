# sqlite - lock

```sql
sqlite> SELECT sqlite_version();
```

```sql
sqlite> CREATE TABLE IF NOT EXISTS LOCKTEST(
   ID   INTEGER PRIMARY KEY AUTOINCREMENT,
   NAME TEXT NOT NULL
);

sqlite> INSERT INTO LOCKTEST (NAME) VALUES ('test');
```


## reading lock

```sql
session 1                           session 2
BEGIN;
                                    SELECT * FROM LOCKTEST;      -- pass
                                    INSERT INTO LOCKTEST (NAME)  -- pass
                                        VALUES ('s20');
INSERT INTO LOCKTEST (NAME)
    VALUES ('s11');
                                    SELECT * FROM LOCKTEST;      -- pass
                                    INSERT INTO LOCKTEST (NAME)  -- error
                                        VALUES ('s22');
COMMIT;
```


```sql
session 1                           session 2
BEGIN;
                                    BEGIN;
                                    SELECT * FROM LOCKTEST;      -- pass
                                    INSERT INTO LOCKTEST (NAME)  -- pass
                                        VALUES ('s20');   
INSERT INTO LOCKTEST (NAME) -- error
    VALUES ('s11');
                                    COMMIT;
COMMIT;
```


---

## writing lock

```sql
session 1                           session 2
BEGIN EXCLUSIVE;
                                    SELECT * FROM LOCKTEST;     -- error
                                    INSERT INTO LOCKTEST (NAME) -- error
                                        VALUES ('s21');
INSERT INTO LOCKTEST (NAME)
    VALUES ('s11');
                                    SELECT * FROM LOCKTEST;     -- pass
                                    INSERT INTO LOCKTEST (NAME) -- error
                                        VALUES ('s22');
COMMIT;
```

```sql
session 1                           session 2
BEGIN EXCLUSIVE;
                                    BEGIN EXCLUSIVE;    -- error
COMMIT;
```

```sql
session 1                           session 2
BEGIN EXCLUSIVE;
                                    BEGIN IMMEDIATE;    -- error
COMMIT;
```

```sql
session 1                           session 2
BEGIN EXCLUSIVE;
                                    BEGIN;                      -- pass
                                    INSERT INTO LOCKTEST (NAME) -- error
                                        VALUES ('s11');
INSERT INTO LOCKTEST (NAME) --pass
    VALUES ('s11');
                                    COMMIT;
COMMIT;
```


---

## reserved lock

```sql
session 1                           session 2
BEGIN IMMEDIATE;
                                    SELECT * FROM LOCKTEST;     -- pass
                                    INSERT INTO LOCKTEST (NAME) -- error
                                        VALUES ('s20');
INSERT INTO LOCKTEST (NAME)
    VALUES ('s11');
                                    SELECT * FROM LOCKTEST;     -- pass
                                    INSERT INTO LOCKTEST (NAME) -- error
                                        VALUES ('s22');
COMMIT;
```

```sql
session 1                           session 2
BEGIN IMMEDIATE;
                                    BEGIN EXCLUSIVE; -- error
COMMIT;
```

```sql
session 1                           session 2
BEGIN IMMEDIATE;
                                    BEGIN IMMEDIATE; -- error
COMMIT;
```

```sql
session 1                           session 2
BEGIN IMMEDIATE;
                                    BEGIN; -- pass
                                    SELECT * FROM LOCKTEST;     -- pass
                                    INSERT INTO LOCKTEST (NAME) -- error
                                        VALUES ('s20');
COMMIT; -- error
                                    COMMIT;
COMMIT;
```


---

## ref

[Understanding SQLITE_BUSY](https://activesphere.com/blog/2018/12/24/understanding-sqlite-busy)
