"""Compose the cup/machine overview figure (double- and single-column variants).
Pure white background, Liberation Sans (Arial-metric) labels, subtle contact
shadow so light objects read on white, ID/OOD sub-rows, and a highlight legend."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import features

SANS      = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_IT   = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

INK   = (20, 20, 20)
SUB   = (70, 70, 70)
RULE  = (180, 180, 180)

GROUPS = {
    "cups_id":  [("cup_white_basic","White"),("cup_orange","Orange"),
                 ("cup_black","Black"),("cup_red","Red")],
    "cups_ood": [("cup_brown","Brown"),("cup_gray","Gray"),
                 ("cup_pink","Pink"),("cup_white_ceramic","White (ceramic)")],
    "mach_id":  [("machine_keurig","Keurig"),("machine_black","Black"),
                 ("machine_cyan","Teal"),("machine_white","White")],
    "mach_ood": [("machine_red","Red"),("machine_tastyle","Tastyle"),
                 ("machine_blue","Blue")],
}

# Hand-highlighted machine PNGs (clearance region filled in PowerPoint).
# Note machine_cyan -> teal_highlight.
HIGHLIGHT_MACHINE = {
    "machine_keurig": "keurig", "machine_black": "black", "machine_cyan": "teal",
    "machine_white": "white", "machine_red": "red", "machine_tastyle": "tastyle",
    "machine_blue": "blue",
}

def _tight(img):
    """Crop an RGBA image to its alpha bounding box."""
    a = np.array(img)[:, :, 3]
    ys, xs = np.where(a > 10)
    if len(ys) == 0:
        return img
    return img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

_render_cache = {}
def get_obj(name, shadow=True):
    if name in _render_cache:
        return _render_cache[name]
    if name in HIGHLIGHT_MACHINE:
        img = _tight(Image.open(
            f"highlight_machine/{HIGHLIGHT_MACHINE[name]}_highlight_outline.png").convert("RGBA"))
    else:
        img = features.render(name).convert("RGBA")   # cup: cyan handle highlight
    if shadow:
        img = with_shadow(img)
    _render_cache[name] = img
    return img

def with_shadow(img, opacity=0.20):
    W, H = img.size
    blur = max(6, int(0.018*H)); dy = int(0.012*H); pad = int(blur*3)+dy
    canvas = Image.new("RGBA", (W+2*pad, H+2*pad), (0,0,0,0))
    a = img.split()[3]
    sa = Image.new("L", canvas.size, 0)
    sa.paste(a, (pad, pad+dy))
    sa = sa.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v*opacity))
    sh = Image.new("RGBA", canvas.size, (30,30,30,0)); sh.putalpha(sa)
    canvas = Image.alpha_composite(canvas, sh)
    canvas.alpha_composite(img, (pad, pad))
    # remember where the real object bottom is (for baseline alignment)
    canvas.info["obj_bottom"] = pad + H
    return canvas

def font(path, size): return ImageFont.truetype(path, size)
def tsize(d, s, f):
    b = d.textbbox((0,0), s, font=f); return b[2]-b[0], b[3]-b[1]

def fit_font(d, text, path, max_w, start):
    s = start
    while s > 8:
        f = font(path, s)
        if tsize(d, text, f)[0] <= max_w: return f
        s -= 1
    return font(path, 8)

def render_panel(sections, title, panel_w, fs, n_cols=None, colpad_frac=0.10,
                 uniform=False):
    """sections: list of (subheader, [(name,label),...]). Returns RGBA panel image."""
    items = [it for _, sec in sections for it in sec]
    if n_cols is None:
        n_cols = max(len(sec) for _, sec in sections)
    objs = {nm: get_obj(nm) for nm, _ in items}
    if uniform:
        # normalize every object to the same display height (shadow height ~
        # proportional to content height, so this equalizes apparent size)
        Th = max(o.height for o in objs.values())
        prescale = {nm: Th / o.height for nm, o in objs.items()}
    else:
        prescale = {nm: 1.0 for nm in objs}
    base = {nm: (o.width*prescale[nm], o.height*prescale[nm]) for nm, o in objs.items()}
    max_w = max(b[0] for b in base.values())
    max_h = max(b[1] for b in base.values())
    col_w = panel_w / n_cols
    colpad = col_w * colpad_frac
    scale = (col_w - 2*colpad) / max_w
    obj_area_h = max_h * scale

    f_title = font(SANS_BOLD, fs["title"])
    f_sub   = font(SANS_BOLD, fs["sub"])
    f_lab   = font(SANS, fs["label"])

    tmp = Image.new("RGBA", (panel_w, 10)); d0 = ImageDraw.Draw(tmp)
    title_h = tsize(d0, title, f_title)[1]
    sub_h   = tsize(d0, "In-distribution", f_sub)[1]
    lab_h   = tsize(d0, "Ag", f_lab)[1]

    pad_title = int(fs["title"]*0.7)
    pad_sub   = int(fs["sub"]*0.55)
    pad_lab   = int(fs["label"]*0.5)
    pad_row   = int(fs["label"]*1.4)

    # measure total height
    y = 0
    y += title_h + pad_title
    for sh_text, sec in sections:
        y += sub_h + pad_sub
        y += obj_area_h + pad_lab + lab_h + pad_row
    panel_h = int(y) + 4

    panel = Image.new("RGBA", (panel_w, panel_h), (0,0,0,0))
    d = ImageDraw.Draw(panel)

    y = 0
    tw = tsize(d, title, f_title)[0]
    d.text(((panel_w-tw)/2, y), title, font=f_title, fill=INK)
    # rule under title
    ry = y + title_h + int(pad_title*0.45)
    d.line([(panel_w*0.12, ry),(panel_w*0.88, ry)], fill=RULE, width=2)
    y += title_h + pad_title

    for sh_text, sec in sections:
        # subheader (left) with thin rule to the right
        d.text((colpad*0.5, y), sh_text, font=f_sub, fill=SUB)
        shw = tsize(d, sh_text, f_sub)[0]
        ly = y + sub_h*0.62
        d.line([(colpad*0.5+shw+fs["sub"]*0.5, ly),(panel_w-colpad*0.5, ly)],
               fill=RULE, width=1)
        y += sub_h + pad_sub

        baseline = y + obj_area_h
        m = len(sec)
        # center a short row within the panel
        start_x = (panel_w - m*col_w)/2 if m < n_cols else 0
        for i, (nm, label) in enumerate(sec):
            o = objs[nm]
            s_i = prescale[nm] * scale
            ow, oh = max(1, int(o.width*s_i)), max(1, int(o.height*s_i))
            os_ = o.resize((ow, oh), Image.LANCZOS)
            cx = start_x + (i+0.5)*col_w
            px = int(cx - ow/2)
            py = int(baseline - oh)
            panel.alpha_composite(os_, (px, py))
            # label
            lf = fit_font(d, label, SANS, col_w-6, fs["label"])
            lw_, lh_ = tsize(d, label, lf)
            d.text((cx - lw_/2, baseline + pad_lab), label, font=lf, fill=INK)
        y = baseline + pad_lab + lab_h + pad_row

    return panel

def draw_legend(d, x, y, w, fs, items):
    """items: list of ('loop'|'trace', color, text)."""
    f = font(SANS, fs["legend"])
    sw = int(fs["legend"]*1.7)           # swatch width
    gap = int(fs["legend"]*0.5)
    lh = int(fs["legend"]*1.9)
    cy = y
    for kind, color, text in items:
        # swatch
        if kind == "loop":
            d.ellipse([x, cy, x+sw, cy+int(sw*0.95)], outline=color, width=max(3,fs["legend"]//7))
            d.ellipse([x+sw*0.30, cy+sw*0.28, x+sw*0.78, cy+sw*0.72],
                      outline=color, width=max(2,fs["legend"]//9))
        else:  # trace: a C / bracket
            cx0, cy0 = x, cy
            pts = [(x+sw*0.85, cy0+sw*0.05),(x+sw*0.30, cy0+sw*0.02),
                   (x+sw*0.08, cy0+sw*0.35),(x+sw*0.10, cy0+sw*0.80),
                   (x+sw*0.55, cy0+sw*0.95),(x+sw*0.9, cy0+sw*0.86)]
            d.line(pts, fill=color, width=max(3,fs["legend"]//6), joint="curve")
        d.text((x+sw+gap, cy+int(sw*0.08)), text, font=f, fill=INK)
        cy += lh
    return cy

def build_double(out_path, W=2150):
    margin = int(W*0.022); divider_gap = int(W*0.045)
    inner = W - 2*margin - divider_gap
    cups_w = int(inner*0.47); mach_w = inner - cups_w
    fs = dict(title=int(W*0.0225), sub=int(W*0.0150), label=int(W*0.0150),
              legend=int(W*0.0150))
    cups = render_panel(
        [("In-distribution", GROUPS["cups_id"]),
         ("Out-of-distribution", GROUPS["cups_ood"])],
        "Cups", cups_w, fs, colpad_frac=0.05)
    mach = render_panel(
        [("In-distribution", GROUPS["mach_id"]),
         ("Out-of-distribution", GROUPS["mach_ood"])],
        "Coffee Machines", mach_w, fs, colpad_frac=0.07, uniform=True)

    body_h = max(cups.height, mach.height)
    H = margin*2 + body_h
    canvas = Image.new("RGBA", (W, H), (255,255,255,255))
    d = ImageDraw.Draw(canvas)
    cx0 = margin
    mx0 = margin + cups_w + divider_gap
    canvas.alpha_composite(cups, (cx0, margin))
    canvas.alpha_composite(mach, (mx0, margin))
    # vertical divider
    dxv = margin + cups_w + divider_gap//2
    d.line([(dxv, margin+int(W*0.005)),(dxv, margin+body_h-int(W*0.005))],
           fill=RULE, width=2)
    canvas.convert("RGB").save(out_path, dpi=(300,300))
    print("wrote", out_path, canvas.size)

def build_single(out_path, W=1040):
    margin = int(W*0.03)
    inner = W - 2*margin
    fs = dict(title=int(W*0.040), sub=int(W*0.028), label=int(W*0.027),
              legend=int(W*0.028))
    cups = render_panel(
        [("In-distribution", GROUPS["cups_id"]),
         ("Out-of-distribution", GROUPS["cups_ood"])],
        "Cups", inner, fs)
    mach = render_panel(
        [("In-distribution", GROUPS["mach_id"]),
         ("Out-of-distribution", GROUPS["mach_ood"])],
        "Coffee Machines", inner, fs, uniform=True)
    gap = int(W*0.03)
    H = margin*2 + cups.height + gap + mach.height
    canvas = Image.new("RGBA", (W, int(H)), (255,255,255,255))
    d = ImageDraw.Draw(canvas)
    y = margin
    canvas.alpha_composite(cups, (margin, y)); y += cups.height + gap
    d.line([(margin, y-gap//2),(W-margin, y-gap//2)], fill=RULE, width=1)
    canvas.alpha_composite(mach, (margin, y))
    canvas.convert("RGB").save(out_path, dpi=(300,300))
    print("wrote", out_path, canvas.size)

if __name__ == "__main__":
    build_double("figure_collection_2col.png")
    build_single("figure_collection_1col.png")
