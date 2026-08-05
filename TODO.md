# TODO

Outstanding work. Split into what is genuinely this project's own work to do,
and what depends on someone else entirely.

---

## 1. Outside this project's reach — GORILA plate collation

**This is not this project's TODO in any actionable sense. It is a list of
what a trained epigrapher, with physical or high-resolution access to the
plates, would need to check.** Twenty items, none resolved. Full procedure
and per-item reasoning for the AI-assisted attempt already made:
`docs/PLATE_COLLATION.md` — result was 0 of 20, an honest adequacy finding,
not a gap this project failed to close. Only one item (`AP Za 2`) has a
documented multi-scholar disagreement; the other 19 are disagreements between
digital editions. All plates: Godart & Olivier 1976–1985, *Études Crétoises
XXI*, at `https://cefael.efa.gr` (volume URLs in `docs/SOURCES.md` §2).

- **D9 — word division, 4 sites** (`PK Za 8`, `PR Za 1`, `SY Zb 7`,
  `HT Zd 157+156`; `KN Zc 6` already explained via SigLA, needs no plate).
  What to check: presence or absence of a word-divider dot at the contested
  ridge. Gates libation-formula segmentation, the highest-value genre for
  grammatical analysis.
- **D11 — `AP Za 2`, 1 site.** Three editors (van Soesbergen, Brice,
  Raison-Pope) read `i-na-ja-re-nu` against GORILA's `-ta`, in the libation
  formula's final slot. GORILA vol. 4, HM 2479+2480.
- **D7 — numeral conflicts, 4 sites** (`HT 10a`: 14 vs. **104**; `HT 113`: 30
  vs. 2; `HT 17`: 37 vs. 38; `HT 4`: 1 vs. 2). `HT 10a`'s order-of-magnitude
  gap is the one worth checking first if only one is ever checked.
- **D8/D10 — nine sign-conflict positions, 8 tablets** (`ARKH 1b`, `HT 15`,
  `HT 17`, `HT 34` ×2 positions, `HT 49a`, `KH 74`, `KH 8`, `MA 10b`) —
  survivors of a 137→9 triage (`data/divergences.json`,
  `triage.genuine_conflicts`) that already filtered out everything explainable
  by naming convention alone.
- **D4 — two unadjudicated documents, plus an unconfirmed gender variant
  across the fourteen already corrected.** Two distinct gaps, both needing
  plate access, both filed under D4:
  - The fifteen-site AB21/AB22 correction (`src/build_corpus.py`) fixes
    *sign identity* only — SigLA confirms the source swapped AB21↔AB22, but
    SigLA does not record the M/F gender diacritic. Concretely: the corpus
    now reads `AB022F` where it previously read `AB021F`; the `AB022` is
    confirmed by SigLA, the `F` is confirmed by nothing. If the source's
    gender variants were also mis-assigned, family-level agreement with
    SigLA would hide it completely — nothing in this project tests that.
    Until checked, any analysis distinguishing male from female livestock
    should treat the gender variant as unverified.
  - Two further documents (`PH(?) 31a`, `PH(?) 31b`) are absent from SigLA
    entirely and outside the fifteen-site adjudication altogether. Whether
    the same inversion pattern extends to them is currently an assumption,
    not a finding.
  - What to check: the gender diacritic on the fourteen corrected documents,
    plus sign identity on the two unadjudicated ones. `docs/PLATE_COLLATION.md`
    flags the two-document pair as the best candidate if higher-resolution
    access ever becomes available, since that check is more mechanical than
    the other four defects.

---

## 2. This project's own remaining work

### 2.1 KU-RO: resolved, and the residue is now mostly explained

Per-commodity sectioning was implemented and **made no difference** to the match
rate. The result was instead settled by a proper null model: sections sum to
their own stated total rather than another tablet's at z = +13.4.

The 50% mismatch rate is not a uniform residue. Every numeral in the corpus
already carries a damage/completeness flag (`src/kuro_test.py.is_damaged`,
`mismatch_damage_breakdown`), so the three candidate explanations named
against it were checked, not just listed:

- **Damaged/incomplete numerals: 9 of 13 mismatches (69%)** involve one, in
  the summed section or the stated total. Directly evidenced, not a guess.
- **D7 numeral conflicts: don't apply.** None of the four open D7 sites
  (`HT10a`, `HT113`, `HT17`, `HT4`) are among these 26 testable tablets.
  Adjudicating D7 would not touch a single one of these mismatches.
