"""Concession and succession, computed.

Every quantity below is a property of an explicitly stated model. Nothing here
is fitted to any campaign, estimates any real probability, or describes any
particular country. The functional forms are stipulated; what is computed is
what they jointly imply, which is the point, since the mechanisms are familiar
one at a time and their interaction is not.

1. The incumbent's choice. Concede, repress or wait, compared on perceived cost
   to the incumbent rather than cost to anyone else. Repression is cheap while
   the institutions that carry it out cooperate and expensive as they stop.
   Escalation raises the cost of conceding, because a ruler who expects to be
   killed or tried after leaving values staying more highly. The concession
   region is mapped over institutional cooperation and material leverage, and
   the effect of raising attention alone is measured by counting which cells
   change their answer and to what.

2. Differential attrition. Civilian organizations need assembly, publicity and
   open membership; clandestine armed organizations need less of each. Giving
   them different sensitivities to repression, the armed share of what survives
   rises with no recruitment, no conversion and no change of belief. The number
   of periods of maximal repression after which the two wings reach parity is
   computed in closed form, along with how little capacity is left by then.

3. The coupling. Removal, durability and accountability are three outcomes, not
   one. Escalation is allowed to raise all three, and the escalation level that
   maximises each is located separately. The institutional condition is reduced
   to one interpretable quantity, the cooperation an intact civilian campaign
   can strip from the apparatus, and the conditions under which escalation
   improves the odds of removal are found rather than assumed. The divergence is
   then tested across a random ensemble of parameter draws rather than displayed
   at one hand-chosen point.

Seeded. A failed invariant fails the run.
"""
from __future__ import annotations

import numpy as np

SEED = 20260906


def _py(x):
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    if isinstance(x, (np.floating,)):
        return float(f"{float(x):.6g}")
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, np.ndarray):
        return [_py(v) for v in x.tolist()]
    if isinstance(x, float):
        return float(f"{x:.6g}")
    return x


# ---------------------------------------------------------------------------
# 1. The incumbent's choice
# ---------------------------------------------------------------------------
CONCEDE_BASE = 25.0      # perceived cost of relinquishing power at zero escalation
EXIT_FEAR = 18.0         # how much escalation adds to that cost
REPRESS_BASE = 6.0       # cost of repression when the apparatus fully cooperates
REPRESS_ATTENTION = 4.0  # external and political cost of repression under attention
REPRESS_LEVERAGE = 10.0  # withdrawn cooperation is not restored by force
WAIT_BASE = 3.0
WAIT_LEVERAGE = 40.0     # disruption from withdrawn cooperation
WAIT_ATTENTION = 14.0    # disruption from attention alone
LOYALTY_GRID = np.round(np.linspace(0.05, 1.00, 96), 4)
LEVERAGE_GRID = np.round(np.linspace(0.00, 1.00, 51), 4)
ATTENTION_LOW, ATTENTION_HIGH = 0.10, 0.90
OPTIONS = ("concede", "repress", "wait")


def _costs(loyalty, leverage, attention, escalation):
    concede = CONCEDE_BASE + EXIT_FEAR * escalation
    repress = (REPRESS_BASE / max(loyalty, 1e-6) + REPRESS_ATTENTION * attention
               + REPRESS_LEVERAGE * leverage)
    wait = WAIT_BASE + WAIT_LEVERAGE * leverage + WAIT_ATTENTION * attention
    return {"concede": concede, "repress": repress, "wait": wait}


def _choice(loyalty, leverage, attention, escalation) -> str:
    c = _costs(loyalty, leverage, attention, escalation)
    return min(OPTIONS, key=lambda k: c[k])


def _field(attention, escalation) -> np.ndarray:
    return np.array([[OPTIONS.index(_choice(l, e, attention, escalation))
                      for e in LEVERAGE_GRID] for l in LOYALTY_GRID])


