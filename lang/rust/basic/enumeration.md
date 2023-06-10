# enumeration

## enum

```rust
// c style
#[derive(Debug)]
enum Ordering {
    Less,
    Equal,
    Greater,
}

fn compare(n: i32, m: i32) -> Ordering {
    if n < m {
        Ordering::Less
    } else if n > m {
        Ordering::Greater
    } else {
        Ordering::Equal
    }
}

fn main() {
    let result = compare(2, 2);
    println!("{:?}", result);
}
```

---

## with different value

```rust
#[derive(Debug)]
enum IpAddrKind {
    V4,
    V6,
}

#[derive(Debug)]
struct IpAddr {
    kind: IpAddrKind,
    address: String,
}

fn main() {
    let home = IpAddr {
        kind: IpAddrKind::V4,
        address: String::from("127.0.0.1"),
    };
    println!("{:?}", home);

    let loopback = IpAddr {
        kind: IpAddrKind::V6,
        address: String::from("::1"),
    };

    println!("{:?}", loopback);
}
```

refactor ->

```rust
#[derive(Debug)]
enum IpAddr {
    V4(String),
    V6(String),
}

fn main() {
    let home = IpAddr::V4(String::from("127.0.0.1"));
    println!("{:?}", home);

    let loopback = IpAddr::V6(String::from("::1"));
    println!("{:?}", loopback);
}
```

refactor ->

```rust
#[derive(Debug)]
enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

fn main() {
    let home = IpAddr::V4(127, 0, 0, 1);
    println!("{:?}", home);

    let loopback = IpAddr::V6(String::from("::1"));
    println!("{:?}", loopback);
}
```

---

## option

```rust
// defined by the standard library
enum Option<T> {
    None,
    Some(T),
}
```

```rust
let some_number = Some(5);
let some_char = Some('e');
let absent_number: Option<i32> = None;

let x: i8 = 5;
let y: Option<i8> = Some(5);
// let sum = x + y; // error
```

---

## match

---

```rust
#[derive(Debug)]
enum HttpStatus {
    Ok = 200,
    NotModified = 304,
    NotFound = 404,
}

// match
fn http_status_from_u32(n: u32) -> Option<HttpStatus> {
    match n {
        200 => Some(HttpStatus::Ok),
        304 => Some(HttpStatus::NotModified),
        404 => Some(HttpStatus::NotFound),
        _ => None,
    }
}

fn main() {
    assert_eq!(HttpStatus::Ok as i32, 200);
    let result = http_status_from_u32(404);
    println!("{:?}", result);
}
```

---

## impl

```rust
#[derive(Copy, Clone)]
enum Week {
    Monday = 1,
    Tuesday,
    Wednesday,
    Thursday,
    Friday,
    Saturday,
    Sunday,
}

impl Week {
    fn is_weekend(&self) -> bool {
        if (*self as u8) > 5 {
            return true;
        }
        false
    }
}

fn main() {
    let d = Week::Thursday;
    println!("{}", d.is_weekend());
}
```
