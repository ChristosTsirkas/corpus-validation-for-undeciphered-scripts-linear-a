#!/usr/bin/env python3
"""
Stage 2c: libation formula segmentation under BOTH word-division readings.

D9 established that word division in the religious corpus is contested between
Douros (our source) and Younger. Rather than adjudicate, this runs the entire
segmentation twice, once per reading, and reports only structure that survives
both. Anything that appears under one reading and not the other is flagged, not
claimed.

No phonetic value or language hypothesis is used. Words are compared as sign
strings. Slot structure is derived from observed relative order, not from any
published schema of the formula.
"""
import json, re, difflib, collections

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402
import sweep1 as s1  # noqa: E402


ANCHOR = re.compile(r'SASARA|UNA(RU)?KANA|ATAI|TANAI|IPINAMA|SIRUTE|JAPAQA'
                    r'|TANARATE|ADIKITE|JADIKITU')
JUNK = {'TypesofSupports'}
SIM = 0.62          # clustering threshold on sign-string similarity

# Younger's apparatus that survives canonicalization: uncertainty markers,
# numbered reconstruction labels, bare punctuation.
NOISE = re.compile(r'^(\d+\??|\?+|:|\.|,|/|_+|[A-Z]?\d\?)$')


def strip_noise(words) -> list[str]:
    return [w for w in words if w and not NOISE.match(w)]


