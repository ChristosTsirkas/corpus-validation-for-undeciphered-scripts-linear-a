# Methodology and Reproducibility

This document has two jobs. **Part 1** explains, in enough detail that a
reviewer or a technically-minded reader can independently check it, how the
software was built, how the data was produced, and what the pipeline actually
does at every stage — so that reproducing this paper's numbers is a matter of
running commands, not taking anything on faith. **Part 2** explains how to
take this same framework and point it at a different undeciphered script.

Written for two readers at once: an academic with no programming background
who needs to understand what a claim rests on, and a programmer (academic or
otherwise) who needs to actually run or adapt the code. Where the two need
different things, both are given.

---

# Part 1 — How this was built

## 1.1 What the corpus is made of, and under what terms

Nothing in this project's own analysis is built on data this project has the
right to give away. Every corpus is either generated locally from a source
you fetch yourself, or is original output with no third-party content in it.
The short version:

| what                                                              | where it comes from                                                                                             | can it be redistributed?           |
|-------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|------------------------------------|
| Linear A transcriptions                                           | GORILA (Godart & Olivier, 1976–1985) via Douros's tabulation, via a public GitHub mirror (`mwenge/lineara.xyz`) | no — no license statement upstream |
| SigLA comparison corpus                                           | Salgarella & Castellan's SigLA database, decoded from its public web app                                        | no — CC BY-NC-SA 4.0, share-alike  |
| Linear B lexicon                                                  | Luo, Cao & Barzilay (2019), `NeuroDecipher`                                                                     | check that repo's own license      |
| fraction values                                                   | Corazza et al. (2021), cited by number, not copied                                                              | n/a — no data file, just constants |
| this project's own analysis (divergence register, power analysis) | original work                                                                                                   | yes — PolyForm Shield 1.0.0        |

The full reasoning for each row — why building locally instead of shipping a
copy is the right call, what the residual legal exposure is, and exactly what
each license permits — is in `data/README.md`, item by item. That file is the
authority on licensing; this document assumes you've read it and focuses on
mechanics.

**The practical consequence:** a fresh clone of this repository has no corpus
data in it at all. `data/` holds only two committed files
(`divergences.json`, `power_analysis.json`) plus documentation. Everything
else — the working corpus, the SigLA comparison corpus, all intermediate
files — has to be built by you, once, using the commands below. This is
slower than shipping a zip, and that's the point: it means nobody has to trust
that this project was allowed to redistribute what it's shipping, because it
isn't shipping anything.

## 1.2 Environment

```bash
python3 --version   # 3.10 or later — the code uses X | Y union syntax
node --version       # any recent LTS; only extract_raw.js needs it
pip install --break-system-packages scipy beautifulsoup4
```

`scipy` is used for the Mann-Whitney U test (`validate_final.py`) and for
`packard_v3.py`'s scoring. `beautifulsoup4` is used only by the two Younger
HTML parsers (`parse_younger.py`, `parse_younger_freetext.py`). Nothing else
outside the standard library is required for `src/`.

If you intend to check the type annotations (recommended before any code
change — see §1.7):

```bash
npm install -g pyright
```

## 1.3 Obtaining the inputs

```bash
./setup.sh
```

This clones two upstream repositories into the repository root:

- `raw_repo/` — `mwenge/lineara.xyz`, the digital Linear A corpus.
- `nd/` — `j-luo93/NeuroDecipher`, which bundles the Linear B lexicon used for
  one specific replication (§1.6.5).

It deliberately does **not** fetch the SigLA database — that's a separate,
opt-in step, because retrieving another project's data should be a deliberate
act with the license terms read first, not a default. See `data/README.md`
item 3 for why and how.

**Checking what you have, at any point:**

```bash
./data/verify.sh
```

