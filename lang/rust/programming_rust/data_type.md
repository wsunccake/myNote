# data type

## numeric

### integer

| type | value                                        |
| :--- | :------------------------------------------- |
| i8   | $$ -2^7 \sim 2^7, (-128 \sim 127) $$         |
| i16  | $$ -2^15 \sim 2^15, (-32,768 \sim 32,767) $$ |
| i32  | $$ -2^31 \sim 2^31 $$                        |
| i64  | $$ -2^63 \sim 2^63 $$                        |
| i128 | $$ -2^127 \sim 2^127 $$                      |
| u8   | $$ 0 \sim 2^8, (0 \sim 255) $$               |
| u16  | $$ 0 \sim 2^16, (0 \sim 65,535) $$           |
| u32  | $$ 0 \sim 2^32 $$                            |
| u64  | $$ 0 \sim 2^64 $$                            |
| u128 | $$ 0 \sim 2^128 $$                           |

| literal     | type     | decimal value |
| :---------- | :------- | :------------ |
| 116i8       | i8       | 116           |
| 116_i8      | i8       | 116           |
| 0x_cafe_u32 | u32      | 51966         |
| 0b0010_1010 | inferred | 42            |
| 0o_106      | inferred | 70            |

```rust
let v1: i8 = 10_i8;
let v2 = 2525_u16;

assert_eq!(v1 as u16, 10_u16);
assert_eq!(v2 as i16, 2525_i16);
assert_eq!(-1_i16 as i32, -1_i32);
assert_eq!(65535_u16 as i32, 65535_i32);
assert_eq!(1000_i16 as u8, 232_u8);
assert_eq!(65535_u32 as i16, -1_i16);
assert_eq!(-1_i8 as u8, 255_u8);
assert_eq!(255_u8 as i8, -1_i8);

assert_eq!(2_u16.pow(4), 16);
assert_eq!((-4_i32).abs(), 4);
assert_eq!(0b101101_u8.count_ones(), 4);

// println!("{}", (-4).abs());
println!("{}", (-4_i32).abs());
println!("{}", i32::abs(-4));
```

```rust
// checked
let mut i: i16 = 1_000;
// i = i * 1_000;
i = i.checked_mul(1_000).expect("multiplication overflow");
print!("{}", i);

assert_eq!((10_u8).checked_add(20), Some(30));
assert_eq!((100_u8).checked_add(200), None);

// wrapping
assert_eq!(100_u16.wrapping_mul(200), 20000);
assert_eq!(500_u16.wrapping_mul(500), 53392);
assert_eq!(500_i16.wrapping_mul(500), -12144);
assert_eq!(5_i16.wrapping_shl(17), 10);

// saturating
assert_eq!(32760_i16.saturating_add(10), 32767);
assert_eq!((-32760_i16).saturating_sub(10), -32768);

// overflowing
assert_eq!(255_u8.overflowing_sub(2), (253, false));
assert_eq!(255_u8.overflowing_add(2), (1, true));
```

| operation           | suffix |
| :------------------ | :----- |
| addtion             | add    |
| subtraction         | sub    |
| multiplication      | mul    |
| division            | div    |
| remainder           | rem    |
| negation            | neg    |
| absolute            | abs    |
| exponentiation      | pwd    |
| bitwise left shift  | shl    |
| bitwise right shift | shr    |

### floating point

| type | value                                               |
| :--- | :-------------------------------------------------- |
| f32  | $$ -3.4 \times 10^{38} \sim 3.4 \times 10^{38} $$   |
| f64  | $$ -1.8 \times 10^{308} \sim 1.8 \times 10^{308} $$ |

$
\begin{aligned}
\underbrace{\text{31415}}_{\text{integer}}
\overbrace{\text{.926}}^{\text{fractional}}
\underbrace{\text{e-4}}_{\text{exponent}}
\overbrace{\text{f64}}^{\text{type}}
\end{aligned}
$

```rust
assert!((-1. / f32::INFINITY).is_sign_negative());
assert_eq!(-f32::MIN, f32::MAX);
assert_eq!(5f32.sqrt() * 5f32.sqrt(), 5.); // exactly 5.0, per IEEE
assert_eq!((-1.01f64).floor(), -2.0);
```

---

## bool

```rust
assert_eq!(false as i32, 0);
assert_eq!(true as i32, 1);
```

---

## char

```rust
assert_eq!('*'.is_alphabetic(), false);
assert_eq!('β'.is_alphabetic(), true);
assert_eq!('8'.to_digit(10), Some(8));
assert_eq!('􏰀'.len_utf8(), 3);
assert_eq!(std::char::from_digit(2, 10), Some('2'));
```

---

## tuple

```rust
let text = "I see the eigenvalue in thine eye";
let (head, tail) = text.split_at(21);
assert_eq!(head, "I see the eigenvalue ");
assert_eq!(tail, "in thine eye");
assert_eq!(head, "I see the eigenvalue ");
assert_eq!(tail, "in thine eye");

let text = "I see the eigenvalue in thine eye"; let temp = text.split_at(21);
let head = temp.0;
let tail = temp.1;
assert_eq!(head, "I see the eigenvalue ");
assert_eq!(tail, "in thine eye");
```

