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

## SQLAlchemy
