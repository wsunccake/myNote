# poetry

## install

```bash
linux:~ $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
linux:~ $ ls $HOME/.poetry/bin
linux:~ $ export PATH="$HOME/.poetry/bin:$PATH"

# update profile / shrc
linux:~ $ vi $HOME/.profile
linux:~ $ vi $HOME/.zshrc
```


---

## usage

```bash
# version / help
linux:~ $ poetry --version
linux:~ $ poetry --help
linux:~ $ poetry help init

# init
linux:~ $ mkdir <project>
linux:~ $ cd <project>
linux:~ $ poetry init
linux:~/<project> $ cat pyproject.toml

# config
linux:~/<project> $ poetry config --list
linux:~/<project> $ poetry config <key> <value>

# virtualenv
linux:~/<project> $ poetry env use <python>
linux:~/<project> $ poetry env info
linux:~/<project> $ poetry env list
linux:~/<project> $ poetry env remove <virtualenv>

# shell
linux:~/<project> $ poetry shell

# package
linux:~/<project> $ poetry show
linux:~/<project> $ poetry add <pcakage>
linux:~/<project> $ poetry remove <package>
```


---

## example

```bash
# init
linux:~ $ mkdir poetry-demo
linux:~ $ cd poetry-demo
linux:~/poetry-demo $ poetry init
linux:~/poetry-demo $ cat pyproject.toml
[tool.poetry]
name = "poetry-demo"
version = "0.1.0"
description = ""
authors = ["User <user@mail.com>"]

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

# setup virtualenv
linux:~/poetry-demo $ poetry config virtualenvs.in-project true
linux:~/poetry-demo $ poetry env use python3
linux:~/poetry-demo $ poetry env info
linux:~/poetry-demo $ poetry env list

# launch virtualenv
linux:~/poetry-demo $ poetry shell

# package
(.venv) poetry-demo $ poetry add pendulum
(.venv) poetry-demo $ poetry add pendulum@^2.0.5
(.venv) poetry-demo $ poetry add "pendulum>=2.0.5"
(.venv) poetry-demo $ poetry show
```


---

## ref

[python-poetry docs](https://python-poetry.org/docs)
