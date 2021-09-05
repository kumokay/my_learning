# Learning Rust
- The Rust Programming Language: https://doc.rust-lang.org/book/title-page.html
- Online playground: https://play.rust-lang.org/

## Common Programming Concepts
### Variables: const, immutable, mutable, shadow, type casting
Example:
```rust
fn main() {
    const SECS_PER_DAY: u32 = 86_400;
    println!("The value of SECS_PER_DAY is: {}", SECS_PER_DAY);
    // const SECS_PER_DAY: u32 = 86_401; // error: redefined
    
    let immutable_x: u32 = 5;
    println!("The value of immutable_x is: {}", immutable_x);
    // immutable_x = 6; // error: cannot alter immutable variable x
    let immutable_x: u16 = 6;
    println!("The value of shadowed immutable_x is: {}", immutable_x);
    
    let mut mutable_x: u64 = std::convert::Into::<u64>::into(immutable_x);
    println!("The value of mutable_x is: {}", mutable_x);
    mutable_x = mutable_x * (SECS_PER_DAY as u64);
    println!("The value of mutable_x is: {}", mutable_x);
}
```
Output:
```
The value of SECS_PER_DAY is: 86400
The value of immutable_x is: 5
The value of shadowed immutable_x is: 6
The value of mutable_x is: 6
The value of mutable_x is: 518400
```
### Primitive data types
- Scalar types
  - Integers: 
    - i8, i16, i32, i64, i128, isize
    - u8, u16, u32, u64, u128, usize
  - Floats: f32 and f64
  - Boolean: bool
  - Characters: char
- Compound types: tuples and arrays

Example:
```rust
fn main() {
    // Scalar types
    let mut integer: i32 = 5 + 10;
    println!("The value of integer is: {}", integer);

    let mut float: f64 = 95.5 - 4.3;
    println!("The value of float is: {}", float);
    
    let mut unsigned: u8 = 15 % 2;
    println!("The value of unsigned is: {}", unsigned);
    
    let boolean: bool = false;
    println!("The value of boolean is: {}", boolean);
    
    let char_a: char = 'a';
    let char_b: char = std::char::from_u32(98).unwrap();
    println!("Two characters: {}, {}", char_a, char_b);
    
    // Compound types: tuples and arrays
    const LEN: usize = 5;
    let array : [i32; LEN]= [1, 2, 3, 4, 5];
    println!("The values in the array: {:?}", array);
    println!("First and second: {}, {}", array[0], array[1]);
    
    let tuple: (i32, f64, u8, [i32; LEN]) = (500, 6.4, 1, array);
    println!("The value of tuple is: {:?}", tuple);
    integer = tuple.0 * 2;
    float = tuple.1 * 2.0;
    unsigned = tuple.2 * 2;
    println!("integer, float, unsigned: {}, {}, {}", integer, float, unsigned);
    let (integer, float, unsigned, array) = tuple;
    println!("Print everything: {:#?}", (integer, float, unsigned, array));
}
```
Output:
```
The value of integer is: 15
The value of float is: 91.2
The value of unsigned is: 1
The value of boolean is: false
Two characters: a, b
The values in the array: [1, 2, 3, 4, 5]
First and second: 1, 2
The value of tuple is: (500, 6.4, 1, [1, 2, 3, 4, 5])
integer, float, unsigned: 1000, 12.8, 2
Print everything: (
    500,
    6.4,
    1,
    [
        1,
        2,
        3,
        4,
        5,
    ],
)
```
### Functions
Example:
```rust
fn add(lhs: i32, rhs: i32) -> i32 { 
    lhs + rhs // without a semicolon at the end will return the value
}

fn print(name: &str, value: i32) { 
    println!("The value of {} is: {}", name, value);
    // with a semicolon at the end will return nothing
}

fn main() {
    fn increment(x: i32) -> i32 { x + 1 }

    let y = {
      let x: i32 = 100;
      add(increment(x), 5)
    };
    print("x", y);
}
```
Output:
```
The value of x is: 106
```
### Control Flow
Example:
```rust
fn demo_if(number: u32) {
    if number % 4 == 0 {
        println!("{} is divisible by 4", number);
    } else if number % 3 == 0 {
        println!("{} is divisible by 3", number);
    } else if number % 2 == 0 {
        println!("{} is divisible by 2", number);
    } else {
        println!("{} is not divisible by 4, 3, or 2", number);
    }
}

fn demo_while(number: u32) {
    let array: [u32; 3] = [4, 3, 2];
    let mut idx = 0;
    while idx != array.len() {
        if number % array[idx] == 0 {
            println!("{} is divisible by {}", number, array[idx]);
            break;
        }
        idx = idx + 1;
    }
    if idx == array.len() {
        println!("{} is not divisible by 4, 3, or 2", number);
    }
}

fn demo_loop(number: u32) {
    let array: [u32; 3] = [4, 3, 2];
    let mut idx = 0;
    let is_divisible = loop {
        if idx == array.len() {
            break false;
        } else if number % array[idx] == 0 {
            break true;
        } else {
            idx = idx + 1;
        }
    };
    if is_divisible { 
        println!("{} is divisible by {}", number, array[idx]);
    } else {
        println!("{} is not divisible by 4, 3, or 2", number);
    }
}

fn demo_for_range(number: u32) {
    let array: [u32; 3] = [4, 3, 2];
    let mut is_divisible: bool = false;
    for idx in 0..array.len() {
        if number % array[idx] == 0 {
            println!("{} is divisible by {}", number, array[idx]);
            is_divisible = true;
            break;
        }
    }
    if !is_divisible { 
        println!("{} is not divisible by 4, 3, or 2", number);
    }
}

fn demo_for_iter(number: u32) {
    let array: [u32; 3] = [4, 3, 2];
    let mut is_divisible: bool = false;
    for x in array.iter() {
        if number % x == 0 {
            println!("{} is divisible by {}", number, x);
            is_divisible = true;
            break;
        }
    }
    if !is_divisible { 
        println!("{} is not divisible by 4, 3, or 2", number);
    }
}

fn demo_match(number: u32) {
    match (number % 4, number % 3, number % 2) {
        (0, ..) => println!("{} is divisible by 4", number),
        (_, 0, _) => println!("{} is divisible by 3", number),
        (.., 0) => println!("{} is divisible by 2", number),
        _ => println!("{} is not divisible by 4, 3, or 2", number),
    }
}

fn main() {
    demo_if(15);
    demo_while(16);
    demo_loop(17);
    demo_for_range(18);
    demo_for_iter(19);
    demo_match(20);
}
```
Output:
```
15 is divisible by 3
16 is divisible by 4
17 is not divisible by 4, 3, or 2
18 is divisible by 3
19 is not divisible by 4, 3, or 2
20 is divisible by 4
```
