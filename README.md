# corpus-validation-for-undeciphered-scripts-linear-a

> ## 🔬 Research Artifact
>
> **AI-assisted. Unverified. Released for discussion and replication.**
>
> This project was produced in extended collaboration with a large language
> model, which wrote the code, ran the analysis and drafted the text. The human
> author directed the work and takes responsibility for releasing it, but
> **claims no expertise in Aegean scripts, historical linguistics or
> philology**, and no part of this work has been peer-reviewed by a specialist.
>
> Procedural rigor was applied throughout — reproducible pipeline, null models,
> power analysis, a documented divergence register, and five substantive claims
> withdrawn before publication — but **procedure is not expertise, and
> reproducibility is not correctness.** The code producing the same numbers
> twice does not make those numbers right about Linear A.
>
> Please read **[`AI_DISCLOSURE.md`](AI_DISCLOSURE.md)** before citing,
> reviewing or building on anything here. Corrections are actively wanted.

**A reproducible audit and adequacy-testing framework for undeciphered-script corpora, with a worked demonstration on Linear A.**

Every attempt at decipherment starts from the data as given — the transcriptions, the readings, the sign identities — without first checking whether any of it can be trusted. This project asks that question before anyone tries to read a single word.

Chris Tsirkas, independent researcher.

This project does **not** attempt a decipherment. It produces a validated corpus,
an auditable defect register, a set of null-tested structural results, and
explicit bounds on what the data can support.

---

## Headline results

| Result                                            | What it means                                                                                                                                                                                                                                                                                                         |
|---------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **A systematic corpus error found and corrected** | A widely used digital Linear A corpus inverts AB21 (sheep) and AB22 (goats) across 14 documents. A third witness agrees with the alternative reading at **15 of 15** attestable sites, in both directions.                                                                                                            |
| **Packard (1974) replicated**                     | First re-run in 52 years. His weak evidence reproduces (alternations 1.55 : 1, p = 0.17); his strong evidence is independently confirmed (Knossos name parallels **4.74 : 1, z = +4.34, p = 0.0020**, on his own Knossos-restricted criterion). His conclusion stands; the figure the field cites is the weaker half. |
| **A dataset recovered**                           | SigLA ships as OCaml `Marshal` blobs with field names discarded. A decoder is included: 802 documents, 5144 attestations, with reading-certainty annotation.                                                                                                                                                          |
| **137 logged disagreements triaged to 9**         | The rest are naming conventions, ligature tokenisation and annotation markers.                                                                                                                                                                                                                                        |
| **Three adequacy bounds**                         | No alternation grid recoverable (below chance). Conditional entropy unestimable by two orders of magnitude. Vowel harmony of strength ≥ 0.10 excluded.                                                                                                                                                                |

---

## Last pipeline verification

**2026-08-04** — full pipeline re-run from a genuinely clean state: fresh
`git clone` of `raw_repo/` and `nd/`, fresh SigLA fetch/decode, every
generated file in `data/` deleted first and rebuilt by
`SLOW=1 ./src/run_all.sh` (both slow stages included, not skipped). Exact
results:

| check                                      | result                                                                                                                                      |
|--------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `corpus_v1.json` checksum                  | MATCH — byte-identical to the published snapshot                                                                                            |
| `sigla_corpus.json` checksum               | MATCH — byte-identical to the published snapshot                                                                                            |
| Sweep 1 / 2 / 3 (three-witness agreement)  | 92.0% / 94.7% (80.6% libation) / 95.9% — all exact                                                                                          |
| Affixation z-scores                        | +5.91 administrative, +6.74 religious — exact                                                                                               |
| Adequacy bounds                            | grid null z = −1.63 / −1.46 (below chance); H2 short by ~2.3 orders of magnitude; vowel harmony max z = +1.33 (not significant) — all exact |
| Packard alternation                        | 1.55 : 1, z = +1.19, p = 0.1665 — exact                                                                                                     |
| Packard name-parallel (Knossos-restricted) | 4.74 : 1, z = +4.34, p = 0.0020 — exact                                                                                                     |
| KU-RO null                                 | z = +13.40 — exact                                                                                                                          |
| Test suite                                 | 48 passed, 3 skipped (git-dependent, expected outside a checkout)                                                                           |
| pyright                                    | 0 errors                                                                                                                                    |

