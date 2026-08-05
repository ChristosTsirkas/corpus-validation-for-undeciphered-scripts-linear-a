#!/usr/bin/env python3
# noinspection GrazieInspection
"""
Replication of Packard (1974), 'confirmatory alternations'.

METHOD, AS ORIGINALLY RUN
Packard (A Study of the Minoan Linear A Tablets, Harvard 1967; Minoan Linear A,
1974) built NINE fictitious decipherments, redistributing Linear B phonetic
values among Linear A signs so that no sign kept its value, re-allocating only
within the same frequency band. He then compared the rate of 'confirmatory
alternations' under the true Ventris values against the average of the nine.
Result: just over 2:1 in favor of the Ventris values. Pope & Raison (Etudes
minoennes I, 1978, 24-25) adjusted for context and reported 3:1.

That is a permutation test with n = 9. This script re-runs it with n = 4000 and
reports an effect size and a p-value, which the original could not.

STATISTIC
A minimal pair is two attested types of equal length differing at exactly one
position (already computed for the grid feasibility test). The alternating pair
of signs is CONFIRMATORY if, under the value assignment, the two signs share a
consonant or share a vowel - i.e. the alternation looks phonologically
systematic rather than arbitrary. If inherited values are real, the true
assignment should yield more confirmatory alternations than a random one.

NULL
Two nulls are run:
  (a) unconstrained permutation of values among signs
  (b) Packard's own constraint: permute only WITHIN frequency bands
Both are reported, since (b) is the harder and more honest test.
"""
import collections, random, statistics

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402
import grid_feasibility as gf  # noqa: E402
import phonology_test as pt  # noqa: E402


random.seed(20260731)
TRIALS = 4000
VOWELS = 'aeiou'


def split_val(v) -> tuple[str, str]:
    """'da' -> ('d','a'); 'a' -> ('', 'a'); 'ra2' -> ('r','a')."""
    v = ''.join(c for c in v if not c.isdigit())
    for i, ch in enumerate(v):
        if ch in VOWELS:
            return v[:i], v[i]
    return v, ''


def build_values() -> dict[str, tuple[str, str]]:
    m = {}
    m.update(pt.CERTAIN); m.update(pt.POSSIBLE); m.update(pt.ASSUMED)
    return {k: split_val(v) for k, v in m.items()}


def confirmatory_rate(pairs, vmap) -> tuple[float, int]:
    conf = tot = 0
    for _, _, _, x, y in pairs:
        if x not in vmap or y not in vmap or x == y:
            continue
        cx, vx = vmap[x]; cy, vy = vmap[y]
        tot += 1
        if (cx and cx == cy) or (vx and vx == vy):
            conf += 1
    return (conf / tot if tot else 0.0), tot


def freq_bands(types, signs, n_bands=4) -> list[list[str]]:
    """Packard's constraint: values may only move within a frequency band."""
    freq = collections.Counter(s for t in types for s in t)
    ordered = sorted(signs, key=lambda s: -freq.get(s, 0))
    size = max(1, len(ordered) // n_bands)
    return [ordered[i:i + size] for i in range(0, len(ordered), size)]


def run(name, groups) -> None:
    types = sorted({tuple(t) for t in groups if len(t) > 1})
    pairs = gf.minimal_pairs(types)
    vmap = build_values()
    obs, n = confirmatory_rate(pairs, vmap)

    print(f'\n=== {name} ===')
    print(f'  types {len(types)}  minimal pairs {len(pairs)}  '
          f'testable (both signs valued) {n}')
    if n < 30:
        print('  -> too few testable alternations')
        return
    print(f'  observed confirmatory rate : {obs:.4f}')

    signs = [s for s in vmap]
    vals = [vmap[s] for s in signs]

    # (a) unconstrained permutation
    null_a = []
    for _ in range(TRIALS):
        random.shuffle(vals)
        null_a.append(confirmatory_rate(pairs, dict(zip(signs, vals)))[0])
    m, s = float(statistics.mean(null_a)), float(statistics.pstdev(null_a))
    p = (sum(1 for v in null_a if v >= obs) + 1) / (TRIALS + 1)
    print(f'  null (a) unconstrained     : {m:.4f} +/- {s:.4f}   '
          f'z = {(obs-m)/s:+.2f}   p = {p:.4f}')

    # (b) Packard's frequency-band constraint
    bands = freq_bands(types, signs)
    null_b = []
    for _ in range(TRIALS):
        perm = {}
        for band in bands:
            bv = [vmap[s] for s in band]
            random.shuffle(bv)
            perm.update(dict(zip(band, bv)))
        null_b.append(confirmatory_rate(pairs, perm)[0])
    m2, s2 = float(statistics.mean(null_b)), float(statistics.pstdev(null_b))
    p2 = (sum(1 for v in null_b if v >= obs) + 1) / (TRIALS + 1)
    print(f'  null (b) freq-band (Packard): {m2:.4f} +/- {s2:.4f}   '
          f'z = {(obs-m2)/s2:+.2f}   p = {p2:.4f}')

    # Packard-style ratio, for comparability with the 1974 figure
    print(f'  Packard-style ratio vs null: {obs/m:.2f} : 1 (unconstrained), '
          f'{obs/m2:.2f} : 1 (banded)')
    print('  [Packard 1974 reported 2:1; Pope & Raison 1978, 3:1]')
    print(f'  -> {"SIGNAL" if p2 < 0.05 else "no signal at p<0.05"}')


def main() -> None:
    g = json_load('data/signgroups_by_genre.json')
    print(f'PACKARD REPLICATION: confirmatory alternations, {TRIALS} permutations')
    run('administrative', [tuple(t) for t in g['administrative']])
    run('religious', [tuple(t) for t in g['religious']])
    run('combined', [tuple(t) for t in g['administrative'] + g['religious']])


if __name__ == '__main__':
    main()
