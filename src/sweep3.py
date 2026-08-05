#!/usr/bin/env python3
"""
Sweep 3: corpus_v1 vs SigLA, all overlapping documents.

Third independent witness, and the only one that carries reading certainty.
Comparison is on GORILA sign ids, so no convention aliasing is needed - this is
the sweep the sign-id principle was designed for.

Two comparisons are run:
  (a) STRICT    - every sign SigLA records, including doubtful ones
  (b) CONFIDENT - only signs SigLA marks confident

The gap between (a) and (b) measures how much of our disagreement with SigLA is
concentrated in readings SigLA itself flags as uncertain, i.e. how much of the
apparent conflict is really D12 in disguise.
"""
import collections, difflib, json, os, re
from typing import TypedDict

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402


class CompareFinding(TypedDict):
    record_id: str
    op: str
    ours: list[str]
    sigla: list[str]


NUM = re.compile(r'^AB?(\d+)')



# --- Cross-witness sign identity ------------------------------------------
# The two corpora use different variant conventions for the SAME sign: ours
# A100-102 / A028B / A131C and gender variants AB021M/F; SigLA AB100 / AB028 /
# AB131 / AB021. Compare on sign NUMBER. AB021 vs AB022 stays distinct, which
# is what the D4 adjudication required.
def base_id(i) -> str | None:
    """Compare on SIGN NUMBER only.

    The two corpora use different variant conventions for the same sign:
      ours A100-102 / A028B / A131C   vs   SigLA AB100 / AB028 / AB131
      ours AB021M/F (gender variants) vs   SigLA AB021
    Series prefix and variant suffix are notation; the number is the identity.
    AB021 vs AB022 remains distinct, which is what D4 required.
    """
    if not i:
        return None
    m = NUM.match(i)
    return m.group(1) if m else i


def our_docs() -> dict[str, list[str]]:
    out = {}
    for r in json_load('data/corpus_v1.json'):
        seq = []
        for t in r['tokens']:
            if t['type'] not in ('signgroup', 'measure'):
                continue
            for i in t['sign_ids']:
                b = base_id(i)
                if b:
                    seq.append(b)
        out[r['record_id']] = seq
    return out


def sigla_docs() -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    strict, conf = {}, {}
    for d in json_load('data/sigla_corpus.json'):
        key = d['name'].replace(' ', '')
        s, c = [], []
        for a in sorted(d['attestations'], key=lambda x: x['n'] if isinstance(x['n'], int) else 0):
            b = base_id(a['sign_id'])
            if b is None:
                continue
            s.append(b)
            if a['confident']:
                c.append(b)
        strict[key], conf[key] = s, c
    return strict, conf


def compare(ours, theirs, label) -> tuple[list[CompareFinding], collections.Counter[str]]:
    stats = collections.Counter()
    findings = []
    for doc, a in ours.items():
        if doc not in theirs:
            continue
        b = theirs[doc]
        if not a and not b:
            continue
        stats['documents'] += 1
        stats['tokens_ours'] += len(a)
        stats['tokens_theirs'] += len(b)
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                stats['agree'] += (i2 - i1)
                continue
            stats['op_' + tag] += 1
            findings.append({'record_id': doc, 'op': tag,
                             'ours': a[i1:i2], 'sigla': b[j1:j2]})
    tot = stats['tokens_ours']
    print(f'\n=== {label} ===')
    print(f'  documents compared : {stats["documents"]}')
    print(f'  tokens ours        : {stats["tokens_ours"]}')
    print(f'  tokens SigLA       : {stats["tokens_theirs"]}')
    print(f'  agreeing           : {stats["agree"]}')
    if tot:
        print(f'  TOKEN AGREEMENT    : {100*stats["agree"]/tot:.1f}%')
    print(f'  divergence sites   : {len(findings)}')
    return findings, stats


def main() -> None:
    if not os.path.exists('data/sigla_corpus.json'):
        print('data/sigla_corpus.json not present - SigLA comparison skipped.')
        print('See data/README.md to generate it.')
        return
    ours = our_docs()
    # SigLA under-records fraction/measure signs relative to GORILA: 332 against
    # our 447, and A732 (JE) is absent entirely. A palaeographic database indexes
    # drawn sign forms, and composite fractions may be drawn as their components
    # or omitted. Excluding them isolates the SYLLABOGRAM comparison, which is
    # what the two corpora both claim to record exhaustively.
    fraction_ids = {str(n) for n in range(701, 740)}
    ours_syl = {k: [x for x in v if x not in fraction_ids] for k, v in ours.items()}
    strict, conf = sigla_docs()
    overlap = set(ours) & set(strict)
    print(f'overlapping documents: {len(overlap)}')

    f_strict, _ = compare(ours, strict, 'STRICT (all SigLA signs)')
    compare(ours, conf, 'CONFIDENT ONLY (SigLA certain signs)')

    strict_syl = {k: [x for x in v if x not in fraction_ids] for k, v in strict.items()}
    conf_syl = {k: [x for x in v if x not in fraction_ids] for k, v in conf.items()}
    compare(ours_syl, strict_syl, 'SYLLABOGRAMS ONLY, all SigLA signs')
    compare(ours_syl, conf_syl, 'SYLLABOGRAMS ONLY, SigLA confident only')

    with open('data/sweep3_findings.json', 'w', encoding='utf-8') as _f:
        json.dump(f_strict, _f,
              ensure_ascii=False, indent=1)
    # substitution patterns: which sign pairs disagree most?
    subs = collections.Counter()
    for d in f_strict:
        if d['op'] == 'replace' and len(d['ours']) == 1 and len(d['sigla']) == 1:
            subs[(d['ours'][0], d['sigla'][0])] += 1
    print('\n=== most frequent single-sign substitutions (ours -> SigLA) ===')
    for (o, s), n in subs.most_common(15):
        print(f'  {n:4d}  {o:8s} -> {s}')

    # which documents disagree most?
    bydoc = collections.Counter(d['record_id'] for d in f_strict)
    print('\n=== documents with most divergence sites ===')
    for doc, n in bydoc.most_common(10):
        print(f'  {n:4d}  {doc}')


if __name__ == '__main__':
    main()
