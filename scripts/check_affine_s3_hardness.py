#!/usr/bin/env python3
"""Checks S3 nested-commutator #2SAT reduction and F5 Fourier example.

Standard library only. Trial loop enumerates ORIGINAL variables and legal
ternary selectors, rather than exponential inconsistent occurrence copies.
"""
from itertools import product
from random import Random

ID=(0,1,2)
A=(1,0,2)
B=(0,2,1)
C=A

def mul(g,h):
    return tuple(g[h[i]] for i in range(3))

def inv(g):
    out=[None]*3
    for i,j in enumerate(g):
        out[j]=i
    return tuple(out)

def comm(g,h):
    return mul(mul(mul(g,h),inv(g)),inv(h))

R=comm(A,B)

def nested(a,b,c,inverse=False):
    g=comm(comm(A if a else ID,B if b else ID),C if c else ID)
    return inv(g) if inverse else g

def reduction_trial(clauses,n):
    count=0
    satcount=0
    valid_codes=((0,0),(1,0),(0,1))
    for x in product((0,1),repeat=n):
        false_pairs=[(int(x[i]==sg),int(x[j]==tg))
                     for ((i,sg),(j,tg)) in clauses]
        satcount+=not any(a and b for a,b in false_pairs)
        for ys in product(valid_codes,repeat=len(clauses)):
            g=ID
            for (a,b),(u,v) in zip(false_pairs,ys):
                g=mul(nested(a,b,u),g)
                g=mul(nested(a,b,v,inverse=True),g)
            count+=g==ID
    m=len(clauses)
    assert count==3**(m-1)*(2**n+2*satcount),(n,m,count,satcount)

def walsh_support(vals,field):
    vals=list(vals)
    n=len(vals)
    span=1
    while span<n:
        for base in range(0,n,2*span):
            for j in range(base,base+span):
                a,b=vals[j],vals[j+span]
                vals[j]=(a+b)%field
                vals[j+span]=(a-b)%field
        span*=2
    return sum(v!=0 for v in vals)

def main():
    r2=mul(R,R)
    for a,b,c in product((0,1),repeat=3):
        assert nested(a,b,c)==(r2 if a*b*c else ID)
    rng=Random(20261030)
    for _ in range(300):
        n,m=rng.randint(2,5),rng.randint(1,5)
        clauses=[((rng.randrange(n),rng.randrange(2)),
                  (rng.randrange(n),rng.randrange(2))) for _ in range(m)]
        reduction_trial(clauses,n)
    for k in (3,5,7,9,11):
        vals=[int(mask.bit_count()%4==0) for mask in range(1<<k)]
        assert walsh_support(vals,5)==1<<k
    print('PASS: 8 S3 commutator cases, 300 #2SAT reductions,',
          '5 full F5 Fourier-support tests')

if __name__=='__main__':main()
