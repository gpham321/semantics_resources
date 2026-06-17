"""Generate report.html (styled) and report.md (Notion paste) from eval_data.py."""
import eval_data as D

COND_LABELS = {
    "id_id": ("ID Cup / ID Machine", "ID Cup / ID Bowl"),
    "id_od": ("ID Cup / OOD Machine", "ID Cup / OOD Bowl"),
    "od_id": ("OOD Cup / ID Machine", "OOD Cup / ID Bowl"),
    "od_od": ("OOD Cup / OOD Machine", "OOD Cup / OOD Bowl"),
}

# ---- stats ----------------------------------------------------------------
def cell_pass(cell):
    return cell is not None and cell[0] == "P"

def rate(cells):
    run = [c for c in cells if c is not None]
    p = sum(1 for c in run if c[0] == "P")
    return p, len(run)

def grid_cells(grid, scored_cups=None):
    out = []
    for row in grid.values():
        for cup, cell in row.items():
            if scored_cups is not None and cup not in scored_cups:
                continue
            out.append(cell)
    return out

def run_rate(run, scored=None):
    cells = []
    for cond, g in run.items():
        cells += grid_cells(g, scored)
    return rate(cells)

# ---- shared cell text -----------------------------------------------------
def notes_str(notes):
    return ",".join(str(n) for n in notes) if notes else ""

# ===========================================================================
# HTML
# ===========================================================================
def html_cell(cell):
    if cell is None:
        return '<td class="blank">—</td>'
    res, grasp, notes = cell
    cls = "pass" if res == "P" else "fail"
    mark = "✓" if res == "P" else "✗"
    g = f'<span class="g g{grasp}">{grasp}</span>' if grasp in ("S", "T") else ""
    n = f'<sup class="fn">{notes_str(notes)}</sup>' if notes else ""
    return f'<td class="{cls}">{mark}{g}{n}</td>'

def html_table(grid, cups, rowlabels, row_name_map, col_name_map, rowhdr):
    h = ['<table class="grid">']
    h.append("<tr><th class='corner'>" + rowhdr + "</th>" +
             "".join(f"<th>{col_name_map[c]}</th>" for c in cups) + "</tr>")
    for r in rowlabels:
        row = grid[r]
        h.append(f"<tr><th class='rowh'>{row_name_map[r]}</th>" +
                 "".join(html_cell(row[c]) for c in cups) + "</tr>")
    h.append("</table>")
    return "".join(h)

def html_cond_block(run, task, cups_id, cups_od, rows_id, rows_od,
                    cup_names, row_names, rowhdr, scored=None):
    blocks = []
    for cond in ("id_id", "id_od", "od_id", "od_od"):
        if cond not in run:
            continue
        cups = cups_id if cond.startswith("id") else cups_od
        rows = rows_id if cond.endswith("id") else rows_od
        p, n = rate(grid_cells(run[cond], scored))
        pct = f"{100*p/n:.0f}%" if n else "—"
        label = COND_LABELS[cond][0 if task == "coffee" else 1]
        blocks.append(
            f'<div class="cond"><div class="condhead"><span>{label}</span>'
            f'<span class="badge">{p}/{n} &middot; {pct}</span></div>'
            + html_table(run[cond], cups, rows, row_names, cup_names, rowhdr)
            + "</div>")
    return '<div class="conds">' + "".join(blocks) + "</div>"

def summary_cards(rows):
    cards = []
    for title, sub, p, n in rows:
        pct = f"{100*p/n:.0f}%" if n else "—"
        cards.append(f'<div class="card"><div class="cardpct">{pct}</div>'
                     f'<div class="cardn">{p}/{n}</div>'
                     f'<div class="cardt">{title}</div>'
                     f'<div class="cards2">{sub}</div></div>')
    return '<div class="cards">' + "".join(cards) + "</div>"

def cond_breakdown_table(runs):
    """runs: list of (name, run, scored). Rows=runs, cols=conditions+overall."""
    conds = ["id_id", "id_od", "od_id", "od_od"]
    h = ['<table class="summary"><tr><th>Run</th>']
    for c in conds:
        h.append(f"<th>{c.replace('_','/').upper()}</th>")
    h.append("<th>Overall</th></tr>")
    for name, run, scored in runs:
        h.append(f"<tr><th class='rowh'>{name}</th>")
        tot_p = tot_n = 0
        for c in conds:
            if c in run:
                p, n = rate(grid_cells(run[c], scored))
            else:
                p, n = 0, 0
            tot_p += p; tot_n += n
            cellpct = f"{100*p/n:.0f}%" if n else "—"
            shade = pct_class(p, n)
            h.append(f"<td class='{shade}'>{cellpct}<br><span class='sn'>{p}/{n}</span></td>")
        opct = f"{100*tot_p/tot_n:.0f}%" if tot_n else "—"
        h.append(f"<td class='{pct_class(tot_p,tot_n)} ov'>{opct}<br><span class='sn'>{tot_p}/{tot_n}</span></td></tr>")
    h.append("</table>")
    return "".join(h)

# ---- task suite (data-collection overview, from the whiteboard) -----------
# (task, objects, config label, episodes, avg teleop seconds/demo, in-report?)
TASK_SUITE = [
    ("Cup on Coffee Machine", "cup → coffee machine", "4×4",      "16", 30, True),
    ("Cup Pour into Bowl",    "cup → bowl",           "5×3",      "15", 35, True),
    ("Hang Cup on Mug Tree",  "cup → mug tree",       "5×1",      "5",  27, True),
    ("Brick into Drawer",     "power brick → drawer", "5×1",      "5",  32, False),
    ("Power Drill on Pad",    "drill → mouse pad",    "1×1",      "1",  16, False),
    ("Bottle/Can on Coaster", "bottle/can → coaster", "(1+1)×1",  "2",  11, False),
    ("Faucet",                "turn faucet",          "1",        "1",  23, False),
]

def task_suite_table():
    h = ['<table class="suite"><tr><th>#</th><th>Task</th><th>Objects</th>'
         '<th>Config</th><th>Variations</th><th class="num">Avg teleop / demo</th>'
         '<th>In report</th></tr>']
    for i, (task, objs, cfg, variations, secs, inrep) in enumerate(TASK_SUITE, 1):
        pill = ("<span class='pill pill-yes'>✓ below</span>" if inrep
                else "<span class='pill pill-mut'>collected</span>")
        h.append(f"<tr><td class='num'>{i}</td><td class='lft'><b>{task}</b></td>"
                 f"<td class='lft'>{objs}</td><td><span class='cfg'>{cfg}</span></td>"
                 f"<td class='num'>{variations}</td>"
                 f"<td class='num'>~{secs}s</td><td>{pill}</td></tr>")
    h.append("</table>")
    return "".join(h)

def pct_class(p, n):
    if not n:
        return "blank"
    r = p / n
    if r >= 0.8:
        return "s4"
    if r >= 0.6:
        return "s3"
    if r >= 0.4:
        return "s2"
    if r >= 0.2:
        return "s1"
    return "s0"

