#!/usr/bin/env python3
"""
Stage 2d, step 1: FEASIBILITY TEST for an alternation grid.

Before attempting a Ventris-style grid we need to know whether the corpus can
support one. The grid is built from minimal pairs: attested types of equal
length differing in exactly one position. Each such pair asserts that the two
differing signs can occupy the same slot in the same environment.

If the count is small, no grid is recoverable and this stage stops here rather
than producing a sparse lattice and over-reading it.
"""
import collections, itertools

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402


def load() -> dict[str, list[tuple[str, ...]]]:
    g = json_load('data/signgroups_by_genre.json')
    return {k: [tuple(x) for x in v] for k, v in g.items()}


def minimal_pairs(types) -> list[tuple[int, tuple[str, ...], tuple[str, ...], str, str]]:
    """Pairs differing in exactly one position, same length."""
    by_len = collections.defaultdict(list)
    for t in types:
        by_len[len(t)].append(t)
    pairs = []
    for n, group in by_len.items():
        if n < 2:
            continue
        # index by (position blanked) signature for O(n * len) lookup
        for pos in range(n):
            buckets = collections.defaultdict(list)
            for t in group:
                key = t[:pos] + ('*',) + t[pos + 1:]
                buckets[key].append(t)
            for key, members in buckets.items():
                if len(members) < 2:
                    continue
                for a, b in itertools.combinations(sorted(members), 2):
                    pairs.append((pos, a, b, a[pos], b[pos]))
    return pairs


def report(name, groups) -> tuple[list[tuple[int, tuple[str, ...], tuple[str, ...], str, str]], collections.Counter[tuple[str, str]], list[set[str]]] | None:
    multi = [t for t in groups if len(t) > 1]
    types = sorted(set(multi))
    pairs = minimal_pairs(types)

    print(f'\n=== {name} ===')
    print(f'  multi-sign tokens        : {len(multi)}')
    print(f'  distinct types           : {len(types)}')
    print(f'  minimal pairs            : {len(pairs)}')
    if not pairs:
        return None

    # substitution classes: which signs alternate with which
    subs = collections.Counter()
    for _, _, _, x, y in pairs:
        subs[tuple(sorted((x, y)))] += 1
    print(f'  distinct substitutions   : {len(subs)}')
    print(f'  signs involved           : '
          f'{len({s for k in subs for s in k})}')

    # how many substitutions are attested more than once?
    repeated = {k: v for k, v in subs.items() if v >= 2}
    print(f'  substitutions attested >1: {len(repeated)}')

    # connectivity: a grid needs the substitution graph to be connected
    adj = collections.defaultdict(set)
    for (x, y) in subs:
        adj[x].add(y); adj[y].add(x)
    seen, comps = set(), []
    for s in adj:
        if s in seen:
            continue
        stack, comp = [s], set()
        while stack:
            u = stack.pop()
            if u in comp:
                continue
            comp.add(u); seen.add(u)
            stack.extend(adj[u] - comp)
        comps.append(comp)
    comps.sort(key=len, reverse=True)
    print(f'  substitution graph       : {len(comps)} components, '
          f'largest = {len(comps[0]) if comps else 0} signs')

    print('\n  most frequent substitutions:')
    for (x, y), n in subs.most_common(12):
        print(f'    {x:9s} ~ {y:9s}  {n}')

    return pairs, subs, comps


def main() -> None:
    g = load()
    print('FEASIBILITY TEST: can this corpus support an alternation grid?')
    ra = report('administrative', g['administrative'])
    rr = report('religious', g['religious'])

    print('\n\n=== VERDICT ===')
    for name, r in (('administrative', ra), ('religious', rr)):
        if not r:
            print(f'  {name}: no minimal pairs, grid not recoverable')
            continue
        pairs, subs, comps = r
        rep = sum(1 for v in subs.values() if v >= 2)
        print(f'  {name}: {len(pairs)} pairs, {len(subs)} substitutions, '
              f'{rep} repeated, largest component {len(comps[0])} signs')


if __name__ == '__main__':
    main()
