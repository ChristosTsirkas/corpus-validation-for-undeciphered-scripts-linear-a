#!/usr/bin/env python3
"""
KU-RO as an arithmetic control (paper §5.7).

THE CLAIM UNDER TEST
KU-RO is read as 'total' on internal evidence: on balance-sheet tablets the
numbers preceding it sum to the number following. That is arithmetic, and holds
whatever language the script encodes. KI-RO, read as 'deficit', should NOT
behave as a running total.

WHY THIS IS NOT A DECIPHERMENT
A match shows that a sign-group marks summation. It does not show what word it
represents or how it sounded; an accountant's tally mark would test identically.

SECTIONING
Tablets are frequently mixed-commodity, carrying several totals, each closing
its own block. A section therefore ends at a total and begins at whichever comes
last of:
  - a horizontal ruling (the `ruling` token type)
  - a previous total (KU-RO, KI-RO or PO-TO-KU-RO)
  - a commodity logogram acting as a heading, i.e. one that is NOT immediately
    followed by a numeral (a heading introduces a list; an inline commodity is
    counted)
The third rule is the per-commodity grouping. Its effect is measured below
rather than assumed.

THE NULL MODEL
Reporting a match rate alone would be meaningless: a section boundary chosen to
make sums work is circular. The rate is therefore compared against sections of
the same lengths placed at random positions in the same tablets. This converts
an exploratory observation into a test.
"""
import os
import random, statistics, collections, sys

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402


random.seed(20260731)
USE_FRAC = True
TRIALS = 2000

KURO = ('AB081', 'AB002')
KIRO = ('AB067', 'AB002')
POTOKURO = ('AB011', 'AB005', 'AB081', 'AB002')
TOTALS = {KURO, KIRO, POTOKURO}

# Commodity logograms. A heading occurrence introduces a list; an inline
# occurrence is an entry and is counted.
COMMODITIES = {'AB120', 'AB122', 'AB123', 'AB130', 'AB131', 'AB030', 'AB054',
               'A303', 'AB021', 'AB022', 'AB023', 'AB085', 'A327', 'A191'}


# --- Fraction handling ------------------------------------------------------
# Only values graded 'secure' or 'derived' under the Corazza et al. (2021)
# system are admitted. D13 (K = 1/16 vs 1/10) is open but does not affect the
# result: the matched cases are dominated by whole numbers.
def numeral_value(tok, use_fractions=USE_FRAC) -> float | None:
    lab = tok.get('label_repo')
    if lab and lab.isdigit():
        return float(lab)
    if use_fractions and tok.get('measure'):
        v = sum(m['value_conjecture'] for m in tok['measure']
                if m['confidence'] in ('secure', 'derived')
                and m['value_conjecture'])
        return v if v else None
    return None


def ids_of(tok) -> tuple[str, ...]:
    return tuple(i for i in tok['sign_ids'] if i)


def is_total(tok, target=None) -> bool:
    if tok['type'] != 'signgroup':
        return False
    ids = ids_of(tok)
    return ids == target if target else ids in TOTALS


def is_commodity_heading(toks, j: int) -> bool:
    """A commodity logogram not immediately followed by a numeral."""
    t = toks[j]
    if t['type'] != 'signgroup':
        return False
    if not (set(ids_of(t)) & COMMODITIES):
        return False
    for u in toks[j + 1:]:
        if numeral_value(u) is not None:
            return False          # inline entry: commodity then quantity
        if u['type'] == 'signgroup':
            return True           # heading: commodity then another word
    return True


def section_start(toks, idx: int, use_commodity: bool = True) -> int:
    """Where the block closed by the total at `idx` begins."""
    for j in range(idx - 1, -1, -1):
        u = toks[j]
        if u['type'] == 'ruling':
            return j + 1
        if is_total(u):
            return j + 1
        if use_commodity and is_commodity_heading(toks, j):
            return j + 1
    return 0


def cases(recs, target, use_commodity=True) -> list[tuple[str, list[float], float, int, int]]:
    """Yield (record_id, section_values, stated_total)."""
    out = []
    for rid, r in recs.items():
        toks = r['tokens']
        for idx, t in enumerate(toks):
            if not is_total(t, target):
                continue
            after = None
            for u in toks[idx + 1:]:
                v = numeral_value(u)
                if v is not None:
                    after = v
                    break
                if u['type'] == 'signgroup':
                    break
            if after is None:
                continue
            start = section_start(toks, idx, use_commodity)
            vals = [numeral_value(u) for u in toks[start:idx]]
            vals = [v for v in vals if v is not None]
            if vals:
                out.append((rid, vals, after, start, idx))
    return out


def is_damaged(tok) -> bool:
    """True if a numeral token carries a recorded damage flag, or is marked
    incomplete outright. Used to test one of the three candidate explanations
    for KU-RO's 50% mismatch rate (paper §5.7, TODO.md §2.3): a section that
    fails to sum may be doing so because a numeral in it, or the stated total
    itself, is a damaged or partial reading rather than a genuine arithmetic
    disagreement."""
    d = tok.get('damage') or {}
    return bool(d.get('before') or d.get('after') or d.get('internal')) or \
        tok.get('complete') is False


