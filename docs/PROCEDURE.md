# Linear A Pipeline: Procedure and Defect Register

Version: corpus_v1
Status: Stage 1 complete (ingestion + normalization). Stage 2 (structural analysis) not started.

This document records every transformation applied between the source data and
`corpus_v1.json`. It exists so that results can be reproduced, audited, and
compared against other people's datasets on equal terms. Nothing in the pipeline
should be trusted further than this register allows.

---

## 1. Provenance chain

| Layer                              | Source                                                                                                                           | Status                                     |
|------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|
| Sign transcription                 | GORILA (Godart & Olivier, *Recueil des inscriptions en linéaire A*, EtCret 21, vols. 1-5, 1976-1985), digitised at cefael.efa.gr | Peer-reviewed standard corpus              |
| Word division, ideograms, numerals | George Douros, spreadsheet tabulation                                                                                            | Independent compilation, NOT peer-reviewed |
| Commentary                         | John G. Younger, *Linear A Texts & Inscriptions in Phonetic Transcription*                                                       | Credentialed, explicitly non-decipherment  |
| Extraction / OCR / CSV → JSON      | `mwenge/lineara.xyz` (hobbyist pipeline)                                                                                         | Unreviewed; own error surface              |

Our ingest point is the `mwenge/lineara.xyz` JSON. Every defect below originates
at that layer or the Douros layer, not in GORILA.

**Validation performed.** Independent spot-checks against published scholarship:

- Libation genre: IO Za 2, PK Za 11, PK Za 12 match Karetsou/Godart/Olivier readings exactly.
- Administrative: HT 18, HT 19, HT 86a, HT 95a, HT 114, ARKH 2, ARKH 3, AP Za 1, AP Za 2, AR Zf 1, AR Zf 2 match Younger exactly.

Conclusion: the source is **sound at the level of sign sequences**. All defects
found were in the derived ASCII label layer, not in the signs themselves.

---

## 2. Governing principle

> **The Unicode sign identity is the data. Every ASCII label in the source repo
> is a lossy, derived rendering and is regenerated from the sign ID.**

Defects D1, D2 and D3 are three symptoms of one cause: analysis was being drawn
from `transliteratedWords` (labels) rather than `words` (signs). Adopting the
sign layer as authoritative fixes all three at once.

---

## 3. Defect register

| ID      | Defect                                                                                                                                                            | Impact                                                                                                              | Status                                                                                                                                |
|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| **D1**  | Break/damage marker `U+1076B` present in `words` but **stripped** from `transliteratedWords`. 990 of 3612 sign-groups affected.                                   | Fragments silently read as whole words. Would have inflated the lexicon by 374 phantom types (1247 → 873 distinct). | **FIXED** (S2)                                                                                                                        |
| **D2**  | Fraction signs pre-converted to numeric values (A703 D → `¹⁄₅`, A706 H → `¹⁄₆`). Younger flags these as *surmised*, not demonstrable; only J, E, F, K are secure. | Uncertain conjecture hardened into data. Same contamination class as `translatedWords`.                             | **FIXED** (S3)                                                                                                                        |
| **D3**  | L-subfraction index dropped in labels (`GRA+K+L` for sign A584 = GRA+K+**L2**). Also VINa flattened to `VIN` while VINb survived as `*131B`.                      | Would corrupt metrology and commodity-variant analysis.                                                             | **FIXED** (S1) — the sign ID never lost the distinction; only the label did.                                                          |
| **D4**  | AB21/AB22 systematically inverted in our source (sheep vs goats), 18 sites across 14 documents.                                                                   | Livestock species assignment wrong corpus-wide.                                                                     | **RESOLVED and CORRECTED** (S7) — SigLA agrees with Younger 15/15; our source is the outlier. Inversion applied in `build_corpus.py`. |
| **D12** | Doubtful-reading marks absent from every layer of our source.                                                                                                     | A doubtful sign is indistinguishable from a confident one; contaminates every frequency statistic.                  | **RESOLVED** (S7) — SigLA carries certainty natively: 4712 confident, 44 doubtful, 388 unreadable of 5144.                            |
| **D5**  | `KN Zg 57b`: 10 signs present, zero transliteration.                                                                                                              | Single gap in Douros.                                                                                               | Logged, not blocking                                                                                                                  |
| **D6**  | 4 stray codepoints (`U+1076C-E`, `U+FD1EB`) not valid signs.                                                                                                      | Extraction noise.                                                                                                   | **FIXED** (S1, stripped and counted)                                                                                                  |

