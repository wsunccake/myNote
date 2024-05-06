# crate example

## content

- [workspace](#workspace)
- [bin](#bin)
  - [single bin](#single-bin)
  - [multi bin](#multi-bin)
- [lib](#lib)
  - [lazy lib](#lazy-lib)
  - [local lib](#local-lib)
  - [scope path and use module](#scope-path-and-use-module)
  - [separate module to file](#separate-module-to-file)
  - [separate module to folder](#separate-module-to-folder)

---

## workspace

```bash
# crate
linux:~/worksapce $ cargo new cli
linux:~/worksapce $ cargo new gui

# config
linux:~/worksapce $ vi Cargo.toml

# folder
linux:~/worksapce $ tree
.
├── Cargo.toml
├── cli
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── gui
    ├── Cargo.toml
    └── src
        └── main.rs

# cargo
linux:~/worksapce $ cargo build             # build binary
linux:~/worksapce $ cargo run --bin cli     # run specific binary
linux:~/worksapce $ cargo run --bin cli     # run specific binary
```

```conf
# Cargo.toml
[workspace]

members = [
    "cli",
    "gui",
]
```

---

## bin

### single bin

```bash
# crate
linux:~/worksapce $ cargo new demo --bin

# folder
linux:~/worksapce $ tree demo
demo
├── Cargo.toml      # config
└── src
    └── main.rs     # code

# cargo
linux:~/worksapce $ cargo run --manifest-path demo/Cargo.toml       # run binary
linux:~/worksapce $ cargo build --manifest-path demo/Cargo.toml     # build binary
```

```rs
// main.rs
fn main() {
    println!("Hello, world!");
}
```

```conf
# Cargo.toml
[package]
name = "demo"
version = "0.1.0"
edition = "2021"

[dependencies]
```

### multi bin

```bash
linux:~/worksapce $ cargo new demo --bin

# edit hey.rs, hi.rs, Cargo.toml

# folder
linux:~/worksapce $ tree demo
demo
├── Cargo.toml      # config
└── src             # code
    ├ hey.rs
    ├ hi.rs
    └── main.rs

# cargo
## build specific binary
linux:~/worksapce $ cargo build --bin demo --manifest-path demo/Cargo.toml
linux:~/worksapce $ cargo build --bin hi   --manifest-path demo/Cargo.toml
linux:~/worksapce $ cargo build --bin hey  --manifest-path demo/Cargo.toml

## build all binary
linux:~/worksapce $ cargo build --bins     --manifest-path demo/Cargo.toml

## run specific binary
linux:~/worksapce $ cargo run --bin demo   --manifest-path demo/Cargo.toml
linux:~/worksapce $ cargo run --bin hi     --manifest-path demo/Cargo.toml
linux:~/worksapce $ cargo run --bin hey    --manifest-path demo/Cargo.toml
```

```rs
// hi.rs
fn main() {
    println!("Hi, rust!");
}
```

```rs
// hey.rs
fn main() {
    println!("Hey, rust!");
}
```

```conf
# Cargo.toml
[package]
name = "demo"
version = "0.1.0"
edition = "2021"

[[bin]]
name = "hi"
path = "src/hi.rs"

[[bin]]
name = "hey"
path = "src/hey.rs"

[dependencies]
```

---

## lib

## lazy lib

```bash
# crate
linux:~/worksapce $  cargo new app --bin
linux:~/worksapce $  mkdir app/src/garden

# code
# edit app/src/garden/vegetables.rs, app/src/garden.rs, app/src/main.rs

# folder
linux:~/worksapce $ tree app
app
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs

# cargo
linux:~/worksapce $ cargo run --manifest-path app/Cargo.tom
```

```rs
// app/src/garden/vegetables.rs
#[derive(Debug)]
pub struct Asparagus {}
```

```rs
// app/src/garden.rs
pub mod vegetables;
```

```rs
// app/src/main.rs
use crate::garden::vegetables::Asparagus;

pub mod garden;

fn main() {
    let plant = Asparagus {};
    println!("I'm growing {:?}!", plant);
}
```

### local lib

```bash
###
### create crate lib
###

# crate
linux:~/worksapce $ cargo new add --lib

# folder
linux:~/worksapce $ tree add
add
├── Cargo.toml
└── src
    └── lib.rs

# config
linux:~/worksapce $ cat add/Cargo.toml

# code
linux:~/worksapce $ cat add/src/lib.rs

# cargo
linux:~/worksapce $ cargo build --lib  --manifest-path add/Cargo.toml
linux:~/worksapce $ cargo test         --manifest-path add/Cargo.toml

###
### import crate lib
###

# crate
linux:~/worksapce $ cargo new demo --bin

# config
linux:~/worksapce $ cat demo/Cargo.toml

# code
linux:~/worksapce $ cat demo/src/main.rs

# cargo
linux:~/worksapce $ cargo run    --manifest-path demo/Cargo.toml
```

```conf
# add/Cargo.toml
[package]
name = "add"
version = "0.1.0"
edition = "2021"

[dependencies]
```

```rs
// add/src/lib.rs
pub fn add(left: usize, right: usize) -> usize {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
```

```conf
# demo/Cargo.toml
[package]
name = "demo"
version = "0.1.0"
edition = "2021"

[dependencies]
add = { path = "../add" }
```

```rs
// demo/src/main.rs
use add::add;

fn main() {
    println!("Hello, world!");
    println!("{:#?}", add(1, 2));
}
```

### scope path and use module

### separate module to file

### separate module to folder
