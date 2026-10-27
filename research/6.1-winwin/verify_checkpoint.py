"""Finite independent sanity checks for the research checkpoint; stdlib only.

These checks do not verify the cited SAT/isolation/reversibility theorems.
They test the new elementary counting identities and permutation gadgets.
"""
from itertools import combinations, permutations, product
from fractions import Fraction
from pathlib import Path
import json


def rank(columns):
    basis = {}
    for value in columns:
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def components(n, edges):
    seen = set()
    count = 0
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    for start in range(n):
        if start in seen:
            continue
        count += 1
        stack = [start]
        seen.add(start)
        while stack:
            for other in adj[stack.pop()]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
    return count


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(a):
    result = [0] * len(a)
    for i, value in enumerate(a):
        result[value] = i
    return tuple(result)


def cycle_count(a):
    return components(len(a), list(enumerate(a)))


def check_rank_filters():
    checks = 0
    for n in range(1, 5):
        possible = list(combinations(range(n), 2))
        for host_bits in product((0, 1), repeat=len(possible)):
            host = [e for e, bit in zip(possible, host_bits) if bit]
            host_rank = rank([(1 << u) ^ (1 << v) for u, v in host])
            # Independently choose smallest vertex per host component.
            roots = []
            for v in range(n):
                if not any(components(n, host + [(u, v)]) == components(n, host)
                           for u in range(v)):
                    roots.append(v)
            for selected in product((0, 1), repeat=len(host)):
                yes = [e for e, bit in zip(host, selected) if bit]
                no = [e for e, bit in zip(host, selected) if not bit]
                selected_rank = rank([(1 << u) ^ (1 << v) for u, v in yes])
                cut_count = sum(
                    all(((labels >> r) & 1) == 0 for r in roots)
                    and all(((labels >> u) & 1) == ((labels >> v) & 1)
                            for u, v in yes)
                    for labels in range(1 << n))
                assert cut_count == 1 << (host_rank - selected_rank)
                circulation_count = 0
                for z in range(1 << len(no)):
                    incidence = 0
                    for i, (u, v) in enumerate(no):
                        if (z >> i) & 1:
                            incidence ^= (1 << u) ^ (1 << v)
                    circulation_count += incidence == 0
                no_rank = rank([(1 << u) ^ (1 << v) for u, v in no])
                assert circulation_count == 1 << (len(no) - no_rank)
                dual_ground_rank = len(host) - host_rank
                dual_selected_rank = len(yes) - host_rank + no_rank
                assert circulation_count == 1 << (dual_ground_rank - dual_selected_rank)
                checks += 1
    return checks


def check_long_clauses():
    checks = 0
    literals = (1, -1, 2, -2, 3, -3)
    for length in range(5):
        for clause in product(literals, repeat=length):
            for x in product((0, 1), repeat=3):
                satisfied = any(bool(x[abs(lit)-1]) == (lit > 0) for lit in clause)
                extensions = sum(all(not t or
                    not (bool(x[abs(lit)-1]) == (lit > 0))
                    for lit in clause) for t in (0, 1))
                assert extensions == (1 if satisfied else 2)
                checks += 1
    return checks


def check_cycle_merge():
    checks = 0
    ring_checks = 0
    for w in range(2, 7):
        dummy = w
        size = w + 1
        for perm in permutations(range(w)):
            p = tuple(perm) + (dummy,)
            for start in range(w):
                rho = list(range(size))
                rho[start], rho[dummy] = rho[dummy], rho[start]
                for target in range(w):
                    tau = list(range(size))
                    long_cycle = [a for a in range(size) if a != target]
                    for a, b in zip(long_cycle, long_cycle[1:] + long_cycle[:1]):
                        tau[a] = b
                    q = compose(tau, compose(p, compose(rho, inverse(p))))
                    assert cycle_count(q) == (1 if p[start] == target else 3)
                    checks += 1
                    if w <= 4:
                        # Three genuine layers; last transition has product q.
                        transitions = [tuple(range(size)), tuple(range(size)), q]
                        edges = [(i * size + a, ((i+1) % 3) * size + tr[a])
                                 for i, tr in enumerate(transitions) for a in range(size)]
                        assert components(3 * size, edges) == cycle_count(q)
                        columns = [(1 << u) ^ (1 << v) for u, v in edges]
                        assert rank(columns) == 3 * size - cycle_count(q)
                        ring_checks += 1
    return {"cycle_merge_cases": checks, "ring_rank_cases": ring_checks}


