"""Black-box matroid relaxation oracle gap on BP-derived LGS gadgets."""
from itertools import product

def bp(p,even,secret,extra):
    states=[(i,par,eq) for i in range(p) for par in (0,1) for eq in (0,1)]
    A=('accept',); R=('reject',)
    ids={v:j for j,v in enumerate(states+[A,R])}
    edges=[]
    for i,par,eq in states:
        for z in (0,1):
            newpar=par^z
            neweq=eq and (z==secret[i])
            if i+1==p:
                good=(newpar==0 if even else newpar==1) or (extra and neweq)
                dest=A if good else R
            else:dest=(i+1,newpar,neweq)  # patched below
            edges.append((ids[(i,par,eq)],ids[dest], i+1 if z else -(i+1)))
    edges.append((ids[(0,0,1)],ids[R],None))
    edges.append((ids[A],ids[R],0))
    return len(ids),edges

def instance(p,secret,is_yes):
    n1,e1=bp(p,True,secret,False)
    n2,e2=bp(p,False,secret,is_yes)
    edges=e1+[(u+n1,v+n1,lab) for u,v,lab in e2]
    edges.append((0,n1,None))
    return n1+n2,edges

def relax(n,edges,partial):
    parent=list(range(n))
    def root(a):
        while parent[a]!=a:a=parent[a]
        return a
    for u,v,lab in edges:
        on=lab is None or (lab!=0 and (abs(lab) not in partial
              or partial[abs(lab)]==(lab>0)))
        if on:parent[root(u)]=root(v)
    return len({root(i) for i in range(n)})==1

def test():
    ncases=0
    for p in range(2,6):
        for secret in product((0,1),repeat=p):
            if sum(secret)%2:continue
            no=instance(p,secret,False)
            yes=instance(p,secret,True)
            for vals in product((None,False,True),repeat=p):
                alpha={j+1:v for j,v in enumerate(vals) if v is not None}
                full=len(alpha)==p
                assert relax(*no,alpha)==(not full)
                match=full and all(alpha[j+1]==bool(secret[j]) for j in range(p))
                assert relax(*yes,alpha)==((not full) or match)
                ncases+=1
    print('PASS',ncases,'partial assignments')

if __name__=='__main__':test()
