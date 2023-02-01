# python environment in vscode

## settings.json

```json
{
  "files.trimTrailingWhitespace": true,
  "python.linting.enabled": true,
  // linter option: 'bandit', 'flask8', 'mypy', 'prospector',
  //                'pycodestyle', 'pylama', 'pylint'
  // "python.linting.pylintEnabled": true,
  // "python.linting.pylintArgs": ["--disable=C0111"],
  "python.linting.mypyEnabled": true,
  // formater option: 'autopep8', 'black', 'yapf'
  "python.formatting.provider": "autopep8",
  "python.envFile": "${workspaceFolder}/.env",
  "[python]": {
    "editor.formatOnType": true,
    "editor.formatOnSave": true,
    "editor.insertSpaces": true,
    "editor.detectIndentation": true,
    "editor.tabSize": 4
  }
}
```

---

## launch.json

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "robotfraemwork",
      "type": "python",
      "request": "launch",
      "module": "robot",
      "args": ["${file}"],
      "console": "integratedTerminal",
      "justMyCode": true,
      "environment": [
        {
          "PYTHONPATH": "${workspaceFolder}"
        }
      ],
      "cwd": "${fileDirname}"
    },
    {
      "name": "pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["--alluredir", "tmp", "--clean-alluredir", "${file}"],
      "environment": [
        {
          "PYTHONPATH": "${workspaceFolder}"
        }
      ],
      "justMyCode": true
    }
  ]
}
```

---

## .env

```json
PYTHONPATH=$HOME/$WORKSPACE/lib:$PYTHONPATH
```

---

## plugin

(Python)[https://marketplace.visualstudio.com/items?itemName=ms-python.python]
