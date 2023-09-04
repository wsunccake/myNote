# python environment in vscode

---

## content

- [basic](#basic)
  - [基本設定](#基本設定)
  - [執行參數](#執行參數)
  - [環境變數](#環境變數)
- [application](#application)
  - [locust](#locust)
  - [robotframework](#robotframework)
  - [pytest](#pytest)

---

## basic

先安裝 [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) plugin, 在開始設定

### 基本設定

```json
// settings.json
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

### 執行參數

```json
// launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

### 環境變數

在 settings.json 設定 "python.envFile": "${workspaceFolder}/.env", 在執行 vscode 的 run / debug, 會載入該環境變數

```json
// .env
PYTHONPATH=${HOME}/${WORKSPACE}/lib:${PYTHONPATH}
```

---

## application

### locust

```bash
# .env
PYTHONPATH=${workspaceFolder}/lib:${PYTHONPATH}
GEVENT_SUPPORT=True
```

```json
// launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "locust",
      "type": "python",
      "request": "launch",
      "module": "locust",
      //   "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true,
      "args": [
        "--loglevel",
        "DEBUG",
        "-f",
        "${file}",
        "--headless",
        "--print-stats",
        "--html",
        "result.html",
        "-t",
        "5m",
        "--host",
        "https://api.server.com"
      ],
      "env": {
        "PYTHONPATH": "${workspaceFolder}:${env:PYTHONPATH}"
      },
      "cwd": "${fileDirname}"
    }
  ]
}
```

### robotframework

```json
// launch.json
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
      "env": {
        "PYTHONPATH": "${workspaceFolder}${pathSeparator}lib:${env:PYTHONPATH}"
      },
      "cwd": "${fileDirname}"
    }
  ]
}
```

### pytest

```json
// launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["--alluredir", "tmp", "--clean-alluredir", "${file}"],
      "env": { "PYTHONPATH": "${workspaceFolder}" },
      "justMyCode": true
    }
  ]
}
```