Excluded upstream by standing decision: **`translatedWords`** (Linear B-derived
semantic glosses, e.g. rendering KI-RO as "owed"). Held in reserve for late-stage
cross-check only. It is never pipeline input.

---

## 4. Transformation sequence

**S0. Extract.** `raw_repo/LinearAInscriptions.js` evaluated in a JS sandbox,
Map serialized to `inscriptions_clean.json`. `translatedWords` dropped at this step.

**S1. Sign resolution.** For each token, characters resolved to GORILA/Unicode
sign IDs (`AB008`, `A584`, `A709-2`) via the Unicode character name. Stray
codepoints stripped. The repo's ASCII string is retained as `label_repo` for
reference only and is never read by analysis code.

**S2. Damage preservation.** `U+1076B` parsed into structured flags:

- `damage.before` : material missing before the token (`]WORD`)
- `damage.after`  : material missing after the token (`WORD[`)
- `damage.internal`: break inside the token
- `complete` : true only if none of the above

Positional counts: 537 leading, 586 trailing, 227 both, 28 internal, 553 standalone lacunae.

**S3. Measure annotation.** Fraction and weight signs are recorded by **sign
identity**. Any numeric value is carried separately as annotated conjecture with
an explicit confidence grade and citation:

- `secure` (300 tokens): J, E, F, K and their composites JE, EF, JF. Demonstrable (Pope 1960; Bennett 1999).
- `conjectured` (153): A, B, D, H, L2, JH, Om, DD. Proposed but explicitly uncertain.
- `unknown` (32): L, L3, L4, L6, W, X, Y.

Analysis code must not consume `value_conjecture` without filtering on `confidence`.

**S4. Token typing.** `signgroup` / `numeral` / `measure` / `divider` / `ruling` /
`lacuna` / `line_break`. Note `ruling`: the em dash in the source is not a sign
but a horizontal rule marking a **section boundary** on administrative tablets
(56 occurrences, e.g. between the A-KA-RU and A-DU lists on HT 86a). Recovered as
structural data.

**S5. Record identity.** Recto/verso are separate records in the source. `doc_id`
and `side` are split out. 1721 records resolve to **1621 distinct documents**.
Any document-level statistic must aggregate on `doc_id`, not `record_id`.

**S7. External adjudication against SigLA.** SigLA (Salgarella & Castellan,
CC BY-NC-SA) ships its corpus in `database.js` as two OCaml `Marshal` blobs
escaped as decimal octets inside JavaScript string literals. Field names are
absent because `Marshal` stores records positionally, so the data is not
greppable; it was decoded with a purpose-built parser (`ocaml_marshal.py`) and
the record layout recovered structurally, cross-checked against
`sigil/import/importer.ml`. Yield: **802 documents, 5144 attestations**, of
which 686 documents overlap our 1721 records.

This resolved two defects.

**D4 is corrected, against our own source.** On the twelve shared AB21/AB22
documents SigLA agrees with Younger on **15 of 15 sites, in both directions**,
without exception. A perfect inversion across fifteen independent sites is not
fifteen misreadings; it is a systematic mis-mapping in the Douros tabulation.
The inversion is now applied at build time and the corpus reproduces SigLA on
12/12 documents. Note the consequence for policy S6: the divergence register
existed to defer adjudication, and here deferral was vindicated — had we
silently "corrected" toward either witness at the time, we would have had no
means of detecting that the disagreement was systematic rather than scattered.

