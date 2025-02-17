# texlive

## install

```bash
linux:~ # apt install texlive-base          # base package
linux:~ # apt install texlive-latex-base    # pdflatex

linux:~ # apt install texlive-xetex         # xelatex (support utf-8)

linux:~ # apt install texlive-latex-extra
linux:~ # apt install texlive-full          # full package
```

---

## test

```bash
linux:~ $ tex '\empty Hello world!\bye'     # texput.dvi, texput.log
linux:~ $ pdftex '\empty Hello world!\bye'  # texput.pdf, texput.log
```

---

## manager

```bash
linux:~ $ tlmgr --version
linux:~ $ tlmgr --help

linux:~ $ tlmgr init-usertree     # $HOME/texmf
# export TEXMFHOME=~/texmf

linux:~ $ tlmgr info collections
linux:~ $ tlmgr list [--only-installed]
linux:~ $ tlmgr
```

---

## typesetter

```
.tex -> .dvi -> .pdf
```

```tex
% hello.tex
\documentclass{article}
\begin{document}

Hello, World!

\end{document}
```

```bash
linux:~ $ tex hello.tex         # tex -> dvi
linux:~ $ xdvi hello.dvi        # display on monitor
linux:~ $ dvipdf hello.dvi      # dvi -> pdf

linux:~ $ pdflatex hello.tex    # tex -> pdf

linux:~ $ xelatex hello.tex     # tex -> pdf
```

---

## circuitikz

| 符號 | 意義                        |
| ---- | --------------------------- |
| --   | 直接畫一條線。              |
| o-   | 起點有開放圓圈（open）      |
| \*-  | 起點有封閉圓圈（solid dot） |
| -\*  | 終點有封閉圓圈（solid dot） |
| o-\* | 兩端開放圓圈和封閉圓圈組合  |

```
short 畫一條導線
V 電壓標記

[short, i_ = ...]
i_ = ... 標記該設置的電流(小寫的電流變數)
I_ = ... 標記該設置的電流(大寫的電流變數)
l_ = ... 標記該設置的下標對齊方式。
```