Reports presence, size and checksum for every input against the values the
paper was written against, and prints the exact command to produce anything
missing. A checksum that doesn't match isn't an error — upstream sources are
living scholarly resources and can change — it means the paper's specific
figures may no longer describe your build, and `tests/test_pipeline.py` will
tell you which assertions to disregard rather than failing opaquely.

## 1.4 The pipeline, stage by stage

Running everything, in order:

```bash
node src/extract_raw.js                 # S0
python3 src/build_corpus.py             # S1
python3 src/extract_sigla.py --fetch    # optional, SigLA-dependent stages only
./src/run_all.sh                        # S2 onward
```

or individually, in the order below — later stages generally depend on
earlier ones' output files being present in `data/`.

### Corpus construction (S0–S1)

| stage | script            | input                             | output                         |
|-------|-------------------|-----------------------------------|--------------------------------|
| S0    | `extract_raw.js`  | `raw_repo/LinearAInscriptions.js` | `data/inscriptions_clean.json` |
| S1    | `build_corpus.py` | `data/inscriptions_clean.json`    | `data/corpus_v1.json`          |

`extract_raw.js` runs in Node because the upstream file is a JavaScript `Map`
literal, not JSON — it can't be parsed by a JSON library, it has to be
evaluated. This stage also drops the `translatedWords` field: that field
carries Linear B-derived semantic glosses, which is interpretation layered on
top of the transcription, not the transcription itself, and keeping it would
quietly import someone else's decipherment assumptions into what's supposed to
be raw sign data.

`build_corpus.py` does the real construction work:

- resolves every character in the transcription to its GORILA sign
  identifier (the canonical id, not the ASCII transliteration, which is a
  lossy derivative — see §1.5.1);
- parses damage markers (`[`, `]`, `?`, and combinations) into structured
  boolean flags rather than leaving them embedded in strings;
- annotates numeric measures with a confidence grade, following Corazza et
  al.'s (2021) published fraction values, cited by number rather than copied
  from their paper;
- applies the D4 correction — a systematic AB21/AB22 (sheep/goat)
  sign-identity inversion identified against SigLA, corrected once here at
  build time rather than patched ad hoc downstream.

Expected result: 1721 records, 1621 distinct documents, 2659 complete
sign-groups, checksums in `data/README.md` item 2.

### The SigLA comparison corpus

| stage | script             | input              | output                   |
|-------|--------------------|--------------------|--------------------------|
| —     | `extract_sigla.py` | `data/database.js` | `data/sigla_corpus.json` |

SigLA ships its corpus as two OCaml `Marshal` blobs, escaped as decimal octets
inside JavaScript string literals — not a documented export format, a raw dump
of an OCaml web application's internal serialized state. `Marshal` stores
records positionally: there are no field names in the file, so the data can't
be located by text search, only by implementing the binary format and
recovering the structure from first principles.

`src/ocaml_marshal.py` implements that format — the header, the small-int and
small-string and small-block prefix encodings, the sharing table used for
back-references, and the block/string/double/custom type codes.
`extract_sigla.py` then walks the decoded tree and maps it onto documents and
attestations. Paper Appendix D describes the decoding process, and its
three-way validation (structural recovery producing an independently-correct
reading; cross-checking against SigLA's own public import source; validation
against known published figures), in full.

Expected result: 802 documents, 5144 attestations (4712 confident / 44
doubtful / 388 unreadable-or-unclassified, 104 erasures, 7 ghosts). Checksums
in `data/README.md` item 4.

### Witness parsing and cross-witness comparison

Two independent published sources exist for (some of) the same inscriptions:
John Younger's tabular transcription and free-text commentary, and SigLA. Each
is parsed into the same shape as the working corpus, then compared
sign-by-sign.

