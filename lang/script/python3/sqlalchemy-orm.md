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

## ref

[Object Relational Tutorial (1.x API)](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)

[SQLAlchemy Tutorial](https://www.tutorialspoint.com/sqlalchemy/index.htm)

[pysheeet - SQLAlchemy](https://www.pythonsheets.com/notes/python-sqlalchemy.html)
