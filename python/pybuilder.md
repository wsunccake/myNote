# pybuilder


## Install

```
Linux:~ # pip install pybuilder  # 安裝
Linux:~ # pyb -h  # help
Linux:~ # pyb --version
Linux:~ # pyb -t  # list task
```


## Folder Structure

```
Linux:~ # mkdir pyproject
Linux:~ # cd pyproject
Linux:~/pyproject # mkdir -p src/main/{python,scripts} src/unittest/python
```


## Source Code

```
Linux:~/pyproject # vi src/main/python/helloworld.py
import sys

def helloworld(out):
    out.write("Hello world of Python\n")

Linux:~/pyproject # vi build.py
from pybuilder.core import use_plugin

use_plugin("python.core")

default_task = "publish"

Linux:~/pyproject # pyb
Linux:~/pyproject # pyb clean
```


## Runnable Script

```
Linux:~/pyproject # vi src/main/scripts/hello-pybuilder
#!/usr/bin/env python
import sys

sys.stdout.write('Hello from my script!\n')

Linux:~/pyproject # pyb
```


## Unit Test

```
Linux:~/pyproject # src/unittest/python/helloworld_tests.py
from mockito import mock, verify
import unittest

from helloworld import helloworld

class HelloWorldTest(unittest.TestCase):
    def test_should_issue_hello_world_message(self):
        out = mock()

        helloworld(out)

        verify(out).write("Hello world of Python\n")

Linux:~/pyproject # vi build.py
from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")

default_task = "publish"

@init
def initialize(project):
    project.build_depends_on('mockito')


Linux:~/pyproject # pby clean run_unit_tests
```


## Test Coverage

```
Linux:~/pyproject # vi build.py
from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.install_dependencies")

default_task = "publish"

@init
def initialize(project):
    project.version = "0.1"
    project.build_depends_on('mockito')

Linux:~/pyproject # pyb
```


## Publish

```
Linux:~/pyproject # vi build.py
from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")

name = "pyproject"
default_task = "publish"

@init
def initialize(project):
    project.version = "0.1"
    project.build_depends_on('mockito')


Linux:~/pyproject # pyb clean package
Linux:~/pyproject # ls target/dist/pyproject-0.1.dev0

Linux:~/pyproject # pyb clean install
Linux:~/pyproject # ls -lart /usr/lib/python2.7/site-packages/pyproject-0.1.dist-info
```

### clean

清除 build 時產生的檔案

### run_unit_tests

執行 unittest

### package

產生 target/dist 的套件

### analyze

產生 target/reports

### publish

clean + run_unit_tests + package + analyze


## Other

```
Linux:~/pyproject # pyb --start-project
```