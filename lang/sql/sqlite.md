# SQLite

## install

```bash
linux:~ # dnf install sqlite
```


---

## basic

```bash
linux:~ # sqlite3
linux:~ # sqlite3 db.sqlite3
```

```sql
sqlite> .help                     -- help
sqlite> .databases                -- show database
sqlite> .tables [<table_name>]    -- show table
sqlite> .schema [<table_name>]    -- show schema
sqlite> .show                     -- show config
sqlite> .quit
sqlite> .exit
```


---

## table


### create table

```sql
sqlite> CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);

sqlite> DROP TABLE IF EXISTS DEPARTMENT;
sqlite> CREATE TABLE DEPARTMENT(
   ID INT PRIMARY KEY      NOT NULL,
   DEPT           CHAR(50) NOT NULL,
   EMP_ID         INT      NOT NULL
);


-- show table
sqlite> .tables
sqlite> .tables company
sqlite> .tables comp%

-- show schema
sqlite> .schema
sqlite> .schema company
sqlite> .schema comp%
```

### alter table

```sql
-- reanme table
sqlite> ALTER TABLE COMPANY RENAME TO COMPANY_RENAME;
sqlite> .tables

-- add column
sqlite> ALTER TABLE COMPANY_RENAME ADD COLUMN SEX CHAR(1);

-- rename column
sqlite> ALTER TABLE COMPANY_RENAME RENAME COLUMN SEX TO SEX_RENAME;
sqlite> .schema COMPANY_RENAME 

-- drop column
PRAGMA foreign_keys=off;
BEGIN TRANSACTION;
CREATE TABLE COMPANY(
   ID INTEGER PRIMARY KEY AUTOINCREMENT,
   NAME           TEXT     NOT NULL,
   AGE            INT      DEFAULT 20,
   ADDRESS        CHAR(50) NOT NULL,
   SALARY         REAL     CHECK(SALARY > 0)
);
INSERT INTO COMPANY (ID, NAME, AGE, ADDRESS, SALARY)
  SELECT ID, NAME, AGE, ADDRESS, SALARY
  FROM COMPANY_RENAME;
COMMIT;
PRAGMA foreign_keys=on;
```


### drop table

```sql
sqlite> DROP TABLE COMPANY;
sqlite> .tables
```


---

## row

### insert into

```sql
sqlite> INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
   VALUES (1, 'Paul', 32, 'California', 20000.00);
sqlite> INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
   VALUES (2, 'Allen', 25, 'Texas', 15000.00),
   (3, 'Teddy', 23, 'Norway', 20000.00),
   (4, 'Mark', 25, 'Rich-Mond ', 65000.00),
   (5, 'David', 27, 'Texas', 85000.00),
   (6, 'Kim', 22, 'South-Hall', 45000.00);
sqlite> INSERT INTO COMPANY
   VALUES (7, 'James', 24, 'Houston', 10000.00),
   (8, 'Paul', 24, 'Houston', 20000.00 ),
   (9, 'James', 44, 'Norway', 5000.00 ),
   (10, 'James', 45, 'Texas', 5000.00 );

sqlite> INSERT INTO DEPARTMENT (ID, DEPT, EMP_ID)
   VALUES (1, 'IT Billing', 1 ),
   (2, 'Engineering', 2 ),
   (3, 'Finance', 7 );
```


### select

```sql
sqlite> .header on
sqlite> .mode column
sqlite> SELECT * FROM COMPANY;
sqlite> SELECT NAME, AGE FROM COMPANY;

sqlite> .header on
sqlite> .mode column
sqlite> .width on
sqlite> .width 10, 20, 10
sqlite> SELECT * FROM COMPANY;

-- shema
sqlite> SELECT tbl_name FROM sqlite_master WHERE type = 'table';
sqlite> SELECT sql FROM sqlite_master WHERE type = 'table' AND tbl_name = 'COMPANY';
```


### operator

