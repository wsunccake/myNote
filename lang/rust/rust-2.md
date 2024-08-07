# rust - oop / object-oriented programming

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
- [trait](#trait)
  - [trait - struct](#trait---struct)
  - [trait - function](#trait---function)
  - [trait - where](#trait---where)
  - [trait - default method](#trait---default-method)
- [allocate memory](#allocate-memory)
  - [memory allocation](#memory-allocation)
  - [static allocation](#static-allocation)
  - [stack allocation](#stack-allocation)
  - [heap allocation](#heap-allocation)
  - [box](#box)
  - [data representation](#data-representation)
  - [data size](#data-size)
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

```rs
// as_ref:
Option<T>, &Option<T>, &mut Option<T> => Option<&T>

// as_mut:
Option<T>, &mut Option<T> => Option<&mut T>
&Option<T> !=> Option<&mut T>

// take: take out ownership
let n = p.take(); // n get p ownership then p => None
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

## trait

### trait - struct

```rust
struct Triangle {
    base: f64,
    height: f64,
}
trait HasArea {
    fn area(&self) -> f64;
}

impl HasArea for Triangle {
    fn area(&self) -> f64 {
        0.5 * (self.base * self.height)
    }
}
fn main() {
    let a = Triangle {
        base: 10.5,
        height: 17.4,
    };
    let triangle_area = a.area();
    println!("area: {}", triangle_area);
}
```

### trait - function

```rust
trait HasArea {
    fn area(&self) -> f64;
}
struct Triangle {
    base: f64,
    height: f64,
}

impl HasArea for Triangle {
    fn area(&self) -> f64 {
        0.5 * (self.base * self.height)
    }
}
struct Square {
    side: f64,
}

impl HasArea for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }
}

// fn area<T>(item: T) {
//     println!("area: {}", item.area());
// }

fn area<T: HasArea>(item: T) {
    println!("area: {}", item.area());
}

fn main() {
    let a = Triangle {
        base: 10.5,
        height: 17.4,
    };
    let b = Square { side: 4.5 };

    area(a);
    area(b);
}
```

```rs
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        println!("run Rectangle Area");
        self.width * self.height
    }
}

trait HasArea {
    fn area(&self) -> u32;
}

impl HasArea for Rectangle {
    fn area(&self) -> u32 {
        println!("run trait HasArea");
        self.width * self.height
    }
}

fn print_area<T: HasArea>(t: T) {
    println!("print area");
    t.area();
}

fn main() {
    let r = Rectangle {
        width: 1,
        height: 2,
    };
    println!("area: {}", r.area());
    println!("area: {}", HasArea::area(&r));
    print_area(r);
}
```

### trait - where

```rust
trait Perimeter {
    fn a(&self) -> f64;
}
struct Square {
    side: f64,
}
impl Perimeter for Square {
    fn a(&self) -> f64 {
        4.0 * self.side
    }
}
struct Rectangle {
    length: f64,
    breadth: f64,
}
impl Perimeter for Rectangle {
    fn a(&self) -> f64 {
        2.0 * (self.length + self.breadth)
    }
}

// fn print_perimeter<Square: Perimeter, Rectangle: Perimeter>(s: Square, r: Rectangle)
fn print_perimeter<Square, Rectangle>(s: Square, r: Rectangle)
where
    Square: Perimeter,
    Rectangle: Perimeter,
{
    let r1 = s.a();
    let r2 = r.a();
    println!("Perimeter of a square is {}", r1);
    println!("Perimeter of a rectangle is {}", r2);
}

fn main() {
    let sq = Square { side: 6.2 };
    let rect = Rectangle {
        length: 3.2,
        breadth: 5.6,
    };
    print_perimeter(sq, rect);
}
```

### trait - default method

```rust
trait Sample {
    fn a(&self);
    fn b(&self) {
        println!("Print b");
    }
}

struct Example {
    a: i32,
    b: i32,
}

impl Sample for Example {
    fn a(&self) {
        println!("Value of a is {}", self.a);
    }

    fn b(&self) {
        println!("Value of b is {}", self.b);
    }
}

fn main() {
    let r = Example { a: 5, b: 7 };
    r.a();
    r.b();
}
```

---

## allocate memory

### memory allocation

- In processor register
- Static
- In the stack
- In the heap

### static allocation

```rust
fn main() {
    static _V: i32 = 3;
    let _v = 3;

    // 1. static use static allocation
    //    let use stack allocation
    // 2. static requires the explicit specification of the type of the variable
    //    optional using let
    // 3. normal code cannot change the value of a static variable
    //    even if it has the mut specification
    //    for safety reason, in Rust static variables are normally immutable
}
```

### stack allocation

```rust
const SIZE: usize = 100_000;
const N_ARRAY: usize = 1_000_000;

fn create_array() -> [u8; SIZE] {
    [0u8; SIZE]
}

fn recursive_func(n: usize) {
    let a = create_array();
    println!("{} {}", N_ARRAY - n + 1, a[0]);
    if n > 1 {
        recursive_func(n - 1)
    }
}

fn main() {
    let v = N_ARRAY;
    recursive_func(v);
}
```

### heap allocation

```rust
const SIZE: usize = 100_000;
const N_ARRAY: usize = 1_000_000;
fn create_array() -> Box<[u8; SIZE]> {
    Box::new([0u8; SIZE])
}
fn recursive_func(n: usize) {
    let a = create_array();
    println!("{} {}", N_ARRAY - n + 1, a[0]);
    if n > 1 {
        recursive_func(n - 1)
    }
}

fn main() {
    let v = N_ARRAY;
    recursive_func(v);
}
```

### box

```rust
fn f(p: &f64) {
    let a = Box::new(*p);
    {
        let b = Box::new([1, 2, 3]);
        println!("{} {:?}", *a, *b);
    }
    let c = Box::new(true);
    println!("{} {}", a, c);
}

fn main() {
    f(&3.14);
}
```

```rust
fn main() {
    let a = 7;
    let a_box: Box<i32>;
    let mut a_ref: &i32 = &a;

    println!(
        "value   =>  a: {:16}, *a_ref: {:16}, a_ref: {:16}",
        a, *a_ref, a_ref
    );
    println!(
        "address => &a: {:16p}, &a_ref: {:16p}, a_ref: {:16p}",
        &a, &a_ref, a_ref
    );

    a_box = Box::new(a + 2);
    a_ref = &*a_box;
    println!(
        "address => &a: {:16p},  a_ref: {:16p}, a_box: {:16p}",
        &a, a_ref, a_box
    );
}
```

```rust
fn main() {
    let a = 7;
    let mut a_box: Box<i32>;
    let a_ref: &i32 = &a;

    println!("{} {}", a, a_ref);
    a_box = Box::new(a + 2);
    println!(
        "value   =>  a: {:16}, a_ref: {:16}, a_box: {:16}",
        a, a_ref, a_box
    );
    println!(
        "address => &a: {:16p}, a_ref: {:16p}, a_box: {:16p}",
        &a, a_ref, a_box
    );

    a_box = Box::new(*a_ref + 4);
    println!(
        "value   =>  a: {:16}, a_ref: {:16}, a_box: {:16}",
        a, a_ref, a_box
    );
    println!(
        "address => &a: {:16p}, a_ref: {:16p}, a_box: {:16p}",
        &a, a_ref, a_box
    );
}
```

### data representation

```rust
use std::mem::size_of;
use std::slice::from_raw_parts;

fn as_bytes<T>(o: &T) -> &[u8] {
    unsafe { from_raw_parts(o as *const _ as *const u8, size_of::<T>()) }
}
fn main() {
    println!("{:?}", as_bytes(&1i8));
    println!("{:?}", as_bytes(&2i16)); // little endian => [2, 0], big endian => [0, 2]
    println!("{:?}", as_bytes(&3i32));
    println!("{:?}", as_bytes(&(4i64 + 5 * 256 + 6 * 256 * 256)));
    println!("{:?}", as_bytes(&'A'));
    println!("{:?}", as_bytes(&true));
    println!("{:?}", as_bytes(&&1i8));
}
```

```rust
fn main() {
    let b1 = true;
    let b2 = true;
    let b3 = false;
    println!("&b1 address: {}", &b1 as *const bool as usize);
    println!("&b2 address: {}", &b2 as *const bool as usize);
    println!("&b3 address: {}", &b3 as *const bool as usize);
}
```

### data size

```rust
use std::mem::size_of;
use std::mem::size_of_val;

fn main() {
    println!("bool: {} byte", size_of::<bool>());
    println!("char: {} byte", size_of::<char>());

    println!("u8  : {} byte", size_of::<u8>());
    println!("u16 : {} byte", size_of::<u16>());
    println!("u32 : {} byte", size_of::<u32>());
    println!("u64 : {} byte", size_of::<u64>());
    println!("u128: {} byte", size_of::<u128>());

    println!("i8  : {} byte", size_of::<i8>());
    println!("i16 : {} byte", size_of::<i16>());
    println!("i32 : {} byte", size_of::<i32>());
    println!("i64 : {} byte", size_of::<i64>());
    println!("i128: {} byte", size_of::<i128>());

    println!("f32 : {} byte", size_of::<f32>());
    println!("f64 : {} byte", size_of::<f64>());

    println!("&12 : {} byte", size_of_val(&12));
    let v = 4_i32;
    println!("let v = 4_i32;");
    println!("&v  :  {} byte", size_of_val(&v));
}
```

```rust
use std::mem::*;

enum E1 {
    E1a,
    E1b,
}
enum E2 {
    E2a,
    E2b(f64),
}

struct S1 {
    a: i8,
}

struct S2 {
    a: i8,
    b: i32,
}

fn main() {
    println!("&0i16                  : {} byte", size_of_val(&0i16));
    println!("&0i64                  : {} byte", size_of_val(&0i64));

    println!("&[0i16; 1]             : {} byte", size_of_val(&[0i16; 1]));
    println!("&[0i16; 10]            : {} byte", size_of_val(&[0i16; 10]));

    println!(
        "&(0i16, 0i64)          : {} byte",
        size_of_val(&(0i16, 0i64))
    );
    println!(
        "&[(0i16, 0i64); 10]    : {} byte",
        size_of_val(&[(0i16, 0i64); 10])
    );

    println!("&E1::E1a               : {} byte", size_of_val(&E1::E1a));
    println!("&E2::E2a               : {} byte", size_of_val(&E2::E2a));

    println!(
        "&S1                    : {} byte",
        size_of_val(&S1 { a: 1 })
    );
    println!(
        "&S2                    : {} byte",
        size_of_val(&S2 { a: 1, b: 2 })
    );

    println!(
        "&vec![(0i16, 0i64); 10]: {} byte",
        size_of_val(&vec![(0i16, 0i64); 10])
    );
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
