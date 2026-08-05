#!/usr/bin/env python3
"""
Linear A pipeline - Stage 2: structural analysis.

METHOD NOTE
-----------
This stage is deliberately language-agnostic. No phonetic value, no Linear B
reading and no language hypothesis enters any computation here. Signs are
treated as opaque symbols identified only by GORILA id. The aim is a typological
fingerprint derived from distribution alone, following the order Ventris used:
build the internal grid first, test language hypotheses against it afterward.

Inputs are filtered hard:
  * only `signgroup` tokens (numerals, measures, dividers, rulings excluded)
  * only tokens with `complete == True` (no damage), because a fragment's
    first or last sign is not evidence of word-initial or word-final position
"""
import json, collections
from collections.abc import Iterator
from typing import Any

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402


# Genre from physical support. Mechanical, not interpretive.
# Z-type supports (stone/metal/clay vessels, architecture, objects) carry the
# religious/votive corpus; clay administrative documents carry the accounts.
ADMIN_SUPPORTS = {
    'Nodule', 'Tablet', 'Roundel', 'Sealing', 'Lames (short thin tablet)',
    '3-sided bar', '4-sided bar', 'Label',
}
RELIGIOUS_SUPPORTS = {
    'Stone vessel', 'Stone object', 'Metal object', 'Clay vessel', 'clay vessel',
    'Architecture', 'Inked inscription', 'Graffito', 'ivory object',
    'Loom weight', 'Triton',
}


def genre(rec) -> str:
    s = rec.get('support')
    if s in ADMIN_SUPPORTS:
        return 'administrative'
    if s in RELIGIOUS_SUPPORTS:
        return 'religious'
    return 'unclassified'


def load() -> list[dict[str, Any]]:
    return json_load('data/corpus_v1.json')


def signgroups(recs, only_complete=True) -> Iterator[tuple[str, list[str]]]:
    """Yield (genre, sign_ids) for signgroup tokens."""
    for r in recs:
        g = genre(r)
        for t in r['tokens']:
            if t['type'] != 'signgroup':
                continue
            if only_complete and not t['complete']:
                continue
            ids = [i for i in t['sign_ids'] if i]
            if ids:
                yield g, ids


def main() -> None:
    recs = load()

    # ---- genre distribution ----------------------------------------------
    gcount = collections.Counter(genre(r) for r in recs)
    print('=== genre tagging (by support) ===')
    for k, v in gcount.most_common():
        print(f'  {k:16s} {v:5d} records')

    # ---- corpus size per genre -------------------------------------------
    print('\n=== usable signgroup inventory (complete tokens only) ===')
    per_genre = collections.defaultdict(list)
    for g, ids in signgroups(recs):
        per_genre[g].append(ids)
    for g in ('administrative', 'religious', 'unclassified'):
        toks = per_genre[g]
        multi = [t for t in toks if len(t) > 1]
        print(f'  {g:16s} tokens={len(toks):5d}  multi-sign={len(multi):5d}  '
              f'distinct={len({tuple(t) for t in toks}):5d}')

    # ---- word length distribution ----------------------------------------
    print('\n=== sign-group length distribution (complete, multi-sign) ===')
    print(f'  {"len":>4}  {"admin":>8}  {"relig":>8}')
    lens = {g: collections.Counter(len(t) for t in per_genre[g] if len(t) > 1)
            for g in ('administrative', 'religious')}
    for n in range(2, 11):
        a = lens['administrative'].get(n, 0)
        r = lens['religious'].get(n, 0)
        if a or r:
            print(f'  {n:>4}  {a:>8}  {r:>8}')
    for g in ('administrative', 'religious'):
        tot = sum(lens[g].values())
        mean = sum(n * c for n, c in lens[g].items()) / tot if tot else 0
        print(f'  mean length {g:16s} {mean:.2f}  (n={tot})')

    # ---- positional distribution -----------------------------------------
    # Only multi-sign groups: in a single-sign token the sign is trivially both
    # initial and final, which would corrupt the positional signal.
    print('\n=== positional profile ===')
    for g in ('administrative', 'religious'):
        init = collections.Counter(); fin = collections.Counter()
        med = collections.Counter(); tot = collections.Counter()
        for ids in per_genre[g]:
            if len(ids) < 2:
                continue
            init[ids[0]] += 1
            fin[ids[-1]] += 1
            for s in ids[1:-1]:
                med[s] += 1
            for s in ids:
                tot[s] += 1
        n_tokens = sum(1 for t in per_genre[g] if len(t) > 1)
        print(f'\n  --- {g} (n={n_tokens} multi-sign groups, '
              f'{len(tot)} distinct signs) ---')
        print(f'  {"sign":10s} {"tot":>5} {"init":>5} {"med":>5} {"fin":>5}  {"skew":>6}')
        for s, n in tot.most_common(15):
            i, m, fi = init[s], med[s], fin[s]
            # positional skew: +1 strictly initial, -1 strictly final
            skew = (i - fi) / n if n else 0
            print(f'  {s:10s} {n:5d} {i:5d} {m:5d} {fi:5d}  {skew:+6.2f}')

    with open('data/signgroups_by_genre.json', 'w', encoding='utf-8') as _f:
        json.dump({g: [list(t) for t in per_genre[g]] for g in per_genre}, _f,
              ensure_ascii=False)
if __name__ == '__main__':
    main()
