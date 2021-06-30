# sqlalchemy - core

## install

```bash
# sqlalchemy 1.4+
linux:~ # pip install sqlalchemy

# for mysql
linux:~ # pip install pymysql
linux:~ # pip install cryptography

# for postgresql
linux:~ # pip install psycopg2
```


---

## connect database

```python
from sqlalchemy import create_engine

# dialect[+driver]://user:password@host/dbname                                          # syntax
engine = create_engine('sqlite:///<database>')                                          # for sqlite
engine = create_engine("mysql://<user>:<password>@<host>[:<port>]/<database>")          # for mysql
engine = create_engine('postgresql://<user>:<password>@<host>[:<port>]/<database>')     # for postgresql

engine = create_engine('sqlite:///college.db', echo=True)
engine = create_engine("mysql+pymysql://<user>:<pwd>@localhost/colleage", echo=True)
engine = create_engine('postgresql+psycopg2://<user>:<pwd>@localhost/colleage', echo=True) 
```

[Engine Configuration](https://docs.sqlalchemy.org/en/14/core/engines.html)


---

## create table

```python
from sqlalchemy import Table, Column, Integer, String, MetaData
meta = MetaData()

students = Table(
    'students',
    meta,
    Column('id', Integer, primary_key=True),
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
from sqlalchemy import inspect
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

for row in conn.execute(txt_stmt):
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

## alias

```python
from sqlalchemy.sql import alias, select

st = students.alias("a")
s = select([st]).where(st.c.id > 2)
print(s)

for row in conn.execute(s).fetchall():
    print(row)
```


---

## updte expression

```python
update_stmt = students.update().where(students.c.name == 'Khanna').values(name='Kapoor')
print(update_stmt)
conn.execute(update_stmt)

select_stmt = students.select()
for row in conn.execute(select_stmt).fetchall():
    print(row)
```

---

## delete expression

```python
delete_stmt = students.delete().where(students.c.id > 2)
print(delete_stmt)
conn.execute(delete_stmt)

select_stmt = students.select()
for row in conn.execute(select_stmt).fetchall():
    print(row)
```


---

## multiple table

```python
from sqlalchemy.sql import select
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

engine = create_engine('sqlite:///college.db', echo=True)
meta = MetaData()
conn = engine.connect()

students = Table(
    'students', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String)
)
meta.create_all(engine)

conn.execute(students.insert(), [
    {'name': 'Ravi'},
    {'name': 'Rajiv'},
    {'name': 'Komal'},
    {'name': 'Abdul'},
    {'name': 'Priya'},
])

addresses = Table(
    'addresses', meta,
    Column('id', Integer, primary_key=True),
    Column('st_id', Integer, ForeignKey('students.id'), nullable=False),
    Column('postal_add', String),
    Column('email_add', String)
)
meta.create_all(engine)

conn.execute(addresses.insert(), [
    {'st_id': 1, 'postal_add': 'Shivajinagar Pune', 'email_add': 'ravi@gmail.com'},
    {'st_id': 1, 'postal_add': 'ChurchGate Mumbai', 'email_add': 'kapoor@gmail.com'},
    {'st_id': 3, 'postal_add': 'Jubilee Hills Hyderabad', 'email_add': 'komal@gmail.com'},
    {'st_id': 5, 'postal_add': 'MG Road Bangaluru', 'email_add': 'as@yahoo.com'},
    {'st_id': 2, 'postal_add': 'Cannought Place new Delhi', 'email_add': 'admin@khanna.com'},
])

select_stmt = select([students, addresses]).where(students.c.id == addresses.c.st_id)
for row in conn.execute(select_stmt):
    print(row)
```

```sql
CREATE TABLE students (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        PRIMARY KEY (id)
)

CREATE TABLE addresses (
        id INTEGER NOT NULL, 
        st_id INTEGER NOT NULL, 
        postal_add VARCHAR, 
        email_add VARCHAR, 
        PRIMARY KEY (id), 
        FOREIGN KEY(st_id) REFERENCES students (id)
)
```


---

## multiple table update

```python
update_stmt = students\
    .update()\
    .values(name='xyz')\
    .where(students.c.id == addresses.c.id)
print(update_stmt)
conn.execute(update_stmt)   # backend not support sqlite
```

---

## multiple table delete

```python
delete_stmt = students\
    .delete()\
    .where(students.c.id == addresses.c.id)\
    .where(addresses.c.email_add.startswith('xyz%'))
conn.execute(delete_stmt)   # backend not support sqlite
```


---

## join

```python
from sqlalchemy import join
from sqlalchemy.sql import select

j = students.join(addresses, students.c.id == addresses.c.st_id)
and_stmt = select([students]).where(and_(students.c.name == 'Ravi', students.c.id <3))
join_stmt = select([students]).select_from(j)
print(join_stmt)
for row in conn.execute(join_stmt):
    print(row)
```


---

## conjunction

```python
from sqlalchemy import and_, or_
print(and_stmt)

or_stmt = select([students]).where(or_(students.c.name == 'Ravi', students.c.id <3))
print(or_stmt)

from sqlalchemy import asc, desc, between
asc_stmt = select([students]).order_by(asc(students.c.name))
print(asc_stmt)

