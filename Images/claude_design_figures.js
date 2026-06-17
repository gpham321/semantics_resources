/* ===== data ===== */
const DIR = 'uploads/orig/';
const CUPS = {
  id:  [['white_basic','White'],['orange','Orange'],['black','Black'],['red','Red']],
  ood: [['brown','Brown'],['gray','Gray'],['pink','Pink'],['white_ceramic','White (ceramic)']]
};
const MACH = {
  id:  [['keurig','Keurig'],['black','Black'],['cyan','Teal'],['white','White']],
  ood: [['red','Red'],['tastyle','Tastyle'],['blue','Blue']]
};
const cupSrc  = (f)=> `${DIR}cup_${f}.png`;
const machSrc = (f)=> `${DIR}machine_${f}.png`;

/* ===== atoms ===== */
function spec(src,name,h,cap){
  return `<figure class="spec"><div class="tile" style="--h:${h}px"><img src="${src}" alt="${name}"></div>`+
         `<figcaption style="font-size:${cap}px;margin-top:${Math.round(cap*0.5)}px;">${name}</figcaption></figure>`;
}
function cupRow(list,h,cap){ return `<div class="specrow">${list.map(([f,n])=>spec(cupSrc(f),n,h,cap)).join('')}</div>`; }
function machRow(list,h,cap){ return `<div class="specrow">${list.map(([f,n])=>spec(machSrc(f),n,h,cap)).join('')}</div>`; }

function panel(kind,label,inner,labFs,padTop){
  return `<div class="panel ${kind}" style="flex:1;padding:${padTop}px 16px 12px;">`+
         `<div class="panel-lbl" style="top:10px;left:18px;font-size:${labFs}px;">${label}</div>${inner}</div>`;
}
function legend(fs,gap){
  return `<div class="legend" style="font-size:${fs}px;gap:${gap}px;justify-content:center;">`+
    `<div class="it"><span class="lg-chip id"></span>In-distribution (training)</div>`+
    `<div class="it"><span class="lg-chip ood"></span>Out-of-distribution (held&#8209;out)</div>`+
    `<div class="it"><span class="lg-handle"></span>Cup handle geometry</div>`+
    `<div class="it"><span class="lg-clear"></span>Mug clearance zone</div>`+
  `</div>`;
}
function secH(t,fs){ return `<div class="sec-h"><span class="r"></span><span class="t" style="font-size:${fs}px">${t}</span><span class="r"></span></div>`; }

/* dimension annotations (figure-coord px) */
function dimH(x,y,w,label,below){
  return `<div class="dim" style="left:${x}px;top:${y}px;width:${w}px;">`+
    `<div class="bar" style="left:0;top:7px;width:100%;height:1.5px;"></div>`+
    `<div class="bar" style="left:0;top:1px;width:1.5px;height:13px;"></div>`+
    `<div class="bar" style="right:0;top:1px;width:1.5px;height:13px;"></div>`+
    `<div class="cap" style="left:50%;transform:translateX(-50%);${below?`top:12px`:`top:-16px`};font-size:13px;">${label}</div></div>`;
}
function dimV(x,y,h,label){
  return `<div class="dim" style="left:${x}px;top:${y}px;height:${h}px;">`+
    `<div class="bar" style="top:0;left:7px;height:100%;width:1.5px;"></div>`+
    `<div class="bar" style="top:0;left:1px;width:13px;height:1.5px;"></div>`+
    `<div class="bar" style="bottom:0;left:1px;width:13px;height:1.5px;"></div>`+
    `<div class="cap" style="left:16px;top:50%;transform:translateY(-50%);font-size:13px;">${label}</div></div>`;
}
function leader(x,y,len,ang,label,labDx,labDy,color){
  color=color||'var(--handle)';
  return `<div class="anno" style="left:${x}px;top:${y}px;">`+
    `<div style="position:absolute;width:${len}px;height:1.5px;background:${color};transform:rotate(${ang}deg);transform-origin:left center;"></div>`+
    `<div style="position:absolute;width:6px;height:6px;border-radius:50%;background:${color};left:-3px;top:-3px;"></div>`+
    `<div class="lab" style="left:${labDx}px;top:${labDy}px;color:${color};border-color:${color};">${label}</div></div>`;
}

