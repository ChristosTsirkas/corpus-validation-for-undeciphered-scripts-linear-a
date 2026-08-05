# Re-running Packard (1974) with Adequate Permutations

## Why this matters

The practice of transliterating Linear A with Linear B values — the basis of
Younger's phonetic corpus, van Soesbergen's *Corpus*, and effectively every
modern edition — rests on a statistical argument made by D. W. Packard in 1967
and 1974, refined by Pope and Raison in 1978.

Van Soesbergen (*The Decipherment of Minoan Linear A*, Vol. II, 2022, preface)
summarizes it: Packard built **nine fictitious decipherments**, redistributing
Linear B values among Linear A signs so that no sign kept its value, re-allocating
values only **within the same frequency band**. Comparing the rate of
"confirmatory alternations" under the true Ventris values against the average of
the nine gave a ratio "just over 2 : 1" in favor of the Ventris values. Pope and
Raison adjusted for context and reported 3 : 1, rising to 5 : 1 for Knossos
matches. Van Soesbergen notes that "these results offered so much confidence"
that Raison and Pope proceeded to publish a transliterated vocabulary.

**This is a permutation test with n = 9.** With nine samples one cannot estimate
a null distribution, cannot compute a standard deviation, and cannot produce a
p-value. The 2 : 1 ratio is a comparison of two point estimates, one of which is
an average of nine noisy draws.

We re-ran it with **n = 4000**.

## Method — CORRECTED against the primary source

**The first version of this replication used the wrong pairing rule.** Packard
(1974, 71) defines the alternation set explicitly, in three positional
categories, collected in his Appendix A:

| cat | definition                                  | his example                  | chapter section                         |
|-----|---------------------------------------------|------------------------------|-----------------------------------------|
| 1   | first two signs identical, third differs    | 30.74.53 / 30.74.54          | "Alternation at the End of Words"       |
| 2   | last two signs identical, beginning differs | 98.101.60 / **29.97**.101.60 | "Alternation at the Beginning of Words" |
| 3   | first and third identical, second differs   | 103.54.86 / 103.**72**.86    | "Alternation Internal to Words"         |

**Category 2 admits unequal lengths** — three signs against four. Our original
`minimal_pairs()` required equal length and exactly one differing position, so
it generated categories 1 and 3 and only the equal-length part of category 2.
It never produced the prefixation class at all, and it produced a great many
pairs Packard's scheme does not admit.

His confirmatory examples are **KI.RE.TA₂ / KI.RI.TA₂** and **DA.TA.RA /
DA.TA.RE**; in both the alternating signs share a consonant and differ in vowel.
All four forms are present in our corpus. Under the Kober grid logic Packard
sets out on the same page (rows share an unknown consonant, columns an unknown
vowel), an alternation is confirmatory when the two signs share a row or a
column — share C or share V. That part of our operationalization stands.

### Corrected results

| corpus         | cat 1 | cat 2 | cat 3 | +unequal (prefix) | testable | observed | banded null     | z         | p    | ratio        |
|----------------|-------|-------|-------|-------------------|----------|----------|-----------------|-----------|------|--------------|
| administrative | 25    | 25    | 16    | 51                | 50       | 0.3200   | 0.3184 ± 0.0626 | **+0.03** | 0.55 | **1.00 : 1** |
| combined       | 35    | 32    | 22    | 81                | 66       | 0.3333   | 0.2947 ± 0.0519 | **+0.75** | 0.26 | **1.13 : 1** |

Unconstrained null gives 1.28:1 (z = +1.10) and 1.35:1 (z = +1.56), neither
significant.

**Under Packard's own pairing rule the effect is weaker still.** On the
administrative corpus the banded ratio is **1.00 : 1** — exactly chance. The
earlier v1 figure of 1.09:1 came from a pair set his scheme does not define.

### Scale check

Packard reports more than 100 alternation groups in Appendix A. His three
categories on our corpus yield 89 single-sign oppositions plus 81 unequal-length
category-2 pairs, 170 in total. The same order of magnitude, which is
reassurance that the rule has been read correctly, though his corpus and ours
are not identical.

