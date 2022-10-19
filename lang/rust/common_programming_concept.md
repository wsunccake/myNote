# variable and mutability

```rust
fn main() {
    let x = 5;      // immutable variable
    println!("The value of x is: {x}");
    x = 6;
    println!("The value of x is: {x}");
}
```

->

```rust
fn main() {
    let mut x = 5;
    println!("The value of x is: {x}");
    x = 6;
    println!("The value of x is: {x}");
}
```


## constant

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```


## shadowing

```rust
fn main() {
    let x = 5;

    let x = x + 1;

    {
        let x = x * 2;
        println!("The value of x in the inner scope is: {x}");
    }

    println!("The value of x is: {x}");
}
```

```rust
// shadow
let spaces = "   ";
let spaces = spaces.len();

// vs

// immutabile
let mut spaces = "   ";
spaces = spaces.len();
```


---

# data type

## scalar type

```
Length      Signed      Unsigned
8-bit       i8          u8
16-bit      i16         u16
32-bit      i32         u32
64-bit      i64         u64
128-bit     i128        u128
arch	    isize       usize
```

```
Number literals         Example
Decimal	                98_222
Hex	                    0xff
Octal	                0o77
Binary	                0b1111_0000
Byte (u8 only)	        b'A'
```

```rust
// integer type
let guess: u32 = "42".parse().expect("Not a number!");


// floating-point type
let x = 2.0; // f64
let y: f32 = 3.0; // f32


// numeric operation
// addition
let sum = 5 + 10;

// subtraction
let difference = 95.5 - 4.3;

// multiplication
let product = 4 * 30;

// division
let quotient = 56.7 / 32.2;
let floored = 2 / 3; // Results in 0

// remainder
let remainder = 43 % 5;


// boolean type
let t = true;
let f: bool = false; // with explicit type annotation


// character type
let c = 'z';
let z: char = 'ℤ'; // with explicit type annotation
let heart_eyed_cat = '😻';
```


## compound type

### tuple type

```rust
let tup: (i32, f64, u8) = (500, 6.4, 1);
let (x, y, z) = tup;
let five_hundred = tup.0;
let six_point_four = tup.1;
let one = tup.2;
```

### array type

```rust
let a = [1, 2, 3, 4, 5];
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
let a: [i32; 5] = [1, 2, 3, 4, 5];
let a = [3; 5];     // a = [3, 3, 3, 3, 3];


// accessing array element
let a = [1, 2, 3, 4, 5];
let first = a[0];
let second = a[1];
```


```rust
// invalid array element access
use std::io;

fn main() {
    let a = [1, 2, 3, 4, 5];

    println!("Please enter an array index.");

    let mut index = String::new();

    io::stdin()
        .read_line(&mut index)
        .expect("Failed to read line");

    let index: usize = index
        .trim()
        .parse()
        .expect("Index entered was not a number");

    let element = a[index];

    println!("The value of the element at index {index} is: {element}");
}
```

```rust
fn type_of<T>(_: T) -> &'static str {
    std::any::type_name::<T>()
}

fn main() {
    let x = 21;
    let y = 2.5;
    println!("{}", type_of(123));
    println!("{}", type_of(x));
    println!("{}", type_of(&x));
    println!("{}", type_of(y));

    let s1 = "ABC";
    let s2 = String::from("ABC");
    println!("{}", type_of("abc"));
    println!("{}", type_of(s1));
    println!("{}", type_of(String::from("abc")));
    println!("{}", type_of(s2));

    println!("{}", type_of(vec![1, 2, 3]));
    println!("{}", type_of(main));
}
```

---

# function

```rust
fn main() {
    println!("Hello, world!");
    another_function();
}

fn another_function() {
    println!("Another function.");
}
```


## parameter

```rust
fn main() {
    another_function(5);
}

fn another_function(x: i32) {
    println!("The value of x is: {x}");
    print_labeled_measurement(5, 'h');
}

fn print_labeled_measurement(value: i32, unit_label: char) {
    println!("The measurement is: {value}{unit_label}");
}
```


## statement and expression

```rust
// statement
let y = 6;
let x = (let y = 6);    // error


// expression
let y = {
    let x = 3;
    x + 1
};
```


## function with return value

```rust
fn five() -> i32 {
    5
}

fn main() {
    let x = five();
    println!("The value of x is: {x}");
}
```


---

# comment

```rust
// So we’re doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew! Hopefully, this comment will
// explain what’s going on.

fn main() {
    let lucky_number = 7; // I’m feeling lucky today
}
```


---

# control flow

## if expression

```rust
let number = 3;
if number < 5 {
    println!("condition was true");
} else {
    println!("condition was false");
}

// handling multiple condition with else if
let number = 6;
if number % 4 == 0 {
    println!("number is divisible by 4");
} else if number % 3 == 0 {
    println!("number is divisible by 3");
} else if number % 2 == 0 {
    println!("number is divisible by 2");
} else {
    println!("number is not divisible by 4, 3, or 2");
}


// using if in a let statement
let condition = true;
let number = if condition { 5 } else { 6 };
println!("The value of number is: {number}");
```


## repetition with loop

```rust
// repeating code with loop
loop { println!("again!"); }


// returning value from loop
let mut counter = 0;
let result = loop {
    counter += 1;
    if counter == 10 {
        break counter * 2;
    }
};
println!("The result is {result}");


// loop label to disambiguate between multiple loop
let mut count = 0;
'counting_up: loop {
    println!("count = {count}");
    let mut remaining = 10;
    loop {
        println!("remaining = {remaining}");
        if remaining == 9 {
            break;
        }
        if count == 2 {
            break 'counting_up;
        }
        remaining -= 1;
    }
    count += 1;
}
println!("End count = {count}");


// conditional loop with while
let mut number = 3;
while number != 0 {
    println!("{number}!");
    number -= 1;
}
println!("LIFTOFF!!!");


// looping through a collection with for
let a = [10, 20, 30, 40, 50];
let mut index = 0;
while index < 5 {
    println!("the value is: {}", a[index]);
    index += 1;
}

// -->
let a = [10, 20, 30, 40, 50];
for element in a {
    println!("the value is: {element}");
}


for number in (1..4).rev() {
    println!("{number}!");
}
println!("LIFTOFF!!!");
```
