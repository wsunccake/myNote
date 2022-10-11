# install

```bash
linux:~ # yum group install "Development Tools"     # for centos / rhel
linux:~ # dnf groupinfo "Development Tools"         # for centos / rhel
linux:~ # apt install build-essential               # for debian / ubuntu

linux:~ $ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash

linux:~ $ source $HOME/.cargo/env
linux:~ $ rustc -h
linux:~ $ rustc -V
```


---

# test

```bash
linux:~ $ cat << EOF > main.rs
fn main() {
    println!("Hi rust");
}
EOF

linux:~ $ rustc main.rs -o main
linux:~ $ ./main
```


---

# cargo

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
fn main() {
    println!("Hello, world!");
}

linux:~ $ cat Cargo.toml
[package]
name = "hello"
version = "0.1.0"
edition = "2021"

[dependencies]

linux:~ $ cargo build
linux:~ $ cargo run
linux:~ $ cargo clean
```


---

# uninstall

```bash
linux:~ $ rustup self uninstall
```
