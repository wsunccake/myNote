# ollama

## require

```bash
# Debian/Ubuntu
linux:~ # apt-get install zstd

# RHEL/CentOS/Fedora
linux:~ # dnf install zstd

# Arch
linux:~ # pacman -S zstd
```

---

## install

```bash
linux:~ # curl -fsSL https://ollama.com/install.sh | sh
```

---

## uninstall

```bash
linux:~ # systemctl stop ollama
linux:~ # systemctl disable ollama
linux:~ # rm /etc/systemd/system/ollama.service
linux:~ # rm -f $(which ollama)
linux:~ # rm -rf /usr/share/ollama
linux:~ # userdel ollama
linux:~ # groupdel ollama
linux:~ # rm -rf /usr/local/lib/ollama
```

---

## run

```bash
linux:~ # ollama --version
linux:~ # journalctl -e -u ollama

linux:~ # ollama pull llama3:8b
linux:~ # ollama run llama3:8b

# model folder
linux:~ # ls /usr/share/ollama/.ollama    # for system
linux:~ # ~/.ollama/models                # for user
linux:~ # export OLLAMA_HOME=             # for env var
```

---

## model

```bash
linux:~ $ ollama list
linux:~ $ ollama show <model>
linux:~ $ ollama pull <model>
linux:~ $ ollama rm <model>
linux:~ $ ollama cp <old model> <new model>
```

## launch

```bash
# in-active mode
linux:~ $ ollama run <model>

# active mode
linux:~ $ ollama run <model> "<question>"
```

---

## service

```bash
linux:~ # systemctl start ollama
linux:~ # systemctl enable ollama
linux:~ # systemctl stop ollama
linux:~ # systemctl status ollama

linux:~ # systemctl edit ollama.service     # ref: /etc/systemd/system/ollama.service
linux:~ # mkdir -p /etc/systemd/system/ollama.service.d
linux:~ # vi /etc/systemd/system/ollama.service.d/override.conf
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_KEEP_ALIVE=-1"
...

linux:~ # systemctl daemon-reload
linux:~ # systemctl restart ollama
```

| var               | description                                | default         |
| ----------------- | ------------------------------------------ | --------------- |
| OLLAMA_HOST       | IP Address for the ollama server           | 127.0.0.1:11434 |
| OLLAMA_KEEP_ALIVE | duration that models stay loaded in memory | 5m              |

---

## test

```bash
linux:~ $ curl http://127.0.0.1:11434

linux:~ $ curl http://localhost:11434/api/generate -d '{
  "model": "<model>",
  "prompt":"<question>"
}'


linux:~ $ curl http://localhost:11434/api/generate -d '{
  "model": "llama3:8b",
  "prompt":"what is llm?"
}'
```
