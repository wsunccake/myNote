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

```bash
# crate
linux:~/worksapce $ cargo new --lib restaurant

# code
# edit lib.rs, main.rs

# folder
linux:~/worksapce $ tree restaurant
restaurant
├── Cargo.toml
└── src
    ├── lib.rs
    └── main.rs

# cargo
linux:~/worksapce $ cargo build --manifest-path restaurant/Cargo.toml
linux:~/worksapce $ cargo run   --manifest-path restaurant/Cargo.toml
```

```rs
// lib.rs
pub mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {
            // absolute path
            crate::front_of_house::hosting::seat_at_table(); // same module private function
            crate::front_of_house::serving::take_order(); // diff moudle public function
                                                          // crate::front_of_house::serving::serve_order(); // private function

            // relative path
            seat_at_table(); // same module private function
            self::seat_at_table(); // same module private function
            super::serving::take_order(); // diff moudle public function
            super::super::eat_at_restaurant();
        }
        fn seat_at_table() {
            println!("front_of_house -> hosting -> seat_at_table");
        }
    }

    mod serving {
        pub fn take_order() {
            println!("front_of_house -> serving -> take_order");
        }
        fn serve_order() {}
        fn take_payment() {}
    }
}

#[allow(dead_code)]
mod back_of_house {
    pub struct Breakfast {
        pub toast: String,
        seasonal_fruit: String,
    }

    impl Breakfast {
        pub fn summer(toast: &str) -> Breakfast {
            Breakfast {
                toast: String::from(toast),
                seasonal_fruit: String::from("peaches"),
            }
        }
    }

    #[derive(Debug)]
    pub enum Appetizer {
        Soup,
        Salad,
    }
}

#[allow(dead_code)]
pub fn eat_at_restaurant() {
    // import function
    // crate::front_of_house::hosting::add_to_waitlist(); // absolute path
    // front_of_house::hosting::add_to_waitlist(); // relative path

    // import struct
    let mut meal = back_of_house::Breakfast::summer("Rye");
    meal.toast = String::from("Wheat");
    println!("I'd like {} toast please", meal.toast);

    // import enum
    let order1 = back_of_house::Appetizer::Soup;
    let order2 = back_of_house::Appetizer::Salad;
    println!("order1: {:?}, order2: {:?}", order1, order2);
}

#[allow(dead_code)]
mod customer {
    // use path
    use crate::front_of_house::hosting;
    use std::fmt::Result;
    use std::io::Result as IoResult; // as name

    pub fn eat_at_restaurant() {
        hosting::add_to_waitlist();
    }
}
```

```rs
// main.rs
use restaurant::eat_at_restaurant;

fn main() {
    restaurant::front_of_house::hosting::add_to_waitlist();
    eat_at_restaurant();
}
```

### separate module to file

