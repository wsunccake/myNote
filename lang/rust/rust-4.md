# rust - other

---

## content

- [collection](#collection)
  - [vector](#vector)
  - [hashmap](#hashmap)
  - [hashset](#hashset)
- [error handle](#error-handle)
  - [panic](#panic)
  - [enum result - match](#enum-result---match)
  - [unwrap](#unwrap)
  - [expect](#expect)
- [generic](#generic)
  - [generic - struct](#generic---struct)
  - [multi generic - struct](#multi-generic---struct)
  - [generic - struct - method](#generic---struct---method)
  - [generic - function](#generic---function)
- [trait](#trait)
  - [evaluate](#evaluate)
  - [method](#method)
  - [self](#self)
  - [standard trait](#standard-trait)
  - [type](#type)
  - [generic trait](#generic-trait)
  - [iterator trait](#iterator-trait)

---

## collection

### vector

```rust
let mut instance_name = Vec::new();
let instance_name = Vec::from([val1, val2]);
let vector_name = vec![val1, val2, val3];
```

```rust
fn main() {
    // let mut v = Vec::new();
    let mut v = Vec::from([1, 2, 3]);
    println!("{:#?}", v[0]);
    println!("{:#?}", v.get(0));
    v[0] = 0;

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

    let mut v1 = vec![9, 8];
    v.append(&mut v1);
    println("v len: {}, v1 len: {}", v.len(), v1.len());
}
```

```rs
fn main() {
    let vec1 = vec![1, 2, 3, 4];
    println!("vec1: {vec1:#?}");
    // consumer
    for v in vec1 {
        println!("{v:#?}");
    }
    println!("vec1: {vec1:#?}"); // error: borrow of moved

    let vec2 = vec![1, 2, 3, 4];
    println!("vec2: {vec2:#?}");
    // producer
    for v in vec2.iter() {
        println!("{v:#?}");
    }
    println!("vec2: {vec2:#?}");
    vec2.iter().for_each(|x| println!("{x:?}"));

    let mut vec3 = vec![1, 2, 3, 4];
    println!("vec3: {vec3:#?}");
    // producer
    for mut v in vec3.iter_mut() {
        *v += 1;
        println!("{v:#?}");
    }
    println!("vec3: {vec3:#?}");

    let vec4 = vec![1, 2, 3, 4];
    println!("vec4: {vec4:#?}");
    // consumer
    for mut v in vec4.into_iter() {
        v += 1;
        println!("{v:#?}");
    }
    // println!("vec4: {vec4:#?}"); // error: borrow of moved
}
```

producer: iter, iter_mut

consumer: into_iter

```rust
fn main() {
    let mut v = vec![0; 0];
    println!("len: {}, capacity: {}", v.len(), v.capacity());
    v.push(11);
    println!("len: {}, capacity: {}", v.len(), v.capacity());
    v.push(22);
    println!("len: {}, capacity: {}", v.len(), v.capacity());
    v.push(33);
    println!("len: {}, capacity: {}", v.len(), v.capacity());
    v.push(44);
    println!("len: {}, capacity: {}", v.len(), v.capacity());
    v.push(55);
    println!("len: {}, capacity: {}", v.len(), v.capacity());
}
```

```rust
fn main() {
    let mut v = vec![0; 0];
    let mut prev_capacity = std::usize::MAX;
    for i in 0..1_000 {
        let cap = v.capacity();
        if cap != prev_capacity {
            println!("{} {} {}", i, v.len(), cap);
            prev_capacity = cap;
        }
        v.push(1);
    }
}
```

### hashmap

```rust
let mut instance_name = HashMap::new();
let mut instance_name = HashMap::HashMap::from([(k1, v1), (k2, v2)]);
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

## input and output

### command-line argument

```rust
fn main() {
    let command_line: std::env::Args = std::env::args();
    for argument in command_line {
        println!("[{}]", argument);
    }
}
```

```bash
linux:~/proj $ cargo run abx XYZ
```

### process return code

```rust
fn main() {
    std::process::exit(107);
}
```

```bash
linux:~ $ ./main
linux:~ $ echo $?
```

### environment variable

```rust
fn main() {
    for var in std::env::vars() {
        println!("[{}]=[{}]", var.0, var.1);
    }

    println!(
        "{}",
        if std::env::var("HOME").is_ok() {
            "Already defined"
        } else {
            "Undefined"
        }
    );

    std::env::set_var("XYZ", "This is the value");
    println!(
        ", {}.",
        match std::env::var("XYZ") {
            Ok(value) => value,
            Err(err) => format!("Still undefined: {}", err),
        }
    );
}
```

### read from onsole

```rust
fn main() {
    let mut line = String::new();
    println!("{:?}", std::io::stdin().read_line(&mut line));
    println!("[{}]", line);
}
```

```rust
fn main() {
    let mut text = format!("First: ");
    let inp = std::io::stdin();
    inp.read_line(&mut text).unwrap();
    text.push_str("Second: ");
    inp.read_line(&mut text).unwrap();
    println!("{}: {} bytes", text, text.len());
}
```

### writing to console

```rust
use std::io::Write;

fn main() {
    //ILLEGAL: std::io::stdout().write("Hi").unwrap();
    //ILLEGAL: std::io::stdout().write(String::from("Hi")).unwrap();
    std::io::stdout().write("Hello ".as_bytes()).unwrap();
    std::io::stdout()
        .write(String::from("world").as_bytes())
        .unwrap();
}
```

### convert value to string

```rust
fn main() {
    let int_str: String = 45.to_string();
    let float_str: String = 4.5.to_string();
    let bool_str: String = true.to_string();
    println!("{} {} {}", int_str, float_str, bool_str);
}
```

### file input / output

```rust
use std::io::Read;
use std::io::Write;

fn main() {
    let mut file = std::fs::File::create("data.txt").unwrap();
    file.write_all("eè€".as_bytes()).unwrap();

    let mut file = std::fs::File::open("data.txt").unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    println!("{}", contents);
}
```

```rust
use std::io::Read;
use std::io::Write;

fn main() {
    let mut command_line: std::env::Args = std::env::args();
    command_line.next().unwrap();
    let source = command_line.next().unwrap();
    let destination = command_line.next().unwrap();
    let mut file_in = std::fs::File::open(source).unwrap();
    let mut file_out = std::fs::File::create(destination).unwrap();
    let mut buffer = [0u8; 4096];
    loop {
        let nbytes = file_in.read(&mut buffer).unwrap();
        file_out.write(&buffer[..nbytes]).unwrap();
        if nbytes < buffer.len() {
            break;
        }
    }
}
```

### text file

```rust
fn main() {
    let mut command_line = std::env::args();
    command_line.next();
    let pathname = command_line.next().unwrap();
    let counts = count_lines(&pathname).unwrap();
    println!("file: {}", pathname);
    println!("n. of lines: {}", counts.0);
    println!("n. of empty lines: {}", counts.1);
    fn count_lines(pathname: &str) -> Result<(u32, u32), std::io::Error> {
        use std::io::BufRead;
        let f = std::fs::File::open(pathname)?;
        let f = std::io::BufReader::new(f);
        let mut n_lines = 0;
        let mut n_empty_lines = 0;
        for line in f.lines() {
            n_lines += 1;
            if line?.trim().len() == 0 {
                n_empty_lines += 1;
            }
        }
        Ok((n_lines, n_empty_lines))
    }
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
fn my_panic() {
    println!("Error");
    panic!();
}

fn main() {
    my_panic();
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

### run time

```rust
fn f1(x: i32) -> Result<i32, String> {
    if x == 1 {
        Err(format!("Err. 1"))
    } else {
        Ok(x)
    }
}

fn f2(x: i32) -> Result<i32, String> {
    if x == 2 {
        Err(format!("Err. 2"))
    } else {
        Ok(x)
    }
}

fn f3(x: i32) -> Result<i32, String> {
    if x == 3 {
        Err(format!("Err. 3"))
    } else {
        Ok(x)
    }
}

fn f4(x: i32) -> Result<i32, String> {
    if x == 4 {
        Err(format!("Err. 4"))
    } else {
        Ok(x)
    }
}

fn f(x: i32) -> Result<i32, String> {
    match f1(x) {
        Ok(result) => match f2(result) {
            Ok(result) => match f3(result) {
                Ok(result) => f4(result),
                Err(err_msg) => Err(err_msg),
            },
            Err(err_msg) => Err(err_msg),
        },
        Err(err_msg) => Err(err_msg),
    }
}

// refactor f()
fn g(x: i32) -> Result<i32, String> {
    let result1 = f1(x);
    if result1.is_err() {
        return result1;
    }
    let result2 = f2(result1.unwrap());
    if result2.is_err() {
        return result2;
    }
    let result3 = f3(result2.unwrap());
    if result3.is_err() {
        return result3;
    }
    f4(result3.unwrap())
}

// refactor f()
fn h(x: i32) -> Result<i32, String> {
    f4(f3(f2(f1(x)?)?)?)
}
// e? (e is generic type Result<T, E>)
// => match e { Some(v) => v, _ => return e }

fn main() {
    match f(2) {
        Ok(y) => println!("{}", y),
        Err(e) => println!("Error: {}", e),
    }

    match f(4) {
        Ok(y) => println!("{}", y),
        Err(e) => println!("Error: {}", e),
    }

    match f(5) {
        Ok(y) => println!("{}", y),
        Err(e) => println!("Error: {}", e),
    }

    match g(2) {
        Ok(y) => println!("{}", y),
        Err(e) => println!("Error: {}", e),
    }

    match g(4) {
        Ok(y) => println!("{}", y),
        Err(e) => println!("Error: {}", e),
    }

    match g(5) {
        Ok(y) => println!("{}", y),
        Err(e) => println!("Error: {}", e),
    }

    match h(2) {
        Ok(y) => println!("{}", y),
        Err(e) => println!("Error: {}", e),
    }

    match h(4) {
        Ok(y) => println!("{}", y),
        Err(e) => println!("Error: {}", e),
    }

    match h(5) {
        Ok(y) => println!("{}", y),
        Err(e) => println!("Error: {}", e),
    }
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

### evaluate

```rust
fn quartic_root_f64(x: f64) -> f64 {
    x.sqrt().sqrt()
}
fn quartic_root_f32(x: f32) -> f32 {
    x.sqrt().sqrt()
}

fn main() {
    println!("quartic_root_f64: {}", quartic_root_f64(100f64),);
    println!("quartic_root_f32: {}", quartic_root_f32(100f32),);
}
```

=>

```rust
fn quartic_root<Number>(x: Number) -> Number {
    x.sqrt().sqrt() // method not found in `Number`
}

fn main() {
    // fail to run
    println!("quartic_root f64: {}", quartic_root(100f64),);
    println!("quartic_root f32: {}", quartic_root(100f32));
}
```

=>

```rust
trait HasSquareRoot {
    fn sq_root(self) -> Self;
}

impl HasSquareRoot for f32 {
    fn sq_root(self) -> Self {
        f32::sqrt(self)
    }
}
impl HasSquareRoot for f64 {
    fn sq_root(self) -> Self {
        f64::sqrt(self)
    }
}
fn quartic_root<Number>(x: Number) -> Number
where
    Number: HasSquareRoot,
{
    x.sq_root().sq_root()
}

fn main() {
    println!("quartic_root f64: {}", quartic_root(100f64),);
    println!("quartic_root f32: {}", quartic_root(100f32));
}
```

=>

```rust
fn sqrt() {}

trait HasSquareRoot {
    fn sqrt(self) -> Self;
}

impl HasSquareRoot for f32 {
    fn sqrt(self) -> Self {
        f32::sqrt(self)
    }
}

impl HasSquareRoot for f64 {
    fn sqrt(self) -> Self {
        f64::sqrt(self)
    }
}
fn quartic_root<Number>(x: Number) -> Number
where
    Number: HasSquareRoot,
{
    x.sqrt().sqrt()
}

fn main() {
    sqrt();
    println!("quartic_root f64: {}", quartic_root(100f64),);
    println!("quartic_root f32: {}", quartic_root(100f32));
}
```

=>

```rust
trait HasSqrtAndAbs {
    fn sqrt(self) -> Self;
    fn abs(self) -> Self;
}

impl HasSqrtAndAbs for f32 {
    fn sqrt(self) -> Self {
        f32::sqrt(self)
    }
    fn abs(self) -> Self {
        f32::abs(self)
    }
}

impl HasSqrtAndAbs for f64 {
    fn sqrt(self) -> Self {
        f64::sqrt(self)
    }
    fn abs(self) -> Self {
        f64::abs(self)
    }
}
fn abs_quartic_root<Number>(x: Number) -> Number
where
    Number: HasSqrtAndAbs,
{
    x.abs().sqrt().sqrt()
}

fn main() {
    println!("abs_quartic_root f64: {}", abs_quartic_root(100f64),);
    println!("abs_quartic_root f32: {}", abs_quartic_root(100f32));
}
```

=>

```rust
trait HasSquareRoot {
    fn sqrt(self) -> Self;
}

impl HasSquareRoot for f32 {
    fn sqrt(self) -> Self {
        f32::sqrt(self)
    }
}

impl HasSquareRoot for f64 {
    fn sqrt(self) -> Self {
        f64::sqrt(self)
    }
}

trait HasAbsoluteValue {
    fn abs(self) -> Self;
}

impl HasAbsoluteValue for f32 {
    fn abs(self) -> Self {
        f32::abs(self)
    }
}

impl HasAbsoluteValue for f64 {
    fn abs(self) -> Self {
        f64::abs(self)
    }
}

fn abs_quartic_root<Number>(x: Number) -> Number
where
    Number: HasSquareRoot + HasAbsoluteValue,
{
    x.abs().sqrt().sqrt()
}

fn main() {
    println!("abs_quartic_root f64: {}", abs_quartic_root(100f64),);
    println!("abs_quartic_root f32: {}", abs_quartic_root(100f32));
}
```

### method

```rust
fn main() {
    println!("*** run with method ***");
    println!("{},", "abcd".to_string());
    println!("{},", [1, 2, 3].len());
    let mut v1 = vec![0u8; 0];
    v1.push(7u8);
    println!("{:?}; ", v1);

    println!("*** run with function ***");
    println!("{},", std::string::ToString::to_string("abcd"));
    println!("{:?},", <[i32]>::len(&[1, 2, 3]));
    let mut v2 = vec![0u8; 0];
    Vec::push(&mut v2, 7u8);
    println!("{:?}", v2);
}
```

```rust
fn double(x: i32) -> i32 {
    x * 2
}

trait CanBeDoubled {
    fn double(self) -> Self;
}

impl CanBeDoubled for i32 {
    fn double(self) -> Self {
        self * 2
    }
}

fn main() {
    println!("doube(7i32): {}", double(7i32));

    println!("7i32.doube(): {}", 7i32.double());
}
```

### self

```rust
// same
fn double(self) -> Self { }
fn double(self: Self) -> Self { }
fn double(self: i32) -> Self { }
fn double(self) -> i32 { }
fn double(self: Self) -> i32 { }
fn double(self: i32) -> i32 { }
```

```rust
trait LettersCount {
    fn letters_count(&self, ch: char) -> usize;
}
impl LettersCount for str {
    fn letters_count(&self, ch: char) -> usize {
        let mut count = 0;
        for c in self.chars() {
            if c == ch {
                count += 1;
            }
        }
        count

        // self.chars().filter(|c| *c == ch).count()
    }
}

fn main() {
    println!("{} ", "".letters_count('a'));
    println!("{} ", "ddd".letters_count('a'));
    println!("{} ", "ddd".letters_count('d'));
    println!("{} ", "foobarbaz".letters_count('a'));
}
```

### standard trait

```rust
struct Complex {
    re: f64,
    im: f64,
}
impl std::fmt::Display for Complex {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(
            f,
            "{} {} {}i",
            self.re,
            if self.im >= 0. { '+' } else { '-' },
            self.im.abs()
        )
    }
}

fn main() {
    let c1 = Complex { re: -2.3, im: 0. };
    let c2 = Complex { re: -2.1, im: -5.2 };
    let c3 = Complex { re: -2.2, im: 5.2 };
    println!("{}", c1);
    println!("{}", c2);
    println!("{}", c3);
}
```

### type

```rust
fn f1(x: f32) -> f32 {
    x
}
fn f2(x: f32) -> f32 {
    x
}
fn main() {
    let a: f32 = 2.3;
    let b: f32 = 3.4;
    println!("{} {}", f1(a), f2(b));
}
```

=>

```rust
type Number = f32;
fn f1(x: Number) -> Number {
    x
}
fn f2(x: Number) -> Number {
    x
}

fn main() {
    let a: f32 = 2.3;
    let b: f32 = 3.4;
    println!("{} {}", f1(a), f2(b));
}
```

```rust
fn main() {
    type Number = f32;
    let a: Number = 2.3;
    let _b: f32 = a;
}
```

### generic trait

```rust
trait Searchable<Key> {
    fn contains(&self, key: Key) -> bool;
}
struct RecordWithId {
    id: u32,
    _descr: String,
}
struct NameSetWithId {
    data: Vec<RecordWithId>,
}

impl Searchable<u32> for NameSetWithId {
    fn contains(&self, key: u32) -> bool {
        for record in self.data.iter() {
            if record.id == key {
                return true;
            }
        }
        false
    }
}

fn is_present<Collection>(coll: &Collection, id: u32) -> bool
where
    Collection: Searchable<u32>,
{
    coll.contains(id)
}

fn main() {
    let names = NameSetWithId {
        data: vec![
            RecordWithId {
                id: 34,
                _descr: "John".to_string(),
            },
            RecordWithId {
                id: 49,
                _descr: "Jane".to_string(),
            },
        ],
    };
    println!("{}", is_present(&names, 48),);
    println!("{}", is_present(&names, 49),);
}
```

=>

```rust
trait Searchable<Key, Count> {
    fn contains(&self, key: Key) -> bool;
    fn count(&self, key: Key) -> Count;
}
struct RecordWithId {
    id: u32,
    _descr: String,
}
struct NameSetWithId {
    data: Vec<RecordWithId>,
}

impl Searchable<u32, usize> for NameSetWithId {
    fn contains(&self, key: u32) -> bool {
        for record in self.data.iter() {
            if record.id == key {
                return true;
            }
        }
        false
    }
    fn count(&self, key: u32) -> usize {
        let mut c = 0;
        for record in self.data.iter() {
            if record.id == key {
                c += 1;
            }
        }
        c
    }
}

fn is_present<Collection>(coll: &Collection, id: u32) -> bool
where
    Collection: Searchable<u32, usize>,
{
    coll.contains(id)
}

fn main() {
    let names = NameSetWithId {
        data: vec![
            RecordWithId {
                id: 34,
                _descr: "John".to_string(),
            },
            RecordWithId {
                id: 49,
                _descr: "Jane".to_string(),
            },
        ],
    };
    println!("{}, {}", names.count(48), is_present(&names, 48),);
    println!("{}, {}", names.count(49), is_present(&names, 49),);
}
```

=>

```rust
trait Searchable {
    type Key;
    type Count;
    fn contains(&self, key: Self::Key) -> bool;
    fn count(&self, key: Self::Key) -> Self::Count;
}
struct RecordWithId {
    id: u32,
    _descr: String,
}
struct NameSetWithId {
    data: Vec<RecordWithId>,
}

impl Searchable for NameSetWithId {
    type Key = u32;
    type Count = usize;

    fn contains(&self, key: Self::Key) -> bool {
        for record in self.data.iter() {
            if record.id == key {
                return true;
            }
        }
        false
    }

    fn count(&self, key: Self::Key) -> usize {
        let mut c = 0;
        for record in self.data.iter() {
            if record.id == key {
                c += 1;
            }
        }
        c
    }
}

fn is_present<Collection>(coll: &Collection, id: <Collection as Searchable>::Key) -> bool
where
    Collection: Searchable,
{
    coll.contains(id)
}

fn main() {
    let names = NameSetWithId {
        data: vec![
            RecordWithId {
                id: 34,
                _descr: "John".to_string(),
            },
            RecordWithId {
                id: 49,
                _descr: "Jane".to_string(),
            },
        ],
    };

    println!("{}, {}", names.count(48), is_present(&names, 48),);
    println!("{}, {}", names.count(49), is_present(&names, 49),);
}
```

### iterator trait

```rust
fn get_third_for_range() {
    println!("*** for rnage ***");
    fn get_third(r: std::ops::Range<u32>) -> Option<u32> {
        if r.len() >= 3 {
            Some(r.start + 2)
        } else {
            None
        }
    }
    println!("{:?} {:?}", get_third(10..12), get_third(20..23));
}

fn get_third_for_slice() {
    println!("*** for slice ***");

    fn get_third(s: &[f64]) -> Option<f64> {
        if s.len() >= 3 {
            Some(s[2])
        } else {
            None
        }
    }

    println!(
        "{:?} {:?}",
        get_third(&[1.0, 2.0]),
        get_third(&[1.1, 2.1, 3.1])
    );
}

fn get_third_for_iterator() {
    println!("*** for iterator ***");

    fn get_third<Iter, Item>(mut iterator: Iter) -> Option<Item>
    where
        Iter: std::iter::Iterator + Iterator<Item = Item>,
    {
        iterator.next();
        iterator.next();
        iterator.next()
    }

    println!("{:?} {:?}", get_third(10..12), get_third(20..23));
    println!(
        "{:?} {:?}",
        get_third([1.0, 2.0].iter()),
        get_third([1.1, 2.1, 3.1].iter())
    );
}

fn main() {
    get_third_for_range();
    get_third_for_slice();
    get_third_for_iterator();
}
```

```rust
// trait Iterator {
//     type Item;
//     fn next(&mut self) -> Option<Self::Item>;
// }

struct MyRangeIterator<T> {
    current: T,
    limit: T,
}

impl Iterator for MyRangeIterator<u32> {
    type Item = u32;
    fn next(&mut self) -> Option<Self::Item> {
        if self.current == self.limit {
            None
        } else {
            self.current += 1;
            Some(self.current - 1)
        }
    }
}

fn run_next() {
    println!("*** iterator next ***");
    let mut range_it = MyRangeIterator {
        current: 10,
        limit: 13,
    };
    println!("{:?}, ", range_it.next());
    println!("{:?}, ", range_it.next());
    println!("{:?}, ", range_it.next());
    println!("{:?}, ", range_it.next());
    println!("{:?}, ", range_it.next());
}

fn run_range() {
    println!("*** iterator range ***");
    let range_it = MyRangeIterator {
        current: 10,
        limit: 13,
    };
    for i in range_it {
        println!("{} ", i);
    }
}

fn main() {
    run_next();
    run_range();
}
```
