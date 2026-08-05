# Sources

All URLs verified reachable as of 31 July 2026 unless marked otherwise.
Access status noted where it affects reproducibility.

---

## 1. Primary corpus data (used in the pipeline)

**This project's approach: link, do not host; build locally, do not ship.**
No GORILA transcription, Younger commentary text, or GORILA plate image is
committed to this repository or distributed by it in any form. `setup.sh`
clones a public GitHub repository at the user's own instruction and on the
user's own machine — an action GitHub's Terms of Service expressly permit
for any public repository — and the pipeline then builds
`data/corpus_v1.json` locally from that clone. That file is gitignored and
never shipped (`data/README.md`).

| Source                                                                                                                                      | URL                                     | Status                     |
|---------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------|----------------------------|
| **mwenge/lineara.xyz** — `LinearAInscriptions.js` and `commentary/`, sparse-checked-out (non-Windows only; see below). Our ingestion point. | `https://github.com/mwenge/lineara.xyz` | Public, sparse-checked-out |
| mwenge/LinearA — the extraction/processing repo behind the above                                                                            | `https://github.com/mwenge/LinearA`     | Public                     |
| Linear A Explorer (live site)                                                                                                               | `https://lineara.xyz`                   | Public                     |

The corpus derives from GORILA transcriptions plus George Douros's
tabulation. Younger's commentary is vendored inside the repo at
`commentary/` (1736 files, all recovered - `setup.sh` fetches ~20 with
Windows-illegal filenames individually rather than dropping them), which is
what both validation sweeps compare against. **No network access beyond
that one-time clone was required for either sweep.** `setup.sh`
deliberately does not clone the full repository: `images/` (~142 MB of
tablet facsimiles) and `papers/` (~368 MB) are never fetched, since nothing
in this project's code reads them and `images/` in particular is very
likely the same GORILA plate photography under separate copyright
(`data/README.md` item 7).

**Windows is not supported by `setup.sh` for this source.** Some filenames
in this upstream repository use characters (`<`, `>`, `:`, `?`, `"`) illegal
on Windows/NTFS - confirmed directly, `git clone` itself fails on Windows
with `invalid path` errors for these, not merely a checkout-configuration
issue. `setup.sh` detects Windows and refuses to attempt this fetch rather
than fail partway or silently drop data, stating why without pointing
anywhere else.

**Neither GORILA's transcriptions nor Younger's commentary carry an
explicit license from their respective sources.** This project holds no
rights in either and cannot grant permission for their use; it does not
host, redistribute, or circumvent any access restriction on them. Full
account of the reasoning, the residual risk, and what would remove it:
`data/README.md` item 1. This is a factual description of this project's
approach, not legal advice.

## 2. GORILA — Recueil des inscriptions en linéaire A

Godart & Olivier, Études Crétoises XXI, 1–5, Paris 1976–1985. Digitised by the
École française d'Athènes. **Blocks automated access (robots.txt); must be
downloaded manually.**

| Vol | Contents                                       | URL                                                                                                        |
|-----|------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| 1   | Tablets published before 1970                  | `https://cefael.efa.gr/detail.php?site_id=1&actionID=page&serie_id=EtCret&volume_number=21&issue_number=1` |
| 2   | Nodules, sealings, roundels before 1970        | `...&issue_number=2`                                                                                       |
| 3   | Tablets/nodules/roundels published 1975–76     | `...&issue_number=3`                                                                                       |
| 4   | Other documents — **libation corpus, AP Za 2** | `...&issue_number=4`                                                                                       |
| 5   | Addenda, concordances, sign tables, plates     | `...&issue_number=5`                                                                                       |

**Priority documents for adjudication:**
- **AP Za 2** (D11, three editors against GORILA) — Vol. 4
- **D9 word division**: PK Za 8, PR Za 1, KN Zc 6, SY Zb 7 — Vol. 4; HT Zd 157+156 — Vol. 1
- **D4 AB21/AB22**, 14 documents — Vols. 1–3

## 3. Younger — Linear A Texts in Phonetic Transcription

The Kansas server was retired in early 2024; Younger migrated the files to
Academia.edu. Our copy is the version vendored in the mwenge repo.

