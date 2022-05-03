# Postge SQL


## package

```bash
linux:~ # yum install postgresql
```


--

## service


```bash
linux:~ # yum install postgresql-server

# initial database
linux:~ # postgresql-setup initdb

# service
linux:~ # systemctl enable postgresql.service
linux:~ # systemctl start postgresql.service
linux:~ # systemctl status postgresql.service

# control command
linux:~ # pg_ctl start
linux:~ # pg_ctl stop
linux:~ # pg_ctl status
linux:~ # pg_ctl restart
linux:~ # pg_ctl reload

# psql default port 5432
linux:~ # netstat -luntp | grep 5432

# config
linux:~ # pg_config                                 # show config
linux:~ # ls /var/lib/pgsql/data                    # psql config & db folder
linux:~ # cat /var/lib/pgsql/data/postgresql.conf   # default config
linux:~ # psql -c "SHOW ALL;"
```


---

## basic

```bash
# login
linux:~ # su - postgres
linux:~ $ psql

# service
linux:~ # pg_ctl reload

# user
linux:~ $ createuser -P [-c <n>] [-d|-D] [-r|-R] [-s|-S] <new_user>
# -c: --connection-limit
# -d: --createdb, -D: --no-createdb
# -r: --createrole, -R: --no-createrole
# -s: --superuser, -S: --no-superuser
linux:~ $ dropuser <user>           # delete user
linux:~ $ psql -c "\du"             # list user

# password
linux:~ $ psql -c "\password [<db_user>]"       # change password
linux:~ $ psql << EOF
ALTER USER <db_user> WITH PASSWORD '<new_password>';
EOF

# db
linux:~ $ createdb -O <db_user> <db>
linux:~ $ dropdb <db>               # delete db
linux:~ $ psql -c "\l"              # list db
linux:~ $ psql << EOF
\l
EOF

# login
linux:~ # psql -U <db_user> -d <db> -h <host> -p <port> -W

# remote login config
linux:~ # grep -Ev '^#|^$|^\s+#' /var/lib/pgsql/data/postgresql.conf
linux:~ # vi /var/lib/pgsql/data/postgresql.conf
listen_addresses = '0.0.0.0'
port = 5432
...

linux:~ # psql -c "SHOW hba_file;" -U postgres
linux:~ # vi /var/lib/pgsql/data/pg_hba.conf
host    all    all    0.0.0.0/0    md5
host    all    all    ::0/0        md5
...

linux:~ # systemctl restart postgresql.service

# test
linux:~ # cat << EOF > create_users.sql
create table users (
  id   serial primary key,
  name text not null,
  age  int  not null
);
EOF

linux:~ # cat << EOF > insert_users.sql
insert into users(id, name, age) values(1, 'lpj', 20);
EOF

linux:~ # psql -U <db_user> -d <db> -h <host> -p <port> -W -f create_users.sql
linux:~ # psql -U <db_user> -d <db> -h <host> -p <port> -W -f insert_users.sql
linux:~ # psql -U <db_user> -d <db> -h <host> -p <port> -W -c "select * from users;"
linux:~ # psql -U <db_user> -d <db> -h <host> -p <port> << EOF
\l
select * from users;
EOF
```

```bash
# password file
linux:~ # cat $HOME/.pgpass
<host>:<port>:<db>:<db_user>:<db_password>
...

linux:~ # chmod 0600 $HOME/.pgpass
linux:~ # psql -c "select * from users;"

# environment variable
linux:~ # export PGHOST=<host>
linux:~ # export PGPORT=<port>
linux:~ # export PGUSER=<db_user>
linux:~ # export PGPASSWORD=<db_password>
linux:~ # psql -c "select * from users;"

# uri -> postgresql://[<db_user>[:<db_password>]@][<host>[:<port>]][/dbname][?params]
```

```sql
-- help
postgres=# \h  -- help with SQL
postgres=# \?  -- help with psql

-- user
postgres=# \du
postgres=# \password <db_user>
```


---

## databse

DDL

