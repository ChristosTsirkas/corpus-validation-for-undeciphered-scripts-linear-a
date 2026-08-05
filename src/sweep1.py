#!/usr/bin/env python3
"""
Sweep 1, step B: align corpus_v1 against Younger's tables and classify every
mismatch as either a KNOWN CONVENTION DIFFERENCE or a SUBSTANTIVE DIVERGENCE.

Comparison is done on canonicalized tokens. Label conventions differ between
Douros (our source) and Younger, so an alias table folds documented equivalences
together first. Anything left over is a real disagreement about the tablet.
"""
import json, re, difflib, collections
from typing import TypedDict

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402


class OurToken(TypedDict):
    val: str
    raw_label: str | None
    sign_ids: list[str | None]
    type: str
    damaged: bool
    line: int


# Younger label -> Douros/repo canonical form. These are DOCUMENTED equivalences
# for the same sign, not guesses. The AB number is given for audit.
YOUNGER_ALIAS = {
    'FIC':   'NI',      # AB030
    'CYP':   '*303',
    'VINa':  'VIN',     # AB131
    'VINb':  '*131B',
    'VINc':  '*131C',
    'BOS':   '*23',     'MU':    '*23',     # AB023
    'BOSm':  '*23M',    'BOSf':  '*23F',
    'CAP':   '*22',                          # AB022
    'CAPm':  '*22M',    'CAPf':  '*22F',
    'QI':    '*21',     'OVIS':  '*21',      # AB021
    'QIf':   '*21F',    'OVISf': '*21F',
    'QIm':   '*21M',    'OVISm': '*21M',
    'SUS':   '*85',     'AU':    '*85',      # AB085
    'TELA':  '*54',                          # AB054
    'AES':   '*327',
    'GAL':   '*191',
}

# Notation/formatting variance for the SAME sign. Folded, but counted apart
# from hard aliases so the report can separate convention from substance.
SOFT_ALIAS = {
    'CYP': '*303',          # Younger numbers it, Douros names it
    'AROM': '*123',
    'MA+RU': '*560', 'MA+RUME': '*560ME',
    'I+[?]': '*516',
    'VIR+[?]': 'VIR',
    'QA': 'QA2',            # Younger's own tables vary against his sign list
    '*28B': 'IB',           # AB028 = I
    'MARUME': '*560ME', 'MARU': '*560',
    'GRA+K+L': 'GRA+K+L2',   # label artifact: sign A584 is defined as GRA+K+L2
}
VAS_RE = re.compile(r'^(\*\d+)VAS')

SUB = str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')


def _up(d) -> dict[str, str]:
    return {k.upper(): v.upper() for k, v in d.items()}

HARD = _up(YOUNGER_ALIAS)
SOFT = _up(SOFT_ALIAS)

# Younger notation that is not part of the sign string
NOISE_RE = re.compile(r'\+?\[\??\]|\[\]|\{[^}]*\}')
TRAIL_RE = re.compile(r'[-\.]+$')


# --- Canonicalization ------------------------------------------------------
# Editions differ in NOTATION far more than in READING. Folding documented
# equivalences before counting is what takes agreement from 70.5% to 92.0%.
# Everything folded here is a naming convention, never a reading judgement.
def canon(tok) -> str:
    if tok is None:
        return ''
    t = tok.translate(SUB)
    t = re.sub(r'[\s\u00b7•]', '', t)
    t = re.sub(r'^\]+|\[+$', '', t)      # break brackets: damage, compared separately
    t = t.upper()
    t = NOISE_RE.sub('', t)              # +[?] adjunct-unclear markers
    t = TRAIL_RE.sub('', t)              # Younger's continuation hyphen
    t = VAS_RE.sub(r'\1', t)             # *401VAS -> *401
    t = t.lstrip('*') if t.startswith('*OLIV') else t
    parts = re.split(r'([+\-])', t)
    parts = [str(HARD.get(p, SOFT.get(p, p))) if p not in '+-' else p
             for p in parts]
    t = ''.join(parts)
    t = HARD.get(t, SOFT.get(t, t))
    # ligature marking and the VAS/VS vessel suffix are notation, not evidence
    t = re.sub(r'\bV(?:AS|S)\b', '', str(t))
    t = t.replace('-', '').replace('+', '')
    return t


EDITORIAL = {'VEST', 'VACAT', 'VACANT', 'DEEST', 'DESUNT', 'DEESUNT',
             'SUPRAMUTILA', 'INFRAMUTILA', 'MUTILA', 'LACUNA', ''}


