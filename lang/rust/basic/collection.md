# collection

## vector

```rust
fn main() {
    let mut v1: Vec<i32> = Vec::new();
    v1.push(5);
    v1.push(6);
    v1.push(7);
    v1.push(8);

    let v2 = vec![1, 2, 3, 4, 5];
    assert_eq!(v2.len(), 5);
    assert_eq!(v2[0], 1);
    assert_eq!(v2.pop(), Some(5));
    assert_eq!(v2.len(), 4);

    v2.extend([1, 2, 3]);
    for i in &v2 {
        println!("{i}");
    }

    let third: Option<&i32> = v2.get(2);
    match third {
        Some(third) => println!("The third element is {third}"),
        None => println!("There is no third element."),
    }

    // let does_not_exist = &v2[100]; // error: index out of bounds
    let does_not_exist = v2.get(100);
    println!("{:?}", does_not_exist);

    let v3 = Vec::from([0, 0, 0]);
    let v4 = vec![0; 3];
    assert_eq!(v3, v4);
}
```

---

## string

```rust
let s = "initial contents".to_string();
let s = String::from("initial contents");

let hello = String::from("السلام عليكم");
let hello = String::from("Dobrý den");
let hello = String::from("Hello");
let hello = String::from("שָׁלוֹם");
let hello = String::from("नमस्ते");
let hello = String::from("こんにちは");
let hello = String::from("안녕하세요");
let hello = String::from("你好");
let hello = String::from("Olá");
let hello = String::from("Здравствуйте");
let hello = String::from("Hola");

let mut s = String::from("lo");
s.push('l');
assert_eq(s, "lol");

let s1 = String::from("tic");
let s2 = String::from("tac");
let s3 = String::from("toe");

let s = s1 + "-" + &s2 + "-" + &s3;
assert_eq!(s, "tic-tac-toe");

let s = format!("tic-{s2}-{s3}");
assert_eq!(s, "tic-tac-toe");

let hello = String::from("Hola");
let answer = &hello[0];
let s = &hello[0..4];

for c in hello.chars() {
    println!("{c}");
}
```

---

## hash map

```rust
use std::collections::HashMap;

fn main() {
    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);

    let team_name = String::from("Blue");
    let score = scores.get(&team_name).copied().unwrap_or(0);

    for (key, value) in &scores {
        println!("{key}: {value}");
    }

    scores.entry(String::from("Blue")).or_insert(50);
    println!("{:?}", scores);

    let text = "hello world wonderful world";
    let mut map = HashMap::new();
    for word in text.split_whitespace() {
        let count = map.entry(word).or_insert(0);
        *count += 1;
    }
    println!("{:?}", map);
}
```
