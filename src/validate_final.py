#!/usr/bin/env python3
"""
Final internal validation: null models for the two remaining untested claims.

Two concerns motivate this.

1. PSEUDO-REPLICATION. The register length difference was tested with
   Mann-Whitney over individual words, which treats every word as an independent
   observation. Words inside one document share a scribe, a document type and a
   subject, so they are not independent. The correct unit of permutation is the
   RECORD, not the word. Word-level tests will overstate significance, possibly
   by a wide margin.

2. MULTIPLE COMPARISONS. The positional-preference table reported per-sign
   binomial p-values with no correction across the ~20 signs tested, and against
   an analytic null rather than a permutation of the actual word shapes.

Both are re-run here properly. Where the corrected result is weaker, the
corrected result stands.
"""
import collections, random, statistics
from scipy import stats

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import structural as st  # noqa: E402


random.seed(20260731)
TRIALS = 5000


def record_words(recs) -> list[tuple[str, list[list[str]]]]:
    """Per record: genre and its complete multi-sign words."""
    out = []
    for r in recs:
        ws = [[i for i in t['sign_ids'] if i]
              for t in r['tokens']
              if t['type'] == 'signgroup' and t['complete']]
        ws = [w for w in ws if len(w) > 1]
        if ws:
            out.append((st.genre(r), ws))
    return out


# ---------------------------------------------------------------- length ----
# --- Pseudo-replication ----------------------------------------------------
# Words inside one document share a scribe, a document type and a subject, so a
# word-level test treats non-independent observations as independent. The
# correct unit of permutation is the RECORD. The original word-level p-value
# (6.2e-18) was unusable.
def length_test(recs) -> None:
    data = record_words(recs)
    data = [(g, ws) for g, ws in data if g in ('administrative', 'religious')]

    def mean_diff(assignment) -> float:
        a = [len(w) for lab, (_, ws) in zip(assignment, data)
             if lab == 'religious' for w in ws]
        b = [len(w) for lab, (_, ws) in zip(assignment, data)
             if lab == 'administrative' for w in ws]
        if not a or not b:
            return 0.0
        return float(statistics.mean(a)) - float(statistics.mean(b))

    labels = [g for g, _ in data]
    obs = mean_diff(labels)

    n_admin_rec = sum(1 for g, _ in data if g == 'administrative')
    n_relig_rec = len(data) - n_admin_rec

    null = []
    for _ in range(TRIALS):
        sh = labels[:]
        random.shuffle(sh)
        null.append(mean_diff(sh))
    m, s = float(statistics.mean(null)), float(statistics.pstdev(null))
    p = (sum(1 for v in null if abs(v) >= abs(obs)) + 1) / (TRIALS + 1)

    print('=== register length difference ===')
    print(f'  records: administrative {n_admin_rec}, religious {n_relig_rec}')
    print(f'  observed mean-length difference : {obs:+.3f} signs')
    print(f'  record-permuted null            : {m:+.3f} +/- {s:.3f}')
    print(f'  z                               : {(obs - m)/s:+.2f}')
    print(f'  p (record-level permutation)    : {p:.4f}')

    # for contrast, the word-level test originally reported
    la = [len(w) for g, ws in data if g == 'administrative' for w in ws]
    lr = [len(w) for g, ws in data if g == 'religious' for w in ws]
    _, p_word = stats.mannwhitneyu(la, lr, alternative='two-sided')
    print(f'  (word-level Mann-Whitney, orig) : p = {p_word:.3g}')
    print(f'  NOTE: the permutation p is floored at 1/(trials+1) = '
          f'{1/(TRIALS+1):.4f}, so it reads as a bound, not a point estimate.')
    print(f'  The z of {(obs - m)/s:+.2f} is the informative figure. The word-level')
    print('  p-value assumed independent words and is not comparable.')


# ------------------------------------------------------------ positional ----
# --- Within-word permutation ----------------------------------------------
# Shuffles sign order INSIDE each word, preserving word lengths and each word's
# sign multiset, destroying only arrangement. With BH correction, roughly half
# the originally reported positional preferences do not survive.
def positional_test(recs, genre, min_n=15) -> None:
    """Null: shuffle sign order WITHIN each word. Preserves word lengths and
    each word's sign multiset; destroys only positional arrangement."""
    words = [w for g, ws in record_words(recs) if g == genre for w in ws]

    def edge_counts(word_list) -> tuple[collections.Counter[str], collections.Counter[str], collections.Counter[str]]:
        first = collections.Counter()
        last = collections.Counter()
        total = collections.Counter()
        for w in word_list:
            first[w[0]] += 1
            last[w[-1]] += 1
            for sign in w:
                total[sign] += 1
        return first, last, total

    init, fin, tot = edge_counts(words)
    cand = [s for s, n in tot.items() if n >= min_n]

    null_init = collections.defaultdict(list)
    null_fin = collections.defaultdict(list)
    for _ in range(TRIALS):
        sh = []
        for w in words:
            x = w[:]; random.shuffle(x); sh.append(x)
        i2, f2, _ = edge_counts(sh)
        for s in cand:
            null_init[s].append(i2[s])
            null_fin[s].append(f2[s])

    rows = []
    for s in cand:
        ni, nf = null_init[s], null_fin[s]
        p_i = (sum(1 for v in ni if v >= init[s]) + 1) / (len(ni) + 1)
        p_f = (sum(1 for v in nf if v >= fin[s]) + 1) / (len(nf) + 1)
        p = min(p_i, p_f) * 2                      # two-sided over the two edges
        bias = 'INITIAL' if p_i < p_f else 'FINAL'
        rows.append((s, tot[s], init[s], fin[s],
                     float(statistics.mean(ni)), float(statistics.mean(nf)), min(p, 1.0), bias))

    rows.sort(key=lambda r: r[6])
    m = len(rows)
    print(f'\n=== positional preference: {genre} (within-word permutation) ===')
    print(f'  signs tested (n>={min_n}): {m}   words: {len(words)}')
    print(f'  {"sign":9s}{"n":>5}{"init":>6}{"exp":>7}{"fin":>6}{"exp":>7}{"p":>9}{"BH":>8}  bias')
    survivors = 0
    for i, (s, n, ii, ff, ei, ef, p, bias) in enumerate(rows, 1):
        crit = 0.05 * i / m
        ok = p <= crit
        survivors += ok
        print(f'  {s:9s}{n:5d}{ii:6d}{ei:7.1f}{ff:6d}{ef:7.1f}{p:9.4f}{crit:8.4f}'
              f'{"  *" if ok else "   "} {bias}')
    print(f'  surviving BH correction: {survivors}/{m}')


def main() -> None:
    recs = st.load()
    print(f'RECORD-LEVEL AND WITHIN-WORD PERMUTATION TESTS ({TRIALS} trials)\n')
    length_test(recs)
    positional_test(recs, 'administrative')
    positional_test(recs, 'religious')


if __name__ == '__main__':
    main()
