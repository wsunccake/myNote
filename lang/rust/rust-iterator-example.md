# rust iterator

---

## content

- [basic](#basic)
  - [next](#next)
- [iterator adapter](#iterator-adapter)
  - [enumerate](#enumerate)
  - [filter](#filter)
  - [map](#map)
  - [filter_map]
  - [flat_map]
  - [scan](#scan)
  - [take]
  - [take_while]
  - [rev](#rev)
  - [skip](#skip)
  - [nth](#nth)
- [iterator consumer](#iterator-consumer)

---

## basic

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

[iterator adapter](#iterator-adapter)

[iterator consumer](#iterator-consumer): [any](#any), [all](#all), [fold](#fold), [count](#count), [sum](#sum), product, collect

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

---

## iterator adapter

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

---

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

---
