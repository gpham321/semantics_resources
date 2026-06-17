/* figures.js — overview figure (mug -> coffee-maker). Based on the claude_design
   layout, with two fixes:
     (1) images come from the base64-embedded, transparent, feature-highlighted
         assets (figure_assets.js) instead of the missing uploads/orig/ path;
     (2) objects sit on the panel washes with NO white tile box.
   Cups carry a cyan handle highlight; machines a green mug-clearance fill. */

/* ===== assets ===== */
const src = p => (window.FIG_ASSETS && window.FIG_ASSETS[p]) || p;   // embedded data URI, else path
const CUPS = {
  id:  [['white_basic','White'],['orange','Orange'],['black','Black'],['red','Red']],
  ood: [['brown','Brown'],['gray','Gray'],['pink','Pink'],['white_ceramic','Ceramic']]
};
const MACH = {
  id:  [['keurig','Keurig'],['black','Black'],['cyan','Teal'],['white','White']],
  ood: [['red','Red'],['tastyle','Tastyle'],['blue','Blue']]
};
const MACH_FILE = {keurig:'keurig',black:'black',cyan:'teal',white:'white',
                   red:'red',tastyle:'tastyle',blue:'blue'};
const cupSrc  = (f)=> src(`highlight_cup/${f}.png`);
const machSrc = (f)=> src(`highlight_machine/${MACH_FILE[f]}_highlight_outline.png`);

/* ===== atoms ===== */
/* transparent specimen: image floats directly on the wash, baseline-aligned */
function spec(s,name,h,cap,scale){
  // Cells are equal-width flex items (see .spec/.simg CSS): the image fits within
  // its cell (max-width) and the row height (max-height), so a row of N objects
  // always fits its panel without clipping. Captions may wrap to a second line.
  const fs = name.length > 9 ? Math.round(cap*0.82) : cap;
  const mh = Math.round((scale||1)*100);
  return `<figure class="spec"><div class="simg" style="--h:${h}px;height:${h}px;">`+
         `<img src="${s}" alt="${name}" style="max-height:${mh}%"></div>`+
         `<figcaption style="font-size:${fs}px;white-space:normal;margin-top:${Math.round(cap)}px;">${name}</figcaption></figure>`;
}
/* even gap between specimens (centered, never touching, never too far apart) */
const rowGap = (h)=> Math.round(h*0.30);
function cupRow(list,h,cap){ return `<div class="specrow" style="gap:${rowGap(h)}px">${list.map(([f,n,sc])=>spec(cupSrc(f),n,h,cap,sc)).join('')}</div>`; }
function machRow(list,h,cap){ return `<div class="specrow" style="gap:${rowGap(h)}px">${list.map(([f,n,sc])=>spec(machSrc(f),n,h,cap,sc)).join('')}</div>`; }

function panel(kind,label,inner,labFs,padTop){
  // flex column + justify-center lets a panel fill extra height (when its column
  // is stretched to match the other) with the objects centred, not top-packed.
  return `<div class="panel ${kind}" style="flex:1;padding:${padTop}px 22px 22px;`+
         `display:flex;flex-direction:column;justify-content:center;">`+
         `<div class="panel-lbl" style="top:14px;left:22px;font-size:${labFs}px;">${label}</div>${inner}</div>`;
}
function legend(fs,gap){
  return `<div class="legend" style="font-size:${fs}px;gap:${gap}px;justify-content:center;flex-wrap:nowrap;white-space:nowrap;">`+
    `<div class="it"><span class="lg-chip id"></span>In-distribution</div>`+
    `<div class="it"><span class="lg-chip ood"></span>Out-of-distribution</div>`+
    `<div class="it"><span class="lg-handle"></span>Handle geometry</div>`+
    `<div class="it"><span class="lg-clear"></span>Clearance zone</div>`+
  `</div>`;
}
function secH(t,fs){ return `<div class="sec-h"><span class="r"></span><span class="t" style="font-size:${fs}px">${t}</span><span class="r"></span></div>`; }

