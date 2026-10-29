#!/usr/bin/env python3
"""Brute-force audits for checkpoint 24: commuting-sweep two-pass BP #SAT.

Uses only the Python standard library. This is a regression test, not a
proof of the recurrence or an empirical runtime benchmark.
"""
import itertools
import random


def power(perm, exponent):
    out = tuple(range(len(perm)))
    for _ in range(exponent):
        out = tuple(perm[j] for j in out)
    return out


def brute(a, b, order, start, accepts):
    total = 0
    for bits in itertools.product((0, 1), repeat=len(a)):
        state = start
        for i in range(len(a)):
            state = a[i][bits[i]][state]
        for i in order:
            state = b[i][bits[i]][state]
        total += state in accepts
    return total


def commuting_first(a, b, order, start, accepts):
    width = len(a[0][0])
    total = 0
    for middle in range(width):
        dp = {(start, middle): 1}
        for i in order:
            nxt = {}
            for (u, v), ways in dp.items():
                for bit in (0, 1):
                    key = a[i][bit][u], b[i][bit][v]
                    nxt[key] = nxt.get(key, 0) + ways
            dp = nxt
        total += sum(
            ways for (u, v), ways in dp.items()
            if u == middle and v in accepts
        )
    return total


def commuting_segments(a, b, order, start, accepts, exceptional):
    n = len(a)
    width = len(a[0][0])
    exceptional = sorted(exceptional)
    exceptional_set = set(exceptional)
    segment = {}
    seg = 0
    for i in range(n):
        if i in exceptional_set:
            seg += 1
        else:
            segment[i] = seg
    q = len(exceptional)
    total = 0
    for choices in itertools.product((0, 1), repeat=q):
        fixed = dict(zip(exceptional, choices))
        # Guesses are starts of segments 1..q, then middle state.
        for guessed in itertools.product(range(width), repeat=q + 1):
            starts = (start,) + guessed[:-1]
            middle = guessed[-1]
            dp = {(starts, middle): 1}
            for i in order:
                next_dp = {}
                for (curr, v), ways in dp.items():
                    for bit in ((fixed[i],) if i in fixed else (0, 1)):
                        updated = list(curr)
                        if i not in fixed:
                            j = segment[i]
                            updated[j] = a[i][bit][updated[j]]
                        key = (tuple(updated), b[i][bit][v])
                        next_dp[key] = next_dp.get(key, 0) + ways
                dp = next_dp
            for (curr, v), ways in dp.items():
                if v not in accepts or curr[-1] != middle:
                    continue
                if all(
                    starts[j + 1] == a[idx][fixed[idx]][curr[j]]
                    for j, idx in enumerate(exceptional)
                ):
                    total += ways
    return total


def main():
    rng = random.Random(20261029)
    for trial in range(2000):
        w, p = rng.randint(2, 6), rng.randint(1, 8)
        cycle = tuple((j + 1) % w for j in range(w))
        a = [
            (power(cycle, rng.randrange(w)), power(cycle, rng.randrange(w)))
            for _ in range(p)
        ]
        b = [
            (tuple(rng.randrange(w) for _ in range(w)),
             tuple(rng.randrange(w) for _ in range(w)))
            for _ in range(p)
        ]
        order = list(range(p))
        rng.shuffle(order)
        start = rng.randrange(w)
        accepts = {j for j in range(w) if rng.randrange(2)}
        assert commuting_first(a, b, order, start, accepts) == brute(
            a, b, order, start, accepts
        ), trial

    for trial in range(200):
        w, p = rng.randint(2, 4), rng.randint(2, 7)
        exceptions = set(rng.sample(range(p), rng.randint(0, min(2, p))))
        a = [None] * p
        begin = 0
        for j in range(p + 1):
            if j in exceptions or j == p:
                perm = list(range(w))
                rng.shuffle(perm)
                for i in range(begin, j):
                    a[i] = (power(perm, rng.randrange(1, w + 1)),
                            power(perm, rng.randrange(1, w + 1)))
                if j < p:
                    a[j] = (tuple(rng.randrange(w) for _ in range(w)),
                            tuple(rng.randrange(w) for _ in range(w)))
                begin = j + 1
        b = [
            (tuple(rng.randrange(w) for _ in range(w)),
             tuple(rng.randrange(w) for _ in range(w)))
            for _ in range(p)
        ]
        order = list(range(p))
        rng.shuffle(order)
        start = rng.randrange(w)
        accepts = {j for j in range(w) if rng.randrange(2)}
        assert commuting_segments(a, b, order, start, accepts, exceptions) == brute(
            a, b, order, start, accepts
        ), trial

    print("PASS: 2000 commuting-first and 200 commuting-segment exact #SAT checks")


if __name__ == "__main__":
    main()
