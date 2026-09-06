"""Reproduce every number and both figures.

    cd simulation && uv run run_all.py
"""
from __future__ import annotations

import json
from pathlib import Path

from analyses import run

OUT = Path(__file__).parent / "output"


def main() -> None:
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    results = run()
    (OUT / "results.json").write_text(json.dumps(results, indent=2))

    from figures import plot_choice, plot_divergence
    plot_choice(results, str(OUT / "figures" / "choice.png"))
    plot_divergence(results, str(OUT / "figures" / "divergence.png"))

    C, A, K = results["choice"], results["attrition"], results["coupling"]
    print("the incumbent's choice:")
    print(f"  {C['grid_cells']} cells; attention moves {C['wait_to_repress']} waiting "
          f"cells to repression and {C['wait_to_concede']} to concession, "
          f"a ratio of {C['urgency_ratio']:.3f}")
    print(f"  concession region {C['share_concede_low_attention']:.3f} → "
          f"{C['share_concede_high_attention']:.3f} with attention, then "
          f"{C['share_concede_escalated']:.3f} after escalation")
    print(f"  cooperation a ruler can still command and concede: "
          f"{C['crossing_at_zero_leverage']:.3f} at zero leverage, "
          f"{C['crossing_at_full_leverage']:.3f} at full leverage")
    print("differential attrition:")
    print(f"  closed form matches iteration to "
          f"{A['closed_form_max_error']:.2e}")
    print(f"  armed share {A['armed_share_initial']:.2f} → "
          f"{A['armed_share_full_repression']:.3f} after {A['periods']} periods of "
          f"maximal repression, with {A['capacity_full_repression']:.3f} of the "
          f"campaign left")
    print(f"  parity at {A['periods_to_parity_full_repression']:.2f} periods; "
          f"indiscriminate repression leaves the share at "
          f"{A['armed_share_indiscriminate_null']:.2f}")
    print("the coupling:")
    print(f"  escalation raises the chance of removal only where an intact civilian "
          f"campaign could strip at most {K['strip_threshold']:.3f} of the "
          f"apparatus's cooperation")
    print(f"  there, removal peaks at escalation {K['argmax_removal']:.2f} and "
          f"accountable succession at {K['argmax_accountable']:.2f}")
    print(f"  taking the removal optimum buys "
          f"{K['removal_gain_from_escalating']:.4f} of removal probability and "
          f"retains {K['accountable_retained_share']:.3f} of accountable succession")
    print(f"  ensemble: escalation helped in {K['ensemble_helped']} of "
          f"{K['ensemble_draws']} draws; in "
          f"{K['ensemble_diverged']} of those it cost accountability, best case "
          f"{K['ensemble_max_retained']:.3f}")
    print("checks:", f"{sum(results['checks'].values())}/{len(results['checks'])}")
    print("wrote", OUT / "results.json")


if __name__ == "__main__":
    main()