/* dimension annotations (figure-coord px) */
function dimH(x,y,w,label,below){
  return `<div class="dim" style="left:${x}px;top:${y}px;width:${w}px;">`+
    `<div class="bar" style="left:0;top:11px;width:100%;height:2px;"></div>`+
    `<div class="bar" style="left:0;top:2px;width:2px;height:20px;"></div>`+
    `<div class="bar" style="right:0;top:2px;width:2px;height:20px;"></div>`+
    `<div class="cap" style="left:50%;transform:translateX(-50%);${below?`top:22px`:`top:-36px`};font-size:28px;">${label}</div></div>`;
}
function dimV(x,y,h,label){
  return `<div class="dim" style="left:${x}px;top:${y}px;height:${h}px;">`+
    `<div class="bar" style="top:0;left:11px;height:100%;width:2px;"></div>`+
    `<div class="bar" style="top:0;left:2px;width:20px;height:2px;"></div>`+
    `<div class="bar" style="bottom:0;left:2px;width:20px;height:2px;"></div>`+
    `<div class="cap" style="left:26px;top:50%;transform:translateY(-50%);font-size:28px;">${label}</div></div>`;
}
function leader(x,y,len,ang,label,labDx,labDy,color){
  color=color||'var(--handle)';
  return `<div class="anno" style="left:${x}px;top:${y}px;">`+
    `<div style="position:absolute;width:${len}px;height:1.5px;background:${color};transform:rotate(${ang}deg);transform-origin:left center;"></div>`+
    `<div style="position:absolute;width:6px;height:6px;border-radius:50%;background:${color};left:-3px;top:-3px;"></div>`+
    `<div class="lab" style="left:${labDx}px;top:${labDy}px;color:${color};border-color:${color};">${label}</div></div>`;
}
/* two parallel gripper "fingers" centred on (x,y). vert=true -> fingers come
   from above/below (top grasp); vert=false -> from the sides (side grasp). */
function grip(x,y,vert,color){
  const fl=44,fw=9,gap=26;
  const bar=vert?(d)=>`left:${x+d}px;top:${y-fl/2}px;width:${fw}px;height:${fl}px`
                :(d)=>`left:${x-fl/2}px;top:${y+d}px;width:${fl}px;height:${fw}px`;
  return `<div class="anno" style="left:0;top:0;"><div style="position:absolute;${bar(-gap/2-fw)};background:${color};border-radius:4px;"></div>`+
         `<div style="position:absolute;${bar(gap/2)};background:${color};border-radius:4px;"></div></div>`;
}

/* ===== Direction A — catalog panels ===== */
function buildA(mode){
  if(mode==='wide'){
    const cupH=152,machH=186,cap=37,sec=46,lab=34,pTop=66;
    const col = (title,p1,p2)=>`<section style="flex:1;display:flex;flex-direction:column;gap:18px;min-width:0;">
        ${secH(title,sec)}
        <div style="display:flex;flex-direction:column;gap:16px;flex:1;">${p1}${p2}</div></section>`;
    return `<div style="padding:34px 42px 26px;display:flex;flex-direction:column;gap:18px;">
      <div style="display:flex;gap:38px;flex:1;min-height:0;">
        ${col('Cups',
            panel('id','In-distribution',cupRow(CUPS.id,cupH,cap),lab,pTop),
            panel('ood','Out-of-distribution',cupRow(CUPS.ood,cupH,cap),lab,pTop))}
        <div style="width:1px;background:#e3e3e9;"></div>
        ${col('Coffee Machines',
            panel('id','In-distribution',machRow(MACH.id,machH,cap),lab,pTop),
            panel('ood','Out-of-distribution',machRow(MACH.ood,machH,cap),lab,pTop))}
      </div>
      ${legend(33,30)}
    </div>`;
  } else {
    const cupH=132,machH=156,cap=36,sec=44,lab=34,pTop=62;
    const block=(title,p1,p2)=>`<section style="display:flex;flex-direction:column;gap:13px;">
        ${secH(title,sec)}<div style="display:flex;flex-direction:column;gap:13px;">${p1}${p2}</div></section>`;
    return `<div style="padding:30px 30px 22px;display:flex;flex-direction:column;gap:22px;">
      ${block('Cups',
          panel('id','In-distribution',cupRow(CUPS.id,cupH,cap),lab,pTop),
          panel('ood','Out-of-distribution',cupRow(CUPS.ood,cupH,cap),lab,pTop))}
      ${block('Coffee Machines',
          panel('id','In-distribution',machRow(MACH.id,machH,cap),lab,pTop),
          panel('ood','Out-of-distribution',machRow(MACH.ood,machH,cap),lab,pTop))}
      <div style="margin-top:6px;">${legend(17,11)}</div>
    </div>`;
  }
}

