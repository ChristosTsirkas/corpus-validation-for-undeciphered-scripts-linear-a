# Tests

```bash
python3 tests/test_pipeline.py        # no pytest required
python3 -m pytest tests/ -v           # or with pytest, for nicer output
```

53 tests. **Most of them need generated data to be present, and will SKIP —
not fail — if it isn't.** This is deliberate: the suite has to be meaningful
on a fresh clone, before anything has been built, so absence of data is
reported as "skipped, here's why" rather than a wall of failures.

## What you need, and what runs without it

- Full setup and pipeline instructions are in
  - `setup.sh` (clones `raw_repo/` and `nd/`, the two upstream sources).
  - `src/run_all.sh` (runs every data generation stage, in order, in one command).  
 You should run these files in sequence.  
 The main `README.md`'s "Reproducing this" section walks through both end to end.
- SigLA is separate data, and deliberately opt-in, by using `python3 src/extract_sigla.py --fetch`.  
  It is publicly served and openly licensed (CC BY-NC-SA 4.0), so retrieving it is
  lawful; but taking on a license's obligations should be a knowing act, not a side effect.

| you have present                                                                   | additional tests unlocked                                                                                                                                                                            | running total |
|------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| nothing built, not a git checkout                                                  | 23 — pure-function tests on hand-constructed input (need only `src/` itself), `TestRegister` (`divergences.json` ships committed), `TestPowerAnalysisFigure` (`power_analysis.json` ships committed) | 23 of 53      |
| + `nd/` (`./setup.sh`)                                                             | 3 (`TestPackardNames`)                                                                                                                                                                               | 26 of 53      |
| + `data/corpus_v1.json` (`node src/extract_raw.js && python3 src/build_corpus.py`) | 13 (`TestCorpusSchema` ×5, `TestPublishedFigures` ×5, `TestD4Correction.test_correction_applied`, `TestKuroDamageBreakdown` ×2)                                                                      | 39 of 53      |
| + `data/signgroups_by_genre.json` (`python3 src/structural.py`)                    | 3 (`TestRotationNulls`)                                                                                                                                                                              | 42 of 53      |
| + `data/sigla_corpus.json` (`python3 src/extract_sigla.py --fetch`)                | 5 (`TestSiglaDecoder` ×2, `TestD4Correction.test_matches_sigla`, `TestSiglaCoverage.test_real_data_matches_paper_figures`, `TestSweep3Figure`)                                                       | 47 of 53      |
| + `data/younger_tokens.json` (`python3 src/parse_younger.py`)                      | 1 (`TestSweep1Figure`)                                                                                                                                                                               | 48 of 53      |
| + `data/younger_freetext.json` (`python3 src/parse_younger_freetext.py`)           | 2 (`TestSweep2Figure`, `TestFormulaDualFigure`)                                                                                                                                                      | 50 of 53      |
| + a git checkout (not just an unzipped copy)                                       | 3 (`TestLicensingHygiene`)                                                                                                                                                                           | the full 53   |

`./src/run_all.sh` runs every generation stage above in the right order in one
command (SigLA excepted, by design — see above). `./data/verify.sh` reports
exactly what's present, what's missing, and the exact command that produces
it.

## Why some tests need a git checkout specifically, not just the files

`TestLicensingHygiene`'s three tests aren't about whether the data files
exist — they're about whether git would **publish** them. `.gitignore` stops
a file from being *added*, but does not untrack a file that was already added
before the ignore rule existed. Checking this needs an actual `.git` directory
(`git ls-files`, `git check-ignore`); on a plain unzipped copy of the
repository there's nothing to check against, so these three skip rather than
report a false pass.

## Why one test can skip even with everything present

`test_corpus_checksum` (in `TestPublishedFigures`) skips — not fails — if
`data/corpus_v1.json`'s md5 doesn't match the snapshot the paper was written
against. Upstream corpora are living scholarly resources and can change; a
mismatch means the specific figures in the paper may no longer describe your
build, not that anything is broken. The other `TestPublishedFigures` tests
still run against whatever you have and will fail normally if the numbers are
actually wrong for your snapshot.

## Reading the output

`OK (skipped=N)` is a healthy result on a partial build — check the skip
reasons (printed per-test) against the table above before assuming something
is wrong. A `FAILED` other than the one named at the top of this file means
an actual problem, on data you do have present.
