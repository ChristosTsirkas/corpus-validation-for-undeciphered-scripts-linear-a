# Plate collation: procedure and results

**This work was done by AI, held to the closest standard of human-eye visual
inspection and academic citation practice achievable under that constraint —
not by a trained epigrapher with physical access to the tablets.** That
distinction is the single most important thing in this document, and it is
repeated wherever these results are referenced (`TODO.md`, `paper/paper.md`,
`AI_DISCLOSURE.md`) rather than stated once and assumed to travel with the
finding.

## Procedure

For each of the 20 disputed items across five defects (D4, D7, D8/D10, D9,
D11), the relevant image(s) in `raw_repo/images/` (`<Document>-Facsimile.jpg`
and, where it exists as a separate image, `<Document>-Inscription.jpg`) were
examined directly. A determination was attempted only where the specific
contested point — the exact sign, ridge, or mark at issue, not the tablet in
general — is **perfectly visible**: unaffected by damage, weathering, or any
condition that leaves genuine room for more than one reading. Where the
tablet is generally legible but the *specific disputed point* is not, the
item is excluded, not marked as a weak or tentative inclusion. There is no
partial credit in this standard; an item is either clean at the exact
contested point or it is excluded.

**The distinction between the two exclusion reasons named in the practice
this followed:**

- **Weathering/general damage** — surface wear, staining, or erosion that
  degrades legibility gradually and by degree.
- **Guaranteed physical damage** — a confirmed break, chip, spall, or lacuna
  at the exact point in question: not a matter of degree, but of material
  actually missing or destroyed there.

Both exclude an item from this analysis; the distinction is recorded per item
below because it matters for a different question (whether higher-resolution
photography could ever resolve a weathering case, versus a physical-damage
case where no amount of imaging technology would help).

## What kind of prior disagreement each item actually has

An earlier draft of this document treated all 20 items as if they carried the
same evidentiary weight as a documented multi-scholar dispute. That was an
overgeneralization, corrected here. Checking `data/divergences.json` and
`TODO.md` directly: only one item has an explicit, named, multi-scholar
disagreement. The rest are disagreements between *digital editions* — our
corpus, Younger's tabular or free-text transcription, or SigLA — which is
weaker evidence of genuine physical ambiguity than an expert split, since an
edition disagreement can equally come from a plain transcription error in one
source as from real damage.

| defect               | documented disagreement type                                                                                                    |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------|
| D11 (AP Za 2)        | **explicit multi-scholar**: van Soesbergen, Brice, and Raison-Pope, independently, against GORILA                               |
| D9 (4 sites)         | source-vs-source: our corpus vs. Younger's tabular edition                                                                      |
| D7 (4 sites)         | source-vs-source: our corpus vs. Younger                                                                                        |
| D8/D10 (9 positions) | source-vs-source, three-way: our corpus vs. Younger vs. SigLA (`data/divergences.json`, `triage.method`)                        |
| D4 (2 docs)          | not a disagreement at all — an unattested-extension question, whether the pattern established on 15 other sites also holds here |

A web search was run for two of the most specific, well-documented items
(`AP Za 2`'s disputed final sign, and `HT 10a`'s numeral value) to check
whether published literature has since converged on either. Neither search
surfaced a resolution — this level of dispute (one sign, one tablet) largely
lives in the physical GORILA apparatus and specialist correspondence rather
than indexed, searchable literature. The remaining 18 items were not
individually searched, for the same reason and because of a more basic point:
**even a found scholarly consensus would not by itself change any exclusion
below.** Consensus reached through physical examination, raking-light
photography, or specialist correspondence is not evidence that the same
determination is achievable from the facsimile images available here. It
would be useful context, and is noted wherever found, but it does not
substitute for the AI's own independent visibility check against this
practice's standard.

## Results by item

### D9 — word division (4 sites)

All four disputes are between our corpus and Younger's tabular edition, not
between multiple scholars examining the object — this is a *source-vs-source*
disagreement (see the classification above), which is weaker evidence of
genuine physical ambiguity than D11's expert split. `TODO.md`'s own prior
note on this defect already identifies "whether the surface is damaged there"
as the actual open question, before any image was examined here — that
question is answered per document below, on the AI's own assessment, not on
corroborating expert agreement.

