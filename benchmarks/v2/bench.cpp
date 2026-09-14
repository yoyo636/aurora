#include <iostream>
#include <cmath>
using namespace std;

int count_primes(int n) {
    int count = 0;
    for (int i = 2; i < n; i++) {
        bool is_prime = true;
        for (int j = 2; j * j <= i; j++) {
            if (i % j == 0) { is_prime = false; break; }
        }
        if (is_prime) count++;
    }
    return count;
}

int fib(int n) {
    if (n < 2) return n;
    return fib(n-1) + fib(n-2);
}

long long loop_sum(int n) {
    long long sum = 0;
    for (int i = 0; i < n; i++) sum += i;
    return sum;
}

long long sum_tail(int n, long long acc) {
    if (n == 0) return acc;
    return sum_tail(n-1, acc+n);
}

int main() {
    cout << count_primes(100000) << endl;
    cout << fib(35) << endl;
    cout << loop_sum(10000000) << endl;
    cout << sum_tail(1000000, 0) << endl;
    return 0;
}
