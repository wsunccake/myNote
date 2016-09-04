# pip

```
linux:~ # pip list
linux:~ # pip help
linux:~ # pip search virtualenv
linux:~ # pip install virtualenv
linux:~ # python -m pip install requests
linux:~ # pip install --upgrade pip
linux:~ # cat requirements.txt
pybuild
linux:~ # pip install -r requirements.txt
linux:~ # pip uninstall requests
```


# virtualenv

```
linux:~ # virtualenv --python=python3 myproject3
linux:~/myproject3 # source bin/activate
linux:~/myproject3 # VIRTUAL_ENV_DISABLE_PROMPT=1 source bin/activate
linux:~/myproject3 # deactivate
```


# PyBuilder

## project

```
linux:~/myproject3 # mkdir demo
linux:~/myproject3/demo # pyb -h
linux:~/myproject3/demo # pyb --start-project
```

## source code

```
linux:~/myproject3/demo # mkdir -p src/main/python
linux:~/myproject3/demo # cat src/main/python/hell.py
import sys

def helloworld(out):
    out.write('Hello Python\n')
```

## executable

```
linux:~/myproject3/demo # mkdir -p src/main/scripts
linux:~/myproject3/demo # cat src/main/scripts/hello
#!/usr/bin/env python
import sys

sys.stdout.write('Hello Python\n')


linux:~/myproject3/demo # chmod +x src/main/scripts/hello 
```

## unit test

```
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

## build file

```
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


## run

```
linux:~/myproject3/demo # pyb install_dependencies
linux:~/myproject3/demo # pyb
```