CSS = """
:root{--bg:#0f1115;--panel:#171a21;--panel2:#1c2029;--ink:#e6e8ee;--mut:#9aa3b2;
 --line:#2a2f3a;--accent:#7aa2ff;}
*{box-sizing:border-box}
body{font:15px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
 color:var(--ink);margin:0;background:var(--bg);padding:0 0 80px}
.wrap{max-width:1080px;margin:0 auto;padding:0 28px}
header{background:linear-gradient(135deg,#1b2747,#2b3f6b);padding:38px 0 30px;margin-bottom:8px;
 border-bottom:1px solid var(--line)}
h1{font-size:27px;margin:0 0 6px;font-weight:650;color:#fff}
.sub{opacity:.9;font-size:15px;color:#dfe6f5}
h2{font-size:21px;margin:42px 0 6px;padding-bottom:7px;border-bottom:2px solid var(--line)}
h3{font-size:16.5px;margin:26px 0 4px;color:#aebfe6}
.note{color:var(--mut);font-size:13.5px;margin:4px 0 14px}
.cards{display:flex;gap:14px;flex-wrap:wrap;margin:18px 0 6px}
.card{flex:1;min-width:150px;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px;box-shadow:0 1px 2px rgba(0,0,0,.25)}
.cardpct{font-size:30px;font-weight:680;letter-spacing:-.5px;color:#fff}
.cardn{color:var(--mut);font-size:13px;margin-top:-2px}
.cardt{margin-top:8px;font-weight:600;font-size:14px}
.cards2{color:var(--mut);font-size:12.5px}
table{border-collapse:collapse;background:var(--panel)}
table.summary{width:100%;margin:14px 0 6px;border:1px solid var(--line);border-radius:10px;overflow:hidden;table-layout:fixed}
table.summary th,table.summary td{padding:9px 10px;text-align:center;border:1px solid var(--line);font-size:13.5px}
table.summary th:first-child,table.summary td:first-child{width:170px;text-align:left}
table.summary th{background:var(--panel2);font-weight:600}
table.summary td.ov{font-weight:700}
.sn{font-size:11px;color:var(--mut)}
.conds{display:grid;grid-template-columns:1fr 1fr;gap:20px 26px;margin:14px 0}
.cond{}
.condhead{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px}
.condhead span:first-child{font-weight:600;font-size:14px}
.badge{background:#22304f;color:#9bb6ff;border-radius:20px;padding:2px 10px;font-size:12px;font-weight:600}
table.grid{width:100%;border:1px solid var(--line);table-layout:fixed}
table.grid th,table.grid td{border:1px solid var(--line);padding:6px 4px;text-align:center;font-size:13px;word-wrap:break-word;overflow-wrap:break-word}
table.grid th{background:var(--panel2);font-weight:600;font-size:12px;color:#cfd6e4}
table.grid th.rowh{text-align:right;padding-right:8px;white-space:normal;background:#191d25}
table.grid th.corner,table.grid th.rowh{width:118px}
table.grid th.corner{background:#222734}
td.pass{background:#15351f;color:#74e39a;font-weight:600}
td.fail{background:#3a1c1f;color:#ff8d85;font-weight:600}
td.blank{color:#5a6273}
.g{display:inline-block;font-size:9.5px;font-weight:700;border-radius:4px;padding:0 3px;margin-left:2px;vertical-align:middle}
.gS{background:#1f3358;color:#8fb6ff}
.gT{background:#4a3217;color:#f0b878}
sup.fn{font-size:9px;color:#c7a96b;margin-left:1px}
.s4{background:#1c4a2c;color:#bdf3cd}.s3{background:#2f4a23;color:#dcefc0}
.s2{background:#4d431d;color:#f2e3ac}.s1{background:#4d2f1c;color:#f4c8a8}.s0{background:#4a2122;color:#f3b3ad}
.legend{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:14px 0;font-size:13px;columns:2;column-gap:34px}
.legend b{color:#aebfe6}
.legend ul{margin:5px 0 10px;padding-left:18px}
.legend li{margin:2px 0;break-inside:avoid}
.pending{background:var(--panel);border:1px dashed #3a4150;border-radius:10px;padding:12px 18px;color:var(--mut);font-size:13.5px}
.kk{display:inline-block;background:#222734;border-radius:5px;padding:1px 6px;font-size:12px;margin:2px 3px;color:#cfd6e4}
details.appendix{margin:34px 0 0;border-top:2px solid var(--line);padding-top:4px}
details.appendix>summary{font-size:21px;font-weight:600;cursor:pointer;list-style:none;
 padding:10px 0;color:var(--ink);user-select:none}
details.appendix>summary::-webkit-details-marker{display:none}
details.appendix>summary::before{content:'\\25B8';color:var(--accent);margin-right:11px;font-size:14px}
details.appendix[open]>summary::before{content:'\\25BE'}
details.appendix>summary .tag{font-size:12px;font-weight:600;color:var(--mut);margin-left:10px}
details.appendix .inner{padding-top:4px}
.dslabel{display:block;color:var(--mut);font-size:13px;font-weight:400;margin-top:3px}
.dslabel b{color:#aebfe6}
.szb{display:inline-block;background:#22304f;color:#9bb6ff;border-radius:6px;padding:1px 9px;font-size:12.5px;font-weight:600;margin-left:8px;vertical-align:middle;letter-spacing:.2px}
table.runs{width:100%;margin:14px 0 6px;border:1px solid var(--line);border-radius:10px;overflow:hidden}
table.runs th,table.runs td{padding:7px 10px;text-align:center;border:1px solid var(--line);font-size:13px}
table.runs th{background:var(--panel2);font-weight:600;color:#cfd6e4}
table.runs td.lft{text-align:left}
table.suite{width:100%;margin:14px 0 6px;border:1px solid var(--line);border-radius:10px;overflow:hidden;table-layout:fixed}
table.suite th,table.suite td{padding:9px 11px;text-align:center;border:1px solid var(--line);font-size:13.5px}
table.suite th{background:var(--panel2);font-weight:600;color:#cfd6e4}
table.suite td.lft,table.suite th.lft{text-align:left}
table.suite td.num,table.suite th.num{text-align:center;color:#cfd6e4}
table.suite tr:hover td{background:var(--panel2)}
.cfg{display:inline-block;background:#22304f;color:#9bb6ff;border-radius:6px;padding:1px 9px;font-size:12.5px;font-weight:600;letter-spacing:.3px}
tr.eval-done{background:#13251a}
.pill{display:inline-block;border-radius:20px;padding:1px 9px;font-size:11.5px;font-weight:600}
.pill-yes{background:#1c4a2c;color:#bdf3cd}.pill-no{background:#3a1c1f;color:#ff9a93}
.pill-prog{background:#4a3a17;color:#f0c878}.pill-mut{background:#262b36;color:#8a93a3}
.st-done{color:#8fe0a8}.st-train{color:#f0c878}.st-queue{color:#9aa3b2}
.flag{background:#2a2114;border:1px solid #5a4424;border-radius:8px;padding:10px 14px;margin:12px 0;color:#e8cf9a;font-size:13px}
details.tpl{margin:14px 0 0;border:1px dashed #3a4150;border-radius:10px;padding:2px 14px;background:#141821}
details.tpl>summary{cursor:pointer;list-style:none;padding:9px 0;color:#aebfe6;font-weight:600;font-size:14px;user-select:none}
details.tpl>summary::-webkit-details-marker{display:none}
details.tpl>summary::before{content:'\\25B8';color:var(--accent);margin-right:9px;font-size:12px}
details.tpl[open]>summary::before{content:'\\25BE'}
details.tpl>summary .tag{color:var(--mut);font-weight:500;font-size:12px;margin-left:8px}
details.tpl .inner{padding:2px 0 12px}
details.tpl h4{margin:14px 0 4px;color:#cfd6e4;font-size:13.5px;font-weight:600}
td.tplcell{background:#12151c}
footer{color:#6b7384;font-size:12px;text-align:center;margin-top:40px}
"""

