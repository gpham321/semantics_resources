"""Export each figure from both figure studios as its own PNG, at native
resolution (2x device scale for crisp text/strokes). Reuses each page's head
CSS + build functions; renders one figure per page (no fit-scaling), then trims
surrounding whitespace. Run from the Images/ folder."""
import os, subprocess
import numpy as np
from PIL import Image

CHROME   = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
BASE_WIN = r"C:\Users\gpham\Documents\ARMLab\Semantic\Code\Images"
OUT = "exports"
os.makedirs(OUT, exist_ok=True)

SOURCES = [
 ('MugMachine','mug_machine_figures.html','figure_assets.js','figures.js',
   {'A2':'DirA-Catalog','B2':'DirB-GenAxis','C2':'DirC-Annotated','A1':'DirA-Catalog','B1':'DirB-GenAxis'}),
 ('TaskSuite','task_figures.html','task_assets.js','task_figures.js',
   {'A2':'DirA-Gallery','B2':'DirB-Gallery','C2':'DirC-Suite','A1':'DirA-Gallery','B1':'DirB-Gallery'}),
]
MODES  = {'A2':'wide','B2':'wide','C2':'wide','A1':'tall','B1':'tall'}
WIDTHS = {'A2':1600,'B2':1600,'C2':1600,'A1':760,'B1':760}

def head_of(path):
    t = open(path, encoding='utf-8').read()
    i = t.lower().find('</head>')
    return t[:i+len('</head>')]

def export_html(head, assets, figjs, key):
    return head + f"""
<body style="margin:0;background:#fff;padding:0;">
<div id="export"></div>
<script src="{assets}"></script>
<script src="{figjs}"></script>
<script>
(function(){{
  var key="{key}";
  var modes={{A2:'wide',B2:'wide',C2:'wide',A1:'tall',B1:'tall'}};
  var widths={{A2:1600,B2:1600,C2:1600,A1:760,B1:760}};
  var fn = key.charAt(0)=='A'?buildA:(key.charAt(0)=='B'?buildB:buildC);
  var html = fn(modes[key]);
  document.getElementById('export').innerHTML =
    '<div class="fig" style="position:relative;width:'+widths[key]+'px;background:#fff;">'+html+'</div>';
}})();
</script>
</body></html>"""

def render(tmp, out_win, w):
    url = 'file:///' + (BASE_WIN + '\\' + tmp).replace('\\','/')
    subprocess.run([CHROME,'--headless=new','--disable-gpu','--no-sandbox',
        '--hide-scrollbars','--force-device-scale-factor=2',
        f'--window-size={w},2600','--virtual-time-budget=7000',
        f'--screenshot={out_win}', url], capture_output=True)

def trim(path, margin=28):
    im = Image.open(path).convert('RGB')
    a = np.asarray(im)
    mask = (a < 250).any(2)
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return im
    x0, x1 = max(0, xs.min()-margin), min(im.width-1,  xs.max()+margin)
    y0, y1 = max(0, ys.min()-margin), min(im.height-1, ys.max()+margin)
    c = im.crop((x0, y0, x1+1, y1+1)); c.save(path); return c

rows = []
for prefix, html, assets, figjs, names in SOURCES:
    head = head_of(html)
    for key in ['A2','B2','C2','A1','B1']:
        col  = '2col' if key.endswith('2') else '1col'
        name = f"{prefix}_{names[key]}_{col}"
        tmp  = f"_exp_{prefix}_{key}.html"
        open(tmp,'w',encoding='utf-8').write(export_html(head, assets, figjs, key))
        render(tmp, f"{BASE_WIN}\\{OUT}\\{name}.png", WIDTHS[key])
        c = trim(f"{OUT}/{name}.png")
        rows.append((name, c.size))
        os.remove(tmp)

print("exported %d figures to %s/:" % (len(rows), OUT))
for n, s in rows:
    print(f"  {n}.png  {s[0]}x{s[1]}")
