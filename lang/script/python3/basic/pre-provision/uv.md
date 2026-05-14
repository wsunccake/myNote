# uv

## install

```bash
linux:~ $ curl -LsSf https://astral.sh/uv/install.sh | sh

# specific version
linux:~ $ curl -LsSf https://astral.sh/uv/0.6.11/install.sh | sh
```

```bash
linux:~ $ uv version

linux:~ $ uv help
linux:~ $ uv help <command>
```

```powershell
PS C:\Users\user> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# Installing C:\Users\user\.local\bin  uv.exe, uvx.exe
# set Path=C:\Users\hwang1\.local\bin;%Path%                (cmd)
# $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"'      (powershell)

PS C:\Users\user> echo '$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"' >> $PROFILE
```

---

## python

```bash
linux:~ $ uv python --help
linux:~ $ uv python list
linux:~ $ uv python install <version>
linux:~ $ uv python uninstall <version>
linux:~ $ uv python pip <version>
```

---

## virtual environment

```bash
linux:~ $ uv venv [--python <version>] [<.venv>]    # <.venv> 底下不會有 <.venv>/bin/pip
linux:~ $ uv pip install <package>                  # <.venv> 要使用 uv pip 管理
linux:~ $ uv pip list
linux:~ $ uv pip uninstall <package>
linux:~ $ uv pip tree
```

```bash
linux:~ $ uv venv
linux:~ $ source .venv/bin/active
(.venv):~ $ which python

(.venv):~ $ uv pip install cowsay
(.venv):~ $ python3 -c "from cowsay import cow;cow('hello, world')"
```

```powershell
PS C:\Users\user> uv venv
PS C:\Users\user> .\.venv\Scripts\activate.ps1
(.venv) PS C:\Users\user> Get-Command python
```

---

## project

```bash
# new project
linux:~ $ uv init <project>     # create project
linux:~ $ uv add <package>
linux:~ $ uv remove <package>

# old project
linux:~/project $ uv init
linux:~/project $ uv venv
linux:~/project $ uv pip install
```

---

## tool

```bash
linux:~ $ uv tool dir
linux:~ $ uv tool list
linux:~ $ uv tool install <package>
linux:~ $ uv tool uninstall <package>

linux:~ $ uv tool run <script>      # uvx <script>
```

---

## run

```bash
linux:~ $ uv run python -m http.server
```

---

## example

```bash
# create project
linux:~ $ uv init zen
linux:~ $ cd zen

# setup venv
linux:~/zen $ uv venv [<venv_dir>]              # <venv_dir>: 預設是 .venv
linux:~/zen $ source <venv_dir>/bin/active

# add package
linux:~/zen $ uv add requests --active          # 若不使用預設 <venv_dir>, 則需要 --active 將 package 安裝
linux:~/zen $ cat pyproject.toml
[project]
name = "zen"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "requests>=2.32.5",
]

# run script 
linux:~/zen $ vi hello.py
linux:~/zen $ uv run hello.py

# build tool
linux:~/zen $ vi pyproject.toml
[project.scripts]
zen = "hello:main"
 ^       ^     ^
command  |     function or file
     file or dir
              
linux:~/zen $ uv build                                  # build package
linux:~/zen $ ls dist
linux:~/zen $ uv tool install .                         # install package from local
linux:~/zen $ uv tool install dist/zen-0.1.0.tar.gz     # install package from dist

linux:~/zen $ uv tool run zen                           # run         
```

```python
# hello.py
import requests

def main():
    r = requests.get("https://api.github.com/zen")
    print(f"GitHub zen: {r.text}")

if __name__ == "__main__":
    main()
```
