"""Reproducible U1-U4 checks: hidden-exception exact counting via chain neighborhoods.
Python 3 standard library. Run: python verify_universal_slice_interpolation.py
Brute force is used ONLY in the tests, NOT in the proposed algorithm.
"""
from itertools import combinations, product
from fractions import Fraction
from math import comb
from random import Random

def chain_queries(p, b):
    """Build Q_{p,b} without scanning the 2^p Boolean cube."""
    out = [set() for _ in range(p+1)]
    for t in range(p+1):
        pref = [int(i < t) for i in range(p)]
        for j in range(min(b,p)+1):
            for flipped in combinations(range(p),j):
                x = pref[:]
                for i in flipped:x[i] ^= 1
                out[sum(x)].add(tuple(x))
    return [sorted(q) for q in out]

def exact_gauss(a, y):
    """Gaussian elimination over Q for a square non-singular integer matrix."""
    n = len(y)
    rows = [[Fraction(v) for v in a[i]]+[Fraction(y[i])]
            for i in range(n)]
    for j in range(n):
        pivot=next((r for r in range(j,n) if rows[r][j]),None)
        if pivot is None:raise ValueError("singular slice evaluation matrix")
        rows[j],rows[pivot]=rows[pivot],rows[j]
        factor=rows[j][j]
        rows[j]=[z/factor for z in rows[j]]
        for i in range(n):
            if i==j or not rows[i][j]:continue
            factor=rows[i][j]
            rows[i]=[u-factor*v for u,v in zip(rows[i],rows[j])]
    return [row[-1] for row in rows]

def exact_count(p,b,eval_f,query_sets=None):
    """Exact under the slice-degree<=b PROMISE; unknown exception set."""
    qs = query_sets if query_sets is not None else chain_queries(p,b)
    total = Fraction(0)
    for w in range(p+1):
        d=min(b,w,p-w)
        points=qs[w]
        monomials=list(combinations(range(p),d))
        assert len(points)==len(monomials)==comb(p,d)
        M=[[int(all(x[i] for i in T)) for T in monomials] for x in points]
        coeff=exact_gauss(M,[eval_f(x) for x in points])
        total+=comb(p-d,w-d)*sum(coeff)
    assert total.denominator==1
    return int(total)

def discover_exception_set(p,b,eval_f,qs=None):
    """Promise learner: find SOME B of exactly b exceptional positions."""
    qs = qs if qs is not None else chain_queries(p,b)
    observed={x:eval_f(x) for layer in qs for x in layer}
    for B in combinations(range(p),b):
        rest=tuple(i for i in range(p) if i not in B)
        table={}
        for z in product((0,1),repeat=b):
            for k in range(p-b+1):
                x=[0]*p
                for i,v in zip(B,z):x[i]=v
                for i in rest[:k]:x[i]=1
                table[z,k]=eval_f(tuple(x))
        if all(table[tuple(x[i] for i in B),sum(x[i] for i in rest)]==value
               for x,value in observed.items()):
            return B,table
    raise AssertionError("no promised exception set found")

def cyclic_one_exception_count(p,eval_f):
    total=0
    for w in range(p+1):
        pref=(1,)*w+(0,)*(p-w)
        total+=comb(p,w)*sum(eval_f(pref[t:]+pref[:t]) for t in range(p))
    assert total%p==0
    return total//p

def main():
    rng=Random(20261028)
    for p in range(1,10):
        for b in range(min(3,p)+1):
            qs=chain_queries(p,b)
            assert all(len(qs[w])==comb(p,min(b,w,p-w))
                       for w in range(p+1))
            assert sum(map(len,qs)) <= (p+1)*comb(p,b) if b<=p//2 else True
    print("PASS canonical query cardinalities p=1..9")

    for p in range(1,9):
        for trial in range(12):
            b=rng.randrange(min(3,p)+1)
            hidden=tuple(sorted(rng.sample(range(p),b)))
            table={(z,k):rng.randrange(2)
                   for z in product((0,1),repeat=b)
                   for k in range(p-b+1)}
            def f(x):
                return table[tuple(x[i] for i in hidden),
                             sum(x[i] for i in range(p) if i not in hidden)]
            qs=chain_queries(p,b)
            predicted=exact_count(p,b,f,qs)
            expected=sum(f(x) for x in product((0,1),repeat=p))
            assert predicted==expected,(p,b,hidden,predicted,expected)
            found,g=discover_exception_set(p,b,f,qs)
            rest=tuple(i for i in range(p) if i not in found)
            assert all(g[tuple(x[i] for i in found),sum(x[i] for i in rest)]==f(x)
                       for x in product((0,1),repeat=p))
            if b==1:
                assert cyclic_one_exception_count(p,f)==expected
    print("PASS 96 exact counts, 96 recovered exception sets, brute comparison")

    for p in range(1,10):
        for trial in range(20):
            i=rng.randrange(p)
            val={(bit,k):rng.randrange(2)
                 for bit in (0,1) for k in range(p)}
            def f(x):return val[x[i],sum(x)-x[i]]
            assert cyclic_one_exception_count(p,f)==sum(
                f(x) for x in product((0,1),repeat=p))
    print("PASS 180 cyclic-shift exact-count identities")

if __name__=="__main__":main()