```sql
postgres=# CREATE DATABASE <database_name>;  -- create database
postgres=# DROP DATABASE <database_name>;    -- delete database
postgres=# \l                                -- list database
postgres=# \c <database_name>                -- use database

-- example
postgres=# CREATE DATABASE testdb;
postgres=# \l
postgres=# \c testdb                         -- after chage database, prompt become database name
testdb=#
postgres=# DROP DATABASE testdb;
```


### dump

```bash
# backup
linux:~ # pg_dump -U postgres <database_name> > <database_name>.sql
linux:~ # pg_dump -U postgres <database_name> | gzip > <database_name>.gz

# restore
linux:~ # psql -U postgres --set ON_ERROR_STOP=on <database_name> < <database_name>.sql
linux:~ # gunzip -c <database_name>.gz | psql -U postgres --set ON_ERROR_STOP=on <database_name>
linux:~ # cat <database_name>.gz | gunzip | psql -U postgres --set ON_ERROR_STOP=on <database_name>
```


---

## table

DDL


### create table

```sql
postgres=# CREATE TABLE <table_name>(<column_name> <data_type>);

-- example
postgres=# CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL,
   JOIN_DATE      DATE
);

postgres=# CREATE TABLE DEPARTMENT(
   ID INT PRIMARY KEY      NOT NULL,
   DEPT           CHAR(50) NOT NULL,
   EMP_ID         INT      NOT NULL
);
```


### drop table

```sql
postgres=# DROP TABLE <table_name>;

-- example
postgres=# DROP TABLE COMPANY;
```

### alter table

```sql
postgres=# ALTER TABLE <table_name> ADD|DROP|ALTER|RENAME <column_name> <data_type>;

-- example
postgres=# ALTER TABLE COMPANY ADD TMP_COLUNM INT;
postgres=# ALTER TABLE COMPANY RENAME TMP_COLUNM TO TMP_COL;
postgres=# ALTER TABLE COMPANY ALTER COLUMN TMP_COL TYPE char(3);
postgres=# ALTER TABLE COMPANY DROP TMP_COL ;
```


### list table

```sql
postgres=# \dt
postgres=# \d
postgres=# \d COMPANY
```


---

## row


### create / add

DML

```sql
postgres=# INSERT INTO <table_name> [(<column>, ...)] VALUES (<value>, ...);    -- create row

-- example
postgres=# INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY,JOIN_DATE)
   VALUES (1, 'Paul', 32, 'California', 20000.00 ,'2001-07-13'),
   (2, 'Allen', 25, 'Texas', 10000.00,'2007-12-13'),
   (3, 'Teddy', 23, 'Norway', 20000.00, DEFAULT ),
   (4, 'Mark', 25, 'Rich-Mond ', 65000.00, NOW()),
   (5, 'David', 27, 'Texas', 85000.00, DEFAULT),
   (6, 'Kim', 22, 'South-Hall', 45000.00, NOW()),
   (7, 'James', 24, 'Houston', 10000.00, NOW()),
   (8, 'Paul', 24, 'Houston', 20000.00,NOW() ),
   (9, 'James', 44, 'Norway', 5000.00,NOW() ),
   (10, 'James', 45, 'Texas', 5000.00, DEFAULT);

postgres=# INSERT INTO DEPARTMENT (ID, DEPT, EMP_ID)
   VALUES (1, 'IT Billing', 1 ),
   (2, 'Engineering', 2 ),
   (3, 'Finance', 7 );
```

### read / query

DQL


#### selet

```sql
-- query usage:
postgres=#  SELECT *|<column1>, <column2>, ... <columnN> FROM <table1>, <table2>...
  [WHERE <clause>]
  [OFFSET M ][LIMIT N]

-- example
postgres=# SELECT * FROM COMPANY;
postgres=# SELECT name, AGE FROM COMPANY;
```


#### express

```sql
postgres=# SELECT 3 + 1
postgres=# SELECT (15 + 6) AS ADDITION;
postgres=# SELECT COUNT(*) AS "RECORDS" FROM COMPANY;
postgres=# SELECT CURRENT_TIMESTAMP;
postgres=# SELECT DATETIME('now','localtime');
```


#### operator

