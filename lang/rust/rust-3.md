# rust - fp / functional programming

---

## content

- [closure](#closure)
  - [function argurment](#function-argurment)
- [iterator](#iterator)
  - [scanning string](#scanning-string)
  - [range to iterator](#range-to-iterator)
  - [array, slice, vector](#array-slice-vector)
  - [immutable and mutable](#immutable-and-mutable)
- [iterator adapter](#iterator-adapter)
  - [filter](#filter)
  - [map](#map)
  - [enumerate](#enumerate)
- [iterator consumer](#iterator-consumer)
  - [all](#all)
  - [count](#count)
  - [sum](#sum)
  - [min & max](#min--max)
  - [collect](#collect)
- [iterator chain](#iterator-chain)
- [iterator lazy](#iterator-lazy)

---

## closure

```rs
fn main() {
    fn add_one_v1(x: u32) -> u32 { x + 1 }
    let add_one_v2 = |x: u32| -> u32 { x + 1 };
    let add_one_v3 = |x| { x + 1 };
    let add_one_v4 = |x| x + 1;

    println!("add_one_v1: {:#?}", add_one_v1(1));
    println!("add_one_v2: {:#?}", add_one_v2(1));
    println!("add_one_v3: {:#?}", add_one_v3(1));
    println!("add_one_v4: {:#?}", add_one_v4(1));
}
```

### function argurment

```rs
fn max_num(v: &Vec<u8>) -> u8 {
    let mut m: u8 = v[0];
    for &val in v.iter() {
        m = if val > m { val } else { m };
    }
    m
}

fn min_num(v: &Vec<u8>) -> u8 {
    let mut m: u8 = v[0];
    for &val in v.iter() {
        m = if val < m { val } else { m };
    }
    m
}

fn cmp_num(v: &Vec<u8>, f: fn(u8, u8) -> bool) -> u8 {
    let mut m: u8 = v[0];
    for &val in v.iter() {
        m = if f(m, val) { m } else { val };
    }
    m
}

fn main() {
    let v1 = vec![1, 2, 3, 4, 5];
    let m1 = max_num(&v1);
    println!("{:#?} max: {m1}", v1);

    let v2 = vec![1, 2, 3, 4, 5];
    let m2 = min_num(&v1);
    println!("{:#?} min: {m2}", v2);

    let cmp = |x, y| x > y;
    let v3 = vec![1, 2, 3, 4, 5];
    let m3 = cmp_num(&v3, cmp);
    println!("{:#?} max: {m3}", v3);

    let v4 = vec![1, 2, 3, 4, 5];
    let m4 = cmp_num(&v4, |x, y| x < y);
    println!("{:#?} min: {m4}", v4);
}
```

---

## iterator

### scanning string

```rust
fn print_nth_char1(s: &str, mut n: u32) {
    let mut iter: std::str::Chars = s.chars();
    loop {
        let item: Option<char> = iter.next(); // use next
        match item {
            Some(c) => {
                if n == 1 {
                    println!("{}", c);
                }
            }
            None => {
                break;
            }
        }
        n -= 1;
    }
}

fn print_nth_char2(s: &str, mut n: u32) {
    let mut iter: std::str::Chars = s.chars();
    while let Some(c) = iter.next() {
        if n == 1 {
            println!("{}", c);
        }
        n -= 1;
    }
}

fn print_nth_char3(s: &str, mut n: u32) {
    for c in s.chars() {
        if n == 1 {
            println!("{}", c);
        }
        n -= 1;
    }
}

fn print_codes1(s: &str) {
    let mut iter = s.chars();
    loop {
        match iter.next() {
            Some(c) => {
                println!("{}: {}", c, c as u32);
            }
            None => {
                break;
            }
        }
    }
}

fn print_codes2(s: &str) {
    let mut iter = s.chars();
    while let Some(c) = iter.next() {
        println!("{}: {}", c, c as u32);
    }
}

fn print_codes3(s: &str) {
    for c in s.chars() {
        println!("{}: {}", c, c as u32);
    }
}

fn main() {
    let s = "€èe";
    print_nth_char1(s, 3);
    print_nth_char2(s, 3);
    print_nth_char3(s, 3);
    print_codes1(s);
    print_codes2(s);
    print_codes3(s);
}
```

### range to iterator

```rust
fn main() {
    // OK: std::ops::Range<u32> is an iterator
    let mut _v1: std::ops::Range<u32> = 0u32..10;
    let _it1: Option<u32> = _v1.next();

    // OK: std::ops::RangeFrom<u32> is an iterator
    let mut _v2: std::ops::RangeFrom<u32> = 5u32..;
    let _it2: Option<u32> = _v2.next();

    // Illegal: std::ops::RangeTo<u32> is not an iterator
    let mut _v3: std::ops::RangeTo<u32> = ..8u32;
    // let _it3 = _v3.next();

    // Illegal: std::ops::RangeFull is not an iterator
    let mut _v4: std::ops::RangeFull = ..;
    // let _it3 = _v4.next();
}
```

### array, slice, vector

```rust
fn main() {
    println!("*** slice ***");
    // slice
    for item_ref in (&[11u8, 22, 33]).iter() {
        println!("{} ", *item_ref);
    }
    // =>
    let slice: &[u8] = &[11u8, 22, 33];
    let slice_it: std::slice::Iter<u8> = slice.iter();
    for item_ref in slice_it {
        println!("{} ", *item_ref);
    }

    println!("*** array ***");
    // array
    for item_ref in [44, 55, 66].iter() {
        println!("{} ", *item_ref);
    }
    // =>
    let arr: [i32; 3] = [44, 55, 66];
    let arr_it: std::slice::Iter<i32> = arr.iter();
    for item_ref in arr_it {
        println!("{} ", *item_ref);
    }

    println!("*** vector ***");
    // vector
    for item_ref in vec!['a', 'b', 'c'].iter() {
        println!("{} ", *item_ref);
    }
    // =>
    let vec: Vec<char> = vec!['a', 'b', 'c'];
    let vec_it: std::slice::Iter<char> = vec.iter();
    for item_ref in vec_it {
        println!("{} ", *item_ref);
    }
}
```

### immutable and mutable

```rust
fn without_mutation() {
    println!("*** without mutation ***");

    let mut arr = [1, 2, 3, 4];
    println!("{:?}", arr);
    for iterator in arr {
        arr = [9, 8, 7, 6];
        println!("iterator: {}", iterator); // i still raw value
    }
    println!("{:?}", arr);

    let arr = [1, 2, 3, 4];
    println!("{:?}", arr);
    for mut iterator in arr {
        iterator += 10;
        println!("i: {}", iterator);
    }
    println!("{:?}", arr); // arr still raw value
}

fn with_mutation() {
    println!("*** with mutation ***");

    let arr = &[3, 4, 5];
    let iterator = arr.iter();
    for item_ref in iterator {
        print!("[{}] ", *item_ref);
    }
    println!("{:?}", arr);

    // let mut arr = &mut [3, 4, 5];
    // {
    //     let mut iterator = arr.iter();
    //     for mut item_ref in iterator {
    //         *item_ref += 1; // item_ref still immutable, compile error
    //     }
    // }
    // println!("{:?}", arr);

    let arr = &mut [3, 4, 5];
    {
        let iterator = arr.iter_mut();
        for item_ref in iterator {
            *item_ref += 10;
        }
    }
    println!("{:?}", arr);
}

fn array_slice_vector() {
    let slice: &mut [u8] = &mut [11u8, 22, 33];
    println!("+++ slice: {:?} +++", slice);
    let slice_it: std::slice::IterMut<u8> = slice.iter_mut();
    for item_ref in slice_it {
        *item_ref += 10;
        println!("{} ", *item_ref);
    }
    println!("--- slice: {:?} ---", slice);

    let mut arr: [i32; 3] = [44, 55, 66];
    println!("+++ arr: {:?} +++", arr);
    let arr_it: std::slice::IterMut<i32> = arr.iter_mut();
    for item_ref in arr_it {
        *item_ref += 10;
        println!("{} ", *item_ref);
    }
    println!("--- arr: {:?} ---", arr);

    let mut vec: Vec<char> = vec!['a', 'b', 'c'];
    println!("+++ vec: {:?} +++", vec);
    let vec_it: std::slice::IterMut<char> = vec.iter_mut();
    for item_ref in vec_it {
        *item_ref = if *item_ref == 'b' { 'B' } else { '-' };
        println!("{} ", *item_ref);
    }
    println!("--- vec: {:?} ---", vec);
}

fn main() {
    without_mutation();
    with_mutation();
    array_slice_vector();
}
```

---

## iterator adapter

### filter

```rust
fn main() {
    let arr = [66, -8, 43, 19, 0, -31];
    for n in arr.iter() {
        if *n < 0 {
            print!("{} ", n);
        }
    }

    let arr = [66, -8, 43, 19, 0, -31];
    for n in arr.iter().filter(|x| **x < 0) {
        print!("{} ", n);
    }
}
```

### map

```rust
fn main() {
    let arr = [66, -8, 43, 19, 0, -31];
    for n in arr.iter() {
        print!("{} ", n * 2);
    }

    let arr = [66, -8, 43, 19, 0, -31];
    for n in arr.iter().map(|x| *x * 2) {
        print!("{} ", n);
    }
}
```

### enumerate

```rust
fn main() {
    let arr = ['a', 'b', 'c'];
    for i in 0..arr.len() {
        print!("{} {}, ", i, arr[i]);
    }

    let arr = ['a', 'b', 'c'];
    for ch in arr.iter() {
        print!("{}, ", ch);
    }

    let arr = ['a', 'b', 'c'];
    let mut i = 0;
    for ch in arr.iter() {
        print!("{} {}, ", i, *ch);
        i += 1;
    }

    let arr = ['a', 'b', 'c'];
    for (i, ch) in arr.iter().enumerate() {
        print!("{} {}, ", i, *ch);
    }
}
```

---

## iterator consumer

```rust
fn main() {
    let s = "Hello, world!";
    let ch = 'R';
    let mut contains = false;
    for c in s.chars() {
        if c == ch {
            contains = true;
        }
    }
    print!(
        "\"{}\" {} '{}'.",
        s,
        if contains {
            "contains"
        } else {
            "does not contain"
        },
        ch
    );

    let s = "Hello, world!";
    let ch = 'R';
    print!(
        "\"{}\" {} '{}'.",
        s,
        if s.chars().any(|c| c == ch) {
            "contains"
        } else {
            "does not contain"
        },
        ch
    );
}
```

```rust
fn main() {
    print!("{} ", [45, 8, 2, 6].iter().any(|n| *n < 0));
    print!("{} ", [45, 8, -2, 6].iter().any(|n| *n < 0));
    print!(
        "{} ",
        [45, 8, 2, 6].iter().any(|n: &i32| -> bool { *n < 0 })
    );
    print!(
        "{} ",
        [45, 8, -2, 6].iter().any(|n: &i32| -> bool { *n < 0 })
    );
}
```

### all

```rust
fn main() {
    print!(
        "{} ",
        [45, 8, 2, 6].iter().all(|n: &i32| -> bool { *n > 0 })
    );
    print!(
        "{} ",
        [45, 8, -2, 6].iter().all(|n: &i32| -> bool { *n > 0 })
    );
}
```

### count

```rust
fn main() {
    let s = "€èe";
    print!("{} {}", s.chars().count(), s.len());
}
```

### sum

```rust
fn main() {
    print!("{}", [45, 8, -2, 6].iter().sum::<i32>());

    let s: i32 = [45, 8, -2, 6].iter().sum();
    print!("{}", s);

    let s: u32 = [].iter().sum();
    print!("{}", s);
}
```

### min & max

```rust
fn main() {
    let arr = [45, 8, -2, 6];
    match arr.iter().min() {
        Some(n) => print!("{} ", n),
        _ => (),
    }
    match arr.iter().max() {
        Some(n) => print!("{} ", n),
        _ => (),
    }
    match [0; 0].iter().min() {
        Some(n) => print!("{} ", n),
        _ => print!("---"),
    }

    let arr = ["hello", "brave", "new", "world"];
    match arr.iter().min() {
        Some(n) => print!("{} ", n),
        _ => (),
    }
    match arr.iter().max() {
        Some(n) => print!("{} ", n),
        _ => (),
    }
}
```

### collect

```rust
fn main() {
    let arr = [36, 1, 15, 9, 4];
    let v = arr.iter().collect::<Vec<&i32>>();
    println!("{:?}", v);

    let arr = [36, 1, 15, 9, 4];
    let v = arr.iter().collect::<Vec<_>>();
    println!("{:?}", v);

    let arr = [36, 1, 15, 9, 4];
    let v: Vec<_> = arr.iter().collect();
    println!("{:?}", v);

    let s = "Hello";
    println!("{:?}", s.chars().collect::<String>());
    println!("{:?}", s.chars().collect::<Vec<char>>());
    println!("{:?}", s.bytes().collect::<Vec<u8>>());
    println!("{:?}", s.as_bytes().iter().collect::<Vec<&u8>>());
}
```

---

## iterator chain

```rust
fn main() {
    let arr = [66, -8, 43, 19, 0, -31];
    let mut v = vec![];
    for i in 0..arr.len() {
        if arr[i] > 0 {
            v.push(arr[i] * 2);
        }
    }
    println!("{:?}", v);

    let arr = [66, -8, 43, 19, 0, -31];
    let mut v = vec![];
    for n in arr.iter() {
        if *n > 0 {
            v.push(*n * 2);
        }
    }
    println!("{:?}", v);

    let arr = [66, -8, 43, 19, 0, -31];
    let mut v = vec![];
    for n in arr.iter().filter(|x| **x > 0).map(|x| *x * 2) {
        v.push(n);
    }
    println!("{:?}", v);

    let arr = [66, -8, 43, 19, 0, -31];
    let v = arr
        .iter()
        .filter(|x| **x > 0)
        .map(|x| *x * 2)
        .collect::<Vec<_>>();
    println!("{:?}", v);
}
```

---

## iterator lazy

```rust
fn main() {
    let v = [66, -8, 43, 19, 0, -31]
        .iter()
        .filter(|x| {
            print!("F{} ", x);
            **x > 0
        })
        .map(|x| {
            println!("M{} ", x);
            *x * 2
        })
        .collect::<Vec<_>>();
    println!("{:?}", v);

    [66, -8, 43, 19, 0, -31]
        .iter()
        .filter(|x| {
            print!("F{} ", x);
            **x > 0
        })
        .map(|x| {
            print!("M{} ", x);
            *x * 2
        });
}
```