```sql
-- arithmetic operator
sqlite> .mode line
sqlite> SELECT 10 + 20;
sqlite> SELECT 10 - 20;
sqlite> SELECT 10 * 20;
sqlite> SELECT 10 / 5;
sqlite> SELECT 12 % 5;

-- bitwise operator
sqlite> .mode line
sqlite> SELECT 60 | 13;
sqlite> SELECT 60 & 13;
sqlite> SELECT (~60);
sqlite> SELECT (60 << 2);
sqlite> SELECT (60 >> 2);

-- comparison operator
sqlite> .mode column
sqlite> SELECT * FROM COMPANY WHERE SALARY > 50000;
sqlite> SELECT * FROM COMPANY WHERE SALARY = 20000;
sqlite> SELECT * FROM COMPANY WHERE SALARY != 20000;
sqlite> SELECT * FROM COMPANY WHERE SALARY <> 20000;
sqlite> SELECT * FROM COMPANY WHERE SALARY >= 65000;
sqlite> SELECT * FROM COMPANY WHERE SALARY !> 65000;

-- logical operator
sqlite> .mode column
sqlite> SELECT * FROM COMPANY WHERE AGE >= 25 AND SALARY >= 65000;
sqlite> SELECT * FROM COMPANY WHERE AGE >= 25 OR SALARY >= 65000;
sqlite> SELECT * FROM COMPANY WHERE AGE IS NOT NULL;
sqlite> SELECT * FROM COMPANY WHERE NAME LIKE 'Ki%';  -- case in-sensitive
sqlite> SELECT * FROM COMPANY WHERE NAME GLOB 'Ki*';  -- case sensitive
sqlite> SELECT * FROM COMPANY WHERE AGE IN ( 25, 27 );
sqlite> SELECT * FROM COMPANY WHERE AGE NOT IN ( 25, 27 );
sqlite> SELECT * FROM COMPANY WHERE AGE BETWEEN 25 AND 27;
sqlite> SELECT AGE FROM COMPANY 
   WHERE EXISTS (SELECT AGE FROM COMPANY WHERE SALARY > 65000);
sqlite> SELECT * FROM COMPANY 
   WHERE AGE > (SELECT AGE FROM COMPANY WHERE SALARY > 65000);
```


### expression

```sql
sqlite> .mode column
sqlite> SELECT * FROM COMPANY WHERE SALARY = 10000;

sqlite> .mode line
sqlite> SELECT (15 + 6) AS ADDITION;
sqlite> SELECT COUNT(*) AS "RECORDS" FROM COMPANY;
sqlite> SELECT CURRENT_TIMESTAMP;
sqlite> SELECT DATETIME('now','localtime');
```


### where

```sql
-- and, or
sqlite> SELECT * FROM COMPANY WHERE AGE >= 25 AND SALARY >= 65000;
sqlite> SELECT * FROM COMPANY WHERE AGE >= 25 OR SALARY >= 65000;

sqlite> SELECT * FROM COMPANY WHERE AGE IS NOT NULL;

-- like
sqlite> SELECT * FROM COMPANY WHERE NAME LIKE 'Ki%';

-- %, _
sqlite> SELECT * FROM COMPANY WHERE AGE LIKE '%2';
sqlite> SELECT * FROM COMPANY WHERE AGE LIKE '_2';
sqlite> SELECT * FROM COMPANY WHERE ADDRESS LIKE '%-%';
sqlite> SELECT * FROM COMPANY WHERE ADDRESS NOT LIKE '%-%';
sqlite> SELECT * FROM COMPANY WHERE ADDRESS LIKE '____-%';

-- glob
sqlite> SELECT * FROM COMPANY WHERE NAME GLOB 'Ki*';

-- *, ?
sqlite> SELECT * FROM COMPANY WHERE AGE GLOB '2*';
sqlite> SELECT * FROM COMPANY WHERE AGE GLOB '2?';
sqlite> SELECT * FROM COMPANY WHERE ADDRESS GLOB '*-*';
sqlite> SELECT * FROM COMPANY WHERE ADDRESS GLOB '????-*';

-- in, between
sqlite> SELECT * FROM COMPANY WHERE AGE IN (25, 27);
sqlite> SELECT * FROM COMPANY WHERE AGE NOT IN (25, 27);
sqlite> SELECT * FROM COMPANY WHERE AGE BETWEEN 25 AND 27;

-- limit, offset
sqlite> SELECT * FROM COMPANY LIMIT 2;
sqlite> SELECT * FROM COMPANY LIMIT 2 OFFSET 3;

-- order by ... asc|desc
sqlite> SELECT * FROM COMPANY ORDER BY SALARY ASC;
sqlite> SELECT * FROM COMPANY ORDER BY NAME DESC, SALARY ASC;

-- group by
sqlite> SELECT NAME, SUM(SALARY), COUNT(*), AVG(SALARY)
   FROM COMPANY GROUP BY NAME ORDER BY NAME;

-- having
sqlite> SELECT * FROM COMPANY GROUP BY name HAVING count(name) > 1;

-- distinct
sqlite> SELECT name FROM COMPANY;
sqlite> SELECT DISTINCT name FROM COMPANY;

-- sub-where
sqlite> SELECT AGE FROM COMPANY 
   WHERE EXISTS (SELECT AGE FROM COMPANY WHERE SALARY > 65000);
sqlite> SELECT * FROM COMPANY 
   WHERE AGE > (SELECT AGE FROM COMPANY WHERE SALARY > 65000);

```


