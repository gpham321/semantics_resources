"""Render highlighted cutouts:
  - cups: handle traced in cyan-blue (outline + low-opacity fill of the handle)
  - machines: the cup-clearance pocket (platform -> inner wall -> under the
              dispenser) as a contour-following FILLED region in bright green,
              low opacity, with a glowing bright-green outline.
Output = RGBA on transparent."""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
from cup_handles import handle_geometry, CUPS

CYAN = (0, 255, 255)        # #00FFFF pure cyan -- cup handles
GREEN_FILL = (90, 245, 40)  # bright green -- clearance fill
GREEN_LINE = (70, 230, 25)  # bright green -- clearance outline / glow
CASING = (255, 255, 255)
HANDLE_FILL = 0.43          # brighter handle fill (was 0.34, +25%)
REGION_FILL = 0.34          # bright but still low-opacity clearance fill
CUP_FILL_DEFAULT = False    # cups: outline the handle only (no translucent fill)
CUP_OUTLINE_MULT = 1.7      # thicken the cyan handle outline (x base line width)

MACHINES = ["machine_keurig","machine_black","machine_cyan","machine_white",
            "machine_red","machine_tastyle","machine_blue"]

# Cup-clearance pocket as a CLOSED contour (front-opening side closes back to the
# first point). Ordered top-front -> top-back(under dispenser) -> down inner wall
# -> along platform -> bottom-front. FRACTIONAL coords.
TRACE = {
    "machine_keurig":  [(0.80,0.50),(0.58,0.46),(0.45,0.47),(0.37,0.55),(0.355,0.78),
                        (0.40,0.85),(0.55,0.875),(0.80,0.865)],
    "machine_cyan":    [(0.86,0.42),(0.66,0.37),(0.55,0.40),(0.49,0.55),(0.475,0.73),
                        (0.55,0.80),(0.70,0.825),(0.84,0.795)],
    "machine_white":   [(0.87,0.43),(0.64,0.37),(0.55,0.41),(0.49,0.55),(0.475,0.72),
                        (0.55,0.785),(0.70,0.805),(0.85,0.78)],
    "machine_black":   [(0.83,0.42),(0.55,0.36),(0.40,0.40),(0.335,0.55),(0.325,0.80),
                        (0.40,0.855),(0.58,0.875),(0.83,0.85)],
    "machine_red":     [(0.55,0.46),(0.68,0.45),(0.79,0.46),(0.80,0.63),(0.79,0.79),
                        (0.72,0.85),(0.60,0.855),(0.55,0.80)],
    "machine_tastyle": [(0.88,0.45),(0.60,0.41),(0.47,0.45),(0.44,0.58),(0.445,0.85),
                        (0.52,0.905),(0.68,0.915),(0.88,0.885)],
    "machine_blue":    [(0.93,0.71),(0.81,0.71),(0.70,0.735),(0.645,0.79),(0.645,0.845),
                        (0.74,0.885),(0.89,0.88),(0.93,0.85)],
}

def _chaikin(pts, iters=3):
    pts = [tuple(p) for p in pts]
    for _ in range(iters):
        out = [pts[0]]
        for i in range(len(pts)-1):
            p, q = pts[i], pts[i+1]
            out.append((0.75*p[0]+0.25*q[0], 0.75*p[1]+0.25*q[1]))
            out.append((0.25*p[0]+0.75*q[0], 0.25*p[1]+0.75*q[1]))
        out.append(pts[-1])
        pts = out
    return np.array(pts)

def _trace_px(name, W, H):
    pts = _chaikin(TRACE[name])
    return (pts * np.array([W, H], np.float32))

def _outline(out, polys, color, lw, cas):
    H, W = out.shape[:2]
    line_rgb = np.zeros((H, W, 3), np.uint8)
    line_a = np.zeros((H, W), np.uint8)
    for pts, closed in polys:
        p = pts.astype(np.int32).reshape(-1, 1, 2)
        cv2.polylines(line_rgb, [p], closed, CASING, lw+2*cas, cv2.LINE_8)
        cv2.polylines(line_a,  [p], closed, 255,    lw+2*cas, cv2.LINE_8)
    for pts, closed in polys:
        p = pts.astype(np.int32).reshape(-1, 1, 2)
        cv2.polylines(line_rgb, [p], closed, color, lw, cv2.LINE_8)
    m = line_a > 0
    out[m, :3] = line_rgb[m]
    out[m, 3] = 255

def _fill_clipped(out, mask, color, alpha):
    rgb = out[:, :, :3].astype(np.float32)
    fm = (mask > 0) & (out[:, :, 3] > 20)
    col = np.array(color, np.float32)
    rgb[fm] = (1-alpha)*rgb[fm] + alpha*col
    out[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)

def _clearance_region(out, poly, fill_color, line_color, fill_alpha, lw, glow):
    """Fill a closed contour pocket (tints both the open cavity and any machine
    surface it overlaps) and stroke a glowing bright outline. out: HxWx4 uint8."""
    H, W = out.shape[:2]
    pts = [tuple(map(float, p)) for p in poly]
    base = Image.fromarray(out)

    # 1) translucent fill over the closed pocket (includes the open/transparent area)
    fill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(fill).polygon(pts, fill=(*fill_color, int(fill_alpha*255)))
    base = Image.alpha_composite(base, fill)

    # 2) soft outer glow
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow_layer).line(pts + [pts[0]], fill=(*line_color, 255),
                                    width=int(lw*glow), joint="curve")
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(lw*glow*0.5))
    glow_layer = Image.eval(glow_layer.split()[3], lambda a: int(a*0.7))  # dim alpha
    g = Image.new("RGBA", (W, H), (*line_color, 0)); g.putalpha(glow_layer)
    base = Image.alpha_composite(base, g)

    # 3) crisp bright outline on top
    crisp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(crisp).line(pts + [pts[0]], fill=(*line_color, 255),
                               width=lw, joint="curve")
    base = Image.alpha_composite(base, crisp)
    return np.array(base)

def render(name, scale=1.0, cup_fill=CUP_FILL_DEFAULT):
    im = Image.open(f"cutouts/{name}.png").convert("RGBA")
    out = np.array(im)
    H, W = out.shape[:2]
    lw = max(3, int(round(0.010 * min(W, H) * scale)))
    cas = max(2, int(round(lw * 0.5)))
    if name in CUPS:
        clw = max(4, int(round(lw * CUP_OUTLINE_MULT)))
        ccas = max(2, int(round(cas * CUP_OUTLINE_MULT)))
        _, polylines, fillmask = handle_geometry(name)
        if cup_fill:
            _fill_clipped(out, fillmask, CYAN, HANDLE_FILL)
        _outline(out, polylines, CYAN, clw, ccas)
        return Image.fromarray(out)
    else:
        trace = _trace_px(name, W, H)
        out = _clearance_region(out, trace, GREEN_FILL, GREEN_LINE,
                                REGION_FILL, lw, glow=3.0)
        return Image.fromarray(out)

def on_white(img):
    bg = Image.new("RGBA", img.size, (255,255,255,255)); bg.alpha_composite(img)
    return bg.convert("RGB")

if __name__ == "__main__":
    import sys
    targets = sys.argv[1:] or MACHINES
    for n in targets:
        on_white(render(n)).save(f"_thumbs/feat_{n}.png")
        print("rendered", n)