# ---- dataset labels & training-run cross-list ----------------------------
def ds_label_html(task_key):
    """Per-task dataset caption: N×M config + the three training sizes.
    (Each grid's heading already states its own size, so don't repeat it here.)"""
    name, ds, variants, sizes = D.TASK_CONFIG[task_key]
    vstr = " & ".join(f"<b>{v}</b>" for v in variants)
    szstr = " / ".join(str(s) for s in sizes)
    return (f"<span class='dslabel'>Dataset <b>{ds}</b> &nbsp;·&nbsp; "
            f"config {vstr} &nbsp;·&nbsp; trained at {szstr} demos</span>")

EVAL_PILL = {
    "Yes":         ("pill-yes",  "Eval ✓ done"),
    "No":          ("pill-no",   "Eval ✗"),
    "In Progress": ("pill-prog", "Eval ◑ in progress"),
    "":            ("pill-mut",  "—"),
}
TRAIN_CLS = {"Done": "st-done", "Training": "st-train",
             "Queued": "st-queue", "": "st-queue"}

def train_runs_table():
    h = ['<table class="runs"><tr>'
         '<th>Dataset</th><th>Size</th><th>Train</th><th>Computer</th>'
         '<th>Done</th><th>Eval</th><th>On xArm</th></tr>']
    for model, ds, size, train, comp, done, ev, xarm in D.TRAIN_RUNS:
        pill, plabel = EVAL_PILL.get(ev, EVAL_PILL[""])
        rowcls = " class='eval-done'" if ev in ("Yes", "In Progress") else ""
        tcls = TRAIN_CLS.get(train, "st-queue")
        h.append(
            f"<tr{rowcls}><td class='lft'>{ds}</td><td>{size}</td>"
            f"<td class='{tcls}'>{train or '—'}</td><td>{comp or '—'}</td>"
            f"<td>{done or '—'}</td>"
            f"<td><span class='pill {pill}'>{plabel}</span></td>"
            f"<td>{'✓' if xarm else '—'}</td></tr>")
    h.append("</table>")
    return "".join(h)


# ---- empty fill-in templates for not-yet-evaluated dataset sizes ----------
def pending_sizes(task_key, sizes):
    """Sizes still to fill in: every trained size whose grid isn't filled yet."""
    filled = D.FILLED_SIZES.get(task_key, {150})
    return [s for s in sizes if s not in filled]

def empty_grid_table(cols, rows, col_names, row_names, rowhdr):
    h = ['<table class="grid"><tr><th class="corner">' + rowhdr + "</th>" +
         "".join(f"<th>{col_names[c]}</th>" for c in cols) + "</tr>"]
    for r in rows:
        h.append(f"<tr><th class='rowh'>{row_names[r]}</th>" +
                 "".join("<td class='blank tplcell'>&nbsp;</td>" for _ in cols) + "</tr>")
    h.append("</table>")
    return "".join(h)

def empty_conds(task, conds_spec, col_names, row_names, rowhdr):
    blocks = []
    for cond, rows, cols in conds_spec:
        label = COND_LABELS[cond][0 if task == "coffee" else 1]
        n = len(rows) * len(cols)
        blocks.append(f'<div class="cond"><div class="condhead"><span>{label}</span>'
                      f'<span class="badge">0/{n}</span></div>'
                      + empty_grid_table(cols, rows, col_names, row_names, rowhdr)
                      + "</div>")
    return '<div class="conds">' + "".join(blocks) + "</div>"

def empty_mugtree_table(cups):
    h = ['<table class="grid" style="max-width:640px"><tr><th class="corner">'
         "Cup ↓ / Trial →</th>" +
         "".join(f"<th>{i}</th>" for i in range(1, 6)) + "<th>Rate</th></tr>"]
    for cup in cups:
        nm = D.CUP_NAMES[cup] + (" *" if cup == "TWC" else "")
        h.append(f"<tr><th class='rowh'>{nm}</th>" +
                 "".join("<td class='blank tplcell'>&nbsp;</td>" for _ in range(5)) +
                 "<td class='blank tplcell'>&nbsp;</td></tr>")
    h.append("</table>")
    return "".join(h)

COFFEE_CONDS = [("id_id", D.MACH_ID, D.CUPS_ID), ("id_od", D.MACH_OOD, D.CUPS_ID),
                ("od_id", D.MACH_ID, D.CUPS_OOD), ("od_od", D.MACH_OOD, D.CUPS_OOD)]
POUR_CONDS = [("id_id", D.BOWLS_ID, D.POUR_CUPS_ID), ("id_od", D.BOWLS_OOD, D.POUR_CUPS_ID),
              ("od_id", D.BOWLS_ID, D.POUR_CUPS_OOD), ("od_od", D.BOWLS_OOD, D.POUR_CUPS_OOD)]