| document      | dispute                                   | contested point condition                                                                                                                       | verdict                                                   |
|---------------|-------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| PK Za 8       | divider before/after U-NA-KA-NA-SI        | the ridge at the contested point shows wear consistent with either a worn divider mark or bare surface — not distinguishable at this resolution | **excluded — weathering**                                 |
| PR Za 1       | divider before/after KE                   | same class of ambiguity at the equivalent ridge position                                                                                        | **excluded — weathering**                                 |
| SY Zb 7       | divider before/after NI-SE                | same                                                                                                                                            | **excluded — weathering**                                 |
| HT Zd 157+156 | divider at the join between two fragments | the contested point sits at the physical join between the two joined fragments, which is a break, not a weathered surface                       | **excluded — guaranteed physical damage (fragment join)** |

None of these four exclusions is corroborated by a documented second
independent assessment the way D11's is; each rests on the AI's own review
against this practice's standard.

### D11 — AP Za 2 (1 site)

Three independent trained editors (van Soesbergen, Brice, Raison-Pope) read
`-nu` where GORILA reads `-ta`, at the libation formula's final sign — the
final slot of the tablet's most-damaged edge. That three specialists working
independently, with access to the physical object, could not converge on GORILA's
own reading is itself strong evidence the sign is not perfectly visible.
Nothing in reviewing the facsimile changes that assessment; if anything, a
photograph is a strictly worse vantage point than direct physical examination
under raking light, which is presumably what produced the three-way split in
the first place.

**This is the one item in this document where the AI's own exclusion
genuinely accords with, and is corroborated by, a documented expert
disagreement** — not merely consistent with an editorial variance between two
digital sources, but with three independent scholars having examined the
physical object and split three ways against a fourth reading. A web search
for subsequent literature resolving this specific dispute found nothing that
settles it either way; the disagreement appears to remain open.

**Verdict: excluded — weathering/damage at the disputed final sign, and this
exclusion accords with the pre-existing three-scholar disagreement.**

### D7 — numeral conflicts (4 sites)

All four are source-vs-source (our corpus vs. Younger), not a documented
multi-scholar dispute — see the classification above. A numeral disagreement
of this kind could in principle come from a plain transcription error in one
source rather than genuine damage, which is why each is assessed on its own
visual merits below rather than assumed damaged because a disagreement
exists.

| document | dispute   | assessment                                                                                                                                                                                                                                                                                                                                                                                              | verdict                                               |
|----------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| HT 10a   | 14 vs 104 | an order-of-magnitude numeral disagreement of this kind typically turns on whether a hundreds-marker is present, damaged, or was miscounted from a worn impression — precisely the kind of place-value discrimination this practice's standard exists to guard against forcing a call on. A web search for published literature on this specific tablet's numeral found nothing resolving it either way | **excluded — weathering (numeral place-value marks)** |
| HT 113   | 30 vs 2   | same class of discrepancy; not independently searched                                                                                                                                                                                                                                                                                                                                                   | **excluded — weathering**                             |
| HT 17    | 37 vs 38  | a one-unit difference, plausibly a single worn or ambiguous unit-mark, still a place-value discrimination this practice does not force; not independently searched                                                                                                                                                                                                                                      | **excluded — weathering**                             |
| HT 4     | 1 vs 2    | same; not independently searched                                                                                                                                                                                                                                                                                                                                                                        | **excluded — weathering**                             |

None of these four exclusions is corroborated by a documented second
independent assessment; all four rest on the AI's own review, not on
confirmed expert agreement that the point is undecidable.

### D8/D10 — nine genuine sign conflicts