Upstream corpora and this project's own shared code can both drift day to
day, so treat this date, not the one on the paper, as the actual currency of
every figure on this page.

---

## Why this matters beyond Linear A

The Linear A results are a demonstration. The underlying contribution is
relevant to corpus linguistics, quantitative linguistics, digital philology,
and computational linguistics generally — anywhere a corpus is disputed,
incomplete, or unevenly edited across sources:

| Method                                       | Problem it addresses                                                                                                                                                                                                                                                               |
|----------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Adequacy protocol                            | Whether a corpus has enough observations to support a claim, checked before the claim is made — not implicit in most corpus linguistics work.                                                                                                                                      |
| Document-level null models                   | Treating every word in a document as an independent observation is a common pseudo-replication error; permuting by document instead fixes it.                                                                                                                                      |
| Power analysis on negative results           | A "no effect" finding is uninterpretable without knowing what effect size the corpus could actually have detected; this quantifies it.                                                                                                                                             |
| Divergence register                          | A machine-readable, evidence-linked log of disagreements between editions, rather than a silently adopted reading.                                                                                                                                                                 |
| Structured uncertainty                       | Damage, confidence grade, and certainty markers travel with the data instead of being flattened into a single transcription.                                                                                                                                                       |
| Checksums and a verification script          | Anyone can confirm their build matches the one the paper's numbers were actually computed from, rather than trusting it on faith.                                                                                                                                                  |
| A transferable framework, not a one-off tool | None of the methods above know anything about Linear A specifically. Adapting them to a different disputed or undeciphered corpus means replacing the data loader and the sign/edition tables, not rewriting the statistics — see "Using this on a different script" further down. |

None of these seven is a new statistical idea on its own. What's uncommon is
running all of them together on a real, disputed corpus, with the code, the
data-construction steps, and the resulting numbers all public and checkable —
see [`docs/METHODOLOGY_AND_REPRODUCIBILITY.md`](docs/METHODOLOGY_AND_REPRODUCIBILITY.md)
for exactly how.

---

## Quick start

**Prerequisites: Python 3.10+ and Git, on Linux or macOS.**

**Windows is not supported by `setup.sh`.** The upstream Linear A corpus
repository (`mwenge/lineara.xyz`) contains filenames with characters illegal
on Windows/NTFS - confirmed directly, `git clone` itself fails on Windows
with `invalid path` errors for these, independent of anything in this
project's own code. `setup.sh` detects Windows and refuses to attempt the
fetch rather than fail partway or silently drop data. It prints the
repository URL instead: obtaining it, by whatever means, is left to the
user. Everything else in this project runs fine on Windows once `raw_repo/`
and `nd/` exist by whatever route.

```bash
git clone https://github.com/ChristosTsirkas/corpus-validation-for-undeciphered-scripts-linear-a
cd corpus-validation-for-undeciphered-scripts-linear-a
./setup.sh          # fetches the Linear A corpus and Linear B lexicon
./data/verify.sh    # what you have, what is missing, and how to produce it
./src/run_all.sh    # runs the pipeline
```

