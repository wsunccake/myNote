# Basic


## Connect

```bash
# for PostgreSQL
linux:~ # psql -U postgre [-h localhost] [-p 5432] [-d postgres]

# for MariaDB
linux:~ # mysql -u root [-h localhost] [-P 3306] [-p]

# for SQLite
linux:~ # sqlite3 db.sqlite3
```

## Help

```sql
-- for PostgreSQL
\h # help with SQL
\? # help with PSQL

-- for MariaDB
\?
\h
help;

-- for SQLite
.help
```


## Script

```sql
-- for PostgreSQL
\i xxx.psql
```


## Shell

```sql
-- for PostgreSQL
\! ls
```

## Expression

```sql
SELECT (15 + 6) AS ADDITION;
SELECT CURRENT_TIMESTAMP;
```

----


# Database


## Create Database

```sql
-- for PostgreSQL
CREATE DATABASE testdb;
```


## Delete Database

```sql
-- for PostgreSQL
DROP DATABASE testdb;
```


## Show All Database

```sql
-- for PostgreSQL
\l
SELECT datname FROM pg_database;

-- for MariaDB
show databases;
```


## Show Current Database

```sql
-- for PostgreSQL
\c
```


## Use Database

```sql
-- for PostgreSQL
\c testdb
```

----


# Table


## Create Table

```sql
CREATE TABLE company(
  id   INT              NOT NULL,
  name VARCHAR (20)     NOT NULL,
  age  INT              NOT NULL,
  address  CHAR (25) ,
  salary   DECIMAL (18, 2),       
  PRIMARY KEY (id)
);
```

## Delete Table

```sql
DROP TABLE company;
```

## Show Table

```sql
-- for PostgreSQL
\d

-- for SQLite
.table
```

## Show Table Schema

```sql
-- for PostgreSQL
\d company

-- for SQLite
.schema company
```

----


# Record


## Create Record

```sql
INSERT INTO company (id, name, age, address, salary)
VALUES (1, 'Ramesh', 32, 'Ahmedabad', 2000.00 );

INSERT INTO company (id, name, age, address, salary)
VALUES (2, 'Khilan', 25, 'Delhi', 1500.00 );

INSERT INTO company (id, name, age, address, salary)
VALUES (3, 'Kaushik', 23, 'Kota', 2000.00 ),
(4, 'Chaitali', 25, 'Mumbai', 6500.00 ),
(5, 'Hardik', 27, 'Bhopal', 8500.00 ),
(6, 'Komal', 22, 'MP', 4500.00 ),
(7, 'Paul', 23, 'Kota', 7000.00 ),
(8, 'James', 25, 'Norway', 7000.00 ),
(9, 'James', 45, 'Houston', 7000.00 ),
```

## Delete Record

```sql
DELETE FROM company;
DELETE FROM company WHERE id = 6;
```

## Update Record

```sql
UPDATE company SET address = 'Pune' WHERE id = 6;
```


## Selete Record

```sql
SELECT * FROM company;
SELECT name, salary FROM company;
SELECT DISTINCT address FROM company;

SELECT name, salary FROM company WHERE salary > 2000;
SELECT name, salary FROM company WHERE name = 'Hardik';
SELECT name, salary FROM company WHERE name LIKE '%ik';
SELECT name, salary FROM company WHERE name LIKE '_a%';
SELECT name, salary FROM company WHERE salary > 2000 AND age < 25;
SELECT name, salary FROM company WHERE salary > 2000 OR age < 25;

SELECT * FROM company LIMIT 3;
SELECT * FROM company ORDER BY age DESC, salary ASC;
```

----


# SQL Function


## Aggregate

```sql
-- max, min, sum, count, avg
SELECT max(salary), min(salary), sum(salary), count(salary), avg(salary) FROM company;

-- GROUP BY
SELECT address, count(name), avg(salary) FROM company GROUP BY address;
SELECT address, count(name), avg(salary) FROM company GROUP BY address HAVING count(name) >= 2;
```

## String

```sql
-- 字串連結 concat 或 ||
SELECT concat(name, ' is ', age) FROM customers;
SELECT name || ' is ' || age FROM customers;

-- 字串長度 length 或 len
SELECT length(name) FROM customers;
SELECT len(name) FROM customers;

-- 字串
SELECT name, substring(name, 0, 3) FROM customers;
SELECT name, substring(name from 0 for 3) FROM customers;


-- 大小寫轉換, upper 或 lower
SELECT upper(name), lower(name) FROM customers;
```

## Mathematical


----


# SQL Advanced 