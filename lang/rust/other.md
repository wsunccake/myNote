```rust
fn main() {
    let x1 = 1;
    println!("x1: {}", x1);

    let x2 = x1; // copy
    println!("x2: {}", x2);
    println!("x1: {}", x1);

    let v1 = vec![1, 2, 3];
    println!("v1: {:?}", v1);

    let v2 = v1; // move
    println!("v2: {:?}", v2);
    println!("v1: {:?}", v1);

    let l1 = "rust";
    println!("l1: {}", l1);

    let l2 = l1; // copy
    println!("l2: {}", l2);
    println!("l1: {}", l1);

    let s1 = String::from("rust");
    println!("s1: {}", s1);

    let s2 = s1; // move
    println!("s2: {}", s2);
    println!("s1: {}", s1);
}
```

```rust
fn main() {
    let x1 = 1;
    println!("x1: {}", x1);

    let x2 = addx(x1); // copy
    println!("x2: {}", x2);
    println!("x1: {}", x1);

    let v1 = vec![1, 2, 3];
    println!("v1: {:?}", v1);

    let v2 = addv(v1); // move
    println!("v2: {:?}", v2);
    println!("v1: {:?}", v1);
}

fn addx(x: i32) -> i32 {
    x + 1
}

fn addv(v: Vec<i32>) -> Vec<i32> {
    let mut n = Vec::new();
    for i in v {
        n.push(i + 1);
    }
    n
}
```

---

## borrowing

```rust
fn main() {
    let v = vec![1, 2, 3];
    println!("main v: {:?}", v);

    print_vector1(v);
    println!("after vector1: {:?}", v);

    print_vector2(&v);
    println!("after vector2: {:?}", v);
}

fn print_vector1(v: Vec<i32>) {
    println!("print vector1: {:?}", v);
}

fn print_vector2(v: &Vec<i32>) {
    println!("print vector2: {:?}", v);
}
```

---