A_NUM = re.compile(r'^A(\d+)-VAS$')   # vessel signs only


# --- Vessel sign notation -------------------------------------------------
# The repo labels A402-VAS as '*815' and writes the VAS suffix as '-VS'. Left
# uncorrected this manufactured 20 false divergences and one spurious scribal
# 'finding' at p = 9.8e-08. See paper section 9, artefact 3.
def derive_label(tok) -> str:
    """Prefer the GORILA sign id over the repo's ASCII label.

    The repo labels vessel signs idiosyncratically: A402-VAS is written '*815'
    and the VAS suffix appears as '-VS'. The sign id is unambiguous, so vessel
    signs are rendered from it. Everything else keeps the repo label, since
    conventional names (OLE, CYP, GRA) cannot be derived from a number.
    """
    ids = tok.get('sign_ids') or []
    lab = tok.get('label_repo') or ''
    parts = lab.split('-')
    if not ids or len(parts) != len(ids):
        return lab
    out = []
    for i, p in zip(ids, parts):
        m = A_NUM.match(i or '')
        out.append('*' + str(int(m.group(1))) if m else p)
    return '-'.join(out)


def our_token_stream(rec) -> list[OurToken]:
    """Canonical token stream for one corpus_v1 record."""
    out = []
    for t in rec['tokens']:
        if t['type'] in ('divider', 'line_break', 'ruling', 'lacuna'):
            continue
        if t['type'] == 'measure' and t.get('measure'):
            val = ''.join(m['label'] for m in t['measure'])
        else:
            val = derive_label(t)
        out.append({'val': canon(val), 'raw_label': t['label_repo'],
                    'sign_ids': t['sign_ids'], 'type': t['type'],
                    'damaged': not t['complete'], 'line': t['line']})
    return out


def compare(recs, younger) -> tuple[list[dict], collections.Counter]:
    """The actual comparison, isolated from I/O so it's independently
    testable - same shape as sweep3.compare()."""
    stats = collections.Counter()
    findings = []

    for ykey, ytoks in younger.items():
        # group Younger tokens by side; unsided -> single record
        sides = collections.defaultdict(list)
        for t in ytoks:
            if t['erased']:
                stats['younger_erased_skipped'] += 1
                continue
            sides[t['side']].append(t)

        for side, toks in sides.items():
            rid = ykey + (side or '')
            if rid not in recs:
                # try bare key when Younger gives no side, but we split sides
                if side is None and ykey + 'a' in recs:
                    rid = ykey + 'a'
                else:
                    stats['no_matching_record'] += 1
                    continue

            ours = our_token_stream(recs[rid])
            ours = [x for x in ours if x['val'] not in EDITORIAL]
            a = [x['val'] for x in ours]
            b = [c for c in (canon(t['val']) for t in toks)
                 if c not in EDITORIAL]
            stats['records_compared'] += 1
            stats['tokens_ours'] += len(a)
            stats['tokens_younger'] += len(b)

            sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == 'equal':
                    stats['tokens_agree'] += (i2 - i1)
                    continue
                stats['op_' + tag] += 1
                findings.append({
                    'record_id': rid,
                    'op': tag,
                    'ours': [{'label': ours[k]['raw_label'],
                              'canon': a[k],
                              'sign_ids': ours[k]['sign_ids'],
                              'type': ours[k]['type'],
                              'damaged': ours[k]['damaged']} for k in range(i1, i2)],
                    'younger': [{'canon': b[k]} for k in range(j1, j2)],
                })
    return findings, stats


def main() -> None:
    recs = {r['record_id']: r for r in
            json_load('data/corpus_v1.json')}
    younger = json_load('data/younger_tokens.json')

    findings, stats = compare(recs, younger)

    with open('data/sweep1_findings.json', 'w', encoding='utf-8') as _f:
        json.dump(findings, _f,
              ensure_ascii=False, indent=1)
    print('=== sweep 1: corpus_v1 vs Younger ===')
    for k in sorted(stats):
        print(f'  {str(k):26s} {stats[k]}')
    tot = stats['tokens_ours']
    ag = stats['tokens_agree']
    if tot:
        print(f'\n  token agreement: {ag}/{tot} = {100*ag/tot:.1f}%')
    print(f'  divergence sites logged: {len(findings)}')


if __name__ == '__main__':
    main()
