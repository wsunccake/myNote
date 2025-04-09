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
linux:~ $ uv venv [<.venv>]             # <.venv> 底下不會有 <.venv>/bin/pip
linux:~ $ uv pip install <package>      # <.venv> 要使用 uv pip 管理
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
linux:~ $ uv init <project>     # create project
linux:~ $ uv add <package>
linux:~ $ uv remove <package>
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