/* ===== Direction A — catalog panels ===== */
function buildA(mode){
  if(mode==='wide'){
    const cupH=150,machH=188,cap=17,sec=26,lab=13.5,pTop=36;
    const col = (title,p1,p2)=>`<section style="flex:1;display:flex;flex-direction:column;gap:16px;min-width:0;">
        ${secH(title,sec)}
        <div style="display:flex;flex-direction:column;gap:16px;flex:1;">${p1}${p2}</div></section>`;
    return `<div style="padding:34px 42px 26px;height:100%;display:flex;flex-direction:column;gap:18px;">
      <div style="display:flex;gap:38px;flex:1;min-height:0;">
        ${col('Cups',
            panel('id','In-distribution',cupRow(CUPS.id,cupH,cap),lab,pTop),
            panel('ood','Out-of-distribution',cupRow(CUPS.ood,cupH,cap),lab,pTop))}
        <div style="width:1px;background:#e3e3e9;"></div>
        ${col('Coffee machines',
            panel('id','In-distribution',machRow(MACH.id,machH,cap),lab,pTop),
            panel('ood','Out-of-distribution',machRow(MACH.ood,machH,cap),lab,pTop))}
      </div>
      ${legend(14,30)}
    </div>`;
  } else {
    const cupH=124,machH=150,cap=15,sec=23,lab=12.5,pTop=32;
    const block=(title,p1,p2)=>`<section style="display:flex;flex-direction:column;gap:13px;">
        ${secH(title,sec)}<div style="display:flex;flex-direction:column;gap:13px;">${p1}${p2}</div></section>`;
    return `<div style="padding:30px 30px 22px;height:100%;display:flex;flex-direction:column;gap:22px;">
      ${block('Cups',
          panel('id','In-distribution',cupRow(CUPS.id,cupH,cap),lab,pTop),
          panel('ood','Out-of-distribution',cupRow(CUPS.ood,cupH,cap),lab,pTop))}
      ${block('Coffee machines',
          panel('id','In-distribution',machRow(MACH.id,machH,cap),lab,pTop),
          panel('ood','Out-of-distribution',machRow(MACH.ood,machH,cap),lab,pTop))}
      <div style="margin-top:auto;">${legend(13,18)}</div>
    </div>`;
  }
}

/* ===== Direction B — generalization axis ===== */
function buildB(mode){
  if(mode==='wide'){
    const cupH=140,machH=178,cap=16;
    const arrow = `<div style="display:flex;align-items:center;gap:0;height:34px;margin:2px 0 10px;">
        <div style="width:96px;"></div>
        <div style="flex:1;position:relative;height:100%;">
          <div style="position:absolute;left:0;right:0;top:50%;height:2px;background:#9aa0a8;"></div>
          <div style="position:absolute;right:-2px;top:50%;transform:translateY(-50%);width:0;height:0;border-left:13px solid #9aa0a8;border-top:8px solid transparent;border-bottom:8px solid transparent;"></div>
          <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#fff;padding:0 12px;font-family:ui-sans-serif,system-ui,sans-serif;font-style:italic;color:#6a6f77;font-size:15px;">increasing distribution shift &#8594; generalization</div>
        </div></div>`;
    const head = `<div class="bgrid" style="grid-template-rows:auto;margin-bottom:6px;">
        <div></div>
        <div class="bhead id">Training distribution &mdash; in-distribution</div>
        <div class="bhead ood">Held-out &mdash; out-of-distribution</div></div>`;
    const cell=(kind,inner)=>`<div class="bcell ${kind}">${inner}</div>`;
    const gut=(t)=>`<div class="bcell gutter"><span class="glab">${t}</span></div>`;
    return `<div style="padding:30px 40px 24px;height:100%;display:flex;flex-direction:column;">
      ${arrow}${head}
      <div class="bgrid bregions" style="flex:1;">
        ${gut('Cups')}${cell('id',cupRow(CUPS.id,cupH,cap))}${cell('ood',cupRow(CUPS.ood,cupH,cap))}
        ${gut('Coffee machines')}${cell('id',machRow(MACH.id,machH,cap))}${cell('ood',machRow(MACH.ood,machH,cap))}
      </div>
    </div>`;
  } else {
    const cupH=116,machH=140,cap=15;
    const region=(kind,label,sub)=>`<div class="vregion ${kind}">
        <div class="vrlab">${label}<span>${sub}</span></div>
        <div class="vsub">Cups</div>${kind==='id'?cupRow(CUPS.id,cupH,cap):cupRow(CUPS.ood,cupH,cap)}
        <div class="vsub">Coffee machines</div>${kind==='id'?machRow(MACH.id,machH,cap):machRow(MACH.ood,machH,cap)}
      </div>`;
    const arrow=`<div class="vaxis"><div class="vline"></div><div class="vhead"></div><span>generalization</span></div>`;
    return `<div style="padding:28px 28px 24px;height:100%;display:flex;flex-direction:column;gap:0;">
      ${region('id','In-distribution','training')}
      ${arrow}
      ${region('ood','Out-of-distribution','held-out')}
    </div>`;
  }
}