def empty_templates_html(task_key):
    """Collapsible block of blank grids for each not-yet-run dataset size."""
    sizes = D.TASK_CONFIG[task_key][3]
    if task_key == "coffee":
        variants = [("1×1", "Mug/Machine 1by1"), ("4×4", "Mug/Machine 4by4")]
    elif task_key == "pouring":
        variants = [("5×3", "Pour Task")]
    else:
        variants = [("5×1", "Mug Tree Task")]

    inner, labels = [], []
    for vlabel, dsname in variants:
        for size in pending_sizes(task_key, sizes):
            labels.append(f"{vlabel}@{size}")
            inner.append(f"<h4>{vlabel} VLA @ {size} demos "
                         "<span class='note' style='font-weight:400'>— blank, fill in "
                         "as this eval completes</span></h4>")
            if task_key == "coffee":
                inner.append(empty_conds("coffee", COFFEE_CONDS, D.CUP_NAMES,
                                         D.MACH_NAMES, "Machine ↓ / Cup →"))
            elif task_key == "pouring":
                names = {**D.CUP_NAMES, "TWC": "Tall W.C.*"}
                inner.append(empty_conds("pour", POUR_CONDS, names,
                                         D.BOWL_NAMES, "Bowl ↓ / Cup →"))
            else:
                inner.append("<h5 style='margin:8px 0 2px;color:#9aa3b2;font-size:12.5px;"
                             "font-weight:600'>ID cups</h5>")
                inner.append(empty_mugtree_table(D.MUGTREE_CUPS_ID))
                inner.append("<h5 style='margin:10px 0 2px;color:#9aa3b2;font-size:12.5px;"
                             "font-weight:600'>OOD cups</h5>")
                inner.append(empty_mugtree_table(D.MUGTREE_CUPS_OOD))
    if not inner:
        return ""
    return ("<details class='tpl'><summary>Empty grids for pending dataset sizes "
            f"<span class='tag'>{', '.join(labels)} · fill in later</span></summary>"
            "<div class='inner'>" + "".join(inner) + "</div></details>")


def coffee_block(run, scored=None):
    return html_cond_block(
        run, "coffee", D.CUPS_ID, D.CUPS_OOD, D.MACH_ID, D.MACH_OOD,
        D.CUP_NAMES, D.MACH_NAMES, "Machine ↓ / Cup →", scored)

def pouring_block(run):
    return html_cond_block(
        run, "pour", D.POUR_CUPS_ID, D.POUR_CUPS_OOD, D.BOWLS_ID, D.BOWLS_OOD,
        {**D.CUP_NAMES, "TWC": "Tall W.C.*"}, D.BOWL_NAMES, "Bowl ↓ / Cup →",
        scored=["WB", "O", "Bk", "R", "Br", "WC", "Gr", "P"])

def legend_html(notes, title, extra=""):
    items = "".join(f"<li><b>{k}.</b> {v}</li>" if isinstance(k, int)
                    else f"<li><b>{k}</b> {v}</li>" for k, v in notes.items())
    return (f'<div class="legend"><b>{title}</b><ul>{items}</ul>{extra}</div>')

def mugtree_rate(run, scored=None):
    cells = []
    for cup, trs in run["id_cup"].items():
        if scored is not None and cup not in scored:
            continue
        cells += trs
    return rate(cells)

def mugtree_table(cells_by_cup, skip_blank=False):
    h = ['<table class="grid" style="max-width:640px">']
    h.append("<tr><th class='corner'>Cup ↓ / Trial →</th>" +
             "".join(f"<th>{i}</th>" for i in range(1, 6)) + "<th>Rate</th></tr>")
    for cup, trs in cells_by_cup.items():
        p, n = rate(trs)
        if skip_blank and n == 0:
            continue
        pct = f"{100*p/n:.0f}%" if n else "—"
        nm = D.CUP_NAMES[cup] + (" *" if cup == "TWC" else "")
        h.append(f"<tr><th class='rowh'>{nm}</th>" +
                 "".join(html_cell(c) for c in trs) +
                 f"<td class='{pct_class(p,n) if n else 'blank'}'>{pct}"
                 f" <span class='sn'>{p}/{n}</span></td></tr>")
    h.append("</table>")
    return "".join(h)

def mugtree_html(run):
    return mugtree_table(run["id_cup"])

