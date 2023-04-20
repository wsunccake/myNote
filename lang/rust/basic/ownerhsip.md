# ownership

## heap and stack

```cpp
std::string s = "hello";
// s in stack
// "hello" in heap
```

```rust
let s: String = String::from( "hello");
// s in stack
// "hello" in heap
```

```rust
fn main() {
    let mut s = String::from("hello");
    s.push_str(", world!");
    println!("{}", s);

    let s = "hello";
    // s.push_str(", world!"); // error: string literal can't change
    println!("{}", s);
}
```

## move and copy / clone

```python
s = ['udon', 'ramen', 'soba']
t = s
u = s
# s -> "udon", "ramen", "soba"
# t = s -> "udon", "ramen", "soba"
# u = s -> "udon", "ramen", "soba"
# s, t, u data in same heap
```

```cpp
using namespace std;
vector<string> s = { "udon", "ramen", "soba" };
vector<string> t = s;
vector<string> u = s;
// s -> "udon", "ramen", "soba"
// t -> "udon", "ramen", "soba"
// u -> "udon", "ramen", "soba"
// s, t, u data in different heap
```

```rust
let s = vec!["udon".to_string(), "ramen".to_string, "soba".to_string()];
let t = s;
let u = s;
// s -> "udon", "ramen", "soba"
// t -> "udon", "ramen", "soba", s -> none
// u -> s -> none
```

### same scope

```rust
fn main() {
    let x1 = 1;
    println!("x1: {}", x1);
    let x2 = x1; // copy
    println!("x2: {}", x2);
    println!("x1: {}", x1);

    let s1 = String::from("hello");
    println!("s1: {}", s1);
    let s2 = s1; // move
    println!("s2: {}", s2);
    // println!("s1: {}", s1); // error: s1 value borrowed here after move
    let s3 = s2.clone();
    println!("s3: {}", s3);
    println!("s2: {}", s2);
}
```

```rust
fn main() {
    let x = 0;
    println!("begin x: {}", x);

    let s = "hello".to_string();
    println!("begin s: {}", s);

    {
        let xx = x;
        println!("scope xx:{}", xx);
        let ss = s;
        println!("scope ss:{}", ss);
    }

    println!("end x: {}", x);
    // println!("end s: {}", s);
}
```

### function

```rust
fn main() {
    let x = 5;
    makes_copy(x);
    println!("x: {}", x);

    let s1 = String::from("hello");
    takes_ownership(s1);
    // println!("s1: {}", s1); // error
    let s2 = String::from("hello");
    let s3 = takes_and_gives_back(s2);
    println!("s3: {}", s3);
}

fn makes_copy(some_integer: i32) {
    println!("{}", some_integer);
}

fn takes_ownership(some_string: String) {
    println!("{}", some_string);
}

fn takes_and_gives_back(a_string: String) -> String {
    a_string
}
```

---

## reference and borrowing
