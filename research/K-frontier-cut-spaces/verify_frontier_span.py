"""Brute-force validator of frontier-cut-space LGS decision DP.
Labels: None=always on, 0=always off, +i=x_i, -i=not x_i.
Uses only Python standard library; python verify_frontier_span.py
"""
from itertools import product
from random import Random

def basis(vecs):
    piv={}
    for v in vecs:
        while v:
            j=v.bit_length()-1
            if j in piv: v^=piv[j]
            else: piv[j]=v; break
    return list(piv.values())

def bit(mask, bag, v):
    return 0 if v==0 else (mask >> [w for w in bag if w!=0].index(v))&1

def intro(vec, old, new):
    out=0
    for mask in range(1<<(len(new)-1)):
        prev=sum(bit(mask,new,v)<<j for j,v in enumerate(w for w in old if w!=0))
        if (vec>>prev)&1: out|=1<<mask
    return out

def join(vec, bag, u, v):
    return sum((1<<mask) for mask in range(1<<(len(bag)-1))
               if (vec>>mask)&1 and bit(mask,bag,u)==bit(mask,bag,v))

def forget(vec, old, new):
    out=0
    for mask in range(1<<(len(old)-1)):
        if (vec>>mask)&1:
            nxt=sum(bit(mask,old,v)<<j for j,v in enumerate(w for w in new if w!=0))
            out ^= 1<<nxt
    return out

def solve(n, edges, p):
    if n==1: return True
    if any(not any(u==v or w==v for u,w,_ in edges) for v in range(n)):
        return False
    state={():[1]}; bag=(0,)
    for i,(u,v,label) in enumerate(edges):
        pre=edges[:i]; future=edges[i:]; rest=edges[i+1:]
        seen={abs(t) for _,_,t in pre if t not in (0,None)}
        unseen={abs(t) for _,_,t in future if t not in (0,None)}
        seen_next=seen|({abs(label)} if label not in (0,None) else set())
        later={abs(t) for _,_,t in rest if t not in (0,None)}
        live=sorted(seen&unseen); nextlive=sorted(seen_next&later)
        mid=tuple(sorted(set(bag)|{u,v}))
        later_vertices={z for a,b,_ in rest for z in (a,b)}
        nxtbag=tuple(sorted({0}|(set(mid)&later_vertices)))
        ns={}
        for oldbits, vecs in state.items():
            values=dict(zip(live,oldbits))
            opts=(0,1) if label not in (0,None) and abs(label) not in values else (None,)
            for choice in opts:
                assigned=values.copy()
                if choice is not None: assigned[abs(label)]=choice
                on=label is None or (label not in (0,None) and
                   assigned[abs(label)]==(1 if label>0 else 0))
                img=[]
                for z in vecs:
                    z=intro(z,bag,mid)
                    if on: z=join(z,mid,u,v)
                    z=forget(z,mid,nxtbag)
                    if z: img.append(z)
                key=tuple(assigned[j] for j in nextlive)
                ns[key]=basis(ns.get(key,[])+img)
        state,bag=ns,nxtbag
    return any(z&1 for vs in state.values() for z in vs)

def brute(n,edges,p):
    for assignment in product((0,1),repeat=p):
        parent=list(range(n))
        def find(a):
            while parent[a]!=a: a=parent[a]
            return a
        for u,v,label in edges:
            on=label is None or (label not in (0,None) and
                assignment[abs(label)-1]==(1 if label>0 else 0))
            if on: parent[find(u)]=find(v)
        if len({find(i) for i in range(n)})==1: return True
    return False

def parity_graph(p):
    s=0; reject=2*p; accept=2*p+1
    edges=[(s,reject,None)]
    for i in range(p):
        for z in (0,1):
            edges.append((2*i+z,2*(i+1)+z,-(i+1)))
            edges.append((2*i+z,2*(i+1)+(1-z),i+1))
    edges.append((accept,reject,0))
    return 2*(p+1),edges

def test():
    r=Random(17)
    for trial in range(3000):
        n=r.randrange(2,7); p=r.randrange(1,5); m=r.randrange(1,13)
        labels=[None,0]+[a for i in range(1,p+1) for a in (i,-i)]
        edges=[(r.randrange(n),r.randrange(n),r.choice(labels)) for _ in range(m)]
        assert solve(n,edges,p)==brute(n,edges,p), (trial,edges)
    for p in range(1,11):
        n,edges=parity_graph(p)
        assert solve(n,edges,p)
        # Force all switches to zero: odd parity becomes impossible.
        forced=[(u,v,0 if lab>0 else None if lab<0 else lab)
                for u,v,lab in edges if lab is not None]
        # The constant-on edge was excluded from the preceding comprehension.
        forced=[(u,v,None) for u,v,lab in edges if lab is None]+forced
        assert not solve(n,forced,p)
    print("PASS: 3000 random cases, parity p=1..10")

if __name__=="__main__":
    test()
