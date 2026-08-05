# Data directory

The repository ships **no corpus data**. This file states, for every file that
belongs here, where it comes from, what license governs it, and the exact
command that produces it — so a build can be verified against the paper
without redistributing anything this project doesn't hold rights in.

## What is here

| file                             | provenance                                              | license                                             |
|----------------------------------|---------------------------------------------------------|-----------------------------------------------------|
| `divergences.json`               | original work: the divergence register                  | Shield 1.0.0 + academic carve-out                   |
| `power_analysis.json`            | original work: synthetic power analysis (paper §5.5)    | Shield 1.0.0 + academic carve-out                   |
| `corpus_v1.json`                 | derivative of GORILA / Douros / Younger / `lineara.xyz` | not redistributed — generate locally, item 1        |
| `database.js`                    | SigLA source                                            | CC BY-NC-SA 4.0 — not redistributed, item 3         |
| `sigla_corpus.json`              | derivative of SigLA                                     | CC BY-NC-SA 4.0 — not redistributed, item 4         |
| `damos_knossos_deduplicated.csv` | DĀMOS Knossos word export                               | CC BY-NC-SA 4.0 — not redistributed, item 5b        |
| everything else in `data/`       | intermediate pipeline output                            | regenerated on every run, not individually licensed |

`divergences.json` and `power_analysis.json` are the only two files here that
are committed. Neither contains third-party corpus material:
`power_analysis.json` reports statistics computed on **synthetic** corpora, and
`divergences.json` records sign identifiers with attribution as ordinary
scholarly citation. Everything else is generated on your machine from its
original source and gitignored — see `.gitignore`'s `data/*.json` /
`data/database.js` rules.

This is a deliberate choice, not an oversight. Shipping convenient copies would
require this project to assert redistribution rights over other people's
scholarship that it does not clearly hold.

---

> **A trap worth knowing.** `.gitignore` prevents files being *added*; it does
> not untrack files already added. If you ran `git add -A` before the ignore
> rules existed, the corpora are tracked and will be published. Check with
> `git ls-files data/`, and untrack with `git rm --cached <file>`. The test
> suite catches this (`test_corpus_not_committed`, `test_sigla_not_committed`).

---

## 1. `raw_repo/` — the upstream Linear A corpus

Cloned into the **repository root**, not into this directory.

```bash
git clone --depth 1 https://github.com/mwenge/lineara.xyz.git raw_repo
```

or run `./setup.sh`, which does this and item 5.

**Provenance.** Sign transcriptions from GORILA (Godart & Olivier 1976–1985,
Études Crétoises XXI) — a published scholarly edition, not open access, and the
transcriptions themselves (not only the plate images) may be subject to
copyright. Word division and tabulation by George Douros, an independent
compilation with no explicit open license. Commentary by John G. Younger,
publicly available but carrying no explicit license. `mwenge/lineara.xyz` is
the digital extraction this project ingests.

**The upstream repository carries no LICENSE file**, which under default
copyright is all rights reserved. This is why nothing derived from it is
redistributed here — the corpus is built locally from the upstream source,
which every user is free to clone directly. Check whether a license has since
been added.

> **GORILA data specifically.** This project holds no rights in the underlying
> GORILA sign transcriptions and cannot grant permission for their use. Users
> must satisfy themselves that their own use of GORILA-derived material is
> permitted under applicable law in their jurisdiction and for their purpose.

Three things reduce the exposure of building on that upstream repository,
worth stating plainly rather than assumed:

- **transcriptions are closer to data than to expression.** A sign-by-sign
  transcription of a Bronze Age tablet is a record of what is on the object.
  Jurisdictions differ on how much originality such a record attracts, and the
  EU *sui generis* database right that may apply carries a research exception
  for non-commercial scientific use with attribution — which is this use.
- **nothing is redistributed.** No GORILA image, no GORILA text, no derived
  corpus. `corpus_v1.json` is built on the user's machine and gitignored.