```sql
-- arithmetic operator
postgres=# SELECT 10 + 20;
postgres=# SELECT 10 - 20;
postgres=# SELECT 10 * 20;
postgres=# SELECT 10 / 5;
postgres=# SELECT 12 % 5;

-- bitwise operator
postgres=# SELECT 60 | 13;
postgres=# SELECT 60 & 13;
postgres=# SELECT (~60);
postgres=# SELECT (60 << 2);
postgres=# SELECT (60 >> 2);

-- comparison operator
postgres=# SELECT * FROM COMPANY WHERE SALARY > 50000;
postgres=# SELECT * FROM COMPANY WHERE SALARY = 20000;
postgres=# SELECT * FROM COMPANY WHERE SALARY != 20000;
postgres=# SELECT * FROM COMPANY WHERE SALARY <> 20000;
postgres=# SELECT * FROM COMPANY WHERE SALARY >= 65000;

-- logical operator
postgres=# SELECT * FROM COMPANY WHERE AGE >= 25 AND SALARY >= 65000;
postgres=# SELECT * FROM COMPANY WHERE AGE >= 25 OR SALARY >= 65000;
postgres=# SELECT * FROM COMPANY WHERE AGE IS NOT NULL;
postgres=# SELECT * FROM COMPANY WHERE NAME LIKE 'Ki%';
postgres=# SELECT * FROM COMPANY WHERE AGE IN ( 25, 27 );
postgres=# SELECT * FROM COMPANY WHERE AGE NOT IN ( 25, 27 );
postgres=# SELECT * FROM COMPANY WHERE AGE BETWEEN 25 AND 27;
postgres=# SELECT AGE FROM COMPANY
   WHERE EXISTS (SELECT AGE FROM COMPANY WHERE SALARY > 65000);
postgres=#  SELECT * FROM COMPANY
   WHERE AGE > (SELECT AGE FROM COMPANY WHERE SALARY > 65000);
```


#### where

```sql
-- and, or
postgres=# SELECT * FROM COMPANY WHERE AGE >= 25 AND SALARY >= 65000;
postgres=# SELECT * FROM COMPANY WHERE AGE >= 25 OR SALARY >= 65000;

postgres=# SELECT * FROM COMPANY WHERE AGE IS NOT NULL;

-- like
postgres=# SELECT * FROM COMPANY WHERE NAME LIKE 'Ki%';

-- %, _
postgres=# SELECT * FROM COMPANY WHERE AGE LIKE '%2';
postgres=# SELECT * FROM COMPANY WHERE AGE LIKE '_2';
postgres=# SELECT * FROM COMPANY WHERE ADDRESS LIKE '%-%';
postgres=# SELECT * FROM COMPANY WHERE ADDRESS NOT LIKE '%-%';
postgres=# SELECT * FROM COMPANY WHERE ADDRESS LIKE '____-%';

-- SIMILAR TO
postgres=# SELECT * FROM COMPANY WHERE ADDRESS SIMILAR TO '(N|C)%';
postgres=# SELECT * FROM COMPANY WHERE NAME SIMILAR TO '%l%';

-- ~, posix regex
postgres=# SELECT * FROM COMPANY WHERE NAME ~ 'allen';   -- case sensitive
postgres=# SELECT * FROM COMPANY WHERE NAME ~* 'allen';  -- case insensitive
postgres=# SELECT * FROM COMPANY WHERE NAME !~ 'l$';     -- case sensitive
postgres=# SELECT * FROM COMPANY WHERE NAME !~* 'l$';    -- case insensitive


-- in, between
postgres=# SELECT * FROM COMPANY WHERE AGE IN (25, 27);
postgres=# SELECT * FROM COMPANY WHERE AGE NOT IN (25, 27);
postgres=# SELECT * FROM COMPANY WHERE AGE BETWEEN 25 AND 27;

-- limit, offset
postgres=# SELECT * FROM COMPANY LIMIT 2;
postgres=# SELECT * FROM COMPANY LIMIT 2 OFFSET 3;

-- order by ... asc|desc
postgres=# SELECT * FROM COMPANY ORDER BY SALARY ASC;
postgres=# SELECT * FROM COMPANY ORDER BY NAME DESC, SALARY ASC;

-- group by
postgres=# SELECT NAME, SUM(SALARY), COUNT(*), AVG(SALARY)
   FROM COMPANY GROUP BY NAME ORDER BY NAME;

-- having
postgres=# SELECT NAME FROM COMPANY GROUP BY name HAVING count(name) > 1;

-- distinct
postgres=# SELECT name FROM COMPANY;
postgres=# SELECT DISTINCT name FROM COMPANY;

-- sub-where
postgres=# SELECT AGE FROM COMPANY
   WHERE EXISTS (SELECT AGE FROM COMPANY WHERE SALARY > 65000);
postgres=# SELECT * FROM COMPANY
   WHERE AGE > (SELECT AGE FROM COMPANY WHERE SALARY > 65000);
```


