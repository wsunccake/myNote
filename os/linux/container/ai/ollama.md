# ollama

## install

```bash
linux:~ # OLLAMA_MODEL=<path>
linux:~ # mkdir -p $OLLAMA_MODEL

# only cpu
linux:~ # docker run -d -v $OLLAMA_MODEL:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# nvidia gpu
linux:~ # docker run -d --gpus=all -v $OLLAMA_MODEL:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

## usage

```bash
linux:~ # docker exec -it ollama list
linux:~ # docker exec -it ollama run llama3.2
```

[Ollama Models](https://ollama.com/search)