### update

```sql
sqlite> UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6;
sqlite> UPDATE COMPANY SET ADDRESS = 'Texas', SALARY = 20000.00;
```


### delete

```sql
sqlite> DELETE FROM COMPANY WHERE ID = 7;
sqlite> DELETE FROM COMPANY;
```


---

## advanced


### constraint

```sql
sqlite> CREATE TABLE CONSTRAINT_COMPANY(
   ID INT PRIMARY KEY      NOT NULL,           -- primary key
   NAME           TEXT     NOT NULL UNIQUE,    -- unique
   AGE            INT      DEFAULT 20,         -- default
   ADDRESS        CHAR(50) NOT NULL,           -- not null
   SALARY         REAL     CHECK(SALARY > 0)   -- check
);
```


### join

```sql
-- cross join
sqlite> SELECT EMP_ID, NAME, DEPT FROM COMPANY CROSS JOIN DEPARTMENT;

-- inner join
sqlite> SELECT EMP_ID, NAME, DEPT FROM COMPANY INNER JOIN DEPARTMENT
   ON COMPANY.ID = DEPARTMENT.EMP_ID;

-- outer join
sqlite> SELECT EMP_ID, NAME, DEPT FROM COMPANY LEFT OUTER JOIN DEPARTMENT
   ON COMPANY.ID = DEPARTMENT.EMP_ID;
```


### union

```sql
sqlite> SELECT EMP_ID, NAME, DEPT FROM COMPANY INNER JOIN DEPARTMENT
   ON COMPANY.ID = DEPARTMENT.EMP_ID;
sqlite> SELECT EMP_ID, NAME, DEPT FROM COMPANY LEFT OUTER JOIN DEPARTMENT
   ON COMPANY.ID = DEPARTMENT.EMP_ID;

-- union
sqlite> SELECT EMP_ID, NAME, DEPT FROM COMPANY INNER JOIN DEPARTMENT
     ON COMPANY.ID = DEPARTMENT.EMP_ID
   UNION
   SELECT EMP_ID, NAME, DEPT FROM COMPANY LEFT OUTER JOIN DEPARTMENT
     ON COMPANY.ID = DEPARTMENT.EMP_ID;

-- union all
sqlite> SELECT EMP_ID, NAME, DEPT FROM COMPANY INNER JOIN DEPARTMENT
     ON COMPANY.ID = DEPARTMENT.EMP_ID
   UNION ALL
   SELECT EMP_ID, NAME, DEPT FROM COMPANY LEFT OUTER JOIN DEPARTMENT
     ON COMPANY.ID = DEPARTMENT.EMP_ID;
```


### as

```sql
-- table as ...
sqlite> SELECT C.ID, C.NAME, C.AGE, D.DEPT
   FROM COMPANY AS C, DEPARTMENT AS D
   WHERE  C.ID = D.EMP_ID;

-- column as ...
sqlite> SELECT C.ID AS COMPANY_ID, C.NAME AS COMPANY_NAME, C.AGE, D.DEPT
   FROM COMPANY AS C, DEPARTMENT AS D
   WHERE C.ID = D.EMP_ID;
```


### trigger