- **Sectioning this study cannot resolve:** still a live, untested candidate
  for the 4 remaining cases specifically (below) — nothing here rules it in
  or out.

**4 genuinely unexplained mismatches remain**, no damage flag on any numeral
involved: `HT25b` (+16), `HT100` (−4), `HT118` (+20), `HT123+124b` (+8.68).

**Resolution:** for these four specifically — not the other 9, and not by way
of D7 — either a sectioning rule this study hasn't tried, or plate collation
to check whether the digitized reading itself is faithful to the tablet.

### 2.2 Duhoux 1978 has not been consulted in the original

Not available digitally (Peeters, 1978). Given that this project's
reconstruction of Packard's method was wrong three times before the primary
source corrected it, no weight is placed on our reading of Duhoux's method.

**Resolution:** library or interlibrary request.

---

## 3. Computational work

### 3.1 Resolved

- **SigLA coverage re-check.** Their 2021 paper says administrative documents
  only; the decoded database contains 29-30 Z-type religious documents
  (`src/sigla_coverage.py`, `data/sigla_coverage.json`). Cross-checked against
  an independent citation - Lamonica, ch. 5 in Salgarella & Petrakis (eds.)
  2026, "over 770 documents" - which lands within 1-2 documents of both
  partitions here (771 administrative-support, 772 non-Z-designation), against
  our 802 total. Coverage grew by almost exactly the Z-type set sometime
  between the 2021 paper and the 2026 volume; see paper.md §4.4.

### Other scripts — apply the framework

- **Cypro-Minoan.** Run the adequacy protocol before anyone attempts to settle
  the "one script or several" dispute, which is precisely a distributional
  question. If the corpus cannot support the distinction, the debate is moot
  until more data appears.
- **Indus script.** ~4000 inscriptions, ~400 signs, undeciphered, numerous
  competing claims, multiple digital editions with *different sign inventories*
  — which is exactly the multi-witness comparison problem. Fold conventions, log
  disagreements, then test whether conditional entropy or minimal pairs are
  supported.
- **Proto-Elamite.** ~1600 tablets, ~1000 signs, mostly numerical, clay
  administrative records. Audit the digital corpus against the printed edition;
  determine whether the numerical system is decipherable from extant data.
- **Rongorongo.** ~25 wooden objects, ~800 glyphs. The smallest and most
  contested corpus, so structured preservation of uncertainty matters most.
  Adequacy testing will likely close most routes, which is worth demonstrating.
- **Linear B — the validation case.** The framework works on *deciphered*
  scripts. Running it on Linear B would reveal what editorial decisions are
  embedded in a corpus whose language is known, and what uncertainties have been
  flattened. This is the only way to validate the framework against ground
  truth, and it should arguably be done before trusting it on anything else.
- **Per-commodity sectioning** for KU-RO (§2.3 above).

---

## Not doing

### Packard's two appendices — reconciling our reconstruction against his literal tables

Both appendices (Appendix A, "Alternations within Linear A"; Appendix D,
"Random Decipherments of Linear A") have been read. Building the actual
cross-check — an L-number-to-AB concordance, his 107 pairs checked against
our 92, his nine value-assignment tables checked against our 4000 generated
rotations — has not been done, and isn't going to be.

**Why not, despite having the material.** Two separate reasons, not one:

- **Value is confirmatory only, not a new finding either way.** The
  replication already stands on his documented *rule* (pp. 72–101), applied
  faithfully to this project's own corpus, with the scoring logic
  independently hand-verified and a real bug already found and fixed in the
  null generator. The aggregate results already track his closely (92 vs 107
  alternation groups; name-parallel ratios in the same 4-5:1 range as his; his
  own absolute count of 15 against a comparable 10 once the Knossos
  restriction was added). A pair-by-pair reconciliation could only confirm
  that or surface a handful of borderline classification disagreements — it
  cannot overturn a result already significant at z > 4.
- **Doing it properly means transcribing his compiled tables, not just his
  method.** Building the concordance means typing his literal 107 pairs and
  nine full value-assignment tables into project files — reproducing his
  compiled *expression*, not his described *method*, which is a meaningfully
  different act from everything else this project does with copyrighted
  sources (cites Packard's stated rules and figures, same as it cites GORILA,
  SigLA, or DAMOS's documentation, without transcribing their underlying
  compiled material wholesale). Low confirmatory value against that is not a
  good trade.

