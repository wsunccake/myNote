# Basic


## Connect

```
# for PostgreSQL
Linux:~ # psql -U postgre [-h localhost] [-p 5432] [-d postgres]

# for SQLite
Linux:~ # sqlite3 db.sqlite3
```

## Help

```
-- for PostgreSQL
\h # help with SQL
\? # help with PSQL

-- for SQLite
.help
```


## Script

```
-- for PostgreSQL
\i xxx.psql
```


## Shell

```
-- for PostgreSQL
\! ls
```

## Expression
```
SELECT (15 + 6) AS ADDITION;
SELECT CURRENT_TIMESTAMP;
```

----


# Database


## Create Database

```
-- for PostgreSQL
CREATE DATABASE testdb;
```


## Delete Database

```
-- for PostgreSQL
DROP DATABASE testdb;
```


## Show All Database

```
-- for PostgreSQL
\l
SELECT datname FROM pg_database;
```


## Show Current Database

```
-- for PostgreSQL
\c
```


## Use Database

```
-- for PostgreSQL
\c testdb
```

----


# Table


## Create Table

```
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

```
DROP TABLE company;
```

## Show Table

```
-- for PostgreSQL
\d

-- for SQLite
.table
```

## Show Table Schema

```
-- for PostgreSQL
\d company

-- for SQLite
.schema company
```

----


# Record


## Create Record

```
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

```
DELETE FROM company;
DELETE FROM company WHERE id = 6;
```

## Update Record

```
UPDATE company SET address = 'Pune' WHERE id = 6;
```


## Selete Record

```
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

```
-- max, min, sum, count, avg
SELECT max(salary), min(salary), sum(salary), count(salary), avg(salary) FROM company;

-- GROUP BY
SELECT address, count(name), avg(salary) FROM company GROUP BY address;
SELECT address, count(name), avg(salary) FROM company GROUP BY address HAVING count(name) >= 2;
```

## String

```
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