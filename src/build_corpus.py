#!/usr/bin/env python3
"""
Linear A pipeline - Stage 1 corpus builder.   Output: corpus_v1.json

GOVERNING PRINCIPLE (supervisor-approved)
-----------------------------------------
The Unicode sign identity is the DATA. Every ASCII label in the source repo is a
lossy, derived rendering and is regenerated here from the sign ID. This single
rule resolves defects D1, D2 and D3 (see PROCEDURE.md).

Excluded upstream: `translatedWords` (interpretive glosses). Held in reserve for
later cross-check only, never as pipeline input.
"""

import json, re, unicodedata, collections

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402


BREAK   = '\U0001076b'   # repo-local break marker (unassigned in Unicode)
ODDBALL = {'\U0001076c', '\U0001076d', '\U0001076e', '\U000fd1eb'}
DIVIDER = '\U00010101'   # AEGEAN WORD SEPARATOR LINE
RULING  = '\u2014'       # horizontal rule = section boundary, not a sign

# --- Fraction / measure values -------------------------------------------------
# Sign identity is data. Numeric value is ANNOTATED CONJECTURE with confidence.
# 'secure'      : demonstrable (Pope 1960; Bennett 1999; endorsed by Younger)
# 'conjectured' : proposed but explicitly uncertain in the literature
# 'unknown'     : no value established
# Values follow Corazza, Ferrara, Montecchi, Tamburini & Valerio (2021), "The
# mathematical values of fraction signs in the Linear A script", JAS 125:105214
# (open access). Their optimal system is derived by constraint programming over
# epigraphic, typological and optimality constraints, and supersedes the older
# conjectures collected by Younger. Confidence grades below are theirs.
#
# NOTE ON K: Pope (1960), followed by Younger, gives K = 1/16, and we previously
# graded that 'secure'. Corazza et al. derive K = 1/10 as part of a
# decimal-sexagesimal subset with L2 = 1/20 ... L6 = 1/60. Logged as D13.
FRACTION_VALUES = {
    'A707':   ('J',  0.5,      'secure',      'Pope 1960; Corazza 2021'),
    'A704':   ('E',  0.25,     'secure',      'Pope 1960; Corazza 2021'),
    'A705':   ('F',  0.125,    'secure',      'Pope 1960; Corazza 2021'),
    'A732':   ('JE', 0.75,     'secure',      'J+E'),
    'A721':   ('EF', 0.375,    'secure',      'E+F'),
    'A735':   ('JF', 0.625,    'secure',      'J+F'),
    'A703':   ('D',  1/6,      'derived',     'Corazza 2021 optimal system'),
    'A702':   ('B',  1/5,      'derived',     'Corazza 2021 optimal system'),
    'A708':   ('K',  0.1,      'derived',     'Corazza 2021 (Pope/Younger: 1/16; see D13)'),
    'A709-2': ('L2', 0.05,     'derived',     'Corazza 2021 optimal system'),
    'A709-3': ('L3', 1/30,     'derived',     'Corazza 2021 optimal system'),
    'A709-4': ('L4', 0.025,    'derived',     'Corazza 2021 optimal system'),
    'A709-6': ('L6', 1/60,     'derived',     'Corazza 2021 optimal system'),
    'A706':   ('H',  0.0625,   'tentative',   'Corazza 2021, tentative'),
    'A701':   ('A',  1/24,     'tentative',   'Corazza 2021, tentative'),
    'A736':   ('JH', None,     'unknown',     ''),
    'A709':   ('L',  None,     'excluded',    'Corazza 2021: not an independent sign, p=4e-12'),
    'A710':   ('W',  None,     'unknown',     'Corazza: probably = B B'),
    'A711':   ('X',  None,     'unknown',     'Corazza: probably = A A = 1/12'),
    'A712':   ('Y',  None,     'unknown',     'rare, Middle Minoan II only'),
    'A713':   ('Om', None,     'unknown',     'doubtful, possibly Cretan Hieroglyphic'),
    'A717':   ('DD', 1/3,      'derived',     'Corazza 2021: D+D = 1/3'),
}

SIGN_RE = re.compile(r'^LINEAR A SIGN ([A-Z0-9\-]+)')

# --- D4 correction -------------------------------------------------------
# Our source (Douros via mwenge) systematically inverts AB021 (QI/OVIS, sheep)
# and AB022 (CAP, goats). SigLA agrees with Younger on 15 of 15 attestable
# sites, in BOTH directions, so this is a mis-mapping in the tabulation rather
# than a scholarly disagreement. See divergences.json D4.
D4_INVERT = {'AB021': 'AB022', 'AB021M': 'AB022M', 'AB021F': 'AB022F',
             'AB022': 'AB021', 'AB022M': 'AB021M', 'AB022F': 'AB021F'}
D4_DOCS = {'HT132', 'HT136a', 'HT20', 'HT38', 'HT64', 'KH6', 'KN28a',
           'KNWc29', 'ZA22', 'ZA26a', 'ZA26b', 'ZA9'}


