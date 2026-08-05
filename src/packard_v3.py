#!/usr/bin/env python3
"""
Packard replication v3 - split by his 2= / 3= categories (Table 13).

Packard's Table 13 splits each positional class by how many signs are SHARED:
  Final  2=  X-Y-A  / X-Y-B        (3-sign words)   ratio 1.8, weight 2
  Final  3=  W-X-Y-A / W-X-Y-B     (4-sign words)   ratio 9,   weight 10
  Medial 2=  X-A-Y  / X-B-Y                          ratio 2,   weight 2
  Medial 3=  (4-sign)                                ratio 9,   weight 10
  Initial 2= A-X-Y  / B-X-Y                          ratio 1.1, weight 0
  Initial 3= A-W-X-Y / B-W-X-Y                       ratio 9,   weight 10

Our v2 implemented ONLY the 2= categories. Packard weights those 2, 2 and 0.
"""
import collections, itertools, random, statistics

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402
import packard as pk  # noqa: E402


random.seed(20260731)
TRIALS = 4000


def cats(types) -> dict[str, list[tuple[str, str]]]:
    """Return dict of category -> list of (signA, signB)."""
    out = collections.defaultdict(list)
    for n_shared, wordlen in ((2, 3), (3, 4)):
        by = collections.defaultdict(list)
        # FINAL: first n_shared identical, last differs
        for t in types:
            if len(t) == wordlen:
                by[t[:n_shared]].append(t)
        for ms in by.values():
            for a, b in itertools.combinations(sorted(ms), 2):
                if a[-1] != b[-1]:
                    out[f'final {n_shared}='].append((a[-1], b[-1]))
        # INITIAL: last n_shared identical, first differs
        by = collections.defaultdict(list)
        for t in types:
            if len(t) == wordlen:
                by[t[-n_shared:]].append(t)
        for ms in by.values():
            for a, b in itertools.combinations(sorted(ms), 2):
                if a[0] != b[0]:
                    out[f'initial {n_shared}='].append((a[0], b[0]))
        # MEDIAL: all but one interior position identical
        by = collections.defaultdict(list)
        for t in types:
            if len(t) == wordlen:
                by[(t[0],) + t[2:]].append(t)      # position 1 varies
        for ms in by.values():
            for a, b in itertools.combinations(sorted(ms), 2):
                if a[1] != b[1]:
                    out[f'medial {n_shared}='].append((a[1], b[1]))
    return out


def score(pairs, vmap) -> tuple[int, int]:
    c = t = 0
    for x, y in pairs:
        if x not in vmap or y not in vmap or x == y:
            continue
        cx, vx = vmap[x]; cy, vy = vmap[y]
        t += 1
        if (cx and cx == cy) or (vx and vx == vy):
            c += 1
    return c, t


def main() -> None:
    g = json_load('data/signgroups_by_genre.json')
    types = sorted({tuple(t) for t in
                    [tuple(x) for x in g['administrative'] + g['religious']]
                    if len(t) > 1})
    categories = cats(types)
    vmap = pk.build_values()
    signs = list(vmap)
    bands = pk.freq_bands(types, signs)

    packard_published = {'final 2=': (7, 3.9, 1.8, 2), 'final 3=': (3, 0.33, 9, 10),
               'medial 2=': (2, 1.0, 2.0, 2), 'medial 3=': (1, 0.11, 9, 10),
               'initial 2=': (2, 1.8, 1.1, 0), 'initial 3=': (3, 0.33, 9, 10)}

    print('PACKARD TABLE 13 COMPARISON  (counts of CONFIRMATORY alternations)')
    print(f'{"category":12s}{"ourN":>6}{"ourConf":>8}{"nullConf":>9}{"ratio":>7}'
          f'  |{"PkLinB":>7}{"PkAvg":>7}{"PkRatio":>8}{"wt":>4}')
    for cat in ('final 2=', 'final 3=', 'medial 2=', 'medial 3=',
                'initial 2=', 'initial 3='):
        pairs = categories.get(cat, [])
        obs, n = score(pairs, vmap)
        if n == 0:
            print(f'{cat:12s}{0:>6}{"-":>8}{"-":>9}{"-":>7}  |'
                  f'{packard_published[cat][0]:>7}{packard_published[cat][1]:>7}{packard_published[cat][2]:>8}'
                  f'{packard_published[cat][3]:>4}')
            continue
        null = []
        for _ in range(TRIALS):
            perm = {}
            for band in bands:
                bv = [vmap[x] for x in band]
                random.shuffle(bv)
                perm.update(dict(zip(band, bv)))
            null.append(score(pairs, perm)[0])
        m = float(statistics.mean(null))
        r = obs / m if m else float('inf')
        p, av, pr, wt = packard_published[cat]
        print(f'{cat:12s}{n:>6}{obs:>8}{m:>9.2f}{r:>7.2f}  |{p:>7}{av:>7}{pr:>8}{wt:>4}')

    print('\nNOTE: Packard weights initial 2= at ZERO and the 2= classes at 2,')
    print('      against 10 for every 3= class. Our v2 tested only 2= classes.')


if __name__ == '__main__':
    main()