from [scope path and use module](#scope-path-and-use-module)

```bash
# crate
linux:~/worksapce $ cargo new --lib restaurant

# code
# edit front_of_house.rs, lib.rs, main.rs

# folder
linux:~/worksapce $ tree restaurant
restaurant
├── Cargo.toml
└── src
    ├── front_of_house.rs
    ├── lib.rs
    └── main.rs

# cargo
linux:~/worksapce $ cargo build --manifest-path restaurant/Cargo.toml
linux:~/worksapce $ cargo run   --manifest-path restaurant/Cargo.toml
```

```rs
// front_of_house.rs
pub mod hosting {
    pub fn add_to_waitlist() {
        // absolute path
        crate::front_of_house::hosting::seat_at_table(); // same module private function
        crate::front_of_house::serving::take_order(); // diff moudle public function
                                                      // crate::front_of_house::serving::serve_order(); // private function

        // relative path
        seat_at_table(); // same module private function
        self::seat_at_table(); // same module private function
        super::serving::take_order(); // diff moudle public function
        super::super::eat_at_restaurant();
    }
    fn seat_at_table() {
        println!("front_of_house -> hosting -> seat_at_table");
    }
}

mod serving {
    pub fn take_order() {
        println!("front_of_house -> serving -> take_order");
    }
    fn serve_order() {}
    fn take_payment() {}
}
```

```rs
// lib.rs
pub mod front_of_house;     // front_of_house.rs

#[allow(dead_code)]
mod back_of_house {
    pub struct Breakfast {
        pub toast: String,
        seasonal_fruit: String,
    }

    impl Breakfast {
        pub fn summer(toast: &str) -> Breakfast {
            Breakfast {
                toast: String::from(toast),
                seasonal_fruit: String::from("peaches"),
            }
        }
    }

    #[derive(Debug)]
    pub enum Appetizer {
        Soup,
        Salad,
    }
}

#[allow(dead_code)]
pub fn eat_at_restaurant() {
    // import function
    // crate::front_of_house::hosting::add_to_waitlist(); // absolute path
    // front_of_house::hosting::add_to_waitlist(); // relative path

    // import struct
    let mut meal = back_of_house::Breakfast::summer("Rye");
    meal.toast = String::from("Wheat");
    println!("I'd like {} toast please", meal.toast);

    // import enum
    let order1 = back_of_house::Appetizer::Soup;
    let order2 = back_of_house::Appetizer::Salad;
    println!("order1: {:?}, order2: {:?}", order1, order2);
}

#[allow(dead_code)]
mod customer {
    // use path
    use crate::front_of_house::hosting;
    use std::fmt::Result;
    use std::io::Result as IoResult; // as name

    pub fn eat_at_restaurant() {
        hosting::add_to_waitlist();
    }
}
```

```rs
// main.rs
use restaurant::eat_at_restaurant;

fn main() {
    restaurant::front_of_house::hosting::add_to_waitlist();
    eat_at_restaurant();
}
```

### separate module to folder

from [scope path and use module](#scope-path-and-use-module)

```bash
# crate
linux:~/worksapce $ cargo new --lib restaurant

# code
# edit front_of_house.rs, hosting.rs, serving.rs, lib.rs, main.rs

# folder
linux:~/worksapce $ tree restaurant
 tree restaurant/
restaurant/
├── Cargo.toml
└── src
    ├── front_of_house
    │   ├── hosting.rs
    │   └── serving.rs
    ├── front_of_house.rs
    ├── lib.rs
    └── main.rs

# cargo
linux:~/worksapce $ cargo build --manifest-path restaurant/Cargo.toml
linux:~/worksapce $ cargo run   --manifest-path restaurant/Cargo.toml
```

```rs
// front_of_house.rs
pub mod hosting;
pub mod serving;
```

```rs
// hosting.rs
pub fn add_to_waitlist() {
    // absolute path
    crate::front_of_house::hosting::seat_at_table(); // same module private function
    crate::front_of_house::serving::take_order(); // diff moudle public function
                                                  // crate::front_of_house::serving::serve_order(); // private function

    // relative path
    seat_at_table(); // same module private function
    self::seat_at_table(); // same module private function
    super::serving::take_order(); // diff moudle public function
    super::super::eat_at_restaurant();
}
fn seat_at_table() {
    println!("front_of_house -> hosting -> seat_at_table");
}
```

```rs
// serving.rs
pub fn take_order() {
    println!("front_of_house -> serving -> take_order");
}
fn serve_order() {}
fn take_payment() {}
```

```rs
// lib.rs
pub mod front_of_house;

#[allow(dead_code)]
mod back_of_house {
    pub struct Breakfast {
        pub toast: String,
        seasonal_fruit: String,
    }

    impl Breakfast {
        pub fn summer(toast: &str) -> Breakfast {
            Breakfast {
                toast: String::from(toast),
                seasonal_fruit: String::from("peaches"),
            }
        }
    }

    #[derive(Debug)]
    pub enum Appetizer {
        Soup,
        Salad,
    }
}

#[allow(dead_code)]
pub fn eat_at_restaurant() {
    // import function
    // crate::front_of_house::hosting::add_to_waitlist(); // absolute path
    // front_of_house::hosting::add_to_waitlist(); // relative path

    // import struct
    let mut meal = back_of_house::Breakfast::summer("Rye");
    meal.toast = String::from("Wheat");
    println!("I'd like {} toast please", meal.toast);

    // import enum
    let order1 = back_of_house::Appetizer::Soup;
    let order2 = back_of_house::Appetizer::Salad;
    println!("order1: {:?}, order2: {:?}", order1, order2);
}

#[allow(dead_code)]
mod customer {
    // use path
    use crate::front_of_house::hosting;
    use std::fmt::Result;
    use std::io::Result as IoResult; // as name

    // pub fn eat_at_restaurant() {
    //     hosting::add_to_waitlist();
    // }
}
```

```rs
// main.rs
use restaurant::eat_at_restaurant;

fn main() {
    restaurant::front_of_house::hosting::add_to_waitlist();
    eat_at_restaurant();
}
```
