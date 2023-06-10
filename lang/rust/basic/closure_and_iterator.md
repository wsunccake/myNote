# closure and iterator

## closure

```rust
fn  plus_one_v1   (x: i32) -> i32 { x + 1 }
let plus_one_v2 = |x: i32| -> i32 { x + 1 };
let plus_one_v3 = |x: i32|          x + 1  ;

assert_eq!(2, plus_one_v1(1));
assert_eq!(2, plus_one_v2(1));
assert_eq!(2, plus_one_v3(1));
```

```rust
let mut num = 5;
let plus_num = |x: i32| x + num;
let y = &mut num;
```

fix ->

```rust
let mut num = 5;
{
    let plus_num = |x: i32| x + num;
}
let y = &mut num;
```

## generic and trait

```rust
struct Cacher<T>
where
    T: Fn(u32) -> u32,
{
    calculation: T,
    value: Option<u32>,
}

impl<T> Cacher<T>
where
    T: Fn(u32) -> u32,
{
    fn new(calculation: T) -> Cacher<T> {
        Cacher {
            calculation,
            value: None,
        }
    }

    fn value(&mut self, arg: u32) -> u32 {
        match self.value {
            Some(v) => v,
            None => {
                let v = (self.calculation)(arg);
                self.value = Some(v);
                v
            }
        }
    }
}
```
