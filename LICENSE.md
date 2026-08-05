# License and attribution

This repository mixes original code under a source-available, noncompete
license with third-party data under more restrictive terms. **The parts are
not interchangeable.**

## The paper (`paper/`) — CC BY 4.0

The paper is a scholarly work consisting of original analysis, methodology and
commentary.

**Original content** — text, analysis, figures, tables, conclusions — is
© 2026 Chris Tsirkas and licensed under **CC BY 4.0** (Creative Commons
Attribution 4.0 International). You are free to share and adapt it, including
commercially, provided you give appropriate credit, link to the license, and
indicate whether changes were made.

CC BY rather than MIT because MIT is a software license and the paper is not
software. CC BY is the standard for academic work and is what humanities readers
will expect.

**Third-party material quoted in the paper is not covered by this license** and
remains subject to the terms of its sources:

- **Sign transcriptions and readings** — GORILA (Godart & Olivier 1976–1985) and
  SigLA (Salgarella & Castellan, CC BY-NC-SA 4.0). The libation formula in §5.6,
  the KU-RO and KI-RO sign groups in §5.7, and every sign sequence quoted
  elsewhere are transcriptions from these editions, not this project's readings.
- **Phonetic values** — Packard (1974) and the wider Linear B tradition.
- **Fraction values** — Corazza et al. (2021), CC BY-NC-ND.

These are quoted for scholarly purposes and remain the property of their
respective rightsholders. Their appearance here transfers no license; reuse is
subject to the original terms. **What is licensed is the analysis; the data is
not this project's to license.**

## Original code — PolyForm Shield 1.0.0, plus unrestricted academic use

Everything in `src/`, `tests/`, and the analysis documents in `docs/` are
original work by Chris Tsirkas. Anyone may use, copy, modify, merge, publish,
and distribute this code, including commercially — the one thing restricted
is using it (or a modified version) to provide a product or service that
competes with what the licensor or its affiliates offers using it. Full terms
below; this is the standard, unmodified **PolyForm Shield License 1.0.0**,
with one additional grant appended afterward rather than edited into it, so
that "PolyForm Shield" still means what it's supposed to mean.

### Dual use of the decoder

`src/ocaml_marshal.py` is a general implementation of the OCaml `Marshal`
binary format and **can decode any OCaml `Marshal` stream**. It is licensed
under the same terms as the rest of `src/`, without further restriction.

The CC BY-NC-SA restriction described below applies to its *output* only when
that output is derived from SigLA data. Running the decoder on your own
OCaml data produces data you own; running it on SigLA's produces a
derivative of SigLA.

```
# PolyForm Shield License 1.0.0
<https://polyformproject.org/licenses/shield/1.0.0>

Required Notice: Copyright Chris Tsirkas (https://github.com/ChristosTsirkas/corpus-validation-for-undeciphered-scripts-linear-a)

## Acceptance

In order to get any license under these terms, you must agree to them as
both strict obligations and conditions to all your licenses.

## Copyright License

The licensor grants you a copyright license for the software to do
everything you might do with the software that would otherwise infringe the
licensor's copyright in it for any permitted purpose. However, you may only
distribute the software according to Distribution License and make changes
or new works based on the software according to Changes and New Works
License.

## Distribution License

The licensor grants you an additional copyright license to distribute copies
of the software. Your license to distribute covers distributing the software
with changes and new works permitted by Changes and New Works License.

## Notices

You must ensure that anyone who gets a copy of any part of the software from
you also gets a copy of these terms or the URL for them above, as well as
copies of any plain-text lines beginning with `Required Notice:` that the
licensor provided with the software, including the one above.

## Changes and New Works License

The licensor grants you an additional copyright license to make changes and
new works based on the software for any permitted purpose.

## Patent License

The licensor grants you a patent license for the software that covers patent
claims the licensor can license, or becomes able to license, that you would
infringe by using the software.

## Noncompete

Any purpose is a permitted purpose, except for providing any product that
competes with the software or any product the licensor or any of its
affiliates provides using the software.

## Competition

Goods and services compete even when they provide functionality through
different kinds of interfaces or for different technical platforms.
Applications can compete with services, libraries with plugins, frameworks
with development tools, and so on, even if they're written in different
programming languages or for different computer architectures. Goods and
services compete even when provided free of charge. If you market a product
as a practical substitute for the software or another product, it definitely
competes.

## New Products

If you are using the software to provide a product that does not compete,
but the licensor or any of its affiliates brings your product into
competition by providing a new version of the software or another product
using the software, you may continue using versions of the software
available under these terms beforehand to provide your competing product,
but not any later versions.

## Discontinued Products

You may begin using the software to compete with a product or service that
the licensor or any of its affiliates has stopped providing, unless the
licensor includes a plain-text line beginning with `Licensor Line of
Business:` with the software that mentions that line of business.

[Licensor Line of Business: fill in once a named product/service exists —
this line, if present, keeps the Noncompete term in force for that specific
line of business even after you stop offering it yourself.]

## Sales of Business

If the licensor or any of its affiliates sells a line of business developing
the software or using the software to provide a product, the buyer can also
enforce Noncompete for that product.

## Fair Use

You may have "fair use" rights for the software under the law. These terms
do not limit them.

## No Other Rights

These terms do not allow you to sublicense or transfer any of your licenses
to anyone else, or prevent the licensor from granting licenses to anyone
else. These terms do not imply any other licenses.

## Patent Defense

If you make any written claim that the software infringes or contributes to
infringement of any patent, your patent license for the software granted
under these terms ends immediately. If your company makes such a claim, your
patent license ends immediately for work on behalf of your company.

## Violations

The first time you are notified in writing that you have violated any of
these terms, or done anything with the software not covered by your
licenses, your licenses can nonetheless continue if you come into full
compliance with these terms, and take practical steps to correct past
violations, within 32 days of receiving notice. Otherwise, all your licenses
end immediately.

## No Liability

As far as the law allows, the software comes as is, without any warranty or
condition, and the licensor will not be liable to you for any damages
arising out of these terms or the use or nature of the software, under any
kind of legal claim.

## Definitions

The **licensor** is the individual or entity offering these terms, and the
**software** is the software the licensor makes available under these
terms. A **product** can be a good or service, or a combination of them.
**You** refers to the individual or entity agreeing to these terms. **Your
company** is any legal entity, sole proprietorship, or other kind of
organization that you work for, plus all its affiliates. **Affiliates**
means the other organizations than an organization has control over, is
under the control of, or is under common control with. **Control** means
ownership of substantially all the assets of an entity, or the power to
direct its management and policies by vote, contract, or otherwise. **Your
licenses** are all the licenses granted to you for the software under these
terms. **Use** means anything you do with the software requiring one of your
licenses.
```

