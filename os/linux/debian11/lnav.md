# lnav

## install

```bash
debian:~ # apt install nav
```


---

## usage

```bash
debian:~ $ lnav [<file>|<dir>]
debian:~ $ lnav -r [<compress file>]
```

```
?           help
q/Q         quit
j/k/h/l     up/down/left/right
g/G         top/end of file
f/F         next/previous file
e/E         next/previous error
w/W         next/previous warning
n/N         next/previous search
```


---

## config

```bash
debian:~ $ ls $HOME/.config/lnav
```


---

## format

```json
{
  "pythonlogger": {
    "title": "Python logger format",
    "description": "Log format used by python logger class",
    "url": "",
    "regex": {
      "main": {
        "pattern": "^\\[(?<timestamp>\\d{4}\\-\\d{2}\\-\\d{2} \\d{2}:\\d{2}:\\d{2},\\d{3})] (?<host>(\\S+))\/(?<level>(\\w+))\/(?<module>(\\S+)): (?<body>.*)"
      }
    },
    "timestamp-format": ["%Y-%m-%d %H:%M:%S,%L"],
    "level-field": "level",
    "level": {
      "critical": "CRITICAL",
      "error": "ERROR",
      "warning": "WARNING",
      "info": "INFO",
      "debug": "DEBUG"
    },
    "value": {
      "host": { "kind": "string", "identifier": true },
      "level": { "kind": "string", "identifier": true },
      "module": { "kind": "string", "identifier": true },
      "body": { "kind": "string" }
    },
    "sample": [
      {
        "line": "[2022-03-10 02:10:04,026] dhcp-192-168-1-128/INFO/user@email.com: body: {\"tenantId\":\"xxxx\"}, status: 200, ok: True",
        "line": "[2022-03-10 02:10:04,026] server10/ERROR/locust.user.task: Starting Locust 2.8.2"
      }
    ]
  }
}
```

```bash
debian:~ $ lnav -i <format>.json
debian:~ $ lnav <file>.log
```