/* ===== Direction B — generalization axis ===== */
function buildB(mode){
  if(mode==='wide'){
    const cupH=146,machH=182,cap=36;
    const arrow = `<div style="display:flex;align-items:center;gap:0;height:60px;margin:2px 0 14px;">
        <div style="width:96px;"></div>
        <div style="flex:1;position:relative;height:100%;">
          <div style="position:absolute;left:0;right:0;top:50%;height:2px;background:#9aa0a8;"></div>
          <div style="position:absolute;right:-2px;top:50%;transform:translateY(-50%);width:0;height:0;border-left:13px solid #9aa0a8;border-top:8px solid transparent;border-bottom:8px solid transparent;"></div>
          <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#fff;padding:0 16px;font-family:ui-sans-serif,system-ui,sans-serif;font-style:italic;color:#6a6f77;font-size:34px;white-space:nowrap;">increasing distribution shift &#8594; generalization</div>
        </div></div>`;
    const head = `<div class="bgrid" style="grid-template-rows:auto;margin-bottom:8px;">
        <div></div>
        <div class="bhead id">In-distribution<span class="bq">(training set)</span></div>
        <div class="bhead ood">Out-of-distribution<span class="bq">(held-out)</span></div></div>`;
    const cell=(kind,inner)=>`<div class="bcell ${kind}">${inner}</div>`;
    const gut=(t)=>`<div class="bcell gutter"><span class="glab">${t}</span></div>`;
    return `<div style="padding:30px 40px 24px;display:flex;flex-direction:column;">
      ${arrow}${head}
      <div class="bgrid bregions" style="flex:1;">
        ${gut('Cups')}${cell('id',cupRow(CUPS.id,cupH,cap))}${cell('ood',cupRow(CUPS.ood,cupH,cap))}
        ${gut('Coffee Machines')}${cell('id',machRow(MACH.id,machH,cap))}${cell('ood',machRow(MACH.ood,machH,cap))}
      </div>
    </div>`;
  } else {
    const cupH=128,machH=150,cap=35;
    const region=(kind,label,sub)=>`<div class="vregion ${kind}">
        <div class="vrlab">${label}<span>${sub}</span></div>
        <div class="vsub">Cups</div>${kind==='id'?cupRow(CUPS.id,cupH,cap):cupRow(CUPS.ood,cupH,cap)}
        <div class="vsub">Coffee Machines</div>${kind==='id'?machRow(MACH.id,machH,cap):machRow(MACH.ood,machH,cap)}
      </div>`;
    const arrow=`<div class="vaxis"><div class="vline"></div><div class="vhead"></div><span>generalization</span></div>`;
    return `<div style="padding:28px 28px 24px;display:flex;flex-direction:column;gap:0;">
      ${region('id','In-distribution','training')}
      ${arrow}
      ${region('ood','Out-of-distribution','held-out')}
    </div>`;
  }
}

/* ===== Direction C — annotated specimens + key ===== */
function buildC(mode){
  const cupH=140,machH=178,cap=36,lab=34;
  const miniCups=(list)=>`<div class="specrow" style="gap:${rowGap(cupH)}px">${list.map(([f,n])=>spec(cupSrc(f),n,cupH,cap)).join('')}</div>`;
  const miniMach=(list)=>`<div class="specrow" style="gap:${rowGap(machH)}px">${list.map(([f,n])=>spec(machSrc(f),n,machH,cap)).join('')}</div>`;
  // panel groups flex:1 so the catalog fills the column height to match the left.
  const grid = `<div style="display:flex;flex-direction:column;gap:18px;flex:1;min-width:0;">
      ${secH('Cups',42)}
      <div style="flex:1;display:flex;flex-direction:column;gap:16px;">
        ${panel('id','In-distribution',miniCups(CUPS.id),lab,62)}
        ${panel('ood','Out-of-distribution',miniCups(CUPS.ood),lab,62)}
      </div>
      ${secH('Coffee Machines',42)}
      <div style="flex:1;display:flex;flex-direction:column;gap:16px;">
        ${panel('id','In-distribution',miniMach(MACH.id),lab,62)}
        ${panel('ood','Out-of-distribution',miniMach(MACH.ood),lab,62)}
      </div></div>`;
  // standalone label (sits directly on / beside a feature)
  const tag=(x,y,t,c)=>`<div class="anno" style="left:${x}px;top:${y}px;"><div class="lab" style="left:0;top:0;color:${c};border-color:${c};">${t}</div></div>`;
  // hero cup — rim "cup diameter" bracket on top, "handle" leader to the right.
  const heroCup = `<div class="hero" style="flex:1;justify-content:center;">
      <div class="herobox" style="width:512px;height:380px;position:relative;">
        <img src="${cupSrc('white_basic')}" style="position:absolute;left:60px;bottom:14px;height:300px;">
        ${dimH(63,52,244,'cup diameter',false)}
        ${leader(368,214,50,-6,'handle',56,-18,'var(--handle)')}
      </div>
      <div class="herocap">Cup</div></div>`;
  // hero machine — "clearance area" leader onto the green pocket (label in the
  // left margin), "platform" bracket under the drip tray.
  const heroMach = `<div class="hero" style="flex:1.45;justify-content:center;">
      <div class="herobox" style="width:512px;height:600px;position:relative;">
        <img src="${machSrc('keurig')}" style="position:absolute;left:72px;bottom:56px;height:500px;">
        ${tag(242,312,'clearance<br>area','var(--clear-dk)')}
        ${leader(256,500,30,90,'platform',-46,42,'var(--clear-dk)')}
      </div>
      <div class="herocap">Coffee Machine</div></div>`;
  // hero grasp — real gripper photos grasping the mug (background removed),
  // shown for both top and side grasps in equal boxes.
  const gItem=(img,lab)=>`<div style="display:flex;flex-direction:column;align-items:center;gap:12px;">`+
      `<div style="width:262px;height:256px;display:flex;align-items:center;justify-content:center;">`+
      `<img src="${src(img)}" style="max-height:256px;max-width:262px;width:auto;height:auto;display:block;"></div>`+
      `<div style="font-family:var(--serif);font-style:italic;font-size:32px;color:var(--ink2);">${lab}</div></div>`;
  const heroGrasp = `<div class="hero" style="justify-content:center;">
      <div style="display:flex;align-items:flex-end;justify-content:center;gap:36px;padding:8px 0;width:100%;">
        ${gItem('Grasp/masked/top_grasp.png','Top grasp')}${gItem('Grasp/masked/side_grasp.png','Side grasp')}
      </div></div>`;
  return `<div style="padding:34px 44px 26px;display:flex;flex-direction:column;gap:24px;">
      <div style="display:flex;gap:40px;align-items:stretch;">
        <div style="width:540px;display:flex;flex-direction:column;gap:16px;flex-shrink:0;">
          ${secH('Varied Features',42)}
          <div style="flex:1;display:flex;flex-direction:column;gap:16px;">${heroCup}${heroMach}</div>
          ${secH('Grasp strategies',42)}
          ${heroGrasp}
        </div>
        <div style="width:1px;background:#e3e3e9;"></div>
        <div style="flex:1;display:flex;flex-direction:column;gap:18px;min-width:0;">${grid}</div>
      </div>
      <div style="border-top:1px solid #e3e3e9;padding-top:20px;">${legend(33,30)}</div>
    </div>`;
}

