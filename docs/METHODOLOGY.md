# Methodology: exact commands

This document records precisely how every figure in the paper was produced, so
that a reader can reproduce any single result without running the whole pipeline
or reading the source.

## Environment

Developed on Python 3.12, tested to 3.14 (3.10+ required); Node.js 22 (18+ required),
`scipy` 1.17.1, `beautifulsoup4` 4.14.3, on Ubuntu 24.04.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Node is required only for stage S0: the upstream corpus is a JavaScript `Map`,
not JSON, and is evaluated rather than parsed.

**All commands are run from the repository root.** Every path in the pipeline is
root-relative; running from `src/` produces `FileNotFoundError`.

**All random procedures are seeded with 20260731.** Reported permutation figures
are therefore exactly reproducible, not merely statistically similar.

## 1. Obtaining the inputs

```bash
./setup.sh
```

Clones `mwenge/lineara.xyz` (the Linear A corpus) into `raw_repo/` and
`j-luo93/NeuroDecipher` (the Linear B lexicon) into `nd/`. Installs Python
dependencies.

It deliberately does **not** fetch the SigLA database; see `data/README.md` for
why, and for how to obtain it under its license. SigLA is separate data, and deliberately opt-in, by using `python3 src/extract_sigla.py --fetch`.  
  It is publicly served and openly licensed (CC BY-NC-SA 4.0), so retrieving it is
  lawful; but taking on a license's obligations should be a knowing act, not a side effect.

### Checking what you have

```bash
./data/verify.sh
```

Reports presence, size and checksum for every input, names the command that
produces anything missing, and verifies record counts against the published
snapshot. `data/README.md` documents each file, its provenance and its
checksums in full.  
If you encounter a difference in the md5 checksum of ``data/corpus_v1.json``, you
should accordingly update the value of ``CORPUS_MD5`` in ``tests/test_pipeline.py``

## 2. Running everything

```bash
./src/run_all.sh
```

Sixteen stages in dependency order. Takes roughly four minutes; the permutation
tests dominate. Stages requiring SigLA report the absence and skip.

## 3. Running one result

Stages must run in order because later ones consume earlier outputs. To
reproduce a single figure, run stages S0 and S1 first, then the stage you want.

| To reproduce                                 | Run                                                              | Paper      |
|----------------------------------------------|------------------------------------------------------------------|------------|
| the corpus itself                            | `node src/extract_raw.js && python3 src/build_corpus.py`         | §4.1       |
| genre split, positional profile              | `python3 src/structural.py`                                      | §5.1, §5.4 |
| sweep 1, 92.0%                               | `python3 src/parse_younger.py && python3 src/sweep1.py`          | §4.5       |
| sweep 2, 94.7% / 80.6%                       | `python3 src/parse_younger_freetext.py && python3 src/sweep2.py` | §4.5       |
| sweep 3, 95.9%                               | `python3 src/sweep3.py`                                          | §4.5       |
| affixation, z = +5.91                        | `python3 src/typology.py && python3 src/affix_null.py`           | §5.5       |
| grid feasibility, z = −1.63                  | `python3 src/grid_feasibility.py && python3 src/grid_null.py`    | §6.1       |
| entropy, H2 adequacy failure                 | `python3 src/entropy.py`                                         | §5.3, §6.2 |
| vowel dependency                             | `python3 src/phonology_test.py`                                  | §6.3       |
| three-vowel re-specification                 | `python3 src/phonology_3v.py`                                    | §6.3       |
| power calibration                            | `python3 src/power.py`                                           | §6.3       |
| formula, both readings                       | `python3 src/formula_dual.py`                                    | §5.6       |
| KU-RO arithmetic                             | `python3 src/kuro_test.py --fractions`                           | §5.7       |
| Packard alternations, 1.55:1                 | `python3 src/packard_v4.py`                                      | §8.3       |
| Packard name parallels, 4.74:1               | `python3 src/packard_names.py`                                   | §8.4       |
| record-level permutation                     | `python3 src/validate_final.py`                                  | §5.2, §5.4 |
| scribal clustering (null)                    | `python3 src/scribal.py`                                         | §9         |
| sparse-data smoothing test — **SLOW=1 only** | `python3 src/smoothing_test.py`                                  | §6.2       |
| affix-direction power — **SLOW=1 only**      | `python3 src/affix_power.py`                                     | §5.5       |

`SLOW` only matters to `run_all.sh` (below) — it decides whether *that
script* invokes these two stages at all. Running either script directly, as
above, always runs it; there is no environment variable to set. `VAR=1
command` (used below for `run_all.sh`) is bash/zsh syntax.

### SigLA-dependent stages