- **attribution is complete.** Every generated record retains a `gorila_ref`
  field pointing at the source plate, so the edition is cited rather than
  displaced.
- **cloning the public repository itself is unambiguous.** GitHub's Terms of
  Service expressly permit cloning any public repository; that action is not
  in question here, and is distinct from the licensing status of the content
  inside it, which is what the rest of this section addresses.

Link, do not host; build locally, do not ship.

**Verify:** `raw_repo/LinearAInscriptions.js` exists, roughly 4.5 MB.

---

## 2. `corpus_v1.json` — the working Linear A corpus

**Not redistributed.** Requires item 1. Generate it with:

```bash
node src/extract_raw.js       # raw_repo/LinearAInscriptions.js -> data/inscriptions_clean.json
python3 src/build_corpus.py   # -> data/corpus_v1.json
```

or `./src/run_all.sh`, stages S0 and S1.

**What the two steps do.** `extract_raw.js` evaluates the upstream JavaScript
`Map` — it is not JSON — and drops the `translatedWords` field, which carries
Linear B-derived semantic glosses and is interpretation rather than data.
`build_corpus.py` resolves every character to its GORILA sign identifier,
parses damage markers into structured flags, annotates measures with
confidence grades, and applies the D4 correction.

**Expected result** (as of the 2026-07-31 snapshot the paper was written
against — a different value means the upstream corpus has changed since, which
is expected over time and not an error, but the paper's figures may no longer
describe it; `tests/test_pipeline.py` detects this and skips the dependent
assertions with an explanation rather than failing opaquely):

| property                   | value                                                              |
|----------------------------|--------------------------------------------------------------------|
| size                       | ~2.37 MB                                                           |
| md5                        | `2f5c936f0848fcbcb4ef35669eccca99`                                 |
| sha256                     | `a642976320aaaa52f67f3fc29539a3ee88ea683e25bc2d6d8969e6d6114a93a1` |
| records                    | 1721                                                               |
| distinct documents         | 1621                                                               |
| complete sign-groups       | 2659                                                               |
| damaged sign-groups        | 953                                                                |
| complete multi-sign groups | 927                                                                |

**License of the result.** A derivative of the sources in item 1. This project
does not hold copyright in the underlying transcriptions and cannot license
them. Users must comply with the terms of the original sources and are
responsible for satisfying themselves that their own use is appropriate.

---

## 3. `database.js` — the SigLA raw source