`./src/run_all.sh` runs every stage below in order, deterministically (seed
20260731 throughout). Each stage is also its own `python3 src/<script>.py`,
runnable independently once its own inputs exist — see
[`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) for the exact command behind any
single figure.

| stage | what it does                                     | script                          |
|-------|--------------------------------------------------|---------------------------------|
| S0    | extract (drops `translatedWords`)                | `src/extract_raw.js`            |
| S1    | build corpus                                     | `src/build_corpus.py`           |
| S2    | genre + structural                               | `src/structural.py`             |
| V1    | parse Younger tabular                            | `src/parse_younger.py`          |
| V2    | sweep 1 (administrative)                         | `src/sweep1.py`                 |
| V3    | parse Younger free-text                          | `src/parse_younger_freetext.py` |
| V4    | sweep 2 (libation/non-tabular)                   | `src/sweep2.py`                 |
| A1    | typology + affixation                            | `src/typology.py`               |
| A2    | affix null model                                 | `src/affix_null.py`             |
| A3    | grid feasibility                                 | `src/grid_feasibility.py`       |
| A4    | grid null model                                  | `src/grid_null.py`              |
| A5    | entropy + adequacy                               | `src/entropy.py`                |
| A6    | phonological inheritance test                    | `src/phonology_test.py`         |
| A7    | power calibration                                | `src/power.py`                  |
| A8    | formula, dual reading                            | `src/formula_dual.py`           |
| P1    | Packard v4 (his rules, alternations)             | `src/packard_v4.py`             |
| P2    | Packard name parallels (Table 14)                | `src/packard_names.py`          |
| A9    | KU-RO arithmetic                                 | `src/kuro_test.py --fractions`  |
| V6    | sweep 3 (SigLA, third witness)                   | `src/sweep3.py`                 |
| A10   | sparse-data smoothing test — **SLOW=1 only**     | `src/smoothing_test.py`         |
| A11   | affix-direction power, ~20 min — **SLOW=1 only** | `src/affix_power.py`            |
| V5    | final permutation validation                     | `src/validate_final.py`         |

A10 and A11 are skipped by default (`SLOW=1 ./src/run_all.sh` to run them);
A11's own published table is bundled at `data/power_analysis.json` for
exactly this reason, so reading the paper never requires the 20-minute run.
**`SLOW=1 ./src/run_all.sh` is bash syntax and, if on Windows, must be run
in Git Bash  — it fails with `CommandNotFoundException` in PowerShell or `cmd`,
since neither treats `VAR=value` as setting an environment variable.**

**[`data/README.md`](data/README.md) gives the exact command for every file
the pipeline needs**, with expected sizes, checksums and record counts, and
`data/verify.sh` checks yours against them.

**No corpus data ships in this repository.** Both corpora are generated on your
machine from their original sources — see [`data/README.md`](data/README.md).
This is deliberate: redistributing convenient copies would require asserting
rights over other people's scholarship that this project does not clearly hold.
`setup.sh` and `run_all.sh` build `corpus_v1.json` for you as stages S0–S1.

To include the SigLA-dependent results:

```bash
python3 src/extract_sigla.py --fetch
```

SigLA's `database.js` is publicly served and licensed CC BY-NC-SA 4.0. `--fetch`
downloads it, caches it locally, prints the license obligations, and decodes it.
Opt-in rather than automatic: taking on a license should be deliberate.

`setup.sh` **deliberately does not fetch the SigLA database.** That dataset is
CC BY-NC-SA 4.0 and obtaining it should be a knowing decision under its license,
not a side effect of running a script. See **[`data/README.md`](data/README.md)**
for how to obtain it, how to generate `sigla_corpus.json` with the included
decoder, and what the license requires of you.

Without it the pipeline runs and every non-SigLA result reproduces; the
SigLA-dependent stages report the file is absent and skip.

Requires Python 3.10+ (tested to 3.14), `scipy`, `beautifulsoup4`, and Node.js (the source corpus is
a JavaScript `Map`). All random procedures are seeded (20260731);
`corpus_v1.json` rebuilds byte-identically (md5 `2f5c936f0848fcbcb4ef35669eccca99`).

---

## Methods precluded by corpus adequacy

A common response to undeciphered scripts is to propose increasingly
sophisticated computational methods. The present work argues that method
complexity cannot compensate for insufficient information. Before a model can
be expected to recover linguistic structure, the corpus must contain enough
independent observations to identify the parameters the model attempts to
estimate.

The adequacy analyses presented here show that this condition is not met for
the present Linear A corpus. Minimal-pair recovery performs below chance,
conditional entropy cannot be estimated within acceptable confidence bounds,
and lexical recurrence is insufficient for stable estimation of higher-order
statistical structure. Consequently, several classes of computational
linguistic methods are presently underdetermined by the available evidence.

| Method                                            | Supported by present corpus? | Reason                                                                                                                                                                                                               |
|---------------------------------------------------|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Morphological segmentation (Morfessor, BPE, etc.) | ❌ No                        | Requires substantially greater lexical recurrence than the corpus contains. Segmentation becomes driven by optimisation assumptions rather than recoverable morphology.                                              |
| Hidden Markov Models for morpheme classes         | ❌ No                        | Transition and emission probabilities cannot be estimated robustly from the available observations. Multiple incompatible models fit the data equally well.                                                          |
| Bayesian cognate scoring                          | ❌ No                        | Requires established lexical correspondences or reliable semantic anchors. Neither exists for an undeciphered corpus of this size.                                                                                   |
| Automatic sound-correspondence discovery          | ❌ No                        | Depends on aligned lexical sets whose existence cannot be demonstrated independently.                                                                                                                                |
| Syllable inventory optimisation                   | ❌ No                        | Several competing inventories satisfy the data equally well. The corpus lacks sufficient information to discriminate among them.                                                                                     |
| Affix alignment                                   | ⚠ Limited                   | Recurring terminal sequences can be detected (consistent with the significant affixation results reported here), but grammatical interpretation, morpheme boundaries, and function remain statistically unsupported. |
| Constraint-based phonotactic modelling            | ❌ No                        | Entropy estimation itself fails adequacy testing; higher-order phonotactic constraints therefore cannot be estimated reliably.                                                                                       |
| Cross-entropy ranking of candidate languages      | ❌ No                        | Rankings would primarily reflect corpus sparsity and preprocessing assumptions rather than genuine linguistic affinity.                                                                                              |
| Statistical translation lattices                  | ❌ No                        | Translation models require semantic correspondences unavailable for an undeciphered corpus.                                                                                                                          |
| Automatic proto-language reconstruction           | ❌ No                        | Requires established cognate sets and regular sound correspondences, neither of which can presently be inferred.                                                                                                     |

These conclusions do not invalidate the methods themselves. Rather, they define
the limits imposed by the available evidence. The obstacle is informational,
not algorithmic. Increasing model sophistication cannot recover information
that the corpus does not contain.

Conversely, methods operating on shallow structural regularities remain
appropriate. The present study demonstrates that permutation-tested affixation,
document-level null models, corpus auditing, divergence analysis, and adequacy
testing all remain statistically identifiable despite corpus sparsity. The
appropriate methodological response to an information-limited corpus is
therefore not greater model complexity but explicit identification of which
questions the available evidence can and cannot answer.

## Repository layout

```
paper/    the paper
docs/     the analysis documents, one per result area
src/      pipeline stages plus the SigLA decoder
tests/    regression tests: licensing hygiene, invariants, published figures
data/     divergences.json and power_analysis.json; corpora, database.js and
          verify.sh live here too — see data/README.md for what's generated
          vs. committed
```

## IDE setup (PyCharm)

Two one-time project settings, neither a code change, both fixing real false
positives rather than muting real ones:

- **Mark `src/` as a Sources Root.** Right-click `src/` → *Mark Directory as →
  Sources Root*. Every stage script does `sys.path.insert(0, ...)` to import
  its siblings at runtime (`corpus_io`, `packard`, `packard_names`, etc.);
  PyCharm's indexer doesn't follow that dynamic pattern on its own, so without
  this it reports every sibling import as unresolved. This is the actual fix,
  not a suppression — the imports become genuinely resolvable to the IDE.
- **Exclude `raw_repo/`, `nd/` and `data`.** Right-click each → *Mark Directory as →
  Excluded*. Both are third-party clones fetched by `setup.sh` (a few
  thousand files between them, including `raw_repo`'s own large `.js` data
  files) — not project source, nothing in them benefits from indexing, and
  leaving them included slows search and inspections across the whole
  project for no return.

One inspection can still misfire after both of the above:
**`PyTypeCheckerInspection` on `os.path.join(ROOT, 'src')`-shaped
expressions** in `tests/test_pipeline.py` — a known weak spot in PyCharm's
own overload resolution for chained `os.path` stdlib calls, not a real type
error (checked independently against pyright in strict mode and mypy — both
report zero issues). `ROOT` and `SRC` in `tests/test_pipeline.py` already
carry explicit `: str` annotations for exactly this reason. If it still
fires, suppress it for that one statement (`Alt+Enter` → *Suppress for
statement*) rather than disabling the inspection project-wide, which would
also silence it somewhere it's caught something real.

## Tests

```bash
python3 tests/test_pipeline.py     # no dependencies beyond the stdlib
python3 -m pytest tests/ -v        # if pytest is installed
```

Requires Python 3.10 or later; tested to 3.14.

> **If `test_corpus_not_committed` fails**, a generated corpus is tracked by git
> and would be published. `.gitignore` does not untrack a file that was already
> added — only `git rm --cached` does:
>
> ```bash
> git rm --cached data/corpus_v1.json data/sigla_corpus.json
> git commit -m "Untrack generated data"
> ```
>
> The files stay on your disk. This is the failure mode the licensing tests
> exist to catch, and it is easy to hit by running `git add -A` before the
> ignore rules were in place.

Three groups: **licensing hygiene** (no third-party corpus data is committed),
**structural invariants** (schema, damage/complete consistency, measure
confidence grades, the D4 correction), and **published figures** (the paper's
claims expressed as assertions).

A published-figure failure is informative rather than a defect: it means the
upstream corpus has changed and the paper's numbers no longer describe the data.
The suite checks the corpus checksum first and skips dependent assertions if it
differs, so you see *why* before you see failures.

These tests earned their place during development by catching a stale figure —
a phantom-type count reported before two later corrections.

Exact commands for reproducing any single result are in
[`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

| document                   | contents                                                                  |
|----------------------------|---------------------------------------------------------------------------|
| `docs/PROCEDURE.md`        | provenance, defect register D1–D13, transformation sequence, three sweeps |
| `docs/PACKARD.md`          | the replication, including all four method corrections                    |
| `docs/STRUCTURE.md`        | registers, positional preference, affixation                              |
| `docs/FORMULA.md`          | libation formula under both contested word divisions                      |
| `docs/NEGATIVE_RESULTS.md` | grid feasibility, scribal clustering                                      |
| `docs/ENTROPY.md`          | H1, the H2 adequacy failure, matched-n comparison                         |
| `docs/PHONOLOGY.md`        | inherited values tested, with power calibration                           |
| `docs/METHODOLOGY.md`      | exact commands for every figure, runtime, method notes                    |
| `TODO.md`                  | outstanding work, plate collation list, stated limitations                |
| `docs/SOURCES.md`          | every source with access status                                           |
| `data/divergences.json`    | machine-readable register of every disagreement                           |

---

## What this contributes

### To Linear A studies

| contribution                                                                                                                                                                                                                        | who it helps                                                                                                        |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| **AB21/AB22 correction.** A widely used digital corpus inverts sheep and goats across 14 documents — invisible to users, undetectable without an independent witness. 57 tokens.                                                    | anyone using that corpus for economic analysis: livestock counts, commodity ratios, personnel-to-animal allocations |
| **SigLA decoder.** 802 documents and 5144 attestations, with certainty and boundary annotation, made available for statistical work.                                                                                                | anyone wanting SigLA data programmatically                                                                          |
| **Packard citation redirect.** The circulating 2:1 is the weak half of his argument, which he discounts himself. The name-parallel figure (4.74:1, p=0.0020, Knossos-restricted per his own criterion) is the half that carries it. | anyone citing Packard as warrant for Linear B sound values in Linear A                                              |
| **Adequacy bounds.** Minimal pairs below chance; conditional entropy short by two orders of magnitude; vowel harmony excluded above strength 0.10.                                                                                  | anyone planning a quantitative study — a checklist of what to stop attempting                                       |
| **Affixation confirmed.** z = +5.91 / +6.74, surviving null testing. Direction is *not* measurable.                                                                                                                                 | morphological analysis of Minoan                                                                                    |
| **KU-RO confirmed as a summation marker.** Sections sum to their own stated total, not another tablet's: z = +13.4. KI-RO, the "deficit" term, matches 0 of 7.                                                                      | the one semantic reading resting on arithmetic rather than language comparison                                      |

### To method, beyond Linear A

The Linear A work is the worked example. The framework is the contribution, and
it is script-agnostic because it asks data-structure questions rather than
script-specific ones.

| component                | what it does                                                  | works for                                 |
|--------------------------|---------------------------------------------------------------|-------------------------------------------|
| Sign identity as data    | prevents transliteration losses                               | any script with a standard sign inventory |
| Structured uncertainty   | preserves damage, reading certainty, measure confidence       | any fragmentary corpus                    |
| Multi-witness comparison | folds conventions, logs disagreements, defers adjudication    | any script with multiple editions         |
| Adequacy protocol        | counts cells against observations; power-calibrates negatives | any corpus, any statistic                 |

The adequacy tests are pure counting: how many signs in the inventory, how many
observations, how many cells in the table, are the observations independent,
what is the power to detect an effect. No script-specific knowledge is required,
and the same arguments close or open the same routes for any corpus of similar
size.

`divergences.json` is likewise transferable: competing readings, their sources,
the kind of conflict, the evidence that would settle it, which analyses are
sensitive to it, and its status.

### What it does *not* do

No decipherment, and the paper argues this corpus cannot support one. No claim
about the affiliation of Minoan. Nothing here overturns Packard, Younger, Douros
or Duhoux; where their work is examined it is substantially vindicated, and
where an earlier draft thought otherwise, the paper records the retraction.

### What a specialist might question

| objection                                     | where it is addressed                                                                                       |
|-----------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| Is the working corpus reliable enough?        | §12.2 — three sweeps at 92.0%, 94.7%, 95.9%. A reviewer may still push.                                     |
| Does the KU-RO control add anything?          | §5.7 — yes, once null-tested: z = +13.4. The raw 38% match rate was misleading in both directions.          |
| Is the adequacy protocol too conservative?    | §6.2 — five sparse-data estimators tested; they contradict each other by 3.3 bits.                          |
| Does it overclaim about the libation formula? | §5.6 — "independent recovery of an accepted result is evidence the method works rather than a new finding". |
| Is the D4 correction complete?                | §12.5 — no. Adjudicated at sign-family level; gender variants unverified.                                   |

### Using this on a different script

This isn't plug-and-play. It's a framework with Linear A worked as the example
throughout: the adequacy protocol, null models, divergence register, and power
analysis are script-agnostic; the data loader, sign inventory, and
edition-alias tables are not. Adapting to another undeciphered corpus means
replacing the loader and alias tables, keeping the methods, and rerunning the
same pipeline stages. See
[`docs/METHODOLOGY_AND_REPRODUCIBILITY.md`](docs/METHODOLOGY_AND_REPRODUCIBILITY.md).

## Method in four parts

1. **Sign identity is the data.** Every ASCII label is a lossy derivative and is
   regenerated from the sign identifier. This resolved three of the first four
   defects at a stroke.
2. **Uncertainty survives ingestion** as structured fields — damage, reading
   certainty, measure confidence — not as punctuation inside a string.
3. **Compare against multiple independent witnesses**, folding documented
   conventions first, logging every residual with the evidence that would settle
   it. Never silently patch: the register is what made the AB21/AB22 error
   detectable as *systematic* rather than scattered.
4. **Test adequacy before computing.** Count the cells, count the observations,
   compare to the requirement. A negative result without a power calibration
   excludes nothing.

---

## What is claimed and what is not

Five substantive claims made during this project were **withdrawn before
publication** and are reported rather than removed: an affix-direction challenge
to Duhoux, a scribal clustering effect that reached p = 9.8 × 10⁻⁸ and was false,
a positional finding, an initial reading of the Packard replication as a
refutation, and a hypothesis about where disagreements concentrate.

No claim is made about the language family of Linear A. The measures that could
discriminate — grid recovery, conditional entropy, vowel dependency — are shown
to be beyond this corpus.

---

## Methodological note

Four times in this project a defect in the comparison tooling produced what
looked like a substantive finding. Each ran toward *more* apparent disagreement,
and one was statistically significant, mechanistically plausible and false.

**Significance testing gives no protection against a systematic artifact, because
the artifact is systematic.** The working rule adopted: a positive result from
automated collation is provisional until the documents driving it have been
inspected by hand.

---

## Open items

See **[`TODO.md`](TODO.md)** for outstanding work, including the specific GORILA
plates required for each unresolved defect, and the stated limitations — notably
that the D4 adjudication is at sign-family level only, since the third witness
does not record the gender variants our source carries.

The machine-readable register is `data/divergences.json`.

---

## License compliance checklist

**If you generate the corpora, these obligations attach to *you*, not to this
repository.** Four sources, four different regimes.

- [ ] **GORILA-derived data** (`corpus_v1.json`) — this project holds no rights
      in the transcriptions and cannot grant permission. Satisfy yourself that
      your use is permitted under applicable law. Cite Godart & Olivier
      (1976–1985). Note that the upstream digital extraction carries **no
      license statement at all**; check whether one has been added since.
      The repository links to sources and clones public repositories; it hosts
      nothing. Reasoning in [`data/README.md`](data/README.md) item 1.
- [ ] **SigLA data** (`sigla_corpus.json`) — attribute Salgarella & Castellan;
      **non-commercial** only; **share alike**. The license attaches to the
      data, not to the Shield-licensed code that processes it.
      [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- [ ] **Linear B lexicon** (`nd/`) — check the
      [NeuroDecipher](https://github.com/j-luo93/NeuroDecipher) repository's own
      license before reusing its data. This project neither redistributes it nor
      asserts anything about its terms.
- [ ] **DĀMOS-derived name list** (not currently in this repository) — if you
      build one yourself, it's CC BY-NC-SA 4.0: attribution, non-commercial,
      share-alike, citing Aurora (2015). Unlike everything else in this
      checklist, there's no `src/*.py` script for this — DĀMOS's search is an
      interactive site, not something this pipeline automates. See
      `docs/DAMOS.md` and `data/README.md` item 5b.
- [ ] **Fraction values** — Corazza et al. (2021), CC BY-NC-ND. Used by citation
      only; the paper is not redistributed.

Full detail in [`LICENSE.md`](LICENSE.md) and
[`data/README.md`](data/README.md).

## Licence

Code (`src/`, `tests/`, `docs/`): **PolyForm Shield 1.0.0** — use, modify,
fork, and redistribute freely, even commercially; the one restriction is
using it to compete with what this project offers using it. Universities,
research institutes, and individual academic/research use are exempt from
that restriction entirely. Paper (`paper/`): **CC BY 4.0**. Third-party data
has different terms and is not relicensed — see [`LICENSE.md`](LICENSE.md)
and [`data/README.md`](data/README.md). SigLA is © Salgarella & Castellan, CC
BY-NC-SA 4.0. GORILA plate images are © École française d'Athènes and are
not redistributed.

## Citation

See `CITATION.cff` for citing this project itself. Depending which
third-party data your use draws on, also cite:

- **The corpus itself** (`corpus_v1.json`, or any figure derived from it):
  Godart, L. & Olivier, J.-P. (1976–1985), *Recueil des inscriptions en
  linéaire A*, Études Crétoises XXI, 1–5, Paris: Geuthner.
- **The cross-witness validation** (sweeps 1 and 2, §5.1–5.2): Younger, J. G.
  (2024), *Linear A Texts and Inscriptions in Phonetic Transcription*.
  https://www.academia.edu/117949876/
- **Sweep 3, the D4 correction, D12, or the D8/D10 triage** (anything
  SigLA-derived): Salgarella, E. & Castellan, S. (2021), "SigLA: The Signs of
  Linear A. A Paleographical Database", *Proceedings of the 5th International
  Conference on Digital Access to Textual Cultural Heritage*.
  https://sigla.phis.me/
- **The Packard name-parallel replication** (§8.4, either the Knossos-restricted
  or unrestricted figure): Luo, J., Cao, Y. & Barzilay, R. (2019), "Neural
  Decipherment via Minimum-Cost Flow: From Ugaritic to Linear B", *Proceedings
  of ACL 2019*, 3146–3155.
- **The Knossos-restricted figure specifically** (§8.4, 154-name criterion):
  also Aurora, F. (2015), "DAMOS (Database of Mycenaean at Oslo). Annotating
  a fragmentarily attested language", in P. A. Fuertes-Olivera et al. (eds.),
  *Current Work in Corpus Linguistics*, Procedia - Social and Behavioral
  Sciences 198, 21–31. doi: 10.1016/j.sbspro.2015.07.415
- **Any replication of, or comparison against, Packard's own findings**:
  Packard, D. W. (1974), *Minoan Linear A*, Berkeley, Los Angeles and London:
  University of California Press.
