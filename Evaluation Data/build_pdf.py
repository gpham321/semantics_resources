"""Render the evaluation tables to a PDF you can open and review.

    python3 build_pdf.py            # -> tables.pdf
    python3 build_pdf.py --open     # also open it (xdg-open/open/start)

Pipeline:
  1. (re)generate tables.tex from eval_data.py via build_latex.py
  2. compile tables.tex -> tables.pdf with pdflatex (run twice)
  3. if pdflatex is unavailable or fails, fall back to a matplotlib renderer
     that draws the same tables into a multi-page tables.pdf.

Everything is driven by eval_data.py, so re-running after editing the data
re-evaluates and re-renders the tables.
"""
import os
import shutil
import subprocess
import sys

import eval_data as D
from build_report import rate, grid_cells
from build_latex import build_latex, POUR_SCORED, COND_LABELS, pct

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = "tables.tex"
PDF = "tables.pdf"


# --------------------------------------------------------------------------- #
# 1+2: LaTeX path
# --------------------------------------------------------------------------- #
def compile_with_pdflatex():
    exe = shutil.which("pdflatex")
    if not exe:
        return False
    build_latex()  # refresh tables.tex
    log_tail = ""
    for _ in range(2):  # twice so floats/refs settle
        proc = subprocess.run(
            [exe, "-interaction=nonstopmode", "-halt-on-error", TEX],
            cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        log_tail = proc.stdout[-2500:]
        if proc.returncode != 0:
            print(log_tail)
            print("\n[pdflatex] compile failed — falling back to matplotlib.")
            return False
    # tidy aux files
    for ext in (".aux", ".log", ".out"):
        f = os.path.join(HERE, "tables" + ext)
        if os.path.exists(f):
            os.remove(f)
    return os.path.exists(os.path.join(HERE, PDF))


# --------------------------------------------------------------------------- #
# 3: matplotlib fallback
# --------------------------------------------------------------------------- #
PASS_BG, FAIL_BG, BLANK_BG = "#E4F4E9", "#FBE6E5", "#F2F2F4"
SHADES = [(0.8, "#D4EFD9"), (0.6, "#E6F0CC"), (0.4, "#F6EFCC"),
          (0.2, "#F8E2CE"), (0.0, "#F6D8D5")]


def shade_color(p, n):
    if not n:
        return BLANK_BG
    r = p / n
    for thr, col in SHADES:
        if r >= thr:
            return col
    return SHADES[-1][1]


def cell_text(cell):
    if cell is None:
        return "–", BLANK_BG
    res, grasp, notes = cell
    mark = "✓" if res == "P" else "✗"
    extra = []
    if grasp in ("S", "T"):
        extra.append(grasp)
    if notes:
        extra.append(",".join(str(x) for x in notes))
    if extra:
        mark += " " + " ".join(extra)
    return mark, (PASS_BG if res == "P" else FAIL_BG)


def _draw_table(pdf, title, col_labels, row_labels, cells, cell_colors,
                col_w=None):
    import matplotlib.pyplot as plt
    ncol = len(col_labels)
    fig_w = min(16, 2.2 + 1.5 * ncol)
    fig_h = min(10, 1.2 + 0.5 * (len(row_labels) + 1))
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis("off")
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left", pad=12)
    tbl = ax.table(cellText=cells, rowLabels=row_labels, colLabels=col_labels,
                   cellColours=cell_colors, loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.5)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#cccccc")
        if r == 0 or c == -1:
            cell.set_text_props(fontweight="bold")
            cell.set_facecolor("#EEF1F6")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def _grid_pages(pdf, run, cols_id, cols_od, rows_id, rows_od, col_names,
                row_names, label_prefix, task_idx, scored=None):
    for cond in ("id_id", "id_od", "od_id", "od_od"):
        if cond not in run:
            continue
        cols = cols_id if cond.startswith("id") else cols_od
        rows = rows_id if cond.endswith("id") else rows_od
        p, n = rate(grid_cells(run[cond], scored))
        cells, colors = [], []
        for r_ in rows:
            trow, crow = [], []
            for c in cols:
                t, col = cell_text(run[cond][r_].get(c))
                trow.append(t)
                crow.append(col)
            cells.append(trow)
            colors.append(crow)
        title = (f"{label_prefix} — {COND_LABELS[cond][task_idx]} "
                 f"({p}/{n} = {pct(p,n).replace(chr(92)+'%','%')})")
        _draw_table(pdf, title, [col_names[c] for c in cols],
                    [row_names[r_] for r_ in rows], cells, colors)


def render_with_matplotlib():
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib.backends.backend_pdf import PdfPages

    out = os.path.join(HERE, PDF)
    with PdfPages(out) as pdf:
        # summary
        conds = ["id_id", "id_od", "od_id", "od_od"]
        runs = [("Coffee 4×4 VLA @150", D.coffee_4x4_vla, None),
                ("Coffee 4×4 VLA @100", D.coffee_4x4_vla_100, None),
                ("Coffee 4×4 VLA @50", D.coffee_4x4_vla_50, None),
                ("Coffee 1×1 VLA @150", D.coffee_1x1_vla, None),
                ("Coffee 1×1 VLA @100", D.coffee_1x1_vla_100, None),
                ("Coffee 1×1 VLA @50", D.coffee_1x1_vla_50, None),
                ("Pouring 5×3 VLA @150", D.pouring_5x3_vla_150, POUR_SCORED),
                ("Pouring 5×3 VLA @105", D.pouring_4x4_vla, POUR_SCORED),
                ("Pouring 5×3 VLA @50", D.pouring_5x3_vla_50, POUR_SCORED),
                ("Pouring 1×1 VLA @50 (partial)", D.pouring_1x1_vla_50, POUR_SCORED),
                ("Pouring 1×1 VLA @100 (partial)", D.pouring_1x1_vla_100, POUR_SCORED),
                ("Pouring 1×1 VLA @150 (partial)", D.pouring_1x1_vla_150, POUR_SCORED),
                ("Pouring 1×1 SAP", D.pouring_5x3_sap, POUR_SCORED)]
        cells, colors = [], []
        for name, run, sc in runs:
            trow, crow = [], []
            tp = tn = 0
            for c in conds:
                p, n = rate(grid_cells(run[c], sc)) if c in run else (0, 0)
                tp += p
                tn += n
                trow.append(f"{pct(p,n).replace(chr(92)+'%','%')}\n{p}/{n}")
                crow.append(shade_color(p, n))
            trow.append(f"{pct(tp,tn).replace(chr(92)+'%','%')}\n{tp}/{tn}")
            crow.append(shade_color(tp, tn))
            cells.append(trow)
            colors.append(crow)
        _draw_table(pdf, "Summary — success rate by condition (VLA + SAP baseline)",
                    ["ID/ID", "ID/OOD", "OOD/ID", "OOD/OOD", "Overall"],
                    [r[0] for r in runs], cells, colors)

        # training runs
        tcells, tcolors = [], []
        for _m, ds, size, train, comp, done, evs, xarm in D.TRAIN_RUNS:
            tcells.append([ds, str(size), train or "–", comp or "–",
                           done or "–", evs or "–", "✓" if xarm else "–"])
            base = "#E7F3EA" if evs in ("Yes", "In Progress") else "#FFFFFF"
            tcolors.append([base] * 7)
        _draw_table(pdf, "Training runs & dataset sizes (Model Train Baselines)",
                    ["Dataset", "Size", "Train", "Computer", "Started", "Eval", "xArm"],
                    [""] * len(tcells), tcells, tcolors)

        # our-method (SAP) training runs (underlined + Yes/No eval rows only)
        omcells, omcolors = [], []
        for model, ds, size, status, comp, started, evs in D.OUR_METHOD_TRAINS:
            omcells.append([model, ds, str(size), status or "–", comp or "–",
                            started or "–", evs or "–"])
            base = "#E7F3EA" if evs in ("Yes", "In Progress") else "#FFFFFF"
            omcolors.append([base] * 7)
        _draw_table(pdf, "Our-method (SAP) training runs (Our Method Train)",
                    ["Model", "Dataset", "Size", "Status", "Computer", "Started", "Eval"],
                    [""] * len(omcells), omcells, omcolors)

        # coffee — 150-demo, 100-demo, then 50-demo
        _grid_pages(pdf, D.coffee_4x4_vla, D.CUPS_ID, D.CUPS_OOD, D.MACH_ID,
                    D.MACH_OOD, D.CUP_NAMES, D.MACH_NAMES, "Coffee 4×4 VLA @150 demos", 0)
        _grid_pages(pdf, D.coffee_1x1_vla, D.CUPS_ID, D.CUPS_OOD, D.MACH_ID,
                    D.MACH_OOD, D.CUP_NAMES, D.MACH_NAMES, "Coffee 1×1 VLA @150 demos", 0)
        _grid_pages(pdf, D.coffee_4x4_vla_100, D.CUPS_ID, D.CUPS_OOD, D.MACH_ID,
                    D.MACH_OOD, D.CUP_NAMES, D.MACH_NAMES, "Coffee 4×4 VLA @100 demos", 0)
        _grid_pages(pdf, D.coffee_1x1_vla_100, D.CUPS_ID, D.CUPS_OOD, D.MACH_ID,
                    D.MACH_OOD, D.CUP_NAMES, D.MACH_NAMES, "Coffee 1×1 VLA @100 demos", 0)
        _grid_pages(pdf, D.coffee_4x4_vla_50, D.CUPS_ID, D.CUPS_OOD, D.MACH_ID,
                    D.MACH_OOD, D.CUP_NAMES, D.MACH_NAMES, "Coffee 4×4 VLA @50 demos", 0)
        _grid_pages(pdf, D.coffee_1x1_vla_50, D.CUPS_ID, D.CUPS_OOD, D.MACH_ID,
                    D.MACH_OOD, D.CUP_NAMES, D.MACH_NAMES, "Coffee 1×1 VLA @50 demos", 0)
        # pouring — 150, 105, 50, then SAP baseline
        pour_names = {**D.CUP_NAMES, "TWC": "Tall W.C.*"}
        _grid_pages(pdf, D.pouring_5x3_vla_150, D.POUR_CUPS_ID, D.POUR_CUPS_OOD,
                    D.BOWLS_ID, D.BOWLS_OOD, pour_names, D.BOWL_NAMES,
                    "Pouring 5×3 VLA @150 demos", 1, scored=POUR_SCORED)
        _grid_pages(pdf, D.pouring_4x4_vla, D.POUR_CUPS_ID, D.POUR_CUPS_OOD,
                    D.BOWLS_ID, D.BOWLS_OOD, pour_names, D.BOWL_NAMES,
                    "Pouring 5×3 VLA @105 demos", 1, scored=POUR_SCORED)
        _grid_pages(pdf, D.pouring_5x3_vla_50, D.POUR_CUPS_ID, D.POUR_CUPS_OOD,
                    D.BOWLS_ID, D.BOWLS_OOD, pour_names, D.BOWL_NAMES,
                    "Pouring 5×3 VLA @50 demos", 1, scored=POUR_SCORED)
        _grid_pages(pdf, D.pouring_1x1_vla_50, D.POUR_CUPS_ID, D.POUR_CUPS_OOD,
                    D.BOWLS_ID, D.BOWLS_OOD, pour_names, D.BOWL_NAMES,
                    "Pouring 1×1 VLA @50 demos (partial)", 1, scored=POUR_SCORED)
        _grid_pages(pdf, D.pouring_1x1_vla_100, D.POUR_CUPS_ID, D.POUR_CUPS_OOD,
                    D.BOWLS_ID, D.BOWLS_OOD, pour_names, D.BOWL_NAMES,
                    "Pouring 1×1 VLA @100 demos (partial)", 1, scored=POUR_SCORED)
        _grid_pages(pdf, D.pouring_1x1_vla_150, D.POUR_CUPS_ID, D.POUR_CUPS_OOD,
                    D.BOWLS_ID, D.BOWLS_OOD, pour_names, D.BOWL_NAMES,
                    "Pouring 1×1 VLA @150 demos (partial)", 1, scored=POUR_SCORED)
        _grid_pages(pdf, D.pouring_5x3_sap, D.POUR_CUPS_ID, D.POUR_CUPS_OOD,
                    D.BOWLS_ID, D.BOWLS_OOD, pour_names, D.BOWL_NAMES,
                    "Pouring 1×1 SAP baseline", 1, scored=POUR_SCORED)
        # mug tree
        for which, lbl in (("id_cup", "ID cups"), ("od_cup", "OOD cups")):
            cells, colors, rl = [], [], []
            for cup, trs in D.mugtree_5x1_vla[which].items():
                p, n = rate(trs)
                if which == "od_cup" and n == 0:
                    continue
                trow, crow = [], []
                for c in trs:
                    t, col = cell_text(c)
                    trow.append(t)
                    crow.append(col)
                trow.append(f"{pct(p,n).replace(chr(92)+'%','%') if n else '–'}")
                crow.append(shade_color(p, n))
                cells.append(trow)
                colors.append(crow)
                rl.append(D.CUP_NAMES[cup] + ("*" if cup == "TWC" else ""))
            _draw_table(pdf, f"Mug Tree 5×1 VLA @150 demos — {lbl}",
                        ["1", "2", "3", "4", "5", "Rate"], rl, cells, colors)
    return os.path.exists(out)


# --------------------------------------------------------------------------- #
def maybe_open(path):
    opener = ("open" if sys.platform == "darwin"
              else "start" if os.name == "nt" else "xdg-open")
    try:
        subprocess.Popen([opener, path])
    except Exception as e:  # noqa: BLE001
        print(f"(could not auto-open: {e})")


def main():
    used = "pdflatex"
    if not compile_with_pdflatex():
        used = "matplotlib"
        try:
            ok = render_with_matplotlib()
        except ImportError:
            sys.exit("Neither pdflatex nor matplotlib is available — cannot build PDF.")
        if not ok:
            sys.exit("PDF rendering failed.")
    path = os.path.join(HERE, PDF)
    print(f"wrote {PDF}  (via {used})")
    if "--open" in sys.argv:
        maybe_open(path)


if __name__ == "__main__":
    main()
