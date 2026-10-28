"""Small-case checks of the finite-field trace generator and hidden XOR-junta
recovery. Run: python verify_linear_junta.py (Python stdlib).
The testing field constructor trial-enumerates irreducibles; use Shoup 1990
for the promised general deterministic polynomial-time construction.
"""
from fractions import Fraction
from random import Random

def gf_mul(a,b,poly,m):
    z=0
    for _ in range(m):
        if b&1:z^=a
        b>>=1;a<<=1
        if a&(1<<m):a^=poly
    return z

def remainder(a,poly):
    while a and a.bit_length()>=poly.bit_length():
        a^=poly<<(a.bit_length()-poly.bit_length())
    return a

def gcd(a,b):
    while b:a,b=b,remainder(a,b)
    return a

def irred(poly,m):
    x=remainder(2,poly);z=x
    for _ in range(m):z=remainder(pmul(z,z,poly),poly)
    if z!=x:return False
    divisors=[d for d in range(2,m+1)
              if m%d==0 and all(d%e for e in range(2,int(d**.5)+1))]
    for d in divisors:
        z=x
        for _ in range(m//d):z=remainder(pmul(z,z,poly),poly)
        if gcd(z^x,poly)!=1:return False
    return True

def pmul(a,b,poly):
    z=0
    while b:
        if b&1:z^=a
        a<<=1;b>>=1
    return remainder(z,poly)

def small_bias(p,m):
    poly=next((1<<m)|low for low in range(1,1<<m,2)
              if irred((1<<m)|low,m))
    q=1<<m
    trace=[]
    for a in range(q):
        y=a;v=0
        for _ in range(m):
            v^=y;y=gf_mul(y,y,poly,m)
        assert v in (0,1)
        trace.append(v)
    D=[]
    for b in range(q):
        powers=[1]
        for _ in range(1,p):powers.append(gf_mul(powers[-1],b,poly,m))
        for a in range(q):
            D.append(sum(trace[gf_mul(a,z,poly,m)]<<i
                         for i,z in enumerate(powers)))
    return D

def learn(p,k,f,D):
    def period(v):
        return all(f(x)==f(x^v) for x in D)
    pivots=[];columns=[]
    for i in range(p):
        answer=None
        for pattern in range(1<<len(pivots)):
            v=1<<i
            for j,a in enumerate(pivots):
                if (pattern>>j)&1:v^=1<<a
            if period(v):answer=pattern;break
        if answer is None:
            assert len(pivots)<k
            pivots.append(i)
            answer=1<<(len(pivots)-1)
        columns.append(answer)
    def learned(x):
        z=0
        for i,c in enumerate(columns):
            if (x>>i)&1:z^=c
        represented=sum(((z>>j)&1)<<a for j,a in enumerate(pivots))
        return f(represented)
    return pivots,columns,learned

def test():
    rng=Random(81223)
    for p,m in ((4,6),(5,7),(6,7)):
        D=small_bias(p,m);q=1<<m
        maxbias=max(abs(sum(1 if (x&mask).bit_count()%2==0 else -1
                            for x in D))/len(D)
                    for mask in range(1,1<<p))
        assert maxbias<=(p-1)/q+1e-10
        for k in (1,2):
            for trial in range(12):
                rows=[rng.randrange(1<<p) for _ in range(k)]
                table=[rng.randrange(2) for _ in range(1<<k)]
                def f(x):
                    z=sum(((x&v).bit_count()%2)<<j
                          for j,v in enumerate(rows))
                    return table[z]
                count=sum(f(x) for x in range(1<<p))
                mean=Fraction(sum(f(x) for x in D),len(D))
                approx=mean*(1<<k)
                rounded=(2*approx.numerator+approx.denominator)//(2*approx.denominator)
                if (p-1)/q*(2**(k/2))<2**(-k-1):
                    assert rounded*(1<<(p-k))==count
                pivots,columns,h=learn(p,k,f,D)
                assert len(pivots)<=k
                assert all(f(x)==h(x) for x in range(1<<p))
    print("PASS finite-field trace bias, exact counting, unknown quotient recovery")

if __name__=="__main__":test()
