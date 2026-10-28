"""Verify explicit block-local BP -> Set Cover gadgets.
Python 3 stdlib. Compares exhaustive BP-SAT with exact-group cover choices.
"""
from itertools import product,combinations
from math import comb
from random import Random

def antichain(w):
    q=1
    while comb(q,q//2)<w:q+=1
    return q,[set(z) for z in combinations(range(q),q//2)][:w]

def accepts(layers,start,final,bits):
    s=start
    for layer in layers:
        i,a,b=layer[s];s=(a,b)[bits[i]]
    return s in final

def compile_cover(layers,p,w,cuts,start,final):
    B=len(cuts)-1
    support=[sorted({t[0] for layer in layers[cuts[j]:cuts[j+1]] for t in layer})
             for j in range(B)]
    q,codes=antichain(w)
    incidence={i:[j for j,s in enumerate(support) if i in s] for i in range(p)}
    arcs={}
    universe=[('privx',i) for i in range(p)]+[('privb',j) for j in range(B)]
    for i,js in incidence.items():
        if not js:continue
        nodes=[('x',i)]+[('b',j) for j in js]
        for k,a in enumerate(nodes):
            e=('arc',i,k)
            arcs[e]=(a,nodes[(k+1)%len(nodes)])
            universe.append(e)
    universe += [('state',j,k) for j in range(B-1) for k in range(q)]
    idx={e:i for i,e in enumerate(universe)}
    def make(node,values,extra):
        chosen=set(extra)
        for e,(a,b) in arcs.items():
            if node==a and values[e[1]]==0:chosen.add(e)
            if node==b and values[e[1]]==1:chosen.add(e)
        return sum(1<<idx[e] for e in chosen)
    groups=[]
    for i in range(p):
        groups.append([make(('x',i),{i:v},[('privx',i)]) for v in (0,1)])
    for j,supp in enumerate(support):
        opts=[]
        for assignment in product((0,1),repeat=len(supp)):
            values=dict(zip(supp,assignment))
            for s in range(w):
                if j==0 and s!=start:continue
                t=s
                for layer in layers[cuts[j]:cuts[j+1]]:
                    i,a,b=layer[t];t=(a,b)[values[i]]
                if j==B-1 and t not in final:continue
                extra=[('privb',j)]
                if j>0:extra += [('state',j-1,k) for k in codes[s]]
                if j<B-1:extra += [('state',j,k) for k in set(range(q))-codes[t]]
                opts.append(make(('b',j),values,extra))
        groups.append(opts)
    h=sum(map(len,support));used=sum(bool(js) for js in incidence.values())
    assert len(universe)==p+B+h+used+q*(B-1)
    return universe,groups

def coverable(universe,groups):
    goal=(1<<len(universe))-1
    def rec(i,mask):
        if i==len(groups):return mask==goal
        return any(rec(i+1,mask|s) for s in groups[i])
    return rec(0,0)

def test():
    rng=Random(2886)
    for trial in range(650):
        p=rng.randint(1,3);w=rng.randint(2,5);L=rng.randint(1,6)
        layers=[[(rng.randrange(p),rng.randrange(w),rng.randrange(w))
                 for _ in range(w)] for _ in range(L)]
        start=rng.randrange(w)
        final={s for s in range(w) if rng.randrange(2)}
        cuts=sorted({0,L}|set(rng.sample(range(1,L),rng.randrange(L)))) if L>1 else [0,1]
        univ,groups=compile_cover(layers,p,w,cuts,start,final)
        yes=any(accepts(layers,start,final,x) for x in product((0,1),repeat=p))
        assert yes==coverable(univ,groups),(trial,p,w,L,cuts)
    for w in range(2,22):
        q,codes=antichain(w)
        for i in range(w):
            for j in range(w):
                cov=(set(range(q))-codes[i])|codes[j]
                assert (len(cov)==q)==(i==j)
    print('PASS: 650 random BP instances, antichain equality w=2..21')

if __name__=='__main__':test()
