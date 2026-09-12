// C++ 数学库 — 通过 extern "C" 导出给 Aurora(FFI)
// 构建:clang++ -shared -fPIC -O2 cpp_math.cpp -o libcpp_math.dylib

#include <cstdint>

extern "C" {

/// 整数减法:sub(a, b)
int32_t sub(int32_t a, int32_t b) {
    return a - b;
}

/// 整数除法(截断):div(a, b)
int32_t div_i(int32_t a, int32_t b) {
    return b == 0 ? 0 : a / b;
}

/// 最大公约数:gcd(a, b)
int32_t gcd(int32_t a, int32_t b) {
    while (b != 0) {
        int32_t t = b;
        b = a % b;
        a = t;
    }
    return a < 0 ? -a : a;
}

/// 次方:ipow(base, exp) — 快速幂
int64_t ipow(int64_t base, int64_t exp) {
    int64_t r = 1;
    while (exp > 0) {
        if (exp & 1) r *= base;
        base *= base;
        exp >>= 1;
    }
    return r;
}

}  // extern "C"
