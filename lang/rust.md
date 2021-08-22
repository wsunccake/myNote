# rust

## install

```bash
[linux:~ ] # curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
[linux:~ ] # source $HOME/.cargo/env

[linux:~ ] # rustup update              # update
[linux:~ ] # rustup self uninstall      # uninstall
[linux:~ ] # rustc --version            # version
```


---

## hello world

```bash
[linux:~ ] # cat << EOF > main.rs
fn main() {
    println!("Hello, world!");
}
EOF

[linux:~ ] # rustc main.rs
[linux:~ ] # ./main
```


---

## cargo

cargo: package manager

```bash
[linux:~ ] # cargo --version
[linux:~ ] # cargo new hello_cargo
[linux:~ ] # cd hello_cargo
[linux:~/hello_cargo ] # cat Cargo.toml
[linux:~/hello_cargo ] # cat << EOF > src/main.rs
fn main() {
    println!("Hello, world!");
}
EOF
[linux:~/hello_cargo ] # cargo build
[linux:~/hello_cargo ] # cargo run
[linux:~/hello_cargo ] # cargo check
```