def run_choice() -> dict:
    low = _field(ATTENTION_LOW, 0.0)
    high = _field(ATTENTION_HIGH, 0.0)
    escalated = _field(ATTENTION_HIGH, 0.60)
    total = low.size

    def share(field, option):
        return float((field == OPTIONS.index(option)).sum() / total)

    waiting = low == OPTIONS.index("wait")
    to_repress = int(((high == OPTIONS.index("repress")) & waiting).sum())
    to_concede = int(((high == OPTIONS.index("concede")) & waiting).sum())
    still_waiting = int(((high == OPTIONS.index("wait")) & waiting).sum())

    # how far institutional cooperation must fall before repression stops being
    # the cheapest answer, at each level of leverage, with attention high
    thresholds = []
    for lev in (0.0, 0.25, 0.50, 0.75, 1.00):
        concede_cells = [float(l) for l in LOYALTY_GRID
                         if _choice(l, lev, ATTENTION_HIGH, 0.0) == "concede"]
        highest = max(concede_cells) if concede_cells else None
        analytic = (REPRESS_BASE / (CONCEDE_BASE - REPRESS_ATTENTION * ATTENTION_HIGH
                                    - REPRESS_LEVERAGE * lev)
                    if CONCEDE_BASE - REPRESS_ATTENTION * ATTENTION_HIGH
                    - REPRESS_LEVERAGE * lev > 0 else None)
        thresholds.append({"leverage": float(lev),
                           "highest_loyalty_conceding": highest,
                           "analytic_crossing": analytic})

    return {
        "grid_cells": total,
        "share_concede_low_attention": share(low, "concede"),
        "share_concede_high_attention": share(high, "concede"),
        "share_repress_low_attention": share(low, "repress"),
        "share_repress_high_attention": share(high, "repress"),
        "share_wait_low_attention": share(low, "wait"),
        "waiting_cells": int(waiting.sum()),
        "wait_to_repress": to_repress,
        "wait_to_concede": to_concede,
        "wait_unchanged": still_waiting,
        "urgency_ratio": (to_repress / to_concede) if to_concede else float("inf"),
        "share_concede_escalated": share(escalated, "concede"),
        "concession_region_lost_to_escalation":
            share(high, "concede") - share(escalated, "concede"),
        "loyalty_thresholds": thresholds,
        "crossing_at_zero_leverage": thresholds[0]["analytic_crossing"],
        "crossing_at_full_leverage": thresholds[-1]["analytic_crossing"],
        "fields": {"low": low.tolist(), "high": high.tolist(),
                   "escalated": escalated.tolist()},
        "loyalty_grid": LOYALTY_GRID.tolist(),
        "leverage_grid": LEVERAGE_GRID.tolist(),
    }




# ---------------------------------------------------------------------------
# 2. Differential attrition
# ---------------------------------------------------------------------------
# Civilian organizations need assembly, publicity and open membership;
# clandestine armed organizations need less of each, so repression removes them
# more slowly. Nobody in this block changes their mind about anything: the
# composition of the surviving campaign moves without anyone converting.

ARMED_SHARE_0 = 0.10
RETENTION_ARMED_0 = 0.95
RETENTION_CIVIC_0 = 0.92
SENS_ARMED = 0.28        # sensitivity of armed retention to repression
SENS_CIVIC = 0.60        # sensitivity of civilian retention to repression
PERIODS = 6
REPRESSION_GRID = np.round(np.linspace(0.0, 1.0, 51), 4)


def _retentions(repression: float) -> tuple:
    return (RETENTION_ARMED_0 * np.exp(-SENS_ARMED * repression),
            RETENTION_CIVIC_0 * np.exp(-SENS_CIVIC * repression))


def _capacities(repression: float, t: int, w0: float = ARMED_SHARE_0) -> tuple:
    """Surviving armed and civilian capacity as fractions of the original whole."""
    sa, sc = _retentions(repression)
    return w0 * sa ** t, (1.0 - w0) * sc ** t


def _armed_share(repression: float, t: int, w0: float = ARMED_SHARE_0) -> float:
    a, c = _capacities(repression, t, w0)
    return a / (a + c)


def _total_capacity(repression: float, t: int, w0: float = ARMED_SHARE_0) -> float:
    return sum(_capacities(repression, t, w0))


