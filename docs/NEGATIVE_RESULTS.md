# Stage 2d-e: Two Negative Results

Both computations returned negative. Both are worth having, and one of them
settles a question that would otherwise have absorbed a great deal of effort.

---

## 1. No alternation grid is recoverable

The Ventris method builds a syllabic grid from minimal pairs: attested types of
equal length differing in exactly one position. Each pair asserts that two signs
can occupy the same slot in the same environment. Enough of them constrain a
consonant-series by vowel-series lattice without any phonetic assumption.

**Raw counts looked encouraging:**

|                                       | administrative | religious |
|---------------------------------------|----------------|-----------|
| distinct types                        | 519            | 142       |
| minimal pairs                         | 609            | 46        |
| distinct substitutions                | 514            | 45        |
| substitutions attested more than once | 77             | 1         |

609 pairs is not a small number. But 514 distinct substitutions across 609 pairs
means almost every sign pair alternates exactly once, and the substitution graph
is a single near-complete component of 96 of the 98 signs involved. A real
paradigm looks like the opposite: a few sign pairs alternating repeatedly across
many environments, producing a sparse, structured graph.

**Null model.** Types were resampled preserving the length distribution and the
positional unigram distribution of signs, 300 trials.

| metric                          | observed | null mean | null sd | z         |
|---------------------------------|----------|-----------|---------|-----------|
| minimal pairs (admin)           | 609      | 683.7     | 45.8    | **-1.63** |
| substitutions repeated >1       | 77       | 90.0      | 15.7    | -0.83     |
| max repeats of one substitution | 4        | 4.4       | 0.8     | -0.51     |

p(null ≥ observed) = **0.94** administrative, **0.95** religious.

The corpus produces **fewer** minimal pairs than chance, not more. Every metric
sits below the null mean. There is no paradigmatic signal to extract.

**Conclusion: no alternation grid is recoverable from this corpus.** This is not
a limitation of method that a better algorithm would overcome; the information
is absent. With 519 short types over a ~98-sign inventory, apparent minimal
pairs are collisions.

This is the quantified form of the constraint we had already accepted. It is
worth stating precisely because it closes off the single most attractive line of
attack, and it does so on evidence rather than on resignation.

## 2. Reading disagreements do not cluster by scribal hand

Hypothesis: if contested readings concentrate in particular hands, the dispute is
partly palaeographic — that scribe's forms are genuinely hard to distinguish —
which would reframe adjudication.

**First run showed a strong effect.** HT Scribe 12: 10 divergences over 49 signs,
a rate of 0.204 against a baseline of 0.022, p = 9.8e-08, surviving
Benjamini-Hochberg correction across 22 hands. Nine times the expected rate.

**It was an artifact of our comparator.** HT Scribe 12 wrote HT 31 and HT 39,
both vessel-inventory tablets. Every divergence was vessel-logogram notation:
our source labels sign A402-VAS as `*815`, writes the VAS suffix as `-VS`, and
omits the `+` ligature marker that Younger uses. The underlying sign ids agreed
with Younger throughout. This is precisely the defect class the governing
principle exists to catch — the label is lossy, the sign id is not — and the
comparator was still reading labels because Younger publishes only labels.

After rendering vessel signs from the sign id and stripping ligature notation:

- HT Scribe 12 drops from 10 divergences to 2
- **no hand is significant after correction**
- sweep 1 agreement rises from 91.4% to **92.0%**, divergence sites 211 → 188
- D8 (the long tail) shrinks from 127 sites to 103

**Conclusion: no scribal clustering.** Disagreements are distributed across hands
at their expected rates.

**D4 specifically does not cluster.** Only 5 of its 18 sites carry an attribution,
and those 5 fall under 5 different scribes (HT 9, HT 10, HT 8, HT 21, KH 2). The
AB21/AB22 dispute is therefore not one scribe's idiosyncratic forms. It is a
general disagreement about the sign pair, and adjudicating it requires a single
decision about the AB21/AB22 distinction rather than per-scribe judgments. That
is a more tractable to-do than the alternative would have been.

---

## 3. Methodological note

This is the third time a comparator defect has masqueraded as a finding: the
scare-quoted `"fraction"` header in sweep 1, the malformed red-font nesting in
sweep 2, and now vessel notation here. In each case the first number out was
wrong in the direction of *more* apparent disagreement, and in this case it
produced a result that was statistically significant, mechanistically plausible,
and false.

The working rule that follows: **a positive result from the comparator is
provisional until the specific documents driving it have been inspected by
hand.** Significance testing does not protect against a systematic artifact,
because the artifact is systematic. Negative results are safer, which is part of
why the grid verdict above can be trusted more than the scribal one could have
been.
