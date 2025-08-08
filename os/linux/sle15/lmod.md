# lmod - lua-based environment modules

在高效能運算（HPC / High Performance Computing）領域，如何讓多個使用者同時使用不同版本的軟體，這是共用系統中常見的痛點

1. `Environment Modules` (1990 年代初)

Environment Modules 是模組管理系統的先驅，它在 1990 年代初期問世，為高效能運算環境解決了軟體版本管理的一大難題。

- 核心思想： 透過簡單的 module 指令，動態地修改使用者的 shell 環境變數。每個軟體版本都有一個對應的 模組檔案 (modulefile)，這個檔案用 Tcl 語言撰寫，定義了載入該軟體時需要做的所有環境變數設定。
- 基本指令：
  - module avail：列出所有可用的軟體模組。
  - module load <模組名稱>：載入一個軟體模組，自動更新 $PATH、$LD_LIBRARY_PATH 等變數。
  - module list：查看目前已載入的模組清單。
  - module switch <舊模組> <新模組>：快速在不同版本的模組之間切換。
  - module purge：清除所有已載入的模組，回到乾淨的環境。
- 相容性： 支援多種常見的 shell，例如 bash、tcsh、zsh 等。
- 優點： 由於其簡單、靈活的設計，Environment Modules 在很長一段時間內都是 HPC 領域的標準，讓使用者和系統管理員都能有效率地管理軟體版本。

2. `Lmod` (約 2010 年)

Lmod 是由德州大學奧斯汀分校 (TACC) 的 Robert McLay 所開發，被視為 Environment Modules 的現代化、高效能替代方案。它的誕生是為了應對傳統系統在面對日益龐大與複雜的 HPC 環境時所遇到的挑戰。

- 基於 Lua 語言：
  - Lmod 模組檔案是用 Lua 語言撰寫的，這是一種輕量、快速且高效能的腳本語言。
  - Lmod 在處理數千個模組檔案時，module avail 等指令的執行速度遠快於傳統的 Tcl-based 系統。
  - 相容性： Lmod 能夠讀取並執行舊有的 Tcl 模組檔案，確保了良好的向下相容性。
- 革命性的軟體分層架構 (Software Hierarchy)：
  - 這是 Lmod 最重要的功能之一。在 HPC 叢集上，軟體有複雜的相依性，例如一個應用程式可能需要特定版本的編譯器和 MPI 函式庫。
  - 傳統系統會一次性顯示所有可用的模組，清單龐大且容易出錯。
  - Lmod 的分層架構會根據你目前已載入的模組，智慧地過濾 module avail 的結果。當你載入了一個編譯器，它只會顯示所有依賴於該編譯器的軟體。這使得使用者能直觀地遵循正確的載入順序。
- 使用者體驗優化：
  - ml 指令： 提供了 module 指令的簡寫 ml，讓輸入更快速。
  - 自動切換 (Autoswap)： 當你載入一個與當前已載入模組衝突的新模組時（例如從 Python 2 切換到 Python 3），Lmod 會自動卸載舊模組並載入新模組，使用者無需手動操作。

| 特性     | Tcl modulefile                                                               | Lua modulefile                                        |
| -------- | ---------------------------------------------------------------------------- | ----------------------------------------------------- |
| 系統     | 主要用於 Environment Modules。                                               | Lmod 的原生格式。                                     |
| 腳本語言 | Tcl (Tool Command Language)。                                                | Lua (輕量級腳本語言)。                                |
| 執行效率 | 較慢，因為 Lmod 需要將 Tcl 檔案轉換為 Lua 才能執行。                         | 極快，Lmod 可直接執行，並且快取模組資訊。             |
| 檔案命名 | 通常沒有副檔名。                                                             | 建議使用 .lua 作為副檔名，以明確區分。                |
| 語法     | setenv VAR value、prepend-path。                                             | setenv("VAR", "value")、prepend_path()。              |
| 功能     | 較為基礎，主要集中在環境變數設定。                                           | 更強大，支援軟體分層、動態判斷、pathJoin 等進階功能。 |
| 相容性   | Lmod 可以讀取 Tcl 模組檔案，但傳統 Environment Modules 不支援 Lua 模組檔案。 | 只能被 Lmod 系統原生讀取。                            |

---

## install

```bash
sle:~ # zypper in lua-lmod
```

---

## usage

```bash
sle:~ # echo $MODULEPATH

sle:~ # module help
sle:~ # ml help                 # ml 同 module

sle:~ # ml list
sle:~ # ml avail                # ml av

sle:~ # ml add <module>         # ml load <module>
sle:~ # ml del <module>         # ml unload <module>
sle:~ # ml whatis <module>
sle:~ # ml show <module>
```

---

## example

```bash
# package
sle:~ # mkdir -p /usr/local/hello/{v1,v2}
sle:~ # echo -e '#!/bin/bash\necho "hello v1"' > /usr/local/hello/v1/hello
sle:~ # echo -e '#!/bin/bash\necho "hello v2"' > /usr/local/hello/v2/hello

sle:~ # tree -a /usr/local/hello/
/usr/local/hello/
├── v1
│   └── hello
└── v2
    └── hello

# modulefile
sle:~ # mkdir -p /usr/share/lmod/modulefiles/hello
sle:~ # vi /usr/share/lmod/modulefiles/hello/v1
sle:~ # vi /usr/share/lmod/modulefiles/hello/v2.lua

sle:~ # tree /usr/share/lmod/modulefiles/hello/
/usr/share/lmod/modulefiles/hello/
├── v1
└── v2.lua
```

```tcl
#%Module1.0
## Tcl-based modulefile
## v1

set version v1
set root /usr/local/hello/$version

prepend-path PATH            $root:$root/bin
prepend-path LD_LIBRARY_PATH $root/lib

setenv HELLO_HOME $root

module-whatis "This is hello version $version, written in Tcl."
```

```lua
--
-- Lua-based modulefile
-- v2.lua

local version = "v2"
local root = "/usr/local/hello/" .. version

prepend_path("PATH", root)
prepend_path("PATH", pathJoin(root, "bin"))
prepend_path("LD_LIBRARY_PATH", pathJoin(root, "lib"))

setenv("HELLO_HOME", root)

whatis("This is hello version " .. version .. ", written in Lua.")
```

---

## sh convert to modulefile

```sh
#!/bin/bash
# foo.sh

APP_ROOT=/opt/my_app/1.2.0

export PATH=$APP_ROOT/bin:$PATH
export LD_LIBRARY_PATH=$APP_ROOT/lib:$LD_LIBRARY_PATH
export MY_APP_VERSION=1.2.0

echo "Environment for my_app 1.2.0 has been set."
```

```bash
sle:~ # $LMOD_DIR/sh_to_modulefile foo.sh > foo.lua
```

---

## hpc lmod plugin

```bash
sle:~ # zypper se '*-hpc'
sle:~ # zypper info gnu-compilers-hpc
sle:~ # zypper info python3-numpy-gnu-hpc
sle:~ # zypper info python3-scipy-gnu-hpc
```