def build_html():
    p1, n1 = run_rate(D.coffee_1x1_vla)
    p4, n4 = run_rate(D.coffee_4x4_vla)
    p1_50, n1_50 = run_rate(D.coffee_1x1_vla_50)
    p4_50, n4_50 = run_rate(D.coffee_4x4_vla_50)
    pp, np_ = run_rate(D.pouring_4x4_vla,
                       scored=["WB", "O", "Bk", "R", "Br", "WC", "Gr", "P"])
    pm, nm = mugtree_rate(D.mugtree_5x1_vla, scored=["WB", "O", "Bk", "R"])
    po, no = run_rate(D.coffee_4x4_vla_old)

    grasp_legend = ('<b>Grasp tag</b><ul>'
                    '<li><span class="g gS">S</span> Side grasp &nbsp; '
                    '<span class="g gT">T</span> Top grasp</li></ul>')

    html = [f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>Semantic Evaluation Results</title><style>{CSS}</style></head><body>"]
    html.append("<header><div class='wrap'><h1>Semantic Manipulation — Evaluation Results</h1>"
                "<div class='sub'>Robot arm: <b>xArm</b> &nbsp;·&nbsp; Policy: <b>VLA</b> "
                "(π-style) &nbsp;·&nbsp; Datasets: coffee <b>1×1</b> &amp; <b>4×4</b>, "
                "pouring <b>5×3</b>, mug-tree <b>5×1</b> &nbsp;·&nbsp; "
                "Training sizes: <b>50 / ~100 / 150</b> demos "
                "(coffee @50 &amp; @150, pouring @105, mug-tree @150 filled)"
                "</div></div></header>")
    html.append("<div class='wrap'>")

    # task suite (data-collection overview)
    html.append("<h2>Task suite</h2>")
    html.append("<p class='note'>Seven teleoperated manipulation tasks were collected "
                "on the xArm. <b>Config</b> is the object-variation grid (e.g. 4×4 = 4 cups "
                "× 4 machines); <b>Variations</b> is the number of distinct object pairings. "
                "<b>Avg teleop / demo</b> is the mean time to teleoperate one demonstration. "
                "The first three tasks have evaluation grids in this report; the rest are "
                "collected and pending evaluation.</p>")
    html.append(task_suite_table())

    # overview
    html.append("<h2>Overview</h2>")
    html.append("<p class='note'>Each trial places/pours with a chosen grasp "
                "(<b>S</b>ide or <b>T</b>op). ✓ = success, ✗ = failure; superscripts are "
                "failure/condition notes (see legends). Objects are split into "
                "in-distribution (ID, seen in training) and out-of-distribution (OOD).</p>")
    html.append(summary_cards([
        ("Coffee · 4×4 VLA", "main model · 150-size", p4, n4),
        ("Pouring · 5×3 VLA", "cup → bowl · 105-size", pp, np_),
        ("Mug Tree · 5×1 VLA", "hang on tree · 150-size", pm, nm),
        ("Coffee · 1×1 VLA", "single-view · 150-size", p1, n1),
    ]))
    html.append("<h3>Success rate by condition</h3>")
    html.append(cond_breakdown_table([
        ("Coffee · 4×4 VLA · @150", D.coffee_4x4_vla, None),
        ("Coffee · 4×4 VLA · @50", D.coffee_4x4_vla_50, None),
        ("Coffee · 1×1 VLA · @150", D.coffee_1x1_vla, None),
        ("Coffee · 1×1 VLA · @50", D.coffee_1x1_vla_50, None),
        ("Pouring · 5×3 VLA · @105", D.pouring_4x4_vla,
         ["WB", "O", "Bk", "R", "Br", "WC", "Gr", "P"]),
    ]))
    html.append("<p class='note'>Dataset-size scaling is visible on coffee: the <b>4×4</b> "
                f"model climbs {100*p4_50/n4_50:.0f}% → {100*p4/n4:.0f}% from 50→150 demos, "
                f"while the <b>1×1</b> model stays low "
                f"({100*p1_50/n1_50:.0f}% → {100*p1/n1:.0f}%).</p>")

    # Training runs cross-list (from Model Train Baselines.png)
    html.append("<h2>Training runs &amp; dataset sizes</h2>")
    html.append("<p class='note'>Cross-listed with <b>Model Train Baselines</b>. "
                "Every task is trained at three dataset sizes "
                "(<b>50 / ~100 / 150</b> demos). The eval-complete rows (highlighted) match "
                "the grids in this report: Coffee 1×1 &amp; 4×4 @50 and @150, Pour @105, "
                "Mug-Tree @150.</p>")
    html.append(train_runs_table())

    # Task 1 coffee
    html.append("<h2>Task 1 — Cup on Coffee Machine</h2>")
    html.append(ds_label_html("coffee"))

    # --- 150-demo dataset (main) ---
    html.append("<h3>150-demo dataset</h3>")
    html.append(f"<h4 style='margin:14px 0 4px;color:#aebfe6;font-size:14.5px'>4×4 VLA "
                f"<span class='szb'>@ 150 demos</span> &nbsp;<span class='note'>"
                f"({p4}/{n4} = {100*p4/n4:.0f}%)</span></h4>")
    html.append(coffee_block(D.coffee_4x4_vla))
    html.append(f"<h4 style='margin:18px 0 4px;color:#aebfe6;font-size:14.5px'>1×1 VLA "
                f"<span class='szb'>@ 150 demos</span> &nbsp;<span class='note'>"
                f"({p1}/{n1} = {100*p1/n1:.0f}%)</span></h4>")
    html.append("<p class='note'>The single-view (1×1) model fails almost everything; "
                "its only successes are on the (taller-clearance) OOD machines.</p>")
    html.append(coffee_block(D.coffee_1x1_vla))
    # WB redo
    html.append("<h4 style='margin:18px 0 4px;color:#aebfe6;font-size:14.5px'>"
                "1×1 VLA — White-Basic re-run (supplementary)</h4>")
    html.append("<table class='grid' style='max-width:560px'><tr><th class='corner'>"
                "Machine</th><th>Result</th><th>Grasp</th><th>Notes</th></tr>")
    for cond in ("id_id", "id_od"):
        for m, cell in D.coffee_1x1_vla_wb_redo[cond].items():
            res, grasp, notes = cell
            cls = "pass" if res == "P" else "fail"
            mark = "✓" if res == "P" else "✗"
            nn = ", ".join(str(x) for x in notes) if notes else ""
            html.append(f"<tr><th class='rowh'>WB / {D.MACH_NAMES[m]}</th>"
                        f"<td class='{cls}'>{mark}</td><td>{grasp}</td>"
                        f"<td style='font-size:11px;color:#777'>{nn}</td></tr>")
    html.append("</table>")
    html.append(legend_html(D.COFFEE_NOTES, "Coffee-machine notes (150-demo sheets)",
                            grasp_legend))

    # --- 50-demo dataset (new) ---
    html.append("<h3>50-demo dataset</h3>")
    html.append("<p class='note'>Smaller training set. Note numbers here use the "
                "<b>50-demo legend</b> below (different from the 150-demo legend above).</p>")
    html.append(f"<h4 style='margin:14px 0 4px;color:#aebfe6;font-size:14.5px'>4×4 VLA "
                f"<span class='szb'>@ 50 demos</span> &nbsp;<span class='note'>"
                f"({p4_50}/{n4_50} = {100*p4_50/n4_50:.0f}%)</span></h4>")
    html.append(coffee_block(D.coffee_4x4_vla_50))
    html.append(f"<h4 style='margin:18px 0 4px;color:#aebfe6;font-size:14.5px'>1×1 VLA "
                f"<span class='szb'>@ 50 demos</span> &nbsp;<span class='note'>"
                f"({p1_50}/{n1_50} = {100*p1_50/n1_50:.0f}%)</span></h4>")
    html.append(coffee_block(D.coffee_1x1_vla_50))
    html.append(legend_html(D.COFFEE_NOTES_50, "Coffee-machine notes (50-demo sheets)"))

    html.append("<p class='note'>Codes — Cups: WB White-Basic, O Orange, Bk Black, "
                "R Red (ID); Br Brown, WC White-Ceramic, Gr Gray, P Pink (OOD). "
                "Machines: K Keurig, Bk Black, T Teal, W White (ID); R Red, "
                "TS Tastyle, Bl Blue (OOD).</p>")
    html.append(empty_templates_html("coffee"))

    # Task 2 pouring
    html.append("<h2>Task 2 — Cup Pouring (into bowl)</h2>")
    html.append(ds_label_html("pouring"))
    html.append(f"<h3>5×3 VLA <span class='szb'>@ 105 demos</span> &nbsp;"
                f"<span class='note'>({pp}/{np_} = {100*pp/np_:.0f}%; "
                f"*Tall-White-Ceramic column shown but not scored)</span></h3>")
    html.append(pouring_block(D.pouring_4x4_vla))
    html.append(legend_html(D.POUR_NOTES, "Pouring notes", grasp_legend))
    html.append("<p class='note'>Codes — Cups: WB White-Basic, O Orange, Bk Black, "
                "R Red, TWC Tall-White-Ceramic* (ID box); Br Brown, WC White-Ceramic, "
                "Gr Gray, P Pink (OOD). Bowls: BL Blue, LB Light-Blue, BK Black (ID); "
                "P Pink, TB Tall, W White (OOD).</p>")
    html.append(empty_templates_html("pouring"))

    # Task 3 mug tree
    pmo, nmo = mugtree_rate({"id_cup": D.mugtree_5x1_vla["od_cup"]},
                            scored=["Br", "WC", "Gr", "P", "Pu"])
    html.append("<h2>Task 3 — Hang Cup on Mug Tree</h2>")
    html.append(ds_label_html("mugtree"))
    html.append(f"<h3>5×1 VLA <span class='szb'>@ 150 demos</span> &nbsp;"
                f"<span class='note'>(ID cups {pm}/{nm} = {100*pm/nm:.0f}%; "
                f"5 trials per cup; *Tall-White-Ceramic shown but not scored)</span></h3>")
    html.append("<p class='note'>One object axis — the mug tree is fixed, so each cup is "
                "run 5 times. No grasp tag was recorded for this task. "
                "Eval is <b>complete</b> per the training tracker.</p>")
    html.append("<h4 style='margin:14px 0 4px;color:#aebfe6;font-size:14px'>ID cups</h4>")
    html.append(mugtree_table(D.mugtree_5x1_vla["id_cup"]))
    html.append(f"<h4 style='margin:18px 0 4px;color:#aebfe6;font-size:14px'>OOD cups "
                f"<span class='note'>({pmo}/{nmo} = {100*pmo/nmo:.0f}% so far)</span></h4>")
    html.append(mugtree_table(D.mugtree_5x1_vla["od_cup"], skip_blank=True))
    html.append("<p class='note'>All five OOD cups (Brown, White-Ceramic, Gray, Pink, "
                "Purple) have now been run.</p>")
    html.append(legend_html(D.MUGTREE_NOTES, "Mug-tree notes"))
    html.append("<p class='note'>Codes — Cups: WB White-Basic, O Orange, Bk Black, "
                "R Red, TWC Tall-White-Ceramic* (ID); Br Brown, WC White-Ceramic, "
                "Gr Gray, P Pink, Pu Purple (OOD).</p>")
    html.append(empty_templates_html("mugtree"))

    # appendix A (collapsible, closed by default)
    html.append("<details class='appendix'><summary>Appendix A — Coffee 4×4 VLA @ 150 "
                "demos (OLD run)"
                f"<span class='tag'>{po}/{no} · {100*po/no:.0f}%</span></summary>"
                "<div class='inner'>")
    html.append(f"<p class='note'>Earlier run; Blue (OOD) machine not yet available, so "
                f"those cells are blank. Overall {po}/{no} = {100*po/no:.0f}% of run trials.</p>")
    html.append(coffee_block(D.coffee_4x4_vla_old))
    html.append("</div></details>")

    # appendix B — planned SAP baseline (pending)
    html.append("<details class='appendix'><summary>Appendix B — Planned baseline: SAP "
                f"(no data yet)<span class='tag'>{len(D.PLANNED_BASELINES)} configs</span>"
                "</summary><div class='inner'>")
    html.append("<div class='pending'>SAP is the planned secondary baseline. Blank "
                "evaluation templates exist for both configs; results not yet recorded:<br>" +
                "".join(f"<span class='kk'>{a} · {pol} · {v}</span>"
                        for a, pol, v in D.PLANNED_BASELINES) + "</div>")
    html.append("</div></details>")

    # appendix C — optional baselines DP & R2R2R (may not run)
    html.append("<details class='appendix'><summary>Appendix C — Optional baselines: "
                "Diffusion Policy &amp; R2R2R (may not run)"
                f"<span class='tag'>{len(D.OPTIONAL_BASELINES)} configs</span></summary>"
                "<div class='inner'>")
    html.append("<div class='pending'>Diffusion Policy (DP) and R2R2R are kept as an "
                "<b>option</b> — we may not run these. Blank templates exist; no results:<br>" +
                "".join(f"<span class='kk'>{a} · {pol} · {v}</span>"
                        for a, pol, v in D.OPTIONAL_BASELINES) + "</div>")
    html.append("</div></details>")

    html.append("<footer>Transcribed from handwritten evaluation sheets · "
                "auto-generated report</footer>")
    html.append("</div></body></html>")
    with open("index.html", "w") as f:
        f.write("".join(html))
    return (p1, n1, p4, n4, pp, np_, po, no)


# ===========================================================================
# Markdown (Notion)
# ===========================================================================
def md_cell(cell):
    if cell is None:
        return "—"
    res, grasp, notes = cell
    mark = "✅" if res == "P" else "❌"
    s = mark
    if grasp:
        s += f" {grasp}"
    if notes:
        s += f" ({notes_str(notes)})"
    return s

def md_table(grid, cups, rows, cup_names, row_names, rowhdr):
    head = "| " + rowhdr + " | " + " | ".join(cup_names[c] for c in cups) + " |"
    sep = "| " + " | ".join(["---"] * (len(cups) + 1)) + " |"
    lines = [head, sep]
    for r in rows:
        row = grid[r]
        lines.append("| **" + row_names[r] + "** | " +
                     " | ".join(md_cell(row[c]) for c in cups) + " |")
    return "\n".join(lines)

def md_run(run, task, cups_id, cups_od, rows_id, rows_od, cup_names, row_names,
           rowhdr, scored=None):
    out = []
    for cond in ("id_id", "id_od", "od_id", "od_od"):
        if cond not in run:
            continue
        cups = cups_id if cond.startswith("id") else cups_od
        rows = rows_id if cond.endswith("id") else rows_od
        p, n = rate(grid_cells(run[cond], scored))
        pct = f"{100*p/n:.0f}%" if n else "—"
        label = COND_LABELS[cond][0 if task == "coffee" else 1]
        out.append(f"**{label}** — {p}/{n} ({pct})\n")
        out.append(md_table(run[cond], cups, rows, cup_names, row_names, rowhdr))
        out.append("")
    return "\n".join(out)

def md_coffee(run, scored=None):
    return md_run(run, "coffee", D.CUPS_ID, D.CUPS_OOD, D.MACH_ID, D.MACH_OOD,
                  D.CUP_NAMES, D.MACH_NAMES, "Machine ↓ / Cup →", scored)

def md_pouring(run):
    return md_run(run, "pour", D.POUR_CUPS_ID, D.POUR_CUPS_OOD, D.BOWLS_ID,
                  D.BOWLS_OOD, {**D.CUP_NAMES, "TWC": "Tall W.C."}, D.BOWL_NAMES,
                  "Bowl ↓ / Cup →",
                  scored=["WB", "O", "Bk", "R", "Br", "WC", "Gr", "P"])

def md_mugtree(cells_by_cup, skip_blank=False):
    lines = ["| Cup ↓ / Trial → | 1 | 2 | 3 | 4 | 5 | Rate |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for cup, trs in cells_by_cup.items():
        p, n = rate(trs)
        if skip_blank and n == 0:
            continue
        pct = f"{100*p/n:.0f}% ({p}/{n})" if n else "—"
        nm = D.CUP_NAMES[cup] + (" *" if cup == "TWC" else "")
        lines.append(f"| **{nm}** | " + " | ".join(md_cell(c) for c in trs) +
                     f" | {pct} |")
    return "\n".join(lines)

def md_train_runs():
    lines = ["| Dataset | Size | Train | Computer | Done | Eval | On xArm |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for model, ds, size, train, comp, done, ev, xarm in D.TRAIN_RUNS:
        evtxt = {"Yes": "✅ done", "No": "❌", "In Progress": "◑ in progress",
                 "": "—"}.get(ev, ev)
        lines.append(f"| {ds} | {size} | {train or '—'} | {comp or '—'} | "
                     f"{done or '—'} | {evtxt} | {'✓' if xarm else '—'} |")
    return "\n".join(lines)

def md_notes(notes, title, grasp=False):
    lines = [f"**{title}:**"]
    for k, v in notes.items():
        lines.append(f"- {k}. {v}" if isinstance(k, int) else f"- **{k}** {v}")
    if grasp:
        lines.append("- **Grasp:** S = side grasp, T = top grasp.")
    return "\n".join(lines)

def md_empty_grid(cols, rows, col_names, row_names, rowhdr):
    head = "| " + rowhdr + " | " + " | ".join(col_names[c] for c in cols) + " |"
    sep = "| " + " | ".join(["---"] * (len(cols) + 1)) + " |"
    lines = [head, sep]
    for r in rows:
        lines.append("| **" + row_names[r] + "** | " +
                     " | ".join("" for _ in cols) + " |")
    return "\n".join(lines)

def md_empty_mugtree(cups):
    lines = ["| Cup ↓ / Trial → | 1 | 2 | 3 | 4 | 5 | Rate |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for cup in cups:
        nm = D.CUP_NAMES[cup] + (" *" if cup == "TWC" else "")
        lines.append("| **" + nm + "** | " + " | ".join("" for _ in range(6)) + " |")
    return "\n".join(lines)

def md_empty_templates():
    """Appendix of blank grids for each not-yet-evaluated dataset size."""
    tasks = [
        ("coffee", [("1×1", "Mug/Machine 1by1"), ("4×4", "Mug/Machine 4by4")]),
        ("pouring", [("5×3", "Pour Task")]),
        ("mugtree", [("5×1", "Mug Tree Task")]),
    ]
    out = []
    for task_key, variants in tasks:
        name, _ds, _v, sizes = (D.TASK_CONFIG[task_key][0],) + D.TASK_CONFIG[task_key][1:]
        for vlabel, dsname in variants:
            for size in pending_sizes(dsname, sizes):
                out.append(f"### {name} — {vlabel} VLA @ {size} demos (blank)\n")
                if task_key == "coffee":
                    for cond, rows, cols in COFFEE_CONDS:
                        out.append(f"**{COND_LABELS[cond][0]}**\n")
                        out.append(md_empty_grid(cols, rows, D.CUP_NAMES,
                                                 D.MACH_NAMES, "Machine ↓ / Cup →"))
                        out.append("")
                elif task_key == "pouring":
                    names = {**D.CUP_NAMES, "TWC": "Tall W.C."}
                    for cond, rows, cols in POUR_CONDS:
                        out.append(f"**{COND_LABELS[cond][1]}**\n")
                        out.append(md_empty_grid(cols, rows, names,
                                                 D.BOWL_NAMES, "Bowl ↓ / Cup →"))
                        out.append("")
                else:
                    out.append("**ID cups**\n")
                    out.append(md_empty_mugtree(D.MUGTREE_CUPS_ID))
                    out.append("\n**OOD cups**\n")
                    out.append(md_empty_mugtree(D.MUGTREE_CUPS_OOD))
                    out.append("")
    return "\n".join(out)

def build_md(stats):
    p1, n1, p4, n4, pp, np_, po, no = stats
    m = []
    m.append("# Semantic Manipulation — Evaluation Results\n")
    pm, nm = mugtree_rate(D.mugtree_5x1_vla, scored=["WB", "O", "Bk", "R"])
    pmo, nmo = mugtree_rate({"id_cup": D.mugtree_5x1_vla["od_cup"]},
                            scored=["Br", "WC", "Gr", "P", "Pu"])
    p1_50, n1_50 = run_rate(D.coffee_1x1_vla_50)
    p4_50, n4_50 = run_rate(D.coffee_4x4_vla_50)
    m.append("**Arm:** xArm  ·  **Policy:** VLA  ·  **Datasets:** coffee 1×1 & 4×4, "
             "pouring 5×3, mug-tree 5×1  ·  **Training sizes:** 50 / ~100 / 150 demos "
             "(coffee @50 & @150, pouring @105, mug-tree @150 filled)\n")
    m.append("Legend: ✅ success · ❌ failure · grasp **S**=side / **T**=top · "
             "`(n)` = note number (see Legends). ID = in-distribution, "
             "OOD = out-of-distribution.\n")

    m.append("## Task suite\n")
    m.append("_Seven teleoperated tasks collected on the xArm. Config = object-variation "
             "grid; Variations = distinct object pairings; Avg teleop/demo = mean time to "
             "teleoperate one demo. Tasks 1–3 have eval grids below; the rest are collected, "
             "eval pending._\n")
    m.append("| # | Task | Objects | Config | Variations | Avg teleop/demo | In report |")
    m.append("| --- | --- | --- | --- | --- | --- | --- |")
    for i, (task, objs, cfg, variations, secs, inrep) in enumerate(TASK_SUITE, 1):
        m.append(f"| {i} | **{task}** | {objs} | {cfg} | {variations} | ~{secs}s | "
                 f"{'✅ below' if inrep else 'collected'} |")
    m.append("")

    m.append("## Summary — success rate by condition\n")
    m.append("| Run | ID/ID | ID/OOD | OOD/ID | OOD/OOD | Overall |")
    m.append("| --- | --- | --- | --- | --- | --- |")
    for name, run, scored in [
        ("Coffee · 4×4 VLA · @150", D.coffee_4x4_vla, None),
        ("Coffee · 4×4 VLA · @50", D.coffee_4x4_vla_50, None),
        ("Coffee · 1×1 VLA · @150", D.coffee_1x1_vla, None),
        ("Coffee · 1×1 VLA · @50", D.coffee_1x1_vla_50, None),
        ("Pouring · 5×3 VLA · @105", D.pouring_4x4_vla,
         ["WB", "O", "Bk", "R", "Br", "WC", "Gr", "P"]),
    ]:
        cells = []
        tp = tn = 0
        for c in ("id_id", "id_od", "od_id", "od_od"):
            p, n = rate(grid_cells(run[c], scored)) if c in run else (0, 0)
            tp += p; tn += n
            cells.append(f"{100*p/n:.0f}% ({p}/{n})" if n else "—")
        cells.append(f"**{100*tp/tn:.0f}% ({tp}/{tn})**" if tn else "—")
        m.append(f"| **{name}** | " + " | ".join(cells) + " |")
    m.append("")
    m.append(f"_Dataset-size scaling (coffee): 4×4 climbs {100*p4_50/n4_50:.0f}% → "
             f"{100*p4/n4:.0f}% (50→150 demos); 1×1 stays low "
             f"({100*p1_50/n1_50:.0f}% → {100*p1/n1:.0f}%)._\n")
    m.append(f"_Mug Tree · 5×1 VLA: ID cups {pm}/{nm} ({100*pm/nm:.0f}%) + OOD cups "
             f"{pmo}/{nmo} ({100*pmo/nmo:.0f}%) so far — single object axis, shown in "
             "Task 3._\n")

    m.append("## Training runs & dataset sizes\n")
    m.append("_Cross-listed with **Model Train Baselines**. Each task is trained at "
             "50 / ~100 / 150 demos. The eval-complete rows match the grids in this report: "
             "Coffee 1×1 & 4×4 @50 and @150, Pour @105, Mug-Tree @150._\n")
    m.append(md_train_runs())
    m.append("")

    m.append("## Task 1 — Cup on Coffee Machine\n")
    m.append("_Dataset **Mug/Machine** · config 1×1 & 4×4 · trained at 50 / ~100 / 150 "
             "demos (50 & 150 filled; 100 pending)._\n")

    m.append("### 150-demo dataset\n")
    m.append(f"#### 4×4 VLA @ 150 demos — {p4}/{n4} ({100*p4/n4:.0f}%)\n")
    m.append(md_coffee(D.coffee_4x4_vla))
    m.append(f"#### 1×1 VLA @ 150 demos — {p1}/{n1} ({100*p1/n1:.0f}%)\n")
    m.append("_Single-view model fails nearly everything; only successes are on the "
             "OOD (taller-clearance) machines._\n")
    m.append(md_coffee(D.coffee_1x1_vla))
    m.append("#### 1×1 VLA — White-Basic re-run (supplementary)\n")
    m.append("| Machine | Result | Grasp | Notes |")
    m.append("| --- | --- | --- | --- |")
    for cond in ("id_id", "id_od"):
        for mc, cell in D.coffee_1x1_vla_wb_redo[cond].items():
            res, grasp, notes = cell
            mark = "✅" if res == "P" else "❌"
            nn = ", ".join(str(x) for x in notes) if notes else ""
            m.append(f"| WB / {D.MACH_NAMES[mc]} | {mark} | {grasp} | {nn} |")
    m.append("")
    m.append(md_notes(D.COFFEE_NOTES, "Coffee-machine notes (150-demo sheets)", grasp=True))
    m.append("")

    m.append("### 50-demo dataset\n")
    m.append("_Smaller training set; note numbers use the **50-demo legend** below._\n")
    m.append(f"#### 4×4 VLA @ 50 demos — {p4_50}/{n4_50} ({100*p4_50/n4_50:.0f}%)\n")
    m.append(md_coffee(D.coffee_4x4_vla_50))
    m.append(f"#### 1×1 VLA @ 50 demos — {p1_50}/{n1_50} ({100*p1_50/n1_50:.0f}%)\n")
    m.append(md_coffee(D.coffee_1x1_vla_50))
    m.append(md_notes(D.COFFEE_NOTES_50, "Coffee-machine notes (50-demo sheets)"))
    m.append("\n_Codes — Cups: WB White-Basic, O Orange, Bk Black, R Red (ID); "
             "Br Brown, WC White-Ceramic, Gr Gray, P Pink (OOD). Machines: K Keurig, "
             "Bk Black, T Teal, W White (ID); R Red, TS Tastyle, Bl Blue (OOD)._\n")

    m.append("## Task 2 — Cup Pouring (into bowl)\n")
    m.append("_Dataset **Pour Task** · config 5×3 · trained at 50 / ~105 / 150 demos "
             "(grid shown = 105-demo model)._\n")
    m.append(f"### 5×3 VLA @ 105 demos — {pp}/{np_} ({100*pp/np_:.0f}%)\n")
    m.append("_Tall-White-Ceramic (Tall W.C.) column is an extra OOD cup — shown but "
             "not counted in the rate._\n")
    m.append(md_pouring(D.pouring_4x4_vla))
    m.append("")
    m.append(md_notes(D.POUR_NOTES, "Pouring notes", grasp=True))
    m.append("\n_Codes — Cups: WB White-Basic, O Orange, Bk Black, R Red, "
             "TWC Tall-White-Ceramic* (ID box); Br Brown, WC White-Ceramic, Gr Gray, "
             "P Pink (OOD). Bowls: BL Blue, LB Light-Blue, BK Black (ID); P Pink, "
             "TB Tall, W White (OOD)._\n")

    m.append("## Task 3 — Hang Cup on Mug Tree\n")
    m.append("_Dataset **Mug Tree Task** · config 5×1 · trained at 50 / ~100 / 150 demos "
             "· eval complete._\n")
    m.append(f"### 5×1 VLA @ 150 demos — ID cups {pm}/{nm} ({100*pm/nm:.0f}%)\n")
    m.append("_One object axis (fixed mug tree): each cup is run 5 times; no grasp tag. "
             "Tall-White-Ceramic (*) shown but not scored._\n")
    m.append("**ID cups**\n")
    m.append(md_mugtree(D.mugtree_5x1_vla["id_cup"]))
    m.append("")
    m.append(f"**OOD cups** — {pmo}/{nmo} ({100*pmo/nmo:.0f}%) so far\n")
    m.append(md_mugtree(D.mugtree_5x1_vla["od_cup"], skip_blank=True))
    m.append("\n_All five OOD cups (Brown, White-Ceramic, Gray, Pink, Purple) now run._\n")
    m.append(md_notes(D.MUGTREE_NOTES, "Mug-tree notes"))
    m.append("\n_Codes — Cups: WB White-Basic, O Orange, Bk Black, R Red, "
             "TWC Tall-White-Ceramic* (ID); Br Brown, WC White-Ceramic, Gr Gray, "
             "P Pink, Pu Purple (OOD)._\n")

    m.append("## Appendix A — Coffee 4×4 VLA @ 150 demos (OLD run)\n")
    m.append(f"_Earlier run; Blue (OOD) machine not yet available (blank cells). "
             f"Overall {po}/{no} ({100*po/no:.0f}%) of run trials._\n")
    m.append(md_coffee(D.coffee_4x4_vla_old))

    m.append("## Appendix B — Planned baseline: SAP (no data yet)\n")
    m.append("SAP is the planned secondary baseline; blank templates exist, no results:\n")
    for a, pol, v in D.PLANNED_BASELINES:
        m.append(f"- {a} · {pol} · {v}")
    m.append("")

    m.append("## Appendix C — Optional baselines: Diffusion Policy & R2R2R (may not run)\n")
    m.append("DP and R2R2R are kept as an **option** — we may not run these:\n")
    for a, pol, v in D.OPTIONAL_BASELINES:
        m.append(f"- {a} · {pol} · {v}")
    m.append("")

    m.append("## Appendix D — Empty grids for pending dataset sizes (fill in later)\n")
    m.append("_Blank templates for the dataset sizes not yet evaluated; fill in as each "
             "eval completes (sizes already done are omitted)._\n")
    m.append(md_empty_templates())

    with open("report.md", "w") as f:
        f.write("\n".join(m))


if __name__ == "__main__":
    stats = build_html()
    build_md(stats)
    print("wrote index.html and report.md")
    p1, n1, p4, n4, pp, np_, po, no = stats
    print("Coffee 1x1 VLA: %d/%d | 4x4 VLA: %d/%d | Pouring: %d/%d | OLD: %d/%d"
          % (p1, n1, p4, n4, pp, np_, po, no))
