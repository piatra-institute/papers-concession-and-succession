# Concession and Succession

Where Escalation Buys Removal at the Price of an Accountable Successor.
Two findings about campaigns against entrenched rulers are secure separately and
have never been put in the same model. Nonviolent campaigns unseat incumbents
more often than armed ones, and campaigns that escalate lose the participation
that produces removal. Yet armed revolutions that do succeed resist
counterrevolution, while sustained unarmed mobilization is what produces
successors that answer to anyone. This paper couples removal, durability and
accountability in one stipulated model and computes what the coupling implies.
Making a campaign visible makes a ruler more likely to act rather than to
concede: attention moves 610 waiting cases of the incumbent's decision problem to
repression against 400 to concession, and though it enlarges the concession
region, escalation then takes back more than it gained. Under repression a
campaign's composition shifts toward its armed wing with nobody converting and
nobody recruiting, reaching parity after 6.24 periods of maximal repression, by
which point 0.025 of the original campaign is left standing; set the two
sensitivities equal and the composition does not move at all. Coupling the two,
escalation improves the odds of removal only where an intact civilian campaign
could strip at most 0.0475 of the apparatus's cooperation. Read where escalation
looks best, it raises the probability of removal from 0.107 to 0.184 and retains
0.109 of the accountable succession that not escalating would have secured.
Across 600 random parameter draws escalation helped removal in 62, and lowered
accountable succession in all 62.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

Twenty-four invariant checks fail the run if broken, among them the agreement
between the closed-form odds ratio and the period-by-period iteration, the null
in which indiscriminate repression leaves the campaign's composition exactly
where it began, the interior peak of armed capacity, the monotone loss of
civilian capacity to escalation, and the requirement that the ensemble never
aligns removal with accountable succession. Two grids are swept exhaustively; the
robustness test is a seeded ensemble of 600 draws. Execution is recorded in
`verification/coupling.json` and every number quoted in the manuscript is bound
to a JSON pointer in `claims.yaml`. Nothing here is calibrated to any campaign,
country or ruler, and the model estimates no real probability.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run
`papers build concession-and-succession`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace
docs for the research and writing pipelines.
