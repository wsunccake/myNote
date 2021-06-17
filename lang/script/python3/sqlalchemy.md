# sqlalchemy

## install

```bash
linux:~ # pip install sqlalchemy  # 1.4+
```


---

## connect database

```python
from sqlalchemy import create_engine

# dialect[+driver]://user:password@host/dbname                            # syntax
engine = create_engine('sqlite:///college.db', echo=True)                 # for sqlite
engine = create_engine("mysql://user:pwd@localhost/college", echo=True)   # for mysql
```


---

## create table

```python
from sqlalchemy import Table, Column, Integer, String, MetaData
meta = MetaData()

students = Table(
    'students',
    meta,
    Column('id', Integer, primary_key = True),
    Column('name', String)
)

meta.create_all(engine)
```

-->

```sql
CREATE TABLE students (
        id INTEGER NOT NULL,
        name VARCHAR,
        PRIMARY KEY (id)
);
```

```python
from sqlalchemy inspect
from sqlalchemy import Table, Column, Integer, String, MetaData

table_name = 'students'
insp = inspect(engine)
meta = MetaData(engine)
students = Table(
    table_name,
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String)
)

if not insp.has_table(table_name):
    meta.create_all(engine)

print (engine.table_names())
```

-->

```sql
CREATE TABLE IF NOT EXISTS students (
        id INTEGER NOT NULL,
        name VARCHAR,
        PRIMARY KEY (id)
);
```


---

## sql expression

```python
ins_stmt = students.insert().values(name='Karan')

str(ins_stmt)
print(ins_stmt)
print(ins_stmt.compile().params)
```

---

## execute

```python
from sqlalchemy import create_engine, inspect
from sqlalchemy import Table, Column, Integer, String, MetaData

engine = create_engine('sqlite:///college.db', echo=True)
table_name = 'students'
insp = inspect(engine)
meta = MetaData(engine)
students = Table(
    table_name,
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String)
)

if not insp.has_table(table_name):
    meta.create_all(engine)

conn = engine.connect()

ins_stmt = students.insert().values(name='Karan')
result = conn.execute(ins_stmt)

conn.execute(students.insert(), [
    {'name': 'Rajiv'},
    {'name': 'Komal'},
    {'name': 'Abdul'},
    {'name': 'Priya'}
])
```


---

## select

```python
# selet statement
sel_stmt = students.select()
print(sel_stmt)

# fetchone method
result = conn.execute(sel_stmt)
row = result.fetchone())
print("id:", row._mapping[students.c.id], "; name:", row._mapping[students.c.name])
print("id:", row[0], "; name:", row[1])

print(result.fetchone())

# for loop 
result = conn.execute(sel_stmt)
for row in result:
    print (row, "id:", row._mapping[students.c.id], "; name:", row._mapping[students.c.name])

# with where statement
sel_stmt = students.select().where(students.c.name == "Rajiv")
result = conn.execute(sel_stmt)

for row in result:
    print (row)
```

```python
# table
from sqlalchemy import select

sel_stmt = select([students])
print(conn.execute(sel_stmt).fetchone())
```


---

## textual sql

```python
from sqlalchemy import text

txt_stmt = text("SELECT * FROM students")
print(txt_stmt)

for row in connection.execute(txt_stmt):
    print(row)
```

```python
from sqlalchemy.sql import text

txt_stmt = text("SELECT students.name FROM students WHERE students.name BETWEEN :x AND :y")
print(txt_stmt)

for row in conn.execute(txt_stmt, x='A', y='L').fetchall():
    print(row)
```

```python
from sqlalchemy.sql import text

txt_stmt = text("SELECT students.name FROM students WHERE students.name BETWEEN :x AND :y")
txt_stmt = txt_stmt.bindparams(x='A', y='L')
print(txt_stmt)

for row in conn.execute(txt_stmt).fetchall():
    print(row)
```

```python
from sqlalchemy.sql import text, select

txt_stmt = select([text('students.name FROM students')]).where(text('students.name between :x and :y'))
print(txt_stmt)

for row in conn.execute(txt_stmt, x = 'A', y = 'L').fetchall():
    print (row)
```

```python
from sqlalchemy.sql import select, text
from sqlalchemy import and_

txt_stmt = select([text('students.name FROM students')]).where(
  and_(
    text('students.name between :x and :y'),
    text('students.id > :n')
  )
)
for row in conn.execute(txt_stmt, x='A', y='L', n=3).fetchall():
   print (row)
```


---

## ref

[SQL Expression Language Tutorial (1.x API)](https://docs.sqlalchemy.org/en/14/core/tutorial.html)

[SQLAlchemy Tutorial](https://www.tutorialspoint.com/sqlalchemy/index.htm)
