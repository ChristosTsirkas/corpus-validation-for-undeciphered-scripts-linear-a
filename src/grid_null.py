#!/usr/bin/env python3
"""
Stage 2d, step 2: is the minimal-pair count SIGNAL or COLLISION?

609 minimal pairs in the administrative corpus looks encouraging until you note
that 514 of the 514 distinct substitutions are attested once or twice. With 519
short types drawn from a ~98-sign inventory, accidental near-identity is
expected. A paradigm would show specific sign pairs alternating repeatedly in
many environments; chance shows a flat, near-complete substitution graph.

Null model: resample types preserving (a) the length distribution and (b) the
positional unigram distribution of signs, then count minimal pairs. If the
observed count sits inside the null distribution, the pairs carry no paradigm
information and no grid is recoverable.
"""
import collections, random, statistics

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402
import grid_feasibility as gf  # noqa: E402


random.seed(20260731)
N_TRIALS = 300


# --- Null model ------------------------------------------------------------
# Preserves length distribution AND the positional frequency of each sign, so a
# 'finding' that merely reflects which signs are common where cannot survive.
# This is the null used throughout the project.
def positional_dists(types) -> dict[tuple[int, int], tuple[list[str], list[int]]]:
    """P(sign | position, length) from the observed corpus."""
    d = collections.defaultdict(collections.Counter)
    for t in types:
        for i, s in enumerate(t):
            d[(len(t), i)][s] += 1
    out = {}
    for k, c in d.items():
        signs, weights = zip(*c.items())
        out[k] = (list(signs), list(weights))
    return out


def resample(types, dists) -> list[tuple[str, ...]]:
    new = set()
    for t in types:
        n = len(t)
        attempt = []
        for i in range(n):
            signs, w = dists[(n, i)]
            attempt.append(random.choices(signs, weights=w, k=1)[0])
        new.add(tuple(attempt))
    return sorted(new)


def stats_for(types) -> tuple[int, int, int, int]:
    pairs = gf.minimal_pairs(types)
    subs = collections.Counter(tuple(sorted((x, y))) for _, _, _, x, y in pairs)
    repeated = sum(1 for v in subs.values() if v >= 2)
    maxrep = max(subs.values()) if subs else 0
    return len(pairs), len(subs), repeated, maxrep


def run(name, groups) -> tuple[tuple[int, int, int, int], list[int]]:
    types = sorted({tuple(t) for t in groups if len(t) > 1})
    obs = stats_for(types)
    dists = positional_dists(types)

    null = [stats_for(resample(types, dists)) for _ in range(N_TRIALS)]
    npairs = [x[0] for x in null]
    nrep = [x[2] for x in null]
    nmax = [x[3] for x in null]

    def zscore(value: float, null_samples) -> float:
        null_mean = float(statistics.mean(null_samples))
        null_sd = float(statistics.pstdev(null_samples)) or 1e-9
        return (value - null_mean) / null_sd

    print(f'\n=== {name} ===')
    print(f'  observed types           : {len(types)}')
    print(f'  {"metric":26s}{"observed":>10}{"null mean":>12}{"null sd":>9}{"z":>8}')
    for lbl, o, arr in (('minimal pairs', obs[0], npairs),
                        ('substitutions repeated>1', obs[2], nrep),
                        ('max repeats of one sub', obs[3], nmax)):
        m, s = float(statistics.mean(arr)), float(statistics.pstdev(arr))
        print(f'  {lbl:26s}{o:>10}{m:>12.1f}{s:>9.1f}{zscore(o, arr):>8.2f}')
    p = sum(1 for v in npairs if v >= obs[0]) / len(npairs)
    print(f'  p(null >= observed pairs): {p:.3f}')
    return obs, npairs


def main() -> None:
    g = json_load('data/signgroups_by_genre.json')
    print('NULL MODEL: minimal pairs against positional resampling '
          f'({N_TRIALS} trials)')
    run('administrative', [tuple(t) for t in g['administrative']])
    run('religious', [tuple(t) for t in g['religious']])


if __name__ == '__main__':
    main()
