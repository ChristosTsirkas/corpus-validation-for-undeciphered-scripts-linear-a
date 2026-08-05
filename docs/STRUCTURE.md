# Stage 2: Structural Findings

Status: first pass complete. Genre tagging, length distribution, positional
profile, affixation measure.

**Method constraint.** Every computation below was run on GORILA sign ids only.
No phonetic value, Linear B reading or language hypothesis entered any
calculation. Provisional Linear B values appear in this document *after* the
fact, in brackets, purely so the results are readable. They are not inputs and
must not be treated as findings.

**Data filter.** Only `signgroup` tokens, only `complete == True` (undamaged),
only multi-sign groups for positional and affix work. A fragment's first sign is
not evidence of word-initial position, and a single-sign token is trivially both
initial and final.

---

## 1. Genre tagging

Mechanical, from physical support. No interpretation.

| Genre                                                       | Records | Complete multi-sign groups |
|-------------------------------------------------------------|---------|----------------------------|
| administrative (tablets, nodules, roundels, sealings, bars) | 1517    | 767                        |
| religious (stone/clay/metal vessels, objects, architecture) | 204     | 160                        |

Nothing fell to `unclassified`.

## 2. The two registers are structurally distinct

|                        | administrative | religious |
|------------------------|----------------|-----------|
| mean sign-group length | 2.81           | 4.06      |
| n                      | 767            | 160       |

Mann-Whitney U = 36325, p = 6.2e-18 — but that test treats every word as an
independent observation, and words inside one document share a scribe, a
document type and a subject. It is pseudo-replicated and its p-value is not
usable.

**Re-tested by permuting genre labels across records** (259 administrative, 99
religious; 5000 trials), which is the correct unit:

|                                 | value          |
|---------------------------------|----------------|
| observed mean-length difference | +1.249 signs   |
| record-permuted null            | −0.001 ± 0.122 |
| **z**                           | **+10.21**     |

The finding survives at full strength. The difference is not marginal and not an
artifact of sample size or of pseudo-replication. Length 6+
groups are 25 of 160 in the religious corpus against 7 of 767 in the
administrative. This vindicates the decision to split genres before analysis:
pooling them would have produced a meaningless average over two different things.

The cause is open. Longer religious words are consistent with (a) genuinely
longer lexemes in that register, (b) affixation or compounding in formulaic
language, or (c) heavy abbreviation and personal-name shortening in the accounts.
The current data does not separate these.

## 3. Positional preference: about half the claims survive correction

