# install

```bash
centos:~ # yum install python34 python34-pip            # for centos 7
centos:~ # dnf module install python36                  # for centos 8

debian:~ # apt install python3-pip                      # for debian 11

linux:~ $ wget https://bootstrap.pypa.io/get-pip.py     # for user
linux:~ $ python3 get-pip.py --user
```


```batch
C:\Users\user> curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py   # windows 10
C:\Users\user> python get-pip.py
```


```bash
# install python 3.x
osx:~ # installer -pkg python-3.x-macos11.pkg -target /

# uninstall all python3.x
osx:~ # rm -rf /Library/Frameworks/Python.framework
osx:~ # find /usr/local/bin -type l -and -lname "*/Library/Frameworks/Python.framework/*" -delete
osx:~ # pkgutil --pkgs | grep Python | xarg -I{} pkgutil --forget {}

# uninstall python3.x
osx:~ # rm -rf /Library/Frameworks/Python.framework/Versions/3.x
osx:~ # rm find /usr/local/bin -type l -and -lname "*/Library/Frameworks/Python.framework/Versions/3.x*" -delete
osx:~ # rm pkgutil --forget org.python.Python.PythonFramework-3.x
osx:~ # rm pkgutil --forget org.python.Python.PythonDocumentation-3.x
osx:~ # rm pkgutil --forget org.python.Python.PythonApplications-3.x
osx:~ # rm pkgutil --forget org.python.Python.PythonUnixTools-3.x
```


---

# package management

## pip

安裝 virtualenv, pybuilder 為例子

```bash
linux:~ # pip -V
linux:~ # pip list
linux:~ # pip help

# package
linux:~ # pip search virtualenv             # search package

linux:~ # pip install virtualenv            # install package
linux:~ # cat requirements.txt
pybuilder
linux:~ # pip install -r requirements.txt   # install package from requirements file
linux:~ # python -m pip install requests    # install package by module

linux:~ # pip install --upgrade pip         # upgrade package
linux:~ # pip uninstall requests            # remove package

# show package avaible version
linux:~ # pip index versions pylibmc                                  # pip >= 21.2
linux:~ # pip install pylibmc==                                       # pip >= 21.1
linux:~ # pip install --use-deprecated=legacy-resolver pylibmc==      # pip >= 20.3
linux:~ # pip install pylibmc==                                       # pip >= 9.0
linux:~ # pip install pylibmc==blork                                  # pip < 9.0
```


---

# virtual environment

## virtualenv

```bash
linux:~ # virtualenv --python=python3 myproject3
linux:~/myproject3 # source bin/activate
linux:~/myproject3 # VIRTUAL_ENV_DISABLE_PROMPT=1 source bin/activate
linux:~/myproject3 # deactivate
```


## venv

```bash
linux:~ # python3 -m venv venv
linux:~ # source venv/bin/activate
(venv) linux:~ # deactivate

linux:~ # cat venv/pyvenv.cfg
prompt =
```

```batch
C:\Users\user> py -m venv venv
C:\Users\user> .\venv\Scripts\activate
(venv) C:\Users\user> deactivate
```


## pipenv

```bash
linux:~ # pip install pipenv

linux:~ # pipenv --help

# setup pip + venv + python ver
linux:~ # pipenv --python 2.7
linux:~ # pipenv --python 3.6
linux:~ # pipenv --two
linux:~ # pipenv --three

# environment
linux:~ # pipenv --py
linux:~ # pipenv --venv

# install package
linux:~ # pipenv install <package>
linux:~ # pipenv install -r requirements.txt

# run
linux:~ # pipenv run python <script.py>

linux:~ # source `pipenv --venv`/bin/activate
(venv) linux:~ #

# remove
linux:~ # pipenv --rm
```


---

# read-eval-print loop / repl

## ipython

```bash
linux:~ # pip install ipython
linux:~ # ipython
```


## jupyter

```bash
linux:~ # pip install jupyter
linux:~ # jupyter notebook
```


---

# build tool

## PyBuilder

### project

```bash
linux:~/myproject3 # mkdir demo
linux:~/myproject3/demo # pyb -h
linux:~/myproject3/demo # pyb --start-project
```


### pycharm/intellij ide plugin

```bash
linux:~/project $ vi build.py
...
use_plugin('python.pycharm')

linux:~/project $ pyb pycharm_generate
```


### source code

```bash
linux:~/myproject3/demo # mkdir -p src/main/python
linux:~/myproject3/demo # cat src/main/python/hell.py
import sys

def helloworld(out):
    out.write('Hello Python\n')
```

### executable

```bash
linux:~/myproject3/demo # mkdir -p src/main/scripts
linux:~/myproject3/demo # cat src/main/scripts/hello
#!/usr/bin/env python
import sys

sys.stdout.write('Hello Python\n')


linux:~/myproject3/demo # chmod +x src/main/scripts/hello
```

### unit test

```bash
linux:~/myproject3/demo # cat src/unittest/python/hello_tests.py
from mockito import mock, verify
import unittest

from hello import hello

class HelloTest(unittest.TestCase):
    def test_should_issue_hello_message(self):
        out = mock()
        hello(out)
        verify(out).write('Hello Python\n')
```

### build file

```bash
linux:~/myproject3/demo # cat build.py
from pybuilder.core import init, use_plugin

use_plugin('python.core')
use_plugin('python.unittest')
use_plugin('python.coverage')
use_plugin('python.install_dependencies')
use_plugin('python.distutils')

name = 'demo'
default_task = ['clean', 'publish']


@init
def initialize(project):
    project.build_depends_on('mockito')
    project.version = '0.1'
```

### run

```bash
linux:~/myproject3/demo # pyb install_dependencies
linux:~/myproject3/demo # pyb
```


---

# class

```bash
#!/usr/bin/env python3

class First(object):
    def say(self):
        print("from First")

class Second(object):
    def say(self):
        print("from Second")

class Third(object):
    def say(self):
        print("from Third")

class Son(First, Second, Third):
    def say(self):
        #super().say()                     # from First (same as super(Son, self).say())
        super(First, self).say()           # from Second
        #super(Second, self).say()         # from Third
        #super(Third, self).say()          # error

son = Son()
son.say()
```
