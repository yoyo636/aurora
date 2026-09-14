#include <iostream>
using namespace std;
int fib(int n) { if (n < 2) return n; return fib(n-1) + fib(n-2); }
int main() { cout << fib(35) << endl; return 0; }