### Additional grant: unrestricted academic and research use

*This clause is this project's own addition, layered on top of the
unmodified PolyForm Shield text above rather than edited into it.*

Notwithstanding the Noncompete term, the licensor grants the following users
an unrestricted copyright license to the software — equivalent to the MIT
License, with no Noncompete term — to use, copy, modify, merge, publish,
distribute, sublicense, and deal in the software for any purpose, including
building a product or service that would otherwise compete with the
licensor's:

- a university, research institute, or other nonprofit academic or
  educational institution;
- an individual acting in a personal research, academic, or educational
  capacity, and not on behalf of a for-profit entity;
- a peer-reviewed publication, thesis, or dataset built on the software,
  regardless of the author's affiliation.

This additional grant does **not** extend to a for-profit company or anyone
acting on its behalf, even one affiliated with or spun out of an academic
institution, and does not extend to any commercial product or service built
on the software by a for-profit entity.

**This is not legal advice, and this clause has not been reviewed by a
lawyer.** The boundary cases that matter most in practice — university
spinouts, industry-funded academic labs, dual-affiliation researchers — are
exactly the kind of thing a real IP attorney should look at before this is
relied on for anything consequential. Treat the above as a clear statement
of intent, not a finished legal instrument.

## Third-party data — NOT redistributed

**No corpus data ships in this repository.** Both corpora are generated locally
from their original sources. See [`data/README.md`](data/README.md) for how, and
for what each source's terms require of you.

This is deliberate. Redistributing convenient copies would require asserting
rights over other people's scholarship that this project does not clearly hold.

### `data/corpus_v1.json` — generated, not shipped

A compiled derivative of GORILA (Godart & Olivier 1976–1985, Études Crétoises
XXI), George Douros's tabulation, John G. Younger's commentary, and the
`mwenge/lineara.xyz` digital extraction.

**The upstream repository carries no LICENSE file and no license statement.**
Under default copyright that is all rights reserved. This project therefore does
not redistribute it and builds the corpus locally instead.

The build scripts (`src/extract_raw.js`, `src/build_corpus.py`) are original work
licensed under PolyForm Shield 1.0.0 (see above). Their **output is not**: it is
a derivative of the sources above and carries whatever terms those sources
impose. Users should consult the original sources for their terms of use.

### `data/sigla_corpus.json` — generated, not shipped

Derived from the **SigLA** database.

> © 2020– Ester Salgarella and Simon Castellan.
> Dataset and drawings licensed **CC BY-NC-SA 4.0**. https://sigla.phis.me/
> Full license terms: https://creativecommons.org/licenses/by-nc-sa/4.0/

**The license attaches to the data, not to the code that processes it.**
`src/ocaml_marshal.py` and `src/extract_sigla.py` are original work licensed
under PolyForm Shield 1.0.0, but any output they produce from SigLA input is a
derivative work of SigLA and remains **CC BY-NC-SA 4.0**. Re-encoding a format
does not create a new copyright in the underlying material.

Distributing that output obliges you to attribute Salgarella and Castellan, use
it non-commercially, and share alike.

Cite as: Salgarella, E. & Castellan, S. (2021), "SigLA: The Signs of Linear A. A
Paleographical Database", *Proceedings of the 5th International Conference on
Digital Access to Textual Cultural Heritage*.