/* ===== Direction C — annotated specimens + key ===== */
function buildC(mode){
  const cupH=92,machH=120,cap=14,lab=12;
  const miniCups=(list)=>`<div class="specrow">${list.map(([f,n])=>spec(cupSrc(f),n,cupH,cap)).join('')}</div>`;
  const miniMach=(list)=>`<div class="specrow">${list.map(([f,n])=>spec(machSrc(f),n,machH,cap)).join('')}</div>`;
  const grid = `<div style="display:flex;flex-direction:column;gap:14px;flex:1;min-width:0;">
      ${secH('Cups',22)}
      <div style="display:flex;flex-direction:column;gap:12px;">
        ${panel('id','In-distribution',miniCups(CUPS.id),lab,30)}
        ${panel('ood','Out-of-distribution',miniCups(CUPS.ood),lab,30)}
      </div>
      ${secH('Coffee machines',22)}
      <div style="display:flex;flex-direction:column;gap:12px;">
        ${panel('id','In-distribution',miniMach(MACH.id),lab,30)}
        ${panel('ood','Out-of-distribution',miniMach(MACH.ood),lab,30)}
      </div>`;
  // hero cup (white_basic, ar 1.13) box 320x250 ; hero machine (keurig, ar .735) box 330x430
  const heroCup = `<div class="hero">
      <div class="herobox" style="width:320px;height:250px;position:relative;">
        <img src="${cupSrc('white_basic')}" style="position:absolute;left:50%;bottom:0;transform:translateX(-50%);height:240px;">
        ${dimH(20,8,236,'opening diameter',false)}
        ${leader(250,150,40,18,'handle geometry',46,-8,'var(--handle)')}
      </div>
      <div class="herocap">Exemplar cup &mdash; <i>White</i></div></div>`;
  const heroMach = `<div class="hero">
      <div class="herobox" style="width:340px;height:430px;position:relative;">
        <img src="${machSrc('keurig')}" style="position:absolute;left:50%;bottom:0;transform:translateX(-50%);height:420px;">
        ${dimV(228,150,150,'clearance<br>height')}
        ${leader(214,300,40,150,'mug clearance',-150,30,'var(--clear-dk)')}
        ${dimH(150,408,150,'platform footprint',true)}
      </div>
      <div class="herocap">Exemplar machine &mdash; <i>Keurig</i></div></div>`;
  return `<div style="padding:32px 40px 26px;height:100%;display:flex;gap:40px;">
      <div style="width:360px;display:flex;flex-direction:column;gap:18px;flex-shrink:0;">
        ${secH('Varied features',22)}
        ${heroCup}${heroMach}
      </div>
      <div style="width:1px;background:#e3e3e9;"></div>
      <div style="flex:1;display:flex;flex-direction:column;gap:14px;min-width:0;">${grid}</div>
    </div>`;
}

/* ===== caption ===== */
const CAPTION = `We evaluate pick-and-place policies on a single task &mdash; a robot arm grasps a mug and places it on the platform of a single-serve coffee maker &mdash; across <b>[N]</b> arm/policy configurations. The object suite comprises eight mugs and seven coffee makers, each split into in-distribution instances seen during training (cool panels) and held-out instances used only at test time (warm panels). <b>Cups</b> (in-distribution: White, Orange, Black, Red; held-out: Brown, Gray, Pink, White-ceramic) vary in <i>handle geometry</i> &mdash; open C-loops vs. closed D-loops, round vs. squared cross-sections, thick vs. thin walls (teal highlight) &mdash; as well as wall taper, rim diameter, and surface material (matte plastic, enamel, vacuum-steel, wood-grain). <b>Coffee makers</b> (in-distribution: Keurig, Black, Teal, White; held-out: Red, Tastyle, Blue) vary in body height and silhouette, drip-platform shape, and the <i>mug-clearance volume</i> beneath the spout (green region) that bounds feasible placement poses. Absolute dimensions for every object are reported in Table&nbsp;[X]. All objects are shown to scale within each category; backgrounds removed for clarity.`;

/* ===== mount + fit ===== */
function mount(id, html, w, h){
  const stage=document.getElementById(id);
  if(!stage) return;
  const fig=document.createElement('div');
  fig.className='fig'; fig.dataset.fw=w; fig.dataset.fh=h;
  fig.style.width=w+'px'; fig.style.height=h+'px';
  fig.innerHTML=html;
  stage.appendChild(fig);
}
function fitAll(){
  document.querySelectorAll('.stage').forEach(st=>{
    const fig=st.querySelector('.fig'); if(!fig) return;
    const fw=+fig.dataset.fw, fh=+fig.dataset.fh;
    const s=Math.min(1, st.clientWidth/fw);
    fig.style.transform=`scale(${s})`;
    st.style.height=(fh*s)+'px';
  });
}
mount('stage-A2', buildA('wide'), 1600, 760);
mount('stage-B2', buildB('wide'), 1600, 760);
mount('stage-C2', buildC('wide'), 1600, 940);
mount('stage-A1', buildA('tall'), 760, 1500);
mount('stage-B1', buildB('tall'), 760, 1500);
document.getElementById('caption').innerHTML = CAPTION;
window.addEventListener('resize', fitAll);
window.addEventListener('load', fitAll);
fitAll();
