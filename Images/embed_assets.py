"""Embed the transparent object images into figure_assets.js as base64 WebP
(alpha preserved) so mug_machine_figures.html renders with no external file
access. Re-run after changing highlight_cup/ or highlight_machine/."""
import os, io, base64, json
from PIL import Image

FOLDERS = ["highlight_cup", "highlight_machine"]
EXTRA   = ["Grasp/masked/side_grasp.png", "Grasp/masked/top_grasp.png"]  # real gripper grasps (bg removed) for Direction C
MAXSIDE = 560          # display is <=300px; ~2x for retina
QUALITY = 86

def _embed(out, path):
    im = Image.open(path).convert("RGBA")
    m = MAXSIDE / max(im.size)
    if m < 1:
        im = im.resize((round(im.width*m), round(im.height*m)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=QUALITY, method=6)
    b = buf.getvalue()
    out[path] = "data:image/webp;base64," + base64.b64encode(b).decode()
    return len(b)

def main():
    out, total = {}, 0
    for folder in FOLDERS:
        for f in sorted(os.listdir(folder)):
            if f.endswith(".png"):
                total += _embed(out, f"{folder}/{f}")
    for path in EXTRA:
        if os.path.exists(path):
            total += _embed(out, path)
    with open("figure_assets.js", "w") as fh:
        fh.write("/* Base64-embedded transparent object images (WebP, alpha) so the\n"
                 "   figure renders without external file access. Source: highlight_cup/,\n"
                 "   highlight_machine/. Regenerate via embed_assets.py. */\n")
        fh.write("window.FIG_ASSETS = " + json.dumps(out) + ";\n")
    print(f"embedded {len(out)} images, {total/1024:.0f} KB -> figure_assets.js "
          f"({os.path.getsize('figure_assets.js')/1024:.0f} KB)")

if __name__ == "__main__":
    main()