def run_attrition() -> dict:
    # the closed form for the odds ratio, checked against period-by-period iteration
    max_error = 0.0
    for repression in (0.0, 0.3, 0.6, 1.0):
        sa, sc = _retentions(repression)
        a, c = ARMED_SHARE_0, 1 - ARMED_SHARE_0
        for t in range(1, PERIODS + 1):
            a, c = a * sa, c * sc
            closed = (ARMED_SHARE_0 / (1 - ARMED_SHARE_0)) * (sa / sc) ** t
            max_error = max(max_error, abs(a / c - closed))

    rows = [{"repression": float(r),
             "armed_share": _armed_share(float(r), PERIODS),
             "total_capacity": _total_capacity(float(r), PERIODS)}
            for r in REPRESSION_GRID]
    majority = next((r for r in rows if r["armed_share"] >= 0.5), None)

    trajectories = {}
    for repression in (0.0, 0.4, 0.8):
        trajectories[f"r_{repression:g}"] = {
            "armed_share": [_armed_share(repression, t) for t in range(PERIODS + 1)],
            "total_capacity": [_total_capacity(repression, t)
                               for t in range(PERIODS + 1)],
        }

    # how much of the composition shift survives if the two wings are equally
    # exposed: the null in which repression is indiscriminate
    # periods of maximal repression until the two wings are equal in size
    sa1, sc1 = _retentions(1.0)
    parity = float(np.log((1 - ARMED_SHARE_0) / ARMED_SHARE_0) / np.log(sa1 / sc1))

    equal = RETENTION_CIVIC_0 * np.exp(-SENS_CIVIC * 1.0)
    a_eq = ARMED_SHARE_0 * equal ** PERIODS
    c_eq = (1 - ARMED_SHARE_0) * equal ** PERIODS

    return {
        "armed_share_initial": ARMED_SHARE_0, "periods": PERIODS,
        "retention_armed_base": RETENTION_ARMED_0,
        "retention_civic_base": RETENTION_CIVIC_0,
        "sensitivity_armed": SENS_ARMED, "sensitivity_civic": SENS_CIVIC,
        "closed_form_max_error": max_error,
        "rows": rows, "trajectories": trajectories,
        "repression_for_armed_majority":
            majority["repression"] if majority else None,
        "capacity_at_armed_majority":
            majority["total_capacity"] if majority else None,
        "armed_share_no_repression": _armed_share(0.0, PERIODS),
        "armed_share_full_repression": _armed_share(1.0, PERIODS),
        "capacity_full_repression": _total_capacity(1.0, PERIODS),
        "armed_share_indiscriminate_null": a_eq / (a_eq + c_eq),
        "periods_to_parity_full_repression": parity,
        "capacity_at_parity_full_repression": _total_capacity(1.0, parity),
        "armed_share_at_parity": _armed_share(1.0, parity),
    }


# ---------------------------------------------------------------------------
# 3. Removal, durability, accountability
# ---------------------------------------------------------------------------
# Escalation is allowed to help. Arming shifts the campaign's composition at the
# source as well as through attrition, and an armed wing can remove an incumbent
# by force without waiting for the apparatus to defect. What escalation cannot
# do is rebuild the civilian organization it spends. The three outcomes are
# scored separately and their maxima located separately.
#
# The institutional condition is summarized by one quantity: how much of the
# apparatus's cooperation an intact civilian campaign can strip. An apparatus
# that can be stripped of a lot is responsive; one that can be stripped of
# little is insulated, whether by coup-proofing, ethnic stacking, foreign
# patronage or simple indifference to domestic opinion.

ESCALATION_GRID = np.round(np.linspace(0.0, 1.0, 101), 4)
STRIP_GRID = np.round(np.linspace(0.0, 0.60, 241), 4)

BASE = {
    "arming": 0.60,             # share of the campaign escalation can convert
    "repression_floor": 0.15,   # repression when nothing is escalated
    "repression_gain": 0.75,    # how much escalation raises repression
    "rally": 0.30,              # cooperation the incumbent regains under escalation
    "coercion": 0.50,           # coercive weight of a fully loyal apparatus
    "removal_civic": 1.80,      # removal hazard per unit withdrawn cooperation
    "removal_armed": 1.10,      # removal hazard per unit armed advantage
    "durable_arms": 1.40,
    "durable_floor": 0.15,
    "accountable_civic": 2.20,
    "accountable_penalty": 1.60,
}


def _civic_intact(p: dict) -> float:
    """Civilian capacity surviving the repression an unescalated campaign draws."""
    return _capacities(p["repression_floor"], PERIODS, ARMED_SHARE_0)[1]


