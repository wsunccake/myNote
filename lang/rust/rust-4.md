# rust

---

## content

- [closure](#closure)
- [iterator](#iterator)
  - [iterator consumer](#iterator-consumer)

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

### closure - function argurment

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

iterator

[iterator consumer](#iterator-consumer): [any](#any), [all](#all), [fold](#fold), [count](#count), [sum](#sum), product, collect

iterator adpater

```rs
let v: Vec<i32> = vec![1, 2, 3, 4, 5];

let r: std::ops::RangeInclusive<i32> = 1..=5;
```

```rs
fn main() {
    // no iterator, maybe out of range
    let v = vec![1, 2, 3, 4, 5];
    for idx in 0..v.len() {
        println!("{:?}", v[idx]);
    }

    // iterator
    let v = vec![1, 2, 3, 4, 5];
    for val in v.iter() {
        println!("{val:?}");
    }

    // iterator
    let v = vec![1, 2, 3, 4, 5];
    let mut iter = v.iter();
    loop {
        match iter.next() {
            Some(val) => println!("{val:?}"),
            None => break,
        }
    }
}
```

```rs
// imperative programming
fn sum_of_not_d2_d3_d5_1(num: u32) -> u32 {
    let mut sum = 0;
    for v in 0..=num {
        if (v % 2 != 0) && (v % 3 != 0) && (v % 5 != 0) {
            sum += v;
        }
    }
    sum
}

// functional programming
fn sum_of_not_d2_d3_d5_2(num: u32) -> u32 {
    (0..=num)
        .filter(|v| (v % 2 != 0) && (v % 3 != 0) && (v % 5 != 0))
        .sum()
}

fn main() {
    let sum = sum_of_not_d2_d3_d5_1(7);
    println!("{sum:?}");

    let sum = sum_of_not_d2_d3_d5_2(7);
    println!("{sum:?}");
}
```

### next

```rs
fn main() {
    let a = [1, 2, 3];
    let mut iter = a.iter();

    assert_eq!(Some(&1), iter.next());
    assert_eq!(Some(&2), iter.next());
    assert_eq!(Some(&3), iter.next());

    assert_eq!(None, iter.next());
    assert_eq!(None, iter.next());
    assert_eq!(None, iter.next());
}
```

### filter

```rs
fn main() {
    for v in 0..=100 {
        if v % 3 == 0 {
            println!("{v:?}");
        }
    }

    for v in (0..=100).filter(|v| v % 3 == 0) {
        println!("{v:?}");
    }

    let vec: Vec<i32> = vec![1, 2, 3, 4, 5];
    for v in vec.iter().filter(|&x| *x % 3) {
        println!("{v:?}");
    }
}
```

### enumerate

```rs
fn main() {
    let vec = vec![1, 2, 3, 4, 5];

    let mut pos = 0;
    for num in vec.iter() {
        println!("{pos}: {num}");
        pos += 1;
    }

    for (idx, num) in vec.iter().enumerate() {
        println!("{idx}: {num}");
    }
}
```

### map

```rs
fn main() {
    let vec = vec![1, 2, 3, 4, 5];
    for num in vec.iter().map(|x| x + x) {
        println!("{num}");
    }
}
```

### rev

```rs
fn main() {
    let vec = vec![1, 2, 3, 4, 5];
    for i in vec.iter().rev() {
        println!("{i}");
    }
}
```

### scan

```rs
fn main() {
    let vec = vec![1, 2, 3, 4, 5];
    for step in vec.iter().scan(0, |acc, x| {
        *acc += *x;
        Some(*acc)
    }) {
        println!("{} ", step);
    }
}
```

### skip

### nth

### count

### find

### cycle

### position

### iterator consumer

#### any

```rs
fn main() {
    let vec = vec![1, 2, 3, 4, 5];
    let res = vec.iter().any(char::is_uppercase);
    println!("{}", res);
}
```

#### all

```rs
fn main() {
    let vec = vec![1, 2, 3, 4, 5];
    let res = vec.iter().all(|&x| x != 2);
    println!("{}", res);
}
```

#### fold

```rs
fn main() {
    let vec = vec![1, 2, 3, 4, 5];
    let res = vec.iter().fold(0, |acc, x| acc + x);
    println!("{}", res);
}
```

#### sum

```rs
fn main() {
    let vec = vec![1, 2, 3, 4, 5];
    let sum = vec.iter().sum::<i32>();
    println!("{sum}");
}
```

#### product

```rs
fn main() {
    let vec = vec![1, 2, 3, 4, 5];
    let product = vec.iter().product::<i32>();
    println!("{product}");
}
```

#### max

```rs
fn main() {
    let vec = vec![1, 2, 3, 4, 5];
    let max = vec.iter().max().unwrap_or(&0);
    println!("{max}");
}
```

#### min

```rs
fn main() {
    let vec = vec![1, 2, 3, 4, 5];
    let min = vec.iter().min().unwrap_or(&0);
    println!("{min}");
}
```

#### collection

```rs
fn main() {
    let vec = (0..=100).collect::<Vec<_>>();
    println!("{vec:#?}");

    let vec = vec![1, 2, 3, 4, 5];
    let num_vec = vec.iter().map(|x| x + x).collect::<Vec<_>>();
    println!("{num_vec:#?}");
}
```
