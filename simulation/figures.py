"""Figures for *Concession and Succession*."""
from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

INK, GRID = "#1a1a1a", "#d9d9d9"
AMBER, GREEN, BLUE, GRAY, RED = "#b45309", "#15803d", "#2563eb", "#57534e", "#b3202c"


def _style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=8.5)
    ax.set_axisbelow(True)
    ax.grid(True, color=GRID, lw=0.6)


def plot_choice(res, path):
    """What the incumbent finds cheapest, and what survives repression."""
    C, A = res["choice"], res["attrition"]
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.7))
    cmap = ListedColormap([GREEN, RED, GRAY])   # concede, repress, wait
    lev, loy = C["leverage_grid"], C["loyalty_grid"]
    extent = [lev[0], lev[-1], loy[0], loy[-1]]

    for ax, key, title in (
            (axes[0], "high", "a. the choice, campaign in full view"),
            (axes[1], "escalated", "b. the same, after escalation")):
        ax.imshow(np.array(C["fields"][key]), origin="lower", aspect="auto",
                  extent=extent, cmap=cmap, vmin=0, vmax=2, interpolation="nearest")
        ax.set_xlabel("material leverage withdrawn", fontsize=8.5)
        ax.set_title(title, fontsize=9.5, color=INK, loc="left")
        ax.tick_params(colors=INK, labelsize=8.5)
    axes[0].set_ylabel("cooperation the apparatus still extends", fontsize=8.5)
    axes[0].legend(handles=[Patch(facecolor=GREEN, label="concede"),
                            Patch(facecolor=RED, label="repress"),
                            Patch(facecolor=GRAY, label="wait")],
                   loc="lower left", fontsize=8, frameon=True, framealpha=0.92,
                   facecolor="white", edgecolor="none")
    axes[1].text(0.04, 0.93,
                 f"concession region\n{C['share_concede_high_attention']:.3f}"
                 f" → {C['share_concede_escalated']:.3f}",
                 transform=axes[1].transAxes, fontsize=8.2, color=INK, va="top")

    ax = axes[2]
    _style(ax)
    rep = [r["repression"] for r in A["rows"]]
    ax.plot(rep, [r["armed_share"] for r in A["rows"]], color=RED, lw=1.8,
            label="armed share of what survives")
    ax.plot(rep, [r["total_capacity"] for r in A["rows"]], color=BLUE, lw=1.8,
            label="capacity still standing")
    ax.axhline(A["armed_share_initial"], color=INK, lw=0.9, ls=":")
    ax.text(0.02, A["armed_share_initial"] + 0.02, "armed share at the outset",
            fontsize=8, color=INK)
    ax.set_xlabel("repression intensity", fontsize=8.5)
    ax.set_ylabel(f"fraction, after {A['periods']} periods", fontsize=8.5)
    ax.set_ylim(0, 1.0)
    ax.set_title("c. attrition changes the campaign without changing anyone's mind",
                 fontsize=9.5, color=INK, loc="left")
    ax.legend(fontsize=8, frameon=False, loc="upper left")

    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_divergence(res, path):
    """Three outcomes, three maxima, and the ensemble that tests them."""
    K = res["coupling"]
    rows, prof = K["rows"], K["profile"]
    esc = [r["escalation"] for r in rows]
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.7))

    ax = axes[0]
    _style(ax)
    ax.plot(esc, [r["removal"] for r in rows], color=RED, lw=1.8,
            label="incumbent removed")
    ax.plot(esc, [r["removal_and_durable"] for r in rows], color=AMBER, lw=1.8,
            label="removed and the successor survives")
    ax.plot(esc, [r["removal_and_accountable"] for r in rows], color=GREEN, lw=1.8,
            label="removed and the successor is accountable")
    for x, color in ((K["argmax_removal"], RED), (K["argmax_accountable"], GREEN)):
        ax.axvline(x, color=color, lw=0.9, ls="--")
    ax.set_xlabel("escalation", fontsize=8.5)
    ax.set_ylabel("probability", fontsize=8.5)
    ax.set_title("a. the three outcomes do not peak together", fontsize=9.5,
                 color=INK, loc="left")
    ax.legend(fontsize=7.6, frameon=True, framealpha=0.92, facecolor="white",
              edgecolor="none", loc="center right")
    ax.text(K["argmax_removal"] + 0.02, 0.008,
            f"removal peaks at {K['argmax_removal']:.2f}", fontsize=7.8, color=RED)
    ax.text(K["argmax_accountable"] + 0.02, 0.008,
            "accountable succession\npeaks here", fontsize=7.8, color=GREEN)

    ax = axes[1]
    _style(ax)
    strip = [r["strip"] for r in prof]
    ax.plot(strip, [r["argmax_removal"] for r in prof], color=RED, lw=1.8,
            label="escalation that maximises removal")
    ax.plot(strip, [r["argmax_accountable"] for r in prof], color=GREEN, lw=1.8,
            label="escalation that maximises accountable succession")
    ax.axvline(K["strip_threshold"], color=INK, lw=0.9, ls=":")
    ax.axvline(K["focal_strip"], color=AMBER, lw=0.9, ls="--")
    ax.text(K["strip_threshold"] + 0.002, 0.86,
            f"escalation stops helping\nabove {K['strip_threshold']:.4f}",
            fontsize=7.8, color=INK)
    ax.text(K["focal_strip"] + 0.002, 0.30,
            f"escalation's best case,\nat {K['focal_strip']:.4f}",
            fontsize=7.8, color=AMBER)
    ax.set_xlim(0, 0.12)
    ax.set_xlabel("cooperation an intact civilian campaign can strip", fontsize=8.5)
    ax.set_ylabel("escalation at the optimum", fontsize=8.5)
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("b. escalation helps removal only in a narrow corner", fontsize=9.5,
                 color=INK, loc="left")
    ax.legend(fontsize=7.5, frameon=True, framealpha=0.92, facecolor="white",
              edgecolor="none", loc="center right")

    ax = axes[2]
    _style(ax)
    ax.bar([0, 1], [1.0, K["accountable_retained_share"]], width=0.55,
           color=[GREEN, AMBER])
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["escalate for\naccountability", "escalate for\nremoval"],
                       fontsize=8.4)
    ax.set_ylabel("accountable succession, relative to its own best", fontsize=8.5)
    ax.set_ylim(0, 1.5)
    ax.text(1, K["accountable_retained_share"] + 0.04,
            f"{K['accountable_retained_share']:.3f}", ha="center", fontsize=8.4,
            color=INK)
    ax.text(0, 1.04, "1.000", ha="center", fontsize=8.4, color=INK)
    ax.text(0.5, 0.985,
            f"in all {K['ensemble_diverged']} of {K['ensemble_helped']} parameter draws where\n"
            f"escalation raised the chance of removal,\nit lowered this; the best case retained "
            f"{K['ensemble_max_retained']:.3f}",
            transform=ax.transAxes, ha="center", fontsize=7.8, color=INK, va="top",
            bbox=dict(facecolor="white", edgecolor=GRID, linewidth=0.6, pad=3.2))
    ax.set_title("c. the price of the removal optimum", fontsize=9.5, color=INK,
                 loc="left")

    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