SigLA's corpus is served as a publicly accessible JavaScript file, licensed
**CC BY-NC-SA 4.0** ([full terms](https://creativecommons.org/licenses/by-nc-sa/4.0/)),
which permits copying and adaptation for non-commercial use with attribution —
exactly the use made here.

**Automatic (recommended):**

```bash
python3 src/extract_sigla.py --fetch
```

Downloads `database.js` to `data/database.js`, caches it so repeated runs
don't hit an academic project's server again, prints the license notice, and
decodes it in one step. `--fetch` is opt-in rather than the default:
retrieving another project's data should be a deliberate act, and the license
obligations should be read before they're taken on, not after.

**Manual:** place your own copy at `data/database.js` and skip to item 4.

**Your obligations**, which the `--fetch` notice restates: **attribute**
Salgarella and Castellan; **non-commercial** use only; **share alike** — any
derivative you distribute carries CC BY-NC-SA 4.0. Full text:
https://creativecommons.org/licenses/by-nc-sa/4.0/. Cite: Salgarella, E. &
Castellan, S. (2021), "SigLA: The Signs of Linear A. A Paleographical
Database".

**Verify:** roughly 2.5 MB, beginning `\132\149\166\190` — the OCaml `Marshal`
magic number `0x8495A6BE` as decimal escapes.

---

## 4. `sigla_corpus.json` — the SigLA comparison corpus

**Not redistributed.** Requires item 3. Generate it with:

```bash
python3 src/extract_sigla.py --input data/database.js \
                             --output data/sigla_corpus.json
```

**What this does.** SigLA ships its corpus as two OCaml `Marshal` blobs escaped
as decimal octets inside JavaScript string literals. `Marshal` stores records
positionally, so field names are absent and the data cannot be located by text
search. `src/ocaml_marshal.py` implements the format — header, prefix
encodings, sharing table for back-references — and `extract_sigla.py` maps the
recovered structure onto documents and attestations. Paper Appendix D
describes this in full.

**Expected result:**

| property                          | value                                                              |
|-----------------------------------|--------------------------------------------------------------------|
| size                              | ~848 KB                                                            |
| md5                               | `f3cb6d5805bd5376eef7099705d3d2ef`                                 |
| sha256                            | `7e2157090b847a1bafccd2a7465babd8a9c9b4f7de5b28ce22ecf9ce3f5106b8` |
| documents                         | 802                                                                |
| attestations                      | 5144                                                               |
| confident / doubtful / unreadable | 4712 / 44 / 388                                                    |
| erasures / ghosts                 | 104 / 7                                                            |

A different result means SigLA has been updated since. Expected over time; the
test suite will say so.

**License of the result — this one binds.** © 2020– Ester Salgarella and Simon
Castellan, **CC BY-NC-SA 4.0**. This license attaches to the data, not to the
code that processes it: `src/ocaml_marshal.py` and `src/extract_sigla.py` are
original work licensed under PolyForm Shield 1.0.0 (see `LICENSE.md`), but any
output they produce from SigLA input is a derivative of SigLA and remains CC
BY-NC-SA 4.0. Re-encoding a format does not create a new copyright in the
underlying material.

If you distribute `sigla_corpus.json` or anything derived from it, you must:

- **attribute** Salgarella and Castellan, citing: Salgarella, E. & Castellan,
  S. (2021), "SigLA: The Signs of Linear A. A Paleographical Database",
  *Proceedings of the 5th International Conference on Digital Access to
  Textual Cultural Heritage*;
- use it **non-commercially**;
- **share alike**, under the same CC BY-NC-SA 4.0 terms.

The extractor deliberately takes only sign identifiers, document metadata and
the certainty and boundary fields. It does not touch the drawings, which are
the substantial creative content of SigLA and should be consulted on their
site.

---

## 5. `nd/` — the Linear B lexicon

Cloned into the **repository root**.

```bash
git clone --depth 1 https://github.com/j-luo93/NeuroDecipher.git nd
```

**Provenance.** Luo, Cao & Barzilay (2019), ACL. Used only by
`src/packard_names.py` for the name-parallel replication (paper §8.4). The
authors note their set is a modification of Tselentis (2011).

**Check that repository's own license before reusing its data**, and check
whether it has changed since this was written. This project neither
redistributes it nor asserts anything about its terms.

**Verify:** `nd/data/linear_b-greek.names.cog` exists, 920 lines.

---

## 5b. DĀMOS — Knossos-restricted Linear B names (in use)

**Not redistributed.** `data/damos_knossos_deduplicated.csv` is gitignored;
generate your own copy by repeating the search below. Used by
`src/packard_names.py.load_linear_b_knossos_names` to restrict the
name-parallel replication (`docs/PACKARD.md` §"name-parallel test") to
Knossos-attested names, closing `TODO.md` §2.2.

**Source:** `https://damos.hf.uio.no/` — Database of Mycenaean at Oslo, a
free, public, searchable, annotated corpus of all published Mycenaean Linear
B texts, covering Knossos among other sites.

**License:** **CC BY-NC-SA 4.0** on the content (same family of terms as
SigLA — attribution, non-commercial, share-alike); GPL-3.0 on the site's own
software, which is not relevant to reusing the text data.

**Required citation**, per the site's own `/howto` page:

> Aurora, Federico. 2015. DAMOS (Database of Mycenaean at Oslo). Annotating
> a fragmentarily attested language. In: Pedro A. Fuertes-Olivera et al.
> (eds.), *Current Work in Corpus Linguistics: Working with
> Traditionally-conceived Corpora and Beyond. Selected Papers from the 7th
> International Conference on Corpus Linguistics (CILC2015)* (Procedia -
> Social and Behavioral Sciences, 198), 21-31,
> doi: 10.1016/j.sbspro.2015.07.415

**How to reproduce the export:** not automated, and not expected to be —
DĀMOS's search is an interactive, JavaScript-driven application, not a
static export or documented API, so there is no `src/*.py` script for this
the way there is for every other source in this document. Filter by find-place
= Knossos, run a Word Search with the pattern left open (searching for the
site code "KN" literally returns nothing — it's an archive label, not a word
any scribe wrote), and export. Expected result: 19,559 word-token rows,
2,880 distinct lexical items after deduplication (column `wordsortcontent`).
Full methodology and AI-disclosure: `docs/DAMOS.md`.

**Classifying which entries are personal names.** DĀMOS's own `wordtype`
field doesn't distinguish names from common words — every real word is
tagged `"common word"` regardless of grammatical category (`docs/DAMOS.md`).
Rather than needing a separate onomasticon, the classification runs the other
way: intersect this Knossos word list against the *already-classified* names
in item 5's NeuroDecipher lexicon (`nd/data/linear_b-greek.names.cog`, 429
names of three-plus signs) by exact transliteration match. Result: **154**
words that are both classified as names and Knossos-attested.

**License of the result.** A derivative of both DĀMOS and NeuroDecipher.
Carries the citation above and complies with CC BY-NC-SA 4.0 — the same
non-commercial, share-alike, attribution terms already documented for SigLA
in item 4, not redistributed beyond what that license permits.

---

## 6. Fraction values

The fraction system of Corazza et al. (2021, *JAS* 125: 105214, open access,
**CC BY-NC-ND**) is **used** — the numeric values appear in
`src/build_corpus.py` with citations — but their paper is not redistributed.
Using published values with attribution is ordinary scholarly citation.

---

## 7. GORILA plate images

Not redistributed, and not fetched by `setup.sh` either (`docs/SOURCES.md`
§1 has the full account of what `setup.sh` does and does not clone, and the
disclaimer covering GORILA- and Younger-derived material generally). Plate
images are © École française d'Athènes. Each record in the generated
`corpus_v1.json` retains a `gorila_ref` field linking to the source plate on
the publisher's site.

---

## Intermediate outputs

`inscriptions_clean.json`, `signgroups_by_genre.json`, `younger_tokens.json`,
`younger_freetext.json`, `sweep1_findings.json`, `sweep2_findings.json`,
`sweep3_findings.json`, `formula_dual.json`, `sigla_coverage.json` — all
gitignored, all regenerated by the relevant pipeline stage, nothing lost if you
delete them. `./src/run_all.sh` recreates them. None carries a license beyond
what its inputs above already state.

---

## Verify everything at once

```bash
./data/verify.sh
```

Reports each file's presence, size and checksum; names the command that
produces anything missing; warns where a checksum differs from the published
one.

## Which results need which file

| file                             | needed for                                                        |
|----------------------------------|-------------------------------------------------------------------|
| `corpus_v1.json`                 | everything                                                        |
| `sigla_corpus.json`              | sweep 3, the D4 correction, the D12 resolution, the D8/D10 triage |
| `nd/`                            | the Packard name-parallel replication (both rows)                 |
| `damos_knossos_deduplicated.csv` | the Knossos-restricted name-parallel row specifically             |

Without `sigla_corpus.json` the pipeline runs and every other result
reproduces; the SigLA-dependent stages report the file is absent and skip, as
do five of the fifty tests (`tests/README.md` has the full breakdown by file).

---

## Disclaimer

This repository distributes original code and analysis, and generates
third-party data locally rather than redistributing it. Every effort has been
made to respect the terms of the underlying scholarship, some of which has
complex or unstated copyright status. Users are responsible for ensuring their
own use complies with all applicable terms.

If you hold rights in any material referenced here and believe it is handled
incorrectly, please contact the author for correction or removal.
