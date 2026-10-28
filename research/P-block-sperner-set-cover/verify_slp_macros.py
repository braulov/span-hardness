"""Check SLP composition of input-dependent finite-state transition maps."""
from random import Random

def compile_repeats(word,k):
    nodes=[('terminal',x) for x in word]
    layer=list(range(len(word)))
    while len(layer)>1:
        newer=[]
        for j in range(0,len(layer),2):
            if j+1==len(layer):newer.append(layer[j])
            else:
                nodes.append(('compose',layer[j],layer[j+1]))
                newer.append(len(nodes)-1)
        layer=newer
    powers=[layer[0]]
    while (1<<len(powers))<=k:
        nodes.append(('compose',powers[-1],powers[-1]))
        powers.append(len(nodes)-1)
    root=None
    for bit,node in enumerate(powers):
        if k&(1<<bit):
            if root is None:root=node
            else:
                nodes.append(('compose',root,node))
                root=len(nodes)-1
    return nodes,root

def evaluate(nodes,root,bits,w):
    values=[]
    for item in nodes:
        if item[0]=='terminal':
            var,z,o=item[1]
            values.append(tuple((z[s],o[s])[bits[var]] for s in range(w)))
        else:
            f=values[item[1]];g=values[item[2]]
            values.append(tuple(g[f[s]] for s in range(w)))
    return values[root]

def test():
    rng=Random(566)
    for trial in range(700):
        p=rng.randrange(1,8);w=rng.randrange(2,6)
        m=rng.randrange(1,13);k=rng.randrange(1,26)
        word=[(rng.randrange(p),tuple(rng.randrange(w) for _ in range(w)),
               tuple(rng.randrange(w) for _ in range(w))) for _ in range(m)]
        nodes,root=compile_repeats(word,k)
        assert len(nodes)<=m+2*m+2*k.bit_length()+5
        for _ in range(3):
            bits=tuple(rng.randrange(2) for _ in range(p))
            values=list(range(w))
            for _ in range(k):
                for var,z,o in word:
                    values=[(z[s],o[s])[bits[var]] for s in values]
            assert evaluate(nodes,root,bits,w)==tuple(values),(trial,bits)
    print('PASS: 700 random macros x 3 assignments')

if __name__=='__main__':test()
