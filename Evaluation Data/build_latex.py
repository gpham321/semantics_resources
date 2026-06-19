"""Emit `tables.tex` — clean, copy-paste-ready LaTeX tables for the paper.

Single source of truth is `eval_data.py`.  Run directly to (re)write tables.tex:

    python3 build_latex.py

Design choices that keep it tidy:
  * short object codes (WB, O, K, ...) as column/row headers -> narrow,
    equal-width columns, no wrapping; a compact code key sits in the intro;
  * coloured check / cross marks instead of full-cell background fills;
  * fixed equal-width data columns via a `C{}` column type;
  * every table in its own ``\\begin{table}`` block, delimited by a
    ``% ==== name ====`` comment, so you can lift just the ones you need.

Cells show the mark plus a small grey superscript = grasp (S/T) and note #s.
"""
import eval_data as D
from build_report import rate, grid_cells, notes_str  # noqa: F401

OUT = "tables.tex"

COND_LABELS = {
    "id_id": ("ID Cup / ID Machine", "ID Cup / ID Bowl"),
    "id_od": ("ID Cup / OOD Machine", "ID Cup / OOD Bowl"),
    "od_id": ("OOD Cup / ID Machine", "OOD Cup / ID Bowl"),
    "od_od": ("OOD Cup / OOD Machine", "OOD Cup / OOD Bowl"),
}
POUR_SCORED = ["WB", "O", "Bk", "R", "Br", "WC", "Gr", "P"]

# fixed column widths (keep every data column equal within a table)
W_GRID = "1.15cm"     # coffee / pouring data columns
W_GRIDLBL = "1.5cm"   # coffee / pouring row-label column
W_TRIAL = "0.92cm"    # mug-tree trial columns
W_RATE = "1.5cm"      # mug-tree rate column
W_MUGLBL = "1.5cm"
W_SUM = "2.15cm"      # summary data columns
W_SUMLBL = "3.6cm"


# --------------------------------------------------------------------------- #
def esc(s):
    s = str(s)
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
                 ("}", r"\}"), ("~", r"\textasciitilde{}"),
                 ("^", r"\textasciicircum{}")):
        s = s.replace(a, b)
    return s


def note_sup(cell):
    """Small grey superscript: grasp then note numbers (or empty)."""
    _, grasp, notes = cell
    bits = []
    if grasp in ("S", "T"):
        bits.append(grasp)
    if notes:
        bits.append(esc(notes_str(notes)))
    return r"\nt{" + r"\,".join(bits) + "}" if bits else ""


def tex_cell(cell):
    if cell is None:
        return r"\bl"
    return (r"\pass" if cell[0] == "P" else r"\fail") + note_sup(cell)


def pct(p, n):
    return f"{100*p/n:.0f}\\%" if n else "--"


def shade(p, n):
    if not n:
        return "shadeN"
    r = p / n
    return ("shadeD" if r >= .8 else "shadeC" if r >= .6 else
            "shadeB" if r >= .4 else "shadeA" if r >= .2 else "shade0")


# --------------------------------------------------------------------------- #
# grid table (coffee / pouring condition block) — headers are short codes
# --------------------------------------------------------------------------- #
def grid_table(grid, cols, rows, corner, label, p, n):
    colspec = ">{\\raggedright\\arraybackslash}p{%s}%s" % (
        W_GRIDLBL, ("C{%s}" % W_GRID) * len(cols))
    out = [r"\begin{table}[ht]\centering\small",
           r"\renewcommand{\arraystretch}{1.18}",
           f"\\caption{{{esc(label)} \\,({p}/{n}, {pct(p,n)}).}}",
           r"\begin{tabular}{%s}" % colspec, r"\toprule",
           r"\textbf{%s} & %s \\" % (esc(corner),
                                     " & ".join(r"\textbf{%s}" % esc(c) for c in cols)),
           r"\midrule"]
    for r_ in rows:
        out.append(r"\textbf{%s} & %s \\"
                   % (esc(r_), " & ".join(tex_cell(grid[r_][c]) for c in cols)))
    out += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    return "\n".join(out)


