# rust

## install

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

---

## auto completion

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

---

## editor - vim

```bash
# for vim 8
linux:~ $ git clone https://github.com/rust-lang/rust.vim ~/.vim/pack/plugins/start/rust.vim
```

## editor - vscode

(rust-analyzer)[https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer]

(CodeLLDB)[https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb]

---

## test

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

```bash
linux:~ $ cargo -V

linux:~ $ cargo new hello
linux:~ $ tree hello
hello
├── Cargo.toml
└── src
    └── main.rs

1 directory, 2 files

linux:~ $ cat hello/src/main.rs
...

linux:~ $ cat hello/Cargo.toml
...

linux:~ $ cargo build --manifest-path ./hello/Cargo.toml

# usage
linux:~/project $ cargo build [--release]
linux:~/project $ cargo run
linux:~/project $ cargo clean
linux:~/project $ cargo fmt
linux:~/project $ cargo test
```

---

## uninstall

```bash
linux:~ $ rustup self uninstall
```
