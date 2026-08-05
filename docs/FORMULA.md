# Libation Formula: Dual-Reading Segmentation

Status: first pass complete. Method chosen to bypass D9 rather than resolve it.

## Why this method

D9 established that word division in the religious corpus is contested between
Douros (our source) and Younger, at five sites, in exactly the genre where
segmentation matters most. Rather than adjudicate, the entire analysis was run
**twice, once under each reading**, and only structure surviving both is
reported. Anything appearing under one reading and not the other is flagged, not
claimed.

Corpus: 31 formula-bearing records under reading A, 29 under reading B, selected
by presence of any recurring formula element. No phonetic value or language
hypothesis entered the computation. Slot structure was derived from observed
distribution, **not** imported from any published schema of the formula.

---

## 1. Word order, derived rather than assumed

Mean relative position turned out to be the wrong estimator: on fragmentary texts
a missing head shifts every index, and it produced an ordering that conflicted
with the literature. Pairwise precedence is the correct measure — for each pair
of slots, how often does X precede Y within the same text.

**Reading A and reading B produce identical constraint sets. Ten constraints,
zero contradicting pairs under either reading.**

The derived order:

```
ATAI-*301-WA-JA  →  [SASARA slot]  →  U-NA-KA-NA-SI  →  I-PI-NA-MA  →  SI-RU-TE
```

This was recovered from distribution alone and then found to agree with Younger's
published schema (his words 1, 4, 5, 6, 7). Independent recovery of an accepted
result is the useful outcome here: it is evidence the pipeline works, not a new
finding. The corollary matters more — the ordering is **invariant under the
contested word division**, so D9 does not threaten it.

## 2. Boundary-stable slots

Five slots recovered identically under both readings:

| Slot            | Position     | Attestations |
|-----------------|--------------|--------------|
| ATAI-*301-WA-JA | always first | 11 / 10      |
| I-PI-NA-MA      | medial       | 6 / 6        |
| U-NA-KA-NA-SI   | medial       | 4 / 6        |
| SI-RU-TE        | late         | 7 / 6        |
| I               | always last  | 2 / 2        |

## 3. The SASARA slot: alternation is real, its form is not

This is the substantive result, and it is a *qualified* one.

|          | Reading A (Douros)                  | Reading B (Younger)                   |
|----------|-------------------------------------|---------------------------------------|
| variants | JA-SA-SA-RA-ME (7), SA-SA-RA-ME (2) | JA-SA-SA-RA-ME (4), A-SA-SA-RA-ME (3) |

**The existence of an alternation in this slot is boundary-stable.** Both readings
agree that the slot has a variable left edge, and both agree on its position in
the sequence.

**What alternates is boundary-dependent.** Under reading A, the alternation is
presence against absence of an initial JA-. Under reading B it is JA- against A-.
These are different morphological analyses: the first is an affix that may be
absent, the second is an affix with two allomorphs.

The distinction is not cosmetic. Duhoux's I-/J- prefix analysis, the basis for
reading a case or directional marker here, depends on which of these is correct,
and the corpus cannot currently decide between them. **Any claim about prefixation
in the libation formula inherits this ambiguity** and should state which reading
it assumes.

## 4. Boundary-dependent, reported but not claimed

Two slots appear only under reading B: I-NA-JA-RE-TA and QA2. Both come from
AP Za 2, where Younger prints a reconstructed re-ordering after the text. The
duplicate block is filtered, but the underlying reading remains his reconstruction
rather than a direct transcription, and it should not be treated as attested.

---

## 5. Peer-review to-do

Carried forward for the final paper. These are *not* blockers for the analysis
above, which is by construction independent of them, but they are the checks a
reviewer will ask for.

1. **GORILA plate adjudication of D9.** Five contested word-division sites, each
   requiring inspection for a word-divider dot at a specific ridge. Requires
   autopsy; cannot be done computationally. Resolving it would collapse the dual
   reading to a single one and settle the SASARA alternation.
2. **SigLA cross-check.** Independent, ERC-backed witness on word division and
   palaeography. Currently blocked: `sigla.phis.me` is outside the sandbox network
   allowlist. Needs an allowlist change or a manual export.
3. **External validation against an independent sample dataset.** To be run when
   one is available. The comparison must align on GORILA sign ids, never on
   labels, and should be audited on the five axes in PROCEDURE.md section 6.
   Purpose is confirmation of the pipeline, not new data.
4. **D4 (AB21/AB22)** and **D7 (numerals)** remain open but gate only the
   livestock and accounting analyses respectively. Neither touches this section.

## 6. Standing caveat on sample size

The whole formula rests on 119 word tokens under reading A and 124 under B.
Individual slots are attested 2 to 11 times. Nothing here should be quoted
without its n, and any slot attested fewer than about 5 times is a hypothesis.