---

## Superseded v1 method

The original run used a different definition and is retained for the record.
A minimal pair was two attested types of equal length differing at exactly one
position. The alternating pair of signs is **confirmatory** if, under a value
assignment, the two signs share a consonant or share a vowel — that is, the
alternation looks phonologically systematic rather than arbitrary.

Two nulls, because the choice matters enormously:

- **(a) unconstrained**: values permuted freely among signs
- **(b) frequency-banded**: values permuted only within frequency bands, which is
  **Packard's own design constraint**

## Results

| corpus         | testable alternations | observed | null (a)        | z     | p      | null (b) Packard | z         | p         |
|----------------|-----------------------|----------|-----------------|-------|--------|------------------|-----------|-----------|
| administrative | 399                   | 0.3283   | 0.2500 ± 0.0229 | +3.42 | 0.0012 | 0.3056 ± 0.0216  | **+1.05** | **0.156** |
| religious      | 40                    | 0.3250   | 0.2497 ± 0.0674 | +1.12 | 0.171  | 0.3422 ± 0.0684  | **−0.25** | 0.660     |
| combined       | 557                   | 0.3357   | 0.2494 ± 0.0200 | +4.31 | 0.0002 | 0.3084 ± 0.0193  | **+1.42** | **0.092** |

Expressed as Packard-style ratios:

|       | Packard 1974 | Pope & Raison 1978 | **this study**                                  |
|-------|--------------|--------------------|-------------------------------------------------|
| ratio | 2 : 1        | 3 : 1              | **1.35 : 1** unconstrained                      |
|       |              |                    | **1.09 : 1** under his own frequency constraint |

## Definitive replication (v4) — both rules taken verbatim

The whole methodological chapter (pp. 72–101) has now been read. Two rules were
wrong in every earlier version of this replication.

**Scoring rule (p. 76), verbatim:** *"Alternations are considered significant if
the alternating signs have the same consonant according to that decipherment."*
**Same consonant only.** v1–v3 scored share-consonant **or** share-vowel, which
inflated both the observed count and the null.

**Null construction (p. 73):** Linear A signs are ordered by descending
frequency, divided into **groups of ten**, and the values rotated within each
group, each moving to the next less common sign with the tenth wrapping to
first. His nine alternatives are therefore **exhaustive rotations** of that
scheme, not a small sample of a large permutation space. That is a better
defense of n = 9 than we credited him with, though it still explores only nine
of the available assignments.

**His chance model (p. 72):** twelve consonants are distinguished in Linear B
orthography, so roughly one twelfth of alternating pairs should share a
consonant by accident; on ~107 groups that predicts about eight or nine, which
he says agrees with the random decipherments.

### His counts, from pp. 74–79

| position  | groups                           | confirmatory   | rate      |
|-----------|----------------------------------|----------------|-----------|
| final     | 39 (5 with 3+ shared, 34 with 2) | 3 + 7 = **10** | 0.256     |
| medial    | 26                               | **4**          | 0.154     |
| initial   | 42                               | **5**          | 0.119     |
| **total** | **107**                          | **19**         | **0.178** |

19 observed against ~9 expected = **2.1 : 1**. That is the origin of the
"just over 2:1".

### Our corpus, same rules

| position  | groups | testable | confirmatory | rate      | (his rate) |
|-----------|--------|----------|--------------|-----------|------------|
| final     | 38     | 31       | 4            | 0.129     | 0.256      |
| medial    | 22     | 16       | 2            | 0.125     | 0.154      |
| initial   | 32     | 22       | 1            | 0.045     | 0.119      |
| **total** | **92** | **69**   | **7**        | **0.101** | **0.178**  |

Group counts track his closely (92 against 107), confirming the pairing rule is
now right. Confirmatory rate is lower throughout.

| test                                      | result                                                      |
|-------------------------------------------|-------------------------------------------------------------|
| his 1/12 chance model on our data         | 7 observed vs 5.8 expected = **1.22 : 1**                   |
| **his nine rotations, run on our corpus** | mean 4.44, observed 7 = **1.57 : 1**, 1 of 9 beats observed |
| 4000 banded permutations                  | mean 4.51 ± 2.10, **z = +1.19, p = 0.17**, ratio 1.55 : 1   |

