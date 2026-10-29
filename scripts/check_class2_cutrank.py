#!/usr/bin/env python3
"""Reproducible tests for Checkpoints 26--27 (standard library only).

Checks exact #SAT for class-two reordering, with arbitrary first-sweep
choices g_i^0/g_i^1 and arbitrary deterministic second-sweep transitions.
Also checks the increasing-oscillation permutation family.
"""
from collections import defaultdict
from itertools import product
from random import Random


ELEMENTS = list(product((0, 1), repeat=3))
INDEX = {g: i for i, g in enumerate(ELEMENTS)}
IDENTITY = (0, 0, 0)
CENTER = (0, 0, 1)


def multiply(g, h):
    a, b, c = g
    d, e, f = h
    return (a ^ d, b ^ e, c ^ f ^ (a & e))


def left_permutation(g):
    return tuple(INDEX[multiply(g, s)] for s in ELEMENTS)


Z_ACTION = left_permutation(CENTER)


def commutator_exponent(g, h):
    return (g[0] & h[1]) ^ (g[1] & h[0])


def rank_binary(rows):
    basis = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = row
                break
            row ^= basis[pivot]
    return len(basis)


def quadratic_data(first, order):
    """Coefficients of the central correction in second-pass read order."""
    p = len(first)
    linear = [0] * p
    rows = [0] * p
    constant = 0
    for t in range(p):
        for s in range(t + 1, p):
            if order[t] < order[s]:
                continue
            left, right = first[order[t]], first[order[s]]
            c00 = commutator_exponent(left[0], right[0])
            c10 = commutator_exponent(left[1], right[0])
            c01 = commutator_exponent(left[0], right[1])
            c11 = commutator_exponent(left[1], right[1])
            constant ^= c00
            linear[t] ^= c10 ^ c00
            linear[s] ^= c01 ^ c00
            if c11 ^ c10 ^ c01 ^ c00:
                rows[t] |= 1 << s
    rank = max(
        rank_binary([rows[i] >> t for i in range(t)])
        for t in range(p + 1)
    )
    return constant, linear, rows, rank


def count_via_cutrank(first, second, order, start, accepts):
    p = len(first)
    width = len(ELEMENTS)
    actions = [
        [left_permutation(first[i][bit]) for bit in (0, 1)]
        for i in range(p)
    ]
    q0, linear, rows, rank = quadratic_data(first, order)
    total = 0
    for guessed_middle in range(width):
        dp = {(start, guessed_middle, 0, q0): 1}
        for t, i in enumerate(order):
            next_dp = defaultdict(int)
            for (u, v, signature, q), count in dp.items():
                for bit in (0, 1):
                    new_u = actions[i][bit][u]
                    new_v = second[i][bit][v]
                    new_q = q ^ (bit & (linear[t] ^ ((signature >> t) & 1)))
                    new_signature = (
                        signature ^ (rows[t] if bit else 0)
                    ) & ~((1 << (t + 1)) - 1)
                    next_dp[new_u, new_v, new_signature, new_q] += count
            dp = next_dp
        total += sum(
            count for (u, v, _, q), count in dp.items()
            if guessed_middle == (Z_ACTION[u] if q else u)
            and v in accepts
        )
    return total, rank


def exhaustive_count(first, second, order, start, accepts):
    actions = [
        [left_permutation(first[i][bit]) for bit in (0, 1)]
        for i in range(len(first))
    ]
    total = 0
    for assignment in product((0, 1), repeat=len(first)):
        state = start
        for i, bit in enumerate(assignment):
            state = actions[i][bit][state]
        for i in order:
            state = second[i][assignment[i]][state]
        total += state in accepts
    return total


def oscillation(k):
    return tuple(
        [1] + [v for j in range(1, k) for v in (2*j+1, 2*j-2)]
        + [2*k-2]
    )


def is_simple(perm):
    n = len(perm)
    for a in range(n):
        lo = hi = perm[a]
        for b in range(a + 1, n):
            lo, hi = min(lo, perm[b]), max(hi, perm[b])
            if b - a + 1 < n and hi - lo == b - a:
                return False
    return True


def main():
    rng = Random(20261029)
    for trial in range(400):
        p = rng.randint(1, 8)
        first = [
            (IDENTITY if trial < 200 else rng.choice(ELEMENTS),
             rng.choice(ELEMENTS))
            for _ in range(p)
        ]
        second = [
            [tuple(rng.randrange(8) for _ in range(8)) for bit in (0, 1)]
            for i in range(p)
        ]
        order = list(range(p))
        rng.shuffle(order)
        start = rng.randrange(8)
        accepts = {s for s in range(8) if rng.randrange(2)}
        observed, _ = count_via_cutrank(first, second, order, start, accepts)
        expected = exhaustive_count(first, second, order, start, accepts)
        assert observed == expected, (trial, observed, expected)

    a, b = (1, 0, 0), (0, 1, 0)
    for k in range(3, 25):
        p = 2 * k
        order = oscillation(k)
        first = [
            (IDENTITY, a if i % 2 == 0 else b)
            for i in range(p)
        ]
        _, _, _, rank = quadratic_data(first, order)
        assert sorted(order) == list(range(p))
        assert is_simple(order)
        assert rank == 2, (p, rank)

    print("PASS: 400 random exact-count tests and 22 prime-order cutrank tests")


if __name__ == "__main__":
    main()
