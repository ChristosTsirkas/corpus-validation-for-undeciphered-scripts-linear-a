# DĀMOS (Database of Mycenaean at Oslo): methodology, license, and status

**This document was written by AI. The research described in it — checking
license terms, locating the citation requirement, evaluating what the
resulting word list does and doesn't contain, and identifying the further
source needed to isolate personal names — was likewise done by AI, not by a
human researcher. The reader should understand this before relying on
anything here.** This is the same standard of disclosure this project
applies everywhere else (see `AI_DISCLOSURE.md`), restated here because this
document covers a new source not discussed elsewhere. The Knossos word
search itself was run directly on the DĀMOS site and its result supplied for
this analysis; how that search was performed is described below.

## Why DĀMOS

The Packard name-parallel replication (`docs/PACKARD.md` §8.4,
`src/packard_names.py`) originally used a general Linear B lexicon, not
restricted to the Knossos-attested names Packard's own criterion required.
That looseness made the *ratio* reported valid but the absolute counts not
directly comparable to Packard's fifteen — a real gap, since resolved (see
"Current status" below). It required a Knossos-specific Linear B name
list. DĀMOS (Database of Mycenaean at Oslo) was identified as a candidate
source: a free, public, searchable, annotated corpus of all published
Mycenaean Linear B texts, explicitly covering the Knossos archive.

## What was actually done

A web search located DĀMOS (`https://damos.hf.uio.no/`) and confirmed its
scope and relevance. Direct page fetches were then attempted against the
site to check its license terms and, separately, to see whether its search
or browse functionality could be queried directly.

**The license and citation terms were successfully retrieved** from the
site's own footer, present on every page checked:

- **Content: CC BY-NC-SA 4.0** (Creative Commons Attribution-NonCommercial-
  ShareAlike 4.0 International) —
  https://creativecommons.org/licenses/by-nc-sa/4.0/
- **Software: GPL-3.0** — this governs DĀMOS's own application code, not its
  textual content, and is not directly relevant to reusing the corpus data.
- **Maintained by:** the DMLF unit at the University of Oslo's Faculty of
  Humanities; contact Federico Aurora, federico.aurora@ub.uio.no.
- **Required citation**, quoted verbatim from `https://damos.hf.uio.no/howto`:

  > Aurora, Federico. 2015. DAMOS (Database of Mycenaean at Oslo). Annotating
  > a fragmentarily attested language. In: Pedro A. Fuertes-Olivera et al.
  > (eds.), *Current Work in Corpus Linguistics: Working with
  > Traditionally-conceived Corpora and Beyond. Selected Papers from the 7th
  > International Conference on Corpus Linguistics (CILC2015)* (Procedia -
  > Social and Behavioral Sciences, 198), 21-31,
  > doi: 10.1016/j.sbspro.2015.07.415

**Direct page fetches could not drive the interactive search — this was a
real tooling limitation, not a licensing one.** Every page fetched from
`damos.hf.uio.no` — including `/howto`, `/about/content/`, and
`/about/texts/` — returned only the site's static navigation shell. The
document browser and word search are a dynamic, JavaScript-driven
application; a web search engine and a static page fetcher can't drive an
interactive filter-and-search interface or submit a query to it.

**The word list was subsequently obtained by search, run directly on the
DĀMOS site itself** (restricting to the Knossos site filter, then a Word
Search with the pattern left open rather than searching for the site code
literally — an earlier attempt to search for "KN" as if it were a word
failed for exactly that reason, since KN is a modern archive label applied
to documents, not a token any scribe wrote). The result was a full word-level
CSV export: 19,559 rows, 2,880 distinct lexical items after deduplication.

**That export's own `wordtype` field turned out not to distinguish personal
names from any other word.** Every actual word — name, place, common noun —
is tagged simply `"common word"` (6,825 of the 19,559 rows); the categories
DĀMOS actually distinguishes are token type (word vs. number vs. logogram vs.
divider), not grammatical category. Checking the highest-frequency "common
word" items confirmed this the hard way: the top entries are dominated by
well-attested place-names (`pa-i-to` = Phaistos, `ku-ta-to`, `da-wo`) and
grammatical particles (`jo`, `o`, `ja`), not personal names — exactly the
kind of thing an ad hoc frequency-based guess would get wrong.

**An authoritative, peer-reviewed onomasticon was identified as the correct
cross-reference for this** — rather than inventing a filter (e.g. "series A
tablets are personnel records, so guess from that") for something this
consequential to the replication. The cross-reference itself has not been
obtained in a form this project can use; see "Current status" below.

## Current status

- **License and citation for DĀMOS: established, documented, in use.**
- **DĀMOS Knossos word list: obtained and verified.** The export described
  below (19,559 rows, 2,880 distinct lexical items after deduplication) is
  now present in this project's working files (`data/damos_knossos_deduplicated.csv`,
  not redistributed — see `data/README.md` item 5b) and was independently
  re-counted rather than taken on trust: the same 2,880-row total, same
  intersection size.
- **Personal-name cross-reference: resolved, by reusing an existing project
  source rather than a new one.** Rather than classifying DĀMOS's own
  `wordtype` field (which, as found below, doesn't distinguish names from
  common words), the intersection runs the other way: the NeuroDecipher
  lexicon already in use for the unrestricted name-parallel test
  (`nd/data/linear_b-greek.names.cog`, `docs/SOURCES.md` §4b) already flags
  proper nouns. Intersecting its 429 names of three-plus signs against the
  DĀMOS Knossos word list by exact transliteration gives **154** words that
  are both classified as names and Knossos-attested — closing `TODO.md` §2.2.
  `src/packard_names.py.load_linear_b_knossos_names` implements this;
  `docs/PACKARD.md` reports the re-run figures.
- **Tselentis 2011** was not needed once the above worked, and remains
  unchecked for availability; no claim is made about it here. Tracked in
  `TODO.md`'s "Not doing" (not active work, but not forgotten either).
