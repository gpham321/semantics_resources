"""Composite the xArm gripper grasping the white-basic mug handle so the handle
sits BETWEEN the jaws: the gripper is split by a line through the grasp point —
the cup-side part is placed BEHIND the mug, the rest stays in FRONT.
Produces two grasps: side (middle of handle) and top (top of handle)."""
import math
import numpy as np
from PIL import Image

CUP  = "cutouts/cup_white_basic.png"
GRIP = "Other/gripper_crop.png"
JAW  = (0.30, 0.60)      # jaw-gap centre on the gripper image (frac)
CUP_H = 760

def rot_point(px, py, w, h, deg):
    r = math.radians(deg); cx, cy = w/2, h/2; dx, dy = px-cx, py-cy
    ca, sa = math.cos(-r), math.sin(-r)
    rx, ry = dx*ca-dy*sa, dx*sa+dy*ca
    nw, nh = abs(w*ca)+abs(h*sa), abs(w*sa)+abs(h*ca)
    return rx+nw/2, ry+nh/2

def place_gripper(gscale, grot):
    grip = Image.open(GRIP).convert("RGBA"); gw0, gh0 = grip.size
    jx0, jy0 = JAW[0]*gw0, JAW[1]*gh0
    gr = grip.rotate(grot, expand=True, resample=Image.BICUBIC)
    jxr, jyr = rot_point(jx0, jy0, gw0, gh0, grot)
    gs = gr.resize((round(gr.width*gscale), round(gr.height*gscale)), Image.LANCZOS)
    return gs, jxr*gscale, jyr*gscale

def compose(out, gscale, grot, handle, split_deg, split_off):
    cup = Image.open(CUP).convert("RGBA")
    cw = round(cup.width*CUP_H/cup.height); cup = cup.resize((cw, CUP_H), Image.LANCZOS)
    grip, jx, jy = place_gripper(gscale, grot)
    pad = 380
    CW, CH = cw+2*pad, CUP_H+2*pad
    cup_layer = Image.new("RGBA", (CW, CH), (0,0,0,0)); cup_layer.alpha_composite(cup, (pad, pad))
    hpx, hpy = pad+handle[0]*cw, pad+handle[1]*CUP_H
    gx, gy = round(hpx-jx), round(hpy-jy)
    grip_layer = Image.new("RGBA", (CW, CH), (0,0,0,0)); grip_layer.alpha_composite(grip, (gx, gy))

    # split: "behind" = pixels on the cup-side of a line through the grasp point.
    nx, ny = math.cos(math.radians(split_deg)), math.sin(math.radians(split_deg))
    yy, xx = np.mgrid[0:CH, 0:CW]
    val = (xx-hpx)*nx + (yy-hpy)*ny
    behind = val > split_off
    g = np.array(grip_layer)
    gb = g.copy(); gb[~behind, 3] = 0
    gf = g.copy(); gf[behind, 3] = 0

    res = Image.new("RGBA", (CW, CH), (0,0,0,0))
    res.alpha_composite(Image.fromarray(gb))   # gripper behind
    res.alpha_composite(cup_layer)             # mug
    res.alpha_composite(Image.fromarray(gf))   # gripper in front

    a = np.array(res)[:, :, 3]; ys, xs = np.where(a > 8); m = 16
    crop = res.crop((xs.min()-m, ys.min()-m, xs.max()+m, ys.max()+m))
    crop.save(out)
    bg = Image.new("RGBA", crop.size, (250,250,250,255)); bg.alpha_composite(crop)
    bg.convert("RGB").save(out.replace(".png", "_prev.png"))
    print(out, crop.size)

if __name__ == "__main__":
    # side grasp: gripper from the right onto the middle of the handle
    compose("Other/grasp_side.png", 0.34, -65, (0.90, 0.45), split_deg=180, split_off=-30)
    # top grasp: gripper upright from above onto the top of the handle
    compose("Other/grasp_top.png",  0.32,  75, (0.80, 0.34), split_deg=80, split_off=-15)
