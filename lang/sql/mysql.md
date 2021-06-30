# MySQL


## install

```bash
linux:~ # yum install mariadb
```

```sql
mysql> SHOW DATABASES;                       -- list database
mysql> SHOW TABLES;                          -- list table
mysql> USE <database_name>                   -- use database
mysql> SHOW COLUMNS FROM <table_name>;
mysql> SHOW INDEX FROM <table_name>;
mysql> SHOW TABLE STATUS LIKE <table_name>;
```


---

## account

```sql
mysql> INSERT INTO user (host, user, password, select_priv, insert_priv, update_priv) 
  VALUES ('localhost', 'guest', PASSWORD('guest123'), 'Y', 'Y', 'Y');
mysql> FLUSH PRIVILEGES;
mysql> SELECT host, user, password FROM user WHERE user = 'guest';
```


---

## run


```bash
linux:~ # cat run.sh
#!/bin/sh

HOST="node-1.domain.tld"

mysql -u root << EOF
USE nova;
SELECT id, created_at, updated_at, hypervisor_hostname FROM compute_nodes;
-- SELECT id, created_at, updated_at, host FROM services;
SELECT id, created_at, updated_at, host FROM services WHERE host = "$HOST";
EOF

linux:~ # ./run.sh
```


---

## database

```sql
mysql> CREATE DATABASE <database_name>;   -- create database
mysql> DROP DATABASE <database_name>;     -- delete database
mysql> SHOW DATABASES;                    -- list database
mysql> USE <database_name>;               -- use database

-- example
mysql> CREATE DATABASE tutorials_db;
mysql> USE tutorials_db;
```


---

## table

```sql
mysql> CREATE TABLE <table_name> (<column_name> <data_type>);        -- create table
mysql> DROP TABLE <table_name>;                                      -- delete table
mysql> SHOW TABLES;                                                  -- list table
mysql> DESCRIBE <table_name>;                                        -- show schema

-- example
mysql> CREATE TABLE tutorials_tbl(
  tutorial_id INT NOT NULL AUTO_INCREMENT,
  tutorial_title VARCHAR(100) NOT NULL,
  tutorial_author VARCHAR(40) NOT NULL,
  submission_date DATE,
  PRIMARY KEY (tutorial_id)
);
mysql> DROP TABLE tutorials_tbl
```


---

## row

### create / add

```sql
mysql> INSERT INTO <table_name> (<column1>, <column2>, ... <columnN>)  -- add row
  VALUES (<value1>, <value2>, ... <valueN>);

-- example
mysql> INSERT INTO tutorials_tbl (tutorial_title, tutorial_author, submission_date)
  VALUES ("Learn PHP", "John", NOW()),
  ("Learn MySQL", "Mary", NOW()),
  ("JAVA Tutorial", "Joe", '2020-01-01');
  ("SQL Tutorial", "John", NOW());
```


### read / query

```sql
mysql> SELECT <column1>, <column2>, ... <columnN> FROM <table1>, <table2>...
  [WHERE Clause]
  [OFFSET M ][LIMIT N]

mysql>  SELECT ...
  FROM ...
  WHERE ...
  GROUP BY ...
  HAVING ...
  ORDER BY ...


-- example
mysql> SELECT * FROM tutorials_tbl;
mysql> SELECT tutorial_author, tutorial_title FROM tutorials_tbl;

-- where
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_author = "john";
mysql> SELECT * FROM tutorials_tbl WHERE BINARY tutorial_author = "john";   -- case sensitive
mysql> SELECT * FROM tutorials_tbl WHERE submission_date <= '2020-12-31';

-- distinct
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_author = "john";
mysql> SELECT DISTINCT * FROM tutorials_tbl WHERE tutorial_author = "john";
mysql> SELECT tutorial_author FROM tutorials_tbl WHERE tutorial_author = "john";
mysql> SELECT DISTINCT tutorial_author FROM tutorials_tbl WHERE tutorial_author = "john";

-- like
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_author LIKE "jo";
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_author LIKE "jo%";

-- order by ... desc|asc
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_author ORDER BY tutorial_author DESC;
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_author LIKE "jo%" ORDER BY tutorial_author ASC;

-- group by ... having
mysql> SELECT tutorial_author FROM tutorials_tbl GROUP BY tutorial_author;
mysql> SELECT tutorial_author, Count(*), Max(tutorial_id), Min(tutorial_id), Sum(tutorial_id), Avg(tutorial_id)
  FROM tutorials_tbl
  GROUP BY tutorial_author;
mysql> SELECT tutorial_author, Count(*)
  FROM tutorials_tbl
  GROUP BY tutorial_author
  HAVING Count(*) >= 2;

-- and, or
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_title LIKE '%sql%' OR tutorial_author = 'john';
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_title LIKE '%sql%' AND tutorial_author = 'john';

-- in
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_author = 'john' OR tutorial_author = 'joe';
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_author IN ('john', 'joe');

-- between
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_id >= 2 AND tutorial_id <= 3;
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_id BETWEEN 2 AND 3;

-- regxp
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_author REGEXP "jo";
mysql> SELECT * FROM tutorials_tbl WHERE tutorial_author REGEXP "j.*n";
```


