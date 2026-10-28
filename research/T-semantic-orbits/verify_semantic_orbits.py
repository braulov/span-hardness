"""Tests for T: symmetric linear-size circuit, A5 Barrington AND words, profile rank.
Run: python verify_semantic_orbits.py (Python 3.10+, stdlib)
"""
from itertools import permutations,product
from math import comb
from random import Random
ID=tuple(range(5))
def mul(a,b):return tuple(a[b[i]] for i in range(5))
def inv(a):return tuple(a.index(j) for j in range(5))
A5=[a for a in permutations(range(5)) if sum(a[i]>a[j] for i in range(5) for j in range(i+1,5))%2==0]
def order(a):
    x=ID
    for i in range(1,61):
        x=mul(x,a)
        if x==ID:return i
    raise Exception('bad element')
FIVE=[a for a in A5 if order(a)==5]
PAIR={}
for a in FIVE:
    for b in FIVE:
        g=mul(mul(mul(a,b),inv(a)),inv(b))
        if order(g)==5: PAIR.setdefault(g,(a,b))
assert len(PAIR)==24
TARGET=(1,2,3,4,0)
def and_word(indices,target=TARGET):
    if len(indices)==1:return [(indices[0],target)]
    assert len(indices)%2==0
    a,b=PAIR[target];m=len(indices)//2
    u=and_word(indices[:m],a);v=and_word(indices[m:],b)
    return u+v+[(i,inv(g)) for i,g in reversed(u)]+[(i,inv(g)) for i,g in reversed(v)]
def eval_word(word,x):
    a=ID
    for i,g in word:
        if x[i]:a=mul(a,g)
    return a
C={g:frozenset(h for h in A5 if mul(g,h)==mul(h,g)) for g in A5}
def rank(A,q):
    a=[r[:] for r in A];i=0
    for j in range(len(a[0])):
        k=next((k for k in range(i,len(a)) if a[k][j]),None)
        if k is None:continue
        a[i],a[k]=a[k],a[i]
        z=pow(a[i][j],-1,q);a[i]=[(z*t)%q for t in a[i]]
        for k in range(len(a)):
            if k!=i and a[k][j]:
                z=a[k][j];a[k]=[(t-z*s)%q for t,s in zip(a[k],a[i])]
        i+=1
    return i
def profile_rank(word,p):
    runs=[]
    for i,g in word:
        if not runs or C[runs[-1][-1][1]]!=C[g]:runs.append([])
        runs[-1].append((i,g))
    matrix=[]
    for run in runs:
        g=run[0][1];powers=[ID]
        for _ in range(4):powers.append(mul(powers[-1],g))
        row=[0]*p
        for i,h in run:row[i]=(row[i]+powers.index(h))%5
        matrix.append(row)
    return rank(matrix,5),len(runs)

class Circuit:
    def __init__(self,p):
        self.gates=[('const',0),('const',1)]+[('input',i) for i in range(p)]
        self.inputs=list(range(2,p+2));self.zero=0;self.one=1
    def add(self,op,*arg):
        i=len(self.gates);self.gates.append((op,*arg));return i
    def eval(self,x):
        v=[]
        for op,*a in self.gates:
            if op=='const':z=a[0]
            elif op=='input':z=x[a[0]]
            elif op=='not':z=1-v[a[0]]
            elif op=='xor':z=v[a[0]]^v[a[1]]
            elif op=='and':z=v[a[0]]&v[a[1]]
            elif op=='or':z=v[a[0]]|v[a[1]]
            v.append(z)
        return v
def compile_symmetric(p,weights):
    c=Circuit(p);bins=[[] for _ in range(p.bit_length()+3)]
    bins[0]=c.inputs[:]
    for j in range(len(bins)-1):
        while len(bins[j])>=3:
            a,b,d=[bins[j].pop() for _ in range(3)]
            t=c.add('xor',a,b)
            s=c.add('xor',t,d)
            carry=c.add('or',c.add('and',a,b),c.add('and',t,d))
            bins[j].append(s);bins[j+1].append(carry)
    carry=c.zero;bits=[]
    for j in range(p.bit_length()):
        a=bins[j][0] if bins[j] else c.zero
        b=bins[j][1] if len(bins[j])>1 else c.zero
        t=c.add('xor',a,b)
        bits.append(c.add('xor',t,carry))
        carry=c.add('or',c.add('and',a,b),c.add('and',t,carry))
    decode=[c.one]
    for bit in reversed(bits):
        neg=c.add('not',bit)
        new=[]
        for d in decode:new.extend((c.add('and',d,neg),c.add('and',d,bit)))
        decode=new
    result=c.zero
    for k in weights:result=c.add('or',result,decode[k])
    return c,result
def test():
    rng=Random(1729)
    for p in range(1,33):
        for _ in range(12):
            weights={k for k in range(p+1) if rng.randrange(2)}
            circuit,out=compile_symmetric(p,weights)
            assert len(circuit.gates)<90*(p+1)
            xs=list(product((0,1),repeat=p)) if p<=8 else [
                tuple(rng.randrange(2) for _ in range(p)) for _ in range(80)]
            for x in xs:assert circuit.eval(x)[out]==int(sum(x) in weights)
            assert sum(comb(p,k) for k in weights)<=2**p
    print('PASS: linear-size circuit, 12 random functions for p=1..32')
    for p in (2,4,8,16):
        word=and_word(list(range(p)))
        assert len(word)==p*p
        rk,runs=profile_rank(word,p)
        assert 4*rk>=p
        if p<=8:
            for x in product((0,1),repeat=p):
                assert eval_word(word,x)==(TARGET if all(x) else ID)
        else:
            assert eval_word(word,(1,)*p)==TARGET
            for j in range(p):
                x=[1]*p;x[j]=0
                assert eval_word(word,x)==ID
        print('AND',p,'length',len(word),'runs',runs,'rank5',rk)
    print('PASS: explicit A5 AND words and profile rank')
if __name__=='__main__':test()
