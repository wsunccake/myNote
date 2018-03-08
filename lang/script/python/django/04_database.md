# install django


----

## DataBase

### SQLite

```
centos:~ # sqlite3 db.sqlite3
sqlite3> .help    # help
sqlite3> .table   # show table
sqlite3> .schema  # show schema
sqlite3> .quit
```

GUI tool

[DB Browser for SQLite](http://sqlitebrowser.org/)

[SQLITE Tutorial](http://www.sqlitetutorial.net/)

### MySQL/MariaDB

```
centos:~ #
```


### PostgreSQL

```
centos:~ #
```


### Oracle

```
centos:~ #
```


### CRUD

```
sql> -- create table
CREATE TABLE person (
  id INT NOT NULL,
  name VARCHAR(20) NOT NULL,
  age INT,
  PRIMARY KEY(id)
);

sql> -- insert record / Create
INSERT INTO person (id, name, age)
VALUES (1, 'Ramesh', 10),
       (2, 'Khilan', 25),
       (3, 'Kaushik', 23);

sql> -- select record / Read
SELECT * FROM person;
SELECT * FROM person WHERE id = 1;
SELECT name FROM person WHERE name LIKE '%ik%';
SELECT name, age FROM person WHERE age < 18;

sql> -- update record / Update
UPDATE person SET age = 11 WHERE id = 1;

sql> -- delete record / Delete
DELETE FROM person WHERE id = 1;
```


### 1 - 1

```
sql>
CREATE TABLE id_card (
  id INT NOT NULL,
  number VARCHAR(20) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(id) REFERENCES person(id)
);

sql>
INSERT INTO id_card (id, number)
VALUES (1, 'A123'),
       (2, 'A234');
```


### 1 - M

```
sql>
CREATE TABLE phone (
  id INT NOT NULL,
  number VARCHAR(20) NOT NULL,
  PRIMARY KEY(id),
  person_id INT NOT NULL,
  FOREIGN KEY(person_id) REFERENCES person(id)
);

sql>
INSERT INTO phone (id, number, person_id)
VALUES (1, '123', 1),
       (2, '234', 2),
       (3, '567', 1);

sql>
SELECT p2.name, p1.number FROM phone p1, person p2 WHERE p1.person_id = p2.id;
```


### M - M

```
sql>
CREATE TABLE item (
  id INT NOT NULL,
  name VARCHAR(20) NOT NULL,  
  price DECIMAL NOT NULL,
  PRIMARY KEY(id)
);

sql>
INSERT INTO item (id, name, price)
VALUES (1, 'watch', 10),
       (2, 'glass', 5);

sql>
CREATE TABLE person_item (
  id INT NOT NULL,
  person_id INT NOT NULL,
  item_id INT NOT NULL,
  state VARCHAR(20) NOT NULL,
  FOREIGN KEY(person_id) REFERENCES person(id),
  FOREIGN KEY(item_id) REFERENCES item(id),
  PRIMARY KEY(id)
);

sql>
INSERT INTO person_item (id, person_id, item_id)
VALUES (1, 1, 1),
       (2, 1, 2),
       (3, 2, 1),
       (4, 3, 2);

sql>
CREATE VIEW order_list
AS SELECT p.name, i.name AS item, pi.state, pi.id AS 'order no'
FROM person_item pi, person p, item i
WHERE p.id = pi.person_id and i.id = pi.item_id;

sql>
SELECT * FROM order_list;
```
