#!/usr/bin/env python3
"""Exact small-instance tests for checkpoint 25's observable quotient.

Run: python3 scripts/check_observable_quotient.py
Standard library only. These tests are not a novelty claim.
"""
import itertools
import random


def classes(keys):
    ids = {}
    out = []
    for key in keys:
        if key not in ids:
            ids[key] = len(ids)
        out.append(ids[key])
    return tuple(out)


def observable_quotient(first, second, order, accepting):
    width = len(first[0][0])
    part = tuple(int(s in accepting) for s in range(width))
    for i in reversed(order):
        part = classes([
            (part[second[i][0][s]], part[second[i][1][s]])
            for s in range(width)
        ])
    behavior = part
    while True:
        nxt = classes([
            (part[s], tuple(
                part[first[i][bit][s]]
                for i in range(len(first)) for bit in (0, 1)
            )) for s in range(width)
        ])
        if len(set(nxt)) == len(set(part)):
            part = nxt
            break
        part = nxt
    representatives = {}
    for s, cls in enumerate(part):
        representatives.setdefault(cls, s)
    d = len(representatives)
    quotient_maps = {
        (i, bit): tuple(
            part[first[i][bit][representatives[c]]]
            for c in range(d)
        )
        for i in range(len(first)) for bit in (0, 1)
    }
    commuting = all(
        quotient_maps[i, bit][quotient_maps[j, value][s]] ==
        quotient_maps[j, value][quotient_maps[i, bit][s]]
        for i in range(len(first))
        for j in range(i + 1, len(first))
        for bit in (0, 1) for value in (0, 1)
        for s in range(d)
    )
    return behavior, part, representatives, quotient_maps, commuting


def count_if_certified(first, second, order, initial, accepting):
    _, part, reps, maps, commuting = observable_quotient(
        first, second, order, accepting
    )
    if not commuting:
        return None
    total = 0
    for target, state in reps.items():
        dp = {(part[initial], state): 1}
        for i in order:
            nxt = {}
            for (u, v), count in dp.items():
                for bit in (0, 1):
                    key = maps[i, bit][u], second[i][bit][v]
                    nxt[key] = nxt.get(key, 0) + count
            dp = nxt
        total += sum(
            count for (u, v), count in dp.items()
            if u == target and v in accepting
        )
    return total


def brute(first, second, order, initial, accepting):
    count = 0
    for assignment in itertools.product((0, 1), repeat=len(first)):
        state = initial
        for i, bit in enumerate(assignment):
            state = first[i][bit][state]
        for i in order:
            state = second[i][assignment[i]][state]
        count += state in accepting
    return count


def main():
    rng = random.Random(20261029)
    certified = 0
    for _ in range(3000):
        p, w = rng.randint(1, 7), rng.randint(2, 6)
        first = [
            [tuple(rng.randrange(w) for _ in range(w)) for _ in range(2)]
            for _ in range(p)
        ]
        second = [
            [tuple(rng.randrange(w) for _ in range(w)) for _ in range(2)]
            for _ in range(p)
        ]
        order = list(range(p))
        rng.shuffle(order)
        initial = rng.randrange(w)
        accepting = {j for j in range(w) if rng.randrange(2)}
        result = count_if_certified(
            first, second, order, initial, accepting
        )
        if result is not None:
            certified += 1
            assert result == brute(first, second, order, initial, accepting)

    for k in range(2, 7):
        p, w = 2 * k, 6
        first = []
        for i in range(p):
            permutation = (1, 0, 2) if i % 2 == 0 else (0, 2, 1)
            first.append([
                tuple(range(w)),
                tuple((q ^ 1) * 3 + permutation[r]
                      for q in (0, 1) for r in range(3))
            ])
        second = []
        for i in range(p):
            second.append([
                tuple(range(w)),
                tuple((q ^ int(i % 2 == 1)) * 3 + r
                      for q in (0, 1) for r in range(3))
            ])
        order = list(range(1, p, 2)) + list(range(0, p, 2))
        accepting = {3, 4, 5}
        _, partition, _, _, holds = observable_quotient(
            first, second, order, accepting
        )
        assert holds and len(set(partition)) == 2
        assert count_if_certified(
            first, second, order, 0, accepting
        ) == 2 ** (p - 1)
        assert any(
            first[i][1][first[j][1][s]] !=
            first[j][1][first[i][1][s]]
            for i in range(p) for j in range(i + 1, p)
            for s in range(w)
        )

    print(f"PASS: 3000 random programs ({certified} certified), "
          "plus six-state noncommuting examples p=4,6,8,10,12")


if __name__ == "__main__":
    main()
