# sqlalchemy - orm

## declare mapping

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///sales.db', echo=True)
Base = declarative_base()

class Customers(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)

Base.metadata.create_all(engine)
```

```sql
CREATE TABLE customers (
        id INTEGER NOT NULL, 
        name VARCHAR, 
        address VARCHAR, 
        email VARCHAR, 
        PRIMARY KEY (id)
)
```

---

## session


```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind = engine)
session = Session()
```


---

## add object

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker

engine = create_engine('sqlite:///sales.db', echo=True)

Base = declarative_base()

class Customers(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)

Base.metadata.create_all(engine)


Session = sessionmaker(bind = engine)
session = Session()

c1 = Customers(name='Ravi Kumar', address='Station Road Nanded', email='ravi@gmail.com')
session.add(c1)
session.commit()

session.add_all([
    Customers(name='Komal Pande', address='Koti, Hyderabad', email='komal@gmail.com'), 
    Customers(name='Rajender Nath', address='Sector 40, Gurgaon', email='nath@gmail.com'), 
    Customers(name='S.M.Krishna', address='Budhwar Peth, Pune', email='smk@gmail.com')]
)

session.commit()
```


---

## query object


```python
q = session.query(Customers).all()
for row in q:
    print ("Name: ",row.name, "Address:",row.address, "Email:",row.email)

user = session.query(Customers).filter_by(id='1').first()
print(user.name)
```

```python
from sqlalchemy.orm import Query

q = Query(Customers, session)
for row in q:
    print ("Name: ",row.name, "Address:",row.address, "Email:",row.email)
```


---

## update object

### commit

```python
x = session.query(Customers).get(2)
print("Name: ", x.name, "Address:", x.address, "Email:", x.email)
x.address = 'Banjara Hills Secunderabad'
session.commit()
print("Name: ", x.name, "Address:", x.address, "Email:", x.email)
```


### rollback

```python
x = session.query(Customers).first()
print("Name: ", x.name, "Address:", x.address, "Email:", x.email)
x.name = 'Ravi Shrivastava'
session.rollback()
print("Name: ", x.name, "Address:", x.address, "Email:", x.email)
```


---

## filter

### equal

```python
for row in session.query(Customers).filter(Customers.id == 2):
    print("ID:", row.id, "Name: ", row.name, "Address:", row.address, "Email:", row.email)
```


### no equal

```python
for row in session.query(Customers).filter(Customers.id != 2):
    print("ID:", row.id, "Name: ", row.name, "Address:", row.address, "Email:", row.email)
```


### like

```python
for row in session.query(Customers).filter(Customers.name.like('Ra%')):
    print("ID:", row.id, "Name: ", row.name, "Address:", row.address, "Email:", row.email)
```


### in

```python
for row in session.query(Customers).filter(Customers.id.in_([1, 3])):
    print("ID:", row.id, "Name: ", row.name, "Address:", row.address, "Email:", row.email)
```


### between

```python
for row in session.query(Customers).filter(Customers.id.between(1, 3)):
    print("ID:", row.id, "Name: ", row.name, "Address:", row.address, "Email:", row.email)
```


### and

```python
for row in session.query(Customers).filter(Customers.id > 2, Customers.name.like('Ra%')):
    print("ID:", row.id, "Name: ", row.name, "Address:", row.address, "Email:", row.email)
```

```python
from sqlalchemy import and_

for row in session.query(Customers).filter(and_(Customers.id > 2, Customers.name.like('Ra%'))):
    print("ID:", row.id, "Name: ", row.name, "Address:", row.address, "Email:", row.email)
```


### or

```python
from sqlalchemy import or_

for row in session.query(Customers).filter(or_(Customers.id > 2, Customers.name.like('Ra%'))):
    print("ID:", row.id, "Name: ", row.name, "Address:", row.address, "Email:", row.email)
```


---

## return list and scalar

### all

```python
for row in session.query(Customers).first():
    print("ID:", row.id, "Name: ", row.name, "Address:", row.address, "Email:", row.email)
```


### first

```python
user = session.query(Customers).first()
print("ID:", user.id, "Name: ", user.name, "Address:", user.address, "Email:", user.email)
```

只顯示第一筆, 找不到時 回傳 none

### one

```python
try:
    user = session.query(Customers).one()
    print("ID:", user.id, "Name: ", user.name, "Address:", user.address, "Email:", user.email)
except Exception as e:
    print(e)
```

只顯示第一筆, 找不到或多筆時, 回傳 exception


### one_or_none

```python
try:
    user = session.query(Customers).one_or_none()
    print("ID:", user.id, "Name: ", user.name, "Address:", user.address, "Email:", user.email)
except Exception as e:
    print(e)
```

只顯示第一筆, 找不到回傳 none, 多筆時回傳 exception


### scalar

```python
user = session.query(Customers).filter(Customers.id == 3).scalar()
print("ID:", user.id, "Name: ", user.name, "Address:", user.address, "Email:", user.email)
```


---

## textual sql

```python
from sqlalchemy import text

for cust in session.query(Customers).filter(text("id < 3")):
    print(cust.name)

cust = session.query(Customers).filter(text("id = :value")).params(value = 1).one()
print(cust.name)

for cust in session.query(Customers).from_statement(text("SELECT * FROM customers")).all():
    print(cust.name)

stmt = text("SELECT name, id, name, address, email FROM customers")
stmt = stmt.columns(Customers.id, Customers.name)
for cust in session.query(Customers.id, Customers.name).from_statement(stmt).all():
    print(cust)
```


---

## build relationship

```python
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///sales.db', echo=True)
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)

class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    custid = Column(Integer, ForeignKey('customers.id'))
    invno = Column(Integer)
    amount = Column(Integer)
    customer = relationship("Customer", back_populates = "invoices")

Customer.invoices = relationship("Invoice", order_by=Invoice.id, back_populates="customer")
Base.metadata.create_all(engine)
```


---

##  related object

```python
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

c1 = Customer(name="Gopal Krishna", address="Bank Street Hydarebad", email="gk@gmail.com")
c1.invoices = [Invoice(invno=10, amount=15000), Invoice(invno=14, amount=3850)]
session.add(c1)
session.commit()

rows = [
    Customer(
        name="Govind Kala",
        address="Gulmandi Aurangabad",
        email="kala@gmail.com",
        invoices=[
            Invoice(invno=7, amount=12000),
            Invoice(invno=8, amount=18500)
        ]
    ),

    Customer(
        name="Abdul Rahman",
        address="Rohtak",
        email="abdulr@gmail.com",
        invoices=[
            Invoice(invno=9, amount=15000), 
            Invoice(invno=11, amount=6000)
        ]
    )
]
session.add_all(rows)
session.commit()
```


---

## ref

[Object Relational Tutorial (1.x API)](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)

[SQLAlchemy Tutorial](https://www.tutorialspoint.com/sqlalchemy/index.htm)

[pysheeet - SQLAlchemy](https://www.pythonsheets.com/notes/python-sqlalchemy.html)
