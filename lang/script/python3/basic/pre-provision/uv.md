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
(.venv):~ $ uv pip install cowsay
(.venv):~ $ python3 -c "from cowsay import cow;cow('hello, world')"
```

---

## project

```bash
linux:~ $ uv init <project>     # create project
linux:~ $ uv add <package>
linux:~ $ uv remove <package>
```