def _outcomes(escalation: float, strip: float, p: dict) -> dict:
    """strip = cooperation an intact civilian campaign can withdraw, in [0, 1]."""
    erosion = strip / _civic_intact(p)
    w0 = p["arming"] * escalation + ARMED_SHARE_0 * (1 - p["arming"] * escalation)
    repression = min(p["repression_floor"] + p["repression_gain"] * escalation, 1.0)
    armed, civic = _capacities(repression, PERIODS, w0)
    capacity = armed + civic
    armed_share = armed / capacity

    loyalty = float(np.clip(1.0 - erosion * civic + p["rally"] * escalation, 0.05, 1.0))
    withdrawn = 1.0 - loyalty
    advantage = armed / (armed + loyalty * p["coercion"])

    removal = 1.0 - np.exp(-(p["removal_civic"] * withdrawn
                             + p["removal_armed"] * advantage))
    durable = 1.0 - np.exp(-p["durable_arms"] * (armed + p["durable_floor"]))
    accountable = (1.0 - np.exp(-p["accountable_civic"] * civic)) \
        * np.exp(-p["accountable_penalty"] * armed_share)
    return {"escalation": escalation, "strip": strip,
            "armed_share_initial": w0, "repression": repression,
            "armed_capacity": armed, "civic_capacity": civic,
            "capacity": capacity, "armed_share": armed_share,
            "loyalty": loyalty, "armed_advantage": advantage,
            "removal": removal, "durable": durable, "accountable": accountable,
            "removal_and_durable": removal * durable,
            "removal_and_accountable": removal * accountable}


def _sweep(strip: float, p: dict) -> list:
    return [_outcomes(float(e), strip, p) for e in ESCALATION_GRID]


def _argmax(rows: list, key: str) -> tuple:
    best = max(rows, key=lambda r: r[key])
    return best["escalation"], best[key]


def _at(rows: list, escalation: float, key: str) -> float:
    return next(r[key] for r in rows if abs(r["escalation"] - escalation) < 1e-9)


def _analyse(strip: float, p: dict) -> dict:
    rows = _sweep(strip, p)
    x_rem, v_rem = _argmax(rows, "removal")
    x_acc, v_acc = _argmax(rows, "removal_and_accountable")
    x_dur, v_dur = _argmax(rows, "removal_and_durable")
    return {"strip": strip, "rows": rows,
            "argmax_removal": x_rem, "max_removal": v_rem,
            "argmax_accountable": x_acc, "max_accountable": v_acc,
            "argmax_durable": x_dur, "max_durable": v_dur,
            "removal_helped": x_rem > 0.0,
            "removal_at_accountable_optimum": _at(rows, x_acc, "removal"),
            "removal_gain": v_rem - _at(rows, x_acc, "removal"),
            "accountable_at_removal_optimum":
                _at(rows, x_rem, "removal_and_accountable"),
            "accountable_retained":
                _at(rows, x_rem, "removal_and_accountable") / v_acc
                if v_acc > 0 else None}


