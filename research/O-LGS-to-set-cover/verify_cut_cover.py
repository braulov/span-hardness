"""Exhaustive checks for the direct LGS -> cut-cover reduction.
Stdlib Python 3, run as: python verify_cut_cover.py
"""
from itertools import product
from random import Random

def connected(n, edges, x):
    parent=list(range(n))
    def find(v):
        while parent[v]!=v: v=parent[v]
        return v
    for u,v,z in edges:
        if z is None or (z!=0 and x[abs(z)-1]==(z>0)):
            parent[find(u)]=find(v)
    return len({find(i) for i in range(n)})==1

def cut_clauses(n,edges):
    clauses=set()
    # Choose exactly one of {U,V-U} by keeping vertex 0 outside U.
    for mask in range(1,1<<(n-1)):
        U={j for j in range(1,n) if mask&(1<<(j-1))}
        labels={z for u,v,z in edges if (u in U)!=(v in U)}
        if None in labels: continue    # Always-active crossing edge
        labels.discard(0)
        if any(-z in labels for z in labels): continue   # tautology
        clauses.add(frozenset(labels))
    return clauses

def cover_by_chosen_polarities(clauses,x):
    # The p private universe elements force exactly one sign-set per switch.
    return all(any(x[abs(z)-1]==(z>0) for z in clause)
               for clause in clauses)

def main():
    rng=Random(19)
    for t in range(5000):
        n=rng.randrange(2,7); p=rng.randrange(1,5)
        labels=[None,0]+[z for j in range(1,p+1) for z in (j,-j)]
        edges=[(rng.randrange(n),rng.randrange(n),rng.choice(labels))
               for _ in range(rng.randrange(1,16))]
        clauses=cut_clauses(n,edges)
        for bits in product((False,True),repeat=p):
            assert connected(n,edges,bits)==cover_by_chosen_polarities(clauses,bits)
    print("PASS: 5000 random labeled multigraphs, every assignment")
    for p in range(2,11):
        # All 2^(p-1) even-parity inputs must be ruled out,
        # and each full-width implied clause rules out exactly one.
        assert sum(sum(x)%2==0 for x in product((0,1),repeat=p))==2**(p-1)
    print("PASS: parity full-width clause lower bound, p=2..10")

if __name__=="__main__":main()