def coffee_block(run, prefix):
    out = []
    for cond in ("id_id", "id_od", "od_id", "od_od"):
        if cond not in run:
            continue
        cols = D.CUPS_ID if cond.startswith("id") else D.CUPS_OOD
        rows = D.MACH_ID if cond.endswith("id") else D.MACH_OOD
        p, n = rate(grid_cells(run[cond]))
        lab = f"{prefix} --- {COND_LABELS[cond][0]}"
        out.append(f"% ==== {lab} ====")
        out.append(grid_table(run[cond], cols, rows, "Machine", lab, p, n))
    return "\n".join(out)


def pouring_block(run, prefix):
    out = []
    for cond in ("id_id", "id_od", "od_id", "od_od"):
        cols = D.POUR_CUPS_ID if cond.startswith("id") else D.POUR_CUPS_OOD
        rows = D.BOWLS_ID if cond.endswith("id") else D.BOWLS_OOD
        p, n = rate(grid_cells(run[cond], POUR_SCORED))
        lab = f"{prefix} --- {COND_LABELS[cond][1]}"
        out.append(f"% ==== {lab} ====")
        out.append(grid_table(run[cond], cols, rows, "Bowl", lab, p, n))
    return "\n".join(out)


# --------------------------------------------------------------------------- #
def summary_table(runs):
    conds = ["id_id", "id_od", "od_id", "od_od"]
    head = ["Run", "ID/ID", "ID/OOD", "OOD/ID", "OOD/OOD", "Overall"]
    colspec = ">{\\raggedright\\arraybackslash}p{%s}%s" % (W_SUMLBL, ("C{%s}" % W_SUM) * 5)
    out = ["% ==== Summary: success rate by condition ====",
           r"\begin{table}[ht]\centering\small",
           r"\renewcommand{\arraystretch}{1.25}",
           r"\caption{Success rate by condition. Coffee shown at 50/100/150 and "
           r"pouring at 50/105/150 demos to expose dataset-size scaling; SAP is a "
           r"secondary baseline on the pouring task.}",
           r"\begin{tabular}{%s}" % colspec, r"\toprule",
           " & ".join(r"\textbf{%s}" % h for h in head) + r" \\", r"\midrule"]
    for name, run, scored in runs:
        cells, tp, tn = [], 0, 0
        for c in conds:
            p, n = rate(grid_cells(run[c], scored)) if c in run else (0, 0)
            tp += p
            tn += n
            cells.append(r"\cellcolor{%s}%s {\tiny %d/%d}" % (shade(p, n), pct(p, n), p, n))
        cells.append(r"\cellcolor{%s}\textbf{%s} {\tiny %d/%d}"
                     % (shade(tp, tn), pct(tp, tn), tp, tn))
        out.append(r"\textbf{%s} & %s \\" % (esc(name), " & ".join(cells)))
    out += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    return "\n".join(out)


def train_table():
    ev = {"Yes": r"\textcolor{ok}{done}", "No": r"\textcolor{bad}{no}",
          "In Progress": r"\textcolor{amber}{in prog.}", "": "--"}
    out = ["% ==== Training runs / dataset sizes (Model Train Baselines) ====",
           r"\begin{table}[ht]\centering\small",
           r"\setlength{\tabcolsep}{6pt}\renewcommand{\arraystretch}{1.2}",
           r"\caption{Training runs and dataset sizes, cross-listed with "
           r"\emph{Model Train Baselines}. Each task is trained at 50 / $\sim$100 / "
           r"150 demos; the eval-done rows match the grids in this report.}",
           r"\begin{tabular}{llcccc}", r"\toprule",
           r"\textbf{Dataset} & \textbf{Size} & \textbf{Train} & \textbf{Started} "
           r"& \textbf{Eval} & \textbf{xArm} \\", r"\midrule"]
    xmark = r"$\checkmark$"
    for _m, ds, size, train, _comp, done, evs, xarm in D.TRAIN_RUNS:
        row = (f"{esc(ds)} & {size} & {esc(train) or '--'} & {esc(done) or '--'} & "
               f"{ev.get(evs, esc(evs))} & {xmark if xarm else '--'}")
        if evs in ("Yes", "In Progress"):
            row = r"\rowcolor{evalbg} " + row
        out.append(row + r" \\")
    out += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    return "\n".join(out)


