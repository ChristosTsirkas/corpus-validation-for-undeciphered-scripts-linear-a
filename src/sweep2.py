#!/usr/bin/env python3
"""Sweep 2: corpus_v1 vs Younger's non-tabular records (incl. the libation corpus)."""
import json, re, difflib, collections

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402
import sweep1 as s1  # noqa: E402


LIBATION = re.compile(r'Z[abcdfg]', re.I)


def compare(recs, y) -> tuple[list[dict], collections.Counter]:
    """The actual comparison, isolated from I/O so it's independently
    testable - same shape as sweep1.compare() / sweep3.compare()."""
    stats: collections.Counter = collections.Counter()
    findings: list = []

    for key, toks in y.items():
        rid = key if key in recs else (key + 'a' if key + 'a' in recs else None)
        if rid is None:
            stats['no_matching_record'] += 1; continue
        ours = [x for x in s1.our_token_stream(recs[rid]) if x['val'] not in s1.EDITORIAL]
        a = [x['val'] for x in ours]
        b = [c for c in (s1.canon(t['val']) for t in toks) if c not in s1.EDITORIAL]
        if not a and not b:
            continue
        is_lib = bool(LIBATION.search(str(rid))) if rid else False
        stats['records_compared'] += 1
        stats['lib_records' if is_lib else 'other_records'] += 1
        stats['tokens_ours'] += len(a); stats['tokens_younger'] += len(b)
        if is_lib:
            stats['lib_tokens_ours'] += len(a)

        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if tag == 'equal':
                stats['tokens_agree'] += (i2 - i1)
                if is_lib: stats['lib_tokens_agree'] += (i2 - i1)
                continue
            findings.append({'record_id': rid, 'libation': is_lib, 'op': tag,
                             'ours': a[i1:i2], 'younger': b[j1:j2]})
    return findings, stats


def main() -> None:
    recs = {r['record_id']: r for r in json_load('data/corpus_v1.json')}
    y = json_load('data/younger_freetext.json')
    findings, stats = compare(recs, y)

    with open('data/sweep2_findings.json', 'w', encoding='utf-8') as _f:
        json.dump(findings, _f,
              ensure_ascii=False, indent=1)
    print('=== sweep 2: corpus_v1 vs Younger (non-tabular) ===')
    for k in sorted(stats): print(f'  {str(k):24s} {stats[k]}')
    t, ag = stats['tokens_ours'], stats['tokens_agree']
    if t: print(f'\n  overall token agreement : {ag}/{t} = {100*ag/t:.1f}%')
    lt, la = stats['lib_tokens_ours'], stats['lib_tokens_agree']
    if lt: print(f'  LIBATION agreement      : {la}/{lt} = {100*la/lt:.1f}%')
    print(f'  divergence sites        : {len(findings)}')


if __name__ == '__main__':
    main()
