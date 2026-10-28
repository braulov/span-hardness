"""Regression tests for Q1/Q2 and the normal-core factorization. Python >=3.10."""
from itertools import product
from random import Random

def mul(a,b): return tuple(a[b[i]] for i in range(len(a)))
def one(w): return tuple(range(w))
def inv(a):
    b=[0]*len(a)
    for i,v in enumerate(a): b[v]=i
    return tuple(b)

def normalize(word,w):
    A=one(w); h=[]
    for i,g0,g1 in word:
        A=mul(A,g0)
        h.append((i,mul(mul(A,mul(inv(g0),g1)),inv(A))))
    return A,h

def evaluate(word,x,w):
    z=one(w)
    for i,g0,g1 in word:z=mul(z,(g0,g1)[x[i]])
    return z

def components(h,p):
    parent=list(range(p))
    def root(i):
        while parent[i]!=i:i=parent[i]
        return i
    for i in range(p):
        for j in range(i):
            if any(mul(a,b)!=mul(b,a) for u,a in h for v,b in h
                   if u==i and v==j):
                parent[root(i)]=root(j)
    cc={}
    for i in range(p):cc.setdefault(root(i),[]).append(i)
    return list(cc.values())

def outcomes(A,h,cc,w):
    available={one(w)}
    for C in cc:
        opts=set()
        for bits in product((0,1),repeat=len(C)):
            x=dict(zip(C,bits));g=one(w)
            for i,a in h:
                if i in x and x[i]:g=mul(g,a)
            opts.add(g)
        available={mul(a,b) for a in available for b in opts}
    return {mul(z,A) for z in available}

def random_perm(r,w):
    a=list(range(w));r.shuffle(a);return tuple(a)

def test():
    r=Random(20261028)
    for trial in range(250):
        p=r.randrange(1,9);L=r.randrange(1,26);w=5
        word=[];A=one(w)
        for t in range(L):
            i=r.randrange(p)
            g0=random_perm(r,w);A=mul(A,g0)
            if trial%2:
                g1=random_perm(r,w)
            else:
                # Desired normalized deltas: two possibly noncommuting
                # variables on 0,1,2 and remaining commuting on 3,4.
                h=list(range(w))
                if i<2:
                    z=list(range(3));r.shuffle(z);h[:3]=z
                elif r.randrange(2):h[3],h[4]=h[4],h[3]
                d=mul(mul(inv(A),tuple(h)),A)
                g1=mul(g0,d)
            word.append((i,g0,g1))
        base,h=normalize(word,w)
        cc=components(h,p)
        values=set()
        for x in product((0,1),repeat=p):
            got=evaluate(word,x,w)
            z=one(w)
            for i,a in h:
                if x[i]:z=mul(z,a)
            assert mul(z,base)==got
            values.add(got)
        assert outcomes(base,h,cc,w)==values
        if trial%2==0:assert max(map(len,cc))<=2
    print("PASS: 250 group programs, all assignments, normalized/component outputs")
    # Test moving exceptional constants through normal-subgroup deltas.
    w=5;rotation=(1,2,3,0,4);flip=(0,3,2,1,4)
    r2=mul(rotation,rotation);sf=mul(flip,rotation)
    N={one(w),r2,sf,mul(r2,sf)}
    G={one(w)}
    while True:
        nxt=G|{mul(g,a) for g in G for a in (rotation,flip)}
        if len(nxt)==len(G):break
        G=nxt
    assert len(G)==8 and all(mul(mul(g,n),inv(g)) in N for g in G for n in N)
    for trial in range(200):
        p=r.randrange(1,8);L=r.randrange(1,23)
        bad={i for i in range(p) if r.randrange(4)==0}
        word=[(r.randrange(p),) for _ in range(L)]
        word=[(i,r.choice(tuple(G if i in bad else N))) for (i,) in word]
        for x in product((0,1),repeat=p):
            acc=one(w);constant=one(w);normal=one(w)
            for i,h in word:
                if x[i]:acc=mul(acc,h)
                if i in bad and x[i]:constant=mul(constant,h)
                elif i not in bad and x[i]:
                    normal=mul(normal,mul(mul(constant,h),inv(constant)))
            assert normal in N and mul(normal,constant)==acc
    print("PASS: 200 normal-core programs, all assignments")

if __name__=="__main__":test()
