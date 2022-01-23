# opensuse

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

# run/load python file
In []: run <file>.py
In []: %hist
```


### jupyter

```bash
(<venv>) opensuse:~ $ pip install jupyter
(<venv>) opensuse:~ $ jupyter notebook password     # $HOME/.jupyter/jupyter_notebook_config.json
(<venv>) opensuse:~ $ jupyter notebook [--ip=0.0.0.0] [--port=8888]
```


### tk

```bash
opensuse:~ # python39-tk
opensuse:~ $ python3.9 -m tkinter
```


### pygame

```bash
(<venv>) opensuse:~ $ pip install pygame
(<venv>) opensuse:~ $ python -m pygame.examples.aliens
```