### Tselentis (2011), *Linear B Lexicon* — checking it as a second Knossos name source

Named, at the time the Knossos-restriction gap was first identified, as the
other candidate cross-reference alongside DĀMOS for restricting the Packard
name-parallel test to Knossos-attested names (`docs/DAMOS.md`). Not obtained,
not checked for availability, and not going to be pursued now: the DĀMOS +
NeuroDecipher intersection already closed the gap (154 Knossos-attested
names, `docs/PACKARD.md` §8.4). A second independent source could in
principle cross-check that 154 against an alternative name list, but nothing
currently suggests the DĀMOS-derived figure is wrong, so this stays a named,
not-obtained, not-currently-warranted item rather than active work. Full
citation: `docs/SOURCES.md` §4b, "Related, not yet obtained."

---

## Completed

- ~~D4 identified, adjudicated at family level from the plates, corrected at
  build time (`src/build_corpus.py`)~~
- ~~D12 resolved: SigLA decoded, certainty field recovered
  (`src/ocaml_marshal.py`, `src/extract_sigla.py`)~~
- ~~D8/D10 triaged: 137 candidate sites → 9 genuine conflicts, 32 explained by
  naming-convention differences alone~~
- ~~D2 resolved: Corazza et al. (2021) fraction system adopted with citation~~
- ~~Packard replication: alternation criterion, name-parallel test, phonology
  test, sparse-data check — all four corrected and re-run~~
- ~~Three independent-witness sweeps: 92.0% (Younger tabular), 94.7% (Younger
  free-text), 95.9% (SigLA)~~
- ~~Adequacy protocol: sign-inventory grid, conditional entropy, vowel
  phonotactics~~
- ~~Sparse-data methods (smoothing, minimal-pairs bootstrap) tested and shown
  not to circumvent the H2 result~~
- ~~Affix-direction power analysis (25 replications × 8 conditions, bundled at
  `data/power_analysis.json`)~~
- ~~Test suite (19 tests), methodology documentation~~
- ~~Licensing: no third-party corpus data redistributed; every generated file
  is gitignored and regenerated locally, checked by `data/verify.sh`~~
- ~~SigLA data use: CC BY-NC-SA 4.0 permits copying and adaptation for
  non-commercial use with attribution; the paper and READMEs state the
  license basis directly (not legal advice)~~
- ~~Reproducibility: `src/extract_sigla.py --fetch` retrieves and caches
  `database.js` from source at runtime; needs network access, not permission
  or correspondence, and redistributes nothing~~
- ~~SigLA coverage re-check (TODO 3.1): 802-record decode cross-checked
  against an independent citation, corroborating that coverage grew beyond
  the 2021 paper's administrative-only scope
  (`src/sigla_coverage.py`, `data/sigla_coverage.json`)~~
- ~~Packard name-parallel scoring logic (`src/packard_names.py.matches`)
  independently hand-traced: one real positive case (AB001-AB073-AB055
  vs Linear B da-mi-ni-jo) derived from the stated rule before checking the
  code, plus two constructed negative cases isolating the third-consonant
  and first-two-signs conditions separately. All three now permanent unit
  tests (`TestPackardNames`, test suite is 22 tests, was 19)~~
- ~~Real bug found and fixed in both Packard null-generators
  (`packard_names.rotations`, `packard_v4.rotation_nulls`): a trailing
  frequency-group of size 1 could never be rotated away from its true
  value. Checked and confirmed the affected sign (`AB074`) never
  participated in any counted match or alternation, so no result was
  silently wrong; fixing the grouping (merge trailing group <2 into the
  previous one) still shifts the null baseline slightly since neighboring
  group composition changes. Corrected throughout `paper/paper.md`,
  `docs/PACKARD.md`, `README.md`: name-parallel 4.74:1→4.62:1, alternation
  1.66:1→1.57:1 (z/p values updated to match); direction, significance and
  every conclusion unchanged~~
- ~~`sigla_coverage.py` partition logic, `split_val()`, the 95.9% sweep3
  figure, and the formula_dual "constraints identical" claim all now have
  direct regression tests rather than resting on a printed number, plus the
  rotation null-generators' core invariant (no sign keeps its own value)
  is now directly tested for both replications, plus `same_consonant()`
  (the alternation-test scoring rule) hand-constructed and unit-tested~~