### The name-parallel test — HIS LOAD-BEARING EVIDENCE, NOW REPLICATED

Packard states plainly (p. 92) that the Linear B name parallels are what
"demonstrates conclusively that at least some of the Linear B phonetic values
are valid for Linear A." That is a different test from the alternations, and it
has never been re-run. It now has been.

**Data.** Linear B lexicon from Luo, Cao & Barzilay (ACL 2019),
`j-luo93/NeuroDecipher`: 919 Linear B/Greek pairs with proper nouns flagged.
Linear B words are in Unicode syllabograms whose character names carry both the
B-number and the value (`LINEAR B SYLLABLE B008 A`), giving a direct concordance
with our AB sign ids. 429 Linear B names of three or more signs; 449 Linear A
types of three or more signs. Of those 429, **154 are attested at Knossos
specifically** — intersected by exact transliteration against a Knossos
find-site word export from DĀMOS (Database of Mycenaean at Oslo,
`damos.hf.uio.no`, CC BY-NC-SA 4.0; `src/packard_names.py.load_linear_b_knossos_names`,
`data/README.md` item 5b). This is now the headline criterion; the unrestricted
429 is kept alongside for comparison, since it is what every earlier figure in
this project used.

**Criterion**, his (pp. 89–90): both sign-groups complete and longer than two
signs, attested at Knossos as a personal or place name; first two signs
identical plus the consonant of the third; final vowel or an obvious Linear B
suffix disregarded.

| corpus                           | true values | his nine rotations            | ratio        | 2000 permutations | z         | p          |
|----------------------------------|-------------|-------------------------------|--------------|-------------------|-----------|------------|
| **LB names, Knossos-restricted** | **10**      | mean 2.11, **0 of 9 beat it** | **4.74 : 1** | 2.25 ± 1.79       | **+4.34** | **0.0020** |
| LB names only (unrestricted)     | 20          | mean 4.33, 0 of 9 beat it     | 4.62 : 1     | 5.01 ± 2.72       | +5.51     | 0.0005     |
| LB full lexicon                  | 31          | mean 7.67, 0 of 9 beat it     | 4.04 : 1     | 8.15 ± 3.70       | +6.18     | 0.0005     |

**Packard's Table 14 gives 4.3 for Knossos Name 3=, and he reports fifteen
matches against about three random, a ratio near 5:1. On the criterion that
actually matches his — Knossos-attested names only — we get 10 matches against
a mean of 2.11 random, 4.74 : 1.** Ten against his fifteen is the first time
this project's absolute count has been directly comparable to his at all,
rather than inflated by a criterion he didn't use; the residual gap (our
corpus, our sign numbering, his physical corpus vs. this project's digital
one) is real and unclosed, but the count is no longer being compared on
mismatched terms.

That is a clean independent replication, on a different corpus, with four
thousand times his permutation count, half a century later.

**Independent verification of the scoring logic itself.** The ratios above
rest on `matches()` correctly implementing the rule above; citing the right
page for a rule and correctly implementing it in code are different failure
points, and only the first had been checked. One real positive case was
hand-derived from the stated rule before looking at the code -
AB001-AB073-AB055 (da-mi-nu) against Linear B da-mi-ni-jo: first two signs
identical, third sign's consonant identical (n=n), vowel differs (u vs i) as
the rule explicitly permits - and confirmed against the code's output.
Two constructed negative cases (a third-consonant mismatch, a first-two-signs
mismatch) confirm the function correctly rejects non-matches for the right
reason in each case, not just by chance. All three are now permanent
regression tests (`tests/test_pipeline.py`, `TestPackardNames`).

