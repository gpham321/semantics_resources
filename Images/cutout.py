"""Background removal + tight crop. Source = Raw Images/, output = cutouts/."""
import os, sys
import numpy as np
from PIL import Image
from rembg import remove, new_session
import cv2

SRC = "Raw Images"
OUT = "cutouts"
os.makedirs(OUT, exist_ok=True)

LONG_SIDE = 2600  # resize long side before rembg

def process(name, sess):
    src = os.path.join(SRC, name + ".jpg")
    im = Image.open(src).convert("RGB")
    w, h = im.size
    scale = LONG_SIDE / max(w, h)
    if scale < 1:
        im = im.resize((round(w*scale), round(h*scale)), Image.LANCZOS)
    out = remove(im, session=sess, post_process_mask=True)
    rgba = np.array(out.convert("RGBA"))
    alpha = rgba[:, :, 3]

    # keep only the largest connected component (drop stray specks)
    bin_mask = (alpha > 20).astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(bin_mask, 8)
    if n > 1:
        largest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        keep = (labels == largest)
        alpha = np.where(keep, alpha, 0).astype(np.uint8)
    rgba[:, :, 3] = alpha

    ys, xs = np.where(alpha > 20)
    if len(ys) == 0:
        print(f"{name:28s} !! EMPTY MASK"); return
    pad = 8
    y0, y1 = max(ys.min()-pad, 0), min(ys.max()+pad+1, alpha.shape[0])
    x0, x1 = max(xs.min()-pad, 0), min(xs.max()+pad+1, alpha.shape[1])
    crop = rgba[y0:y1, x0:x1]
    Image.fromarray(crop).save(os.path.join(OUT, name + ".png"))
    print(f"{name:28s} cutout {crop.shape[1]}x{crop.shape[0]}")

def all_new():
    done = {os.path.splitext(f)[0] for f in os.listdir(OUT) if f.endswith(".png")}
    names = [os.path.splitext(f)[0] for f in sorted(os.listdir(SRC)) if f.lower().endswith(".jpg")]
    return [n for n in names if n not in done]

if __name__ == "__main__":
    sess = new_session("isnet-general-use")
    targets = sys.argv[1:] if len(sys.argv) > 1 else all_new()
    print(f"processing {len(targets)} items")
    for name in targets:
        process(name, sess)