def our_method_table():
    ev = {"Yes": r"\textcolor{ok}{done}", "No": r"\textcolor{bad}{no}", "": "--"}
    out = ["% ==== Our-method (SAP) training runs (Our Method Train) ====",
           r"\begin{table}[ht]\centering\small",
           r"\setlength{\tabcolsep}{6pt}\renewcommand{\arraystretch}{1.2}",
           r"\caption{Our-method (SAP) training runs, cross-listed with "
           r"\emph{Our Method Train}. Only underlined runs carrying a Yes/No in the "
           r"Eval Completed? column are listed; the done row is the 1$\times$1 pouring "
           r"model \texttt{pour\_quality\_2k\_lerobot} (60\%).}",
           r"\begin{tabular}{llcccc}", r"\toprule",
           r"\textbf{Model} & \textbf{Dataset} & \textbf{Size} & \textbf{Status} "
           r"& \textbf{Started} & \textbf{Eval} \\", r"\midrule"]
    for model, ds, size, status, _comp, started, evs in D.OUR_METHOD_TRAINS:
        row = (f"{esc(model)} & {esc(ds)} & {size} & {esc(status) or '--'} & "
               f"{esc(started) or '--'} & {ev.get(evs, esc(evs))}")
        if evs in ("Yes", "In Progress"):
            row = r"\rowcolor{evalbg} " + row
        out.append(row + r" \\")
    out += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    return "\n".join(out)


def mugtree_table(cells_by_cup, label, skip_blank=False):
    colspec = (">{\\raggedright\\arraybackslash}p{%s}%s C{%s}"
               % (W_MUGLBL, ("C{%s}" % W_TRIAL) * 5, W_RATE))
    out = [f"% ==== {label} ====",
           r"\begin{table}[ht]\centering\small",
           r"\renewcommand{\arraystretch}{1.18}",
           f"\\caption{{{esc(label)}.}}",
           r"\begin{tabular}{%s}" % colspec, r"\toprule",
           r"\textbf{Cup} & 1 & 2 & 3 & 4 & 5 & \textbf{Rate} \\", r"\midrule"]
    for cup, trs in cells_by_cup.items():
        p, n = rate(trs)
        if skip_blank and n == 0:
            continue
        nm = cup + ("*" if cup == "TWC" else "")
        rcell = (r"\cellcolor{%s}%s {\tiny %d/%d}" % (shade(p, n), pct(p, n), p, n)
                 if n else r"--")
        out.append(r"\textbf{%s} & %s & %s \\"
                   % (esc(nm), " & ".join(tex_cell(c) for c in trs), rcell))
    out += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    return "\n".join(out)


def wb_redo_table():
    out = ["% ==== Coffee 1x1 VLA --- White-Basic re-run ====",
           r"\begin{table}[ht]\centering\small",
           r"\renewcommand{\arraystretch}{1.2}",
           r"\caption{Coffee 1$\times$1 VLA @150 demos --- White-Basic re-run.}",
           r"\begin{tabular}{>{\raggedright\arraybackslash}p{1.4cm}ccl}", r"\toprule",
           r"\textbf{Machine} & \textbf{Result} & \textbf{Grasp} & \textbf{Notes} \\",
           r"\midrule"]
    for cond in ("id_id", "id_od"):
        for m, cell in D.coffee_1x1_vla_wb_redo[cond].items():
            res, grasp, notes = cell
            mark = r"\pass" if res == "P" else r"\fail"
            nn = esc(", ".join(str(x) for x in notes)) if notes else "--"
            out.append(r"%s & %s & %s & %s \\" % (esc(m), mark, grasp or "--", nn))
    out += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    return "\n".join(out)


