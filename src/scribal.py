#!/usr/bin/env python3
"""
Stage 2e: do reading disagreements cluster by scribal hand?

If contested readings concentrate in particular hands, the dispute is partly
palaeographic rather than purely editorial: that scribe's forms are genuinely
hard to tell apart. That reframes adjudication and is directly useful to the
divergence register.

Test: for each hand, compare its share of divergence sites against its share of
signs written, using a Poisson/binomial rate test with Benjamini-Hochberg
correction for multiple hands.
"""
import collections
from scipy import stats

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402


def main() -> None:
    recs = {r['record_id']: r for r in
            json_load('data/corpus_v1.json')}
    reg = json_load('data/divergences.json')

    # exposure: signs written per hand (only signgroup tokens)
    exposure = collections.Counter()
    for r in recs.values():
        sc = r.get('scribe')
        if not sc:
            continue
        exposure[sc] += sum(t['n_signs'] for t in r['tokens']
                            if t['type'] == 'signgroup')

    # divergence sites per hand
    hits = collections.Counter()
    by_id = collections.defaultdict(lambda: collections.Counter())
    total_sites = 0
    for d in reg['divergences']:
        for s in d.get('sites', []):
            rid = s.get('record_id')
            total_sites += 1
            r = recs.get(rid)
            if r is None:
                continue
            scribe = r.get('scribe')
            if not scribe:
                continue
            hits[scribe] += 1
            by_id[d['id']][scribe] += 1

    tot_exp = sum(exposure.values())
    tot_hits = sum(hits.values())
    base = tot_hits / tot_exp

    print('=== divergence rate by scribal hand ===')
    print(f'  divergence sites total          : {total_sites}')
    print(f'  attributable to a named hand    : {tot_hits}')
    print(f'  signs written by attributed hands: {tot_exp}')
    print(f'  baseline rate                   : {base:.4f} divergences/sign')

    rows = []
    for sc, e in exposure.items():
        if e < 40:
            continue
        h = hits.get(sc, 0)
        p = stats.binomtest(h, e, base, alternative='greater').pvalue
        rows.append((sc, e, h, h / e, p))

    # Benjamini-Hochberg
    rows.sort(key=lambda r: r[4])
    m = len(rows)
    print(f'\n  hands tested (>=40 signs): {m}')
    print(f'\n  {"hand":22s}{"signs":>7}{"div":>5}{"rate":>8}{"p":>10}  {"BH":>6}')
    any_sig = False
    for i, (sc, e, h, rate, p) in enumerate(rows, 1):
        crit = 0.05 * i / m
        sig = p <= crit
        any_sig = any_sig or sig
        print(f'  {sc:22s}{e:>7}{h:>5}{rate:>8.4f}{p:>10.3g}  '
              f'{crit:>6.4f}{" *" if sig else ""}')

    print(f'\n  any hand significant after BH correction: {any_sig}')

    print('\n=== D4 (AB21/AB22) specifically ===')
    d4 = by_id.get('D4', collections.Counter())
    print(f'  D4 sites attributable to a hand: {sum(d4.values())}')
    for sc, n in d4.most_common():
        print(f'    {sc:22s} {n}')
    if sum(d4.values()) < 5:
        print('  -> too few attributed sites to test; the AB21/AB22 documents')
        print('     are largely unattributed in GORILA.')


if __name__ == '__main__':
    main()