### `data/divergences.json` — original work, PolyForm Shield 1.0.0

The divergence register is this project's own analysis. It records competing
readings by sign identifier, with attribution, as ordinary scholarly citation.

### Linear B lexicon — cloned at runtime, not vendored

Luo, J., Cao, Y. & Barzilay, R. (2019), "Neural Decipherment via Minimum-Cost
Flow: From Ugaritic to Linear B", *ACL 2019*, 3146–3155.
https://github.com/j-luo93/NeuroDecipher

`setup.sh` clones it at run time. **Consult that repository's own license before
reusing its data.** This project neither redistributes it nor asserts anything
about its terms.

### Fraction values — used, not redistributed

Corazza, M., Ferrara, S., Montecchi, B., Tamburini, F. & Valério, M. (2021),
"The mathematical values of fraction signs in the Linear A script", *Journal of
Archaeological Science* 125: 105214. CC BY-NC-ND, open access.

Their numeric values appear in `src/build_corpus.py` with citation. Using
published values with attribution is ordinary scholarly citation; the paper
itself is not redistributed.

### GORILA — transcriptions as well as images

Not redistributed, in either form. Plate images are © École française
d'Athènes, and generated records retain a `gorila_ref` field linking to the
source plate rather than reproducing it.

**This project holds no rights in the GORILA transcriptions or Younger's commentary
and cannot grant permission for their use.** The sign readings underlying `corpus_v1.json`
originate there. Users must satisfy themselves that their use of GORILA-derived
and Younger-derived material is permitted under applicable law in their jurisdiction
and for their purpose.

What this repository does is link to `cefael.efa.gr` — EFA's own free digital
library — and clone a public GitHub repository. It hosts neither. The reasoning,
including the residual risk and what would remove it, is set out in
`data/README.md` item 1.

## Summary

| Component                 | Licence                                    | Shipped?               |
|---------------------------|--------------------------------------------|------------------------|
| `src/`, `tests/`, `docs/` | PolyForm Shield 1.0.0 + academic carve-out | yes                    |
| `paper/`                  | CC BY 4.0                                  | yes                    |
| `data/divergences.json`   | PolyForm Shield 1.0.0 + academic carve-out | yes                    |
| `data/corpus_v1.json`     | derivative; upstream unlicensed            | **no — built locally** |
| `data/sigla_corpus.json`  | CC BY-NC-SA 4.0                            | **no — built locally** |
| Linear B lexicon          | see upstream                               | no — cloned at runtime |
| GORILA plate images       | © EFA                                      | no                     |

## Compliance checklist for users

**If you generate `data/corpus_v1.json`:**

- [ ] Satisfy yourself that your use of GORILA transcriptions is appropriate for
      your jurisdiction and purpose
- [ ] Cite Godart, L. & Olivier, J.-P. (1976–1985), *Recueil des inscriptions en
      linéaire A*, Études Crétoises XXI, 1–5
- [ ] Credit the upstream digital extraction (`mwenge/lineara.xyz`), noting that
      it carries no license statement
- [ ] Verify the build: `./data/verify.sh`, or `md5sum data/corpus_v1.json`
      giving `2f5c936f0848fcbcb4ef35669eccca99` (sha256
      `a642976320aaaa52f67f3fc29539a3ee88ea683e25bc2d6d8969e6d6114a93a1`) for
      the 2026-08-05 upstream snapshot.
      A different value means the upstream corpus has changed and the figures in
      the paper may no longer describe it; the test suite will tell you so.

**If you generate `data/sigla_corpus.json`:**

- [ ] Attribute Salgarella and Castellan
- [ ] Cite Salgarella, E. & Castellan, S. (2021), "SigLA: The Signs of Linear A.
      A Paleographical Database"
- [ ] Use it **non-commercially**
- [ ] **Share alike** — any derivative you distribute must carry CC BY-NC-SA 4.0
- [ ] Do not redistribute SigLA's drawings; the extractor does not touch them
- [ ] Verify the extraction: `md5sum data/sigla_corpus.json` gives
      `f3cb6d5805bd5376eef7099705d3d2ef` (sha256
      `7e2157090b847a1bafccd2a7465babd8a9c9b4f7de5b28ce22ecf9ce3f5106b8`) for
      the SigLA snapshot used here;
      802 documents and 5144 attestations, of which 4712
      confident, 44 doubtful, 388 unreadable or unclassified. The test suite
      asserts these. A different count means SigLA has been updated since this
      work, which is expected over time and is not an error.

**If you distribute anything built on both:** the CC BY-NC-SA share-alike term
is the binding constraint, and it applies to the combined work.

## Disclaimer

This repository distributes original code and analysis, and generates
third-party data locally rather than redistributing it. Every effort has been
made to respect the terms of the underlying scholarship, some of which has
complex or unstated copyright status. Users are responsible for ensuring their
own use complies with all applicable terms.

If you hold rights in any material referenced here and believe it is handled
incorrectly, please contact the author for correction or removal.
