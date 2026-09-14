#include <iostream>
using namespace std;
long long sum_tail(int n, long long acc) { if (n == 0) return acc; return sum_tail(n-1, acc+n); }
int main() { cout << sum_tail(1000000, 0) << endl; return 0; }
