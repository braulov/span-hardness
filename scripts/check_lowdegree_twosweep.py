#!/usr/bin/env python3
"""Check deterministic low-degree endpoint / read-once-BP intersection.

Python stdlib only. Test family: UT4(F2) first sweep on eight affine states,
arbitrary potentially irreversible second sweep in random variable order.
"""
from itertools import combinations, product
from random import Random


def ut4_map(e):
    e12, e13, e14, e23, e24, e34 = e
    return tuple(
        ((a ^ (e12 & b) ^ (e13 & c) ^ e14) << 2)
        | ((b ^ (e23 & c) ^ e24) << 1) | (c ^ e34)
        for a, b, c in product((0, 1), repeat=3)
    )


def evaluate_first(first, mask):
    state = 0
    for i, pair in enumerate(first):
        state = pair[(mask >> i) & 1][state]
    return state


def monomials(p, degree):
    subs = []
    for j in range(degree + 1):
        subs += [
            sum(1 << i for i in group)
            for group in combinations(range(p), j)
        ]
    return subs, {S: k for k, S in enumerate(subs)}


def endpoint_coefficients(first, subs):
    """Mobius inversion using ONLY assignments of weight <= degree."""
    observed = {S: evaluate_first(first, S) for S in subs}
    result = [0] * len(first[0][0])
    for j, S in enumerate(subs):
        parity = [0] * len(result)
        T = S
        while True:
            parity[observed[T]] ^= 1
            if not T:
                break
            T = (T - 1) & S
        for state in range(len(result)):
            if parity[state]:
                result[state] |= 1 << j
    return result


def insert(basis, vector):
    while vector:
        pivot = vector.bit_length() - 1
        if pivot in basis:
            vector ^= basis[pivot]
        else:
            basis[pivot] = vector
            break


def intersects(second, order, start, accepts, coefficients, subs, index):
    p = len(second)
    dps = {start: {0: 1 << index[0]}}
    containing = [
        [(j, index[S ^ (1 << i)])
         for j, S in enumerate(subs) if S & (1 << i)]
        for i in range(p)
    ]
    for i in order:
        next_dp = {}
        for state, basis in dps.items():
            for vector in basis.values():
                for bit in (0, 1):
                    new = vector
                    if bit:
                        for j, k in containing[i]:
                            if (vector >> k) & 1:
                                new |= 1 << j
                    dest = second[i][bit][state]
                    insert(next_dp.setdefault(dest, {}), new)
        dps = next_dp
    return any(
        (vec & coefficients).bit_count() & 1
        for state, basis in dps.items()
        if state in accepts for vec in basis.values()
    )


def solve(first, second, order, accepts):
    subs, index = monomials(len(first), min(6, len(first)))
    coefficients = endpoint_coefficients(first, subs)
    return any(
        intersects(second, order, state, accepts,
                   coefficients[state], subs, index)
        for state in range(8)
    )


def brute(first, second, order, accepts):
    for mask in range(1 << len(first)):
        state = evaluate_first(first, mask)
        for i in order:
            state = second[i][(mask >> i) & 1][state]
        if state in accepts:
            return True
    return False


def main():
    rng = Random(20261030)
    for p in range(1, 8):
        for trial in range(13):
            first = [
                (ut4_map(tuple(rng.randrange(2) for _ in range(6))),
                 ut4_map(tuple(rng.randrange(2) for _ in range(6))))
                for _ in range(p)
            ]
            second = [
                (tuple(rng.randrange(8) for _ in range(8)),
                 tuple(rng.randrange(8) for _ in range(8)))
                for _ in range(p)
            ]
            order = list(range(p))
            rng.shuffle(order)
            accepts = {state for state in range(8) if rng.randrange(2)}
            got = solve(first, second, order, accepts)
            expected = brute(first, second, order, accepts)
            assert got == expected, (p, trial, got, expected)
    print("PASS: 91 random UT4 / arbitrary-second two-sweep SAT tests")


if __name__ == "__main__":
    main()
