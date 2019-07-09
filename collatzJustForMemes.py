from sympy import sieve

N = 100

def check(p):
    if p == 2:
        return True
    if p == 3:
        return True
    two_pows = [2]
    exp = 2
    while two_pows[-1] != 1:
        two_pows.append(pow(2, exp, p))
        exp += 1
    three_pows = [3]
    exp = 2
    while three_pows[-1] != 1:
        three_pows.append(pow(3, exp, p))
        exp += 1
    tots = []
    for two_pow in two_pows:
        for three_pow in three_pows:
            prod = two_pow * three_pow % p
            tots.append(prod)
    return set(tots) == set(range(1, p))

primes = list(sieve.primerange(1, N))

for prime in primes:
    if check(prime):
        print(prime)