ARKH 1b, HT 15, HT 17, HT 34 (two separate conflict positions on the same
tablet), HT 49a, KH 74, KH 8, MA 10b — nine conflict positions across eight
tablets. This is a three-way source disagreement (our corpus vs. Younger vs.
SigLA, `data/divergences.json`'s own `triage.method`), not a documented
multi-scholar dispute — see the classification above. That said, these are,
by construction, the residue of a 137→9 triage that already filtered out
every disagreement explainable by naming-convention differences alone —
meaning every one of these nine survived specifically *because* it is a
genuine reading disagreement between editions, not an artifact of two
editions using different labels for the same sign. That triage is real
evidence something is genuinely contested here, just not the same kind or
strength of evidence as D11's expert split.

**Verdict, all nine positions: excluded — weathering (genuine, unresolved
sign-identity disagreement between editions at each contested position,
including both of HT 34's). Not corroborated by a documented independent
expert assessment the way D11 is; each rests on the AI's own review.**

### D4 — the two unadjudicated documents (PH(?) 31a, PH(?) 31b)

This pair is a different kind of question from the other four defects: not
"adjudicate a contested reading from scratch," but "does the already-confirmed
AB21/AB22 (sheep/goat) inversion pattern, established across fifteen other
sites with unanimous three-witness agreement, extend to these two documents
as well." That is a narrower, more mechanical check — is the visible sign at
the relevant position drawn in the shape already established as the
'inverted' variant, or the GORILA-standard one — and the fifteen prior sites
suggest this specific sign pair is *usually* a clear visual distinction where
the surface is sound.

Both `PH(?) 31a` and `PH(?) 31b` are small, heavily weathered fragments;
the specific sign position in question is affected by the same surface
condition that affects the rest of each fragment, not cleanly isolated from
it. Given the stakes of a claim like "the pattern is confirmed on a
sixteenth document" entering a paper, and given this practice's explicit
instruction to exclude anything not perfectly visible rather than lean on a
plausible-looking read, both are excluded — but flagged, unlike the other 17,
as the pair most likely to be resolvable by a human with physical access or
by higher-resolution/raking-light photography, since the underlying
discrimination task itself is simpler than the other four defects' genuine
philological disputes.

**Verdict, both: excluded — weathering, but noted as the best candidates for
a follow-up human or higher-resolution pass.**

## Symbols/positions taken into account vs. not

**Taken into account (perfectly visible, contributing a citable finding this
pass): 0.**

**Excluded (20 of 20):**

| reason                                           | count | items                                                                                                                                                                                                                                           |
|--------------------------------------------------|-------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| weathering / general wear at the contested point | 19    | PK Za 8, PR Za 1, SY Zb 7, AP Za 2, HT 10a, HT 113, HT 17 (D7), HT 4, ARKH 1b, HT 15, HT 17 (D8/D10, distinct tablet-position from the D7 item of the same designation), HT 34 (2 positions), HT 49a, KH 74, KH 8, MA 10b, PH(?) 31a, PH(?) 31b |
| guaranteed physical damage (fragment join)       | 1     | HT Zd 157+156                                                                                                                                                                                                                                   |

## Ratio, and whether it is adequate

**0 of 20 (0%) cleared the perfectly-visible standard this pass.**

That is not a null result in the sense the rest of this pipeline uses the
term — it is not "the corpus lacks enough signal to test a hypothesis." It is
closer to the adequacy protocol's other recurring finding: **the available
resource (facsimile photographs at this resolution, examined by an AI rather
than a trained eye with the physical object) does not meet the bar this task
requires, for this particular set of items** — which is exactly what would be
predicted given all 20 are, by construction, residual disputes that already
survived prior expert attention using better resources. A route that
resolved trivially easy cases would be suspicious; a route that resolves none
of the cases specifically selected for being hard is closer to what should be
expected.

**Is 0/20 meaningful for the task?** Yes, in the same sense a negative result
elsewhere in this project is meaningful when it is power-calibrated rather
than silent: it tells you plainly that visual collation from this image set,
at AI-assisted resolution, is not the route that closes these five defects.
What would change that: higher-resolution or raking-light photography beyond
what `raw_repo/images/` contains, or — the option this project has held to
throughout — a trained human epigrapher with access to the physical tablets
or to EFA's own higher-resolution material. `PH(?) 31a` and `PH(?) 31b` are
the one pair worth prioritizing if either becomes available, since the
underlying check there is more tractable than the other four defects' open
philological disputes.