### update / modify

DDL

```sql
postgres=# postgres=# UPDATE <table_name> SET <column> = <value>, ... [WHERE <clause>];  -- update row

-- example
postgres=# UPDATE COMPANY SET SALARY = 15000 WHERE ID = 1;
```


### delete / remove

DML

```sql
postgres=# DELETE FROM <table_name> [WHERE <clause>];   -- delete row

-- example
postgres=# DELETE FROM COMPANY WHERE ID = 3;
```


### truncate

```sql
-- truncate table
postgres=# TRUNCATE TABLE COMPANY;

postgres=# SELECT * FROM COMPANY;
```


---

## advanced


### constraint

`method1`

```sql
postgres=# CREATE TABLE COMPANY_CONSTRAINT(
   ID INT PRIMARY KEY     NOT NULL,                      -- primary key
   NAME           TEXT    NOT NULL,                      -- not null
   AGE            INT     CHECK(AGE > 0),                -- check
   ADDRESS        CHAR(50),
   SALARY         REAL    DEFAULT 50000.00               -- default
);

postgres=# CREATE TABLE DEPARTMENT_CONSTRAINT(
   ID        INT      UNIQUE,                            -- unique
   DEPT      CHAR(50) NOT NULL,
   EMP_ID    INT      REFERENCES COMPANY_CONSTRAINT(ID)  -- foreign key ... references
);
```


`method2`

```sql
postgres=# CREATE TABLE COMPANY_CONSTRAINT(
   ID             INT     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT,
   ADDRESS        CHAR(50),
   SALARY         REAL    DEFAULT 50000.00,
   CONSTRAINT PRIMARY_KEY_CONSTRAINT PRIMARY KEY (ID),
   CONSTRAINT CHECK_CONSTRAINT CHECK(AGE > 0)
);

postgres=# CREATE TABLE DEPARTMENT_CONSTRAINT(
   ID        INT       NOT NULL,
   DEPT      CHAR(50)  NOT NULL,
   EMP_ID    INT,
   CONSTRAINT UNIQUE_CONSTRAINT UNIQUE(ID),
   CONSTRAINT REFERENCES_CONSTRAINT FOREIGN KEY (EMP_ID) REFERENCES COMPANY_CONSTRAINT(ID)
);
```


`method3`

