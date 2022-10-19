# what is ownership

## ownership rule

Each value in Rust has an owner

There can only be one owner at a time

When the owner goes out of scope, the value will be dropped


## variable scope

```rust
{                      // s is not valid here, it’s not yet declared
    let s = "hello";   // s is valid from this point forward
    // do stuff with s
}                      // this scope is now over, and s is no longer valid
```


## the String Type

```rust
let mut s = String::from("hello");
s.push_str(", world!"); // push_str() appends a literal to a String
println!("{}", s); // This will print `hello, world!`
```


## memory and allocation

```rust
{
    let s = String::from("hello"); // s is valid from this point forward
    // do stuff with s
}                                  // this scope is now over, and s is no longer valid
```


## ways variable and data interact: move

```rust
let s1 = String::from("hello");
let s2 = s1;
// println!("{}, world!", s1);
println!("{}, world!", s2);

let ss1 = "hello";
let ss2 = ss1;
println!("{}, world!", ss1);
println!("{}, world!", ss2);
```


## way variable and data interact: clone

```rust
let s1 = String::from("hello");
let s2 = s1.clone();
println!("{}, world!", s1);
println!("{}, world!", s2);


// stack-only data: copy
let i1 = 1;
let i2 = i1;
println!("i1 = {}", i1);
println!("i2 = {}", i2);
```

