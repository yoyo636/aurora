
import sys
sys.setrecursionlimit(2000000)
def sum_tail(n, acc):
    if n == 0: return acc
    return sum_tail(n-1, acc+n)
try:
    print(sum_tail(1000000, 0))
except RecursionError:
    print("OVERFLOW")
