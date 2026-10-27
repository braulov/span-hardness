"""Exhaustive small-case validation for branch M. Python 3 stdlib."""
from collections import Counter
from itertools import product
from random import Random

def partitions(n):
    def rec(a,top):
        if len(a)==n:
            yield tuple(a)
        else:
            for k in range(top+2):
                yield from rec(a+[k],max(top,k))
    return rec([0],0)

def classify(edges):
    counts={}
    for u,v,z in edges:
        if z not in (0,None):
            counts.setdefault(abs(z),Counter())[z>0]+=1
    light={i for i,c in counts.items() if c[True]==c[False]==1}
    mono={i for i,c in counts.items() if not c[True] or not c[False]}
    heavy=sorted(set(counts)-light-mono)
    return light,mono,heavy

def available(edges,partial):
    light,mono,heavy=classify(edges)
    out=[]
    for j,(u,v,z) in enumerate(edges):
        if z==0:continue
        if z is None:color=('always',j)
        elif abs(z) in mono:color=('monopolar',j)
        elif abs(z) in light:color=('light',abs(z))
        else:
            if abs(z) in partial and partial[abs(z)]!=(z>0):continue
            color=('heavy',j)
        out.append((u,v,color))
    return out

def criterion(n,edges):
    for part in partitions(n):
        colors={color for u,v,color in edges if part[u]!=part[v]}
        if len(colors)<len(set(part))-1:return False
    return True

def rainbow_tree(n,edges):
    def search(i,parent,used,k):
        if k==n-1:return True
        if i==len(edges) or k+len(edges)-i<n-1:return False
        u,v,c=edges[i]
        def rt(a):
            while parent[a]!=a:a=parent[a]
            return a
        a,b=rt(u),rt(v)
        if a!=b and c not in used:
            nxt=parent[:];nxt[a]=b
            if search(i+1,nxt,used|{c},k+1):return True
        return search(i+1,parent,used,k)
    return search(0,list(range(n)),set(),0)

def direct_lgs(n,edges,heavy_assignment):
    light,mono,heavy=classify(edges)
    for light_bits in product([False,True],repeat=len(light)):
        a={**heavy_assignment,**dict(zip(sorted(light),light_bits))}
        parent=list(range(n))
        def rt(v):
            while parent[v]!=v:v=parent[v]
            return v
        for u,v,z in edges:
            active=z is None or (z!=0 and (abs(z) in mono or a[abs(z)]==(z>0)))
            if active:parent[rt(u)]=rt(v)
        if len({rt(v) for v in range(n)})==1:return True
    return False

def test():
    rng=Random(2281);total=0;fully_checked=0
    for rep in range(350):
        n=rng.randrange(2,6);p=rng.randrange(1,5);m=rng.randrange(2,11)
        labels=[None,0]+[z for i in range(1,p+1) for z in (i,-i)]
        edges=[(rng.randrange(n),rng.randrange(n),rng.choice(labels)) for _ in range(m)]
        _,_,heavy=classify(edges)
        for values in product((None,False,True),repeat=len(heavy)):
            alpha={i:v for i,v in zip(heavy,values) if v is not None}
            graph=available(edges,alpha)
            assert criterion(n,graph)==rainbow_tree(n,graph),(rep,alpha,edges)
            if len(alpha)==len(heavy):
                assert criterion(n,graph)==direct_lgs(n,edges,alpha),(rep,alpha,edges)
                fully_checked+=1
            total+=1
    clauses=[[1,2],[1,-2],[-1,2],[-1,-2]]
    path=[(j,j+1,z) for j,clause in enumerate(clauses) for z in clause]
    assert not any(direct_lgs(5,path,{1:x,2:y}) for x,y in product((False,True),repeat=2))
    for part in partitions(5):
        assert sum(0.5 for u,v,z in path if part[u]!=part[v])>=len(set(part))-1
    print('PASS',total,'partial instances;',fully_checked,'full instances; 52 LP gap partitions')

if __name__=='__main__':test()
