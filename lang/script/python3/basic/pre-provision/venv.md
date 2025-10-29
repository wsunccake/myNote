# virtual environment

## venv

```bash
linux:~ $ python3 -m venv [--system-site-packages] venv
# --system-site-packages, 虛擬環境可以存取「系統 Python」已安裝的套件
linux:~ $ source $HOME/venv/bin/activate

# common package / command
(venv)linux:~ $ pip install ipython
(venv)linux:~ $ ipython
In[1]:

(venv)linux:~ $ pip install notebook
(venv)linux:~ $ jupyter notebook --ip 0.0.0.0 --port 8888

(venv)linux:~ $ pip install autopep8
(venv)linux:~ $ autopep8 [-i] <python_file>

(venv)linux:~ $ deactivate
```

## virtualenv

```bash
linux:~/project $ virtualenv .virtualenvs
linux:~/project $ source .virtualenvs/bin/activate

(.virtualenvs)linux:~/project $ deactivate
```

## virtualenvwrapper

```bash
linux:~ $ export WORKON_HOME=$HOME/.virtualenvs
linux:~ $ export VIRTUALENVWRAPPER_PYTHON=$(which python3)
linux:~ $ source /usr/share/virtualenvwrapper/virtualenvwrapper.sh

linux:~ $ lsvirtualenv
linux:~ $ cdvirtualenv <venv_name>
linux:~ $ mkvirtualenv <venv_name>
linux:~ $ rmvirtualenv <venv_name>

linux:~ $ workon <venv_name>
(<venv_name>)linux:~/project $ deactivate
```

✅ 總結比較

| 工具                | 是否內建 | 是否支援 Python 2 | 功能特色                                |
| ------------------- | -------- | ----------------- | --------------------------------------- |
| `venv`              | ✅ 是    | ❌ 不支援         | 官方標準，簡單輕量                      |
| `virtualenv`        | ❌ 否    | ✅ 支援           | 跨版本、功能豐富                        |
| `virtualenvwrapper` | ❌ 否    | ✅ 支援           | 管理虛擬環境更方便（需依賴 virtualenv） |