---

## pointer

### reference

```rust
&T
& mut T
```

### box

```rust
let t = (12, "eggs");
let b = Box::new(t);
```

## raw pointer

```rust
*mut T
*const T
```

---

## array

```rust
let lazy_caterer: [u32; 6] = [1, 2, 4, 7, 11, 16];
let taxonomy = ["Animalia", "Arthropoda", "Insecta"];
assert_eq!(lazy_caterer[3], 7);
assert_eq!(taxonomy.len(), 3);

let mut sieve = [true; 10000];
for i in 2..100 {
    if sieve[i] {
        let mut j = i * i;
        while j < 10000 {
            sieve[j] = false;
            j += i;
        }
    }
}
assert!(sieve[211]);
assert!(!sieve[9876]);

let mut chaos = [3, 5, 4, 1, 2];
chaos.sort();
assert_eq!(chaos, [1, 2, 3, 4, 5]);
```

---

## vector

```rust
let mut primes = vec![2, 3, 5, 7];
assert_eq!(primes.iter().product::<i32>(), 210);
primes.push(11);
primes.push(13);
assert_eq!(primes.iter().product::<i32>(), 30030);

fn new_pixel_buffer(rows: usize, cols: usize) -> Vec<u8> {
    vec![0; rows * cols]
}

let mut pal = Vec::new();
pal.push("step");
pal.push("on");
pal.push("no");
pal.push("pets");
assert_eq!(pal, vec!["step", "on", "no", "pets"]);

let v: Vec<i32> = (0..5).collect();
assert_eq!(v, [0, 1, 2, 3, 4]);

let mut palindrome = vec!["a man", "a plan", "a canal", "panama"];
palindrome.reverse();
assert_eq!(palindrome, vec!["panama", "a canal", "a plan", "a man"]);

let mut v = vec![10, 20, 30, 40, 50];
v.insert(3, 35);
assert_eq!(v, [10, 20, 30, 35, 40, 50]);
v.remove(1);

let mut v = vec!["Snow Puff", "Glass Gem"];
assert_eq!(v.pop(), Some("Glass Gem"));
assert_eq!(v.pop(), Some("Snow Puff"));
assert_eq!(v.pop(), None);

let languages: Vec<String> = std::env::args().skip(1).collect();
for l in languages {
    println!("{}: {}", l,
        if l.len() % 2 == 0 {
            "functional"
        } else {
            "imperative"
        }
    );
}
```

---

## slice

```rust
let v: Vec<f64> = vec![0.0, 0.707, 1.0, 0.707];
let a: [f64; 4] = [0.0, -0.707, -1.0, -0.707];
let sv: &[f64] = &v;
let sa: &[f64] = &a;

fn print(n: &[f64]) { for elt in n {
        println!("{}", elt);
    }
}
print(&a);  // works on array
print(&v);  // work on vector
print(&v[0..2]);
print(&a[2..]);
print(&sv[1..3]);
```

---

## string

### string literal

```rust
let speech = "\"Ouch!\" said the well.\n";

println!("In the room the women come and go,
    Singing of Mount Abora");

println!("It was a bright, cold day in April, and \
    there were four of us-\
    more or less.");

let default_win_install_path = r"C:\Program Files\Gorillas";
let pattern = Regex::new(r"\d+(\.\d+)*");

println!(r###"
    This raw string started with 'r###"'.
    Therefore it does not end until we reach a quote mark ('"')
    followed immediately by three pound signs ('###'):
"###);

assert!("ONE".to_lowercase() == "one");
assert!("peanut".contains("nut"));
assert_eq!("    clean\n".trim(), "clean");

for word in "veni, vidi, vici".split(", ") {
    assert!(word.starts_with("v"));
}
```

### byte string

u8

```rust
let method = b"GET";
assert_eq!(method, &[b'G', b'E', b'T']);

let noodles = "noodles".to_string();
let oodles = &noodles[1..];
let poodles = "􏰀_􏰀";
assert_eq!("􏰀_􏰀".len(), 7);
assert_eq!("􏰀_􏰀".chars().count(), 3);

let mut s = "hello";
// s[0] = 'c'; // error: `&str` cannot be modified
// s.push('\n'); // error: `%str` no push method
```

### string

```rust
let error_message = "too many pets".to_string();

assert_eq!(format!("{}°{:02}′{:02}″N", 24, 5, 23), "24°05′23″N".to_string());

let bits = vec!["veni", "vidi", "vici"];
assert_eq!(bits.concat(), "venividivici");
assert_eq!(bits.join(", "), "veni, vidi, vici");
```

---

## type

```rust
type Bytes = Vec<u8>;

fn decode(data: &Bytes) {
    ...
}
```
