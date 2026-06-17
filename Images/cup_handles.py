"""Auto-detect cup handle and trace an outline. Render previews for review."""
import os, json, numpy as np, cv2
from PIL import Image

CUPS = ["cup_white_basic","cup_orange","cup_black","cup_red",
        "cup_brown","cup_gray","cup_pink","cup_white_ceramic"]

ACCENT = (209, 73, 91)  # crimson (RGB)

def _largest_contour(mask):
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return max(cnts, key=cv2.contourArea) if cnts else None

def handle_geometry(name, rfrac=0.12, margin=10):
    """Trace handle = outer protrusion arc + inner aperture (hole)."""
    from scipy import ndimage
    im = Image.open(f"cutouts/{name}.png").convert("RGBA")
    alpha = np.array(im)[:, :, 3]
    H, W = alpha.shape
    M = (alpha > 20).astype(np.uint8)

    r = max(8, int(rfrac * W))
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*r+1, 2*r+1))
    B = cv2.morphologyEx(M, cv2.MORPH_OPEN, k)        # body (handle removed)
    Bdil = cv2.dilate(B, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*margin+1, 2*margin+1)))

    polylines = []

    # 1) inner aperture = enclosed hole(s) of the silhouette, on the right side
    filled = ndimage.binary_fill_holes(M).astype(np.uint8)
    holes = cv2.subtract(filled, M)
    nh, lh, sh, ch = cv2.connectedComponentsWithStats(holes, 8)
    hx0, hy0, hx1, hy1 = W, H, 0, 0
    found_hole = False
    for i in range(1, nh):
        if sh[i, cv2.CC_STAT_AREA] > 0.001*H*W and ch[i][0] > 0.45*W:
            hole = (lh == i).astype(np.uint8)
            c = _largest_contour(hole)
            if c is not None:
                polylines.append((c.reshape(-1, 2), True))
                x, y, w, h = sh[i, 0], sh[i, 1], sh[i, 2], sh[i, 3]
                hx0, hy0, hx1, hy1 = min(hx0, x), min(hy0, y), max(hx1, x+w), max(hy1, y+h)
                found_hole = True
    if found_hole:                       # gating box for the outer arc = handle region
        px, py = int(0.18*W), int(0.10*H)
        gate = (hx0-px, hy0-py, W, hy1+py)
    else:
        gate = (int(0.5*W), int(0.20*H), W, int(0.85*H))

    # handle material (ribbon) mask for low-opacity fill
    handle_mat = cv2.morphologyEx(cv2.subtract(M, B), cv2.MORPH_OPEN,
                                  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    nm, lm, sm, cm = cv2.connectedComponentsWithStats(handle_mat, 8)
    best, bestscore = 0, -1
    for i in range(1, nm):
        score = sm[i, cv2.CC_STAT_AREA] * (1.0 + cm[i][0]/W)
        if sm[i, cv2.CC_STAT_AREA] > 0.002*H*W and score > bestscore:
            bestscore, best = score, i
    fillmask = (lm == best).astype(np.uint8) if best else np.zeros_like(M)

    # 2) outer handle arc = outer silhouette points beyond the body, within handle region
    c = _largest_contour(M)
    if c is not None:
        pts = c.reshape(-1, 2)
        gx0, gy0, gx1, gy1 = gate
        keep = np.array([(Bdil[min(int(y),H-1), min(int(x),W-1)] == 0)
                         and (gx0 <= x <= gx1) and (gy0 <= y <= gy1)
                         for x, y in pts])
        # contour is a closed loop; rotate so a False is at the seam, then split runs
        if keep.any() and not keep.all():
            start = np.argmax(~keep)
            pts = np.roll(pts, -start, axis=0)
            keep = np.roll(keep, -start)
            run = []
            for p, kp in zip(pts, keep):
                if kp:
                    run.append(p)
                elif run:
                    if len(run) > 8: polylines.append((np.array(run), False))
                    run = []
            if len(run) > 8: polylines.append((np.array(run), False))
    return im, polylines, fillmask

def render(name, polylines, lw=6, on_white=True):
    im, _ = (Image.open(f"cutouts/{name}.png").convert("RGBA"), None)
    base = Image.new("RGBA", im.size, (255,255,255,255) if on_white else (200,255,200,255))
    base.alpha_composite(im)
    arr = np.array(base.convert("RGB"))
    col = (ACCENT[2], ACCENT[1], ACCENT[0])  # BGR for cv2
    arr = arr[:, :, ::-1].copy()
    for pts, closed in polylines:
        # smooth
        p = pts.astype(np.int32).reshape(-1,1,2)
        cv2.polylines(arr, [p], closed, col, lw, cv2.LINE_AA)
    arr = arr[:, :, ::-1]
    return Image.fromarray(arr)

if __name__ == "__main__":
    import math
    cell=380; cols=4; rows=2
    Mt=Image.new("RGB",(cols*cell, rows*cell),(245,245,245))
    from PIL import ImageDraw
    d=ImageDraw.Draw(Mt)
    for i,n in enumerate(CUPS):
        im, pls, _fm = handle_geometry(n)
        prev = render(n, pls, lw=6)
        prev.thumbnail((cell-20,cell-40))
        r,c=divmod(i,cols)
        x=c*cell+(cell-prev.width)//2; y=r*cell+(cell-40-prev.height)//2+8
        Mt.paste(prev,(x,y))
        d.text((c*cell+6,r*cell+cell-20), f"{n} ({len(pls)} seg)", fill=(0,0,0))
    Mt.save("_thumbs/handles_review.png")
    print("ok", Mt.size)
