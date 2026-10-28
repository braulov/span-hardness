"""Star-interaction A5 gadget and abelian-spine DP checks. Python >=3.10."""
from itertools import product,permutations
from collections import deque
from random import Random
W=5; ID=tuple(range(W))
def mul(a,b):return tuple(a[b[i]] for i in range(W))
def inv(a):
    b=[0]*W
    for i,v in enumerate(a):b[v]=i
    return tuple(b)
def parity(p):
    return sum(p[i]>p[j] for i in range(W) for j in range(i+1,W))%2
A5=tuple(z for z in permutations(range(W)) if not parity(z))
a=(1,2,0,3,4); g=(1,2,3,4,0)
CONJ={mul(mul(c,a),inv(c)):c for c in A5}
assert len(CONJ)==20
DECOMP={ID:()}; q=deque([ID])
while q:
    u=q.popleft()
    for cycle in CONJ:
        v=mul(u,cycle)
        if v not in DECOMP:
            DECOMP[v]=DECOMP[u]+(cycle,)
            q.append(v)
assert len(DECOMP)==60 and max(map(len,DECOMP.values()))==2

def eval_word(word,x):
    result=ID
    for i,h in word:
        if x[i]:result=mul(result,h)
    return result

def star_transform(word,ynum):
    result=[]
    for i,h in word:
        for cyc in DECOMP[h]:
            c=CONJ[cyc]
            result.extend(((ynum,c),(i,a),(ynum,inv(c))))
    return result

def solve_abelian_spine(word,p,exceptional,target):
    exceptional=set(exceptional)
    H={ID,a,mul(a,a)}
    assert all(h in H for i,h in word if i not in exceptional)
    others=[i for i in range(p) if i not in exceptional]
    special=sorted(exceptional)
    for bits in product((0,1),repeat=len(special)):
        alpha=dict(zip(special,bits))
        segments=[]; constants=[]; current=[]
        for i,h in word:
            if i in exceptional:
                segments.append(current);current=[]
                constants.append(h if alpha[i] else ID)
            else:current.append((i,h))
        segments.append(current)
        m=len(segments)
        contributions={i:[ID]*m for i in others}
        for j,chunk in enumerate(segments):
            for i,h in chunk:
                contributions[i][j]=mul(contributions[i][j],h)
        reachable={(ID,)*m}
        for i in others:
            nxt=set(reachable)
            for tup in reachable:
                nxt.add(tuple(mul(tup[j],contributions[i][j])
                              for j in range(m)))
            reachable=nxt
        for tup in reachable:
            result=ID
            for j in range(m):
                result=mul(result,tup[j])
                if j<len(constants):result=mul(result,constants[j])
            if result==target:return True
    return False

def test():
    rng=Random(117)
    for trial in range(120):
        p=rng.randint(1,7);L=rng.randint(1,20)
        word=[(rng.randrange(p),rng.choice(A5)) for _ in range(L)]
        transformed=star_transform(word,p)
        assert len(transformed)<=6*L
        for bits in product((0,1),repeat=p):
            assert eval_word(transformed,bits+(1,))==eval_word(word,bits)
            assert eval_word(transformed,bits+(0,)) in {ID,a,mul(a,a)}
    print("PASS: 120 star normal forms, every assignment")
    rng=Random(118);H=(ID,a,mul(a,a))
    for trial in range(220):
        p=rng.randint(2,7)
        B={p-1}
        if p>3 and trial%4==0:B.add(p-2)
        others=[i for i in range(p) if i not in B]
        word=[(rng.choice(others),rng.choice(H))
              for _ in range(rng.randint(1,17))]
        for _ in range(rng.randint(0,5)):
            word.insert(rng.randrange(len(word)+1),
                        (rng.choice(sorted(B)),rng.choice(A5)))
        target=rng.choice(A5)
        expected=any(eval_word(word,x)==target
                     for x in product((0,1),repeat=p))
        assert solve_abelian_spine(word,p,B,target)==expected,trial
    print("PASS: 220 abelian-spine programs, full brute-force comparison")
    print("A5 max conjugate-3-cycle factor length: 2")

if __name__=="__main__":test()
