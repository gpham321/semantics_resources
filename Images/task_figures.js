/* Task-suite figures for the robotics semantics paper.
   Renders the manipulation task gallery in three directions:
     A — background removed (paper-clean cut-outs)
     B — photographic (original scene kept)
     C — annotated with the average teleop data-collection time (red, like the
         lab whiteboard) + the source whiteboard inset
   Images are base64-embedded in task_assets.js (mask/*, bg/*, board). */
const TA = (typeof window!=='undefined' && window.TASK_ASSETS) || {};
const src = k => TA[k] || k;

/* task list — name, short verb, object-variation config, avg teleop sec/demo */
const TASKS = [
  {key:'cup_coffee_machine',  name:'Cup on coffee machine',  verb:'place mug on platform',         cfg:'4×4',     secs:30},
  {key:'pour',                name:'Cup pour into bowl',     verb:'pour cup into bowl',            cfg:'5×3',     secs:35},
  {key:'mug_tree',            name:'Mug on tree',            verb:'hang mug on branch',            cfg:'5×1',     secs:27},
  {key:'power_brick_drawer',  name:'Power brick into drawer',verb:'open drawer, insert power brick',cfg:'5×1',    secs:32},
  {key:'powerdrill_pad',      name:'Drill on mouse pad',     verb:'set drill on pad',              cfg:'1×1',     secs:16},
  {key:'bottle-can_coaster',  name:'Bottle/can on coaster',  verb:'place bottle or can on coaster',cfg:'(1+1)×1', secs:11},
  {key:'faucet',              name:'Turn off faucet',        verb:'push down on faucet handle',    cfg:'1',       secs:23},
];

/* a caption block shared by every tile */
function tcap(t, fs, data){
  const time = data
    ? `<span class="ttime mark">~${t.secs}s<span class="tper">/demo</span></span>`
    : `<span class="ttime">~${t.secs}s</span>`;
  return `<figcaption class="tcap" style="font-size:${fs}px;">
      <div class="tname">${t.name}</div>
      <div class="tsub" style="font-size:${Math.round(fs*0.74)}px;">${t.verb}</div>
      <div class="tmeta" style="font-size:${Math.round(fs*0.8)}px;">
        <span class="cfg">${t.cfg}</span>${time}</div>
    </figcaption>`;
}

/* background-removed tile (optionally with red teleop-time annotation) */
function tileMask(t, imgH, fs, data){
  return `<figure class="tcard">
      <div class="tphoto" style="height:${imgH}px;">
        <img src="${src('mask/'+t.key)}" alt="${t.name}"
             style="max-height:${imgH}px;max-width:94%;width:auto;display:block;">
      </div>
      ${tcap(t, fs, data)}
    </figure>`;
}

/* photographic tile — original scene, cover-cropped into a rounded frame */
function tileBg(t, imgH, fs){
  return `<figure class="tcard">
      <div class="tphoto bg" style="height:${imgH}px;">
        <img src="${src('bg/'+t.key)}" alt="${t.name}"
             style="width:100%;height:100%;object-fit:cover;display:block;">
      </div>
      ${tcap(t, fs, false)}
    </figure>`;
}

/* flex grid: fixed columns, but an incomplete final row is centered. Each item
   may carry an inline `align-self` (used to vertically centre the summary cell). */
function gcell(html, basis, self){
  return `<div style="flex:0 0 ${basis};max-width:${basis};`+
         (self?`align-self:${self};`:``)+`">${html}</div>`;
}
function grid(items, cols, gap){
  const basis = `calc((100% - ${(cols-1)*gap}px) / ${cols})`;
  const cells = items.map(it => typeof it==='string'
      ? gcell(it, basis) : gcell(it.html, basis, it.self)).join('');
  return `<div style="display:flex;flex-wrap:wrap;justify-content:center;`+
         `align-items:end;gap:${gap}px;">${cells}</div>`;
}

