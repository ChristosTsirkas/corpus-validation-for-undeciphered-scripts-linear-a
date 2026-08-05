#!/usr/bin/env python3
"""
Packard's Table 14 test - Linear B name parallels. His LOAD-BEARING evidence.

CRITERION (p. 89-90, verbatim in substance):
  "For the purpose of confirming the phonetic values, the most significant
   parallels are those involving Linear B sign-groups attested at Knossos as
   personal names or as place names. The chance of error is further reduced by
   requiring both sign-groups to be complete and longer than two signs."
  Matches counted when the initial two signs are identical as well as the
  consonant of the third sign; the final vowel or an obvious Linear B suffix
  may be disregarded, since a non-Greek name might be accommodated to a Greek
  inflectional pattern.

  His result: fifteen matches - three exact, eight where the final vowel
  differs, four differing by a recognizable Linear B suffix - against an average
  of about three for the nine random decipherments. Table 14 gives Knossos
  Name 3= at 13 against 3 (ratio 4.3, weight 5) and Name 4= at 2 against 0
  (weight 10).

WHY THIS IS THE TEST THAT MATTERS
Our replication of the internal alternations (packard_v4.py) reproduced his weak
categories. He says himself that the name parallels are what "demonstrates
conclusively that at least some of the Linear B phonetic values are valid for
Linear A" (p. 92). That claim has never been re-tested.

DATA
Linear B lexicon from Luo, Cao & Barzilay (ACL 2019), j-luo93/NeuroDecipher,
`linear_b-greek.cog` (919 pairs) and `linear_b-greek.names.cog` (proper nouns
flagged). Linear B words are in Unicode syllabograms whose character names carry
both the B-number and the value, giving a direct concordance with our AB ids.

KNOSSOS RESTRICTION (resolved; TODO.md "Completed", docs/DAMOS.md, docs/PACKARD.md)
Packard's own criterion requires the Linear B sign-group to be attested at
KNOSSOS as a personal or place name - not just present somewhere in the
Linear B corpus. `load_linear_b(names_only=True)` alone doesn't enforce
that. `load_linear_b_knossos_names()` intersects it against DAMOS (Database
of Mycenaean at Oslo, damos.hf.uio.no, CC BY-NC-SA 4.0), restricted to the
Knossos find-site, by exact transliteration match: 429 candidate names ->
154 that are actually Knossos-attested. This is the criterion now used as
the headline figure; the unrestricted 429 is kept alongside in main() for
comparison, since it's what every earlier figure in this project used.
`data/damos_knossos_deduplicated.csv` is not redistributed (see
`data/README.md` item 5b) - obtain your own export from the DAMOS site.
"""
import unicodedata, re, csv, collections, random, statistics

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from corpus_io import json_load, read_text  # noqa: E402
import packard as pk  # noqa: E402


random.seed(20260731)
VOWELS = 'aeiou'
LB_RE = re.compile(r'^LINEAR B SYLLABLE (B\d+|\w+) (.+)$')


def lb_value(ch) -> str | None:
    m = LB_RE.match(unicodedata.name(ch, ''))
    return m.group(2).lower() if m else None


def load_linear_b(names_only=True) -> list[tuple[str, ...]]:
    """Return list of Linear B words as tuples of values."""
    words = []
    path = 'nd/data/linear_b-greek.names.cog' if names_only else 'nd/data/linear_b-greek.cog'
    for line in read_text(path).split('\n')[1:]:
        if not line.strip():
            continue
        parts = line.split('\t')
        lb = parts[0]
        gloss = parts[1] if len(parts) > 1 else ''
        if names_only and gloss.strip() == '_':
            continue
        vals = [lb_value(c) for c in lb]
        if all(vals) and len(vals) > 2:
            words.append(tuple(vals))
    return words