| stage   | script                      | input                                     | output                       |
|---------|-----------------------------|-------------------------------------------|------------------------------|
| —       | `parse_younger.py`          | `raw_repo/commentary/*.html`              | `data/younger_tokens.json`   |
| —       | `parse_younger_freetext.py` | `raw_repo/commentary/*.html`              | `data/younger_freetext.json` |
| sweep 1 | `sweep1.py`                 | `corpus_v1.json`, `younger_tokens.json`   | `data/sweep1_findings.json`  |
| sweep 2 | `sweep2.py`                 | `corpus_v1.json`, `younger_freetext.json` | `data/sweep2_findings.json`  |
| sweep 3 | `sweep3.py`                 | `corpus_v1.json`, `sigla_corpus.json`     | `data/sweep3_findings.json`  |

Comparison is on **GORILA sign identifiers**, canonicalized against a table of
known convention aliases (`sweep1.py`'s `canon()` / `base_id()`), because the
two corpora don't use identical sign-naming conventions for the same sign
(e.g. gender-variant suffixes, alternate numbering for the same physical
sign). Comparing on the canonical sign id rather than on the raw label string
is what makes the comparison meaningful rather than an artifact of two
editions' different naming habits.

Results: 92.0% agreement (sweep 1, 411 documents, 3644 tokens), 94.7% (sweep
2, 994 documents, 1167 tokens, this one specifically covering non-tabular
material including the religious corpus), 95.9% (sweep 3, 657 documents, 4105
tokens, all overlapping syllabograms against SigLA). Sweep 2 falls to 80.6% on
the libation subset alone, which carries the most weight for the grammatical
argument and is exactly where D9 (word-division disagreement, see §1.5.2)
concentrates.

**The divergence register** (`data/divergences.json`) is where every
disagreement the sweeps find gets logged — sign, documents, both readings,
and (where adjudicated) which reading was adopted and why. This file is not
purely machine-generated: the sweeps populate it automatically, but genuine
conflicts (as opposed to naming-convention artifacts) get a manual
`triage` entry recording the adjudication decision and its evidentiary basis.
It's original work, PolyForm Shield 1.0.0-licensed, and one of the two files this project does
commit — see §1.6.6 for what "adjudication" means concretely and why it isn't
optional.

### Genre split and formula/word-order analysis

| stage | script            | input                                     | output                          |
|-------|-------------------|-------------------------------------------|---------------------------------|
| —     | `structural.py`   | `corpus_v1.json`                          | `data/signgroups_by_genre.json` |
| —     | `formula_dual.py` | `corpus_v1.json`, `younger_freetext.json` | `data/formula_dual.json`        |

`structural.py` splits sign-groups by genre (administrative vs. religious/
libation, by physical support type) — most downstream statistical tests
(entropy, affix, grid) are run per-genre because pooling genres with different
formulaic structure would blur exactly the distinctions those tests are meant
to detect.

`formula_dual.py` tests whether the libation-formula word order is stable
under *both* available readings of the religious corpus (this project's own,
and Younger's), since D9 means the word boundaries themselves are contested
for this material — a word-order finding that only holds under one reading
would be an artifact of that reading, not a fact about the language.

### Adequacy protocol and null-model testing

This is the statistical core: before testing any linguistic claim, ask
whether the corpus is even large enough to test it, then test it against a
model of chance that respects the corpus's actual structure rather than an
idealized one.

| test                      | script(s)                                          | what it checks                                                                                                                                                                                                                                                                                                   |
|---------------------------|----------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| conditional entropy (H2)  | `entropy.py`                                       | how much a sign's identity is predicted by its predecessor, three estimators (MLE, Miller-Madow, Chao-Shen)                                                                                                                                                                                                      |
| sparse-data circumvention | `smoothing_test.py`                                | whether Good-Turing or Bayesian smoothing can recover a *known* H2 at this sample size — if an estimator can't recover a known answer, it can't be trusted on an unknown one                                                                                                                                     |
| affix direction           | `affix_null.py`, `affix_power.py`                  | prefix-vs-suffix rate against a resampled null, plus a power analysis: synthetic corpora with a known injected effect size, to find the smallest effect this corpus could actually detect                                                                                                                        |
| positional grid           | `grid_null.py`, `grid_feasibility.py`              | sign-by-position distribution against a resampled null                                                                                                                                                                                                                                                           |
| vowel phonotactics        | `phonology_test.py`, `phonology_3v.py`, `power.py` | whether a Linear-B-derived phonetic mapping shows vowel-dependency inherited from Linear A; `phonology_3v.py` re-runs this for a three-vowel Minoan hypothesis (Salgarella 2022) instead of the original five-vowel mapping; `power.py` calibrates the detectable effect size the same way `affix_power.py` does |
| scribal clustering        | `scribal.py`                                       | do reading disagreements concentrate in particular scribal hands (Poisson/binomial rate test, Benjamini-Hochberg corrected across hands)?                                                                                                                                                                        |
| KU-RO arithmetic control  | `kuro_test.py`                                     | does KU-RO ("total") actually sum the preceding column on balance-sheet tablets, and does KI-RO ("deficit") *not* behave the same way — a control that tests arithmetic function, not decipherment, since an accountant's tally mark would pass identically                                                      |
| final null-model pass     | `validate_final.py`                                | re-runs the two remaining claims properly: a pseudo-replication fix (permute by *document*, not by word, since words in one document share a scribe and aren't independent observations) and a multiple-comparisons correction across the positional-preference table                                            |

Each of these has a dedicated doc under `docs/` going into the statistical
reasoning in full (`ENTROPY.md`, `PHONOLOGY.md`, `FORMULA.md`,
`NEGATIVE_RESULTS.md`, `STRUCTURE.md`) — this section is the map, not the
territory.

### Packard replication

Packard (1974) argued Linear A shows phonetic patterning consistent with
partial Linear B readings being valid. That argument was never re-run on a
clean, sign-id-based corpus with an actual null model. Four corrected
versions exist because the first three each had a specific flaw found and
fixed in the next:

| script             | what changed                                                                                                           |
|--------------------|------------------------------------------------------------------------------------------------------------------------|
| `packard.py`       | first replication attempt                                                                                              |
| `packard_v2.py`    | corrected category boundaries                                                                                          |
| `packard_v3.py`    | corrected scoring                                                                                                      |
| `packard_v4.py`    | adds a rotation-null baseline                                                                                          |
| `packard_names.py` | the separate name-parallel test — Packard's own stated strongest evidence, using the Linear B/Greek lexicon from `nd/` |

`docs/PACKARD.md` documents exactly what was wrong with each earlier version
and why the next one fixes it — worth reading if you're inclined to trust the
final numbers without re-deriving them, since the history is the actual
argument for why v4 (and the separate name-parallel test) are the ones to
cite.

### Coverage and typology

| stage | script              | input                      | output                                      |
|-------|---------------------|----------------------------|---------------------------------------------|
| —     | `typology.py`       | `signgroups_by_genre.json` | (printed report; affix candidates by genre) |
| —     | `sigla_coverage.py` | `sigla_corpus.json`        | `data/sigla_coverage.json`                  |

`sigla_coverage.py` is the newest stage: it partitions the 802-record SigLA
decode by physical support and by GORILA Z-series designation, and
cross-checks the result against an independent citation (a 2026 volume
chapter stating SigLA holds "over 770 documents") that wasn't consulted while
`extract_sigla.py` was built. Both partitions land within a document or two of
that figure, which corroborates that SigLA's coverage grew beyond the
administrative-only scope stated in its 2021 founding paper, and by roughly
the expected amount.

## 1.5 Two things worth understanding before touching any result

### 1.5.1 Why sign identity, not the ASCII label, is the data

Every printable ASCII rendering of a Linear A sign (`AB21`, `A028B`, etc.) is
a lossy, convention-dependent derivative of the actual sign identifier. Two
editions can use different ASCII conventions for the literal same sign
(gender-variant suffixes, alternate numbering). Comparing corpora, or testing
any structural claim, on the ASCII string instead of the canonical identifier
means part of what you're measuring is which transliteration convention each
source happened to use — not a fact about the script. This single decision
resolved three of the defect register's first four entries outright, and is
the reason `base_id()` / sign-canonicalization functions appear throughout
`src/` rather than being a one-off fix.

### 1.5.2 What "adequacy" and "adjudication" mean here, concretely

**Adequacy** means: before reporting a statistic, ask whether the corpus has
enough observations *in the relevant cells* to support the claim being tested,
not just enough tokens overall. A conditional-entropy table with 0.025
observations per cell is not made trustworthy by a large total token count.
Several results in this project exist specifically to test whether the corpus
clears this bar (§1.4, "adequacy protocol and null-model testing" above) —
and where it doesn't, the paper says so rather than reporting the number
anyway with a caveat buried in a footnote.

**Adjudication** means: when two sources disagree on a reading, the decision
about which to adopt is logged with its evidence in `data/divergences.json`,
not silently resolved in code. A reader can open that file and see exactly
which of the 13 defects (D1–D13) were resolved, how, and on what evidence —
including the ones resolved only at sign-family level with named residual
uncertainty (D4), and the ones still open (see `TODO.md` §1 for the plate
work still needed on several of these).

## 1.6 Running one result, and slow stages

To reproduce a single figure rather than the whole pipeline, run the one
script that produces it — every script in `src/` is independently runnable
given its stated inputs already present in `data/`. `docs/METHODOLOGY.md`
lists the exact invocation and expected runtime for every individual result
if you want a single command rather than reasoning from the tables above.

Slow stages (permutation and bootstrap tests: `affix_power.py`,
`grid_null.py`, `smoothing_test.py`, `power.py`) run several thousand
resamples; expect low single-digit minutes each on ordinary hardware, not
seconds. `docs/METHODOLOGY.md` §"Slow stages" gives per-script figures and how
to reproduce one specific condition without rerunning the full sweep.

## 1.7 Static checking, and why it runs before anything else

Every function in `src/` carries an explicit return type annotation — no
function's return type is left for the type checker to guess and silently
fall back to `Any` on. This isn't cosmetic: retrofitting these annotations
during this project's development surfaced three real correctness gaps that
had been invisible until the types were made explicit (an unguarded `None`
case, a missing shape-check on decoded Marshal data, and a sentinel-list
construction pattern that needed an explicit type). The rule going forward:

```bash
pyright   # must report 0 errors before any pipeline stage is run or changed
```

This is checked with `pyrightconfig.json` at the repository root
(`basic` mode, `src/` and `tests/` only). A change to any `.py` file gets
this run before it gets run for real.

## 1.8 Tests

```bash
python3 tests/test_pipeline.py
```

Nineteen tests in three categories: structural invariants that must hold
regardless of which upstream snapshot is in use (schema shape, the D4
correction, licensing hygiene — including a check that no corpus file is
*tracked* by git even if `.gitignore` would otherwise exclude it, since
`.gitignore` doesn't untrack a file already added); reproduction of the
paper's specific published figures, which will fail — informatively, not
silently — if the upstream corpus has changed since this was written; and
SigLA-decoder checks, which skip rather than fail if `sigla_corpus.json`
isn't present.

---

# Part 2 — Reusing this for a different script

## 2.1 The honest framing

This is not a plug-and-play tool. It's a framework with Linear A worked as
the example throughout every stage above. No one should expect a
one-size-fits-all tool for undeciphered scripts — every corpus has different
conventions, different published editions, and different specific questions
worth asking of it. What transfers is the *method*: the adequacy protocol,
the null models, the divergence-register discipline, the power-analysis
technique. What doesn't transfer automatically is anything that has to know
what a Linear A sign, tablet, or edition looks like.

Two goals someone might have in reusing this, and both are legitimate:

- **(i) Reproduce this paper's own claimed numbers**, to check them rather
  than take them on faith. Part 1 above is written for exactly this — nothing
  in it is withheld.
- **(ii) Adapt the method to a different script entirely** (Cypro-Minoan,
  Indus, Proto-Elamite, Rongorongo, or anything else undeciphered with a
  digitized corpus). This section is for that.

## 2.2 What transfers unchanged, and what needs adapting

| component                                                           | transfers as-is?               | why                                                                                                                                                       |
|---------------------------------------------------------------------|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| adequacy protocol (observations-per-cell check)                     | yes                            | pure counting logic, no script-specific assumption                                                                                                        |
| null models (resampling, permutation)                               | yes                            | operates on whatever sign-space you hand it                                                                                                               |
| divergence register schema (`divergences.json`)                     | yes                            | the JSON shape and the adjudication discipline are script-agnostic; only the contents are new                                                             |
| power analysis method (inject known effect, measure detection rate) | yes                            | same technique regardless of what's being tested                                                                                                          |
| entropy / H2 estimators                                             | yes                            | operate on sign sequences, not on what a sign means                                                                                                       |
| **data loader** (`build_corpus.py`, `extract_raw.js`)               | **no**                         | has to read *your* corpus's actual file format                                                                                                            |
| **sign inventory and identifiers**                                  | **no**                         | this project's canonical-id principle (§1.5.1) still applies, but the actual inventory is script-specific                                                 |
| **edition/convention alias tables** (`base_id()`, `canon()`)        | **no**, but the *pattern* does | you will have your own editions with their own naming quirks; the fix is the same kind of canonicalization table, populated with your data                |
| cross-witness sweep logic                                           | mostly                         | the comparison logic transfers; which witnesses exist and what their export format looks like doesn't                                                     |
| Packard-style phonetic replication                                  | only if relevant               | this specific test only makes sense if there's a claimed partial decipherment to test against, the way Linear B readings are tested against Linear A here |

Roughly: the statistical and procedural machinery is reusable near-verbatim;
everything that touches the shape of a specific corpus is not, and has to be
rewritten against your data.

## 2.3 Step by step

**1. Replace the data loader.** `build_corpus.py` (and, if your source is
also raw HTML/JS rather than clean JSON, `extract_raw.js`) is where a
specific upstream format gets turned into this project's working-corpus
shape: one record per document, one token list per record, each token typed
and flagged for damage/completeness. Write the equivalent for your corpus's
actual export format. Keep the output shape (`record_id`, `doc_id`, `tokens`,
each token's `type` and `sign_ids` and damage flags) — everything downstream
depends on that shape, not on Linear A specifically.

**2. Define your sign inventory and edition aliases.** Decide what a
canonical sign identifier looks like for your script (§1.5.1's argument for
why this matters holds regardless of script), and build the alias table that
maps each edition's naming convention onto it — the same role `base_id()`
and `canon()` play here.

**3. Rerun the same pipeline stages.** Once the loader and inventory exist,
the adequacy protocol, null models, divergence register, and power analysis
all run unchanged against your data. Cross-witness sweeps need pointing at
your specific editions instead of Younger/SigLA, which mostly means writing
one parser per witness export format (§1.4, "witness parsing").

The Linear A version in this repository is the fully worked example: every
method is in Part 1 above and in the paper itself; every line of code is in
`src/`. Adapting the framework to another script is a data-engineering task
(new loader, new alias tables), not a re-derivation of the statistics.

## 2.4 Getting help

The methods here are documented in enough depth that a competent programmer
can adapt them without further input. Adapting them *correctly* to a
different script's specific editorial quirks and conventions — which
alternations matter, which comparisons are meaningful, where the adequacy bar
actually sits for a given inventory size — is a different kind of task, and
one this project's author is available to help with or do directly. Contact
details are in the main `README.md`.
