import sys
sys.setrecursionlimit(2000000)

def count_primes(n):
    count = 0
    for i in range(2, n):
        is_prime = True
        j = 2
        while j * j <= i:
            if i % j == 0:
                is_prime = False
                break
            j += 1
        if is_prime:
            count += 1
    return count

def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

def loop_sum(n):
    s = 0
    for i in range(n):
        s += i
    return s

def sum_tail(n, acc):
    if n == 0:
        return acc
    return sum_tail(n-1, acc+n)

if __name__ == '__main__':
    print(count_primes(100000))
    print(fib(35))
    print(loop_sum(10000000))
    try:
        print(sum_tail(1000000, 0))
    except RecursionError:
        print("OVERFLOW")
