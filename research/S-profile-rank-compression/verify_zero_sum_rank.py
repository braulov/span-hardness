"""Finite-field zero-sum support and F2 basis sparsification checks."""
from itertools import product
from random import Random

def rank(rows,q):
    piv={}
    for row in rows:
        v=list(row)
        for j in sorted(piv):
            if v[j]:
                c=v[j]
                v=[(a-c*b)%q for a,b in zip(v,piv[j])]
        if any(v):
            j=next(i for i,x in enumerate(v) if x)
            f=pow(v[j],-1,q)
            piv[j]=[(x*f)%q for x in v]
    return len(piv)

def support(vals,q):
    k=len(vals[0])
    zero=(0,)*k
    reachable={zero:0}
    for v in vals:
        new=reachable.copy()
        for z,weight in reachable.items():
            w=tuple((a+b)%q for a,b in zip(z,v))
            new[w]=min(new.get(w,10**9),weight+1)
        reachable=new
    return reachable

def test():
    rng=Random(6607)
    for q in (2,3,5):
        for k in range(1,5):
            for case in range(160):
                p=rng.randrange(k,min(k+7,12))
                cols=[tuple(rng.randrange(q) for _ in range(k)) for _ in range(p)]
                rr=rank(cols,q)
                reached=support(cols,q)
                assert all(minweight<=(q-1)*rr for minweight in reached.values())
                if q==2:
                    basis=[]
                    for v in cols:
                        if rank(basis+[v],q)>len(basis):basis.append(v)
                    assert set(reached)==set(support(basis,q))
                    assert len(reached)==2**rr
                    # Every reachable signature has the same # of input preimages.
                    exact={(0,)*k:1}
                    for v in cols:
                        nxt=exact.copy()
                        for z,c in exact.items():
                            w=tuple((a+b)%q for a,b in zip(z,v))
                            nxt[w]=nxt.get(w,0)+c
                        exact=nxt
                    assert set(exact.values())=={2**(p-rr)}
        print("PASS: prime",q,", sparse support and linear rank")
if __name__=="__main__":test()
