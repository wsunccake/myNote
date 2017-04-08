# Flask

## Development Tool

```
# prepare environment
linux:~ $ virtualenv --python=python3 master_flask
linux:~ $ source masater_flask/bin/activate
linux:~ $ pip install pybuilder

# setup project
linux:~ $ mkdir project
linux:~ $ cd project
linux:~/project $ pyb --start-project
linux:~/project $ vi build.py
...
use_plugin('python.pycharm')

linux:~/project $ pyb pycharm_generate

# create requirement
linux:~/project $ pip freeze > requirements.txt
```

## Hello Flask

```
linux:~/hello $ vi build.py
...
def set_properties(project):
    project.version = '0.1'
    project.depends_on('flask')
    project.depends_on('flask-script')

linux:~/hello $ pyb install_dependencies
linux:~/hello $ vi src/main/python/hello.py 
from flask import Flask
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)


@app.route('/')
def home():
    return 'Hello Flask'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

linux:~/hello $ vi  src/main/python/config.py 
class DevConfig(object):
    DEBUG = True


# run server
linux:~/hello $ python src/main/python/hello.py

# add unittest
linux:~/hello $ vi src/unittest/python/hello_test.py
import unittest
import hello


class HelloTest(unittest.TestCase):
    def setUp(self):
        self.app = hello.app.test_client()

    def tearDown(self):
        pass

    def test_home(self):
        uri = '/'
        message = 'Hello Flask'
        rv = self.app.get(uri)
        self.assertEqual(message, rv.data.decode("utf-8"))

# run unittest
linux:~/hello $ pyb run_unit_tests

# add flask-script
linux:~/hello $ vi src/main/python/manage.py
from flask.ext.script import Manager, Server
from hello import app


manager = Manager(app)
manager.add_command('server', Server())


@manager.shell
def make_shell_context():
    return dict(app=app)

if __name__ == '__main__':
    manager.run()

# run flask-script
linux:~/hello $ python src/main/python/manage.py server     # run server
linux:~/hello $ python src/main/python/manage.py server -?  # server help
linux:~/hello $ python src/main/python/manage.py shell      # shell mode
```


## ORM


### SQL

```
## Create Table
sql> CREATE TABLE user (
...>  id INTEGER NOT NULL, 
...>  username VARCHAR(255) NOT NULL, 
...>  password VARCHAR(255), 
...>  PRIMARY KEY (id)
...> );

## Create record
sql> INSERT INTO user (id, name)
...> VALUES (1, 'Ramesh');
sql> INSERT INTO user (id, name)
...> VALUES (2, 'Khilan');
sql> INSERT INTO user (id, name, age, address, salary)
...> VALUES (3, 'Kaushik'),
...> (4, 'Chaitali'),
...> (5, 'Hardik'),
...> (6, 'Komal'),
...> (7, 'Paul'),
...> (8, 'James'),
...> (9, 'James');

## Read record
sql> SELECT * FROM user;
sql> SELECT username FROM user;
sql> SELECT username FROM user LIMIT 3;
sql> SELECT username FROM user ORDER BY user.username DESC;
sql> SELECT DISTINCT username FROM user;

sql> SELECT username FROM user WHERE username = 'Ramesh';
sql> SELECT username FROM user WHERE username LIKE '%ik';
sql> SELECT username FROM user WHERE username LIKE '_a%';
sql> SELECT username FROM user WHERE username LIKE '%ik' OR username LIKE '_a%';

## Update record
sql> UPDATE user SET password='test' WHERE user.username = 'Ramesh';

## Delete record
sql> DELETE FROM user;
sql> DELETE FROM user WHERE user.id = 1;
```

### SQLAlchemy

```
linux:~/orm $ vi build.py
...
def set_properties(project):
    project.version = '0.1'
    project.depends_on('flask')
    project.depends_on('flask-sqlalchemy')

linux:~/orm $ vi src/main/python/main.py 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig


app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)


class User(db.Model):
    # __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)


@app.route('/')
def home():
    return 'Hello Flask'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

linux:~/orm $ vi src/main/python/config.py 
class DevConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
    SQLALCHEMY_ECHO = True

class ProdConfig(object):
    pass

linux:~/orm $ vi src/main/python/manage.py
from flask_script import Manager, Server
from main import app, db, User


manager = Manager(app)
manager.add_command('server', Server())


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User)

if __name__ == '__main__':
    manager.run()

# create table
linux:~/orm $ python src/main/python/manage.py shell
>>> db.create_all()
```