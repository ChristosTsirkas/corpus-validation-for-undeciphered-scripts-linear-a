#!/usr/bin/env python3
"""
Packard replication v4 - DEFINITIVE, both rules taken verbatim from the source.

SCORING RULE (p. 76):
  "Alternations are considered significant if the alternating signs have the
   same consonant according to that decipherment."
  => SAME CONSONANT ONLY. Our v1-v3 used share-consonant OR share-vowel, which
     is too permissive and inflated both observed and null.

NULL CONSTRUCTION (p. 73):
  Linear A signs ordered by descending frequency, divided into groups of TEN,
  phonetic values rotated within each group, each value moving to the next less
  common sign, the tenth wrapping to first. Ten decipherments, of which the
  first is the Linear B assignment. => bands of exactly 10 signs, and the nine
  alternatives are ROTATIONS, not free shuffles.

PACKARD'S OWN CHANCE MODEL (p. 72):
  Twelve consonants are distinguished in Linear B orthography, so about 1/12 of
  alternating pairs should share a consonant by chance. With ~107 alternation
  groups that predicts ~8-9 coincidental alternations, which he says agrees with
  the random decipherments.

HIS COUNTS (pp. 74-79):
  final:    39 groups (5 with 3+ signs shared, 34 with 2) -> 3 + 7 = 10 confirmatory
  medial:   26 groups                                      -> 4 confirmatory
  initial:  42 groups                                      -> 5 confirmatory
  TOTAL:   107 groups                                      -> 19 confirmatory
  19 / ~9 expected = about 2:1.
"""
import collections, random, statistics

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402
import packard as pk  # noqa: E402
import packard_v3 as p3  # noqa: E402


random.seed(20260731)
TRIALS = 4000


# --- Packard's scoring rule, verbatim (1974, p. 76) -----------------------
# 'Alternations are considered significant if the alternating signs have the
# same consonant according to that decipherment.' SAME CONSONANT ONLY. Earlier
# versions of this replication scored consonant-OR-vowel and were wrong.
def same_consonant(pairs, vmap) -> tuple[float, int]:
    """Packard's rule: significant iff the alternating signs share a consonant."""
    c = t = 0
    for x, y in pairs:
        if x not in vmap or y not in vmap or x == y:
            continue
        cx, _ = vmap[x]; cy, _ = vmap[y]
        t += 1
        if cx and cx == cy:
            c += 1
    return c, t


# --- Packard's null construction (1974, p. 73) ----------------------------
# Signs ordered by descending frequency, divided into groups of TEN, values
# rotated within each group. His nine alternatives are exhaustive rotations of
# that scheme, which is a better defense of n=9 than it first appears.
def _frequency_bands(vmap, types, group_size=10) -> list[list[str]]:
    """Order signs by descending frequency, divide into groups of group_size.
    A trailing group smaller than 2 can never be rotated or usefully shuffled
    to a different value (k % 1 == 0 always; shuffling one element is a
    no-op), so it is merged into the previous group instead."""
    freq = collections.Counter(s for t in types for s in t)
    ordered = sorted(vmap, key=lambda s: (-freq.get(s, 0), s))
    groups = [ordered[i:i + group_size] for i in range(0, len(ordered), group_size)]
    if len(groups) > 1 and len(groups[-1]) < 2:
        groups[-2].extend(groups.pop())
    return groups


def rotation_nulls(vmap, types, group_size=10) -> list[dict[str, tuple[str, str]]]:
    """Packard's construction: order signs by frequency, group by ten, rotate
    values within each group. Returns the nine non-identity rotations."""
    groups = _frequency_bands(vmap, types, group_size)
    out = []
    for k in range(1, group_size):
        perm = {}
        for g in groups:
            vals = [vmap[s] for s in g]
            rot = vals[k % len(g):] + vals[:k % len(g)]
            perm.update(dict(zip(g, rot)))
        out.append(perm)
    return out


def main() -> None:
    g = json_load('data/signgroups_by_genre.json')
    types = sorted({tuple(t) for t in
                    [tuple(x) for x in g['administrative'] + g['religious']]
                    if len(t) > 1})
    categories = p3.cats(types)
    vmap = pk.build_values()

    # merge 2= and 3= per position, as Packard reports them
    merged = {'final': categories.get('final 2=', []) + categories.get('final 3=', []),
              'medial': categories.get('medial 2=', []) + categories.get('medial 3=', []),
              'initial': categories.get('initial 2=', []) + categories.get('initial 3=', [])}

    packard_published = {'final': (39, 10), 'medial': (26, 4), 'initial': (42, 5)}

    print('PACKARD v4 - same-consonant rule, rotation nulls')
    print(f'{"position":10s}{"our groups":>11}{"testable":>10}{"our conf":>10}'
          f'{"rate":>8}  |{"Pk groups":>10}{"Pk conf":>9}{"Pk rate":>9}')
    tot_obs = tot_n = 0
    for pos in ('final', 'medial', 'initial'):
        pairs = merged[pos]
        obs, n = same_consonant(pairs, vmap)
        tot_obs += obs; tot_n += n
        pg, pc = packard_published[pos]
        print(f'{pos:10s}{len(pairs):>11}{n:>10}{obs:>10}{obs/n if n else 0:>8.3f}'
              f'  |{pg:>10}{pc:>9}{pc/pg:>9.3f}')
    print(f'{"TOTAL":10s}{sum(len(v) for v in merged.values()):>11}{tot_n:>10}'
          f'{tot_obs:>10}{tot_obs/tot_n:>8.3f}  |{107:>10}{19:>9}{19/107:>9.3f}')

    allpairs = merged['final'] + merged['medial'] + merged['initial']

    # --- Packard's own chance model: 1/12 ---
    print("\nPackard's chance model (1/12 of pairs share a consonant):")
    print(f'  expected on our {tot_n} testable pairs : {tot_n/12:.1f}')
    print(f'  observed                              : {tot_obs}')
    print(f'  ratio                                 : {tot_obs/(tot_n/12):.2f} : 1')
    print('  [Packard: 19 observed / ~9 expected   = 2.1 : 1]')

    # --- his nine rotations ---
    rots = rotation_nulls(vmap, types)
    counts = [same_consonant(allpairs, p)[0] for p in rots]
    print('\nHis nine rotations, run on our corpus:')
    print(f'  counts      : {counts}')
    print(f'  average     : {float(statistics.mean(counts)):.2f}')
    print(f'  observed    : {tot_obs}')
    print(f'  ratio       : {tot_obs/float(statistics.mean(counts)):.2f} : 1'
          if float(statistics.mean(counts)) else '')
    print(f'  n beating observed: {sum(1 for c in counts if c >= tot_obs)}/9')

    # --- full permutation null for a proper p-value ---
    bands = _frequency_bands(vmap, types)
    null = []
    for _ in range(TRIALS):
        perm = {}
        for b in bands:
            bv = [vmap[x] for x in b]
            random.shuffle(bv)
            perm.update(dict(zip(b, bv)))
        null.append(same_consonant(allpairs, perm)[0])
    null_mean, null_sd = float(statistics.mean(null)), float(statistics.pstdev(null))
    p = (sum(1 for v in null if v >= tot_obs) + 1) / (TRIALS + 1)
    print(f'\n{TRIALS} banded permutations (beyond his nine):')
    print(f'  null mean {null_mean:.2f} +/- {null_sd:.2f}   z = {(tot_obs-null_mean)/null_sd:+.2f}   p = {p:.4f}')
    print(f'  ratio observed/null = {tot_obs/null_mean:.2f} : 1')


if __name__ == '__main__':
    main()