**D12 is resolved.** SigLA records reading certainty per attestation: 4712
confident, **44 doubtful**, 388 unreadable or unclassified, plus 104 erasures
and 7 ghosts. 8.4% of attestations fall in categories our corpus cannot express.

**S6. Divergence policy.** Where our source disagrees with published scholarship
on a substantive reading, the **source reading is retained** and the divergence
is logged in `divergences.json`. We do not silently patch, and we do not adopt
alternatives ad hoc. Consistency plus auditability is preferred to case-by-case
correction, because selective patching would make the corpus unreproducible and
would import the patcher's priors invisibly.

*Important qualification.* Retaining the source reading is **not** an independent
judgment in our favor. On a contested sign we have no independent evidence: we
are passing through Douros' reading, and "trusting the pipeline" here means
trusting Douros over Younger on that one point. The pipeline is trustworthy as
*processing*; it has no authority as *autopsy*. Every such case must therefore
carry an `adjudicable_by` field naming the evidence that would settle it, and
downstream results sensitive to it must be re-runnable under the alternative
reading.

---

## 5. Corpus profile (corpus_v1)

```
records                 1721        distinct documents      1621
sign-groups             3612          complete              2659
                                      damaged                953
numerals                1297
measures                 428
dividers                 468
lacunae                  556
rulings                   56
```

Of complete sign-groups, roughly two thirds are **single-sign** tokens
(transaction signs, logograms, ideograms) rather than lexical words. Complete
**multi-sign** sign-group instances number under 1000.

**This is the binding constraint on the whole project.** Any grammatical or
morphological claim rests on that base, and roughly a quarter of the corpus is
fragmentary. Fixing expectations to this number now is preferable to discovering
it after the structural analysis.

---

## 6. Comparing against other datasets

To compare our output with a third party's sample, align on `sign_ids`, not on
labels. Label conventions differ across GORILA, Younger, Douros and SigLA
(e.g. QIf vs `*21F`, CAPm vs `*21M`, FIC vs NI), and label-level comparison will
generate spurious disagreements.

Checklist when importing an external sample:

1. Does it preserve break/damage notation? If not, its word counts are inflated (cf. D1).
2. Does it carry fraction signs or pre-computed values? If values, which confidence grade (cf. D2)?
3. Does it distinguish L/L2/L3/L4/L6 and VINa/VINb/VINc (cf. D3)?
4. Does it merge recto/verso (cf. S5)?
5. Does it carry Linear B-derived semantic glosses, and are they segregated?

---

## 7. Divergence register

Maintained in `divergences.json`. Generated by `sweep1.py`; reproducible.

### Sweep 1: corpus_v1 vs Younger (complete)

Younger's commentary is vendored in the source repo (`raw_repo/commentary/`,
1694 files), so the comparison needed no network access. Of these, 351 are
tabular sign records; 137 are roundel/sealing tables on a different schema
(seal impressions, CMS numbers) and were excluded as non-sign tables; the
remaining ~1200 are non-tabular and were **not** machine-compared.

| Measure                | Value     |
|------------------------|-----------|
| Records compared       | 411       |
| Tokens compared (ours) | 3644      |
| Tokens agreeing        | 3329      |
| **Token agreement**    | **91.4%** |
| Divergence sites       | 211       |

