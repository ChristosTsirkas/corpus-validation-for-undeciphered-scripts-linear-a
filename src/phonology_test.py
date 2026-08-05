#!/usr/bin/env python3
"""
Stage 2g: is the inherited Linear B value system phonologically informative
about Minoan?

FRAMING. The hypothesis is NOT assumed. Linear B writes Greek; Linear A writes
something that is not Greek, so the script crossed a language boundary and sign
values may have been reassigned to suit Greek phonology. Population continuity
does not constrain this. The inherited values are therefore treated as a
falsifiable hypothesis and tested.

TEST. If the values carry real Minoan phonological information, then applying
them to Linear A should expose phonotactic structure - specifically, dependence
between the vowels of consecutive signs within a word (harmony, or any
sequencing constraint). Permuting the sign-to-value assignment destroys any real
signal while preserving the marginal frequency of every value. If the true
assignment does not beat permutations, the values carry no recoverable signal.

Vowels are used rather than full CV values because there are only 5 of them, so
the bigram table is estimable - unlike the 272-sign table in ENTROPY.md.

VALUE SOURCE. Conventional Linear B readings for homomorphic AB-series signs.
Confidence grades follow Younger: only 12 signs have values he calls certain.
The test is run at each confidence level separately.
"""
import collections, random, statistics

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import structural as st  # noqa: E402


random.seed(20260731)
# Younger: "certain: DA, I, JA, KI, PA, PI, RO, RI, SE, SU, TA, O"
CERTAIN = {
    'AB001': 'da', 'AB028': 'i',  'AB057': 'ja', 'AB067': 'ki',
    'AB003': 'pa', 'AB039': 'pi', 'AB002': 'ro', 'AB053': 'ri',
    'AB009': 'se', 'AB058': 'su', 'AB059': 'ta', 'AB061': 'o',
}
# Younger: "possible: TE, A, KO, RA"
POSSIBLE = {'AB004': 'te', 'AB008': 'a', 'AB070': 'ko', 'AB060': 'ra'}

# Conventional readings for the remaining homomorphic signs. These are assumed
# by shape analogy with Linear B and are NOT independently verified for Linear A.
ASSUMED = {
    'AB005': 'to', 'AB006': 'na', 'AB007': 'di', 'AB010': 'u',
    'AB011': 'po', 'AB013': 'me', 'AB016': 'qa', 'AB017': 'za',
    'AB020': 'zo', 'AB021': 'qi', 'AB023': 'mu', 'AB024': 'ne',
    'AB026': 'ru', 'AB027': 're', 'AB030': 'ni', 'AB031': 'sa',
    'AB037': 'ti', 'AB038': 'e',  'AB040': 'wi', 'AB041': 'si',
    'AB044': 'ke', 'AB045': 'de', 'AB046': 'je', 'AB050': 'pu',
    'AB051': 'du', 'AB054': 'wa', 'AB055': 'nu', 'AB065': 'ju',
    'AB069': 'tu', 'AB073': 'mi', 'AB074': 'ze', 'AB077': 'ka',
    'AB078': 'qe', 'AB080': 'ma', 'AB081': 'ku',
}

VOWELS = 'aeiou'


# --- Vowel extraction ------------------------------------------------------
# Vowels rather than full CV values because 5 vowels give a 25-cell table this
# corpus can actually fill, unlike the 272-sign bigram table shown inestimable
# in entropy.py.
def vowel_of(val: str) -> str | None:
    for ch in reversed(val):
        if ch in VOWELS:
            return ch
    return None


# --- Confidence levels -----------------------------------------------------
# Only 12 signs have values Younger calls certain; 52% are assumed by shape
# analogy and never independently verified. The test is run separately at each
# level so the reader can see how much rests on unverified assumptions.
def build_map(level: str) -> dict:
    m = dict(CERTAIN)
    if level in ('possible', 'assumed'):
        m.update(POSSIBLE)
    if level == 'assumed':
        m.update(ASSUMED)
    return {k: vowel_of(v) for k, v in m.items() if vowel_of(v)}


def words_with_coverage(recs, vmap) -> list[list[str]]:
    """Multi-sign words in which every sign has a vowel."""
    out = []
    for r in recs:
        for t in r['tokens']:
            if t['type'] != 'signgroup' or not t['complete']:
                continue
            ids = [i for i in t['sign_ids'] if i]
            if len(ids) < 2:
                continue
            if all(i in vmap for i in ids):
                out.append(ids)
    return out


def vowel_mi(words, vmap) -> tuple[float, int]:
    """Mutual information between vowels of consecutive signs, in bits."""
    pairs: list = []
    for w in words:
        vs = [vmap[i] for i in w]
        pairs.extend(zip(vs, vs[1:]))
    if not pairs:
        return 0.0, 0
    import math
    joint = collections.Counter(pairs)
    left = collections.Counter(a for a, _ in pairs)
    right = collections.Counter(b for _, b in pairs)
    n = len(pairs)
    mi = 0.0
    for (a, b), c in joint.items():
        pxy = c / n
        px = left[a] / n
        py = right[b] / n
        mi += pxy * math.log2(pxy / (px * py))
    return mi, n


def run(level, recs, trials=2000) -> None:
    vmap = build_map(level)
    words = words_with_coverage(recs, vmap)
    obs, n = vowel_mi(words, vmap)

    print(f'\n=== confidence level: {level} ===')
    print(f'  signs with a vowel       : {len(vmap)}')
    print(f'  fully covered words      : {len(words)}')
    print(f'  vowel bigrams            : {n}')
    print(f'  cells (5x5)              : 25   tokens/cell: {n/25:.1f}')
    if n < 125:
        print('  -> UNDERPOWERED: fewer than 5 observations per cell.')
        print('     No conclusion can be drawn at this confidence level.')
        return
    print(f'  observed vowel MI        : {obs:.4f} bits')

    signs = list(vmap)
    vals = [vmap[s] for s in signs]
    null = []
    for _ in range(trials):
        random.shuffle(vals)
        perm = dict(zip(signs, vals))
        null.append(vowel_mi(words, perm)[0])
    m, s = float(statistics.mean(null)), float(statistics.pstdev(null))
    p = (sum(1 for v in null if v >= obs) + 1) / (trials + 1)
    print(f'  permuted null            : {m:.4f} +/- {s:.4f} bits')
    print(f'  z                        : {(obs - m)/s:+.2f}')
    print(f'  p(null >= observed)      : {p:.4f}')
    verdict = ('SIGNAL: values beat permutation' if p < 0.05
               else 'NO SIGNAL detectable at this level')
    print(f'  -> {verdict}')


def main() -> None:
    recs = st.load()
    print('TEST: do inherited Linear B values carry Minoan phonological signal?')
    print('Statistic: mutual information between vowels of consecutive signs.')
    print('Null: sign-to-value assignment permuted, marginals preserved.')
    for level in ('certain', 'possible', 'assumed'):
        run(level, recs)


if __name__ == '__main__':
    main()