desc_stmt = select([students]).order_by(desc(students.c.name))
print(desc_stmt)

between_stmt = select([students]).where(between(students.c.id,2,4))
print(between_stmt)
```


---

## function

```python
from sqlalchemy.sql import func

print(conn.execute(select([func.now()])).fetchone())

print(conn.execute(select([func.count(students.c.id)])).fetchone())

print(conn.execute(select([func.max(students.c.id)])).fetchone())

print(conn.execute(select([func.min(students.c.id)])).fetchone())

print(conn.execute(select([func.avg(students.c.id)])).fetchone())
```


---

## set operation

```python
from sqlalchemy import union, union_all, except_, intersect

union_stmt = union(
    addresses.select().where(addresses.c.email_add.like('%@gmail.com')), 
    addresses.select().where(addresses.c.email_add.like('%@yahoo.com'))
)
print(union_stmt)

union_all_stmt = union_all(
    addresses.select().where(addresses.c.email_add.like('%@gmail.com')),
    addresses.select().where(addresses.c.email_add.like('%@yahoo.com'))
)
print(union_all_stmt)

except_stmt = except_(
    addresses.select().where(addresses.c.email_add.like('%@gmail.com')),
    addresses.select().where(addresses.c.postal_add.like('%Pune'))
)
print(except_stmt)

intersect_stmt = intersect(
    addresses.select().where(addresses.c.email_add.like('%@gmail.com')),
    addresses.select().where(addresses.c.postal_add.like('%Pune'))
)
print(intersect_stmt)
```


---

## connection pool

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# connection pool
conn_num = 4
engine = create_engine('<dialect>+<driver>://<user>:<pwd>@<host>/<database>',
                       echo=False,
                       pool_size=conn_num,
                       max_overflow=0,
                       poolclass=QueuePool,
                       pool_pre_ping=True,
                       pool_use_lifo=True
                      )

conns = [engine.connect() for _ in range(conn_size)]
print(conns)
```


---

## lock

### sqlite

```python
def lock_update(engine, table_name, table_id, name):
    is_successful = False
    result = None

    with engine.connect().execution_options(autocommit=False) as conn:
        try:
            stmt = text("BEGIN EXCLUSIVE;")
            conn.execute(stmt)
        except Exception as e:
            return {'is_successful': is_successful, 'q': result}

        try:
            stmt = text(f"SELECT * FROM {table_name} WHERE id = {table_id};")
            q = conn.execute(stmt).fetchone()
            stmt = text(f"UPDATE {table_name} SET name = '{name}' WHERE id = {q.id};")
            conn.execute(stmt)

            stmt= text(f"SELECT * FROM {table_name} WHERE id = {q.id};")
            result = conn.execute(stmt).fetchone()
            stmt = text("COMMIT;")
            conn.execute(stmt)

            is_successful = True
        except:
            stmt = text("ROLLBACK;")
            conn.execute(stmt)

    return {'is_successful': is_successful, 'q': result}
```


### mysql

```python
def lock_update_fof_lock_table(engine, table_name, table_id, name):
    is_successful = False
    result = None

    with engine.connect().execution_options(autocommit=False) as conn:
        try:
            stmt = text(f'LOCK TABLES {table_name} WRITE;')
            conn.execute(stmt)
        except Exception as e:
            return {'is_successful': is_successful, 'q': result}

        try:
            stmt = text(f"SELECT * FROM {table_name} WHERE id = {table_id};")
            q = conn.execute(stmt).fetchone()
            stmt = text(f"UPDATE {table_name} SET name = '{name}' WHERE id = {q.id};")
            conn.execute(stmt)

            stmt= text(f"SELECT * FROM {table_name} WHERE id = {q.id};")
            result = conn.execute(stmt).fetchone()
            stmt = text("COMMIT;")
            conn.execute(stmt)

            is_successful = True
        except:
            stmt = text("ROLLBACK;")
            conn.execute(stmt)
        finally:
            stmt = text("UNLOCK TABLES;")
            conn.execute(stmt)
```

```python
def lock_update_for_nowait(engine, table_name, table_id, name):
    is_successful = False
    result = None

    with engine.connect().execution_options(autocommit=False) as conn:
        try:
            stmt = text('BEGIN;')
            conn.execute(stmt)

            stmt = text(f'SELECT * FROM {table_name} WHERE id = {table_id} FOR UPDATE NOWAIT;')
            q = conn.execute(stmt).fetchone()

            stmt = text(f"UPDATE {table_name} SET name = '{name}' WHERE id = {q.id};")
            conn.execute(stmt)

            stmt= text(f"SELECT * FROM {table_name} WHERE id = {q.id};")
            result = conn.execute(stmt).fetchone()

            stmt = text('COMMIT;')
            conn.execute(stmt)
        except Exception as e:
            print('fail')
            return {'is_successful': is_successful, 'q': result}
```


### postgresql


---

## ref

[SQL Expression Language Tutorial (1.x API)](https://docs.sqlalchemy.org/en/14/core/tutorial.html)

[SQLAlchemy Tutorial](https://www.tutorialspoint.com/sqlalchemy/index.htm)
