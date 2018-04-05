# Postge SQL #


## Package ##

	linux:~ # yum install postgresql


## Service ##

	linux:~ # systemctl enable postgresql.service
	linux:~ # systemctl start postgresql.service

	# psql default port 5432
	linux:~ # netstat -luntp | grep 5432

	# config
	linux:~ # pg_config # show config
	linux:~ # ls /var/lib/pgsql/data # psql config & db folder
	linux:~ # cat /var/lib/pgsql/data/postgresql.conf # default config


## Concept ##

* DQL: Data Query Language

* DML: Data Manipulation Language

* DDL: Data Definition Language

SQL command (一般習慣使用大寫表示), table name 不分大小寫. Column 有分大小寫

## Basic ##

	# login
	linux:~ # su - postgres
	linux:~ $ psql

	linux:~ # psql -U username -d dbname -h host -p port -W

	postgres=# \h # help with SQL
	postgres=# \? # help with psql


### Databse 操作 ###

DDL

	# database usage:
	postgres=# CREATE DATABASE <db_name>;  # 新增 database
	postgres=# DROP DATABASE <db_name>;    # 刪除 database
	postgres=# \l                          # 顯示所有 database
	postgres=# \c <db_name>                # 使用 database

	# ie
	postgres=# CREATE DATABASE testdb;

	postgres=# \l

	postgres=# \c testdb                   # 當切換 database 後, 提示會變成該 database
	testdb=#

	postgres=# DROP DATABASE testdb;


### Table 操作 ###

DDL

	# table usage:
	postgres=# CREATE TABLE <table_name>(  # 新增 table
	   <column/field>      <data_type>,
	);

	postgres=# DROP TABLE <table_name>;    # 刪除 table

	postgres=# ALTER TABLE <table_name>    # 修改 table
	ADD|DROP|ALTER|RENAME <column> <data_type>;

	postgres=# \d [<table_name>]           # 顯示 table

	# ie
	postgres=# CREATE TABLE COMPANY(
	   ID INT PRIMARY KEY     NOT NULL,
	   NAME           TEXT    NOT NULL,
	   AGE            INT     NOT NULL,
	   ADDRESS        CHAR(50),
	   SALARY         REAL,
	   JOIN_DATE	  DATE
	);

	postgres=# ALTER TABLE company ADD JOIN_DATE DATE;
	postgres=# \d
	postgres=# \d COMPANY

	postgres=# DROP TABLE COMPANY;


### Record 操作 ###

DML

	# record usage:
	postgres=# INSERT INTO <table_name> [(<column>, ...)] # 新增 record
	VALUES (<value>, ...);
	
	postgres=# postgres=# UPDATE <table_name>             # 修改 record
	SET <column> = <value>, ...
	WHERE [condition];
	
	postgres=# DELETE FROM <table_name>                   # 刪除 record
	WHERE [<condition>];

	# ie
	postgres=# INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY,JOIN_DATE)
	VALUES (1, 'Paul', 32, 'California', 20000.00 ,'2001-07-13');
	postgres=# INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,JOIN_DATE)
	VALUES (2, 'Allen', 25, 'Texas', '2007-12-13');
	postgres=# INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY,JOIN_DATE)
	VALUES (3, 'Teddy', 23, 'Norway', 20000.00, DEFAULT );

	postgres=# UPDATE COMPANY SET SALARY = 15000 WHERE ID = 1;

	postgres=# DELETE FROM COMPANY WHERE ID = 3;


### Query 操作 ###

DQL

	# query usage:
	postgres=# SELECT *|<column>      # 查詢 record
	FROM <table_name>

	# ie
	postgres=# SELECT * FROM COMPANY;
	postgres=# SELECT name, age FROM COMPANY;


## Ref ##

[tutorialspoint](http://www.tutorialspoint.com/index.htm)

[W3Schools.com](http://www.w3schools.com/sql/default.asp)

[PostgreSQL 8.0.0 中文文件](http://twpug.net/docs/postgresql-doc-8.0-zh_TW/index.html)
