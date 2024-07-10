# rust - other

---

## content

- [collection](#collection)
  - [vector](#vector)
  - [hashmap](#hashmap)
  - [hashset](#hashset)
- [standard library collection](#standard-library-collection)
  - [measure execution time](#measure-execution-time)
  - [queue performance](#queue-performance)
  - [heap performance](#heap-performance)
  - [set performance](#set-performance)
  - [map performance](#map-performance)
  - [summary](#summary)
- [input and output](#input-and-output)
  - [command-line argument](#command-line-argument)
  - [process return code](#process-return-code)
  - [environment variable](#environment-variable)
  - [read from console](#read-from-console)
  - [writing to console](#writing-to-console)
  - [convert value to string](#convert-value-to-string)
  - [file input / output](#file-input--output)
  - [text file](#text-file)
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
- [object-oriented programming](#object-oriented-programming)
  - [inherit implement](#inherit-implement)
  - [enum implement](#enum-implement)
  - [mutable method](#mutable-method)
  - [constructor](#constructor)
  - [composition instead of inheritance](#composition-instead-of-inheritance)
  - [memory usage](#memory-usage)
  - [static dispatch](#static-dispatch)
  - [dynamic dispatch](#dynamic-dispatch)
  - [reference to trait](#reference-to-trait)
- [value / data](#value--data)
  - [destructor](#destructor)
  - [assignment](#assignment)
  - [move vs copy performance](#move-vs-copy-performance)
  - [ownership](#ownership)
  - [make cloneable or copyable](#make-cloneable-or-copyable)
- [reference](#reference)
  - [borrow](#borrow)
  - [borrow error - after move error](#borrow-error---after-move-error)
  - [borrow error - after drop error](#borrow-error---after-drop-error)
  - [drop order](#drop-order)
  - [multiple borrowing case](#multiple-borrowing-case)
- [lifetmie](#lifetmie)
  - [return reference](#return-reference)
  - [lifetime specfifier](#lifetime-specfifier)
  - [validate lifetime specifier](#validate-lifetime-specifier)
  - [invoked function with lifetime specifier](#invoked-function-with-lifetime-specifier)
  - [lifetime elision](#lifetime-elision)
  - [lifetime elision with object-oriented programming](#lifetime-elision-with-object-oriented-programming)
  - [lifetime specifier for struct](#lifetime-specifier-for-struct)

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

## standard library collection

### measure execution time

```rust
use std::time::Instant;

fn elapsed_ms(t1: Instant, t2: Instant) -> f64 {
    let t = t2 - t1;
    t.as_secs() as f64 * 1000. + t.subsec_nanos() as f64 / 1e6
}

fn main() {
    let time0 = Instant::now();
    for _i in 0..10_000 {
        // println!("{}", i);
    }
    let time1 = Instant::now();

    println!("{}", elapsed_ms(time0, time1));
}
```

```bash
linux:~/package $ rustc src/main.rs -o m

linux:~/package $ rustc -O src/main.rs -o mO
```

```toml
[profile.dev]
opt-level = 2  # opt-level = 2 => -O
```

### vector performance

```rust
use std::time::Instant;

const SIZE: usize = 100_000;

fn elapsed_ms(t1: Instant, t2: Instant) -> f64 {
    let t = t2 - t1;
    t.as_secs() as f64 * 1000. + t.subsec_nanos() as f64 / 1e6
}

fn vec_push_pop() {
    println!("*** vector push & pop ***");
    let t0 = Instant::now();
    let mut v = Vec::<usize>::with_capacity(SIZE);
    let t1 = Instant::now();
    for i in 0..SIZE {
        v.push(i);
    }
    let t2 = Instant::now();
    for _ in 0..SIZE {
        v.pop();
    }
    let t3 = Instant::now();
    println!("init: {}", elapsed_ms(t0, t1));
    println!("push: {}", elapsed_ms(t1, t2));
    println!("pop: {}", elapsed_ms(t2, t3));
}

fn vec_insert_remove() {
    println!("*** vector insert & remove ***");
    let t0 = Instant::now();
    let mut v = Vec::<usize>::with_capacity(SIZE);
    let t1 = Instant::now();
    for i in 0..SIZE {
        v.insert(0, i);
    }
    let t2 = Instant::now();
    for _ in 0..SIZE {
        v.remove(0);
    }
    let t3 = Instant::now();
    println!("init: {}", elapsed_ms(t0, t1));
    println!("insert: {}", elapsed_ms(t1, t2));
    println!("remove: {}", elapsed_ms(t2, t3));
}

fn main() {
    vec_push_pop();
    vec_insert_remove();
}
```

### queue performance

```rust
use std::time::Instant;

const SIZE: usize = 40_000;

fn elapsed_ms(t1: Instant, t2: Instant) -> f64 {
    let t = t2 - t1;
    t.as_secs() as f64 * 1000. + t.subsec_nanos() as f64 / 1e6
}

fn vec_head_remove_tail_push() {
    println!("*** vector head remove & tail push ***");
    let t0 = Instant::now();
    let mut v = Vec::<usize>::new();
    for i in 0..SIZE {
        v.push(i);
        v.push(SIZE + i);
        v.remove(0);
        v.push(SIZE * 2 + i);
        v.remove(0);
    }
    let t1 = Instant::now();
    while v.len() > 0 {
        v.remove(0);
    }
    let t2 = Instant::now();
    println!("push: {}", elapsed_ms(t0, t1));
    println!("remove: {}", elapsed_ms(t1, t2));
}

fn vec_head_insert_tail_pop() {
    println!("*** vector head insert & tail pop ***");
    let t0 = Instant::now();
    let mut v = Vec::<usize>::with_capacity(SIZE);
    for i in 0..SIZE {
        v.insert(0, i);
        v.insert(0, SIZE + i);
        v.pop();
        v.insert(0, SIZE * 2 + i);
        v.pop();
    }
    let t1 = Instant::now();
    while v.len() > 0 {
        v.pop();
    }
    let t2 = Instant::now();
    println!("insert: {}", elapsed_ms(t0, t1));
    println!("pop: {}", elapsed_ms(t1, t2));
}

fn vec_deque_push_back_pop_front() {
    println!("*** vec queue insert & remove ***");
    let t0 = Instant::now();
    let mut vd = std::collections::VecDeque::<usize>::new();
    for i in 0..SIZE {
        vd.push_back(i);
        vd.push_back(SIZE + i);
        vd.pop_front();
        vd.push_back(SIZE * 2 + i);
        vd.pop_front();
    }
    let t1 = Instant::now();
    while vd.len() > 0 {
        vd.pop_front();
    }
    let t2 = Instant::now();

    println!("push_back: {}", elapsed_ms(t0, t1));
    println!("pop_front: {}", elapsed_ms(t1, t2));
}

fn main() {
    vec_head_remove_tail_push();
    vec_head_insert_tail_pop();
    vec_deque_push_back_pop_front();
}
```

### heap performance

```rust
use std::time::Instant;

const A: [i32; 14] = [48, 18, 20, 35, 17, 13, 39, 12, 42, 33, 29, 27, 50, 16];

fn elapsed_ms(t1: Instant, t2: Instant) -> f64 {
    let t = t2 - t1;
    t.as_secs() as f64 * 1000. + t.subsec_nanos() as f64 / 1e6
}

fn vec_add() {
    fn add(v: &mut Vec<i32>, a: i32) {
        v.push(a);
        v.sort();
    }

    println!("*** vec add ***");
    let a = A;
    let mut v = Vec::<i32>::new();
    let t0 = Instant::now();
    for i in 0..a.len() / 2 {
        add(&mut v, a[i * 2]);
        add(&mut v, a[i * 2 + 1]);
        print!("{} ", v.pop().unwrap());
    }
    println!("=>");
    let t1 = Instant::now();
    while !v.is_empty() {
        print!("{} ", v.pop().unwrap());
    }
    let t2 = Instant::now();
    println!("");
    println!("add: {}", elapsed_ms(t0, t1));
    println!("pop: {}", elapsed_ms(t1, t2));
}

fn vec_extract() {
    fn extract(v: &mut Vec<i32>) -> Option<i32> {
        v.sort();
        v.pop()
    }
    println!("*** vec extract ***");
    let a = A;
    let mut v = Vec::<i32>::new();
    let t0 = Instant::now();
    for i in 0..a.len() / 2 {
        v.push(a[i * 2]);
        v.push(a[i * 2 + 1]);
        print!("{} ", extract(&mut v).unwrap());
    }
    let t1 = Instant::now();
    while !v.is_empty() {
        print!("{} ", extract(&mut v).unwrap());
    }
    let t2 = Instant::now();
    println!("");
    println!("push: {}", elapsed_ms(t0, t1));
    println!("extract: {}", elapsed_ms(t1, t2));
}

fn heap_push_pop() {
    println!("*** heap ***");
    let a = A;
    let t0 = Instant::now();
    let mut v = std::collections::BinaryHeap::<i32>::new();
    for i in 0..a.len() / 2 {
        v.push(a[i * 2]);
        v.push(a[i * 2 + 1]);
        print!("{} ", v.pop().unwrap());
    }
    let t1 = Instant::now();
    while !v.is_empty() {
        print!("{} ", v.pop().unwrap());
    }
    let t2 = Instant::now();
    println!("");
    println!("push: {}", elapsed_ms(t0, t1));
    println!("pop: {}", elapsed_ms(t1, t2));
}

fn main() {
    vec_add();
    vec_extract();
    heap_push_pop();
}
```

### set performance

```rust
use std::time::Instant;

const ARR: [i32; 10] = [6, 8, 2, 8, 4, 9, 6, 1, 8, 0];

fn elapsed_ms(t1: Instant, t2: Instant) -> f64 {
    let t = t2 - t1;
    t.as_secs() as f64 * 1000. + t.subsec_nanos() as f64 / 1e6
}

fn vec_run() {
    println!("*** vec ***");
    let t0 = Instant::now();
    let mut v = Vec::<_>::new();
    let t1 = Instant::now();
    for i in ARR.iter() {
        v.push(i);
    }
    let t2 = Instant::now();
    for i in v.iter() {
        print!(" {}", i);
    }
    let t3 = Instant::now();

    println!("");
    println!("init: {}", elapsed_ms(t0, t1));
    println!("push: {}", elapsed_ms(t1, t2));
    println!("iter: {}", elapsed_ms(t2, t3));
}

fn hash_set_run() {
    println!("*** hash set ***");
    let t0 = Instant::now();
    let mut hs = std::collections::HashSet::<_>::new();
    let t1 = Instant::now();
    for i in ARR.iter() {
        hs.insert(i);
    }
    let t2 = Instant::now();
    for i in hs.iter() {
        print!(" {}", i);
    }
    let t3 = Instant::now();

    println!("");
    println!("init: {}", elapsed_ms(t0, t1));
    println!("push: {}", elapsed_ms(t1, t2));
    println!("iter: {}", elapsed_ms(t2, t3));
}

fn btree_set_run() {
    println!("*** btree set ***");
    let t0 = Instant::now();
    let mut bs = std::collections::BTreeSet::<_>::new();
    let t1 = Instant::now();
    for i in ARR.iter() {
        bs.insert(i);
    }
    let t2 = Instant::now();
    for i in bs.iter() {
        print!(" {}", i);
    }
    let t3 = Instant::now();

    println!("");
    println!("init: {}", elapsed_ms(t0, t1));
    println!("push: {}", elapsed_ms(t1, t2));
    println!("iter: {}", elapsed_ms(t2, t3));
}

fn main() {
    vec_run();
    hash_set_run();
    btree_set_run();
}
```

### map performance

```rust
use std::time::Instant;

const ARR: [(i32, char); 5] = [(640, 'T'), (917, 'C'), (412, 'S'), (670, 'T'), (917, 'L')];

fn elapsed_ms(t1: Instant, t2: Instant) -> f64 {
    let t = t2 - t1;
    t.as_secs() as f64 * 1000. + t.subsec_nanos() as f64 / 1e6
}

fn vec_run() {
    println!("*** vec ***");
    let t0 = Instant::now();
    let mut v = Vec::<_>::new();
    let t1 = Instant::now();
    for &(key, value) in ARR.iter() {
        v.push((key, value));
    }
    let t2 = Instant::now();
    for &(key, value) in v.iter() {
        print!("{}: {}", key, value);
    }
    let t3 = Instant::now();

    println!("");
    println!("init: {}", elapsed_ms(t0, t1));
    println!("push: {}", elapsed_ms(t1, t2));
    println!("iter: {}", elapsed_ms(t2, t3));
}

fn hash_map_run() {
    println!("*** hash map ***");
    let t0 = Instant::now();
    let mut hs = std::collections::HashMap::<_, _>::new();
    let t1 = Instant::now();
    for &(key, value) in ARR.iter() {
        hs.insert(key, value);
    }
    let t2 = Instant::now();
    for (key, value) in hs.iter() {
        print!("{}: {}", key, value);
    }
    let t3 = Instant::now();

    println!("");
    println!("init: {}", elapsed_ms(t0, t1));
    println!("push: {}", elapsed_ms(t1, t2));
    println!("iter: {}", elapsed_ms(t2, t3));
}

fn btree_map_run() {
    println!("*** btree set ***");
    let t0 = Instant::now();
    let mut bs = std::collections::BTreeMap::<_, _>::new();
    let t1 = Instant::now();
    for &(key, value) in ARR.iter() {
        bs.insert(key, value);
    }
    let t2 = Instant::now();
    for (key, value) in bs.iter() {
        print!("{}: {}", key, value);
    }
    let t3 = Instant::now();

    println!("");
    println!("init: {}", elapsed_ms(t0, t1));
    println!("push: {}", elapsed_ms(t1, t2));
    println!("iter: {}", elapsed_ms(t2, t3));
}

fn main() {
    vec_run();
    hash_map_run();
    btree_map_run();
}
```

### summary

```txt
Vector
like stack (FILO)
fast: push, pop
slow: insert, remove
適用於 尾進尾出

VecDeque
vector like double-ended queue (FIFO)
fast: push_back, pop_front
適用於 尾進頭出

LinkedList
linked list
適用於 任意位置 插入刪除

BinaryHeap
binary heap

HashSet
hash set => unordered set

BTreeSet
binary tree set => ordered set

HashMap
hash map => unordered map

BTreeMap
binary tree map => ordered map
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

### read from console

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

---

## object-oriented programming

### inherit implement

```rust
trait Tr {
    fn f1(a: u32) -> bool;
    fn f2(&self, b: u16) -> Self;
}
struct Stru {
    x: u16,
    y: u16,
}
impl Tr for Stru {
    fn f1(a: u32) -> bool {
        a == 0
    }
    fn f2(&self, b: u16) -> Self {
        if b == self.x || b == self.y {
            Stru {
                x: self.x + 1,
                y: self.y + 1,
            }
        } else {
            Stru {
                x: self.x - 1,
                y: self.y - 1,
            }
        }
    }
}

fn main() {
    let s = Stru { x: 23, y: 456 };
    println!("{} {}", Stru::f1(500_000), s.f2(456).x);
}
```

=>

```rust
struct Stru {
    x: u16,
    y: u16,
}

impl Stru {
    fn f1(a: u32) -> bool {
        a == 0
    }
    fn f2(&self, b: u16) -> Self {
        if b == self.x || b == self.y {
            Stru {
                x: self.x + 1,
                y: self.y + 1,
            }
        } else {
            Stru {
                x: self.x - 1,
                y: self.y - 1,
            }
        }
    }
}

fn main() {
    let s = Stru { x: 23, y: 456 };
    println!("{} {}", Stru::f1(500_000), s.f2(456).x);
}
```

### enum implement

```rust
enum Continent {
    Africa,
    America,
    Asia,
    Europe,
    Oceania,
}

impl Continent {
    fn name(&self) -> &str {
        match *self {
            Continent::Africa => "Africa",
            Continent::America => "America",
            Continent::Asia => "Asia",
            Continent::Europe => "Europe",
            Continent::Oceania => "Oceania",
        }
    }
}

fn main() {
    println!("{}", Continent::Asia.name());
}
```

### mutable method

getter, setter

```rust
struct S {
    x: u32,
}
impl S {
    fn get_x(&self) -> u32 {
        self.x
    }
    fn set_x(&mut self, x: u32) {
        self.x = x;
    }
}

fn main() {
    let mut s = S { x: 12 };
    println!("{} ", s.get_x());
    s.set_x(17);
    println!("{} ", s.get_x());
}
```

### constructor

```rust
struct Number {
    x: f64,
}
impl Number {
    fn new() -> Number {
        Number { x: 0. }
    }
    fn from(x: f64) -> Number {
        Number { x: x }
    }
    fn value(&self) -> f64 {
        self.x
    }
}

fn main() {
    let a = Number::new();
    let b = Number::from(2.3);
    println!("{} {}", a.value(), b.value());
}
```

### composition instead of inheritance

```rust
struct Text {
    characters: String,
}
impl Text {
    fn from(text: &str) -> Text {
        Text {
            characters: text.to_string(),
        }
    }
    fn draw(&self) {
        print!("{}", self.characters);
    }
}

struct BoxedText {
    text: Text,
    first: char,
    last: char,
}

impl BoxedText {
    fn with_text_and_borders(text: &str, first: char, last: char) -> BoxedText {
        BoxedText {
            text: Text::from(text),
            first: first,
            last: last,
        }
    }
    fn draw(&self) {
        print!("{}", self.first);
        self.text.draw();
        print!("{}", self.last);
    }
}

fn main() {
    let greeting = Text::from("Hello");
    greeting.draw();
    println!("");

    let boxed_greeting = BoxedText::with_text_and_borders("Hi", '[', ']');
    boxed_greeting.draw();
    println!("");
}
```

### memory usage

```rust
use std::mem::size_of;

struct Base1 {
    _x: f64,
}
struct Base2 {}
struct Derived1 {
    _b1: Base1,
    _b2: Base2,
}
struct Derived2 {
    _d1: Derived1,
    _other: f64,
}

fn main() {
    println!("Base1: {}", size_of::<Base1>(),);
    println!("Base2: {}", size_of::<Base2>(),);
    println!("Derived1: {}", size_of::<Derived1>(),);
    println!("Derived2: {}", size_of::<Derived2>(),);
}
```

### static dispatch

```rust
trait Draw {
    fn draw(&self);
}
struct Text {
    characters: String,
}
impl Text {
    fn from(text: &str) -> Text {
        Text {
            characters: text.to_string(),
        }
    }
}
impl Draw for Text {
    fn draw(&self) {
        print!("{}", self.characters);
    }
}
struct BoxedText {
    text: Text,
    first: char,
    last: char,
}

impl BoxedText {
    fn with_text_and_borders(text: &str, first: char, last: char) -> BoxedText {
        BoxedText {
            text: Text::from(text),
            first: first,
            last: last,
        }
    }
}
impl Draw for BoxedText {
    fn draw(&self) {
        print!("{}", self.first);
        self.text.draw();
        print!("{}", self.last);
    }
}

// SOLUTION 1 - pass-by-value
fn draw_text<T>(txt: T)
where
    T: Draw,
{
    txt.draw();
}

// SOLUTION 1 - pass-by-reference
// fn draw_text<T>(txt: &T)
// where
//     T: Draw,
// {
//     txt.draw();
// }

fn main() {
    let greeting = Text::from("Hello");
    let boxed_greeting = BoxedText::with_text_and_borders("Hi", '[', ']');

    draw_text(greeting);
    println!("");

    draw_text(boxed_greeting);
    println!("");
}
```

### dynamic dispatch

```rust
trait Draw {
    fn draw(&self);
}
struct Text {
    characters: String,
}
impl Text {
    fn from(text: &str) -> Text {
        Text {
            characters: text.to_string(),
        }
    }
}
impl Draw for Text {
    fn draw(&self) {
        print!("{}", self.characters);
    }
}
struct BoxedText {
    text: Text,
    first: char,
    last: char,
}

impl BoxedText {
    fn with_text_and_borders(text: &str, first: char, last: char) -> BoxedText {
        BoxedText {
            text: Text::from(text),
            first: first,
            last: last,
        }
    }
}
impl Draw for BoxedText {
    fn draw(&self) {
        print!("{}", self.first);
        self.text.draw();
        print!("{}", self.last);
    }
}

// SOLUTION 2 - pass-by-value
// fn draw_text(txt: dyn Draw) {
//     txt.draw();
// }

// SOLUTION 2 - pass-by-reference
fn draw_text(txt: &dyn Draw) {
    txt.draw();
}

fn main() {
    let greeting = Text::from("Hello");
    let boxed_greeting = BoxedText::with_text_and_borders("Hi", '[', ']');

    draw_text(&greeting);
    println!("");

    draw_text(&boxed_greeting);
    println!("");
}
```

### reference to trait

```rust
use std::mem::size_of_val;

trait Draw {
    fn draw(&self);
}
struct Text {
    characters: String,
}
impl Text {
    fn from(text: &str) -> Text {
        Text {
            characters: text.to_string(),
        }
    }
}
impl Draw for Text {
    fn draw(&self) {
        print!("{}", self.characters);
    }
}
struct BoxedText {
    text: Text,
    first: char,
    last: char,
}

impl BoxedText {
    fn with_text_and_borders(text: &str, first: char, last: char) -> BoxedText {
        BoxedText {
            text: Text::from(text),
            first: first,
            last: last,
        }
    }
}
impl Draw for BoxedText {
    fn draw(&self) {
        print!("{}", self.first);
        self.text.draw();
        print!("{}", self.last);
    }
}

fn draw_text(txt: &dyn Draw) {
    print!(
        "{} {} {} ",
        size_of_val(txt),
        size_of_val(&txt),
        size_of_val(&&txt)
    );
    txt.draw();
}

fn main() {
    let greeting = Text::from("Hello");
    let boxed_greeting = BoxedText::with_text_and_borders("Hi", '[', ']');

    draw_text(&greeting);
    println!("");
    println!(
        "{} {} {}",
        size_of_val(&greeting),
        size_of_val(&&greeting),
        size_of_val(&&&greeting),
    );

    draw_text(&boxed_greeting);
    println!("");
    println!(
        "{} {} {}",
        size_of_val(&boxed_greeting),
        size_of_val(&&boxed_greeting),
        size_of_val(&&&boxed_greeting)
    );
}
```

---

## value / data

### destructor

```rust
struct CommunicationChannel {
    address: String,
    port: u16,
}
impl Drop for CommunicationChannel {
    fn drop(&mut self) {
        println!("Closing port {}:{}", self.address, self.port);
    }
}

impl CommunicationChannel {
    fn create(address: &str, port: u16) -> CommunicationChannel {
        println!("Opening port {}:{}", address, port);
        CommunicationChannel {
            address: address.to_string(),
            port: port,
        }
    }
    fn send(&self, msg: &str) {
        println!(
            "Sent to {}:{} the message '{}'",
            self.address, self.port, msg
        );
    }
}

fn main() {
    let channel = CommunicationChannel::create("usb4", 879);
    channel.send("Message 1");
    {
        let channel = CommunicationChannel::create("eth1", 12000);
        channel.send("Message 2");
    }
    channel.send("Message 3");
}
```

```rust
struct S(i32);
impl Drop for S {
    fn drop(&mut self) {
        println!("Dropped {}", self.0);
    }
}

fn main() {
    let _a = S(1);
    let _b = S(2);
    let _c = S(3);
    {
        let _d = S(4);
        let _e = S(5);
        let _f = S(6);
        println!("INNER");
    }
    println!("OUTER");
}
```

### assignment

share semantic

copy semantic (clone semantic)

move semantic

```rust
fn int_assign() {
    let i1: i32 = 123;
    let i2 = i1.clone();
    let i3 = i1; // copy

    print!("{} ", i1);
    print!("{} ", i2);
    print!("{} ", i3);
}

fn string_assign() {
    let s1 = "abcd".to_string();
    let s2 = s1.clone();
    let s3 = s1; // move

    // print!("{} ", s1.len());
    print!("{} ", s2.len());
    print!("{} ", s3.len());
}

fn vec_assign() {
    let v1 = vec![11, 22, 33];
    let v2 = v1.clone();
    let v3 = v1; // move

    // println!("{} ", v1.len());
    println!("{} ", v3.len());
    println!("{} ", v3.len());
}
fn box_assign() {
    let i1 = Box::new(12345i16);
    let i2 = i1.clone();
    let i3 = i1; // move

    // print!("{} ", i1);
    print!("{} ", i2);
    print!("{} ", i3);
}

fn main() {
    println!("*** begin int_assign ***");
    int_assign();
    println!("*** end int_assign ***");

    println!("*** begin string_assign ***");
    string_assign();
    println!("*** end string_assign ***");

    println!("*** begin vec_assign ***");
    vec_assign();
    println!("*** end vec_assign ***");

    println!("*** begin box_assign ***");
    box_assign();
    println!("*** end box_assign ***");
}
```

### move vs copy performance

```rust
use std::time::Instant;
fn elapsed_ms(t1: Instant, t2: Instant) -> f64 {
    let t = t2 - t1;
    t.as_secs() as f64 * 1000. + t.subsec_nanos() as f64 / 1e6
}

const N_ITER: usize = 100_000_000;

fn copy_semantic() {
    let start_time = Instant::now();
    for i in 0..N_ITER {
        let v1 = vec![11, 22];
        let mut v2 = v1.clone(); // Copy semantics is used
        v2.push(i);
        if v2[1] + v2[2] == v2[0] {
            print!("Error");
        }
    }
    let finish_time = Instant::now();

    println!("**** copy semantic ***");
    print!(
        "{} ns per iteration\n",
        elapsed_ms(start_time, finish_time) * 1e6 / N_ITER as f64
    );
}

fn move_semantic() {
    let start_time = Instant::now();
    for i in 0..N_ITER {
        let v1 = vec![11, 22];
        let mut v2 = v1; // Move semantics is used v2.push(i);
        if v2[1] + v2[2] == v2[0] {
            print!("Error");
        }
    }
    let finish_time = Instant::now();

    println!("move semantic");
    print!(
        "{} ns per iteration\n",
        elapsed_ms(start_time, finish_time) * 1e6 / N_ITER as f64
    );
}

fn main() {
    copy_semantic();
    move_semantic();
}
```

### ownership

```rust
// move semantic
fn main() {
    let v1 = vec![false; 3];
    let mut v2 = vec![false; 2];
    v2 = v1; // move

    // v1;

    fn f(v2: Vec<bool>) {}
    let v1 = vec![false; 3];
    f(v1); // move

    // v1;

    let v1 = vec![false; 0];
    let mut v2 = vec![false; 0];
    v2 = v1; // move

    // v1;

    struct S {}
    let s1 = S {};
    let s2 = s1; // move

    // s1;
}
```

```rust
// copy semantic
fn main() {
    // primitive number
    let i1 = 123;
    let i2 = i1; // copy
    println!("int: {} {}", i1, i2);

    // static string
    let s1 = "abc";
    let s2 = s1; // copy
    println!("&str: {} {}", s1, s2);

    // reference
    let r1 = &i1;
    let r2 = r1; // copy
    print!("ref: {} {}", r1, r2);
}
```

```txt
object          explicitly  implicitly  ie.
copyable        o           o           primitive number
cloneable       o           x           collection
non-cloneable   x           x           file handle
(non-copyable)
```

```rust
fn int_assign() {
    let i1: i32 = 123;
    let i2 = i1.clone();
    let i3 = i1; // copy

    print!("{} ", i1);
    print!("{} ", i2);
    print!("{} ", i3);
}

fn string_assign() {
    let s1 = "abcd".to_string();
    let s2 = s1.clone();
    let s3 = s1; // move

    // print!("{} ", s1.len());
    print!("{} ", s2.len());
    print!("{} ", s3.len());
}

fn vec_assign() {
    let v1 = vec![11, 22, 33];
    let v2 = v1.clone();
    let v3 = v1; // move

    // println!("{} ", v1.len());
    println!("{} ", v3.len());
    println!("{} ", v3.len());
}

fn box_assign() {
    let i1 = Box::new(12345i16);
    let i2 = i1.clone();
    let i3 = i1; // move

    // print!("{} ", i1);
    print!("{} ", i2);
    print!("{} ", i3);
}

fn main() {
    // copyable
    let a1 = 123;
    let b1 = a1.clone();
    let c1 = b1;
    println!("{} {} {}", a1, b1, c1);

    // cloneable
    let a2 = Vec::<bool>::new();
    let b2 = a2.clone();
    let c2 = b2;
    println!(" {:?}", a2);
    // ILLEGAL: print!("{:?}", b2);
    println!(" {:?}", c2);

    // non-cloneable
    let a3 = std::fs::File::open(".").unwrap();
    // ILLEGAL: let b3 = a3.clone();
    let c3 = a3;
    // ILLEGAL: print!("{:?}", a3);
    println!(" {:?}", c3);
}
```

### make cloneable or copyable

```rust
fn main() {
    struct S {}
    let s = S {};
    // s.clone();
    // no implement clone
}
```

=>

```rust
fn main() {
    struct S {}
    impl Clone for S {
        fn clone(&self) -> Self {
            Self {}
        }
    }
    // implement clone

    let s = S {};
    s.clone();

    let _s2 = s;
    // s;
    // no implement copy
}
```

=>

```rust
fn main() {
    struct S {}
    impl Clone for S {
        fn clone(&self) -> Self {
            Self {}
        }
    }
    impl Copy for S {}
    // implement copy & and auto matical from clone

    let s = S {};
    s.clone();

    let _s2 = s;
    s;
}
```

---

## reference

### borrow

```rust
fn case1() {
    println!("*** immut, immut, immut ***");
    let n = 12;
    println!("n: {n}");
    let ref_n = &n;
    println!("ref_n: {ref_n}");
    println!("n: {n}");
}

fn case2() {
    println!("*** immut, immut, mut ***");
    let n = 12;
    println!("n: {n}");
    let mut ref_n = &n;
    println!("ref_n: {ref_n}");
    println!("n: {n}");
}

fn case3() {
    println!("*** immut, mut, immut ***");
    let n = 12;
    println!("n: {n}");
    let ref_n = &12;
    // let ref_n = &mut n; // cannot borrow mutable
    println!("ref_n: {ref_n}");
    println!("n: {n}");
}

fn case4() {
    println!("*** mut, mut, immut ***");
    let mut n = 12;
    println!("n: {n}");
    let ref_n = &mut n;
    println!("ref_n: {ref_n}");
    println!("n: {n}");
}

fn case5() {
    println!("*** mut, mut, mut ***");
    let mut n = 12;
    println!("n: {n}");
    let mut ref_n = &mut n;
    println!("ref_n: {ref_n}");
    println!("n: {n}");
}

fn main() {
    case1();
    case2();
    case3();
    case4();
    case5();
}
```

```rust
fn main() {
    let n = 12;
    println!("n: {n}");
    let ref_n = &n; // n borrow ref_n
    println!("ref_n: {ref_n}");
    println!("n: {n}");
}
```

```rust
fn main() {
    let mut n = 12;
    println!("n: {n}");
    let ref_n = &mut n;  // n move ref_n
    println!("ref_n: {ref_n}");
    // println!("n: {n}"); // no n
    *ref_n += 10;
    println!("ref_n: {ref_n}");
}
```

=>

```rust
fn add(ref_n: &mut i32, val: i32) {
    *ref_n += val;
}

fn main() {
    let mut n = 12;
    println!("n: {n}");
    add(&mut n, 10); // n borrow fn
    println!("n: {n}");
}
```

可變不共用, 共用不可變. mutable is not shared, shared is immutable

### borrow error - after move error

```rust
// "use after move" error
fn main() {
    let ref_to_n;
    {
        let n = 12;
        ref_to_n = &n; // error
        print!("{} ", *ref_to_n);
    }
    print!("{}", *ref_to_n);
}
```

=>

```c
#include <stdio.h>

int main() {
    int* ref_to_n;
    {
        int n = 12;
        ref_to_n = &n; // error
        printf("%d ", *ref_to_n);
    }
    printf("%d", *ref_to_n);
    return 0;
}
```

```rust
// prevent "use after move" error
fn main() {
    let a = 12;
    let mut b = 13;
    println!("a: {}, b: {}", a, b);
    {
        let c = &a;
        let d = &mut b;
        println!("c: {}, d: {} ", c, d);
        *d += 1;
        println!("c: {}, d: {} ", c, d);
    }
    println!("a: {}, b: {}", a, b);
}
```

### borrow error - after drop error

```rust
// "use after drop" error
fn main() {
    let mut v = vec![12];
    let ref_to_first = &v[0];
    v.push(13); // error
    print!("{}", ref_to_first);
}
```

=>

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int* v = malloc(1 * sizeof (int)); v[0] = 12;
    const int* ref_to_first = &v[0];
    v = realloc(v, 2 * sizeof (int)); v[1] = 13; // error
    printf("%d", *ref_to_first);
    free(v);
}
```

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v { 12 };
    const int& ref_to_first = v[0];
    v.push_back(13); // error
    std::cout << ref_to_first;
}
```

### drop order

```rust
struct X(char);
impl Drop for X {
    fn drop(&mut self) {
        println!("{}", self.0);
    }
}

fn main() {
    let _a = X('a');
    let _b;
    let _c = X('c');
    _b = X('b');
}
// c
// b
// a
```

### multiple borrowing case

```rust
fn allowed_case1() {
    let a = 12;
    let _b = &a;
    let _c = &a;
}

fn allowed_case2() {
    let mut a = 12;
    let _b = &a;
    print!("{}", a);
}

fn allowed_case3() {
    let mut a = 12;
    a = 13;
    let _b = &a;
}

fn allowed_case4() {
    let mut a = 12;
    a = 13;
    let _b = &mut a;
}

fn allowed_case5() {
    let mut a = 12;
    print!("{}", a);
    let _b = &a;
}

fn allowed_case6() {
    let mut a = 12;
    print!("{}", a);
    let _b = &mut a;
}

fn illegal_case1() {
    let mut a = 12;
    let _b = &mut a;
    let _c = &a;
}

fn illegal_case2() {
    let mut a = 12;
    let _b = &a;
    let _c = &mut a;
}

fn illegal_case3() {
    let mut a = 12;
    let _b = &mut a;
    let _c = &mut a;
}

fn illegal_case4() {
    let mut a = 12;
    let _b = &a;
    a = 13;
}

fn illegal_case5() {
    let mut a = 12;
    let _b = &mut a;
    a = 13;
}

fn illegal_case6() {
    let mut a = 12;
    let _b = &mut a;
    print!("{}", a);
}

fn main() {
    allowed_case1();
    allowed_case2();
    allowed_case3();
    allowed_case4();
    allowed_case5();
    allowed_case6();

    illegal_case1();
    illegal_case2();
    illegal_case3();
    illegal_case4();
    illegal_case5();
    illegal_case6();
}
```

---

## lifetmie

### return reference

```rust
fn case_val_x1() {
    let v1 = vec![11u8, 22];
    let result;
    {
        let v2 = vec![33u8];
        result = {
            let _x1: &Vec<u8> = &v1;
            let _x2: &Vec<u8> = &v2;
            _x1
        }
    }
    println!("{:?}", *result);
}

fn case1_val_x2() {
    let v1 = vec![11u8, 22];
    let result;
    {
        let v2 = vec![33u8];
        result = {
            let _x1: &Vec<u8> = &v1;
            let _x2: &Vec<u8> = &v2;
            _x2
        }
    }
    println!("{:?}", *result);
}

fn case1_fn_x1() {
    let v1 = vec![11u8, 22];
    let result;
    {
        let v2 = vec![33u8];
        fn func(_x1: &Vec<u8>, _x2: &Vec<u8>) -> &Vec<u8> {
            _x1
        }
        result = func(&v1, &v2);
    }
    println!("{:?}", *result);
}

fn case1_fn_x2() {
    let v1 = vec![11u8, 22];
    let result;
    {
        let v2 = vec![33u8];
        fn func(_x1: &Vec<u8>, _x2: &Vec<u8>) -> &Vec<u8> {
            _x2
        }
        result = func(&v1, &v2);
    }
    println!("{:?}", *result);
}
```

### lifetime specfifier

```rust
// without lifetime specifier
trait Tr {
    fn f(flag: bool, b: &i32, c: (char, &i32)) -> (&i32, f64, &i32);
}
```

```rust
trait Tr {
    fn f<'a>(flag: bool, b: &'a i32, c: (char, &'a i32)) -> (&'a i32, f64, &'static i32);
}
```

```rust
trait Tr {
    fn f<'a>(flag: bool, b: &'a i32, c: (char, &i32)) -> (&'static i32, f64, &'a i32);
}
```

```rust
// two lifetime parameter, a, b
// two type parameter, T1, T2
trait Tr {
    fn f<'a, 'b, T1, T2>(flag: bool, b: &'a T1, c: (char, &'b i32)) -> (&'b i32, f64, &'a T2);
}
```

### validate lifetime specifier

```rust
static FOUR: u8 = 4;
fn f() -> (bool, &'static u8, &'static str, &'static f64) {
    (true, &FOUR, "Hello", &3.14)
}

fn main() {
    println!("{} {} {} {}", f().0, *f().1, f().2, *f().3);
}
```

```rust
fn fun2(n: &u8) -> &'static u8 {
    n // error
}

fn main() {
    println!("{}", *f(&12));
}
```

```rust
fn f<'a, 'b>(x: &'a i32, y: &'b i32) -> (&'b i32, bool, &'a i32) {
    (y, true, x)
}

fn main() {
    let i = 12;
    let j = 13;
    let r = f(&i, &j);
    println!("{} {} {}", *r.0, r.1, *r.2);
}
```

```rust
fn f<'a, 'b>(x: &'a i32, y: &'b i32) -> (&'b i32, bool, &'a i32) {
    (x, true, y) // error
}

fn main() {
    let i = 12;
    let j = 13;
    let r = f(&i, &j);
    println!("{} {} {}", *r.0, r.1, *r.2);
}
```

```rust
fn f<'a>(x: &'a i32, y: &'a i32) -> (&'a i32, bool, &'a i32) {
    (x, true, y)
}

fn main() {
    let i = 12;
    let j = 13;
    let r = f(&i, &j);
    println!("{} {} {}", *r.0, r.1, *r.2);
}
```

```rust
fn f<'a>(n: i32, x: &'a Vec<u8>, y: &Vec<u8>) -> &'a u8 {
    if n == 0 {
        return &x[0];
    }
    if n < 0 {
        &x[1]
    } else {
        &x[2]
    }
}
```

```rust
fn f<'a>(n: i32, x: &'a Vec<u8>, y: &Vec<u8>) -> &'a u8 {
    if n == 0 {
        return &x[0];
    }
    if n < 0 {
        &x[1]
    } else {
        &y[2]
    }
}
```

```rust
fn f<'a>(x: &'a Vec<u8>, y: &Vec<u8>) -> &'a u8 {
    if true {
        &x[0]
    } else {
        &y[0]
    }
}
```

### invoked function with lifetime specifier

```rust
fn f() {
    let v1 = vec![11u8, 22];
    let result;
    {
        let v2 = vec![33u8];
        fn func<'a>(_x1: &'a Vec<u8>, _x2: &Vec<u8>) -> &'a Vec<u8> {
            _x1
        }
        result = func(&v1, &v2);
    }
    println!("{:?}", *result);
}
```

```rust
fn f() {
    let v1 = vec![11u8, 22];
    let result;
    {
        let v2 = vec![33u8];
        fn func<'a>(_x1: &Vec<u8>, _x2: &'a Vec<u8>) -> &'a Vec<u8> {
            _x2
        }
        result = func(&v1, &v2);
    }
    println!("{:?}", *result);
}
```

```rust
fn f<'a, 'b>(x: &'a i32, y: &'b i32) -> (&'a i32, bool, &'b i32) {
    (x, true, y)
}
```

```rust
fn f<'a>(x: &'a i32, y: &'a i32) -> (&'a i32, bool, &'a i32) {
    (x, true, y)
}
```

### lifetime elision

```rust
trait Tr {
    fn f(x: &u8) -> &u8;
}

// ==

trait Tr {
    fn f<'a>(x: &'a u8) -> &'a u8;
}
```

```rust
trait Tr {
    fn f(b: bool, x: (u32, &u8)) -> &u8;
}
```

```rust
trait Tr {
    fn f(x: &u8) -> (&u8, &f64, bool, &Vec<String>);
}

// ==

trait Tr {
    fn f<'a>(x: &'a u8) -> (&u8, &'a f64, bool, &'static Vec<String>);
}
```

### lifetime elision with object-oriented programming

```rust
trait Tr {
    fn f(&self, y: &u8) -> (&u8, &f64, bool, &Vec<String>);
}

// ==

trait Tr {
    fn f<'a>(&'a self, y: &u8) -> (&'a u8, &'a f64, bool, &'a Vec<String>);
}

// ==

trait Tr {
    fn f<'a>(&self, y: &'a u8) -> (&u8, &'a f64, bool, &Vec<String>);
}
```

### lifetime specifier for struct

```rust
// legal
let x: i32 = 12;
let _y: &i32 = &x;

// illegal
let _y: &i32;
let x: i32 = 12;
_y = &x;
```

```rust
struct S {
    _b: bool,
    _ri: &i32,
}
let x: i32 = 12;
let _y: S = S { _b: true, _ri: &x };

// illegal
struct S {
    _b: bool,
    _ri: &i32,
}
let _y: S;
let x: i32 = 12;
_y = S { _b: true, _ri: &x };
```

```rust
struct S {
    _b: bool,
    _ri: &i32,
}

fn create_s(ri: &i32) -> S {
    S { _b: true, _ri: ri }
}

fn main() {
    let _y: S;
    let x: i32 = 12;
    _y = create_s(&x);
}

// =>

struct S {
    _b: bool,
    _ri: &'static i32,
}

fn create_s(ri: &i32) -> S {
    static ZERO: i32 = 0;
    static ONE: i32 = 1;
    S {
        _b: true,
        _ri: if *ri > 0 { &ONE } else { &ZERO },
    }
}

fn main() {
    let _y: S;
    let x: i32 = 12;
    _y = create_s(&x);
}
```

```rust
// syntax error
struct _S1 {
    _f: &i32,
}

struct _S2<'a> {
    _f: &i32,
}

struct _S3 {
    _f: &'a i32,
}

struct _S4<'a> {
    _f: &'static i32,
}

struct _S5 {
    _f: &'static i32,
}

struct _S6<'a> {
    _f: &'a i32,
}
```