### update / modify


```sql
mysql> UPDATE <table_name> SET <column1> = <value1>, <column2> = <value2>, ... <columnN> = <valueN> 
  [WHERE Clause]

-- example
mysql> UPDATE tutorials_tbl SET tutorial_title = 'Learning JAVA' WHERE tutorial_id = 3;
```


### delete / remove

```sql
mysql> DELETE FROM table_name
  [WHERE Clause]

-- example
mysql> DELETE FROM tutorials_tbl WHERE tutorial_id = 3;
```


### join and union

```sql
-- example
mysql> CREATE TABLE tutorials_tbl(
  tutorial_id INT NOT NULL AUTO_INCREMENT,
  tutorial_title VARCHAR(100) NOT NULL,
  tutorial_author VARCHAR(40) NOT NULL,
  submission_date DATE,
  PRIMARY KEY (tutorial_id)
);

mysql> INSERT INTO tutorials_tbl (tutorial_title, tutorial_author, submission_date)
  VALUES
  ("Learn PHP", "John", NOW()),
  ("Learn MySQL", "Mary", NOW()),
  ("Learn JAVA", "Joe", NOW());


mysql> CREATE TABLE tcount_tbl(
  tutorial_author VARCHAR(40) NOT NULL,
  tutorial_count INT
);

mysql> INSERT INTO tcount_tbl (tutorial_author, tutorial_count)
  VALUES
  ('John', 10),
  ('Gill', NULL),
  ('Mary', 20),
  ('Joe', 30);

-- union like full join but not null
mysql> SELECT * FROM tcount_tbl, tutorials_tbl;

-- join same as inner join
mysql> SELECT * FROM tcount_tbl, tutorials_tbl
  WHERE tcount_tbl.tutorial_author = tutorials_tbl.tutorial_author; 
mysql> SELECT tutorials_tbl.tutorial_title, tutorials_tbl.tutorial_author 
  FROM tcount_tbl, tutorials_tbl
  WHERE tcount_tbl.tutorial_author = tutorials_tbl.tutorial_author;
mysql> SELECT b.tutorial_title, a.tutorial_author 
  FROM tcount_tbl a, tutorials_tbl b
  WHERE a.tutorial_author = b.tutorial_author;

-- inner join
mysql> SELECT b.tutorial_title, a.tutorial_author 
  FROM tcount_tbl a 
  INNER JOIN tutorials_tbl b
  ON a.tutorial_author = b.tutorial_author;

-- right join
mysql> SELECT b.tutorial_title, a.tutorial_author 
  FROM tcount_tbl a 
  RIGHT JOIN tutorials_tbl b
  ON a.tutorial_author = b.tutorial_author;

-- left join
mysql> SELECT b.tutorial_title, a.tutorial_author 
  FROM tcount_tbl a 
  LEFT JOIN tutorials_tbl b
  ON a.tutorial_author = b.tutorial_author;

-- full join
mysql> SELECT b.tutorial_title, a.tutorial_author 
  FROM tcount_tbl a 
  LEFT JOIN tutorials_tbl b
  ON a.tutorial_author = b.tutorial_author
  UNION
  SELECT b.tutorial_title, a.tutorial_author 
  FROM tcount_tbl a 
  RIGHT JOIN tutorials_tbl b
  ON a.tutorial_author = b.tutorial_author;
```
