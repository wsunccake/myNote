# LibreChat

## install

```bash
linux:~ $ git clone https://github.com/danny-avila/LibreChat.git
linux:~ $ cd LibreChat
linux:~/LibreChat $ cp .env.example .env
linux:~/LibreChat $ cp docker-compose.override.yml.example docker-compose.override.yml
linux:~/LibreChat $ cp librechat.example.yaml librechat.yaml

linux:~/LibreChat $ vi .env
UID=
GID=

linux:~/LibreChat $ vi docker-compose.override.yml      # uncomment to use config / librechat.yaml
# services:
#   api:
#     volumes:
#     - type: bind
#       source: ./librechat.yaml
#       target: /app/librechat.yaml
#     image: ghcr.io/danny-avila/librechat:latest

linux:~/LibreChat $ cp librechat.yaml                   # uncomment to use mcp
# mcpServers:
#   everything:
#     url: http://localhost:3001/sse
#     timeout: 60000  # 1 minute tim

linux:~ $ docker compose up -d
```

---

## test

```bash
linux:~ $ curl http://127.0.0.1:3080
```
