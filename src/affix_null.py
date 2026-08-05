#!/usr/bin/env python3
"""
Is the affixation measure signal or collision?

STRUCTURE.md reports 42% prefix / 58% suffix from 80 affix relations, and uses
it to argue that Duhoux's 59%-prefix figure is not reproducible. That claim is
only worth making if the affix relations themselves exceed chance. With 519
short types over ~98 signs, "type B = attested type A plus an edge sign" can
arise by accident - exactly as minimal pairs did, which came in BELOW chance.

Null: resample types preserving length distribution and positional unigram
frequencies, recount affix relations.
"""
import collections, random, statistics

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402
import grid_null as gn  # noqa: E402
import typology as ty  # noqa: E402


random.seed(20260731)
TRIALS = 300


# --- Why this null matters -------------------------------------------------
# Affix relations exceed chance by ~6 sd, so affixation is real. But the
# PREFIX SHARE sits within 0.25 sd of a null whose baseline is already ~0.40.
# Distinguishing these two facts is the whole point of the test.
def counts(types) -> tuple[int, int]:
    pre, suf = ty.find_affixes(collections.Counter(types))
    return len(pre), len(suf)


def run(name, groups) -> None:
    types = sorted({tuple(t) for t in groups if len(t) > 1})
    op, os_ = counts(types)
    dists = gn.positional_dists(types)

    npre, nsuf, ntot, nratio = [], [], [], []
    for _ in range(TRIALS):
        r = gn.resample(types, dists)
        p, s = counts(r)
        npre.append(p); nsuf.append(s); ntot.append(p + s)
        if p + s:
            nratio.append(p / (p + s))

    def zscore(value: float, null_samples) -> float:
        null_mean = float(statistics.mean(null_samples))
        null_sd = float(statistics.pstdev(null_samples)) or 1e-9
        return (value - null_mean) / null_sd

    print(f'\n=== {name} ===')
    print(f'  types                    : {len(types)}')
    print(f'  {"metric":24s}{"observed":>10}{"null mean":>12}{"sd":>8}{"z":>8}')
    for lbl, o, arr in (('prefix relations', op, npre),
                        ('suffix relations', os_, nsuf),
                        ('total relations', op + os_, ntot)):
        print(f'  {lbl:24s}{o:>10}{float(statistics.mean(arr)):>12.1f}'
              f'{float(statistics.pstdev(arr)):>8.1f}{zscore(o, arr):>8.2f}')
    obs_ratio = op / (op + os_) if (op + os_) else 0
    m, sd = float(statistics.mean(nratio)), float(statistics.pstdev(nratio))
    print(f'  {"prefix share":24s}{obs_ratio:>10.3f}{m:>12.3f}{sd:>8.3f}'
          f'{(obs_ratio - m)/(sd or 1e-9):>8.2f}')
    p = (sum(1 for v in ntot if v >= op + os_) + 1) / (TRIALS + 1)
    print(f'  p(null >= observed total): {p:.3f}')


def main() -> None:
    g = json_load('data/signgroups_by_genre.json')
    print(f'AFFIX NULL MODEL ({TRIALS} trials)')
    run('administrative', [tuple(t) for t in g['administrative']])
    run('religious', [tuple(t) for t in g['religious']])


if __name__ == '__main__':
    main()