- ~~`sweep1.py`/`sweep2.py` refactored so their headline percentages
  (92.0%, 94.7%/80.6%) are testable: pulled the comparison logic out of
  `main()` into a separable `compare()`, same shape as `sweep3.compare()`
  (`sweep2.py` previously had no `main()` at all - bare module-level code,
  now matches every other stage's structure). Confirmed behavior-preserving:
  both scripts produce byte-identical output before and after.~~
- ~~Full Packard test coverage closed out: `packard_v3.cats()` (the
  final/medial/initial categorization feeding the current v4 alternation
  figures), `lb_value()`/`load_linear_b()` (the Linear B Unicode decoder
  every one of the 429-809 lexicon words depends on - verified against a
  spread of independently-decoded characters plus confirmed a real
  ideogram is correctly excluded, not silently corrupting a word),
  `grid_feasibility.minimal_pairs()` (supplies the alternation pairs
  themselves), and `packard_names.split_val()` (confirmed identical to the
  already-tested `packard.split_val()`). Plus the original checklist's last
  outstanding item: `ocaml_marshal.py` synthetic unit tests (sharing-table
  back-references, nested blocks, bad-magic rejection) - never done before,
  only exercised indirectly via the full SigLA decode. Test suite is now
  48 tests, was 19 at the start of this pass~~
- ~~Packard name-parallel criterion tightened to Knossos-attested names,
  closing §2.2. DĀMOS Knossos word export (2,880 distinct words) intersected
  against the existing NeuroDecipher names lexicon (429 names of 3+ signs) by
  exact transliteration: 154 survive, independently re-counted rather than
  taken on trust. `src/packard_names.py` reworked to report the
  Knossos-restricted figure alongside the old unrestricted one for
  comparison: **20/mean 4.33/4.62:1 (unrestricted) → 10/mean 2.11/4.74:1
  (Knossos-restricted), z = +4.34, p = 0.0020, still 0/9 rotations beating
  observed.** A real, unrelated order-dependency bug found in the same pass:
  the permutation loop shared one `random` stream across all three corpora
  in sequence, so whichever ran second silently depended on how many draws
  the first had consumed. Fixed by reseeding per corpus; only the full-lexicon
  row's permutation stats moved (8.28→8.15, +6.15→+6.18), same direction and
  p-value. Updated throughout `docs/PACKARD.md`, `docs/SOURCES.md`,
  `docs/DAMOS.md`, `docs/PHONOLOGY.md`, `docs/METHODOLOGY.md`,
  `data/README.md`, `paper/paper.md`, `README.md`~~
- ~~`data/verify.sh`'s auto-update of `tests/test_pipeline.py`'s `CORPUS_MD5`
  (added to fix spurious hard-failures on genuine upstream drift) turned out
  to be a real hazard rather than a fix: it silently overwrote the true
  published checksum (`2f5c936f0848fcbcb4ef35669eccca99`) with the checksum
  of a build that was wrong for an unrelated reason - not genuine drift -
  entrenching a false reference that every later run then compared against
  instead of the real one. Confirmed directly: a genuinely fresh, from-clean
  rebuild (`raw_repo`, `nd` freshly cloned, SigLA freshly decoded) reproduces
  the original published figures exactly (411/3644 sweep 1, 94.7%/80.6%
  sweep 2, 95.9% sweep 3) once compared against the restored true checksum -
  there was no upstream drift at any point. `CORPUS_MD5` restored to the
  correct value; `data/verify.sh` no longer auto-writes it, only reports the
  mismatch and asks for a from-clean rebuild to be confirmed before anyone
  updates it by hand.~~
- ~~`src/typology.py`'s positional-preference section ran the original,
  uncorrected binomial-test version with no label saying so - superseded by
  `src/validate_final.py`'s permutation-based version, which is what
  §3.7/§5.4's published 42→24 and 14→3 figures actually come from. Found by
  independently re-verifying those figures against the wrong script first;
  cost a full cycle to discover the two scripts disagree and why. Fixed:
  `typology.py`'s own printed output and a code comment now both state
  clearly that section is superseded and point to `validate_final.py` for
  the published numbers. No data or test changes - this was a labeling gap,
  not a computational error; both scripts always produced what they were
  each individually correct for.~~
