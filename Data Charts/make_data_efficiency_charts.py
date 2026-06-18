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
SAP_EPS, SAP_HOURS, SAP_RATE = 2000, 2.0, 60.0   # our method: 2000 eps in 2 h


def hrs(n_eps):
    """Teleoperation wall-clock to collect n_eps episodes, in hours."""
    return n_eps * TELEOP_MIN_PER_EP / 60.0


def pct(run, scored=None):
    p, n = run_rate(run, scored)
    return 100.0 * p / n


# ---- colours (match the template's warm teleop / cool ours split) ---------
C_MAIN = "#E8883A"   # orange   — main teleop config (4x4 / 5x3)
C_ALT = "#C9952F"    # gold     — secondary teleop config (1x1)
C_SAP = "#1F3A93"    # navy     — our method (SAP), plays the R2R2R role
GRID = "#C9CCD3"


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


def sap_point(ax):
    ax.plot([SAP_HOURS], [SAP_RATE], marker="*", ms=20, color=C_SAP,
            mec="white", mew=1.3, ls="none", label="Our method — SAP", zorder=5)
    annotate(ax, SAP_HOURS, SAP_RATE, f"{SAP_EPS}", C_SAP, xytext=(0, 15))


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


def legend(ax, teleop_labels):
    handles = [
        Line2D([], [], color=C_MAIN, marker="o", lw=2.4, ms=8, mec="white",
               label=teleop_labels[0]),
        Line2D([], [], color=C_ALT, marker="o", lw=2.4, ms=8, mec="white",
               label=teleop_labels[1]),
        Line2D([], [], color=C_SAP, marker="*", ls="none", ms=15, mec="white",
               label=f"Our method — SAP (2000 eps / {SAP_HOURS:g} h)"),
    ]
    ax.legend(handles=handles, loc="upper left", fontsize=9, frameon=True,
              framealpha=0.95, title="Marker label = # episodes",
              title_fontsize=8.5)


def make_chart(title, teleop_main, teleop_alt, labels, out):
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    teleop_series(ax, teleop_main, C_MAIN, labels[0])
    teleop_series(ax, teleop_alt, C_ALT, labels[1])
    sap_point(ax)
    style(ax, title)
    legend(ax, labels)
    note = (f"Human teleoperation: {TELEOP_MIN_PER_EP:g} min/episode  ·  "
            "VLA success rates from the evaluation report  ·  "
            "SAP success rate is a 60% placeholder")
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
    make_chart("Coffee Machine — Data Efficiency",
               coffee_4x4, coffee_1x1,
               ("Human teleop — 4×4 VLA", "Human teleop — 1×1 VLA"),
               "coffee_data_efficiency.png")

    # ---- Pouring: 5x3 & 1x1 (1x1 has only the @150 partial eval) ----
    pour_5x3 = [(50, pct(D.pouring_5x3_vla_50, POUR)),
                (105, pct(D.pouring_4x4_vla, POUR)),
                (150, pct(D.pouring_5x3_vla_150, POUR))]
    pour_1x1 = [(150, pct(D.pouring_1x1_vla_150, POUR))]
    make_chart("Pouring Task — Data Efficiency",
               pour_5x3, pour_1x1,
               ("Human teleop — 5×3 VLA", "Human teleop — 1×1 VLA"),
               "pouring_data_efficiency.png")


if __name__ == "__main__":
    main()
