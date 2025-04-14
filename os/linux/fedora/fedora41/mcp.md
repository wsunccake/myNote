# mcp / model context protocol

## architecture

1. MCP Host:

Programs like Claude Desktop, IDEs, or AI tools that want to access data through MCP

2. MCP Client:

Protocol clients that maintain 1:1 connections with servers

- [Claude Desktop](https://claude.ai)
- [Cline](https://github.com/cline/cline)
- [Cherry Studio](https://cherry-ai.com/)
- [awesome-mcp-clients](https://github.com/punkpeye/awesome-mcp-clients)

3. MCP Server

Lightweight programs that each expose specific capabilities through the standardized Model Context Protocol

- [Awesome MCP Servers](https://mcpservers.org/)
- [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
- [servers](https://github.com/modelcontextprotocol/servers)

Local: stdio / Standard Input/Output
Remote: SSE / Server-Sent Events

---

## install

[node](../../../../lang/script/javascript/nodejs/node.md) 在執行 mcp dev 會呼叫 node

```bash
linux:~ $ uv venv
linux:~ $ source .venv/bin/activate

(.venv):~ $ uv pip install "mcp[cli]"
(.venv):~ $ uv run mcp version
```

---

## mcp client

### vscode + cline

### [Time MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/time)

```bash
(.venv):~ $ pip install mcp-server-time
(.venv):~ $ python -m mcp_server_time
```

~/.config/Code/User/globalStorage/xxxxxxxx.claude-dev/settings/

```json
// cline_mcp_settings.json
{
  "mcpServers": {
    "time": {
      "command": "uvx",
      "args": ["mcp-server-time", "--local-timezone=America/New_York"]
    }
  }
}
```

### [fetch-mcp](https://github.com/zcaceres/fetch-mcp)

```bash
linux:~ $ npm -g in tsc
linux:~ $ npm -g in shx

linux:~ $ git clone https://github.com/zcaceres/fetch-mcp
linux:~ $ cd fetch-mcp

linux:~/fetch-mcp $ npm install
linux:~/fetch-mcp $ npm run build
linux:~/fetch-mcp $ npm start
```

```json
// cline_mcp_settings.json
{
  "mcpServers": {
    "fetch": {
      "command": "node",
      "args": ["~/fetch-mcp/dist/index.js"]
    }
  }
}
```

### vscode + cline

```json
// .vscode/mcp.json
{
  "servers": {
    "my-mcp-server": {
      "type": "stdio",
      "command": "uv",
      "args": ["--directory", "~/demo", "run", "server.py"]
    }
  }
}
```

---

## mcp server

### fastmcp

#### local - stdio

```python
# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo", log_level="ERROR")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\\n\\n{code}"

if __name__ == "__main__":
    mcp.run()
    # mcp.run(transport="stdio")
```

```bash
linux:~ $ mkdir demo
linux:~ $ cd demo
linux:~/demo $ uv venv
linux:~/demo $ source .venv/bin/activate

(.venv):~ $ mcp dev server.py

(.venv):~ $ curl http://localhost:6274
```

```json
// cline_mcp_settings.json
{
  "mcpServers": {
    "local-stdio-demo": {
      "disabled": false,
      "timeout": 60,
      "command": "uv",
      "args": ["--directory", "~/demo", "run", "server.py"],
      "transportType": "stdio"
    }
  }
}
```

#### remote - sse

FastMCP 只能使用 host: 0.0.0.0, port: 8000, /sse

```python
# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo", log_level="ERROR")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\\n\\n{code}"

if __name__ == "__main__":
    mcp.run(transport="sse")
```

```bash
linux:~ $ mkdir demo
linux:~ $ cd demo
linux:~/demo $ uv venv
linux:~/demo $ source .venv/bin/activate

(.venv):~ $ python server.py

(.venv):~ $ curl http://localhost:8000
```

```json
// cline_mcp_settings.json
{
  "mcpServers": {
    "remote-sse-demo": {
      "url": "http://127.0.0.1:8000/sse",
      "disabled": false,
      "autoApprove": ["add"]
    }
  }
}
```

### fastmcp with starlette

```python
# server.py
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo", log_level="ERROR")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)

app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)
```

```bash
(.venv):~ $ uvicorn server:app --host 0.0.0.0 --port 8080

curl http://127.0.0.1:8080/sse
```

---

## ref

- [model context protocol](https://modelcontextprotocol.io/introduction)
