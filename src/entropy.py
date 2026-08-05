#!/usr/bin/env python3
"""
Stage 2f: sign entropy, with bias correction and an explicit adequacy test.

Entropy is the standard script-typology fingerprint: unigram entropy H1 and
conditional entropy H2 separate alphabets, syllabaries and logographic mixes.

Two traps are handled explicitly rather than ignored:

1. ESTIMATOR BIAS. Plain maximum-likelihood entropy is biased DOWNWARD at small
   n, severely so when the alphabet size approaches the sample size. Miller-Madow
   and Chao-Shen corrections are reported alongside the naive value.

2. COMPARABILITY. Published entropy values for known scripts are computed on
   corpora orders of magnitude larger. Because the bias depends on n, comparing
   our estimate to those numbers is invalid. Any comparison must subsample the
   reference to our size. This script does not perform such a comparison and
   the results below must not be read against published figures.
"""
import math, collections, random

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import structural as st  # noqa: E402


random.seed(20260731)
def mle_entropy(counts) -> float:
    n = float(sum(counts.values()))
    return -float(sum((c / n) * math.log2(c / n)
                      for c in counts.values() if c))


# --- Bias corrections ------------------------------------------------------
# Maximum-likelihood entropy is biased DOWNWARD at small n, severely so when the
# alphabet approaches the sample size. Two standard corrections are reported
# alongside so the reader can see the estimator spread rather than one number.
def miller_madow(counts) -> float:
    n = sum(counts.values())
    k = sum(1 for c in counts.values() if c > 0)
    return mle_entropy(counts) + (k - 1) / (2 * n * math.log(2))


def chao_shen(counts) -> float:
    n = sum(counts.values())
    f1 = sum(1 for c in counts.values() if c == 1)
    coverage = 1 - f1 / n if n and f1 < n else 1e-9   # Good-Turing sample coverage
    h = 0.0
    for c in counts.values():
        if not c:
            continue
        pa = coverage * c / n
        if pa <= 0 or pa >= 1:
            continue
        h -= pa * math.log2(pa) / (1 - (1 - pa) ** n)
    return h


# --- Uncertainty -----------------------------------------------------------
# Resampling interval on the point estimate. Reported because a single entropy
# figure invites false precision.
def bootstrap(seq, estimator, trials=200) -> tuple[float, float]:
    """Resampling interval for an entropy estimator.

    `seq` is a flat list of sign ids; `estimator` takes a Counter and returns
    a float (mle_entropy, miller_madow, chao_shen). Returns the 2.5th and
    97.5th percentiles.
    """
    vals = []
    n = len(seq)
    for _ in range(trials):
        resampled = [seq[random.randrange(n)] for _ in range(n)]
        vals.append(estimator(collections.Counter(resampled)))
    vals.sort()
    return vals[int(0.025 * trials)], vals[int(0.975 * trials)]


def sign_stream(recs, genre_filter=None) -> tuple[list[str], list[list[str]]]:
    """Flat sequence of sign ids, and per-word sequences for bigrams."""
    flat, words = [], []
    for r in recs:
        if genre_filter and st.genre(r) != genre_filter:
            continue
        for t in r['tokens']:
            if t['type'] != 'signgroup' or not t['complete']:
                continue
            ids = [i for i in t['sign_ids'] if i]
            if ids:
                flat.extend(ids)
                words.append(ids)
    return flat, words


def report(label, flat, words) -> tuple[float, float, float, bool]:
    uni = collections.Counter(flat)
    n, k = len(flat), len(uni)
    print(f'\n=== {label} ===')
    print(f'  sign tokens n            : {n}')
    print(f'  distinct signs k         : {k}')

    h_mle, h_mm, h_cs = mle_entropy(uni), miller_madow(uni), chao_shen(uni)
    lo, hi = bootstrap(flat, mle_entropy)
    print(f'  H1 (MLE)                 : {h_mle:.3f} bits  [boot 95%: {lo:.3f}-{hi:.3f}]')
    print(f'  H1 (Miller-Madow)        : {h_mm:.3f} bits')
    print(f'  H1 (Chao-Shen)           : {h_cs:.3f} bits')
    print(f'  H1 max possible (log2 k) : {math.log2(k):.3f} bits')

    # --- bigram adequacy ---------------------------------------------------
    bigrams = []
    for w in words:
        bigrams.extend(zip(w, w[1:]))
    bg = collections.Counter(bigrams)
    possible = k * k
    print(f'\n  within-word bigram tokens: {len(bigrams)}')
    print(f'  distinct bigrams observed: {len(bg)}')
    print(f'  bigrams possible (k^2)   : {possible}')
    print(f'  coverage                 : {100*len(bg)/possible:.1f}% of cells')
    print(f'  tokens per cell          : {len(bigrams)/possible:.3f}')
    hapax = sum(1 for v in bg.values() if v == 1)
    print(f'  bigrams seen exactly once: {hapax} ({100*hapax/max(len(bg),1):.0f}% of observed)')

    adequate = len(bigrams) >= 5 * possible
    print(f'  ADEQUATE for H2?         : {adequate} '
          f'(needs ~{5*possible} tokens, have {len(bigrams)})')
    if not adequate:
        print('  -> conditional entropy NOT estimable: the bigram table is')
        print('     emptier than the data can fill. Any H2 figure would be an')
        print('     artefact of undersampling, not a property of the script.')
    return h_mle, h_mm, h_cs, adequate


def main() -> None:
    recs = st.load()
    print('SIGN ENTROPY (bias-corrected) and sampling adequacy')
    flat, words = sign_stream(recs)
    report('whole corpus (complete signgroups)', flat, words)
    for g in ('administrative', 'religious'):
        f, w = sign_stream(recs, g)
        report(g, f, w)


if __name__ == '__main__':
    main()


def register_comparison() -> None:
    """Fair H1 comparison between registers.

    Entropy estimates depend on n, so comparing the religious corpus (n=721) to
    the administrative (n=3813) directly is invalid. The administrative corpus
    is subsampled to the religious n and the comparison made against that
    distribution.
    """
    import statistics
    recs = st.load()
    fa, _ = sign_stream(recs, 'administrative')
    fr, _ = sign_stream(recs, 'religious')
    n = len(fr)
    obs = chao_shen(collections.Counter(fr))
    sub = [chao_shen(collections.Counter(random.sample(fa, n))) for _ in range(400)]
    m, s = float(statistics.mean(sub)), float(statistics.pstdev(sub))
    print('\n=== register comparison at matched n ===')
    print(f'  religious H1 (Chao-Shen)      : {obs:.3f} bits (n={n})')
    print(f'  administrative subsampled     : {m:.3f} +/- {s:.3f} bits')
    print(f'  z                             : {(obs - m) / s:+.2f}')
    p = sum(1 for v in sub if v <= obs) / len(sub)
    print(f'  p(admin <= religious)         : {p:.3f}')