def run_coupling() -> dict:
    profile = [_analyse(float(s), BASE) for s in STRIP_GRID]
    helped = [r for r in profile if r["removal_helped"]]
    threshold_grid = max(r["strip"] for r in helped) if helped else None
    # the grid gives only the last evaluated point where escalation helps; the
    # boundary itself lies between that point and the next and is found by bisection
    threshold = threshold_grid
    if helped and threshold_grid < STRIP_GRID[-1]:
        lo, hi = threshold_grid, threshold_grid + float(STRIP_GRID[1] - STRIP_GRID[0])
        for _ in range(60):
            mid = (lo + hi) / 2
            if _analyse(mid, BASE)["removal_helped"]:
                lo = mid
            else:
                hi = mid
        threshold = lo

    # read the divergence where escalation looks best, not where it looks worst:
    # the institutional condition under which escalating buys the largest gain in
    # the probability of removal
    best = max(helped, key=lambda r: r["removal_gain"]) if helped else profile[0]
    focal = _analyse(best["strip"], BASE)
    rows = focal["rows"]
    rem = np.array([r["removal"] for r in rows])
    acc = np.array([r["removal_and_accountable"] for r in rows])
    dur = np.array([r["removal_and_durable"] for r in rows])
    diverging = (np.diff(rem) > 0) & (np.diff(acc) < 0)
    band = ESCALATION_GRID[:-1][diverging]
    dur_up_acc_down = (np.diff(dur) > 0) & (np.diff(acc) < 0)

    # does the divergence survive parameters other than the ones chosen here?
    rng = np.random.default_rng(SEED)
    draws = 600
    helped_draws, diverged, retained, gains = 0, 0, [], []
    for _ in range(draws):
        p = {k: float(v * rng.uniform(0.6, 1.4)) for k, v in BASE.items()}
        p["arming"] = float(np.clip(p["arming"], 0.0, 1.0))
        p["repression_floor"] = float(np.clip(p["repression_floor"], 0.0, 1.0))
        strip = float(rng.uniform(0.0, 0.6))
        r = _analyse(strip, p)
        if not r["removal_helped"]:
            continue
        helped_draws += 1
        gains.append(r["removal_gain"])
        if r["accountable_retained"] is not None:
            retained.append(r["accountable_retained"])
            if r["accountable_retained"] < 1.0:
                diverged += 1

    return {
        "profile": [{k: v for k, v in r.items() if k != "rows"} for r in profile],
        "focal_strip": focal["strip"], "rows": rows,
        "strip_grid_step": float(STRIP_GRID[1] - STRIP_GRID[0]),
        "strip_threshold": threshold,
        "strip_threshold_grid": threshold_grid,
        "strip_share_helped": threshold / float(STRIP_GRID[-1]),
        "strip_share_helped_grid": len(helped) / len(profile),
        "civic_intact": _civic_intact(BASE),
        "argmax_removal": focal["argmax_removal"],
        "max_removal": focal["max_removal"],
        "argmax_accountable": focal["argmax_accountable"],
        "max_accountable": focal["max_accountable"],
        "argmax_durable": focal["argmax_durable"],
        "max_durable": focal["max_durable"],
        "optimum_gap": focal["argmax_removal"] - focal["argmax_accountable"],
        "removal_at_accountable_optimum": focal["removal_at_accountable_optimum"],
        "removal_gain_from_escalating": focal["removal_gain"],
        "accountable_at_removal_optimum": focal["accountable_at_removal_optimum"],
        "accountable_retained_share": focal["accountable_retained"],
        "divergence_band_low": float(band.min()) if band.size else None,
        "divergence_band_high": float(band.max()) if band.size else None,
        "divergence_band_share": float(band.size / (len(rows) - 1)),
        "durable_up_accountable_down_share":
            float(dur_up_acc_down.sum() / (len(rows) - 1)),
        "ensemble_draws": draws,
        "ensemble_helped": helped_draws,
        "ensemble_helped_share": helped_draws / draws,
        "ensemble_diverged": diverged,
        "ensemble_diverged_share": diverged / helped_draws if helped_draws else None,
        "ensemble_median_retained": float(np.median(retained)) if retained else None,
        "ensemble_max_retained": float(np.max(retained)) if retained else None,
        "ensemble_median_removal_gain": float(np.median(gains)) if gains else None,
        "ensemble_max_removal_gain": float(np.max(gains)) if gains else None,
    }


