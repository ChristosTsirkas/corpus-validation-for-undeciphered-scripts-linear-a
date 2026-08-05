# Stage 2g: Testing Phonological Inheritance

A third feasibility layer, restructured from "assume inheritance, correct for
drift" into "treat inheritance as falsifiable and test it".

---

## 1. Why the original framing had to change

The proposal was to assume phonological inheritance from Linear A to Linear B
for homomorphic signs, adjusted for roughly three centuries of drift, on the
grounds of documented population continuity and the absence of archaeological
evidence for invasion before the Mycenaeans.

Two problems.

**The genetic evidence does not support the premise as stated.** Lazaridis et al.
(*Nature* 548, 2017) found Minoans and Mycenaeans genetically similar, both
drawing at least three-quarters of their ancestry from the first Neolithic
farmers of western Anatolia and the Aegean. But the Mycenaeans differed from
Minoans in carrying additional ancestry ultimately related to Eastern European
and Siberian hunter-gatherers, arriving via a proximal source related to either
the Eurasian steppe or Armenia. The authors' own summary is *continuity but not
isolation*. There is therefore a documented component present in Mycenaeans and
absent in Minoans, and it is the component conventionally associated with
Indo-European arrival. The genetics argues against, not for, an unbroken
population premise.

**More fundamentally, genetic continuity cannot license phonological
inheritance.** Language replacement without genetic replacement is common
(Anatolia to Turkish, Egypt to Arabic). And the specific discontinuity here is
larger than drift: Linear B writes Greek, Linear A writes a language that is not
Greek. The script crossed a language boundary, and scripts adapted to a new
language routinely have their values reassigned to fit the new phonology - Latin
letters for Turkish or Vietnamese, or the Cherokee syllabary borrowing Latin
letterforms with unrelated values. The relevant model is cross-linguistic
borrowing, not three centuries of internal drift, and no degree of population
continuity constrains it.

The idea survives inversion. Rather than assuming the values, test whether they
carry recoverable phonological information.

## 2. How secure are the inherited values in the first place

