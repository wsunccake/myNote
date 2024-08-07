# rust - basic

---

## content

- [data type](#data-type)
  - [declare variable](#decision)
  - [integer](#integer)
  - [float](#float)
  - [boolean](#boolean)
  - [charater](#charater)
- [variable](#variable)
  - [immutable](#immutable)
  - [mutable](#mutable)
  - [constant](#constant)
  - [shadow](#shadow)
- [string](#string)
  - [string literal](#string-literal)
  - [string object](#string-object)
  - [string method](#string-method)
  - [string char](#string-char)
- [operator](#operator)
  - [arithmetic operator](#arithmetic-operator)
  - [relational operator](#relational-operator)
  - [logical operator](#logical-operator)
  - [bitwise operator](#bitwise-operator)
- [decision](#decision)
  - [if](#if)
  - [match](#match)
- [loop](#loop)
  - [for](#for)
  - [while](#while)
  - [loop](#loop)
- [function](#function)
  - [function - define](#function---define)
  - [function - return](#function---return)
  - [function - call by value](#function---call-by-value)
  - [function - call by reference](#function---call-by-reference)
- [tuple](#tuple)
- [array](#array)
  - [array - function - pass by value](#array---function---pass-by-value)
  - [array - function - pass by reference](#array---function---pass-by-reference)
  - [array - declare with constant](#array---declare-with-constant)
- [ownership](#ownership)
  - [ownership - rule](#ownership---rule)
  - [copy](#copy)
  - [move](#move)
  - [clone](#clone)
  - [ownership - function](#ownership---function)
- [borrowing](#borrowing)
  - [reference](#reference)
  - [mutable reference](#mutable-reference)
  - [borrowing - rule](#borrowing---rule)
- [slice](#slice)
  - [range](#range)
  - [array and vector](#array-and-vector)
  - [out of range](#out-of-range)
  - [mutable slice](#mutable-slice)
  - [open-ended range and slice](#open-ended-range-and-slice)

---

## data type

### declare variable

```rust
fn main() {
    let company_string = "TutorialsPoint";     // string type
    let rating_float = 4.5;                    // float type
    let is_growing_boolean = true;             // boolean type
    let icon_char = '♥';                       //unicode character type

    println!("company name is:{}", company_string);
    println!("company rating on 5 is:{}", rating_float);
    println!("company is growing :{}", is_growing_boolean);
    println!("company icon is:{}", icon_char);
}
```

```rust
fn print_type_of<T>(_: &T) {
    println!("{}", std::any::type_name::<T>())
}

fn main() {
    let s = "Hello";
    let i = 42_i8;
    let u = 42_u8;

    print_type_of(&s); // &str
    print_type_of(&i); // i8
    print_type_of(&u); // u8
    print_type_of(&vec![1, 2, 4]); // ::print_type_of<i32>
    print_type_of(&main); // ::main
    print_type_of(&print_type_of::<i32>); // ::print_type_of<i32>
    print_type_of(&{ || "Hi!" }); // ::main::{{closure}}
}
```

### integer

```text
Size	    Signed	    Unsigned
8 bit	    i8	        u8
16 bit	    i16	        u16
32 bit	    i32	        u32
64 bit	    i64	        u64
128 bit	    i128	    u128
Arch	    isize	    usize
```

```rust
fn main() {
    let result = 10;        // i32 by default
    let age: u32 = 20;
    let sum: i32 = 5 - 15;
    let mark: isize = 10;
    let count: usize = 30;

    println!("result value is {}", result);
    println!("sum is {} and age is {}", sum, age);
    println!("mark is {} and count is {}", mark, count);

    // overflow
    // 0 to 255 only allowed for u8
    let weight: u8 = 256;   //overflow value is 0
    let height: u8 = 257;   //overflow value is 1
    let score: u8 = 258;    //overflow value is 2

    println!("weight is {}", weight);
    println!("height is {}", height);
    println!("score is {}", score);
}
```

```rust
fn main() {
    println!("usize MAX: {}, MIN: {}", usize::MAX, usize::MIN);
    println!("u8 MAX: {}, MIN: {}", u8::MAX, u8::MIN);
    println!("u16 MAX: {}, MIN: {}", u16::MAX, u16::MIN);
    println!("u32 MAX: {}, MIN: {}", u32::MAX, u32::MIN);
    println!("u64 MAX: {}, MIN: {}", u64::MAX, u64::MIN);
    println!("u128 MAX: {}, MIN: {}", u128::MAX, u128::MIN);

    println!("isize MAX: {}, MIN: {}", isize::MAX, isize::MIN);
    println!("i8 MAX: {}, MIN: {}", i8::MAX, i8::MIN);
    println!("i16 MAX: {}, MIN: {}", i16::MAX, i16::MIN);
    println!("i32 MAX: {}, MIN: {}", i32::MAX, i32::MIN);
    println!("i64 MAX: {}, MIN: {}", i64::MAX, i64::MIN);
    println!("i128 MAX: {}, MIN: {}", i128::MAX, i128::MIN);

    println!("f32 MAX: {}, MIN: {}", f32::MAX, f32::MIN);
    println!("f64 MAX: {}, MIN: {}", f64::MAX, f64::MIN);
}
```

### float

```rust
fn main() {
    let result = 10.00;         //f64 by default
    let interest: f32 = 8.35;
    let cost: f64 = 15000.600;  //double precision

    println!("result value is {}", result);
    println!("interest is {}", interest);
    println!("cost is {}", cost);

    // automatic type casting
    // integer assigned to float variable
    let interest: f32 = 8;

    println!("interest is {}", interest);

    // number separator
    let float_with_separator = 11_000.555_001;
    println!("float value {}", float_with_separator);

    let int_with_separator = 50_000;
    println!("int value {}", int_with_separator);
}
```

### boolean

```rust
fn main() {
    let isfun: bool = true;
    println!("Is Rust Programming Fun ? {}", isfun);
}
```

### charater

```rust
fn main() {
    let special_character = '@'; //default
    let alphabet: char = 'A';
    let emoji: char = '😁';

    println!("special character is {}", special_character);
    println!("alphabet is {}", alphabet);
    println!("emoji is {}", emoji);
}
```

---

## variable

```rust
// immutable
let variable_name = value;                  // no type specified
let variable_name:dataType = value;         //type specified

// mutable
let mut variable_name = value;              // no type specified
let mut variable_name:dataType = value;     //type specified

// constant
const VARIABLE_NAME:dataType = value;
```

### immutable

```rust
fn main() {
    let fees = 25_000;
    let salary: f64 = 35_000.00;
    println!("fees is {} and salary is {}", fees, salary);

    fees = 35_000;
    println!("fees changed is {}", fees);
}
```

### mutable

```rust
fn main() {
    let mut fees = 25_000;
    let salary: f64 = 35_000.00;
    println!("fees is {} and salary is {}", fees, salary);

    fees = 35_000;
    println!("fees changed is {}", fees);
}
```

### constant

```rust
fn main() {
    const USER_LIMIT: i32 = 100; // integer constant
    const PI: f32 = 3.14;        // float constant

    println!("user limit is {}", USER_LIMIT);
    println!("pi value is {}", PI);
}
```

### shadow

```rust
fn main() {
    let salary = 100.00;
    let salary = 1.50;
    println!("The value of salary is :{}", salary);

    let uname = "Mohtashim";
    let uname = uname.len();
    println!("name changed to integer : {}", uname);

    const NAME: &str = "Mohtashim";
    const NAME: usize = NAME.len();
    println!("name changed to integer : {}", NAME);
}
```

---

## string

```rust
String Literal(&str)
String Object(String)
```

- string literal, static string
- string object, dynamic string

### string literal

```rust
fn main() {
    let hello: &str = "hello";
    let rust: &'static str = "rust";    // &'static str -> const char*

    println!("{} {}", hello, rust);
}
```

```rust
use std::mem::*;

fn main() {
    let a: &str = "";
    let b: &str = "0123456789";
    let c: &str = "abcdè";
    println!(
        "{:10} size: {:2}, {:2}, {:2}",
        a,
        size_of_val(a),
        size_of_val(&a),
        size_of_val(&&a)
    );
    println!(
        "{:10} size: {:2}, {:2}, {:2}",
        b,
        size_of_val(b),
        size_of_val(&b),
        size_of_val(&&b)
    );
    println!(
        "{:10} size: {:2}, {:2}, {:2}",
        c,
        size_of_val(c),
        size_of_val(&c),
        size_of_val(&&c)
    );
}
```

### string object

```rust
use std::mem::*;

fn main() {
    // empty string
    let empty_string = String::new();
    println!("length is {}", empty_string.len());

    // content string
    let content_string = String::from("rust");
    println!("length is {}", content_string.len());

    // change string
    let mut change_string: String = "Xy".to_string();
    println!("change_string: {}", change_string);
    change_string.remove(0);
    println!("change_string: {}", change_string);
    change_string.insert(0, 'H');
    println!("change_string: {}", change_string);
    change_string.pop();
    println!("change_string: {}", change_string);
    change_string.push('i');
    println!("change_string: {}", change_string);

    // string capacity, length, size
    let mut s1 = "".to_string();
    s1.push('e');
    let mut s2 = "".to_string();
    s2.push('è');
    let mut s3 = "".to_string();
    s3.push('€');
    println!(
        "{}: cap: {}, len: {}, size: {}",
        s1,
        s1.capacity(),
        s1.len(),
        size_of_val(&s1)
    );
    println!(
        "{}: cap: {}, len: {}, size: {}",
        s2,
        s2.capacity(),
        s2.len(),
        size_of_val(&s2)
    );
    println!(
        "{}: cap: {}, len: {}, size: {}",
        s3,
        s3.capacity(),
        s3.len(),
        size_of_val(&s3)
    );
}
```

```rust
fn main() {
    // empty string
    let s1 = String::new();
    let s2 = String::from("");
    let s3 = "".to_string();
    let s4 = "".to_owned();
    let s5 = format!("");
    print!("({}{}{}{}{})", s1, s2, s3, s4, s5);

    // content string
    let s = "a,";
    let s1 = String::from(s);
    let s2 = s.to_string();
    let s3 = s.to_owned();
    //let s4 = format!(s);
    //let s5 = format!("a,{}");
    let s6 = format!("{}", s);
    print!("({}{}{}{})", s1, s2, s3, s6);

    // concatenate string
    let ss1 = "He";
    let ss2 = "llo ";
    let ds1 = ss1.to_string();
    let ds2 = ss2.to_string();
    let ds3 = format!("{}{}", ss1, ss2);
    println!("{}", ds3);
    let ds3 = format!("{}{}", ss1, ds2);
    println!("{}", ds3);
    let ds3 = format!("{}{}", ds1, ss2);
    println!("{}", ds3);
    let ds3 = format!("{}{}", ds1, ds2);
    println!("{}", ds3);

    let mut dyn_str = "Hello".to_string();
    dyn_str = format!("{}{}", dyn_str, ", ");
    dyn_str = format!("{}{}", dyn_str, "world");
    dyn_str = format!("{}{}", dyn_str, "!");
    println!("{}", dyn_str);

    let mut dyn_str = "Hello".to_string();
    dyn_str.push_str(", ");
    dyn_str.push_str("world");
    dyn_str.push_str("!");
    println!("{}", dyn_str);

    let mut dyn_str = "Hello".to_string();
    dyn_str += ", ";
    dyn_str += "world";
    dyn_str += "!";
    println!("{}", dyn_str);

    let comma = ", ".to_string();
    let world = "world".to_string();
    let excl_point = '!';
    let mut dyn_str = "Hello".to_string();
    dyn_str += &comma;
    dyn_str.push_str(&world);
    dyn_str.push(excl_point);
    println!("{}", dyn_str);
}
```

```rust
fn type_of<T>(_: T) -> &'static str {
    std::any::type_name::<T>()
    // std::intrinsics::type_name::<T>()
}

fn main() {
    let s1 = "hello";
    println!("s1 value: {}", s1);
    println!("s1 type : {}", type_of(s1));

    let s2 = String::from("hello");
    println!("s2 value: {}", s2);
    println!("s2 type : {}", type_of(s2));

    println!("s1 == s2: {}", s1 == s2);
}
```

### string method

```rust
fn main() {
    // literal to object
    let s0 = "hello".to_string();
    println!("s0: {}", s0);

    // object - push
    let mut s1 = String::new();
    s1.push_str("hello");
    s1.push('!');
    println!("s1: {}", s1);

    // object - chars
    let s2 = String::from("rust");
    for token in s2.chars() {
        println!("token: {}", token);
    }

    // object - concate
    let s3 = String::from("hello");
    let s4 = "rust".to_string();
    let s5 = s3 + &s4;
    println!("s5: {}", s5);

    // object - format!
    let s6 = String::from("hello");
    let s7 = "rust".to_string();
    let s8 = format!("{} {}", s6, s7);
    println!("s8: {}", s8);
}
```

```rust
fn main() {
    // object to literal
    let s1 = String::from("hello");
    let s2 = s1.as_str();
    println!("s1: {}", s1);
    println!("s2: {}", s2);

    // object - replace
    let s3 = String::from("hello world");
    let s4 = s3.replace("world", "rust");
    println!("s4: {}", s4);

    // literal - len
    let s5 = "hello rust";
    println!("s5.len: {}", s5.len());

    // literal - split_whitespace
    let s6 = "c c++ go rust";
    for token in s6.split_whitespace() {
        println!("token: {}", token);
    }

    // literal - split
    let s7 = "c,c++,go,rust";
    for token in s7.split(",") {
        println!("token: {}", token);
    }

    // literal - trim
    let s8 = " c c++ go rust \r\n";
    println!("s8:--{}--!", s8.trim());
}
```

### string char

```rust
fn main() {
    let s = "abc012è€";
    println!("{}", s);
    let r = std::str::from_utf8(&[0xe2, 0x82, 0xac]).unwrap();
    println!("{}", r);

    println!("*** len ***");
    for i in 0..s.len() {
        let u = s.as_bytes()[i];
        let b = s.bytes().nth(i).unwrap_or_default();
        let c = s.chars().nth(i).unwrap_or_default();
        println!("{:2} -> {:4}, {:#02x} => {:4} => {:4}", i, u, u, b, c);
    }

    println!("*** byte ***");
    for b in s.bytes() {
        println!("{:<4} , {:<#8x} -> {:4}", b, b, b as char);
    }

    println!("*** char ***");
    for c in s.chars() {
        println!("{:4} -> {:>6}, {:<#8x}", c, c as u32, c as u32);
    }
}
```

---

## operator

### arithmetic operator

```rust
fn main() {
    let num1 = 10;
    let num2 = 2;
    let mut res: i32;

    res = num1 + num2;
    println!("Sum: {} ", res);

    res = num1 - num2;
    println!("Difference: {} ", res);

    res = num1 * num2;
    println!("Product: {} ", res);

    res = num1 / num2;
    println!("Quotient: {} ", res);

    res = num1 % num2;
    println!("Remainder: {} ", res);
}
```

### relational operator

```rust
fn main() {
    let A: i32 = 10;
    let B: i32 = 20;

    println!("Value of A:{} ", A);
    println!("Value of B : {} ", B);

    let mut res = A > B;
    println!("A greater than B: {} ", res);

    res = A < B;
    println!("A lesser than B: {} ", res);

    res = A >= B;
    println!("A greater than or equal to B: {} ", res);

    res = A <= B;
    println!("A lesser than or equal to B: {}", res);

    res = A == B;
    println!("A is equal to B: {}", res);

    res = A != B;
    println!("A is not equal to B: {} ", res);
}
```

### logical operator

```rust
fn main() {
    let a = 20;
    let b = 30;

    if (a > 10) && (b > 10) {
        println!("true");
    }
    let c = 0;
    let d = 30;

    if (c > 10) || (d > 10) {
        println!("true");
    }
    let is_elder = false;

    if !is_elder {
        println!("Not Elder");
    }
}
```

### bitwise operator

```rust
fn main() {
    let a: i32 = 2; // bit presentation 10
    let b: i32 = 3; // bit presentation 11

    let mut result: i32;

    result = a & b;
    println!("(a & b) => {} ", result);

    result = a | b;
    println!("(a | b) => {} ", result);

    result = a ^ b;
    println!("(a ^ b) => {} ", result);

    result = !b;
    println!("(!b) => {} ", result);

    result = a << b;
    println!("(a << b) => {}", result);

    result = a >> b;
    println!("(a >> b) => {}", result);
}
```

---

## decision

### if

```rust
fn main() {
    let num: i32 = 12;
    // if
    if num > 0 {
        println!("number is positive");
    }

    // if else
    if num % 2 == 0 {
        println!("Even");
    } else {
        println!("Odd");
    }

    // nested if
    if num > 0 {
        println!("{} is positive", num);
    } else if num < 0 {
        println!("{} is negative", num);
    } else {
        println!("{} is neither positive nor negative", num);
    }
}
```

### match

```rust
fn main() {
    let state_code = "MH";
    let state = match state_code {
        "MH" => {
            println!("Found match for MH");
            "Maharashtra"
        }
        "KL" => "Kerala",
        "KA" => "Karnadaka",
        "GA" => "Goa",
        _ => "Unknown",
    };
    println!("State name is {}", state);
}
```

### let if match

```rs
// let - if
fn main() {
    let a = 1;
    let b = 9;
    let max_value = if a > b { a } else { b };

    println!("max(a: {a:#?}, b: {b:#?}) = {max_value:#?}");
}
```

```rs
// match
fn main() {
    let config_max = Some(3u8);
    let value = match config_max {
        Some(max) => max,
        _ => 0,
    };
    println!("value: {value:#?}");
}
```

```rs
// if let
fn main() {
    let config_max = Some(3u8);
    let value = if let Some(max) = config_max { max } else { 0 };
    println!("value: {value:#?}");
}
```

---

## loop

### for

```rust
fn main() {
    let mut count = 0;
    for x in 1..11 {
        // 11 is not inclusive
        if x == 5 {
            continue;
        }

        count += 1;
        println!("x is {}", x);
    }

    println!("count: {} ", count);
}
```

### while

```rust
fn main() {
    let mut x = 0;
    while x < 10 {
        x += 1;
        println!("inside loop x value is {}", x);
    }

    println!("outside loop x value is {}", x);
}
```

### loop

```rust
fn main(){
   let mut x = 0;
   loop {
      x+=1;
      println!("x={}",x);

      if x==15 {
         break;
      }
   }
}
```

### let while match

```rs
// match
fn main() {
    let mut optional = Some(0);
    loop {
        match optional {
            Some(i) => {
                if i > 9 {
                    println!("Greater than 9, quit!");
                    optional = None;
                } else {
                    println!("`i` is `{:?}`. Try again.", i);
                    optional = Some(i + 1);
                }
            }
            _ => {
                break;
            }
        }
    }
}
```

```rs
// while let
fn main() {
    let mut optional = Some(0);
    while let Some(i) = optional {
        if i > 9 {
            println!("Greater than 9, quit!");
            optional = None;
        } else {
            println!("`i` is `{:?}`. Try again.", i);
            optional = Some(i + 1);
        }
    }
}
```

---

## function

```rust
// define function
fn function_name(param1, param2..paramN) {
   // function body
}

// call / invoke function
function_name(val1,val2,valN)

// define function with return
fn function_name(param1, param2..paramN) -> return_type {
    //statements
    return value;
}

fn function_name(param1, param2..paramN) -> return_type {
    //statements
    return value //no semicolon means this value is returned
}
```

### function - define

```rust
fn main() {
    //call function
    say_hello();
}

//define function
fn say_hello() {
    println!("hello rust");
}
```

### function - return

```rust
fn main() {
    println!("pi value is {}", get_pi());
}

fn get_pi() -> f64 {
    22.0 / 7.0
}
```

### function - call by value

```rust
fn main() {
    let no: i32 = 5;
    mutate_no_to_zero(no);
    println!("The value of no is:{}", no);
}

fn mutate_no_to_zero(mut n: i32) {
    n = 0;
}
```

### function - call by reference

```rust
fn main() {
    let mut no: i32 = 5;
    mutate_no_to_zero(&mut no);
    println!("The value of no is:{}", no);
}

fn mutate_no_to_zero(n: &mut i32) {
    *n = 0; //de reference
}
```

---

## tuple

```rust
let tuple_name:(data_type1,data_type2,data_type3) = (value1,value2,value3);
let tuple_name = (value1,value2,value3);
```

```rust
fn main() {
    let tuple: (i32, f64, u8) = (-325, 4.9, 22);
    println!("integer is :{:?}", tuple.0);
    println!("float is :{:?}", tuple.1);
    println!("unsigned integer is :{:?}", tuple.2);
}
```

---

## array

```rust
let variable_name = [value1,value2,value3];
let variable_name:[dataType;size] = [value1,value2,value3];
let variable_name:[dataType;size] = [default_value_for_elements,size]
```

```rust
fn main() {
    let arr:[i32; 4] = [-1; 4];
    println!("array is {:?}", arr);

    let arr: [i32; 4] = [10, 20, 30, 40];
    println!("array is {:?}", arr);
    println!("array size is :{}", arr.len());

    // loop by index
    for index in 0..4 {
        println!("index is: {} & value is : {}", index, arr[index]);
    }

    // loop by iterator
    for val in arr.iter() {
        println!("value is :{}", val);
    }

    // mutable array
    let mut arr: [i32; 4] = [10, 20, 30, 40];
    arr[1] = 0;
    println!("{:?}", arr);
}
```

### array - function - pass by value

```rust
fn main() {
    let arr = [10, 20, 30];
    update(arr);

    print!("Inside main {:?}", arr);
}

fn update(mut arr: [i32; 3]) {
    for i in 0..3 {
        arr[i] = 0;
    }
    println!("Inside update {:?}", arr);
}
```

### array - function - pass by reference

```rust
fn main() {
    let mut arr = [10, 20, 30];
    update(&mut arr);
    print!("Inside main {:?}", arr);
}

fn update(arr: &mut [i32; 3]) {
    for i in 0..3 {
        arr[i] = 0;
    }
    println!("Inside update {:?}", arr);
}
```

```rust
fn main() {
    let mut arr = [10, 20, 30];
    update(&mut arr);
    print!("Inside main {:?}", arr);
}

fn update(arr: &mut [i32]) {
    for i in 0..arr.len() {
        arr[i] = 0;
    }
    println!("Inside update {:?}", arr);
}
```

### array - declare with constant

```rust
fn main() {
    let N: usize = 20;
    let arr = [0; N]; //Error: non-constant used with constant
    print!("{}", arr[10])
}
```

```rust
fn main() {
    const N: usize = 20;
    let arr = [0; N]; // pointer sized
    print!("{}", arr[10])
}
```

---

## ownership

### ownership - rule

```text
each value in rust has an owner / Rust 中每個數值都有個擁有者 (owner)
there can only be one owner at a time / 同時間只能有一個擁有者
when the owner goes out of scope, the value will be dropped / 當擁有者離開作用域時, 數值就會被丟棄
```

heap:

stack: primitive type

```rust
fn main() {
    let msg = "hello";
    println!("main msg: {}", msg);

    {
        let msg = "rust";
        println!("in scope msg: {}", msg);
    }

    println!("main msg: {}", msg);
}
```

```rust
fn main() {
    let mut msg = "hello";
    println!("main msg: {}", msg);

    {
        msg = "rust";
        println!("in scope msg: {}", msg);
    }

    println!("main msg: {}", msg);
}
```

### copy

當 trait 實作 copy, = 則是 copy

當 trait 實作 drop, = 則是 move

copy 跟 drop 無法同時實作, 只能擇一

```rust
fn main() {
    let s1: &str = "rust";
    println!("s1: {}", s1);

    let s2 = s1; // copy
    println!("s2: {}", s2);
    println!("s1: {}", s1);
}
```

### move

```rust
fn main() {
    let s1: String = String::from("rust");
    println!("s1: {}", s1);

    let s2 = s1; // move
    println!("s2: {}", s2);
    println!("s1: {}", s1);
}
```

### clone

```rust
fn main() {
    let s1: String = String::from("rust");
    println!("s1: {}", s1);

    let s2 = s1.clone();
    println!("s2: {}", s2);
    println!("s1: {}", s1);
}
```

### ownership - function

```rust
fn main() {
    let s1: String = String::from("rust");
    println!("s1: {}", s1);
    hi(s1);
    // println!("s1: {}", s1);

    let s2 = "rust";
    println!("s2: {}", s2);
    hey(s2);
    println!("s2: {}", s2);

    let s3 = String::from("rust");
    println!("s3: {}", s3);
    let s3 = hello(s3);
    println!("s3: {}", s3);
}

fn hi(s: String) {
    println!("hi {}", s);
}

fn hey(s: &str) {
    println!("hey {}", s);
}

fn hello(s: String) -> String {
    println!("hello {}", s);
    s
}
```

---

## borrowing

### reference

```rust
fn main() {
    let s = String::from("rust");
    println!("s: {}", s);
    hi(&s);
    println!("s: {}", s);
}

fn hi(s: &String) {
    println!("hi {}", s);
}
```

### mutable reference

```rust
fn main() {
    let s1 = String::from("rust");
    change1(&s1);
    println!("s1: {}", s1);

    let mut s2 = String::from("rust");
    change2(&mut s2);
    println!("s2: {}", s2);
}

fn change1(s: &String) {
    s.push_str("!");
}

fn change2(s: &mut String) {
    s.push_str("!");
}
```

### borrowing - rule

race condition

```text
two or more pointers access the same data at the same time / 同時有兩個以上的指標存取同個資料。
at least one of the pointers is being used to write to the data / 至少有一個指標在寫入資料
there’s no mechanism being used to synchronize access to the data / 沒有針對資料的同步存取機制
```

```rust
fn main() {
    let mut s = String::from("hello");

    let r1 = &mut s;
    let r2 = &mut s;
 }

// =>

fn main() {
    let mut s = String::from("hello");

    {
        let r1 = &mut s;
    }

    let r2 = &mut s;
}
```

```rust
fn main() {
    let mut s = String::from("hello");

    let r1 = &s;
    let r2 = &s;
    let r3 = &mut s;
    println!("r1: {}, r2: {}, r3: {}", r1, r2, r3);
}

// =>

fn main() {
    let mut s = String::from("hello");

    let r1 = &s;
    let r2 = &s;
    println!("r1: {}, r2: {}", r1, r2);

    let r3 = &mut s;
    println!("r3: {}", r3);
}
```

```rust
fn main() {
    let r1 = dangle();
    let r2 = no_dangle();
}

fn dangle() -> &String {
    let s = String::from("hello");

    &s
}

fn no_dangle() -> String {
    let s = String::from("hello");

    s
}
```

---

## slice

```rust
fn main() {
    let s = String::from("hello");
    let len = s.len();

    let s1 = &s[0..2];
    let s2 = &s[..2];
    println!("s1: {}", s1);
    println!("s2: {}", s2);

    let s3 = &s[3..len];
    let s4 = &s[3..];
    println!("s3: {}", s3);
    println!("s4: {}", s4);

    let s5 = &s[0..len];
    let s6 = &s[..];
    println!("s5: {}", s5);
    println!("s6: {}", s6);
}
```

### range

```rust
use std::mem::*;

fn main() {
    let r1 = 3u8..12u8;
    let r2 = 3u8..12;
    let r3 = 3..12u8;
    let r4 = 3..12;
    let r5 = -3..12;
    let r6 = 3..12 as i64;
    println!("{:?} -> {}", r1, size_of_val(&r1),);
    println!("{:?} -> {}", r2, size_of_val(&r2),);
    println!("{:?} -> {}", r3, size_of_val(&r3),);
    println!("{:?} -> {}", r4, size_of_val(&r4),);
    println!("{:?} -> {}", r5, size_of_val(&r5),);
    println!("{:?} -> {}", r6, size_of_val(&r6),);
}
```

```rust
fn min(arr: &[i32]) -> i32 {
    // assume arr is not empty.
    let mut minimum = arr[0];
    for i in 1..arr.len() {
        if arr[i] < minimum {
            minimum = arr[i];
        }
    }
    minimum
}

fn main() {
    println!("{} ", min(&[23, 17, 12, 16, 15, 2][2..5]));

    let arr = [23, 17, 12, 16, 15, 2];
    let range = 2..5;
    let slice_ref = &arr[range];
    println!("{}", min(slice_ref));
}
```

### array and vector

```rust
fn main() {
    let arr = [55, 22, 33, 44, 66, 7, 8];
    let v = vec![55, 22, 33, 44, 66, 7, 8];
    let sr1 = &arr[2..5];
    let sr2 = &v[2..5];
    println!("{:?} {:?} {:?} {:?}", arr, sr1, &sr1[1..2], &sr1[1]);
    println!("{:?} {:?} {:?} {:?}", v, sr2, &sr2[1..2], &sr2[1]);
}
```

### out of range

```rust
fn main() {
    let arr = [55, 22, 33, 44, 66];
    let _r1 = 4..4;
    let _a1 = &arr[_r1];
    let _r2 = 4..3;
    //let _a2 = &arr[_r2];
    let _r3 = -3i32..2;
    //let _a3 = &arr[_r3];
    let _r4 = 3..8;
    //let _a4 = &arr[_r4];
}
```

### mutable slice

```rust
fn main() {
    let mut arr = [11, 22, 33, 44];
    println!("arr: {:?}", arr);
    {
        let sl_ref = &mut arr[1..3];
        println!("sl_ref: {:?}", sl_ref);
        sl_ref[1] = 0;
        println!("sl_ref: {:?}", sl_ref);
    }
    println!("arr: {:?}", arr);
}
```

### open-ended range and slice

```rust
fn main() {
    let arr = [11, 22, 33, 44];
    println!("arr: {:?}", arr);
    let n = 2;

    let sr1a = &arr[0..n];
    let sr2a = &arr[n..arr.len()];
    println!("sr1a: {:?}", sr1a,);
    println!("sr2a: {:?}", sr2a,);

    let sr1b = &arr[..n];
    let sr2b = &arr[n..];
    println!("sr1b: {:?}", sr1b,);
    println!("sr2b: {:?}", sr2b,);

    let range = ..;
    let sr0 = &arr[range];
    println!("sr0: {:?}", sr0,);
}
```
