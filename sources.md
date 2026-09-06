# Sources

The frozen bibliography lives in `references.yaml` as CSL records with stable IDs; the manuscript cites them with Pandoc `[@id]` syntax and `papers refs` reconciles the two. This file records provenance for each entry. Support for particular assertions, as distinct from identity, is bound in `claims.yaml`.

## Provenance

Every entry was resolved through the Crossref REST API against the DOI recorded in `references.yaml`, and the title, author list, container, volume, issue, pages and year printed here were taken from that response rather than from memory. Where an abstract was available through Crossref it was read in full and is quoted or paraphrased in `research.md`; where it was not, that is said below and the manuscript asserts nothing that the abstract would have been needed to support.

- `acemoglu2006` — Crossref, DOI 10.1017/cbo9780511510809. Identity verified. Crossref records the issued year as 2005, which is the online registration; the print year is 2006 and is the one cited. Cited for the central argument of the monograph; not read at page level.
- `buenodemesquita2003` — Crossref, DOI 10.7551/mitpress/4292.001.0001. Identity verified. Cited for the central argument; not read at page level.
- `butcher2014` — Crossref, DOI 10.1177/0022002714541843. Crossref issued year 2014, print issue *Journal of Conflict Resolution* 60(2) in 2016; the Crossref year is cited. Abstract truncated in the Crossref record; cited for the existence of the structural-conditions literature only.
- `chenoweth2015` — Crossref, DOI 10.17813/1086-671x-20-4-427. Abstract read in full. The Crossref title carries a trailing asterisk from the journal's own footnote marker, removed in the CSL record.
- `chenoweth2020` — Crossref, DOI 10.1353/jod.2020.0046. Identity verified; Crossref returns no abstract and the full text was not obtained. Cited as a pointer to the research programme. No claim in the manuscript rests on it.
- `chenoweth2022dynamic` — Crossref, DOI 10.1371/journal.pone.0269976. Abstract read in full. Open access.
- `chenoweth2022navco` — Crossref, DOI 10.1177/00223433221092938. Cited for the dataset's identity.
- `clarke2022` — Crossref, DOI 10.1017/s0003055422001174. Abstract read in full. Crossref issued year 2022, print issue *American Political Science Review* 117(4) in 2023; the Crossref year is cited.
- `debs2010` — Crossref, DOI 10.1017/s0003055410000195. Abstract read in full.
- `escriba2013` — Crossref, DOI 10.1177/0192512113488259. Abstract read in full. A bibliographic search first returned an SSRN preprint (10.2139/ssrn.1705508) and, in an earlier note, an incorrect journal; the published version is in *International Political Science Review* 34(5), and that is what is cited.
- `geddes2014` — Crossref, DOI 10.1017/s1537592714000851. Abstract read in full.
- `haines1984` — Crossref, DOI 10.1525/sp.1984.32.1.03a00030. A duplicate record exists under 10.2307/800260; the Social Problems DOI is the one cited. Crossref returns no abstract and the full text was not obtained. Cited for the provenance of the positive radical-flank hypothesis only, which the title establishes.
- `hess2006` — Crossref, DOI 10.17813/maiq.11.2.3204855020732v63. Identity verified; no abstract available through Crossref. Cited for the central argument.
- `kadivar2018` — Crossref, DOI 10.1177/0003122418759546. Abstract read in full. Carries the article's own numbers: 112 young democracies in 80 countries.
- `kuran1991` — Crossref, DOI 10.2307/2010422. Identity verified; no abstract in the Crossref record. Cited for the central argument.
- `lawrence2016` — Crossref, DOI 10.1017/s0007123415000733. Abstract read in full. Crossref issued year 2016, print issue *British Journal of Political Science* 47(3) in 2017; the Crossref year is cited.
- `levitsky2010` — Crossref, DOI 10.1017/cbo9780511781353. Identity verified. Cited for the central argument; not read at page level.
- `nepstad2013` — Crossref, DOI 10.1177/0022343313476529. Abstract read in full.
- `pearlman2011` — Crossref, DOI 10.1017/cbo9781139013239. Identity verified. Cited for the central argument; not read at page level.
- `raleigh2010` — Crossref, DOI 10.1177/0022343310378914. Cited for the dataset's identity.
- `ritter2016` — Crossref, DOI 10.1017/s0003055415000623. Abstract read in full. A corrigendum was published in 2024 (10.1017/s0003055424000455, under a changed author name); no numeric result from the article is used here, and the citation supports only the endogeneity caution.
- `ryckman2019` — Crossref, DOI 10.1177/0022002719861707. Abstract read in full. Crossref issued year 2019, print issue *Journal of Conflict Resolution* 64(2-3) in 2020; the Crossref year is cited.
- `simpson2022` — Crossref, DOI 10.1093/pnasnexus/pgac110. Abstract read in full. Open access. Carries the article's own sample size: N = 2,772 across two experiments.
- `slater2013` — Crossref, DOI 10.1017/s1537592713002090. Abstract read in full.
- `stephan2008` — Crossref, DOI 10.1162/isec.2008.33.1.7. Abstract read in full. The 2011 Columbia University Press monograph of the same title extends this article; it could not be resolved through Crossref in this pass, so the article, which is what was checked, is the locator cited. Note the author order: Stephan and Chenoweth on the article, Chenoweth and Stephan on the book.
- `sutton2014` — Crossref, DOI 10.1177/0022343314531004. Abstract read in full. A preprint exists under 10.2139/ssrn.2285248 with a variant title; the journal version is cited.
- `svolik2012` — Crossref, DOI 10.1017/cbo9781139176040. Identity verified. Cited for the central argument; not read at page level.
- `weinstein2006` — Crossref, DOI 10.1017/cbo9780511808654. Identity verified. Cited for the central argument; not read at page level.

## Sources considered and not cited

- Staniland, *Networks of Rebellion*. The Crossref record for the Cornell University Press edition (10.7591/9780801471032) reports the year as 2018 and the type as an edited book, both of which conflict with the 2014 authored monograph. Rather than cite a locator whose metadata could not be reconciled, the point about insurgent organizational structure rests on `weinstein2006` alone.
- No source was identified that estimates the differential sensitivity of clandestine and open organizations to repression. The two sensitivities in the model are stipulated, and the manuscript says so and reports the null in which they are equal.

## Numbers taken from sources rather than from the simulation

Three, all from abstracts read in full and all attributed in the manuscript to their source rather than to the model: the roughly half of autocratic regime changes that are transitions from one autocracy to another, over 280 regimes between 1946 and 2010 [@geddes2014]; the 112 young democracies in 80 countries in the survival analysis [@kadivar2018]; and the 2,772 participants across the two radical-flank experiments [@simpson2022]. Every other number in the manuscript is bound to a JSON pointer in a recorded execution.