| category                                      | sign tokens | share |
|-----------------------------------------------|-------------|-------|
| value **certain** (Younger's 12)              | 961         | 21.2% |
| value **possible** (his 4)                    | 329         | 7.3%  |
| AB-series, value **assumed** by shape analogy | 2356        | 52.0% |
| A-only signs, no value at all                 | 888         | 19.6% |

Only about a fifth of the corpus carries a value the standard reference calls
certain. The system the hypothesis rests on is itself largely unverified, which
is why the test below is run separately at each confidence level.

## 3. The test

If inherited values carry real Minoan phonology, applying them should expose
dependence between the vowels of consecutive signs within a word - harmony, or
any sequencing constraint. Permuting the sign-to-value assignment destroys real
signal while preserving every marginal frequency.

Vowels rather than full CV values, because 5 vowels give a 25-cell table that
this corpus can actually fill, unlike the 272-sign bigram table shown to be
inestimable in ENTROPY.md.

| level    | signs | covered words | vowel bigrams | per cell | observed MI | null            | z     | p            |
|----------|-------|---------------|---------------|----------|-------------|-----------------|-------|--------------|
| certain  | 12    | 42            | 62            | 2.5      | —           | —               | —     | underpowered |
| possible | 16    | 80            | 126           | 5.0      | 0.2322      | 0.2144 ± 0.0637 | +0.28 | 0.37         |
| assumed  | 51    | 618           | 1217          | 48.7     | 0.0417      | 0.0288 ± 0.0097 | +1.33 | 0.10         |

**No detectable signal at any level.** The assumed-value level shows a weak
positive trend, but z = +1.33 on a single test is not evidence and should not be
reported as suggestive.

## 4. What the null actually excludes

"No signal" is uninformative without knowing what could have been detected.
Synthetic vowel harmony of known strength was injected into words of the observed
shape and length distribution, at the assumed-value level (n = 1217 bigrams):

| harmony strength | detection rate |
|------------------|----------------|
| 0.05             | 50%            |
| 0.10             | **100%**       |
| 0.15             | 100%           |
| 0.30             | 100%           |

The test detects harmony of strength 0.10 or above every time. Observed data
shows none.

**Conclusion: strong vowel harmony is excluded.** If the inherited values are
approximately right, the language behind Linear A did not have Turkic- or
Uralic-style vowel harmony. Weak constraints below about 0.05 remain untestable
at this corpus size.

**Do not overread this.** Vowel harmony characterizes Turkic and Uralic
languages, but many agglutinative languages lack it entirely - Japanese, Swahili,
Quechua and Georgian among them. Excluding harmony therefore excludes a specific
areal-typological feature, **not** agglutination as a morphological type. The
standard agglutination reading of Linear A is untouched by this result in either
direction.

What the result does exclude is a Turkic/Uralic-type profile specifically, which
is a narrower claim than it may first appear.

## 4b. Re-specification for a three-vowel Minoan

Salgarella (*OCD* 2022), following Palaima & Sikkenga (1999), reports the
standard view that Minoan may have had a **three-vowel system /a i u/**, since in
Linear B most signs carrying /o/ and one carrying /e/ are Greek innovations
rather than inherited from Linear A.

The test above was specified over a five-vowel inventory and is therefore
mis-specified on that view: the e- and o-series would be Greek additions, and
treating them as inherited injects noise into both statistic and null. The test
was re-run with vowels collapsed e→i, o→u.

| level    | inventory | bigrams | per cell | observed MI | null            | z         | p    |
|----------|-----------|---------|----------|-------------|-----------------|-----------|------|
| possible | 5         | 126     | 5.0      | 0.2322      | 0.2156 ± 0.0654 | +0.25     | 0.38 |
| possible | **3**     | 126     | 14.0     | 0.0626      | 0.0697 ± 0.0426 | **−0.17** | 0.50 |
| assumed  | 5         | 1217    | 48.7     | 0.0417      | 0.0290 ± 0.0097 | +1.31     | 0.10 |
| assumed  | **3**     | 1217    | 135.2    | 0.0058      | 0.0075 ± 0.0052 | **−0.34** | 0.56 |

The three-vowel specification has far better sampling — 135 observations per
cell against 49 — and the weak positive trend seen at five vowels **disappears
entirely**, going slightly negative.

Two readings, and the data does not choose between them. Either the trend at
five vowels was noise, which the better-sampled test now shows more clearly; or
the collapse is wrong and destroyed a real distinction. Since the trend was never
significant, the first is the more economical reading.

Either way the conclusion is unchanged and now rests on a better-specified test:
no phonological signal is recoverable, under either vowel inventory.

## 4c. Reconciliation with the name-parallel result

PACKARD.md now reports a **positive** result: Linear A words transcribed with
inherited values match Knossos-attested Linear B names at 4.74 times the rate
of permuted assignments (z = +4.34, p = 0.0020). The inherited values
demonstrably carry real information.

That does **not** contradict the null found here, because the two tests ask
different questions. The name-parallel test asks whether the values are
approximately correct. The vowel-dependency test asks whether the language
behind Linear A had vowel harmony. A language can have correct transcriptions
and no harmony.

But it does require softening how this section is read. "No phonological signal"
must not be taken to mean "the values are uninformative" — they are informative,
demonstrably so. What is absent is *vowel-sequencing structure*, under either a
five- or three-vowel inventory, at the sensitivity established by the power
calibration below.

The conjunction problem in section 5 is correspondingly relaxed: since the
values are now independently shown to carry signal, the more economical reading
of our null is that **Minoan did not have strong vowel harmony**, rather than
that the values are wrong.

## 5. The limitation that must accompany the result

This is a **conjunction test**. The null is:

> the values are uninformative **OR** there is no vowel dependency

Failure to reject cannot separate these. A negative is equally consistent with
(a) Minoan having no vowel harmony, (b) the Linear B values not being inherited,
or (c) both. The result therefore constrains the pair jointly and cannot be
quoted as a fact about Minoan phonology alone.

That ambiguity is not a flaw in the design; it is intrinsic to testing an
unverified value system against an unknown language, and any method claiming to
separate the two without external evidence is overreaching.

## 6. Status

The third feasibility layer is complete and returns, like the other two, a
bounded negative. The three together now delimit what this corpus supports:

- no alternation grid recoverable (below chance)
- conditional entropy not estimable (short by two orders of magnitude)
- no phonological signal in the inherited values; strong vowel harmony excluded
