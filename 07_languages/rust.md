# Learning Rust
- The Rust Programming Language: https://doc.rust-lang.org/book/title-page.html
- Online playground: https://play.rust-lang.org/

## Variables: const, immutable, mutable, shadow
Example:
```rust
fn main() {
    const SECS_PER_DAY: u32 = 86_400;
    println!("The value of SECS_PER_DAY is: {}", SECS_PER_DAY);
    // const SECS_PER_DAY: u32 = 86_401; // error: redefined
    
    let immutable_x: u32 = 5;
    println!("The value of immutable_x is: {}", immutable_x);
    // immutable_x = 6; // error: cannot alter immutable variable x
    let immutable_x: u32 = 6;
    println!("The value of shadowed immutable_x is: {}", immutable_x);
    
    let mut mutable_x = immutable_x;
    println!("The value of mutable_x is: {}", mutable_x);
    mutable_x = mutable_x * SECS_PER_DAY;
    println!("The value of mutable_x is: {}", mutable_x);
}
```
Result:
```
The value of SECS_PER_DAY is: 86400
The value of immutable_x is: 5
The value of shadowed immutable_x is: 6
The value of mutable_x is: 6
The value of mutable_x is: 518400
```