| Item                        | URL                                                                                            |
|-----------------------------|------------------------------------------------------------------------------------------------|
| Original site (HT texts)    | `https://people.ku.edu/~jyounger/LinearA/HTtexts.html`                                         |
| Original site (other texts) | `http://www.people.ku.edu/~jyounger/LinearA/misctexts.html`                                    |
| AB sign grids               | `http://www.people.ku.edu/~jyounger/LinearA/ABgrids.html`                                      |
| Academia.edu (current)      | `https://www.academia.edu/117949876/Linear_A_Texts_and_Inscriptions_in_phonetic_transcription` |
| Folder introduction         | `https://www.academia.edu/117949722/Younger_JG_Linear_A_folder_introduction`                   |

## 4. Packard 1974 — the replication target

Packard, D. W., *Minoan Linear A*, Berkeley/Los Angeles/London: University of
California Press, 1974. ISBN 0-520-02580-6. UC Press reissue (2023):
`https://doi.org/10.1525/9780520332072`.

**Content consulted:** pp. 56–102 — Chapter 2 (classification, Tables 4–5),
Chapter 3 in full (the phonetic values, Tables 6–16), the alternation
categories and counts, the scoring rule, and the null construction.
**The replication in `docs/PACKARD.md` is complete on this material.**

**Read, but deliberately not used for a cross-check.** Appendix A and D were
both read in full; `docs/PACKARD.md`'s caveat section explains why building
the actual cross-check against them was decided against (`TODO.md`, "Not
doing" — Packard's two appendices):

- pp. 123–138 — Appendix A, the 107 alternation groups themselves. Would allow
  pair-by-pair checking against our 92. Confirmatory only; counts already track.
- pp. 178–192 — Appendix D, the nine value assignments in full. Would let us
  check whether our rotation reconstruction matches his mechanically.

Related Packard items not yet obtained:
- Packard 1967, "A Study of the Minoan Linear A Tablets", unpub. diss., Harvard.
- Packard 1968, *Atti … Micenologia* I, 389–394.
- Packard 1971, "Computer Techniques in the Study of the Minoan Linear Script A", *Kadmos* 10:52–59.
- **Pope & Raison 1978**, "Linear A: Changing Perspectives", in *Études minoennes I* (BCILL 14), ed. Duhoux, 24–25 — source of the 3:1 figure.

## 4b. Linear B lexicon (used for the name-parallel test)

Luo, J., Cao, Y. & Barzilay, R. (2019), "Neural Decipherment via Minimum-Cost
Flow: From Ugaritic to Linear B", *ACL 2019*, 3146–3155.

| Item                         | URL                                        |
|------------------------------|--------------------------------------------|
| **Code and data repository** | `https://github.com/j-luo93/NeuroDecipher` |
| Paper (ACL Anthology)        | `https://aclanthology.org/P19-1303/`       |
| Paper (arXiv)                | `https://arxiv.org/pdf/1906.06718`         |

Files used: `data/linear_b-greek.cog` (919 Linear B/Greek pairs) and
`data/linear_b-greek.names.cog` (proper nouns flagged). The authors note their
set is a modification of Tselentis (2011).

**Why it works as a concordance.** Linear B words are stored as Unicode
syllabograms whose character names carry both the sign number and the value
(`LINEAR B SYLLABLE B008 A`). Homomorphic signs share the AB number with Linear
A, so B008 maps directly to our AB008 with no manual table.

**Knossos restriction: resolved.** Packard's criterion required the Linear B
sign-group to be attested at Knossos specifically, not just present anywhere
in the lexicon. `src/packard_names.py.load_linear_b_knossos_names` now
intersects the 429 names of three-plus signs against a DĀMOS Knossos
find-site word export by exact transliteration match: 154 survive. This is
now the headline criterion in `docs/PACKARD.md`; the unrestricted 429 is kept
alongside only for comparison with earlier drafts.

Related, not yet obtained: Tselentis, C. (2011), *Linear B Lexicon*.

**DĀMOS (Database of Mycenaean at Oslo).** `https://damos.hf.uio.no/` — a
free, public, searchable, annotated corpus of all published Mycenaean Linear
B texts, covering Knossos among other sites. License: **CC BY-NC-SA 4.0** on
the content, GPL-3.0 on the site's own software (not relevant to reusing the
text data). Required citation, from the site's own `/howto` page:

