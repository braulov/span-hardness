#!/usr/bin/env python3
"""Independent small-graph checks of rank encodings. Python stdlib only."""
from itertools import combinations
from random import Random

def rank_f2(rows):
    pivots = {}
    for x in rows:
        while x:
            j = x.bit_length() - 1
            if j not in pivots:
                pivots[j] = x
                break
            x ^= pivots[j]
    return len(pivots)

def incidence_rank(n, edges):
    return rank_f2([(1 << a) ^ (1 << b) for a, b in edges])

def components(n, edges, active=None):
    allowed = set(range(n)) if active is None else set(active)
    adj = {u: set() for u in allowed}
    for u, v in edges:
        if u in allowed and v in allowed:
            adj[u].add(v)
            adj[v].add(u)
    seen = set()
    cc = 0
    for root in allowed:
        if root in seen:
            continue
        cc += 1
        seen.add(root)
        stack = [root]
        while stack:
            u = stack.pop()
            for v in adj[u] - seen:
                seen.add(v)
                stack.append(v)
    return cc

def is_forest(n, edges):
    parent = list(range(n))
    def find(x):
        while x != parent[x]:
            x = parent[x]
        return x
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        parent[ru] = rv
    return True

def cycle_space_columns(n, edges):
    m = len(edges)
    parent = list(range(n))
    def find(u):
        while parent[u] != u:
            u = parent[u]
        return u
    tree_adj = [[] for _ in range(n)]
    non_tree = []
    for j, (u, v) in enumerate(edges):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            tree_adj[u].append((v, j))
            tree_adj[v].append((u, j))
        else:
            non_tree.append((j, u, v))
    rows = []
    for j, u, v in non_tree:
        visited = {u}
        stack = [(u, 0)]
        path = None
        while stack:
            node, bits = stack.pop()
            if node == v:
                path = bits
                break
            for other, eid in tree_adj[node]:
                if other not in visited:
                    visited.add(other)
                    stack.append((other, bits ^ (1 << eid)))
        assert path is not None
        rows.append(path | (1 << j))
    columns = [sum(((row >> j) & 1) << i for i, row in enumerate(rows)) for j in range(m)]
    assert len(rows) == m - n + components(n, edges)
    return columns, len(rows)

def test_graph(n, edges):
    m = len(edges)
    for mask in range(1 << m):
        chosen = [edges[i] for i in range(m) if mask & (1 << i)]
        r = incidence_rank(n, chosen)
        assert r == n - components(n, chosen)
        assert (r == len(chosen)) == is_forest(n, chosen)
        degrees = [sum(u == v or w == v for u, w in chosen) for v in range(n)]
        if n >= 3:
            is_cycle = all(d == 2 for d in degrees) and components(n, chosen) == 1
            assert (all(d == 2 for d in degrees) and r >= n-1) == is_cycle
    for mask in range(1 << n):
        S = {v for v in range(n) if mask & (1 << v)}
        remaining = [(u, v) for u, v in edges if u in S and v in S]
        r = incidence_rank(n, remaining)
        assert (r >= len(remaining)) == is_forest(n, remaining)
        if S:
            connected = components(n, remaining, S) == 1
            assert (r >= len(S)-1) == connected
            dominates = all(v in S or any((v == u and w in S) or (v == w and u in S) for u,w in edges) for v in range(n))
            cover = all(u in S or v in S for u,v in edges)
            assert (dominates and r >= len(S)-1) == (dominates and connected)
            assert (cover and r >= len(S)-1) == (cover and connected)
            D = set(range(n))-S
            if D:
                del_edges = [(u,v) for u,v in edges if u in D and v in D]
                full_rank = r + incidence_rank(n, del_edges)
                threshold = len(remaining) + len(D) - 1
                assert (full_rank >= threshold) == (is_forest(n,remaining) and components(n,del_edges,D)==1)

def test_dual_and_hub(n, edges):
    cols, target = cycle_space_columns(n, edges)
    for mask in range(1 << n):
        S = {v for v in range(n) if mask & (1 << v)}
        remaining_indices = [i for i,(u,v) in enumerate(edges) if u in S and v in S]
        complement = set(range(len(edges))) - set(remaining_indices)
        selected = [cols[j] for j in complement]
        retained = [edges[i] for i in remaining_indices]
        assert (rank_f2(selected) == target) == is_forest(n,retained)
        if S:
            root = min(S)
            hub_edges = retained + [(n,v) for v in range(n) if v not in S or v == root]
            assert (incidence_rank(n+1,hub_edges) == n) == (components(n,retained,S)==1)

def test_parity_certificates(n, edges):
    m = len(edges)
    for smask in range(1 << n):
        S = {v for v in range(n) if smask & (1 << v)}
        induced = [e for e in edges if e[0] in S and e[1] in S]
        count_even = 0
        for mask in range(1 << len(induced)):
            chosen = [e for i,e in enumerate(induced) if mask & (1 << i)]
            degrees = [sum(u==v or w==v for u,w in chosen) for v in range(n)]
            count_even += all(d % 2 == 0 for d in degrees)
        assert (count_even % 2 == 1) == is_forest(n,induced)
    for mask in range(1 << m):
        chosen = [e for i,e in enumerate(edges) if mask & (1 << i)]
        degrees = [sum(u==v or w==v for u,w in chosen) for v in range(n)]
        if n < 3 or not all(d==2 for d in degrees):
            continue
        cut_witnesses = 0
        for cutmask in range(1 << (n-1)):
            bit = lambda v: ((cutmask>>(v-1))&1) if v else 0
            cut_witnesses += all(bit(u)==bit(v) for u,v in chosen)
        assert (cut_witnesses%2==1) == (components(n,chosen)==1)

def test_star_cover():
    U = range(4)
    family = [{0,1},{1,2},{3},{0,2,3}]
    for mask in range(1 << len(family)):
        edges = [(0,u+1) for i,S in enumerate(family) if mask & (1 << i) for u in S]
        covered = set().union(*(family[i] for i in range(len(family)) if mask & (1 << i)))
        assert incidence_rank(5,edges) == len(covered)

def main():
    count = 0
    for n in range(2,5):
        edges_all = list(combinations(range(n),2))
        for mask in range(1 << len(edges_all)):
            edges = [e for j,e in enumerate(edges_all) if mask & (1 << j)]
            test_graph(n,edges)
            test_dual_and_hub(n,edges)
            test_parity_certificates(n,edges)
            count += 1
    rng=Random(2048)
    edges_all=list(combinations(range(5),2))
    for _ in range(40):
        edges=[e for e in edges_all if rng.randrange(2)]
        test_graph(5,edges)
        test_dual_and_hub(5,edges)
        test_parity_certificates(5,edges)
        count += 1
    test_star_cover()
    print(f"PASS: graph rank, FVS, Hamiltonian cycle, connectivity, duality, parity and coverage on {count} graphs")

if __name__ == "__main__":
    main()
