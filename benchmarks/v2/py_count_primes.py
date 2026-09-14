
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
print(count_primes(100000))