The original table used per-sign binomial tests against an analytic null, with no
multiple-comparison correction across the ~20 signs examined. Re-run with a
within-word permutation null (sign order shuffled inside each word, preserving
word lengths and each word's sign multiset) and Benjamini-Hochberg correction
across every sign with n ≥ 15:

| register       | signs tested | surviving BH |
|----------------|--------------|--------------|
| administrative | 42           | **24**       |
| religious      | 14           | **3**        |

The strongest administrative effects survive comfortably — AB008 and AB081 and
AB031 and AB001 initial, AB002 and AB027 and AB006 and AB076 and AB024 final —
with observed edge counts far from their permuted expectations (AB002: 64 final
against 32.0 expected; AB008: 71 initial against 24.4).

Roughly half the table does not survive. Signs such as AB077, AB080, AB059,
AB053 and AB007 showed apparent bias under the uncorrected test and do not
exceed permutation once correction is applied. Those should not be cited.

In the religious corpus only 3 of 14 survive (AB004 final, AB057 and AB008
initial), which is what the smaller sample predicts. Note that A301, reported
earlier as striking because all 15 occurrences are medial, does **not** survive:
with words of that length a medial-only distribution is unremarkable under
permutation.

**Caveat that limits the strongest result.** AB008 is the pure-vowel sign. In a
CV syllabary, vowel-only signs cluster word-initially for phonotactic reasons,
because a V syllable is often only licensed in onset position. Its skew is
therefore probably orthographic-phonotactic, **not** morphological, and it should
not be counted as affix evidence. The interesting cases are the CV signs with
strong final bias — AB002, AB027, AB006, AB024, AB076 — whose concentration at
the right edge is not explained by syllabary mechanics.

A301 in the religious corpus is worth noting separately: 15 occurrences, **all
medial**, none initial or final. Consistent with a sign locked inside a fixed
formulaic stem (it is the *301 of A-TA-I-*301-WA-JA).

## 4. Affixation: our measurement does not reproduce the received figure

Definition, chosen to be conservative and reproducible: type B is affixed if B
equals an independently attested type A plus 1-2 signs at one edge. The stem must
itself be attested as a complete word.

|                             | administrative | religious    |
|-----------------------------|----------------|--------------|
| distinct types              | 519            | 142          |
| types with an attested stem | 75 (14.5%)     | 18 (12.7%)   |
| affix relations             | 80             | 21           |
| **prefix**                  | 34 (**42%**)   | 8 (**38%**)  |
| **suffix**                  | 46 (**58%**)   | 13 (**62%**) |

### Null model: affixation is real, its direction is not

The measure was tested against resampled types preserving length distribution
and positional sign frequencies (300 trials).

|                               | observed | null mean | sd    | z         |
|-------------------------------|----------|-----------|-------|-----------|
| **admin** total relations     | 80       | 37.2      | 7.2   | **+5.91** |
| admin prefix relations        | 34       | 15.1      | 4.4   | +4.31     |
| admin suffix relations        | 46       | 22.1      | 5.3   | +4.51     |
| admin **prefix share**        | 0.425    | 0.405     | 0.086 | **+0.23** |
| **religious** total relations | 21       | 4.4       | 2.5   | **+6.74** |
| religious **prefix share**    | 0.381    | 0.302     | 0.268 | **+0.29** |

p(null ≥ observed total) = 0.003 in both registers.

**Affixation is a genuine structural property.** Affix relations exceed chance by
roughly six standard deviations in both registers, and both prefix and suffix
relations do so independently. This is the first positive structural finding in
the project: unlike minimal pairs, which fell *below* chance, this signal is real.

**The prefix/suffix ratio is not.** Observed prefix share sits within a quarter
of a standard deviation of the null in both registers. The chance baseline for
prefix share is itself about 0.40, given the positional distribution of signs.
Our 42% is therefore exactly what randomness produces and carries no information
about the language.

### Consequence: our figure cannot challenge Duhoux

The received figure (Duhoux 1978, via Schoep 2002) is **59% prefixal**, contrasted
with 12% in Linear B and read as evidence for agglutination.

Our earlier reading of this - that the corpus is suffix-dominant and therefore
does not reproduce Duhoux - **does not survive the null model**. A ratio at chance
level cannot contradict anything. It is not evidence for suffix dominance; it is
absence of directional evidence.

Note also that a chance baseline near 0.40 means Duhoux's 59%, if measured this
way, would sit *above* chance. Our result therefore neither confirms nor refutes
his figure. It establishes only that our own method has no directional power at
this corpus size.

### Consequence for the language-family question

An earlier version of this document treated the prefix/suffix direction as
bearing on the Indo-European reading, since IE morphology is overwhelmingly
suffixing. That inference is withdrawn in both directions. We have no directional
evidence, so nothing here speaks for or against any language family. What we do
have is that affixation itself is real, which is compatible with essentially every
candidate and discriminates between none of them.

---

## 5. What this stage does not yet do

- No entropy or conditional-entropy measures.
- No alternation grid: the Ventris move proper is finding signs that substitute
  for one another in the same slot across otherwise identical contexts. That is
  the next computation, and it is where a syllabic grid would come from, if one is
  recoverable at this corpus size.
- No sequence alignment of the libation formula (blocked on D9).
- Sample sizes are small enough that any finding resting on fewer than roughly
  15 attestations should be treated as a hypothesis, not a result.
