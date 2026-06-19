"""Data-efficiency charts: success rate vs. data-generation time.

Mirrors the R2R2R template (r2r2r_fig_no_bg.png): success rate (y, 0-100%) vs
data-generation time in hours (x), each marker annotated with its dataset size
(number of episodes).

Two series families:
  * Human teleoperation (our VLA data) — 1 min / episode.  Success rates pulled
    live from ../Evaluation Data/eval_data.py so they stay in sync with the
    HTML report.  Coffee shows 4x4 & 1x1 configs; pouring shows 5x3 & 1x1.
  * Our method (SAP) — generates 2000 episodes in 2 hours; success rate is a
    placeholder 60% until the real SAP eval lands.

Run:  PYTHONNOUSERSITE=1 python3 make_data_efficiency_charts.py   # -> PNG+PDF here

(The PYTHONNOUSERSITE=1 prefix forces the system NumPy 1.x, which the apt
matplotlib 3.5.1 was built against; the user-site NumPy 2.x otherwise breaks it.)
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "Evaluation Data"))
import eval_data as D                       # noqa: E402
from build_report import run_rate           # noqa: E402

POUR = ["WB", "O", "Bk", "R", "Br", "WC", "Gr", "P"]

# ---- timing model ---------------------------------------------------------
TELEOP_MIN_PER_EP = 1.0          # human teleoperation: 1 min / episode
SAP_EPS, SAP_HOURS = 2000, 2.0   # our method: 2000 eps in 2 h
SAP_PROJ_MAIN = 60.0             # projected success rate, main config (4x4 / 5x3)
SAP_PROJ_1X1 = 40.0              # projected success rate, 1x1 config (if not yet evaluated)


def hrs(n_eps):
    """Teleoperation wall-clock to collect n_eps episodes, in hours."""
    return n_eps * TELEOP_MIN_PER_EP / 60.0


def pct(run, scored=None):
    p, n = run_rate(run, scored)
    return 100.0 * p / n


# ---- colours (match the template's warm teleop / cool ours split) ---------
C_MAIN = "#E8883A"   # orange   — main teleop config (4x4 / 5x3)
C_ALT = "#2E9E5B"    # green    — secondary teleop config (1x1)
# our method (SAP) stars — one cool colour per config so they're distinguishable
C_SAP = "#1F3A93"        # navy    — our method, main config (4x4 / 5x3) SAP
C_SAP_MAIN = "#1F3A93"   # navy    — 4x4 / 5x3 SAP star
C_SAP_1X1 = "#B5179E"    # magenta — 1x1 SAP star
GRID = "#C9CCD3"


def lighten(hexcol, f=0.55):
    """Blend a hex colour toward white by fraction f (for faded projections)."""
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (int(c + (255 - c) * f) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def annotate(ax, x, y, label, color, xytext=(0, 11), ha="center"):
    """Episode-count label, lifted clear of the marker with a white backing so
    it is never obscured by a line."""
    ax.annotate(label, (x, y), textcoords="offset points", xytext=xytext,
                ha=ha, va="center", fontsize=8.5, color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none",
                          alpha=0.8), zorder=6)


def teleop_series(ax, sizes_rates, color, label):
    """sizes_rates: list of (n_episodes, success_pct).  Draws line+markers."""
    xs = [hrs(n) for n, _ in sizes_rates]
    ys = [r for _, r in sizes_rates]
    ax.plot(xs, ys, "-o", color=color, lw=2.4, ms=8, mec="white", mew=1.2,
            label=label, zorder=4)
    for (n, r), x in zip(sizes_rates, xs):
        annotate(ax, x, r, str(n), color)


def sap_points(ax, stars):
    """Plot one 'our method (SAP)' star per config.  `stars` is a list of
    (config_label, rate, done, colour) tuples — each config gets its own colour.
    All SAP runs generate SAP_EPS episodes in SAP_HOURS, so the stars share x; we
    nudge them apart slightly so both are visible.  Done evals are solid; not-yet-
    evaluated placeholders are faded."""
    # Every SAP run is 2000 eps / 2 h, so all stars sit exactly at x = SAP_HOURS.
    # Stars may overlap; done evals are solid, projections are faded.
    for cfg, rate, done, col in stars:
        ax.plot([SAP_HOURS], [rate], marker="*", ms=22 if done else 18, color=col,
                mec="white", mew=1.4, ls="none", alpha=1.0 if done else 0.5,
                zorder=5)
        tag = f"{cfg}" + ("" if done else " (proj.)")
        annotate(ax, SAP_HOURS, rate, tag, col if done else lighten(col, 0.3),
                 xytext=(0, 14))


def style(ax, title):
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel("Data Generation Time (Hours)", fontsize=11)
    ax.set_ylabel("Success Rate", fontsize=11)
    ax.set_ylim(0, 100)
    ax.set_xlim(0, 2.8)
    ax.set_yticks(range(0, 101, 20))
    ax.set_yticklabels([f"{v}%" for v in range(0, 101, 20)])
    ax.grid(True, ls="--", lw=0.7, color=GRID, alpha=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def legend(ax, teleop_labels, stars):
    handles = [
        Line2D([], [], color=C_MAIN, marker="o", lw=2.4, ms=8, mec="white",
               label=teleop_labels[0]),
        Line2D([], [], color=C_ALT, marker="o", lw=2.4, ms=8, mec="white",
               label=teleop_labels[1]),
    ]
    # one star entry per config, coloured to match the plotted star, with a
    # done/projected suffix so the colour + state are both explained.
    for cfg, _rate, done, col in stars:
        suffix = f"done ({SAP_HOURS:g} h)" if done else "projected"
        handles.append(
            Line2D([], [], color=col, marker="*", ls="none", ms=15, mec="white",
                   alpha=1.0 if done else 0.45,
                   label=f"Our method — {cfg} · {suffix}"))
    ax.legend(handles=handles, loc="upper left", fontsize=9, frameon=True,
              framealpha=0.95, title="SAP: 2000 eps / 2 h  ·  teleop label = # eps",
              title_fontsize=8.5)


def make_chart(title, teleop_main, teleop_alt, labels, out, stars):
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    teleop_series(ax, teleop_main, C_MAIN, labels[0])
    teleop_series(ax, teleop_alt, C_ALT, labels[1])
    sap_points(ax, stars)
    style(ax, title)
    legend(ax, labels, stars)
    sap_note = "SAP stars — " + ", ".join(
        f"{cfg.replace(' SAP', '')} {rate:.0f}% "
        f"({'measured' if done else 'projected'})"
        for cfg, rate, done, _col in stars)
    note = (f"Human teleoperation: {TELEOP_MIN_PER_EP:g} min/episode  ·  "
            "VLA success rates from the evaluation report  ·  " + sap_note)
    fig.text(0.5, -0.02, note, ha="center", fontsize=7.5, color="#666")
    fig.tight_layout()
    path = os.path.join(HERE, out)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    fig.savefig(path.replace(".png", ".pdf"), bbox_inches="tight")
    plt.close(fig)
    print("wrote", out, "and", out.replace(".png", ".pdf"))


def main():
    # ---- Coffee Machine: 4x4 & 1x1 ----
    coffee_4x4 = [(50, pct(D.coffee_4x4_vla_50)),
                  (100, pct(D.coffee_4x4_vla_100)),
                  (150, pct(D.coffee_4x4_vla))]
    coffee_1x1 = [(50, pct(D.coffee_1x1_vla_50)),
                  (100, pct(D.coffee_1x1_vla_100)),
                  (150, pct(D.coffee_1x1_vla))]
    # Two SAP stars per chart (main config + 1x1), colour-coded by config;
    # neither coffee eval is done yet.
    make_chart("Coffee Machine — Data Efficiency",
               coffee_4x4, coffee_1x1,
               ("Human teleop — 4×4 VLA", "Human teleop — 1×1 VLA"),
               "coffee_data_efficiency.png",
               stars=[("4×4 SAP", SAP_PROJ_MAIN, False, C_SAP_MAIN),
                      ("1×1 SAP", SAP_PROJ_1X1, False, C_SAP_1X1)])

    # ---- Pouring: 5x3 & 1x1 (1x1 now has @50/@100/@150 partial evals) ----
    pour_5x3 = [(50, pct(D.pouring_5x3_vla_50, POUR)),
                (105, pct(D.pouring_4x4_vla, POUR)),
                (150, pct(D.pouring_5x3_vla_150, POUR))]
    pour_1x1 = [(50, pct(D.pouring_1x1_vla_50, POUR)),
                (100, pct(D.pouring_1x1_vla_100, POUR)),
                (150, pct(D.pouring_1x1_vla_150, POUR))]
    # 1x1 pouring SAP eval is DONE — use the measured rate from the 1x1 SAP grid
    # (pouring_5x3_sap, the "1x1 X-ARM-SAP" sheet); 5x3 SAP star is a projection.
    pour_1x1_sap = pct(D.pouring_5x3_sap, POUR)
    make_chart("Pouring Task — Data Efficiency",
               pour_5x3, pour_1x1,
               ("Human teleop — 5×3 VLA", "Human teleop — 1×1 VLA"),
               "pouring_data_efficiency.png",
               stars=[("5×3 SAP", SAP_PROJ_MAIN, False, C_SAP_MAIN),
                      ("1×1 SAP", pour_1x1_sap, True, C_SAP_1X1)])


if __name__ == "__main__":
    main()
