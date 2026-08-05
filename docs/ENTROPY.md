# Stage 2f: Entropy

One usable result, one formal impossibility, and one comparison that had to be
redone before it meant anything.

---

## 1. Unigram entropy H1

Computed over complete signgroup tokens, sign ids only.

| corpus         | n tokens | k signs | H1 (MLE) | Miller-Madow | Chao-Shen | max (log₂k) |
|----------------|----------|---------|----------|--------------|-----------|-------------|
| whole          | 4534     | 272     | 6.281    | 6.326        | 6.374     | 8.087       |
| administrative | 3813     | 262     | 6.272    | 6.324        | 6.375     | 8.033       |
| religious      | 721      | 93      | 5.614    | 5.706        | 5.732     | 6.539       |

Bootstrap 95% interval on the whole-corpus MLE: 6.179 – 6.291. The three
estimators agree to within about 0.1 bits, so the figure is stable.

Note that k = 272 counts every distinct sign id including logograms, ligatures
and composites, not the ~90 syllabograms in regular use. H1 is therefore a
property of the *script as deployed in these documents*, not of the syllabary.

**Do not compare these numbers to published entropy figures for known scripts.**
Entropy estimates are biased by sample size, and published values come from
corpora orders of magnitude larger. A valid comparison requires subsampling the
reference corpus to our n. That has not been done here and the naive comparison
is invalid.

## 2. Conditional entropy H2 is not estimable

H2, the entropy of a sign given its predecessor, is the measure that actually
discriminates script types. It cannot be computed from this corpus, and the
reason is arithmetic rather than methodological.

| corpus         | bigram tokens | distinct observed | possible (k²) | coverage |
|----------------|---------------|-------------------|---------------|----------|
| whole          | 1875          | 929               | 73984         | **1.3%** |
| administrative | 1386          | 729               | 68644         | 1.1%     |
| religious      | 489           | 312               | 8649          | 3.6%     |

There are 0.025 tokens per cell of the bigram table. 63% of the bigrams that do
occur are seen exactly once. A rule of thumb of five observations per cell would
require roughly 370,000 within-word bigram tokens; we have 1875, short by more
than two orders of magnitude.

**Any H2 figure computed from this corpus would measure the sampling, not the
script.** This is the same class of result as the alternation grid: not a
limitation that a better estimator overcomes, but information that is absent.

Together the two findings close off both standard routes to a script-typology
fingerprint. That is worth stating plainly in the paper, because both are
routinely attempted on Linear A and the adequacy check is rarely shown.

## 3. The registers differ in entropy, tested properly

The naive comparison — religious 5.61 against administrative 6.27 — is invalid
for exactly the reason given above: different n, different k. The correct test
subsamples the administrative corpus to the religious n and compares against
that distribution.

|                                    | value              |
|------------------------------------|--------------------|
| religious H1 (Chao-Shen), n=721    | 5.732 bits         |
| administrative subsampled to n=721 | 6.275 ± 0.070 bits |
| z                                  | **−7.76**          |
| p(admin ≤ religious)               | 0.000 / 400 trials |

**The religious corpus is genuinely lower-entropy**, by about 0.54 bits, and the
effect survives matched-n testing comfortably. It is not a sample-size artifact.

This is independent confirmation of the formulaic structure found in FORMULA.md:
a corpus built around a fixed formula with a small set of recurring slots should
carry less per-sign information than open-ended accounting records, and it does.
The two results were derived by unrelated methods.

It also sharpens the length finding in STRUCTURE.md. The religious register has
*longer* words but *less* information per sign, which is what repetition of a
fixed formula predicts and what a register of genuinely richer vocabulary would
not.

---

## 4. Standing caveats

- H1 depends on the sign inventory chosen. Ours includes logograms and
  ligatures; a syllabogram-only H1 would differ and is not reported here.
- The register comparison holds n constant but not k (93 against 262). Chao-Shen
  is coverage-adjusted, which mitigates this, but does not eliminate it.
- Everything above uses complete tokens only. Including damaged tokens would
  raise n at the cost of introducing fragments as if they were words.