# ---------------------------------------------------------------------------
# Invariants
# ---------------------------------------------------------------------------
def run() -> dict:
    choice = run_choice()
    attrition = run_attrition()
    coupling = run_coupling()

    prof = coupling["profile"]
    helped = [r for r in prof if r["removal_helped"]]
    rows = coupling["rows"]
    at = {round(r["escalation"], 4): r for r in rows}

    checks = {
        # 1. the incumbent's choice
        "every_cell_has_exactly_one_cheapest_option":
            choice["share_concede_low_attention"]
            + choice["share_repress_low_attention"]
            + choice["share_wait_low_attention"] == 1.0,
        "attention_moves_more_cells_to_repression_than_to_concession":
            choice["wait_to_repress"] > choice["wait_to_concede"],
        "attention_alone_enlarges_the_concession_region":
            choice["share_concede_high_attention"]
            > choice["share_concede_low_attention"],
        "escalation_shrinks_the_concession_region":
            choice["share_concede_escalated"]
            < choice["share_concede_high_attention"],
        "the_simulated_crossing_matches_the_analytic_one": all(
            t["highest_loyalty_conceding"] is None
            or abs(t["highest_loyalty_conceding"] - t["analytic_crossing"])
            <= float(LOYALTY_GRID[1] - LOYALTY_GRID[0]) + 1e-9
            for t in choice["loyalty_thresholds"]),
        "leverage_raises_the_cooperation_a_ruler_can_still_command": all(
            choice["loyalty_thresholds"][i + 1]["analytic_crossing"]
            > choice["loyalty_thresholds"][i]["analytic_crossing"]
            for i in range(len(choice["loyalty_thresholds"]) - 1)),
        "force_is_cheapest_against_a_campaign_with_leverage_and_no_witnesses":
            _choice(1.0, 0.30, 0.0, 0.0) == "repress",
        "an_unwatched_ruler_facing_no_leverage_simply_waits":
            _choice(1.0, 0.0, 0.0, 0.0) == "wait",
        "concession_is_cheapest_when_the_apparatus_is_gone":
            _choice(0.05, 1.0, ATTENTION_HIGH, 0.0) == "concede",

        # 2. differential attrition
        "the_closed_form_odds_ratio_matches_the_iteration":
            attrition["closed_form_max_error"] < 1e-9,
        "the_armed_share_rises_with_repression": all(
            attrition["rows"][i + 1]["armed_share"]
            > attrition["rows"][i]["armed_share"]
            for i in range(len(attrition["rows"]) - 1)),
        "total_capacity_falls_with_repression": all(
            attrition["rows"][i + 1]["total_capacity"]
            < attrition["rows"][i]["total_capacity"]
            for i in range(len(attrition["rows"]) - 1)),
        "indiscriminate_repression_leaves_the_composition_alone":
            abs(attrition["armed_share_indiscriminate_null"]
                - ARMED_SHARE_0) < 1e-12,
        "parity_arrives_where_the_closed_form_says":
            abs(_armed_share(1.0, attrition["periods_to_parity_full_repression"])
                - 0.5) < 1e-9,
        "nobody_converts_and_nobody_is_recruited":
            _armed_share(0.0, 0) == ARMED_SHARE_0
            and _armed_share(1.0, 0) == ARMED_SHARE_0,

        # 3. the coupling
        "escalation_raises_armed_capacity_before_it_destroys_it":
            at[0.61]["armed_capacity"] > at[0.0]["armed_capacity"]
            and at[1.0]["armed_capacity"] < at[0.61]["armed_capacity"],
        "escalation_always_costs_civilian_capacity": all(
            rows[i + 1]["civic_capacity"] < rows[i]["civic_capacity"]
            for i in range(len(rows) - 1)),
        "escalation_only_helps_removal_where_cooperation_is_hard_to_strip":
            coupling["strip_threshold"] is not None
            and all(r["strip"] <= coupling["strip_threshold"] for r in helped),
        "the_exact_boundary_lies_within_one_grid_step_of_the_grid_value":
            0.0 <= coupling["strip_threshold"] - coupling["strip_threshold_grid"]
            < coupling["strip_grid_step"]
            and _analyse(coupling["strip_threshold"], BASE)["removal_helped"]
            and not _analyse(coupling["strip_threshold"] + 1e-9, BASE)["removal_helped"],
        "the_three_optima_do_not_coincide":
            coupling["argmax_removal"] != coupling["argmax_accountable"],
        "durability_and_accountability_pull_against_each_other":
            coupling["argmax_durable"] == coupling["argmax_removal"]
            and coupling["argmax_durable"] != coupling["argmax_accountable"],
        "maximising_removal_costs_accountability":
            coupling["accountable_retained_share"] < 1.0,
        "the_ensemble_never_aligns_the_two":
            coupling["ensemble_diverged_share"] == 1.0,
        "the_ensemble_gain_in_removal_is_real_where_it_occurs":
            coupling["ensemble_median_removal_gain"] > 0.0,
        "probabilities_stay_in_the_unit_interval": all(
            0.0 <= r[k] <= 1.0 for r in rows
            for k in ("removal", "durable", "accountable", "loyalty",
                      "armed_share", "capacity")),
    }

    failed = [k for k, v in checks.items() if not v]
    if failed:
        raise AssertionError("invariants failed: " + ", ".join(failed))

    return _py({"seed": SEED, "choice": choice, "attrition": attrition,
                "coupling": coupling, "checks": checks})