def dedupe_block(words) -> list[str]:
    """Younger sometimes prints a reconstructed re-ordering after the text,
    duplicating it verbatim. Drop an exact trailing repeat."""
    n = len(words)
    for k in range(n // 2, 1, -1):
        if words[-k:] == words[-2 * k:-k]:
            return words[:-k]
    return words


def our_reading() -> dict[str, list[str]]:
    recs = json_load('data/corpus_v1.json')
    out = {}
    for r in recs:
        words = [s1.canon(t['label_repo'] or '')
                 for t in r['tokens'] if t['type'] == 'signgroup']
        words = dedupe_block(strip_noise(words))
        if any(ANCHOR.search(w) for w in words):
            out[r['record_id']] = words
    return out


def younger_reading() -> dict[str, list[str]]:
    y = json_load('data/younger_freetext.json')
    out = {}
    for k, toks in y.items():
        if k in JUNK:
            continue
        words = [s1.canon(t['val']) for t in toks]
        words = dedupe_block(strip_noise(words))
        if any(ANCHOR.search(w) for w in words):
            out[k] = words
    return out


# --- Slot identification ---------------------------------------------------
# Group word forms into formula slots by sign-string similarity. Deliberately
# crude: the alternative is imposing the published schema, which would make the
# recovery circular.
def cluster(words) -> dict[str, str]:
    """Group word forms into slots by sign-string similarity."""
    reps, assign = [], {}
    for w in sorted(words, key=lambda x: (-len(x), x)):
        placed = False
        for r in reps:
            if difflib.SequenceMatcher(None, w, r).ratio() >= SIM:
                assign[w] = r; placed = True; break
        if not placed:
            reps.append(w); assign[w] = w
    return assign


def analyse(texts, label) -> tuple[dict[str, set[str]], list[str], collections.Counter[str]]:
    freq = collections.Counter(w for ws in texts.values() for w in ws)
    recurrent = {w for w, n in freq.items() if n >= 2}
    assign = cluster(recurrent)

    # mean relative position of each slot
    pos = collections.defaultdict(list)
    for ws in texts.values():
        n = len(ws)
        if n < 2:
            continue
        for i, w in enumerate(ws):
            if w in assign:
                pos[assign[w]].append(i / (n - 1))
    slots = sorted(pos, key=lambda slot: sum(pos[slot]) / len(pos[slot]))

    members = collections.defaultdict(set)
    for w, r in assign.items():
        members[r].add(w)

    print(f'\n=== {label} ===')
    print(f'  records {len(texts)} | word tokens {sum(len(v) for v in texts.values())} '
          f'| types {len(freq)} | recurrent types {len(recurrent)} '
          f'| slots {len(slots)}')
    print(f'  {"slot":>4}  {"pos":>5}  {"n":>4}  variants')
    for i, s in enumerate(slots, 1):
        mp = sum(pos[s]) / len(pos[s])
        v = sorted(members[s], key=lambda w: -freq[w])
        vs = ', '.join(f'{w}({freq[w]})' for w in v[:5])
        print(f'  {i:>4}  {mp:5.2f}  {len(pos[s]):>4}  {vs}')
    return {s: members[s] for s in slots}, slots, freq


SLOT_KEYS = ['ATAI*301WAJA', 'JASASARAME', 'SASARAME', 'ASASARAME',
             'UNAKANASI', 'IPINAMA', 'SIRUTE']


def _slot(w) -> str:
    return 'SASARA-slot' if w in ('JASASARAME', 'SASARAME', 'ASASARAME') else w


# --- Word order ------------------------------------------------------------
# Pairwise precedence, NOT mean position. Mean position fails on fragmentary
# texts because a missing head shifts every index, and it produced an ordering
# that contradicted the literature before this was corrected.
def precedence(texts) -> collections.Counter[tuple[str, str]]:
    """Pairwise order constraints. More robust than mean position on
    fragmentary texts, where a missing head shifts every index."""
    c = collections.Counter()
    for ws in texts.values():
        idx = {}
        for i, w in enumerate(ws):
            if w in SLOT_KEYS:
                idx.setdefault(_slot(w), i)
        for x in idx:
            for y in idx:
                if x != y and idx[x] < idx[y]:
                    c[(x, y)] += 1
    return c


def report_order(texts, label) -> set[tuple[str, str]]:
    c = precedence(texts)
    pairs, contra = [], 0
    seen = set()
    for (x, y), n in sorted(c.items(), key=lambda kv: -kv[1]):
        if (y, x) in seen:
            continue
        seen.add((x, y))
        r = c.get((y, x), 0)
        if n + r >= 2:
            pairs.append((x, y, n, r))
            if r:
                contra += 1
    print(f'\n  --- {label}: pairwise precedence ---')
    for x, y, n, r in pairs:
        print(f'    {x:14s} before {y:14s}  {n} vs {r}')
    print(f'    contradicting pairs: {contra}')
    return {(x, y) for x, y, n, r in pairs if r == 0}


def main() -> None:
    a, b = our_reading(), younger_reading()
    sa, _, _ = analyse(a, 'READING A (Douros / our source)')
    sb, _, _ = analyse(b, 'READING B (Younger)')

    # --- what survives both readings --------------------------------------
    print('\n\n=== BOUNDARY-STABLE RESULTS (present under both readings) ===')
    stable, only_a, only_b = [], [], []
    for s, v in sa.items():
        match: tuple[float, str | None] = max(
            (difflib.SequenceMatcher(None, s, t).ratio(), t) for t in sb
        ) if sb else (0.0, None)
        best = match[1]
        if match[0] >= SIM and best is not None:
            stable.append((s, best, v, sb[best]))
        else:
            only_a.append((s, v))
    matched_b = {t for _, t, _, _ in stable}
    for t, v in sb.items():
        if t not in matched_b:
            only_b.append((t, v))

    print(f'\n  slots recovered under BOTH readings : {len(stable)}')
    for slot_a, slot_b, va, vb in stable:
        same = 'identical' if va == vb else 'variants differ'
        print(f'    {slot_a:24s} <-> {slot_b:24s}  [{same}]')
        if va != vb:
            print(f'      A only: {sorted(va - vb)}')
            print(f'      B only: {sorted(vb - va)}')

    if only_a:
        print(f'\n  slots present ONLY under reading A ({len(only_a)}):')
        for slot, variants in only_a:
            print(f'    {slot}  {sorted(variants)}')
    if only_b:
        print(f'\n  slots present ONLY under reading B ({len(only_b)}):')
        for slot, variants in only_b:
            print(f'    {slot}  {sorted(variants)}')

    print('\n\n=== FORMULA ORDER (derived, not assumed) ===')
    ca = report_order(a, 'READING A')
    cb = report_order(b, 'READING B')
    print(f'\n  constraints identical across readings: {ca == cb}')
    print(f'  shared constraints: {len(ca & cb)}  |  A-only: {len(ca - cb)}  '
          f'|  B-only: {len(cb - ca)}')

    with open('data/formula_dual.json', 'w', encoding='utf-8') as _f:
        json.dump({'stable': [[a, b, sorted(va), sorted(vb)] for a, b, va, vb in stable],
               'only_A': [[slot, sorted(v)] for slot, v in only_a],
               'only_B': [[slot, sorted(v)] for slot, v in only_b]}, _f,
              ensure_ascii=False, indent=1)
if __name__ == '__main__':
    main()
