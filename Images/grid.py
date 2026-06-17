"""Overlay a fractional coordinate grid on a cutout, for reading off shape coords."""
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont

def gridded(name, n=10, on_white=True, maxside=900):
    im = Image.open(f"cutouts/{name}.png").convert("RGBA")
    base = Image.new("RGBA", im.size, (255,255,255,255) if on_white else (180,180,180,255))
    base.alpha_composite(im); base = base.convert("RGB")
    base.thumbnail((maxside, maxside))
    W, H = base.size
    d = ImageDraw.Draw(base)
    gc = (0, 220, 0)
    for i in range(1, n):
        x = round(W*i/n); y = round(H*i/n)
        d.line([(x,0),(x,H)], fill=gc, width=1)
        d.line([(0,y),(W,y)], fill=gc, width=1)
        d.text((x+1,1), f"{i*10}", fill=(220,0,0))
        d.text((1,y+1), f"{i*10}", fill=(0,0,255))
    return base

if __name__ == "__main__":
    name = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    g = gridded(name, n)
    g.save(f"_thumbs/grid_{name}.png")
    print("ok", g.size, "(x=red %, y=blue %)")