function titleRow(t, sub, fs){
  return `<div class="sec-h"><span class="r"></span>`+
    `<span class="t" style="font-size:${fs}px;">${t}`+
    (sub?` <span class="tsmall">${sub}</span>`:``)+`</span><span class="r"></span></div>`;
}

/* ---- Direction A: background removed -------------------------------------- */
function buildA(mode){
  const wide = mode==='wide';
  const cols = wide?4:2, imgH=wide?226:224, fs=wide?31:30, gap=wide?26:24;
  return `<div style="padding:${wide?'34px 40px 30px':'28px 26px 24px'};">
      ${titleRow('Manipulation Task Suite','',wide?44:38)}
      <div style="height:${wide?22:18}px;"></div>
      ${grid(TASKS.map(t=>tileMask(t,imgH,fs,false)),cols,gap)}
    </div>`;
}

/* ---- Direction B: photographic (background kept) -------------------------- */
function buildB(mode){
  const wide = mode==='wide';
  const cols = wide?4:2, imgH=wide?224:236, fs=wide?31:30, gap=wide?24:22;
  return `<div style="padding:${wide?'34px 40px 30px':'28px 26px 24px'};">
      ${titleRow('Manipulation Task Suite','',wide?44:38)}
      <div style="height:${wide?22:18}px;"></div>
      ${grid(TASKS.map(t=>tileBg(t,imgH,fs)),cols,gap)}
    </div>`;
}

/* ---- Direction C: with average teleop data-collection time ---------------
   7 task cut-outs + the suite-mean summary fill a 4×2 grid (summary = 8th cell). */
function buildC(mode){
  const wide = mode==='wide';
  const cols = 4, imgH=wide?220:0, fs=wide?31:30, gap=wide?26:22;
  const avg = Math.round(TASKS.reduce((s,t)=>s+t.secs,0)/TASKS.length);
  const summary = `<div class="avgbox">
        <div class="avgl" style="margin:0 0 6px;">average teleop<br>per demonstration</div>
        <div class="avgn mark">~${avg}s</div>
        <div class="avgl" style="margin-top:10px;">across ${TASKS.length} tasks</div>
      </div>`;
  const items = TASKS.map(t=>tileMask(t,imgH,fs,true));
  items.push({html:summary, self:'center'});
  return `<div style="padding:${wide?'34px 40px 30px':'28px 26px 24px'};">
      ${titleRow('Task Suite &amp; Teleoperation Cost','',wide?44:38)}
      <div style="height:${wide?20:16}px;"></div>
      ${grid(items, cols, gap)}
    </div>`;
}

/* ===== mount + fit (same machinery as the object-suite studio) ===== */
function mount(id, html, w){
  const stage=document.getElementById(id); if(!stage) return;
  const fig=document.createElement('div');
  fig.className='fig'; fig.dataset.fw=w; fig.style.width=w+'px';
  fig.innerHTML=html; stage.appendChild(fig);
}
function fitAll(){
  document.querySelectorAll('.stage').forEach(st=>{
    const fig=st.querySelector('.fig'); if(!fig) return;
    const fw=+fig.dataset.fw;
    const s=Math.min(1, st.clientWidth/fw);
    const fh=fig.offsetHeight;
    fig.style.transform=`scale(${s})`;
    st.style.height=(fh*s)+'px';
  });
}
mount('stage-A2', buildA('wide'), 1600);
mount('stage-B2', buildB('wide'), 1600);
mount('stage-C2', buildC('wide'), 1600);
mount('stage-A1', buildA('tall'), 760);
mount('stage-B1', buildB('tall'), 760);
window.addEventListener('resize', fitAll);
window.addEventListener('load', fitAll);
fitAll();
// Re-fit once the serif web font is ready (Tinos changes text metrics) and
// whenever a figure's own size changes, so a fit measured against the fallback
// font can't leave a stage too short and overlap the next card.
if(document.fonts && document.fonts.ready){ document.fonts.ready.then(fitAll); }
if(window.ResizeObserver){
  const ro=new ResizeObserver(()=>fitAll());
  document.querySelectorAll('.fig').forEach(f=>ro.observe(f));
}
