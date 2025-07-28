# gemini cli

## install

prerequisites: node.js 18+

```bash
# for debian
debian:~ $ npm install -g @google/gemini-cli

# for windows
PS C:\Users\user> npm install -g @google/gemini-cli
```

---

## setting

Generate a key from [Google AI Studio](https://aistudio.google.com/apikey)

```bash
debian:~ $ export GEMINI_API_KEY="<API_KEY>"
debian:~ $ npm -g x gemini

debian:~ $ gemini -p "hello gemini cli"
```

## usage

```bash
> /help
╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                        │
│ Basics:                                                                                                                                                │
│ Add context: Use @ to specify files for context (e.g., @src/myFile.ts) to target specific files or folders.                                            │
│ Shell mode: Execute shell commands via ! (e.g., !npm run start) or use natural language (e.g. start server).                                           │
│                                                                                                                                                        │
│ Commands:                                                                                                                                              │
│  /help - for help on gemini-cli                                                                                                                        │
│  /docs - open full Gemini CLI documentation in your browser                                                                                            │
│  /clear - clear the screen and conversation history                                                                                                    │
│  /theme - change the theme                                                                                                                             │
│  /auth - change the auth method                                                                                                                        │
│  /editor - set external editor preference                                                                                                              │
│  /stats - check session stats                                                                                                                          │
│  /mcp - list configured MCP servers and tools                                                                                                          │
│  /memory - manage memory. Usage: /memory <show|refresh|add> [text for add]                                                                             │
│  /tools - list available Gemini CLI tools                                                                                                              │
│  /about - show version info                                                                                                                            │
│  /bug - submit a bug report                                                                                                                            │
│  /chat - Manage conversation history. Usage: /chat <list|save|resume> [tag]                                                                            │
│  /quit - exit the cli                                                                                                                                  │
│  /compress - Compresses the context by replacing it with a summary.                                                                                    │
│  ! - shell command                                                                                                                                     │
│                                                                                                                                                        │
│ Keyboard Shortcuts:                                                                                                                                    │
│ Enter - Send message                                                                                                                                   │
│ Shift+Enter - New line                                                                                                                                 │
│ Up/Down - Cycle through your prompt history                                                                                                            │
│ Alt+Left/Right - Jump through words in the input                                                                                                       │
│ Esc - Cancel operation                                                                                                                                 │
│ Ctrl+C - Quit application                                                                                                                              │
│                                                                                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

```bash
$ tree
ℹ .
  └── gemini.md
```

---

## ref

- [gemini cli](https://github.com/google-gemini/gemini-cli)
- [歡迎使用 Gemini CLI 使用手冊](https://gemini-cli.gh.miniasp.com/)