> Aurora, Federico. 2015. DAMOS (Database of Mycenaean at Oslo). Annotating
> a fragmentarily attested language. In: Pedro A. Fuertes-Olivera et al.
> (eds.), *Current Work in Corpus Linguistics: Working with
> Traditionally-conceived Corpora and Beyond. Selected Papers from the 7th
> International Conference on Corpus Linguistics (CILC2015)* (Procedia -
> Social and Behavioral Sciences, 198), 21-31,
> doi: 10.1016/j.sbspro.2015.07.415

**Knossos word export: obtained and in use.** A Knossos-site-restricted
search run directly on `https://damos.hf.uio.no/` (full word-level export,
19,559 rows; 2,880 distinct lexical items after deduplication) is the source
for the restriction above. Not redistributed — see `data/README.md` item 5b
for the license terms and how to reproduce the export yourself. That export's
own `wordtype` field does not
distinguish personal names from any other word — every actual word is
tagged simply `"common word"` — so a further step is needed to isolate names
specifically, and no source for that step has been obtained in a form this
distinguish personal names from any other word — every actual word is tagged
simply "common word" — so the intersection above is deliberately built the
other way round: it takes personal/place names from the NeuroDecipher lexicon
(§4b above) and restricts those by Knossos attestation from DĀMOS, rather than
trying to classify DĀMOS's words by type directly.

## 4c. Fraction values — OBTAINED and adopted

Corazza, M., Ferrara, S., Montecchi, B., Tamburini, F. & Valério, M. (2021),
"The mathematical values of fraction signs in the Linear A script: A
computational, statistical and typological approach", *JAS* 125: 105214.
**Open access, CC BY-NC-ND.**

| Item                            | URL                                                                                                               |
|---------------------------------|-------------------------------------------------------------------------------------------------------------------|
| **Full text PDF (open access)** | `https://flore.unifi.it/retrieve/e398c382-1e6d-179a-e053-3705fe0a4cff/Ferrara-Montecchi-Valério_JAS_125_2021.pdf` |
| DOI                             | `https://doi.org/10.1016/j.jas.2020.105214`                                                                       |
| ScienceDirect                   | `https://www.sciencedirect.com/science/article/pii/S0305440320301357`                                             |

Their optimal system is now adopted in `build_corpus.py`, superseding the
conjectural grades taken from Younger (defect D2). Two consequences logged:
**D12** (doubtful-reading marks absent from our corpus, detected via their sign
counts) and **D13** (K = 1/10 against the 1/16 we had graded "secure").

## 5. Third-witness transliteration

van Soesbergen, P. G., *The Decipherment of Minoan Linear A*, Vol. II: *Corpus of
Transliterated Linear A Texts*, 2nd rev. ed., IngramSpark 2022.
ISBN 9789083275468 (1st ed. 2016, ISBN 9789402158045).

Supplied as PDF. **Caution:** interleaves Hurrian-hypothesis glosses with the
transliteration (`qa[ = ḫa[`); these must be stripped like `translatedWords`.
Uses Raison-Pope numeration and different site codes (AK for Arkhanes, GR for
Khania).

## 6. Reference and background

| Item                                                                                   | URL                                                                                    |
|----------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| Salgarella, "Linear A", *Oxford Classical Dictionary* (2022)                           | `https://doi.org/10.1093/acrefore/9780199381135.013.8927`                              |
| **SigLA — The Signs of Linear A** (Salgarella & Castellan)                             | `https://sigla.phis.me/`                                                               |
| — SigLA paper                                                                          | `https://www.fluxus-editions.fr/gla5-salg.pdf`                                         |
| — SigLA at INSCRIBE                                                                    | `https://site.unibo.it/inscribe/en/linear-a-sigla`                                     |
| Lazaridis et al., "Genetic origins of the Minoans and Mycenaeans", *Nature* 548 (2017) | `https://www.nature.com/articles/nature23310`                                          |
| Corpus of Minoan and Mycenaean Seals (CMS)                                             | `https://arachne.dainst.org/search?fq=facet_kategorie:%22Einzelobjekte%22&fl=20&q=cms` |

### SigLA — obtained, decoded, and in use