```sql
sqlite> CREATE TABLE AUDIT(
   EMP_ID INT NOT NULL,
   ENTRY_DATE TEXT NOT NULL
);

-- create trigger
sqlite> CREATE TRIGGER AUDIT_TRIGGER AFTER INSERT 
ON COMPANY
BEGIN
   INSERT INTO AUDIT(EMP_ID, ENTRY_DATE) VALUES (NEW.ID, datetime('now'));  -- new, old
END;

sqlite> INSERT INTO COMPANY VALUES (11, 'Watson', 50, 'Alabama', 15000.00 );
sqlite> SELECT * FROM AUDIT;

-- select trigger
sqlite> SELECT name FROM sqlite_master WHERE type = 'trigger';
sqlite> SELECT name FROM sqlite_master WHERE type = 'trigger' AND tbl_name = 'COMPANY';

-- drop trigger
sqlite> DROP TRIGGER AUDIT_TRIGGER;
```


### index

```sql
-- create index
sqlite> CREATE INDEX SALARY_INDEX ON COMPANY (SALARY);

sqlite> .indices COMPANY
sqlite> SELECT * FROM COMPANY WHERE SALARY % 3 = 0;

-- select index
sqlite> SELECT * FROM sqlite_master WHERE type = 'index';

-- drop index
sqlite> DROP INDEX SALARY_INDEX;
```


### view

```sql
-- create view
sqlite> CREATE VIEW COMPANY_VIEW AS
   SELECT ID, NAME, AGE
   FROM  COMPANY;

sqlite> SELECT * FROM COMPANY_VIEW;

-- select view
sqlite> SELECT * FROM sqlite_master WHERE type = 'view';

-- drop view
sqlite> DROP VIEW COMPANY_VIEW;
```


### transaction

```sql
-- rollback
sqlite> BEGIN;
sqlite> DELETE FROM COMPANY WHERE AGE = 25;
sqlite> ROLLBACK;

-- commit
sqlite> BEGIN;
sqlite> DELETE FROM COMPANY WHERE AGE = 25;
sqlite> COMMIT;
```


### subquery

```sql
sqlite> SELECT * FROM COMPANY WHERE ID
   IN (SELECT ID FROM COMPANY WHERE SALARY > 45000) ;

sqlite> CREATE TABLE COMPANY_BKP(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);

sqlite> INSERT INTO COMPANY_BKP SELECT * FROM COMPANY WHERE ID
   IN (SELECT ID FROM COMPANY) ;

sqlite> UPDATE COMPANY_BKP SET SALARY = SALARY * 0.50 WHERE AGE
   IN (SELECT AGE FROM COMPANY WHERE AGE >= 27);
```


### autoincrememt

```sql
sqlite> CREATE TABLE COMPANY_NEW(
   ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- autoincrememt
   NAME           TEXT     NOT NULL,
   AGE            INT      DEFAULT 20,
   ADDRESS        CHAR(50) NOT NULL,
   SALARY         REAL     CHECK(SALARY > 0)
);

sqlite> INSERT INTO COMPANY_NEW (NAME, AGE, ADDRESS, SALARY)
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
sqlite> SELECT * FROM COMPANY WHERE SALARY >= 20000;

-- explain
sqlite> EXPLAIN SELECT * FROM COMPANY WHERE SALARY >= 20000;

-- explain query plan
sqlite> EXPLAIN QUERY PLAN SELECT * FROM COMPANY WHERE Salary >= 20000;
```


---

## database

### dump

```bash
linux:~ # sqlite3 db.sqlite3 .dump > db.sql    # backup
linux:~ # sqlite3 db.sqlite3 < db.sql          # restore
```


### attach

```sql
sqlite> ATTACH DATABASE 'new_db.sqlite3' AS 'new_db'
sqlite> .databases
sqlite> .tables
```


### detach

```sql
sqlite> DETACH DATABASE new_db
sqlite> .databases
```


### vacuum

```sql
-- manual vacuum
sqlite> VACUUM;

-- auto vacuum
sqlite> PRAGMA auto_vacuum = FULL;          -- enable full
sqlite> PRAGMA auto_vacuum = INCREMENTAL;   -- enable incremental
sqlite> PRAGMA auto_vacuum = NONE;          -- disable
```

```bash
linux:~ # sqlite3 db.sqlite3 "VACUUM;"
```
