#!/usr/bin/env python3
"""
Packard replication, CORRECTED against the primary source.

Packard (1974, 71) defines the alternation set explicitly. More than 100 groups
of Linear A words are involved in alternations superficially resembling
inflection or orthographic variation, collected in Appendix A in three
categories:

  (1) pairs where the first two signs are identical but the third is not
      e.g. 30.74.53 / 30.74.54        -> alternation at the END
  (2) pairs where the last two signs are identical but not the beginning
      e.g. 98.101.60 / 29.97.101.60   -> alternation at the BEGINNING
  (3) cases where the first and third signs are identical but the second differs
      e.g. 103.54.86 / 103.72.86      -> alternation INTERNAL

These map onto his chapter sections "Alternation at the End of Words",
"Alternation at the Beginning of Words", "Alternation Internal to Words".

His confirmatory examples are KI.RE.TA2 / KI.RI.TA2 and DA.TA.RA / DA.TA.RE:
in both, the alternating signs share a consonant and differ in vowel. Under
Kober's grid logic (which Packard sets out on p. 71: rows share an unknown
consonant, columns share an unknown vowel), an alternation is confirmatory if
the two signs sit in the same row OR the same column - i.e. share C or share V.

WHAT WAS WRONG BEFORE
`grid_feasibility.minimal_pairs()` required EQUAL LENGTH and exactly one
differing position. That generates categories 1 and 3, and category 2 only
when lengths match. Packard's category 2 explicitly admits unequal lengths
(3 signs against 4), which our earlier run never produced.
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


def packard_pairs(types) -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str]], list[tuple[tuple[str, ...], tuple[str, ...]]]]:
    """Generate Packard's three categories. Returns (category, sign_a, sign_b)
    for single-sign oppositions, plus a separate list of unequal-length
    category-2 pairs (prefixation), which cannot be scored as sign-vs-sign."""
    tset = sorted(set(types))
    cat1, cat2, cat3, cat2_unequal = [], [], [], []

    # (1) first two identical, third differs  -> requires len >= 3
    by_head = collections.defaultdict(list)
    for t in tset:
        if len(t) >= 3:
            by_head[t[:2]].append(t)
    for members in by_head.values():
        for a, b in itertools.combinations(members, 2):
            if len(a) == len(b) == 3 and a[2] != b[2]:
                cat1.append((a[2], b[2]))

    # (2) last two identical, beginning differs
    by_tail = collections.defaultdict(list)
    for t in tset:
        if len(t) >= 3:
            by_tail[t[-2:]].append(t)
    for members in by_tail.values():
        for a, b in itertools.combinations(members, 2):
            pa, pb = a[:-2], b[:-2]
            if pa == pb:
                continue
            if len(pa) == len(pb) == 1:
                cat2.append((pa[0], pb[0]))
            else:
                cat2_unequal.append((a, b))

    # (3) first and third identical, second differs -> len == 3
    by_frame = collections.defaultdict(list)
    for t in tset:
        if len(t) == 3:
            by_frame[(t[0], t[2])].append(t)
    for members in by_frame.values():
        for a, b in itertools.combinations(members, 2):
            if a[1] != b[1]:
                cat3.append((a[1], b[1]))

    return cat1, cat2, cat3, cat2_unequal


def confirmatory(pairs, vmap) -> tuple[float, int]:
    conf = tot = 0
    for x, y in pairs:
        if x not in vmap or y not in vmap or x == y:
            continue
        cx, vx = vmap[x]; cy, vy = vmap[y]
        tot += 1
        if (cx and cx == cy) or (vx and vx == vy):
            conf += 1
    return (conf / tot if tot else 0.0), tot


def run(name, groups) -> None:
    types = sorted({tuple(t) for t in groups if len(t) > 1})
    c1, c2, c3, c2u = packard_pairs(types)
    allp = c1 + c2 + c3
    vmap = pk.build_values()

    print(f'\n=== {name} ===')
    print(f'  types {len(types)}')
    print(f'  cat 1 (end)      : {len(c1)}')
    print(f'  cat 2 (beginning): {len(c2)}   [+ {len(c2u)} unequal-length, prefixation]')
    print(f'  cat 3 (internal) : {len(c3)}')
    print(f'  total single-sign oppositions: {len(allp)}')

    obs, n = confirmatory(allp, vmap)
    if n < 30:
        print('  -> too few testable')
        return
    print(f'  testable (both signs valued): {n}')
    print(f'  observed confirmatory rate  : {obs:.4f}')

    signs = list(vmap); vals = [vmap[s] for s in signs]
    null_a = []
    for _ in range(TRIALS):
        random.shuffle(vals)
        null_a.append(confirmatory(allp, dict(zip(signs, vals)))[0])
    m, s = float(statistics.mean(null_a)), float(statistics.pstdev(null_a))
    p = (sum(1 for v in null_a if v >= obs) + 1) / (TRIALS + 1)
    print(f'  null unconstrained : {m:.4f} +/- {s:.4f}  z={(obs-m)/s:+.2f}  p={p:.4f}'
          f'   ratio {obs/m:.2f}:1')

    bands = pk.freq_bands(types, signs)
    null_b = []
    for _ in range(TRIALS):
        perm = {}
        for band in bands:
            bv = [vmap[x] for x in band]
            random.shuffle(bv)
            perm.update(dict(zip(band, bv)))
        null_b.append(confirmatory(allp, perm)[0])
    m2, s2 = float(statistics.mean(null_b)), float(statistics.pstdev(null_b))
    p2 = (sum(1 for v in null_b if v >= obs) + 1) / (TRIALS + 1)
    print(f'  null freq-banded   : {m2:.4f} +/- {s2:.4f}  z={(obs-m2)/s2:+.2f}  p={p2:.4f}'
          f'   ratio {obs/m2:.2f}:1')
    print('  [Packard 1974: 2:1 | Pope & Raison 1978: 3:1]')

    # per-category breakdown, since his chapter treats them separately
    for lbl, cat in (('end', c1), ('beginning', c2), ('internal', c3)):
        o, k = confirmatory(cat, vmap)
        if k >= 20:
            print(f'    {lbl:10s} n={k:4d}  confirmatory {o:.3f}')


def main() -> None:
    g = json_load('data/signgroups_by_genre.json')
    print(f"PACKARD REPLICATION v2 - his three categories, {TRIALS} permutations")
    run('administrative', [tuple(t) for t in g['administrative']])
    run('combined', [tuple(t) for t in g['administrative'] + g['religious']])


if __name__ == '__main__':
    main()
