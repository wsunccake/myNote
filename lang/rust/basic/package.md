# package

## mod

```bash
.
├── Cargo.toml
└── src
    ├── lib
    │   ├── mod.rs
    │   └── util.rs
    ├── main.rs
    └── my.rs

2 directories, 5 files
```

```rust
// src/lib/mod.rs
pub mod util;

```

```rust
// src/lib/util.rs
pub mod greetings {
    pub fn hi() {
        println!("util - greeting - hi");
    }
}

pub fn hi() {
    println!("util - hi");
}
```

```rust
// src/my.rs
pub mod greetings {
    pub fn hi() {
        println!("my - greetings - hi");
    }
}

pub fn hi() {
    println!("my - hi");
}
```

```rust
// src/main.rs
fn hi() {
    println!("hi");
}

mod say {
    pub fn hi() {
        println!("say - hi");
    }
}

mod lib;
mod my;

fn main() {
    hi();
    say::hi();

    my::hi();
    my::greetings::hi();

    lib::util::hi();
    lib::util::greetings::hi();
}
```

---

## crate

```bash
.
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs

2 directories, 4 files
```

```rust
// garden/vegetables.rs
#[derive(Debug)]
pub struct Asparagus {}
```

```rust
// src/garden.rs
pub mod veget
```

```rust
// src/main.rs
use crate::garden::vegetables::Asparagus;

pub mod garden;

fn main() {
    let plant = Asparagus {};
    println!("I'm growing {:?}!", plant);
}
```

---

## package

```bash
.
├── Cargo.toml
└── src
    ├── lib.rs
    └── main.rs

1 directory, 3 files
```

```toml
[package]
name = "hi"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
```

```rust
// src/lib.rs
pub fn hi() {
    println!("lib - hi");
}
```

```rust
// src/main.rs
fn main() {
    hi::hi();
}
```
