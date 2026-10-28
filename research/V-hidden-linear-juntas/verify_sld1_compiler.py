"""Sanity-check for hidden Boolean slice-degree-one -> O(p) weight-indexed circuit.
The generated formulas are known SLD1; this tests reconstruction pointwise.
"""
from itertools import product
from random import Random

def q1(p,w):
    out=set()
    for t in range(p+1):
        x=tuple(int(i<t) for i in range(p))
        if sum(x)==w:out.add(x)
        for i in range(p):
            y=list(x);y[i]^=1
            if sum(y)==w:out.add(tuple(y))
    return out

def reconstruct(p,f):
    reps={}
    for w in range(p+1):
        if w==0 or w==p:
            reps[w]=('constant',f((1,)*w+(0,)*(p-w)))
        elif w in (1,p-1):
            patterns=[]
            for i in range(p):
                x=tuple(int(j==i) if w==1 else int(j!=i)
                        for j in range(p))
                patterns.append(f(x))
            reps[w]=('extreme',tuple(patterns))
        else:
            sample=q1(p,w)
            assert len(sample)==p
            candidates=[('constant',0),('constant',1)]
            candidates += [(sign,i) for i in range(p)
                           for sign in ('positive','negative')]
            def eval_c(c,x):
                sign,i=c
                return i if sign=='constant' else (x[i] if sign=='positive' else 1-x[i])
            reps[w]=next(c for c in candidates
                         if all(eval_c(c,x)==f(x) for x in sample))
    return reps

def eval_rep(reps,x):
    w=sum(x)
    sign,arg=reps[w]
    if sign=='constant':return arg
    if sign=='positive':return x[arg]
    if sign=='negative':return 1-x[arg]
    if w==1:return next(arg[i] for i,z in enumerate(x) if z)
    return next(arg[i] for i,z in enumerate(x) if not z)

def test():
    rng=Random(611)
    for p in range(2,12):
        for trial in range(30):
            spec={}
            for w in range(p+1):
                if 2<=w<=p-2:
                    kind=rng.choice(('constant','positive','negative'))
                    spec[w]=(kind,rng.randrange(2) if kind=='constant' else rng.randrange(p))
                else:spec[w]=('constant',rng.randrange(2))
            edge={}
            for w in (1,p-1):
                for i in range(p):edge[w,i]=rng.randrange(2)
            def f(x):
                w=sum(x)
                if w in (1,p-1):
                    i=next(j for j,v in enumerate(x) if v==(1 if w==1 else 0))
                    return edge[w,i]
                kind,arg=spec[w]
                return arg if kind=='constant' else (x[arg] if kind=='positive' else 1-x[arg])
            rep=reconstruct(p,f)
            for x in product((0,1),repeat=p):
                assert eval_rep(rep,x)==f(x),(p,trial,x)
    print('PASS: 300 random Boolean slice-degree-one functions')

if __name__=='__main__':test()