def check_root_gadget():
    checks = 0
    for n in range(1, 5):
        possible = list(combinations(range(n), 2))
        for bits in product((0, 1), repeat=len(possible)):
            edges = [e for e, b in zip(possible, bits) if b]
            for mask in range(1, 1 << n):
                chosen = [v for v in range(n) if (mask >> v) & 1]
                selected_edges = [(u, v) for u, v in edges
                                  if u in chosen and v in chosen]
                cc_selected = components(n, selected_edges) - (n-len(chosen))
                for root in chosen:
                    augmented = selected_edges + [(root, v) for v in range(n)
                                                  if v not in chosen]
                    assert components(n, augmented) == cc_selected
                    assert (components(n, augmented) == 1) == (cc_selected == 1)
                    ternary_count = 0
                    for labels in product((0, 1), repeat=2*n):
                        a0, a1 = labels[:n], labels[n:]
                        if not a0[root]:
                            continue
                        if not all(
                            (not ((mask >> v) & 1) or a0[v] or a1[v])
                            and (((mask >> v) & 1) or not a0[v])
                            and (((mask >> v) & 1) or not a1[v])
                            and (not a0[v] or not a1[v]) for v in range(n)):
                            continue
                        if all((not a0[u] or not a1[v])
                               and (not a1[u] or not a0[v]) for u, v in edges):
                            ternary_count += 1
                    assert ternary_count == 1 << (cc_selected-1)
                    checks += 1
    return checks


def check_isolation_moment():
    # Enumerate truly pairwise-independent affine hashes for p<=2.
    # This checks the probability proof, not the linear-size hash constructor.
    checks = 0
    for p in range(1, 3):
        domain = list(range(1 << p))
        for subset_mask in range(1, 1 << len(domain)):
            subset = [x for x in domain if (subset_mask >> x) & 1]
            k = len(subset)
            s = max(2, (k-1).bit_length() + 1)
            successes = total = 0
            for rows in product(domain, repeat=s):
                for offset in range(1 << s):
                    z = sum(all(((x & row).bit_count() & 1) == ((offset >> i) & 1)
                                for i, row in enumerate(rows)) for x in subset)
                    successes += z == 1
                    total += 1
            lam = Fraction(k, 1 << s)
            assert Fraction(successes, total) >= lam - lam * lam >= Fraction(3, 16)
            checks += 1
    return checks


def check_branching_program_gadget():
    checks = 0
    for internal in range(1, 4):
        n = internal + 2
        accept, reject = internal, internal+1
        options = [list(product(range(i+1, n), repeat=2)) for i in range(internal)]
        for transitions in product(*options):
            for x in product((0, 1), repeat=2):
                forest = [(i, transitions[i][x[i % 2]]) for i in range(internal)]
                assert components(n, forest) == 2
                for start in range(n):
                    state = start
                    while state < internal:
                        state = transitions[state][x[state % 2]]
                    yes = state == accept
                    selected = forest + [(start, reject)]
                    ground = [(i, t) for i, pair in enumerate(transitions) for t in pair]
                    ground += [(start, reject), (accept, reject)]
                    assert components(n, ground) == 1
                    columns = [(1 << u) ^ (1 << v) for u, v in selected]
                    assert (rank(columns) == n-1) == yes
                    # Complement activation in the cographic matroid is spanning
                    # iff this S-1-edge selected subgraph is a forest.
                    assert (rank(columns) == len(selected)) == yes
                    checks += 1
    return checks


def check_exact_cnf_cancellation():
    checks = 0
    for n in range(1, 4):
        clauses = [tuple((i+1)*sign for i, sign in enumerate(pattern) if sign)
                   for pattern in product((-1, 0, 1), repeat=n)]
        for formula in product(clauses, repeat=2):
            answer = sum(all(any(bool(x[abs(lit)-1]) == (lit > 0) for lit in clause)
                             for clause in formula) for x in product((0, 1), repeat=n))
            edges = [(2*i, 2*i+1) for i in range(n)]
            for i in range(n):
                edges.extend([(2*i, 2*n+i), (2*i+1, 2*n+i)])
            for j, clause in enumerate(formula):
                edges.extend([(2*(abs(lit)-1) + (lit > 0), 3*n+j) for lit in clause])
            count = 0
            for mask in range(1 << (3*n+2)):
                if any(((mask >> u) & 1) and ((mask >> v) & 1) for u, v in edges):
                    continue
                count += (-1) ** ((mask >> (2*n)).bit_count())
            assert count == answer
            checks += 1
    return checks


def main():
    report = {
        "status": "passed",
        "scope": "finite elementary identities only; external theorems not replayed",
        "graphic_cographic_cases": check_rank_filters(),
        "long_clause_cases": check_long_clauses(),
        **check_cycle_merge(),
        "root_gadget_cases": check_root_gadget(),
        "isolation_probability_cases": check_isolation_moment(),
        "branching_program_span_cases": check_branching_program_gadget(),
        "exact_cnf_cancellation_cases": check_exact_cnf_cancellation(),
    }
    path = Path(__file__).with_name("verification.json")
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
