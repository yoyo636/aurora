//! Rust 数学库 — 通过 C ABI 导出给 Aurora(FFI)
//! 构建:cd rust_math && cargo build --release
//! 产物:target/release/librust_math.dylib

use std::ffi::{CStr, CString};
use std::os::raw::c_char;

/// 整数加法:add(a, b)
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}

/// 整数乘法:mul(a, b)
#[no_mangle]
pub extern "C" fn mul(a: i32, b: i32) -> i32 {
    a * b
}

/// 判断偶数:is_even(n) -> 1/0
#[no_mangle]
pub extern "C" fn is_even(n: i32) -> i32 {
    if n % 2 == 0 { 1 } else { 0 }
}

/// 斐波那契:fib(n)
#[no_mangle]
pub extern "C" fn fib(n: i32) -> i32 {
    if n <= 1 {
        n
    } else {
        fib(n - 1) + fib(n - 2)
    }
}

/// 字符串翻转:reverse(s) 返回 C 字符串(调用方需释放?这里返回静态分配简化)
#[no_mangle]
pub extern "C" fn reverse(s: *const c_char) -> *mut c_char {
    if s.is_null() {
        return std::ptr::null_mut();
    }
    let input = unsafe { CStr::from_ptr(s) }.to_string_lossy().to_string();
    let rev: String = input.chars().rev().collect();
    // 简化实现:返回栈上 CString(生命周期仅到函数结束)——为演示,用 Box 泄漏一次
    let c = CString::new(rev).unwrap_or_default();
    let leaked = Box::leak(c.into_bytes_with_nul().into_boxed_slice());
    leaked.as_mut_ptr() as *mut c_char
}
