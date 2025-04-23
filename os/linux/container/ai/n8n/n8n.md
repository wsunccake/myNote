# n8n / nodemation

## install

method 1. by nodejs

```bash
linux:~ $ npm install n8n   # 1.71
linux:~ $ npm x n8n         # run n8n
```

method 2. by docker

```bash
linux:~ $ docker volume create n8n_data

linux:~ $ docker run -itd \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:$HOME/.n8n \
  -e N8N_HOST=0.0.0.0 \
  -e N8N_SECURE_COOKIE=false \
  docker.n8n.io/n8nio/n8n
```

## test

```bash
linux:~ $ curl http://localhost:5678
```

## example