def load_damos_knossos_words(path: str = 'data/damos_knossos_deduplicated.csv') -> set[str]:
    """DAMOS's Knossos-find-site word export, deduplicated: hyphenated
    transliterations (e.g. 'a-ke-u'), lower-cased. See data/README.md 5b."""
    words = set()
    with open(path, encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            w = row.get('wordsortcontent', '').strip().lower()
            if w:
                words.add(w)
    return words


def load_linear_b_knossos_names(names_only: bool = True) -> list[tuple[str, ...]]:
    """Packard's own criterion, tightened: Linear B words that are both (a)
    personal/place names (NeuroDecipher .names.cog) and (b) attested at
    Knossos specifically (DAMOS), complete and longer than two signs."""
    knossos = load_damos_knossos_words()
    return [w for w in load_linear_b(names_only) if '-'.join(w) in knossos]


def split_val(v: str) -> tuple[str, str]:
    v = ''.join(c for c in v if not c.isdigit())
    for i, ch in enumerate(v):
        if ch in VOWELS:
            return v[:i], v[i]
    return v, ''


def matches(la_words, lb_words, vmap) -> int:
    """Packard's criterion: first two signs identical, consonant of third
    identical; both words complete and longer than two signs."""
    index = collections.defaultdict(set)
    for w in lb_words:
        c3, _ = split_val(w[2])
        index[(w[0], w[1], c3)].add(w)
    hits = 0
    for w in la_words:
        try:
            v = [vmap[s] for s in w[:3]]
        except KeyError:
            continue
        c3, _ = split_val(v[2])
        if (v[0], v[1], c3) in index:
            hits += 1
    return hits


def rotations(vmap, types, group_size=10) -> list[tuple[dict[str, str], list[list[str]]]]:
    freq = collections.Counter(s for t in types for s in t)
    ordered = sorted(vmap, key=lambda s: (-freq.get(s, 0), s))
    groups = [ordered[i:i + group_size] for i in range(0, len(ordered), group_size)]
    if len(groups) > 1 and len(groups[-1]) < 2:
        # See packard_v4.rotation_nulls: a trailing group of size 1 can never
        # be rotated away from its true value. Merge it into the previous group.
        groups[-2].extend(groups.pop())
    out = []
    for k in range(1, group_size):
        perm = {}
        for g in groups:
            vals = [vmap[s] for s in g]
            perm.update(dict(zip(g, vals[k % len(g):] + vals[:k % len(g)])))
        out.append((perm, groups))
    return out


DAMOS_HELP = """\
  data/damos_knossos_deduplicated.csv not found - this row needs a DAMOS
  Knossos word export, which this project does not redistribute (third-party
  data, CC BY-NC-SA 4.0). To get it:
    1. https://damos.hf.uio.no/ -> Word Search, find-place = Knossos
    2. export the results as CSV
    3. save the export as data/damos_knossos_deduplicated.csv
  Full instructions: data/README.md, item 5b.
  Continuing without this row - the other two (unrestricted names, full
  lexicon) don't need it."""


def main() -> None:
    g = json_load('data/signgroups_by_genre.json')
    types = sorted({tuple(t) for t in
                    [tuple(x) for x in g['administrative'] + g['religious']]
                    if len(t) > 2})          # longer than two signs, per Packard
    vmap_cv = pk.build_values()
    vmap = {k: (c + v) for k, (c, v) in vmap_cv.items()}

    sources: list[tuple[str, list[tuple[str, ...]]]] = []
    try:
        sources.append(('Linear B NAMES, Knossos-restricted (DAMOS)',
                         load_linear_b_knossos_names(True)))
    except FileNotFoundError:
        print('\n=== Linear B NAMES, Knossos-restricted (DAMOS): SKIPPED ===')
        print(DAMOS_HELP)

    sources.append(('Linear B NAMES only (unrestricted, superseded)', load_linear_b(True)))
    sources.append(('Linear B full lexicon', load_linear_b(False)))

    for label, lb in sources:
        random.seed(20260731)  # per-source, so results don't depend on list order
        obs = matches(types, lb, vmap)
        print(f'\n=== {label} ===')
        print(f'  Linear B words (3+ signs) : {len(lb)}')
        print(f'  Linear A types (3+ signs) : {len(types)}')
        print(f'  matches, TRUE values      : {obs}')

        rots = rotations(vmap, types)
        counts = [matches(types, lb, p) for p, _ in rots]
        print(f'  his nine rotations        : {counts}')
        print(f'  average                   : {float(statistics.mean(counts)):.2f}')
        r = obs / float(statistics.mean(counts)) if float(statistics.mean(counts)) else float("inf")
        print(f'  ratio                     : {r:.2f} : 1')
        print(f'  rotations beating observed: {sum(1 for c in counts if c >= obs)}/9')

        _, groups = rots[0]
        null = []
        for _ in range(2000):
            perm = {}
            for grp in groups:
                bv = [vmap[s] for s in grp]
                random.shuffle(bv)
                perm.update(dict(zip(grp, bv)))
            null.append(matches(types, lb, perm))
        m, s = float(statistics.mean(null)), float(statistics.pstdev(null))
        p = (sum(1 for v in null if v >= obs) + 1) / 2001
        print(f'  2000 banded permutations  : {m:.2f} +/- {s:.2f}'
              f'   z = {(obs-m)/s if s else 0:+.2f}   p = {p:.4f}')
        print('  [Packard: 15 matches vs ~3 random = 5:1; Table 14 ratio 4.3]')


if __name__ == '__main__':
    main()
