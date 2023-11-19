# rust - oop

---

## content

- [struct](#struct)
  - [struct - function](#struct---function)
  - [strcut - method](#strcut---method)
  - [strcut - static method](#strcut---static-method)
- [enum](#enum)
  - [enum - struct](#enum---struct)
  - [enum - option](#enum---option)
  - [enum - match](#enum---match)
  - [enum - match with option](#enum---match-with-option)
  - [enum - match with data type](#enum---match-with-data-type)
- [module](#module)
  - [mod](#mod)
  - [use](#use)
  - [nested mod](#nested-mod)
- [crate](#crate)
  - [workspace](#workspace)
  - [lib](#lib)
  - [bin](#bin)
  - [run](#run)

---

## struct

```rust
// declare
struct Name_of_structure {
   field1:data_type,
   field2:data_type,
   field3:data_type
}

// initialize
let instance_name = Name_of_structure {
   field1: value1,
   field2: value2,
   field3: value3
};

// method
struct My_struct {}
impl My_struct {
   // define method
   fn method_name() {
      // ...
   }
}

// static method
impl Structure_Name {
   // static method
   fn method_name(param1: datatype, param2: datatype) -> return_type {
      // ... without self
   }
}

// invoke method
Structure_name::method_name(v1,v2)

```

### struct - mutable

```rust
#[derive(Debug)]
struct ProgrammingLanguage {
    lang: String,
    design_by: String,
    age: u32,
}

fn main() {
    let pl1 = ProgrammingLanguage {
        design_by: String::from("Graydon Hoare"),
        lang: String::from("Rust"),
        age: 1,
    };
    println!("{:?}", pl1);

    let mut pl2 = ProgrammingLanguage {
        design_by: String::from("Guido van Rossum"),
        lang: String::from("Python"),
        age: 32,
    };
    pl2.age += 1;
    println!("lang:{}, age: {}", pl2.lang, pl2.age);
}
```

### struct - function

```rust
fn print1(pl: ProgrammingLanguage) {
    println!(
        "lang: {}\ndesign by: {}\nage: {}",
        pl.lang, pl.design_by, pl.age
    );
}

fn print2(pl: &ProgrammingLanguage) {
    println!(
        "lang: {}\ndesign by: {}\nage: {}",
        pl.lang, pl.design_by, pl.age
    );
}

fn create_lang(l: String, d: String) -> ProgrammingLanguage {
    let pl = ProgrammingLanguage {
        lang: l,
        design_by: d,
        age: 1,
    };
    return pl;
}

#[derive(Debug)]
struct ProgrammingLanguage {
    lang: String,
    design_by: String,
    age: u32,
}

fn main() {
    let pl1 = ProgrammingLanguage {
        design_by: String::from("Graydon Hoare"),
        lang: String::from("Rust"),
        age: 1,
    };
    print1(pl1);
    print2(&pl1);

    let mut pl2 = ProgrammingLanguage {
        design_by: String::from("Guido van Rossum"),
        lang: String::from("Python"),
        age: 32,
    };
    print2(&pl2);
    print1(pl2);

    let pl3 = create_lang(String::from("mylang"), String::from("myself"));
    println!("{?:}", pl3);
}
```

### strcut - method

```rust
//define struct
struct Rectangle {
    width: u32,
    height: u32,
}

//implement method
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

fn main() {
    let small = Rectangle {
        width: 10,
        height: 20,
    };

    println!(
        "width: {}\nheight: {}\narea of Rectangle: {}",
        small.width,
        small.height,
        small.area()
    );
}
```

### strcut - static method

```rust
//declare structure
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    // static method
    fn create(x: i32, y: i32) -> Point {
        Point { x: x, y: y }
    }
    // method
    fn display(&self) {
        println!("x: {} y: {}", self.x, self.y);
    }
}
fn main() {
    // invoke static method
    let p1 = Point::create(10, 20);

    // invoke method
    p1.display();
}
```

---

## enum

```rust
enum enum_name {
   variant1,
   variant2,
   variant3
}

// option enum
enum Option<T> {
   Some(T),
   None
   the null keyword
}
```

```rust
#[derive(Debug)]
enum GenderCategory {
    Male,
    Female,
}

fn main() {
    let male = GenderCategory::Male;
    let female = GenderCategory::Female;

    println!("{:?}", male);
    println!("{:?}", female);
}
```

### enum - struct

```rust
#[derive(Debug)]
enum GenderCategory {
    Male,
    Female,
}

#[derive(Debug)]
struct Person {
    name: String,
    gender: GenderCategory,
}

fn main() {
    let p1 = Person {
        name: String::from("Mohtashim"),
        gender: GenderCategory::Male,
    };
    let p2 = Person {
        name: String::from("Amy"),
        gender: GenderCategory::Female,
    };
    println!("{:?}", p1);
    println!("{:?}", p2);
}
```

### enum - option

```rust
fn main() {
    let result = is_even(3);
    println!("{:?}", result);
    println!("{:?}", is_even(30));
}

fn is_even(no: i32) -> Option<bool> {
    if no % 2 == 0 {
        Some(true)
    } else {
        None
    }
}
```

### enum - match

```rust
enum CarType {
    Hatch,
    Sedan,
    SUV,
}

fn print_size(car: CarType) {
    match car {
        CarType::Hatch => {
            println!("Small sized car");
        }
        CarType::Sedan => {
            println!("medium sized car");
        }
        CarType::SUV => {
            println!("Large sized Sports Utility car");
        }
    }
}

fn main() {
    print_size(CarType::SUV);
    print_size(CarType::Hatch);
    print_size(CarType::Sedan);
}
```

### enum - match with option

```rust
fn main() {
    match is_even(5) {
        Some(data) => {
            if data == true {
                println!("Even no");
            }
        }
        None => {
            println!("not even");
        }
    }
}

fn is_even(no: i32) -> Option<bool> {
    if no % 2 == 0 {
        Some(true)
    } else {
        None
    }
}
```

### enum - match with data type

```rust
#[derive(Debug)]
enum GenderCategory {
    Name(String),
    UsrID(i32),
}

fn main() {
    let p1 = GenderCategory::Name(String::from("Mohtashim"));
    let p2 = GenderCategory::UsrID(100);
    println!("{:?}", p1);
    println!("{:?}", p2);

    match p1 {
        GenderCategory::Name(val) => {
            println!("{}", val);
        }
        GenderCategory::UsrID(val) => {
            println!("{}", val);
        }
    }
}
```

---

## module

```rust
// public module
pub mod public_module_name {
    // public function
    pub fn public_function() {}

    // private function
    fn private_function() {}
}

// private module
mod private_module_name {
    fn private_function() {}
}

// import public module
use public_module_name::function_name;
```

### mod

```rust
pub mod movies {
    pub fn play(name: String) {
        println!("Playing movie {}", name);
    }
}
fn main() {
    movies::play("Forrest Gump".to_string());
}
```

### use

```rust
pub mod movies {
    pub fn play(name: String) {
        println!("Playing movie {}", name);
    }
}

use movies::play;

fn main() {
    play("Forrest Gump".to_string());
}
```

### nested mod

```rust
pub mod movies {
    pub mod english {
        pub mod comedy {
            pub fn play(name: String) {
                println!("Playing comedy movie {}", name);
            }
        }
    }
}

use movies::english::comedy::play;

fn main() {
    // short syntax
    play("Life Is Beautiful".to_string());

    //full syntax
    movies::english::comedy::play("3 Idiots".to_string());
}
```

---

## crate

### workspace

```bash
linux:~ $ mkdir add
linux:~ $ cd add

# add member
linux:~/add $ cat << EOF >> Cargo.toml
[workspace]

members = [
    "adder",
    "add_one",
]
EOF
```

### lib

```bash
linux:~/add $ cargo new add_one --lib
linux:~/add $ cargo build
linux:~/add $ tree
.
├── add_one
│   ├── Cargo.toml
│   └── src
│   └── lib.rs
├── Cargo.lock
└── Cargo.toml

# config
linux:~/add $ add_one/Cargo.toml
[package]
name = "add_one"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]

# add below
[lib]
crate-type = ["lib", "dylib"]

# code
linux:~/add $ cat << EOF > add_one/src/lib.rs
pub fn add_one(x: i32) -> i32 {
x + 1
}
EOF
```

```bash
linux:~ $ rustc --help
        --crate-type [bin|lib|rlib|dylib|cdylib|staticlib|proc-macro]
                        Comma separated list of types of crates
                        for the compiler to emit
...
```

### bin

```bash
linux:~/add $ cargo new adder [--bin]

# config
linux:~/add $ cat adder/Cargo.toml
[package]
name = "adder"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]

# add below
add_one = { path = "../add_one" }

# code
linux:~/add $ cat << EOF > adder/src/main.rs
use add_one;

fn main() {
let num = 10;
println!("add_one: {}", add_one::add_one(num));
}
EOF

linux:~/add $ cargo build
linux:~/add $ tree
.
├── adder
│   ├── Cargo.toml
│   ├── src
│   │   └── main.rs
│   └── tags
├── add_one
│   ├── Cargo.toml
│   ├── src
│   │   └── lib.rs
│   └── tags
├── Cargo.lock
└── Cargo.toml
```

### run

```bash
linux:~/add $ cargo run [-p adder]
```

### test

```rust
// add_one/src/lib.rs
pub fn add_one(x: i32) -> i32 {
    x + 1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(3, add_one(2));
    }
}
```

```bash
linux:~/add $ cargo test [-p add_one]
```