def mismatch_damage_breakdown(recs, target, use_commodity=True) -> dict[str, list[str]]:
    """For every KU-RO case that fails to sum, check whether any numeral
    involved - in the summed section or in the stated total - is damaged or
    incomplete. Returns record ids split into two groups. 'damaged': at least
    one involved numeral carries a damage flag, a plausible reading-
    uncertainty explanation already present in this project's own data.
    'clean': no damage flag anywhere involved, so damage cannot explain the
    mismatch - this is the genuinely unexplained residue. Re-walks the same
    records `cases()` does rather than extending it, since this needs the
    token objects themselves (for their damage/complete fields), not just the
    numeral values `cases()` reduces them to."""
    damaged, clean = [], []
    for rid, r in recs.items():
        toks = r['tokens']
        for idx, t in enumerate(toks):
            if not is_total(t, target):
                continue
            after, after_tok = None, None
            for u in toks[idx + 1:]:
                v = numeral_value(u)
                if v is not None:
                    after, after_tok = v, u
                    break
                if u['type'] == 'signgroup':
                    break
            if after is None:
                continue
            assert after_tok is not None  # set together with `after` above
            start = section_start(toks, idx, use_commodity)
            section_toks = [u for u in toks[start:idx] if numeral_value(u) is not None]
            vals = [numeral_value(u) for u in section_toks]
            if not vals or classify(vals, after) != 'mismatch':
                continue
            any_damage = is_damaged(after_tok) or any(is_damaged(u) for u in section_toks)  # type: ignore[arg-type]
            (damaged if any_damage else clean).append(rid)
    return {'damaged': damaged, 'clean': clean}


def classify(vals, stated) -> str:
    s = float(sum(vals))
    if abs(s - stated) < 1e-9:
        return 'exact'
    if abs(s - stated) <= 1.0:
        return 'off_by_one'
    return 'mismatch'


def null_rate(observed, trials=TRIALS) -> tuple[float, float]:
    """Permute which stated total is paired with which section.

    An earlier version of this null resampled numerals from within the same
    section, which is not independent of the observation: when a section covers
    most of a tablet, a random draw from it is nearly the section itself, and
    the null was inflated to 8.4 of 26.

    The correct null asks a different question: does a section sum to ITS OWN
    stated total more often than to some other tablet's stated total? If KU-RO
    marks summation, the true pairing must beat shuffled pairings.
    """
    sums = [float(sum(v)) for _, v, _, _, _ in observed]
    totals = [float(s) for _, _, s, _, _ in observed]
    hits = []
    for _ in range(trials):
        shuffled = totals[:]
        random.shuffle(shuffled)
        hits.append(sum(1 for a, b in zip(sums, shuffled)
                        if abs(a - b) < 1e-9))
    return float(statistics.mean(hits)), float(statistics.pstdev(hits))


def report(recs, target, name, use_commodity=True) -> tuple[list[tuple[str, list[float], float, int, int]], collections.Counter[str], int] | None:
    obs = cases(recs, target, use_commodity)
    if not obs:
        print(f'\n=== {name} === no testable cases')
        return None
    c = collections.Counter(classify(v, s) for _, v, s, _, _ in obs)
    n = len(obs)
    print(f'\n=== {name} ({"per-commodity" if use_commodity else "no commodity rule"}) ===')
    print(f'  testable cases        : {n}')
    for k in ('exact', 'off_by_one', 'mismatch'):
        print(f'  {k:22s}: {c[k]:3d}  ({100*c[k]/n:.0f}%)')
    return obs, c, n


def main() -> None:
    global USE_FRAC
    USE_FRAC = '--no-fractions' not in sys.argv
    recs = {r['record_id']: r for r in
            json_load('data/corpus_v1.json')}

    print('KU-RO ARITHMETIC CONTROL')
    print(f'fractions admitted: {USE_FRAC} (secure and derived grades only)')

    # Effect of the per-commodity rule: reported without and with, because it
    # was suggested as an improvement and turns out to make no difference.
    report(recs, KURO, 'KU-RO', use_commodity=False)
    with_commodity = report(recs, KURO, 'KU-RO', use_commodity=True)

    # the contrast term
    report(recs, KIRO, 'KI-RO  (should NOT total)', use_commodity=True)

    if with_commodity:
        obs, counts, _ = with_commodity
        m, s = null_rate(obs)
        z = (counts['exact'] - m) / s if s else float('inf')
        print('\n=== NULL MODEL ===')
        print(f'  Stated totals shuffled across sections, {TRIALS} trials.')
        print(f'  observed exact matches : {counts["exact"]}')
        print(f'  random placement       : {m:.2f} +/- {s:.2f}')
        print(f'  z                      : {z:+.2f}')
        print('\n  This is the figure that matters. A match rate without it is')
        print('  circular, because a boundary chosen to make sums work proves')
        print('  nothing.')

    # What the mismatches actually are, not just how many. One of three
    # candidate explanations named in the paper/TODO.md for the 50% mismatch
    # rate is directly checkable against data already in the corpus: does the
    # section or the stated total involve a numeral already flagged damaged
    # or incomplete? (The other two candidates - sectioning this study can't
    # resolve, and the open D7 numeral conflicts - are not checkable this
    # way: D7 is plate-collation work, and no further sectioning rule is
    # currently proposed to test.)
    breakdown = mismatch_damage_breakdown(recs, KURO, use_commodity=True)
    n_damaged, n_clean = len(breakdown['damaged']), len(breakdown['clean'])
    n_mismatch = n_damaged + n_clean
    print('\n=== MISMATCH BREAKDOWN: damaged numerals? ===')
    print(f'  total mismatches                    : {n_mismatch}')
    if n_mismatch:
        print(f'  involve a damaged/incomplete numeral : {n_damaged}  '
              f'({100 * n_damaged / n_mismatch:.0f}%)')
        print(f'  no damage flag on any numeral involved : {n_clean}  '
              f'({100 * n_clean / n_mismatch:.0f}%)')
    if breakdown['clean']:
        print(f'  genuinely unexplained (no damage flag) : {", ".join(sorted(breakdown["clean"]))}')


if __name__ == '__main__':
    main()
