# Node Manager

🚀 基本介紹

| tool  | 說明                                                                         |
| ----- | ---------------------------------------------------------------------------- |
| `nvm` | 最早且最常用的 Node.js 管理工具，Bash 為主，支援 macOS/Linux                 |
| `fnm` | 以 Rust 開發，主打 **速度快**、**支援 Windows/macOS/Linux**，相容 `nvm` 語法 |

🖥 系統支援

| 作業系統      | `fnm`             | `nvm`                                       |
| ------------- | ----------------- | ------------------------------------------- |
| macOS / Linux | ✅ 支援           | ✅ 支援                                     |
| Windows       | ✅（透過 native） | 🚫（非官方支援，只能用 `nvm-windows` 替代） |

⚙️ 安裝速度與執行效率

| item                  | `fnm`                        | `nvm`                                         |
| --------------------- | ---------------------------- | --------------------------------------------- |
| **安裝速度**          | 🚀 快（Rust 編譯，並行下載） | 🐢 較慢（shell + curl）                       |
| **切換版本速度**      | 🚀 即時切換                  | 🐢 較慢，每次切換重新載入環境變數             |
| **啟動 shell 時影響** | 幾乎無延遲                   | 有些延遲，特別是 `.bashrc` 或 `.zshrc` 載入時 |

🧰 常用語法比較

| 功能           | `nvm`                  | `fnm`            |
| -------------- | ---------------------- | ---------------- |
| 安裝版本       | `nvm install 18`       | `fnm install 18` |
| 使用版本       | `nvm use 18`           | `fnm use 18`     |
| 設定預設版本   | `nvm alias default 18` | `fnm default 18` |
| 顯示版本列表   | `nvm ls`               | `fnm list`       |
| 目前使用中版本 | `nvm current`          | `fnm current`    |

🧩 特色比較

| 特性                             | `fnm`                   | `nvm`                       |
| -------------------------------- | ----------------------- | --------------------------- |
| 支援 `.node-version` / `.nvmrc`  | ✅                      | ✅                          |
| 自動切換 Node 版本（進入資料夾） | ✅（需加上 shell hook） | ❌（需手動 `nvm use`）      |
| 原生 Windows 支援                | ✅                      | ❌（需用 nvm-windows 替代） |
| 佈署速度快（CI/CD）              | ✅                      | ❌                          |
| 記憶體佔用低                     | ✅                      | ❌（Shell Script 開銷較大） |

---

## nvm / Node Version Manager

### install

```bash
# install
linux:~ $ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
linux:~ $ vi ~/.bashrc
...
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# uninstall
linux:~ $ nvm unload
```

### usage

```bash
# usage
linux:~ $ nvm --version
linux:~ $ nvm ls
linux:~ $ nvm ls-remote
linux:~ $ nvm install [--lts] [<version>]
linux:~ $ nvm use <version>

# example
linux:~ $ nvm install --lts [v18.12.0]
linux:~ $ nvm install v18.12.0
```

---

## fnm / Fast Node Manager

### install

```bash
linux:~ $ curl -fsSL https://fnm.vercel.app/install | bash
linux:~ $ vi ~/.bashrc
...
FNM_PATH="/home/tux/.local/share/fnm"
if [ -d "$FNM_PATH" ]; then
  export PATH="$FNM_PATH:$PATH"
  eval "`fnm env`"
fi

linux:~ $ fnm completions --shell <SHELL>
# <SHELL>: bash, zsh, fish, powershell
linux:~ $ fnm completions --shell bash > ~/.fnm-completion.bash      # for bash
linux:~ $ echo "source ~/.fnm-completion.bash" >> ~/.bashrc
```

### usage

```bash
linux:~ $ fnm list-remote
linux:~ $ fnm list

linux:~ $ fnm install <version>
linux:~ $ fnm use <version>
```
