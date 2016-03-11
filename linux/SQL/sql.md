# Basic


## Connect

```
```

## Help

```
# for PostgreSQL
\h # help with SQL
\? # help with PSQL

# for SQLite
.help
```


## Script

```
# for PostgreSQL
\i xxx.psql
```


## Shell

```
# for PostgreSQL
\! ls
```


----


# Database


## Create Database

```
# for PostgreSQL
CREATE DATABASE testdb;
```


## Delete Database

```
# for PostgreSQL
DROP DATABASE testdb;
```


## Show All Database

```
# for PostgreSQL
\l
```


## Show Current Database

```
# for PostgreSQL
\c
```


## Use Database

```
# for PostgreSQL
\c testdb
```

----


# Table


## Create Table

```
CREATE TABLE CUSTOMERS(
  ID   INT              NOT NULL,
  NAME VARCHAR (20)     NOT NULL,
  AGE  INT              NOT NULL,
  ADDRESS  CHAR (25) ,
  SALARY   DECIMAL (18, 2),       
  PRIMARY KEY (ID)
);
```

## Delete Table

```
DROP TABLE CUSTOMERS;
```

## Show Table

```
# for PostgreSQL
\d

# for SQLite
.table
```

## Show Table Schema

```
# for PostgreSQL
\d CUSTOMERS

# for SQLite
.schema CUSTOMERS
```

----


# Query


## Create Query

```
INSERT INTO CUSTOMERS (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (1, 'Ramesh', 32, 'Ahmedabad', 2000.00 );

INSERT INTO CUSTOMERS (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (2, 'Khilan', 25, 'Delhi', 1500.00 );

INSERT INTO CUSTOMERS (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (3, 'kaushik', 23, 'Kota', 2000.00 );

INSERT INTO CUSTOMERS (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (4, 'Chaitali', 25, 'Mumbai', 6500.00 );

INSERT INTO CUSTOMERS (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (5, 'Hardik', 27, 'Bhopal', 8500.00 );

INSERT INTO CUSTOMERS (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (6, 'Komal', 22, 'MP', 4500.00 );
```

## Delete Query

```
DELETE FROM CUSTOMERS;
DELETE FROM CUSTOMERS WHERE ID = 6;
```

## Update Query

```
UPDATE CUSTOMERS SET ADDRESS = 'Pune' WHERE ID = 6;
```


## Selete Query

```
SELECT * FROM CUSTOMERS;
SELECT ID, NAME, SALARY FROM CUSTOMERS;
SELECT ID, NAME, SALARY FROM CUSTOMERS WHERE SALARY > 2000;
SELECT ID, NAME, SALARY FROM CUSTOMERS WHERE NAME = 'Hardik';
SELECT ID, NAME, SALARY FROM CUSTOMERS WHERE NAME LIKE '%m%';

SELECT ID, NAME, SALARY FROM CUSTOMERS WHERE SALARY > 2000 AND age < 25;
SELECT ID, NAME, SALARY FROM CUSTOMERS WHERE SALARY > 2000 OR age < 25;

SELECT * FROM CUSTOMERS LIMIT 3;
SELECT * FROM customers ORDER BY age DESC, salary ASC;
```