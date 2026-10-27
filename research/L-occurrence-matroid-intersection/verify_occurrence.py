from collections import deque
from itertools import product
from random import Random

def forest(n, E, indices):
    parent=list(range(n))
    def root(v):
        while parent[v]!=v:
            parent[v]=parent[parent[v]]
            v=parent[v]
        return v
    for i in indices:
        a,b,_=E[i]
        x,y=root(a),root(b)
        if x==y:return False
        parent[x]=y
    return True

def common_basis_size(n, edges):
    E=[edge for edge in edges if edge[2]!=0]
    groups=list(range(len(E)))
    occurrences={}
    for j,(_,_,lit) in enumerate(E):
        if lit is not None:occurrences.setdefault(abs(lit),[]).append(j)
    assert all(len(a)<=2 for a in occurrences.values())
    for js in occurrences.values():
        if len(js)==2 and E[js[0]][2]==-E[js[1]][2]:
            groups[js[1]]=groups[js[0]]
    def partition(I):
        a=[groups[i] for i in I]
        return len(a)==len(set(a))
    I=set()
    while True:
        O=set(range(len(E)))-I
        starts=[e for e in O if forest(n,E,I|{e})]
        ends={e for e in O if partition(I|{e})}
        prev={v:None for v in starts}
        q=deque(starts)
        goal=None
        while q:
            e=q.popleft()
            if e in ends:
                goal=e;break
            if e not in I:
                for f in I:
                    if f not in prev and partition((I-{f})|{e}):
                        prev[f]=e;q.append(f)
            else:
                for z in O:
                    if z not in prev and forest(n,E,(I-{e})|{z}):
                        prev[z]=e;q.append(z)
        if goal is None:return len(I)
        path=[];v=goal
        while v is not None:
            path.append(v);v=prev[v]
        I.symmetric_difference_update(path)
        assert forest(n,E,I) and partition(I)

def brute(n,E,p):
    for bits in product([0,1],repeat=p):
        parents=list(range(n))
        def root(v):
            while parents[v]!=v:v=parents[v]
            return v
        for a,b,lit in E:
            if lit is None or (lit!=0 and bits[abs(lit)-1]==int(lit>0)):
                parents[root(a)]=root(b)
        if len({root(v) for v in range(n)})==1:return True
    return False

def split_3cnf(clauses,p):
    occurrences=[[] for _ in range(p)]
    out=[]
    k=0
    for c in clauses:
        row=[]
        for lit in c:
            k+=1
            occurrences[abs(lit)-1].append(k)
            row.append(k if lit>0 else -k)
        out.append(row)
    for group in occurrences:
        if len(group)>=2:
            for j,z in enumerate(group):
                out.append([-z,group[(j+1)%len(group)]])
    assert all(sum(abs(l)==j for c in out for l in c)<=3 for j in range(1,k+1))
    return out,k

def sat(clauses,p):
    return any(all(any(bits[abs(l)-1]==int(l>0) for l in c) for c in clauses)
               for bits in product([0,1],repeat=p))

def tests():
    rng=Random(4202)
    for t in range(2500):
        n=rng.randrange(1,8);p=rng.randrange(0,5)
        labels=[]
        for i in range(1,p+1):
            labels.extend([i if rng.randrange(2) else -i for _ in range(rng.randrange(3))])
        labels.extend([None]*rng.randrange(4))
        labels.extend([0]*rng.randrange(4))
        E=[(rng.randrange(n),rng.randrange(n),label) for label in labels]
        assert (common_basis_size(n,E)==n-1)==brute(n,E,p),(t,n,p,E)
    print("PASS: 2500 two-occurrence LGS cases")
    rng=Random(2026)
    for t in range(800):
        p=rng.randrange(1,5)
        clauses=[[rng.choice([-1,1])*rng.randrange(1,p+1)
                  for _ in range(rng.randrange(1,4))]
                 for _ in range(rng.randrange(1,7))]
        converted,k=split_3cnf(clauses,p)
        assert sat(clauses,p)==sat(converted,k)
        assert all(1<=len(c)<=3 for c in converted)
        E=[(j,j+1,lit) for j,c in enumerate(converted) for lit in c]
        assert len(converted)+1>0 and all(abs(a-b)==1 for a,b,_ in E)
    print("PASS: 800 bounded-occurrence SAT-to-path reductions")

if __name__=="__main__":
    tests()
