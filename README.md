# Concession and Succession

Where Escalation Buys Removal at the Price of an Accountable Successor.

Two findings about campaigns against entrenched rulers have been established separately. Nonviolent campaigns remove incumbents more often than armed campaigns, and escalation reduces the participation on which removal depends. Armed revolutions that succeed, however, are less often reversed, while sustained unarmed mobilisation is associated with successor regimes that are more durable and more accountable. Escalation is therefore evaluated against different outcomes in different literatures. We combine the outcomes in a stipulated model. Attention raises the ruler's cost of both waiting and repression, so it moves cases out of delay in both directions: 610 waiting cases of the incumbent's decision problem move to repression and 400 to concession. Attention enlarges the region in which concession is cheapest from 0.158 to 0.286 of the swept region, and escalation then reduces it to 0.102. Repression that removes civilian organisations faster than armed ones shifts a campaign's composition without conversion or recruitment; the two wings reach parity after 6.24 periods of maximal repression, when 0.025 of the original campaign remains. Escalation raises the probability of removal only where an intact civilian campaign could withdraw at most 0.0475 of the coercive apparatus's cooperation. Under the condition most favourable to escalation, it raises the probability of removal from 0.107 to 0.184 and retains 0.109 of the probability of an accountable successor that not escalating would secure. Across 600 random parameter draws, escalation raised the probability of removal in 62 and lowered the probability of an accountable successor in all 62.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

Twenty-four invariant checks fail the run if broken, among them the agreement between the closed-form odds ratio and the period-by-period iteration, the null in which indiscriminate repression leaves the campaign's composition exactly where it began, the interior peak of armed capacity, the monotone loss of civilian capacity to escalation, and the requirement that the ensemble never aligns removal with accountable succession. Two grids are swept exhaustively; the robustness test is a seeded ensemble of 600 draws. Execution is recorded in `verification/coupling.json` and every number quoted in the manuscript is bound to a JSON pointer in `claims.yaml`. Nothing here is calibrated to any campaign, country or ruler, and the model estimates no real probability.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run `papers build concession-and-succession`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace docs for the research and writing pipelines.
