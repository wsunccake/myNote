# setuptools

```bash
linux:~ $ mkdir -p MyApp/mypackage
linux:~ $ cd MyApp

# __init__.py
linux:~/MyApp $ touch mypackage/__init__.py

# greet.py
linux:~/MyApp $ cat << EOF > mypackage/greet.py
def SayHello(name):
    print("Hello ", name)
EOF

# functions.py
linux:~/MyApp $ cat << EOF > mypackage/functions.py
def sum(x,y):
    return x+y

def average(x,y):
    return (x+y)/2

def power(x,y):
    return x**y
EOF

# folder
linux:~/MyApp $ tree
.
└── mypackage
    ├── functions.py
    ├── greet.py
    └── __init__.py

1 directory, 3 files

# test
linux:~/MyApp $ python3 -c "from mypackage import functions;print(functions.power(3,2))"

# setup.py
linux:~/MyApp $ cat << EOF > setup.py
from setuptools import setup

setup(
    name = 'mypackage',
    version = '0.1',
    description = 'Testing installation of Package',
    url = '#',
    author = 'auth',
    author_email = 'author@email.com',
    license = 'MIT',
    packages = ['mypackage'],
    zip_safe = False
)
EOF

# install
linux:~/MyApp $ python setup.py install

# list
linux:~/MyApp $ pip list
```


---

## other

```bash
linux:~/MyApp $ python setup.py --help-commands

# build
linux:~/MyApp $ setup.py build
linux:~/MyApp $ ls build

# dist
linux:~/MyApp $ setup.py sdist
linux:~/MyApp $ ls dist

# update dist to pypi server
linux:~/MyApp $ setup.py sdist upload -r http://<pypi server>:<pypi port>
linux:~/MyApp $ pip install --trusted-host <pypi server>:<pypi port> --index-url http://<pypi server>:<pypi port>/simple/ mypackage
```

[pypi server](../../../../linux/container/app/pypi.md)
