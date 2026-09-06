# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-09-06 — v1, complete

Scope: the whole paper, three mechanisms, the coupling and the evidence base, from the seed chat to the built PDF and the bound claim ledger.

Changes:
  - The paper's contribution is the coupling the seed explicitly declined to claim. The seed's own words were that escalation raising the probability of removal while lowering the probability of a durable, accountable successor was "not yet a result of our prototype". It is the result here, and it is a result about a stipulated model rather than about any campaign.
  - Bibliography built as CSL records in `references.yaml` with Pandoc `[@id]` citations; 28 entries, every one resolved through the Crossref REST API against its DOI, all 28 cited in the manuscript. One seed-adjacent locator was wrong in an earlier working note and is corrected here: Escribà-Folch's "Repression, political threats, and survival under autocracy" is in *International Political Science Review* 34(5) 543–560, not *Democratization*. A bibliographic search returns an SSRN preprint first; the published version is what is cited.
  - Where Crossref carries an online-first year that differs from the print year, the Crossref year is used and each instance is recorded in `sources.md`: Clarke (2022 online, 117(4) in 2023), Ryckman (2019 online, 64(2-3) in 2020), Lawrence (2016 online, 47(3) in 2017), Butcher and Svensson (2014 online, 60(2) in 2016). Acemoglu and Robinson is cited as 2006, the print year, where Crossref records 2005 for the online registration.
  - Staniland's *Networks of Rebellion* was considered and dropped. The Crossref record for the Cornell edition reports 2018 and the type "edited-book", both conflicting with the 2014 authored monograph, and a locator whose metadata could not be reconciled is not worth citing. The point it would have supported rests on Weinstein alone.
  - Full text was obtained for no entry; abstracts were retrieved through Crossref and read in full for nineteen of the twenty-eight. The nine without a Crossref abstract are cited for identity or for a central argument the title establishes, and each is flagged as such in `sources.md`. Nothing in the manuscript asserts more than what was actually read.

Model corrections during the work:
  - The first version of the coupling produced no result. Escalation lowered the probability of removal everywhere and all three optima sat at zero escalation, because repression destroyed armed capacity faster than arming built it. The defect was that escalation was modelled as changing only the repression a campaign draws, when it also changes the campaign's composition at the source. Adding that channel gave armed capacity an interior peak and produced the divergence. This was a modelling error, not a finding, and the corrected model is the one reported.
  - Fixing it required making the armed wing *less* differentially protected from repression: sensitivities of 0.28 against 0.60, a ratio of 2.1, where the first version used 0.10 against 0.55, a ratio of 5.5. The conservative ratio costs the second section its most quotable claim. Under it the armed wing does not acquire a majority of surviving capacity at any repression intensity within six periods; it reaches parity at 6.24 periods. The weaker claim is the one the model supports and the one reported.
  - The results serializer rounded every float to six decimal places, which stored the closed-form verification error as exactly 0.0 and would have made the manuscript's claim about it unbindable and overstated. It now keeps six significant digits, and the stored error is 3.33067e-16. The manuscript states the invariant's tolerance and calls the observed disagreement double-precision rounding rather than quoting a figure whose surface form could not be matched.
  - The divergence was first read at the boundary of the region where escalation helps removal, where the gain in removal probability is 0.0004. Reading it there makes the trade-off look free. It is now read at the institutional condition where escalating buys the largest gain, 0.078, which is the strongest case for escalation. The conclusion survives at the fair reading.

Verification:
  - `papers run --id coupling` records the execution; 24 invariants pass and a failed invariant fails the run. Two grids are enumerated exhaustively (4896 decision cells; 101 escalation levels against 241 institutional conditions) and the robustness test is a seeded ensemble of 600 draws with every constant perturbed by an independent uniform factor in [0.6, 1.4].
  - `claims.yaml` binds 56 claims to the manuscript at its reviewed hash: 33 computations bound to JSON pointers in the recorded run, 14 source claims each with a locator and a candid verification note, 4 assumptions, 2 definitions, 2 interpretations and 1 normative limit. Three numbers in the manuscript come from sources rather than from the simulation and are attributed to them in the text.
  - `papers check --stage local` passes. All eleven PDF pages were inspected at full size and the record is in `visual-review.json`.

Known limits, all stated in the manuscript:
  - The functional forms are stipulated and the ensemble perturbs constants, not forms. The accountability function is the weakest joint: a product of two stipulated terms with two stipulated coefficients.
  - The two retention sensitivities are the parameter section three rests on, and no empirical estimate of them was found. The direction of the composition shift follows from the organizational argument; every magnitude is a function of a ratio nobody has measured.
  - Backfire is absent from the model. Including it would raise the returns to remaining unarmed and strengthen the paper's conclusion, so the result reported is the one obtained without the mechanism that would favour it.
  - Concession from strength is absent. The incumbent concedes only when conceding is the cheapest of three costs, which is a narrower ruler than the literature describes.
  - No parameter was estimated from NAVCO, ACLED or any other data. The model is not fitted and makes no prediction those data could refute.

Editorial:
  - Seventeen voice diagnostics were triaged and all seventeen rewritten; the manuscript now returns zero editorial candidates. Corpus lint reports no statistical outliers.
  - Two figures, both inspected in page context at final scale. Figure 2's ensemble annotation originally rendered as dark text over a green bar and was moved into a boxed area above the bars; its second panel was re-scaled so the threshold step is visible rather than a hairline. Figure 1's categorical legend was given an opaque background so the grey swatch remains visible against the grey region behind it.
  - The paper deliberately makes no reference to any live conflict. A mechanism model with stipulated parameters must not read as advice to people facing an actual decision, and the manuscript says so.
