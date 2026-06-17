"""Background removal for the robot grasp + task scene photos: strips the wood
table and cardboard wall, keeping the robot arm + task items. Outputs transparent
PNGs to Grasp/masked/ and Tasks/masked/, plus light-bg previews to _thumbs/.

Scenes often contain a held object (in the gripper, connected to the arm) AND a
separate object on the table (bowl, drawer, mouse pad, faucet, coaster) — so we
keep every connected component whose area is a meaningful fraction of the largest,
not just the single largest blob. Stray shadow specks are dropped."""
import os, sys
import numpy as np
from PIL import Image
from rembg import remove, new_session
import cv2

MODEL = "birefnet-general"  # full-scene segmentation (keeps low-contrast white arm)
LONG_SIDE = 2000          # resize long side before rembg / output res
KEEP_FRAC = 0.012         # keep components >= this fraction of the largest area
KEEP_ABS  = 1500          # ...and at least this many px (at LONG_SIDE scale)
PAD = 10

JOBS = [
    ("Grasp/side_grasp.jpg",          "Grasp/masked/side_grasp.png"),
    ("Grasp/top_grasp.jpg",           "Grasp/masked/top_grasp.png"),
    ("Tasks/cup_coffee_machine.jpg",  "Tasks/masked/cup_coffee_machine.png"),
    ("Tasks/pour.jpg",                "Tasks/masked/pour.png"),
    ("Tasks/bottle-can_coaster.jpg",  "Tasks/masked/bottle-can_coaster.png"),
    ("Tasks/faucet.jpg",              "Tasks/masked/faucet.png"),
    ("Tasks/power_brick_drawer.jpg",  "Tasks/masked/power_brick_drawer.png"),
    ("Tasks/powerdrill_pad.jpg",      "Tasks/masked/powerdrill_pad.png"),
    ("Tasks/mug_tree.jpg",            "Tasks/masked/mug_tree.png"),
]

def process(src, dst, sess):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    s = LONG_SIDE / max(w, h)
    if s < 1:
        im = im.resize((round(w*s), round(h*s)), Image.LANCZOS)
    out = remove(im, session=sess, post_process_mask=True)
    rgba = np.array(out.convert("RGBA"))
    alpha = rgba[:, :, 3]

    bm = (alpha > 20).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(bm, 8)
    if n > 1:
        areas = stats[1:, cv2.CC_STAT_AREA]
        amax = areas.max()
        thr = max(KEEP_ABS, KEEP_FRAC * amax)
        keep_ids = [i+1 for i, a in enumerate(areas) if a >= thr]
        keep = np.isin(lab, keep_ids)
        alpha = np.where(keep, alpha, 0).astype(np.uint8)
        ncomp = len(keep_ids)
    else:
        ncomp = 0
    rgba[:, :, 3] = alpha

    ys, xs = np.where(alpha > 20)
    if len(ys) == 0:
        print(f"{os.path.basename(src):26s} !! EMPTY"); return
    y0, y1 = max(ys.min()-PAD, 0), min(ys.max()+PAD+1, alpha.shape[0])
    x0, x1 = max(xs.min()-PAD, 0), min(xs.max()+PAD+1, alpha.shape[1])
    crop = rgba[y0:y1, x0:x1]
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    Image.fromarray(crop).save(dst)

    # light-bg preview for inspection
    base = os.path.splitext(os.path.basename(dst))[0]
    bg = np.full_like(crop, 240); bg[:, :, 3] = 255
    a = crop[:, :, 3:4] / 255.0
    comp = (crop[:, :, :3]*a + bg[:, :, :3]*(1-a)).astype(np.uint8)
    os.makedirs("_thumbs", exist_ok=True)
    Image.fromarray(comp).save(f"_thumbs/mask_{base}.png")
    print(f"{os.path.basename(src):26s} {crop.shape[1]}x{crop.shape[0]}  comps={ncomp}")

if __name__ == "__main__":
    sess = new_session(MODEL)
    jobs = JOBS
    if len(sys.argv) > 1:
        sel = set(sys.argv[1:])
        jobs = [j for j in JOBS if any(s in j[0] for s in sel)]
    for src, dst in jobs:
        process(src, dst, sess)