```sql
postgres=# CREATE TABLE COMPANY_CONSTRAINT(
   ID        INT,
   NAME      TEXT,
   AGE       INT,
   ADDRESS   CHAR(50),
   SALARY    REAL
);

-- primary key
postgres=# ALTER TABLE COMPANY_CONSTRAINT ADD CONSTRAINT PRIMARY_KEY_CONSTRAINT PRIMARY KEY (ID);
postgres=# ALTER TABLE COMPANY_CONSTRAINT DROP CONSTRAINT PRIMARY_KEY_CONSTRAINT;

-- check
postgres=# ALTER TABLE COMPANY_CONSTRAINT ADD CONSTRAINT CHECK_CONSTRAINT CHECK(AGE > 0);
postgres=# ALTER TABLE COMPANY_CONSTRAINT DROP CONSTRAINT CHECK_CONSTRAINT;

-- default
postgres=# ALTER TABLE COMPANY_CONSTRAINT ALTER COLUMN SALARY DROP DEFAULT;
postgres=# ALTER TABLE COMPANY_CONSTRAINT ALTER COLUMN SALARY SET DEFAULT(50000.00);


postgres=# CREATE TABLE DEPARTMENT_CONSTRAINT(
   ID        INT,
   DEPT      CHAR(50),
   EMP_ID    INT
);

-- not null
postgres=# ALTER TABLE DEPARTMENT_CONSTRAINT ALTER COLUMN DEPT DROP NOT NULL;
postgres=# ALTER TABLE DEPARTMENT_CONSTRAINT ALTER COLUMN DEPT SET NOT NULL;

-- unique
postgres=# ALTER TABLE DEPARTMENT_CONSTRAINT ADD CONSTRAINT UNIQUE_CONSTRAINT UNIQUE(ID);
postgres=# ALTER TABLE DEPARTMENT_CONSTRAINT DROP CONSTRAINT UNIQUE_CONSTRAINT;

-- foreign key ... references
postgres=# ALTER TABLE DEPARTMENT_CONSTRAINT ADD CONSTRAINT REFERENCES_CONSTRAINT
   FOREIGN KEY (EMP_ID) REFERENCES COMPANY_CONSTRAINT(ID);
postgres=# ALTER TABLE DEPARTMENT_CONSTRAINT DROP CONSTRAINT REFERENCES_CONSTRAINT;
```


### join

```sql
-- cross join
postgres=# SELECT EMP_ID, NAME, DEPT FROM COMPANY CROSS JOIN DEPARTMENT;

-- inner join
postgres=# SELECT EMP_ID, NAME, DEPT FROM COMPANY INNER JOIN DEPARTMENT
   ON COMPANY.ID = DEPARTMENT.EMP_ID;

-- left outer
postgres=# SELECT EMP_ID, NAME, DEPT FROM COMPANY LEFT OUTER JOIN DEPARTMENT
        ON COMPANY.ID = DEPARTMENT.EMP_ID;

-- right outer
postgres=# SELECT EMP_ID, NAME, DEPT FROM COMPANY RIGHT OUTER JOIN DEPARTMENT
        ON COMPANY.ID = DEPARTMENT.EMP_ID;

-- full outer
postgres=# SELECT EMP_ID, NAME, DEPT FROM COMPANY FULL OUTER JOIN DEPARTMENT
        ON COMPANY.ID = DEPARTMENT.EMP_ID;
```


### union


```sql
postgres=# SELECT EMP_ID, NAME, DEPT FROM COMPANY INNER JOIN DEPARTMENT
   ON COMPANY.ID = DEPARTMENT.EMP_ID;
postgres=# SELECT EMP_ID, NAME, DEPT FROM COMPANY LEFT OUTER JOIN DEPARTMENT
   ON COMPANY.ID = DEPARTMENT.EMP_ID;

-- union
postgres=# SELECT EMP_ID, NAME, DEPT FROM COMPANY INNER JOIN DEPARTMENT
     ON COMPANY.ID = DEPARTMENT.EMP_ID
   UNION
   SELECT EMP_ID, NAME, DEPT FROM COMPANY LEFT OUTER JOIN DEPARTMENT
     ON COMPANY.ID = DEPARTMENT.EMP_ID;

-- union all
postgres=# SELECT EMP_ID, NAME, DEPT FROM COMPANY INNER JOIN DEPARTMENT
     ON COMPANY.ID = DEPARTMENT.EMP_ID
   UNION ALL
   SELECT EMP_ID, NAME, DEPT FROM COMPANY LEFT OUTER JOIN DEPARTMENT
     ON COMPANY.ID = DEPARTMENT.EMP_ID;
```


### as

```sql
-- table as ...
postgres=# SELECT C.ID, C.NAME, C.AGE, D.DEPT
   FROM COMPANY AS C, DEPARTMENT AS D
   WHERE  C.ID = D.EMP_ID;

-- column as ...
postgres=# SELECT C.ID AS COMPANY_ID, C.NAME AS COMPANY_NAME, C.AGE, D.DEPT
   FROM COMPANY AS C, DEPARTMENT AS D
   WHERE C.ID = D.EMP_ID;
```


### trigger

