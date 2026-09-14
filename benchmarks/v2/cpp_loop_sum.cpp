#include <iostream>
using namespace std;
long long loop_sum(int n) { long long s = 0; for (int i = 0; i < n; i++) s += i; return s; }
int main() { cout << loop_sum(10000000) << endl; return 0; }
