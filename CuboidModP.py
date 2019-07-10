import itertools as it
from sympy import sieve

N = 20

def gen_quad_residues(p):
    if p == 2:
        return range(2)
    else:
        res = []
        for i in range(0, (p+1) // 2):
            res.append( i * i % p)
        return res

def get_pos_trios(p):
    def get_nontrivial_negations(sol):
        def get_negs(ind):
            if sol[ind] == 0:
                return [sol[ind]]
            else: 
                return [sol[ind], p - sol[ind]]
        nontrivial_negs = []
        a_vals = get_negs(0)
        b_vals = get_negs(1)
        c_vals = get_negs(2)
        for a in a_vals:
            for b in b_vals:
                for c in c_vals:
                    nontrivial_negs.append([a, b, c])
        return nontrivial_negs                    
    res = gen_quad_residues(p)
    sols = []
    for triple in it.combinations_with_replacement(range(0, (p+1)//2), 3):
        a = triple[0] * triple[0] % p
        b = triple[1] * triple[1] % p
        c = triple[2] * triple[2] % p
        if (a+b) % p in res and (b+c) % p in res and (a+c) % p in res and (a + b + c) % p in res:
            new_sols = get_nontrivial_negations([triple[0], triple[1], triple[2]])
            for solution in new_sols:
                if not solution in sols:
                    sols.append(solution)
    return sols
            
primes = list(sieve.primerange(3, N))


for prime in primes:
    print("Values for " + str(prime) + ": \n")
    for sol in get_pos_trios(prime):
        print(sol)
