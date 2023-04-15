# condition

## if

```rust
fn main() {
    let condition = true;
    let number = if condition { 5 } else { 3 }; // if in let

    if number < 5 {
        println!("condition was true");
    } else {
        println!("condition was false");
    }

    // if number { // error
    if number != 0 {
        println!("number was three");
    }

    if number % 4 == 0 {
        println!("number is divisible by 4");
    } else if number % 3 == 0 {
        println!("number is divisible by 3");
    } else if number % 2 == 0 {
        println!("number is divisible by 2");
    } else {
        println!("number is not divisible by 4, 3, or 2");
    }
}
```

---

## loop

```rust
fn main() {
    let mut counter = 0;

    let result = loop {
        counter += 1;
        println!("loop {}", counter);

        if counter == 10 {
            break counter * 2;
        }
    };

    println!("current loop {}", counter);
    println!("The result is {result}");
}
```

```rust
fn main() {
    let mut count = 0;

    // loop label
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
}
```

---

## while

```rust
fn main() {
    let mut number = 3;

    while number != 0 {
        println!("{number}!");
        number -= 1;
    }

    println!("LIFTOFF!!!");
}
```

---

## for

```rust
fn main() {
    // array
    let a = [10, 20, 30, 40, 50];
    let mut index = 0;

    while index < 5 {
        println!("the value is: {}", a[index]);
        index += 1;
    }

    // array
    for element in a {
        println!("the value is: {element}");
    }

    // value
    for number in (1..4).rev() {
        println!("{number}!");
    }
    println!("LIFTOFF!!!");
}
```