```bash
python3 src/extract_sigla.py --input /path/to/database.js \
                             --output data/sigla_corpus.json
python3 src/sweep3.py
```

Required for sweep 3, and for verifying the D4 correction and the D12
resolution. `build_corpus.py` applies the D4 correction unconditionally, from
the site list established in §4.2; SigLA is needed to *verify* it, not to apply
it.

### Superseded implementations

`packard.py`, `packard_v2.py` and `packard_v3.py` are earlier, **incorrect**
versions of the Packard replication, retained deliberately. §8.2 of the paper
documents why each was wrong. They are not part of `run_all.sh` but
`packard_v4.py` imports helpers from `packard.py` and `packard_v3.py`.

### Slow stages, and reproducing one condition

Stages A10 (sparse-data smoothing) and A11 (affix-direction power) are excluded
from the default `run_all.sh` because A11 takes roughly twenty minutes: eight
skew conditions, twenty-five replications each, two hundred permutations per
replication, with affix relations recomputed over ~500 types every time.

```bash
SLOW=1 ./src/run_all.sh          # include them - On Windows Git Bash, not
                                 # PowerShell/cmd (VAR=value is bash syntax)
```

Published results are bundled at `data/power_analysis.json`, so re-running is
optional. To verify a single condition — the 59% case is the one that matters,
since it is the received figure in the literature — takes about two minutes:

```python
import sys, json, random, statistics
sys.path.insert(0, 'src')
import affix_power as ap
random.seed(20260731 + 59)
g = json.load(open('data/signgroups_by_genre.json', encoding='utf-8'))
real = sorted({tuple(t) for t in g['administrative'] if len(t) > 1})
lengths = [len(t) for t in real]
signs = sorted({s for t in real for s in t})
zs = []
for _ in range(25):
    syn = ap.make_corpus(len(real), lengths, signs, 0.59, affix_rate=0.13)
    o, m, z, n = ap.detect(sorted(set(syn)), trials=200)
    if z is not None:
        zs.append(z)
print('mean z:', statistics.mean(zs),
      '| detected:', sum(1 for z in zs if abs(z) > 1.96), '/', len(zs))
```

Expected: mean z ≈ +0.30, detected 0 / 25.

## 4. Tests

```bash
python3 tests/test_pipeline.py          # no dependencies
python3 -m pytest tests/ -v             # if pytest installed
```

Three groups:

- **licensing hygiene** — asserts no third-party corpus data is committed
- **structural invariants** — schema, damage/complete consistency, measure
  confidence grades, the D4 correction
- **published figures** — the paper's claims as assertions

Tests requiring unbuilt data skip rather than fail, so the suite is meaningful
on a fresh clone.

**On failure of a published-figure test:** this is informative, not a defect. It
means the upstream corpus has changed and the paper's numbers no longer describe
the data. `test_corpus_checksum` compares against the md5 of the snapshot used
for the paper (`2f5c936f0848fcbcb4ef35669eccca99`) and skips the dependent
assertions if it differs, so you will see *why* before you see the failures.

This is not hypothetical. During development these tests caught a stale figure:
the phantom-type inflation reported as 383 was computed before two later
corrections and is 374 on the corrected corpus. The paper carries the corrected
figure.

## 5. Method notes that affect interpretation

**Comparison is on sign identifiers, never on labels.** Editions differ in
naming convention far more than in reading. `sweep1.py` carries an alias table
folding documented equivalences (FIC/NI, VINa/VIN, CYP/\*303, QIf/\*21F) before
counting. Without it, agreement reads 70.5% instead of 92.0%, almost all the
difference being spurious.

**Damaged tokens are excluded from all structural analysis.** A fragment's first
sign is not evidence of word-initial position.

**Single-sign tokens are excluded from positional and affix work**, since such a
token is trivially both initial and final.

**Register comparisons permute at document level, not word level.** Words within
a document share a scribe, a document type and a subject.

**Fraction values follow Corazza et al. (2021)** and carry a confidence grade.
Analysis code must filter on `confidence` before consuming `value_conjecture`.

## 6. Expected runtime

| stage group                     | approx. |
|---------------------------------|---------|
| S0–S2 corpus build              | 5 s     |
| V1–V4 sweeps 1–2                | 25 s    |
| A1–A4 affixation, grid          | 45 s    |
| A5–A7 entropy, phonology, power | 90 s    |
| A8–A9 formula, KU-RO            | 5 s     |
| P1–P2 Packard                   | 60 s    |
| A10 smoothing (SLOW=1)          | 60 s    |
| A11 affix power (SLOW=1)        | ~20 min |
| V5–V6 validation, sweep 3       | 40 s    |
