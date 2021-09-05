# Learning Rust
- The Rust Programming Language: https://doc.rust-lang.org/book/title-page.html
- Online playground: https://play.rust-lang.org/

## Variables: const, immutable, mutable, shadow, type casting
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
## Data types
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
