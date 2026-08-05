#!/usr/bin/env python3
"""
Stage 2b: affix detection and typological tests.

The claim under test (Duhoux 1978, via Schoep 2002): Linear A shows a high rate
of affixation, 59% of it prefixal against 12% in Linear B, which is read as
evidence the language is agglutinative rather than inflecting. That claim is
boundary-sensitive, and D9 shows word division is contested in the religious
corpus, so the number is reproduced here from our own data rather than cited.

Method is language-agnostic. An affix candidate is any attested type B that
equals an attested type A plus material at one edge. Signs remain opaque ids.
"""
import collections
from scipy import stats

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402


def load_groups() -> dict[str, list[list[str]]]:
    return json_load('data/signgroups_by_genre.json')


def types_of(groups) -> collections.Counter[tuple[str, ...]]:
    return collections.Counter(tuple(g) for g in groups)


def find_affixes(types, max_affix=2) -> tuple[list[tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]], list[tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]]]:
    """Return prefix and suffix relations among attested types."""
    tset = set(types)
    pre, suf = [], []
    for b in tset:
        for k in range(1, max_affix + 1):
            if len(b) - k < 1:
                continue
            stem_r = b[k:]        # b = affix + stem  -> prefix
            stem_l = b[:-k]       # b = stem + affix  -> suffix
            if stem_r in tset:
                pre.append((b[:k], stem_r, b))
            if stem_l in tset:
                suf.append((b[-k:], stem_l, b))
    return pre, suf


def report(genre, groups) -> tuple[int, int] | None:
    multi = [g for g in groups if len(g) > 1]
    types = types_of(multi)
    pre, suf = find_affixes(types)

    affixed = {t for _, _, t in pre} | {t for _, _, t in suf}
    print(f'\n=== {genre} ===')
    print(f'  multi-sign tokens        : {len(multi)}')
    print(f'  distinct types           : {len(types)}')
    print(f'  types with an attested stem: {len(affixed)} '
          f'({100*len(affixed)/len(types):.1f}% of types)')
    if not (pre or suf):
        return None
    tot = len(pre) + len(suf)
    print(f'  affix relations          : {tot}  '
          f'(prefix {len(pre)} = {100*len(pre)/tot:.0f}%, '
          f'suffix {len(suf)} = {100*len(suf)/tot:.0f}%)')

    pc = collections.Counter(a for a, _, _ in pre)
    sc = collections.Counter(a for a, _, _ in suf)
    print('  top prefix candidates    : ' +
          ', '.join(f'{"-".join(a)}({n})' for a, n in pc.most_common(6)))
    print('  top suffix candidates    : ' +
          ', '.join(f'{"-".join(a)}({n})' for a, n in sc.most_common(6)))
    return len(pre), len(suf)


def main() -> None:
    g = load_groups()
    admin = g['administrative']
    relig = g['religious']

    # --- length difference between registers ------------------------------
    la = [len(x) for x in admin if len(x) > 1]
    lr = [len(x) for x in relig if len(x) > 1]
    u, p = stats.mannwhitneyu(la, lr, alternative='two-sided')
    print('=== sign-group length by register ===')
    print(f'  administrative mean {float(sum(la)/len(la)):.2f} (n={len(la)})')
    print(f'  religious      mean {float(sum(lr)/len(lr)):.2f} (n={len(lr)})')
    print(f'  Mann-Whitney U={u:.0f}, p={p:.3g}')

    # --- positional preference, tested not eyeballed ----------------------
    print('\n=== positional preference (binomial, edge vs interior) ===')
    print('  H0: a sign is distributed across positions in proportion to how')
    print('      many slots of each kind exist in the words it occurs in.')
    for name, groups in (('administrative', admin), ('religious', relig)):
        multi = [x for x in groups if len(x) > 1]
        init = collections.Counter(); fin = collections.Counter()
        tot = collections.Counter(); slots = collections.Counter()
        for w in multi:
            init[w[0]] += 1
            fin[w[-1]] += 1
            for s in w:
                tot[s] += 1
                slots[s] += len(w)
        rows = []
        for s, n in tot.items():
            if n < 15:
                continue
            exp_init = sum(1 / len(w) for w in multi for x in w if x == s)
            p_i = stats.binomtest(init[s], n, exp_init / n).pvalue if n else 1
            p_f = stats.binomtest(fin[s], n, exp_init / n).pvalue if n else 1
            rows.append((s, n, init[s], fin[s], exp_init, min(p_i, p_f),
                         'INITIAL' if init[s] > fin[s] else 'FINAL'))
        rows.sort(key=lambda r: r[5])
        print(f'\n  --- {name} ---')
        print(f'  {"sign":9s}{"n":>5}{"init":>6}{"fin":>5}{"exp":>7}  {"p":>10}  bias')
        for s, n, i, f, e, pv, bias in rows[:10]:
            star = '***' if pv < 0.001 else ('**' if pv < 0.01 else
                                             ('*' if pv < 0.05 else ''))
            print(f'  {s:9s}{n:5d}{i:6d}{f:5d}{e:7.1f}  {pv:10.2e} {star:3s} {bias}')

    # --- affixation --------------------------------------------------------
    print('\n\n=== affixation (language-agnostic) ===')
    report('administrative', admin)
    report('religious', relig)


if __name__ == '__main__':
    main()
