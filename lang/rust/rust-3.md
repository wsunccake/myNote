# rust - advanced

---

## content

- [collection](#collection)
  - [vector](#vector)
  - [hashmap](#hashmap)
  - [hashset](#hashset)
- [error handle](#error-handle)

---

## collection

### vector

```rust
let mut instance_name = Vec::new();
let vector_name = vec![val1, val2, val3];
```

```rust
fn main() {
    let mut v = Vec::new();
    v.push(20);
    v.push(30);
    v.push(40);

    println!("size of vector is :{}", v.len());
    println!("{:?}", v);
    println!("{:?}", v[0]);

    v.remove(1);
    println!("{:?}", v);

    if v.contains(&10) {
        println!("found 10");
    }

    for i in &v {
        println!("{}", i);
    }
}
```

### hashmap

```rust
let mut instance_name = HashMap::new();
```

```rust
use std::collections::HashMap;

fn main() {
    let mut stateCodes = HashMap::new();
    stateCodes.insert("KL", "Kerala");
    stateCodes.insert("MH", "Maharashtra");

    println!("{:?}", stateCodes);
    println!("size of map is {}", stateCodes.len());

    if stateCodes.contains_key(&"GJ") {
        println!("found key");
    }

    for (key, val) in stateCodes.iter() {
        println!("key: {} val: {}", key, val);
    }

    match stateCodes.get(&"KL") {
        Some(value) => {
            println!("Value for key KL is {}", value);
        }
        None => {
            println!("nothing found");
        }
    }

    println!("length of the hashmap {}", stateCodes.len());
    stateCodes.remove(&"GJ");
    println!("length of the hashmap after remove() {}", stateCodes.len());
}
```

### hashset

```rust
let mut hash_set_name = HashSet::new();
```

```rust
use std::collections::HashSet;

fn main() {
    let mut names = HashSet::new();

    names.insert("Mohtashim");
    names.insert("Kannan");
    names.insert("TutorialsPoint");
    names.insert("Mohtashim"); //duplicates not added

    println!("{:?}", names);

    println!("size of the set is {}", names.len());

    for name in names.iter() {
        println!("{}", name);
    }

    match names.get(&"Mohtashim") {
        Some(value) => {
            println!("found {}", value);
        }
        None => {
            println!("not found");
        }
    }
    println!("{:?}", names);

    if names.contains(&"Kannan") {
        println!("found name");
    }

    println!("length of the Hashset: {}", names.len());
    names.remove(&"Kannan");
    println!("length of the Hashset after remove() : {}", names.len());
}
```

---

## error handle

### panic

```rust
fn main() {
    panic!("hello");
    println!("end of main"); //unreachable statement
}
```

```rust
fn main() {
    let a = [10, 20, 30];
    a[10]; //invokes a panic since index 10 cannot be reached
}
```

```rust
fn main() {
    let no = 13;

    if no % 2 == 0 {
        println!("number is even");
    } else {
        panic!("NOT_AN_EVEN");
    }
    println!("end of main");
}
```

### enum result - match

```rust
use std::fs::File;
fn main() {
    let f = File::open("main.jpg"); // main.jpg doesn't exist
    match f {
        Ok(f) => {
            println!("file found {:?}", f);
        }
        Err(e) => {
            println!("file not found \n{:?}", e); //handled error
        }
    }
    println!("end of main");
}
```

```rust
fn is_even(no: i32) -> Result<bool, String> {
    if no % 2 == 0 {
        return Ok(true);
    } else {
        return Err("NOT_AN_EVEN".to_string());
    }
}

fn main() {
    for val in [1, 2].iter() {
        let result = is_even(*val);
        match result {
            Ok(d) => {
                println!("no is even {}", d);
            }
            Err(msg) => {
                println!("Error msg is {}", msg);
            }
        }
    }

    println!("end of main");
}
```

### unwrap

```rust
fn is_even(no: i32) -> Result<bool, String> {
    if no % 2 == 0 {
        return Ok(true);
    } else {
        return Err("NOT_AN_EVEN".to_string());
    }
}

fn main() {
    for val in [2, 3].iter() {
        let result = is_even(*val).unwrap();
        println!("result is {}", result);
    }

    println!("end of main");
}
```

### expect

```rust
fn is_even(no: i32) -> Result<bool, String> {
    if no % 2 == 0 {
        return Ok(true);
    } else {
        return Err("NOT_AN_EVEN".to_string());
    }
}

fn main() {
    for val in [2, 3].iter() {
        let result = is_even(*val).expect("not even");
        println!("result is {}", result);
    }

    println!("end of main");
}
```

---

## generic

### generic - struct

```rust
struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    let _p1: Point<i32> = Point::<i32> { x: 5, y: 10 };
    let _p2 = Point { x: 1.0, y: 4.0 };
    let _p3 = Point { x: 5, y: 4.0 };
}
```

### multi generic - struct

```rust
struct Point<T, U> {
    x: T,
    y: U,
}

fn main() {
    let _p1 = Point { x: 5, y: 10 };
    let _p2 = Point { x: 1.0, y: 4.0 };
    let _p3 = Point { x: 5, y: 4.0 };
}
```

### generic - struct - method

```rust
struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

fn main() {
    let p = Point { x: 5, y: 10 };

    println!("p.x = {}", p.x());
}
```

### generic - function

```rust
fn my_print<T: std::fmt::Display>(list: &[T]) {
    for item in list {
        println!("{} ", item);
    }
}

fn main() {
    let number_list = vec![34, 50, 25, 100, 65];
    my_print(&number_list);

    let char_list = vec!['y', 'm', 'a', 'q'];
    my_print(&char_list);
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
