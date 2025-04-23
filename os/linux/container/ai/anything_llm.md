# anything llm

## install

```bash
linux:~ # export STORAGE_LOCATION=$HOME/anythingllm
linux:~ # mkdir -p $STORAGE_LOCATION
linux:~ # touch "$STORAGE_LOCATION/.env"
linux:~ # docker run -d -p 3001:3001 \
    --cap-add SYS_ADMIN \
    --name anything-llm \
    -v ${STORAGE_LOCATION}:/app/server/storage \
    -v ${STORAGE_LOCATION}/.env:/app/server/.env \
    -e STORAGE_DIR="/app/server/storage" \
    mintplexlabs/anythingllm
```

## test

```bash
linux:~ $ curl http://localhost:3001
```

## rag

step1. "Instance Settings"

```
"AI Provider"
    "LLM"
        "LLM Provider" -> "Ollama"
                            -> "Ollama Model" -> "nomic-embed-text:latest
                            -> "Max Tokens" -> "8192"
    "Vector Database" -> "LanceDB"
```

step2. "workspace"

make retrieval bette

```
Chat Settings > Prompt

Chat Settings > LLM Temperature

Vector Database Settings > Search Preference

Vector Database Settings > Max Context Snippets

Vector Database Settings > Document similarity threshold
```
