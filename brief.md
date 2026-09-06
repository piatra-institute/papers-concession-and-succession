# Brief

## Question

Two findings about campaigns against entrenched rulers are well established separately and have never been put in the same model. Nonviolent campaigns unseat incumbents more often than armed ones. Armed revolutions that do succeed produce regimes that survive counterrevolution, while the successors of demobilized campaigns are more often unaccountable. Escalation is therefore evaluated against one outcome at a time, and the outcomes are different. Under what institutional conditions does escalation raise the probability that the incumbent is removed while lowering the probability that whatever replaces it is accountable, and how large is each of the two effects at the point where escalation looks best?

## Claim

Three results, each a property of an explicitly stated model rather than an estimate of anything.

1. Making a campaign visible does not make a ruler more likely to concede. It makes the ruler more likely to act. Attention raises the cost of waiting and the cost of repression at once, so it converts cells of the incumbent's decision problem out of delay in both directions: in the swept region it sends 610 waiting cases to repression against 400 to concession. Attention enlarges the concession region on net, from 0.158 of the region to 0.286, and escalation then cuts it to 0.102 — a larger loss than attention's gain. The threshold has a closed form: institutional cooperation must fall to 0.280 before conceding is the cheapest answer when the campaign has no material leverage, and to 0.526 when it has all of it. Leverage nearly doubles the cooperation a ruler can still command and yet find concession cheapest.

2. A campaign's composition shifts toward its armed wing under repression with nobody converting, nobody recruiting and nobody changing their mind. Civilian organizations need assembly, publicity and open membership; clandestine ones need less of each. Giving the two wings different sensitivities to repression makes the odds ratio between them a clean exponential in time, verified against period-by-period iteration at double precision. A campaign that begins one-tenth armed reaches parity after 6.24 periods of maximal repression, by which point 2.5% of the original campaign is left standing. Where repression is indiscriminate the composition does not move at all, which locates the effect in the differential and not in the violence.

3. Coupling the two, escalation improves the odds of removal only in a narrow corner: where an intact civilian campaign could strip at most 0.0475 of the apparatus's cooperation, an apparatus insulated from domestic noncooperation by coup-proofing, foreign patronage or indifference. Read at the condition where escalation looks best rather than at the worst, it raises the probability of removal from 0.107 to 0.184 and retains 0.109 of the accountable-succession probability that not escalating would have secured. Removal and durability both peak at escalation 0.61; accountability peaks at 0. Across 600 random parameter draws, escalation raised the chance of removal in 62, and in all 62 it lowered accountable succession, the best case retaining 0.171.

## Kind

Formal-model. A stipulated mechanism model, not an estimate: exhaustive grids where the space permits and a seeded random ensemble for the robustness test. `claims_target` is the bound ledger in claims.yaml.

## Cornerstone literature

The empirical baseline that escalation is on average counterproductive for removal (Stephan and Chenoweth; Chenoweth and Schock; Chenoweth). The conditions under which movements escalate anyway (Ryckman; Pearlman). The two findings that pull against each other on succession: mass mobilization sustains new democracies (Kadivar) against revolutionary violence producing regimes that resist counterrevolution (Clarke). The radical-flank literature that says escalation can help a moderate wing (Haines; Simpson, Willer and Feinberg). The incumbent's side: the canonical concession-versus-repression model (Acemoglu and Robinson), concession from strength (Slater and Wong), the dictator's dependence on subordinates who can stop cooperating (Svolik; Bueno de Mesquita, Smith, Siverson and Morrow), the ruler's post-tenure fate (Debs and Goemans), and backfire (Sutton, Butcher and Svensson; Hess and Martin are the older statement). Preference falsification, for why the apparatus's cooperation can collapse without warning (Kuran). Security-force defection as the proximate mechanism of removal (Nepstad). Insurgent organization and what armed groups become (Weinstein).

## Discipline

No number in the manuscript that is not bound to a JSON pointer in a recorded execution. No claim about any actual country, campaign, or ruler. The model stipulates its functional forms and says so; the results are what those forms jointly imply, which is the point, since each mechanism is familiar on its own and their interaction is not. Where the literature is in tension the tension is reported rather than resolved.
