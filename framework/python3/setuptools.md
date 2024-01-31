# setuptools

## setup command

```bash
# for install
linux:~/proj $ python setup.py install
=>
linux:~/proj $ python setup.py build
linux:~/proj $ python setup.py install


linux:~/proj $ pip install -e .
=>
linux:~/proj $ python setup.py develop

# build
linux:~/proj $ python setup.py sdist --formats=gztar

linux:~/proj $ python setup.py bdist --formats=rpm
=>
linux:~/proj $ python setup.py build_rpm
```

---

## example

```bash
linux:~/demo $ tree
.
├── bin
│   └── say
├── etc
│   └── config.ini
├── example
│   └── sample.py
├── README.md
├── setup.cfg
├── setup.py
└── src
    ├── __init__.py
    └── util
        ├── __init__.py
        └── say.py
```

```py
# bin/say
#!/use/bin/env python3

from demo.util.say import hello
import sys

if __name__ == '__main__':
    print(hello(sys.argv[1]))
```

```ini
; etc/config.ini
[DEFAULT]
USER = demo
```

```py
example/sample.py
from demo.util.say import hello

if __name__ == '__main__':
    print(hello('world'))
```

```md
<!-- README.md -->

# README
```

```conf
; setup.cfg
[metadata]
name = demo
author = user
author_email = user@email.com
description = demo package
license = Apache License 2.0
long_description = file: README.md
version = 0.1
```

```py
setup.py
from setuptools import setup, find_packages
from glob import glob


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


setup(
    python_requires='>=3.6',
    # package_dir={'demo': './src', 'demo.example': './example'},
    package_dir={'demo': './src'},

    # only .py
    # packages=['demo', 'demo.util', 'demo.example'],
    packages=['demo', 'demo.util'],
    # packages=find_packages(),

    # non .py
    data_files=[('share/demo', ['README.md']),
                ('share/demo/etc', ['./etc/config.ini']),
                ('share/demo/example', glob('./example/*.py'))],

    scripts=['bin/say'],  # run command
    # include_package_data=True,  # enable MANIFEST.in

    # install_requires=['docutils>=0.3'],
    # setup_requires=['pbr'],
    # tests_require=[
    #     'pytest>=3.3.1',
    #     'pytest-cov>=2.5.1',
    # ],
    # extras_require={
    #     'PDF':  ["ReportLab>=1.2", "RXP"],
    #     'reST': ["docutils>=0.3"],
    # },
)
```

```py
# src/__init__.py
```

```py
# src/util/__init__.py
```

```py
# src/util/say.py
def hello(name):
    return f"hello {name}!"
```
