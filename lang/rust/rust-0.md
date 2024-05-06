# rust - ready

---

## content

- [prepare](#prepare)
  - [install](#install)
  - [auto completion](#auto-completion)
  - [uninstall](#uninstall)
- [editor](#editor)
  - [vim plugin](#vim-plugin)
  - [vscode plugin](#vscode-plugin)
- [run](#run)
- [cargo](#cargo)

---

## prepare

### install

```bash
# prepare
linux:~ # yum group install "Development Tools"     # for centos / rhel
linux:~ # dnf groupinfo "Development Tools"         # for centos / rhel
linux:~ # apt install build-essential               # for debian / ubuntu

# by apt
linux:~ # apt install rust-all                      # for ubuntu

# by rustup
linux:~ $ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash

linux:~ $ source $HOME/.cargo/env
linux:~ $ rustc -h
linux:~ $ rustc -V
```

### auto completion

```bash
# for bash
linux:~ $ rustup completions bash > ~/.local/share/bash-completion/completions/rustup

# for zsh
linux:~ $ rustup completions zsh > ~/.zfunc/_rustup
linux:~ $ vi ~/.zshrc
...
fpath+=~/.zfunc
autoload -Uz compinit
compinit
```

### uninstall

```bash
# by rustup
linux:~ $ rustup self uninstall
```

---

## editor

### vim plugin

```bash
# for vim 8
linux:~ $ git clone https://github.com/rust-lang/rust.vim ~/.vim/pack/plugins/start/rust.vim
```

### vscode plugin

- [rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer)
- [CodeLLDB](https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb)

---

## run

```rust
// main.rs
fn main() {
    println!("Hi rust");
}
```

```bash
linux:~ $ rustc main.rs -o main
linux:~ $ ./main
```

---

## cargo

### hello

```bash
linux:~ $ cargo help
linux:~ $ cargo help new
linux:~ $ cargo -V

# create project
linux:~ $ cargo new hello
linux:~ $ tree hello
hello
├── Cargo.toml
└── src
    └── main.rs

# build binary
linux:~ $ cargo build
linux:~ $ ls target/debug/

# run executable
linux:~ $ cargo run
```

```rust
// hello/src/main.rs
fn main() {
    println!("Hello, world!");
}
```

```toml
# Cargo.toml
[package]
name = "hello"
version = "0.1.0"
edition = "2021"

[dependencies]
```

### command

```bash
linux:~ $ cargo -V      # version
linux:~ $ cargo --list  # list command

linux:~ $ cargo <command> [--help]

linux:~/project $ cargo add <crate>[@<version>]
linux:~/project $ cargo build [-r|--release]
linux:~/project $ cargo run
linux:~/project $ cargo clean
linux:~/project $ cargo fmt
linux:~/project $ cargo test
```

### build specfic Cargo.toml

```bash
linux:~ $ cargo build --manifest-path Cargo.toml
```

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```
