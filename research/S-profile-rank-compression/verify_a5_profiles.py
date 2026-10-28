"""Regression: canonical A5 abelian runs, exact profile counting, brute force.
Python 3.10+. Run python verify_a5_profiles.py.
"""
from itertools import permutations,product
from collections import deque
from random import Random
ID=tuple(range(5))
def mul(a,b): return tuple(a[b[i]] for i in range(5))
G=tuple(a for a in permutations(range(5))
        if sum(a[i]>a[j] for i in range(5) for j in range(i+1,5))%2==0)
C={a:frozenset(b for b in G if mul(a,b)==mul(b,a)) for a in G}
assert len(G)==60
assert {len(C[a]) for a in G if a!=ID}=={3,4,5}
assert all(mul(u,v)==mul(v,u) for a in G if a!=ID for u in C[a] for v in C[a])
assert all(C[a]==C[b] for a in G if a!=ID for b in C[a] if b!=ID)

def canonical(word):
    word=[z for z in word if z[1]!=ID]
    if not word:return []
    runs=[[word[0]]]
    for z in word[1:]:
        if C[z[1]]==C[runs[-1][-1][1]]:runs[-1].append(z)
        else:runs.append([z])
    return runs

def profiles(segments,p):
    out=[]
    for i in range(p):
        item=[]
        for seg in segments:
            g=ID
            for j,h in seg:
                if i==j:g=mul(g,h)
            item.append(g)
        out.append(tuple(item))
    return out

def histogram_dp(segments,p):
    V=profiles(segments,p)
    zero=tuple(ID for _ in segments)
    D={zero:1}
    for v in V:
        nxt=D.copy()
        for z,n in D.items():
            nz=tuple(mul(a,b) for a,b in zip(z,v))
            nxt[nz]=nxt.get(nz,0)+n
        D=nxt
    hist={}
    for z,n in D.items():
        g=ID
        for h in z:g=mul(g,h)
        hist[g]=hist.get(g,0)+n
    return hist,D

def brute(word,p):
    hist={}
    for x in product((0,1),repeat=p):
        g=ID
        for i,h in word:
            if x[i]:g=mul(g,h)
        hist[g]=hist.get(g,0)+1
    return hist

def size_subgroup(segments,p):
    V=profiles(segments,p)
    zero=tuple(ID for _ in segments)
    seen={zero}
    q=deque([zero])
    while q:
        z=q.popleft()
        for v in V:
            nz=tuple(mul(a,b) for a,b in zip(z,v))
            if nz not in seen:
                seen.add(nz);q.append(nz)
    return len(seen)

def alternate_segments(word,mask):
    out=[];start=0
    for i in range(len(word)-1):
        if mask>>i&1:
            out.append(word[start:i+1]);start=i+1
    return out+[word[start:]]

def valid(segs):
    return all(mul(a[1],b[1])==mul(b[1],a[1])
               for seg in segs for a in seg for b in seg)

def test():
    r=Random(20728)
    for t in range(500):
        p=r.randrange(1,8);L=r.randrange(1,15)
        word=[(r.randrange(p),r.choice(G)) for _ in range(L)]
        segments=canonical(word)
        got,D=histogram_dp(segments,p)
        assert got==brute(word,p),(t,got)
        assert sum(D.values())==2**p
    print("PASS: 500 A5 programs; all output counts equal brute force")
    for t in range(100):
        p=r.randrange(1,4);L=r.randrange(1,7)
        word=[(r.randrange(p),r.choice(G)) for _ in range(L)]
        word=[z for z in word if z[1]!=ID]
        if not word:continue
        mine=size_subgroup(canonical(word),p)
        for mask in range(1<<(len(word)-1)):
            candidate=alternate_segments(word,mask)
            if valid(candidate):
                assert mine<=size_subgroup(candidate,p),(t,mine,mask)
    print("PASS: 100 A5 programs; canonical segmentation optimal among valid cuts")

if __name__=="__main__":test()