```sql
postgres=# CREATE TABLE AUDIT(
    EMP_ID INT NOT NULL,
    ENTRY_DATE TEXT NOT NULL
);

postgres=# CREATE OR REPLACE FUNCTION auditlogfunc() RETURNS TRIGGER AS $example_table$
    BEGIN
        INSERT INTO AUDIT(EMP_ID, ENTRY_DATE) VALUES (new.ID, current_timestamp);
        RETURN NEW;
    END;
$example_table$ LANGUAGE plpgsql;

-- create trigger
postgres=# CREATE TRIGGER EXAMPLE_TRIGGER AFTER INSERT ON COMPANY
   FOR EACH ROW EXECUTE PROCEDURE auditlogfunc();

postgres=# INSERT INTO COMPANY VALUES (11, 'Watson', 50, 'Alabama', 15000.00 );
postgres=# SELECT * FROM AUDIT;

-- list trigger
postgres=# \df
postgres=# SELECT * FROM pg_trigger;
postgres=# SELECT tgname FROM pg_trigger, pg_class WHERE tgrelid=pg_class.oid AND relname='COMPANY';

-- drop trigger
postgres=# DROP TRIGGER trigger_name;
```


### index

```sql
-- create index
postgres=# CREATE INDEX SALARY_INDEX ON COMPANY (SALARY);

-- list index
postgres=# \di
postgres=# \d COMPANY

-- drop index
postgres=# DROP INDEX SALARY_INDEX
```


### view

```sql
-- create view
postgres=# CREATE VIEW COMPANY_VIEW AS
   SELECT ID, NAME, AGE
   FROM  COMPANY;

postgres=# SELECT * FROM COMPANY_VIEW;

-- list view
postgres=# \dv
postgres=# select table_name from INFORMATION_SCHEMA.views;
postgres=# select viewname from pg_catalog.pg_views;

-- drop view
postgres=# DROP VIEW COMPANY_VIEW;
```


### transaction

```sql
-- rollback
postgres=# BEGIN;
postgres=# DELETE FROM COMPANY WHERE AGE = 25;
postgres=# ROLLBACK;

-- commit
postgres=# BEGIN;
postgres=# DELETE FROM COMPANY WHERE AGE = 25;
postgres=# COMMIT;
```


### subquery

```sql
postgres=# CREATE TABLE COMPANY_BKP(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL,
   JOIN_DATE      DATE
);

-- copy COMPANY to COMPANY_BKP
postgres=# INSERT INTO COMPANY_BKP SELECT * FROM COMPANY WHERE ID
   IN (SELECT ID FROM COMPANY) ;

postgres=# UPDATE COMPANY_BKP SET SALARY = SALARY * 0.50 WHERE AGE
   IN (SELECT AGE FROM COMPANY WHERE AGE >= 27);
```


### autoincrememt

```sql
postgres=# CREATE TABLE COMPANY_NEW(
   ID             SERIAL PRIMARY KEY,   -- autoincrememt
   NAME           TEXT      NOT NULL,
   AGE            INT       NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);

postgres=# INSERT INTO COMPANY_NEW (NAME,AGE,ADDRESS,SALARY)
   VALUES ( 'Paul', 32, 'California', 20000.00),
   ('Allen', 25, 'Texas', 15000.00),
   ('Teddy', 23, 'Norway', 20000.00),
   ('Mark', 25, 'Rich-Mond ', 65000.00),
   ('David', 27, 'Texas', 85000.00),
   ('Kim', 22, 'South-Hall', 45000.00),
   ('James', 24, 'Houston', 10000.00);
```


### explain

```sql
postgres=# EXPLAIN SELECT * FROM COMPANY WHERE Salary >= 20000;
postgres=# EXPLAIN ANALYZE SELECT * FROM COMPANY WHERE Salary >= 20000;
postgres=# EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM COMPANY WHERE Salary >= 20000;
```


---

## ref

[tutorialspoint](http://www.tutorialspoint.com/index.htm)

[W3Schools.com](http://www.w3schools.com/sql/default.asp)

[PostgreSQL 8.0.0 中文文件](http://twpug.net/docs/postgresql-doc-8.0-zh_TW/index.html)
