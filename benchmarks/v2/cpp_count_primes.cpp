#include <iostream>
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
int main() { cout << count_primes(100000) << endl; return 0; }
