#!/usr/bin/env python3
"""
Re-specification of the phonological inheritance test for a THREE-VOWEL Minoan.

Salgarella (OCD, 2022) reports the standard view that Minoan may have had a
three-vowel system /a i u/, since in Linear B most signs carrying /o/ and one
carrying /e/ are Greek innovations rather than inherited from Linear A
(Palaima & Sikkenga 1999).

Our original test (PHONOLOGY.md) mapped Linear B values onto Linear A over a
FIVE-vowel inventory. If the three-vowel view is right, that test was
mis-specified: the e- and o-series are largely Greek additions, so treating them
as inherited injects noise into both the statistic and the null.

Re-run with vowels collapsed e->i, o->u, which is the mapping implied if the
Greek e/o signs continue Minoan i/u.
"""
import os
import sys, random, statistics

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import phonology_test as pt  # noqa: E402
import structural as st  # noqa: E402

sys.path.insert(0, 'src')


random.seed(20260731)
COLLAPSE = {'a': 'a', 'i': 'i', 'u': 'u', 'e': 'i', 'o': 'u'}


def run(level, recs, collapse, label, trials=4000) -> tuple[float, float, float, float] | None:
    vmap5 = pt.build_map(level)
    vmap = {k: (collapse[v] if collapse else v) for k, v in vmap5.items()}
    words = pt.words_with_coverage(recs, vmap)
    obs, n = pt.vowel_mi(words, vmap)
    k = len(set(vmap.values()))
    cells = k * k
    print(f'\n  --- {label} ---')
    print(f'  vowel inventory          : {k}   cells: {cells}')
    print(f'  covered words            : {len(words)}   bigrams: {n}'
          f'   per cell: {n/cells:.1f}')
    if n < 5 * cells:
        print('  -> underpowered')
        return None
    signs = list(vmap); vals = [vmap[s] for s in signs]
    null = []
    for _ in range(trials):
        random.shuffle(vals)
        null.append(pt.vowel_mi(words, dict(zip(signs, vals)))[0])
    m, s = float(statistics.mean(null)), float(statistics.pstdev(null))
    p = (sum(1 for v in null if v >= obs) + 1) / (trials + 1)
    print(f'  observed MI              : {obs:.4f} bits')
    print(f'  permuted null            : {m:.4f} +/- {s:.4f}')
    print(f'  z                        : {(obs - m)/s:+.2f}')
    print(f'  p                        : {p:.4f}')
    print(f'  -> {"SIGNAL" if p < 0.05 else "no signal"}')
    return obs, m, s, p


def main() -> None:
    recs = st.load()
    print('PHONOLOGICAL INHERITANCE, RE-SPECIFIED FOR A 3-VOWEL MINOAN')
    print('Salgarella OCD 2022; Palaima & Sikkenga 1999.')
    for level in ('possible', 'assumed'):
        print(f'\n=== confidence level: {level} ===')
        run(level, recs, None, '5-vowel (original specification)')
        run(level, recs, COLLAPSE, '3-vowel (e->i, o->u)')


if __name__ == '__main__':
    main()