# --------------------------------------------------------------------------- #
PREAMBLE = r"""\documentclass[10pt]{article}
\usepackage[margin=0.8in,landscape]{geometry}
\usepackage{booktabs}
\usepackage{array}
\usepackage[table,dvipsnames]{xcolor}
\usepackage{pifont}
\usepackage{amssymb}
\usepackage{caption}
\usepackage{placeins}  % \FloatBarrier between sections (many float tables)
\captionsetup{font=small,labelfont=bf,skip=4pt}

\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}

% result marks (coloured, no cell fill)
\definecolor{ok}{HTML}{1B873F}
\definecolor{bad}{HTML}{C0392B}
\definecolor{amber}{HTML}{B7791F}
\definecolor{notegrey}{HTML}{8A8F99}
\newcommand{\pass}{\textcolor{ok}{\ding{51}}}
\newcommand{\fail}{\textcolor{bad}{\ding{55}}}
\newcommand{\bl}{\textcolor{notegrey}{--}}
\newcommand{\nt}[1]{\,\textsuperscript{\scriptsize\textcolor{notegrey}{#1}}}

% summary heat shades + eval highlight
\definecolor{evalbg}{HTML}{E7F3EA}
\definecolor{shade0}{HTML}{F6D8D5}
\definecolor{shadeA}{HTML}{F8E2CE}
\definecolor{shadeB}{HTML}{F6EFCC}
\definecolor{shadeC}{HTML}{E6F0CC}
\definecolor{shadeD}{HTML}{D4EFD9}
\definecolor{shadeN}{HTML}{F2F2F4}

\begin{document}
\begin{center}\Large\textbf{Semantic Manipulation --- Evaluation Tables}\end{center}
\noindent\footnotesize
xArm $\cdot$ VLA ($\pi$-style) $\cdot$ datasets: coffee 1$\times$1 \& 4$\times$4,
pouring 5$\times$3, mug-tree 5$\times$1 $\cdot$ trained at 50 / $\sim$100 / 150 demos
(filled: coffee @50/100/150, pouring 5$\times$3 @50/105/150, pouring 1$\times$1 @50/100/150 +
1$\times$1 SAP baseline, mug-tree @150). Marks: \pass{} success,
\fail{} failure; superscript = grasp (S/T) and note numbers.\\[2pt]
\textbf{Codes.} Cups: WB White-Basic, O Orange, Bk Black, R Red (ID); Br Brown,
WC White-Ceramic, Gr Gray, P Pink (OOD); TWC Tall-White-Ceramic.\;
Machines: K Keurig, Bk Black, T Teal, W White (ID); R Red, TS Tastyle, Bl Blue (OOD).\;
Bowls: BL Blue, LB Light-Blue, BK Black (ID); P Pink, TB Tall, W White (OOD).
\normalsize
\bigskip
"""


def section(title):
    # titles are author-controlled LaTeX (may contain \& etc.) — do not escape
    # \FloatBarrier flushes queued float tables so we never overflow LaTeX's
    # float limit (this document has many \begin{table} blocks).
    return "\n\\FloatBarrier\n\\section*{%s}\n" % title


def notes_block(notes, title):
    """Compact inline footnote legend for the paper."""
    items = "; ".join(f"\\textbf{{{esc(str(k))}}} {esc(v)}" for k, v in notes.items())
    return f"\\noindent\\footnotesize\\textbf{{{title}.}} {items}\\normalsize\\par\\medskip"