| Item                              | URL                                            | Access                          |
|-----------------------------------|------------------------------------------------|---------------------------------|
| Database interface                | `https://sigla.phis.me/`                       | Public; blocks automated access |
| **Source code / import pipeline** | `https://gitlab.inria.fr/sicastel/sigil`       | Public; behind Anubis anti-bot  |
| Paper (open access)               | `https://www.fluxus-editions.fr/gla5-salg.pdf` | Fetched, read                   |
| Licence                           | CC BY-NC-SA 4.0 (dataset and drawings)         |                                 |

**Why this mattered.** The paper states: *"In SigLA we use the
question-mark for signs of doubtful reading or unreadable."* SigLA therefore
carries the certainty marking that **D12** shows is absent from every layer of
our current source. It also carries erasures and a per-sign function
classification (syllabogram / logogram / transaction-sign / fraction), and the
architecture is deliberately open: *"the database is easily accessible and usable
by other people outside the interface... JSON is one of the best supported data
description languages. Moreover, the website can be downloaded and run locally."*

**How it was obtained.** Not by request — decoded directly. SigLA licenses its
dataset CC BY-NC-SA 4.0, and its own paper states the intent that the database
be usable outside the interface, but the data is served as two OCaml `Marshal`
blobs escaped inside the web app's JavaScript, not as a documented export. A
purpose-built parser (`src/ocaml_marshal.py`, `src/extract_sigla.py`) implements
the `Marshal` binary format and recovers documents and attestations directly
from that serialized state. Retrospective permission for this use has been
sought directly from Salgarella and Castellan; a reply, if it changes
anything, would be reflected here and in `data/README.md`. See
`data/README.md` item 3 for how to reproduce the decoded content yourself.

**What it fixed:** D12 directly (certainty marking), and gave an independent
third witness on D4 (AB21/AB22), D9 (word division) and D11 (AP Za 2) — sweep 3
(§4.5 of the paper) is built on it.

**Caveat from the paper (2021), now resolved:** *"At present the database only
contains administrative documents, more precisely the Linear A tablets found at
the most prominent sites on Crete."* Coverage has since grown: the decoded
802-record corpus includes 29–30 documents of Z-series (religious/votive)
designation, well beyond that administrative-only scope. This is now
cross-checked against an independent citation — Lamonica, ch. 5 in Salgarella &
Petrakis (eds.) 2026, stating SigLA holds "over 770 documents" — see
`src/sigla_coverage.py` and `data/sigla_coverage.json`. D9 and D11 are covered.
corpus, so D9 and D11 would remain open. Coverage may have grown since.

## 7. Literature cited but not yet obtained

- **Steele, P. M. & Meißner, T. (2017)**, "From Linear B to Linear A: The Problem
  of the Backward Projection of Sound Values", in *Understanding Relations
  Between Scripts*, ed. Steele, Oxbow, 93–110. *Directly frames our phonology
  section; should replace our own reasoning as the theoretical anchor.*
- **Davis, B. (2013)**, "Syntax in Linear A: The Word-Order of the 'Libation
  Formula'", *Kadmos* 52.1: 35–52. *The word-order result we independently
  recovered.*
- **Davis, B. (2014)**, *Minoan Stone Vessels with Linear A Inscriptions*,
  Aegaeum 36, Leuven.
- **Duhoux, Y. (1978)**, "Une analyse linguistique du linéaire A", BCILL 14.1:
  65–129. *Source of the 59%-prefix figure our null model could not reproduce.*
- **Palaima, T. & Sikkenga, E. (1999)**, "Linear A > Linear B", in *Meletemata*,
  Aegaeum 20, 599–608. *Source of the three-vowel hypothesis.*
- **Schoep, I. (2002)**, *The Administration of Neopalatial Crete*, Salamanca.
- **Raison, J. & Pope, M.**, *Corpus transnuméré du linéaire A*, BCILL 74, 2nd ed. 1994.

## 8. Software and libraries

Python 3, `scipy` 1.17.1, `beautifulsoup4` 4.14.3, Node.js 22 (to evaluate the
source `Map`). All random procedures seeded `20260731`. See `run_all.sh`.

---

## Note on the corpus license

The SigLA dataset and drawings are CC BY-NC-SA 4.0. GORILA images are © École
Française d'Athènes; the mwenge repo carries `imageRights` and
`imageRightsURL` per record and our `corpus_v1.json` preserves both in the
`gorila_ref` field. Any publication or repo release must honor these.