Comparison is on canonicalized labels with documented convention equivalences
folded first (FIC/NI, VINa/VIN, CYP/*303, AROM/*123, QIf/*21F and so on).
Without that folding raw agreement reads 70.5%, almost all of it spurious.

**Three false alarms were found in our own tooling before the residual settled**,
which is worth recording because each would have inflated the divergence count:
Younger's fraction column header carries scare quotes (`"fraction"`) and was
silently dropped by the key lookup, accounting for ~89 phantom mismatches; the
alias table was consulted after upper-casing so mixed-case keys never matched;
and Younger's editorial apparatus (*vest.*, *vacat*, *supra mutila*) was being
compared as if it were sign data.

### Classified findings

| ID     | Kind                            | Sites                   | Status |
|--------|---------------------------------|-------------------------|--------|
| **D4** | AB21/AB22, sheep vs goats       | 18 sites / 14 documents | open   |
| **D7** | Numeral disagreements           | 4                       | open   |
| **D8** | Other sign readings (long tail) | 127                     | open   |

**D4 is the substantive result of the sweep.** It was originally logged as a
single conflict at HT 20. It is in fact systematic: AB21 (QI/OVIS, sheep) and
AB22 (CAP, goats) are read differently by Douros and Younger across Haghia
Triada, Khania, Knossos, Phaistos and Zakros, and the disagreement runs in
**both directions**. Livestock species assignment is therefore contested corpus
wide, and no analysis of animal categories should be run until it is adjudicated.

**D7 is small but weighted.** Four numeral conflicts, but numerals feed the
accounting analysis directly and HT 10a differs by an order of magnitude
(14 against 104).

**D8 is a long tail** of mostly singleton sign disagreements. Some residual
convention noise is certainly still in this bucket; each site needs individual
adjudication before use, and it should not be quoted as 127 confirmed conflicts.

### Sweep 2: non-tabular records, including the libation corpus (complete)

Younger's free-text records parse differently: `<dd>` transliteration lines with
`<u>` marking doubtful readings and `•` as word divider. 1142 records parsed,
994 compared, of which 139 are religious (Z-type supports).

| Measure                                    | Value     |
|--------------------------------------------|-----------|
| Token agreement, all non-tabular           | **94.7%** |
| Token agreement, libation/religious subset | **80.6%** |
| Divergence sites                           | 44        |

Three further defects were in our tooling, not the data, and each is worth
recording. The scraped HTML has malformed nesting in which red-font commentary
tags *wrap* black-font transliteration; removing red subtrees naively deleted
1002 real records and left only 190. Whitespace inside `<u>` tags fragmented
sign groups and suppressed every doubtful-reading flag, reporting 0 where there
are 121. English prose from Younger's physical descriptions leaked into the
token stream and depressed the libation figure. The pattern from sweep 1 held:
the first number out of a comparator measures the comparator.

### D9: word division in the religious corpus

The substantive result. Five sites have **identical signs but different word
boundaries**, and every one falls on a Z-type support:

| Record        | Ours                     | Younger               |               |
|---------------|--------------------------|-----------------------|---------------|
| HT Zd 157+156 | TA-JA \                  | K                     | TA-JA-K       |
| KN Zc 6       | JU-KU-NA-PA-KU-NU-U-I-ZU | JU-KU-NA-PA-KU-NU-U \ | I-ZU          |
| PK Za 8       | JA-SA-U-NA-KA-NA-SI      | JA-SA \               | U-NA-KA-NA-SI |
| PR Za 1       | TA-NA-SU-TE-KE           | TA-NA-SU-TE \         | KE            |
| SY Zb 7       | RA-KI-NI-SE              | RA-KI \               | NI-SE         |

This matters more than its count suggests. Word division is the **Douros**
contribution, not GORILA, and it is the primary evidence for morphological
segmentation. U-NA-KA-NA-SI is word 5 of the libation formula, the presumed
verbal that Davis reads as opening the subordinate clause. Whether JA-SA is
attached to it or separate changes the segmentation of the formula itself.
Duhoux's affix statistics, the basis of the agglutination claim, are computed
over exactly these boundaries.

### Sweep 3: corpus_v1 vs SigLA (complete)

Third witness, compared on GORILA sign **number** only, since the two corpora use
different variant conventions for the same sign.

| comparison                      | documents | tokens | agreement | sites |
|---------------------------------|-----------|--------|-----------|-------|
| all signs                       | 666       | 4540   | **91.8%** | 301   |
| all signs, SigLA-confident only | 666       | 4540   | 91.2%     | 312   |
| **syllabograms only**           | 657       | 4105   | **95.9%** | 156   |
| syllabograms only, confident    | 657       | 4105   | 95.2%     | 171   |

**Three findings.**

**The 91.8% / 95.9% gap is fractions, not disagreement.** SigLA records 332
fraction tokens against our 447, and A732 (JE) is absent entirely — 32 in ours,
0 in SigLA. A palaeographic database indexes drawn sign forms, so composite
fractions are plausibly drawn as components or not drawn at all. This is a
coverage difference, and SigLA must **not** be used to adjudicate fraction
counts. On syllabograms, where both corpora claim exhaustive coverage,
agreement is **95.9%** — our highest against any witness.

**Certainty does not explain the residual.** Restricting to SigLA-confident
signs makes agreement slightly *worse* (95.9% → 95.2%, sites 156 → 171). Our
disagreements are therefore not concentrated in readings SigLA flags as
doubtful. D12 remains a real defect in our corpus, but it does not account for
the divergence, and the KN Zc 6 case must not be generalized.

**D4 was the only systematic error.** After correction the substitution tail is
flat: no sign pair recurs more than twice across 666 documents. The residual is
a long tail of singletons, consistent with ordinary editorial variation rather
than a second mis-mapping.

### Triage of D8/D10 against SigLA

The two long tails from the Younger sweeps — 137 sites — were never adjudicated.
With a third witness they can be. Sites are testable where the conflict is
sign-type (not fraction or numeral, which sweep 3 showed SigLA under-records) and
the document is in SigLA: **84 of 137**.

| outcome                                         | n     |
|-------------------------------------------------|-------|
| identical after normalisation                   | 14    |
| identical after convention folding              | 18    |
| near-identical / tokenisation / annotation only | 9     |
| SigLA adjudicates, backs our source             | 11    |
| SigLA adjudicates, backs Younger                | 2     |
| ambiguous or absent in SigLA                    | 7     |
| never a conflict (ours == Younger)              | 14    |
| **GENUINE sign conflict**                       | **9** |

**D8 was inflated roughly nine-fold by convention, not disagreement.** The bulk
resolve to the same sign under two naming systems — HIDE = \*180, MU = \*23,
SO = \*363, PU3 = \*314 — or to ligature tokenization and annotation markers.
This is the fourth time comparator convention has masqueraded as substantive
divergence, after the scare-quoted `"fraction"` header, the malformed red-font
nesting, and vessel notation.

**Where SigLA can adjudicate, it backs our source 11 to 2.** That is the
opposite of D4 and worth stating plainly: our source is not globally unreliable.
It had one systematic error, now corrected. The two sites where SigLA sides with
Younger are HT 132 (\*904 vs \*319) and PH 8a (\*416L2 vs \*417L2).

**Nine genuine conflicts remain**, listed in `divergences.json`: ARKH 1b, HT 15,
HT 17, HT 34 (×2), HT 49a, KH 74, KH 8, MA 10b. These need plate collation.

### What remains unswept

The SigLA cross-check is still blocked (`sigla.phis.me` is outside the sandbox
allowlist). D9 raises its priority: word division in the religious corpus is now
known to be contested, and SigLA is the ERC-backed independent witness.

---

## 8. Open items

- **D4** AB21/AB22, 18 sites: gates livestock analysis only.
- **D7** numeral conflicts, 4 sites: gates accounting reconstruction.
- **D8/D10** sign-reading long tail: adjudicate per document before use.
- **D9** word division, 5 sites: **gates libation formula segmentation.**
- SigLA cross-check (blocked, needs allowlist change or manual export).
- Genre tagging not yet applied.
- Provisional Linear B phonetic values remain quarantined from structural
  analysis until the typological profile is built independently.