/* ===== caption ===== */
const CAPTION = `We evaluate pick-and-place policies on a single task &mdash; a robot arm grasps a mug and places it on the platform of a single-serve coffee maker &mdash; across <b>[N]</b> arm/policy configurations. The object suite comprises eight mugs and seven coffee makers, each split into in-distribution instances seen during training (cool panels) and held-out instances used only at test time (warm panels). <b>Cups</b> (in-distribution: White, Orange, Black, Red; held-out: Brown, Gray, Pink, White-ceramic) vary in <i>handle geometry</i> &mdash; open C-loops vs. closed D-loops, round vs. squared cross-sections, thick vs. thin walls (cyan highlight) &mdash; as well as wall taper, rim diameter, and surface material (matte plastic, enamel, vacuum-steel, wood-grain). <b>Coffee makers</b> (in-distribution: Keurig, Black, Teal, White; held-out: Red, Tastyle, Blue) vary in body height and silhouette, drip-platform shape, and the <i>mug-clearance volume</i> beneath the spout (green region) that bounds feasible placement poses. Absolute dimensions for every object are reported in Table&nbsp;[X]. All objects are shown to scale within each category; backgrounds removed for clarity.`;

/* ===== mount + fit ===== */
function mount(id, html, w){
  const stage=document.getElementById(id);
  if(!stage) return;
  const fig=document.createElement('div');
  fig.className='fig'; fig.dataset.fw=w;
  fig.style.width=w+'px';   // height is content-driven (no clipping)
  fig.innerHTML=html;
  stage.appendChild(fig);
}
function fitAll(){
  document.querySelectorAll('.stage').forEach(st=>{
    const fig=st.querySelector('.fig'); if(!fig) return;
    const fw=+fig.dataset.fw;
    const s=Math.min(1, st.clientWidth/fw);
    const fh=fig.offsetHeight;          // layout height, ignores transform
    fig.style.transform=`scale(${s})`;
    st.style.height=(fh*s)+'px';
  });
}
mount('stage-A2', buildA('wide'), 1600, 760);
mount('stage-B2', buildB('wide'), 1600, 760);
mount('stage-C2', buildC('wide'), 1600, 940);
mount('stage-A1', buildA('tall'), 760, 1500);
mount('stage-B1', buildB('tall'), 760, 1500);
const capEl=document.getElementById('caption'); if(capEl) capEl.innerHTML = CAPTION;
window.addEventListener('resize', fitAll);
window.addEventListener('load', fitAll);
// Re-fit once the serif web font is ready: text metrics change when Tinos
// swaps in, so a fit measured against the fallback font would leave the stage
// too short and the next card would overlap (differs by browser load timing).
if(document.fonts && document.fonts.ready){ document.fonts.ready.then(fitAll); }
// Re-fit whenever a figure's own size changes (font swap, image decode, etc.).
if(window.ResizeObserver){
  const ro=new ResizeObserver(()=>fitAll());
  document.querySelectorAll('.fig').forEach(f=>ro.observe(f));
}
fitAll();
