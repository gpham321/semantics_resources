"""Embed task-suite imagery into task_assets.js as base64 WebP so
task_figures.html renders with no external file access.

Three keyed groups:
  mask/<name>  — background-removed scene (alpha, from Tasks/masked/)
  bg/<name>    — original photo, downscaled (with table + wall)
  board        — the data-collection whiteboard (Tasks/task_list.jpg)
Regenerate via:  python3 embed_tasks.py"""
import os, io, base64, json
from PIL import Image

NAMES = ["cup_coffee_machine", "pour", "mug_tree", "power_brick_drawer",
         "powerdrill_pad", "bottle-can_coaster", "faucet"]

MASK_MAX = 700     # background-removed PNGs (display <=340px, ~2x retina)
BG_MAX   = 1100    # photographic tiles (cover-cropped in CSS)
Q_MASK   = 88
Q_BG     = 82

def embed(out, key, im, maxside, quality, alpha):
    mode = "RGBA" if alpha else "RGB"
    im = im.convert(mode)
    m = maxside / max(im.size)
    if m < 1:
        im = im.resize((round(im.width*m), round(im.height*m)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=quality, method=6)
    b = buf.getvalue()
    out[key] = "data:image/webp;base64," + base64.b64encode(b).decode()
    return len(b)

def main():
    out, total = {}, 0
    for n in NAMES:
        mp = f"Tasks/masked/{n}.png"
        if os.path.exists(mp):
            total += embed(out, f"mask/{n}", Image.open(mp), MASK_MAX, Q_MASK, True)
        bp = f"Tasks/{n}.jpg"
        if os.path.exists(bp):
            total += embed(out, f"bg/{n}", Image.open(bp), BG_MAX, Q_BG, False)
    with open("task_assets.js", "w") as fh:
        fh.write("/* Base64-embedded task-suite imagery (WebP). mask/* = bg removed,\n"
                 "   bg/* = original photo. Regenerate: embed_tasks.py */\n")
        fh.write("window.TASK_ASSETS = " + json.dumps(out) + ";\n")
    print(f"embedded {len(out)} images, {total/1024:.0f} KB -> task_assets.js "
          f"({os.path.getsize('task_assets.js')/1024:.0f} KB)")

if __name__ == "__main__":
    main()
