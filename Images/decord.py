"""Remove trailing power cords from machine cutouts via morphological opening."""
import sys, numpy as np, cv2
from PIL import Image

def decord(name, R=14):
    im = Image.open(f"cutouts/{name}.png").convert("RGBA")
    rgba = np.array(im)
    alpha = rgba[:, :, 3]
    mask = (alpha > 20).astype(np.uint8)

    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*R+1, 2*R+1))
    eroded = cv2.erode(mask, k)
    # keep largest connected component of the eroded core (drops severed cord/plug)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(eroded, 8)
    if n > 1:
        largest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        core = (labels == largest).astype(np.uint8)
    else:
        core = eroded
    body = cv2.dilate(core, k)               # regrow body to ~original boundary
    body = cv2.morphologyEx(body, cv2.MORPH_CLOSE, k)
    alpha2 = np.where(body > 0, alpha, 0).astype(np.uint8)
    rgba[:, :, 3] = alpha2

    # tight re-crop
    ys, xs = np.where(alpha2 > 20)
    pad = 8
    y0, y1 = max(ys.min()-pad,0), min(ys.max()+pad+1, alpha2.shape[0])
    x0, x1 = max(xs.min()-pad,0), min(xs.max()+pad+1, alpha2.shape[1])
    crop = rgba[y0:y1, x0:x1]
    Image.fromarray(crop).save(f"cutouts/{name}.png")
    print(f"{name}: {im.size} -> {crop.shape[1]}x{crop.shape[0]}")

if __name__ == "__main__":
    args = sys.argv[1:]
    for a in args:
        name, _, r = a.partition(":")
        decord(name, int(r) if r else 14)