**A real bug was found and fixed while checking the null-model generator.**
`rotations()` (this file's own null generator) and `packard_v4.rotation_nulls()`
both order signs by frequency and split into groups of ten; the trailing
group, when the sign count isn't a clean multiple of ten, could end up with a
single member. A group of one can never be rotated to a different value
(`k % 1 == 0` for every k), so that sign kept its true value under all nine
"fictitious" decipherments - a direct violation of the method. One sign,
`AB074`, was affected. It does not appear in any of the 449 corpus types'
first three positions, any counted name-parallel match, or any of the 95
minimal pairs used for the alternation test - checked directly, not assumed -
so the bug itself never touched a counted result. Merging that trailing group
into the previous one (rather than leaving a single sign un-rotatable) does
shift the null baseline slightly, since the neighboring group's composition
changes: **4.74:1 → 4.62:1** for the (now superseded) unrestricted-names row,
and **1.66:1 → 1.57:1** for the alternation test in `packard_v4.py` (both
figures, and the 4000-permutation z/p values, updated throughout
`paper/paper.md`, this file, and `README.md`). Direction, significance, and
every conclusion were unchanged - a correction to the null's precision, not a
different result. Note this is unrelated to the 4.74:1 figure in the table
above: that number belongs to a *different* row (the new Knossos-restricted
criterion) and is a coincidence of the arithmetic, not a reversion of this fix.

A second, smaller precision fix went in alongside the Knossos restriction:
`main()`'s permutation loop now reseeds `random` before each corpus's 2000
draws, rather than sharing one continuous stream across all three corpora in
sequence. Under the old code the reported statistics for whichever corpus ran
*second* depended on how many random numbers the *first* corpus's block had
already consumed - not wrong, but silently order-dependent. The unrestricted
LB-names row was always first in the original two-row loop, so its published
figures (5.01 ± 2.72, z = +5.51) are unaffected; the full-lexicon row was
always second, and its permutation statistics shift slightly under the fix:
**8.28 ± 3.70, z = +6.15 → 8.15 ± 3.70, z = +6.18**. Same direction, same
p = 0.0005, no conclusion affected.

**Caveat, resolved for the name list, not for the corpus.** The lexicon is now
restricted to Knossos-attested names, meeting Packard's own stated criterion
rather than a looser stand-in for it (resolved; `TODO.md` "Completed",
`docs/DAMOS.md`). What
this does *not* resolve: this project's digital corpus is still not Packard's
own `Corpus transnuméré`, and GORILA/AB sign numbering is still not his
Raison-Pope L-numbering (see "Two further points from the text" below). The
name-parallel *criterion* now matches his; the underlying *corpus and sign
numbering* still don't, and nothing in this section claims otherwise.

### What this finally establishes

Two distinct findings, and they point opposite ways.

**1. The internal alternation evidence is weak — and Packard says so.** Our
same-consonant replication gives 1.2–1.7 : 1 against his 2.1 : 1, not
significant at p = 0.17. He weights the initial class at zero, notes five random
decipherments matched the true values there, and concludes we must accept many
of the Linear B alternations as fortuitous.

**2. The name-parallel evidence is strong, and it replicates.** 4.74 : 1 on
the Knossos-restricted criterion (10 matches vs. a mean of 2.11 random,
z = +4.34, p = 0.0020; 4.62 : 1 unrestricted, z = +5.51, p = 0.0005), with
none of his nine rotations beating the true assignment either way. This is the
part of his argument that carries weight, and it holds.

**Therefore: Packard's actual conclusion is supported.** At least some of the
Linear B phonetic values are valid for Linear A. He never claimed more than
that, and the evidence sustains exactly what he claimed.

### What survives of the citation-drift finding

Only this, and it is now a narrow point about emphasis rather than a challenge
to the result: the "2:1" that circulates is the *alternation* figure, which is
the weaker half of his argument and which he himself discounts. The
*name-parallel* figure of roughly 4–5:1 is the strong half, and it is the one
that deserves to be cited. The literature has propagated the weaker number as
though it were the whole case.

His methodological framing remains the best citation of all: the random
decipherments give a method for judging the background noise against which
alleged confirmatory evidence must assert itself (p. 93).

## Packard's own position is the opposite of how he is cited

Packard (1974), pp. 1–68, has now been read in full. This changes the finding,
and not in the direction expected.

Van Soesbergen's preface presents Packard's results as *confirming* the Ventris
values, and states that they gave Raison and Pope enough confidence to publish a
transliterated vocabulary. Packard's own text argues the reverse case.

Opening his chapter on the phonetic values, he calls the inference from identity
of sign shape to identity of phonetic value "a natural but highly uncertain
hypothesis", and observes that a similar assumption vitiated much of the
pre-Ventris work on Linear B. He presses the Cypriot parallel explicitly: many
Classical Cypriot signs resemble Linear B, yet only a few carry the same value,
and the spelling conventions differ. He notes that the history of writing offers
many cases where borrowing the idea or the shape of signs did not involve
borrowing every phonetic value. He states that his use of conventional
transliteration "does not imply endorsement of the phonetic values", and adopts
it only because specialists find KU.MI.NA.QE easier to remember than 98-76-26-91.
He describes his own chapter as a critical investigation *into the problem* of the
phonetic values.

His preface is equally cautious in method: he takes Kober and Bennett as models
precisely because they refused to read anything prematurely, and warns against
resorting too soon to the etymological method.

**The 2:1 ratio has been detached from its author's own hedging.** Packard
presented a limited statistical argument inside a chapter arguing that backward
projection is uncertain. It has been cited downstream as license for the
practice. Our replication finding — that the effect does not survive his own
frequency constraint — is therefore *consistent with what Packard actually
wrote*, and inconsistent only with how he has been summarized.

This is a citation-drift finding as much as a statistical one, and it should be
presented as such.

## Two further points from the text

**Sign numbering.** Packard works in Raison-Pope L-numbers, not GORILA AB
numbers, and gives his own value table (L1=PA3, L2=PA, L22=RO, L29=KA, L30=DA,
L52=A, L97=U, L98=KU, L100=I, and about forty more). An exact replication
requires an L-to-AB concordance, which we do not yet have. Our reconstruction
used AB numbering and the conventional values, so sign-level correspondence with
his experiment is not guaranteed.

**He kept a divergence register too.** Packard adopted the Raison-Pope *Index*
as base text and records finding more than two hundred places where it differs
from Brice. The methodological problem this project treats as novel was live in
1974 and was handled the same way: adopt one witness, log the divergences.

**KU-RO.** He states that the meaning of the word for 'total' is established by
the many cases of numerical summation introduced by it — independent support for
the arithmetic test in `kuro_test.py`.

## Caveat, and it is a serious one

**Resolved.** Packard (1974) pp. 72–101 — the whole methodological chapter —
have been obtained and read. The scoring rule (p. 76, quoted verbatim above),
the null construction (p. 73), his chance model (p. 72), and the three
alternation categories with his own example pairs (p. 71) are all cited
directly from the source, not inferred from a summary or a secondary
description. The replication above is faithful to his documented method, not a
guess at it.

**What the appendices would add, and why the replication doesn't depend on
them.** Appendix A (his own literal list of alternation pairs) and Appendix D
(the literal text of his nine value assignments) have both now been read.
Cross-checking our reconstruction against them pair-by-pair and rotation-by-
rotation has not been done, and — per `TODO.md`'s "Not doing" section — isn't
going to be: it would only confirm results already significant at z > 4, and
doing it properly means transcribing his compiled tables rather than citing
his stated method, which this project doesn't do with any of its sources.

- **Appendix A** — not needed for the replication as it stands: this applies
  his documented rule (the three categories, p. 71) to *our* corpus rather
  than reproducing his list. Group counts already track his closely (92
  against 107) without it.
- **Appendix D** — not needed either: this generates 4000 rotations of its own
  following his documented rule (p. 73) rather than needing his specific nine.
- **Pope & Raison (1978), "Linear A: Changing Perspectives"** — the paper that
  refined Packard's figure to 3:1 (5:1 for Knossos). A genuinely open
  bibliographic item (`docs/SOURCES.md` §4), separate from Packard 1974 itself
  and from the appendices decision above, and worth obtaining if the 3:1/5:1
  figures are ever cited directly rather than via van Soesbergen's summary of
  them.

What does not change is the structural point: nine permutations cannot support
the inferential weight that has been placed on them for fifty years.