# --- Sign identity --------------------------------------------------------
# The governing principle of the whole project: the Unicode character NAME
# carries the GORILA sign id (e.g. 'LINEAR A SIGN AB008'), so identity comes
# from the codepoint, never from the repo's ASCII label, which is lossy.
def sign_id(ch) -> str | None:
    """GORILA/Unicode sign id, e.g. AB008, A584, A709-2. None if not a sign."""
    m = SIGN_RE.match(unicodedata.name(ch, ''))
    return m.group(1) if m else None


def block_of(ch) -> str:
    o = ord(ch)
    if 0x10600 <= o <= 0x1077F: return 'LinearA'
    if 0x10100 <= o <= 0x1013F: return 'AegeanNumbers'
    if o < 0x80: return 'ASCII'
    return 'other'


def split_id(name) -> tuple[str, str | None]:
    """HT28a -> ('HT28','a'); IOZa2 -> ('IOZa2', None)."""
    m = re.match(r'^(.*\d)([ab])$', name)
    return (m.group(1), m.group(2)) if m else (name, None)


# --- Token typing ---------------------------------------------------------
# Six types. `ruling` matters: the em dash in the source is not a sign but the
# horizontal rule separating sections on administrative tablets, and recovering
# it gives us scribal section boundaries for free (used by kuro_test.py).
def classify(raw, core, ids) -> str:
    if raw == '\n':            return 'line_break'
    if core == RULING:         return 'ruling'
    if core == DIVIDER:        return 'divider'
    if core == '':             return 'lacuna'
    if core and all(block_of(c) == 'AegeanNumbers' for c in core):
        return 'numeral'
    if ids and all(i in FRACTION_VALUES for i in ids if i is not None):
        return 'measure'
    return 'signgroup'


# --- Damage (defect D1) ---------------------------------------------------
# U+1076B marks a break. It survives in the `words` layer but is stripped from
# `transliteratedWords`. Parsing it into structured flags is what prevents 374
# fragments being counted as whole words.
def damage(raw) -> dict:
    if BREAK not in raw:
        return {'before': False, 'after': False, 'internal': False}
    return {'before': raw.startswith(BREAK),
            'after':  raw.endswith(BREAK),
            'internal': BREAK in raw.strip(BREAK)}


def main() -> None:
    src = json_load('data/inscriptions_clean.json')
    out, rep = [], collections.Counter()

    for d in src:
        words = d.get('words', [])
        trans = d.get('transliteratedWords', [])
        if len(words) != len(trans):
            rep['MISALIGNED_DOC'] += 1
            trans = list(trans) + [None] * (len(words) - len(trans))

        doc_id, side = split_id(d['name'])
        tokens, line_no, seq = [], 0, 0

        for raw, tl in zip(words, trans):
            if not isinstance(raw, str):
                continue
            if any(c in ODDBALL for c in raw):
                rep['ODDBALL_STRIPPED'] += 1
                raw = ''.join(c for c in raw if c not in ODDBALL)

            core = raw.replace(BREAK, '')
            ids  = [sign_id(c) for c in core]
            if d['name'] in D4_DOCS:
                ids = [D4_INVERT.get(i, i) if i else i for i in ids]
            ttype = classify(raw, core, ids)
            if ttype == 'line_break':
                line_no += 1
                continue

            dmg = damage(raw)
            tok: dict = {
                'seq': seq, 'line': line_no,
                'raw': raw,
                'sign_ids': ids,
                'n_signs': len(core),
                'type': ttype,
                'damage': dmg,
                'complete': not any(dmg.values()),
                'label_repo': tl if isinstance(tl, str) else None,  # lossy, reference only
            }

            meas = [i for i in ids if i in FRACTION_VALUES]
            if meas:
                tok['measure'] = [{
                    'sign': i,
                    'label': str(FRACTION_VALUES[i][0]),
                    'value_conjecture': FRACTION_VALUES[i][1],
                    'confidence': str(FRACTION_VALUES[i][2]),
                    'source': str(FRACTION_VALUES[i][3]),
                } for i in meas]
                for i in meas:
                    rep['measure_conf_' + str(FRACTION_VALUES[i][2])] += 1

            tokens.append(tok)
            seq += 1
            rep['tok_' + ttype] += 1
            if ttype == 'signgroup':
                rep['signgroup_' + ('complete' if tok['complete'] else 'damaged')] += 1

        out.append({
            'record_id': d['name'], 'doc_id': doc_id, 'side': side,
            'site': d.get('site'), 'support': d.get('support'),
            'findspot': d.get('findspot'), 'context': d.get('context'),
            'scribe': d.get('scribe'), 'gorila_ref': d.get('imageRightsURL'),
            'n_lines': line_no + 1, 'tokens': tokens,
        })
        rep['records'] += 1

    with open('data/corpus_v1.json', 'w', encoding='utf-8') as _f:
        json.dump(out, _f,
              ensure_ascii=False, indent=1)
    print('=== corpus_v1 build report ===')
    for k in sorted(rep):
        print(f'{str(k):28s} {rep[k]}')
    print('\ndistinct documents (sides merged):', len({r['doc_id'] for r in out}))


if __name__ == '__main__':
    main()
