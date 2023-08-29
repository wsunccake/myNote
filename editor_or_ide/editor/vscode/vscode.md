# vscode

## shortcut

```
command palette: Ctrl + Shift + P
keyboard shortcut: Ctrl + K Ctrl + S

show explorer: Ctrl + Shift + E
show search: Ctrl + Shift + F
show control: Ctrl + Shift + G
show run: Ctrl + Shift + D
show extensions: Ctrl + Shift + X

go to file: Ctrl + P
find: Ctrl + F
replace: Ctrl + H
next match: Ctrl + D

toggle terminal: Ctrl + `
toggle sidebar: Ctrl + B
show panel: Ctrl + J

add cursor above: Shift + Alt + UpArrow
add cursor below: Shift + Alt + DownArrow
```

---

## settings.json

```
    "editor.fontSize": 14,
    "editor.fontFamily": "Fira Code",
    "editor.formatOnType": true,
    "editor.insertSpaces": true,
    "editor.rulers": [
        {
            "column": 80,
            "color": "#ff9900"
        },
        {
            "column":100,
            "color":"#fbff11"
        },
        {
            "column": 120,
            "color": "#9f0af5"
        },
    ],
    "editor.minimap.enabled": false,
    "editor.wordWrap": "on",

    "files.autoSave": "afterDelay",
    "files.eol": "\n",
    "files.trimTrailingWhitespace": true,

    "terminal.integrated.fontSize": 14,
```

---

## launch.json

---

## tasks.json

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Hello",
      "type": "shell",
      "command": "echo hello",
      "problemMatcher": []
    },
    {
      "label": "My Task",
      "type": "shell",
      "command": "${file}",
      "problemMatcher": []
    },
    {
      "label": "echo predefine variable",
      "command": "echo",
      "args": ["${env:USERNAME}", "workspaceFolder = ${workspaceFolder}"],
      "type": "shell"
    }
  ]
}
```

---

## plugin

### general

[Material Theme](https://marketplace.visualstudio.com/items?itemName=Equinusocio.vsc-material-theme)

ext install Equinusocio.vsc-material-theme

[Git Graph](https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph)

ext install mhutchie.git-graph

[Path Intellisense](https://marketplace.visualstudio.com/items?itemName=christian-kohler.path-intellisense)

ext install christian-kohler.path-intellisense

[indent-rainbow](https://marketplace.visualstudio.com/items?itemName=oderwat.indent-rainbow)

ext install oderwat.indent-rainbow

[Bracket Pair Colorizer 2](https://marketplace.visualstudio.com/items?itemName=CoenraadS.bracket-pair-colorizer-2)

ext install CoenraadS.bracket-pair-colorizer-2

[FiraCode](https://github.com/tonsky/FiraCode)

[Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)

[Prettier - Code formatter](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)

ext install esbenp.prettier-vscode

### javascript/node

[ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)

ext install dbaeumer.vscode-eslint

[Node.js Modules Intellisense](https://marketplace.visualstudio.com/items?itemName=leizongmin.node-module-intellisense)

ext install leizongmin.node-module-intellisense

[Visual Studio IntelliCode](https://marketplace.visualstudio.com/items?itemName=VisualStudioExptTeam.vscodeintellicode)

ext install VisualStudioExptTeam.vscodeintellicode

---

## other

"Visual Studio Code is unable to watch for file changes in this large workspace" (error ENOSPC)

```bash
linux:~ # cat /proc/sys/fs/inotify/max_user_watches
linux:~ # sysctl fs.inotify.max_user_watches

linux:~ # sysctl -w fs.inotify.max_user_watches=524288
linux:~ # echo "fs.inotify.max_user_watches=524288" >> /etc/sysctl.conf
linux:~ # sysctl -p /etc/sysctl.conf
```