def build_latex():
    parts = [PREAMBLE]

    parts.append(section("Summary"))
    parts.append(summary_table([
        ("Coffee 4x4 VLA @150", D.coffee_4x4_vla, None),
        ("Coffee 4x4 VLA @100", D.coffee_4x4_vla_100, None),
        ("Coffee 4x4 VLA @50", D.coffee_4x4_vla_50, None),
        ("Coffee 1x1 VLA @150", D.coffee_1x1_vla, None),
        ("Coffee 1x1 VLA @100", D.coffee_1x1_vla_100, None),
        ("Coffee 1x1 VLA @50", D.coffee_1x1_vla_50, None),
        ("Pouring 5x3 VLA @150", D.pouring_5x3_vla_150, POUR_SCORED),
        ("Pouring 5x3 VLA @105", D.pouring_4x4_vla, POUR_SCORED),
        ("Pouring 5x3 VLA @50", D.pouring_5x3_vla_50, POUR_SCORED),
        ("Pouring 1x1 VLA @50 (partial)", D.pouring_1x1_vla_50, POUR_SCORED),
        ("Pouring 1x1 VLA @100 (partial)", D.pouring_1x1_vla_100, POUR_SCORED),
        ("Pouring 1x1 VLA @150 (partial)", D.pouring_1x1_vla_150, POUR_SCORED),
        ("Pouring 1x1 SAP (baseline)", D.pouring_5x3_sap, POUR_SCORED),
    ]))

    parts.append(section("Training runs \\& dataset sizes"))
    parts.append(train_table())
    parts.append(our_method_table())

    parts.append(section("Task 1 --- Cup on Coffee Machine (rows: machines, cols: cups)"))
    parts.append("% --- 150-demo dataset (note numbers: COFFEE_NOTES legend) ---")
    parts.append(coffee_block(D.coffee_4x4_vla, "Coffee 4x4 VLA @150 demos"))
    parts.append(coffee_block(D.coffee_1x1_vla, "Coffee 1x1 VLA @150 demos"))
    parts.append(wb_redo_table())
    parts.append("% --- 100-demo dataset (note numbers: COFFEE_NOTES_100 legend) ---")
    parts.append(coffee_block(D.coffee_4x4_vla_100, "Coffee 4x4 VLA @100 demos"))
    parts.append(coffee_block(D.coffee_1x1_vla_100, "Coffee 1x1 VLA @100 demos"))
    parts.append("% --- 50-demo dataset (note numbers: COFFEE_NOTES_50 legend) ---")
    parts.append(coffee_block(D.coffee_4x4_vla_50, "Coffee 4x4 VLA @50 demos"))
    parts.append(coffee_block(D.coffee_1x1_vla_50, "Coffee 1x1 VLA @50 demos"))

    parts.append(section("Task 2 --- Cup Pouring (rows: bowls, cols: cups)"))
    parts.append("% --- 150-demo dataset (note numbers: POUR_NOTES legend) ---")
    parts.append(pouring_block(D.pouring_5x3_vla_150, "Pouring 5x3 VLA @150 demos"))
    parts.append("% --- 105-demo dataset (note numbers: POUR_NOTES legend) ---")
    parts.append(pouring_block(D.pouring_4x4_vla, "Pouring 5x3 VLA @105 demos"))
    parts.append("% --- 50-demo dataset (note numbers: POUR_NOTES legend) ---")
    parts.append(pouring_block(D.pouring_5x3_vla_50, "Pouring 5x3 VLA @50 demos"))
    parts.append("% --- 1x1-config pouring, PARTIAL evals (blank cells intentional) ---")
    parts.append(pouring_block(D.pouring_1x1_vla_50,
                               "Pouring 1x1 VLA @50 demos (partial eval)"))
    parts.append(pouring_block(D.pouring_1x1_vla_100,
                               "Pouring 1x1 VLA @100 demos (partial eval)"))
    parts.append(pouring_block(D.pouring_1x1_vla_150,
                               "Pouring 1x1 VLA @150 demos (partial eval)"))

    parts.append(section("Task 3 --- Hang Cup on Mug Tree (5 trials per cup)"))
    parts.append(mugtree_table(D.mugtree_5x1_vla["id_cup"],
                               "Mug Tree 5x1 VLA @150 demos --- ID cups"))
    parts.append(mugtree_table(D.mugtree_5x1_vla["od_cup"],
                               "Mug Tree 5x1 VLA @150 demos --- OOD cups", skip_blank=True))

    parts.append(section("Task 2b --- Cup Pouring, 1x1 SAP baseline (rows: bowls, cols: cups)"))
    parts.append(pouring_block(D.pouring_5x3_sap, "Pouring 1x1 SAP baseline"))

    parts.append(section("Appendix A --- Coffee 4x4 VLA @150 demos (OLD run)"))
    parts.append(coffee_block(D.coffee_4x4_vla_old, "Coffee 4x4 VLA OLD @150 demos"))

    parts.append(section("Footnote legends"))
    parts.append(notes_block(D.COFFEE_NOTES, "Coffee notes (150-demo \\& OLD sheets)"))
    parts.append(notes_block(D.COFFEE_NOTES_100, "Coffee notes (100-demo sheets)"))
    parts.append(notes_block(D.COFFEE_NOTES_50, "Coffee notes (50-demo sheets)"))
    parts.append(notes_block(D.POUR_NOTES, "Pouring notes (VLA: 50/105/150-demo sheets)"))
    parts.append(notes_block(D.POUR_NOTES_SAP, "Pouring notes (SAP baseline sheet)"))
    parts.append(notes_block(D.MUGTREE_NOTES, "Mug-tree notes"))

    parts.append("\n\\end{document}\n")

    with open(OUT, "w") as f:
        f.write("\n".join(parts))
    return OUT


if __name__ == "__main__":
    print("wrote", build_latex())
