# chapter 01

## network

```bash
opensuse:~ # yast lan
opensuse:~ # yast firewall
```


---

## python

```bash
opensuse:~ # zypper in python3
opensuse:~ # zypper in python39

opensuse:~ $ which python3.6
opensuse:~ $ which python3.9
opensuse:~ $ python3 --version
```


### venv

```bash
opensuse:~ $ python3.9 -m venv <venv>
opensuse:~ $ source py39/bin/activate
(<venv>) opensuse:~ $ which python
(<venv>) opensuse:~ $ python3 --version
(<venv>) opensuse:~ $ deactivate
```


### pip

```bash
(<venv>) opensuse:~ $ which pip
(<venv>) opensuse:~ $ pip help
(<venv>) opensuse:~ $ pip list
(<venv>) opensuse:~ $ pip search <package>
(<venv>) opensuse:~ $ pip install <package>[==<version>]
(<venv>) opensuse:~ $ pip uninstall <package>
```

### ipython

```bash
(<venv>) opensuse:~ $ pip install ipython
(<venv>) opensuse:~ $ ipython

In []: %run <file>.py               # run/load python file
In []: %run -d -b <n> <file>.py     # run python with pdb / debug
ipdb> ?         # help
ipdb> ll        # list code
ipdb> b         # list break point
ipdb> b <n>     # add break point in <n> line
ipdb> cl        # clear all break point
ipdb> cl <m>    # clear <m> break point
ipdb> p <var>   # show var
ipdb> c         # go to next break point
ipdb> q         # q

In []: %%time                       # time execution
...:L = []
...: for n in range(1000):
...:     L.append(n ** 2)
In []: %timeit L = [n ** 2 for n in range(1000)]
In []: %time?

In []: %hist [-n]                   # history
In []: %hist <i> [<j> ...]
In []: %hist <i>-<j>
In []: %hist -f <file>.py
```


### jupyter

```bash
(<venv>) opensuse:~ $ pip install jupyter
(<venv>) opensuse:~ $ jupyter notebook password     # $HOME/.jupyter/jupyter_notebook_config.json
(<venv>) opensuse:~ $ jupyter notebook [--ip=0.0.0.0] [--port=8888]
```


### tk

```bash
opensuse:~ # zypper in python39-tk
opensuse:~ $ python3.9 -m tkinter
```


### pygame

```bash
(<venv>) opensuse:~ $ pip install pygame
(<venv>) opensuse:~ $ python -m pygame.examples.aliens
```


### sample code

http://books.gotop.com.tw/download/ACG006300

[py_samples.zip](http://dlcenter.gotop.com.tw/SampleFiles/ACG006300/download/py_samples.zip)

Pnohtyg
