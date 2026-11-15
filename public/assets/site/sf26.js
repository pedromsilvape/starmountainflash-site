/* Starmountain Flash · desenho 2026. Editar em scripts/novo/js/ e correr scripts/novo/build.py. */
(()=>{
const D=document,d=D.documentElement,$=(s,r=D)=>r.querySelector(s),$$=(s,r=D)=>[...r.querySelectorAll(s)];
d.classList.add('js');
const RM=matchMedia('(prefers-reduced-motion:reduce)').matches;
const cl=(v,a=0,b=1)=>Math.min(b,Math.max(a,v)),ss=(a,b,v)=>{const t=cl((v-a)/(b-a));return t*t*(3-2*t)};
const L=()=>d.dataset.lang==='en'||location.pathname.startsWith('/en')?'en':'pt';
/* relógio */
const tf=new Intl.DateTimeFormat('pt-PT',{hour:'2-digit',minute:'2-digit',timeZone:'Europe/Lisbon'});
const tick=()=>$$('.s-clock').forEach(e=>e.textContent=tf.format(new Date()));tick();setInterval(tick,20000);
/* nav: tema conforme a secção por baixo */
const nav=$('#s-nav'),mn=$('#s-menu'),bg=$('#s-burger');
const DK='[data-t=dk],.s-end,.hero,.band,.dark,.endcta,.cta,.onde,.cbox.dk',LT='[data-t=lt]';
function navTheme(){if(!nav||mn&&mn.classList.contains('on'))return;const home=D.body.classList.contains('home');let lt=!home;
 for(const s of $$(home?LT:DK)){const r=s.getBoundingClientRect();if(r.top<=40&&r.bottom>40&&r.height>0){lt=home;break}}nav.classList.toggle('lt',lt)}
let nt=0;addEventListener('scroll',()=>{if(!nt)nt=requestAnimationFrame(()=>{nt=0;navTheme()})},{passive:true});addEventListener('resize',navTheme);navTheme();setTimeout(navTheme,400);
/* menu */
if(bg&&mn){const tog=o=>{mn.classList.toggle('on',o);bg.setAttribute('aria-expanded',o);bg.setAttribute('aria-label',L()==='en'?(o?'Close menu':'Open menu'):(o?'Fechar menu':'Abrir menu'));D.body.classList.toggle('s-lock',o);if(o)nav.classList.remove('lt');else navTheme()};
 bg.addEventListener('click',()=>tog(!mn.classList.contains('on')));mn.addEventListener('click',e=>{if(e.target.closest('a'))tog(false)});
 addEventListener('keydown',e=>{if(e.key==='Escape'&&mn.classList.contains('on')){tog(false);bg.focus()}})}
/* pop-up */
const md=$('#s-md');
if(md){const ofl=$('.s-md-of',md),of0=ofl?ofl.innerHTML:'';let last=null;
 const mdo=v=>{md.classList.toggle('o',v);md.setAttribute('aria-hidden',!v);D.body.classList.toggle('s-lock',v);if(v){const f=$('.x-cf',md);f&&f.classList.remove('sent','err');setTimeout(()=>{const i=$('input:not([type=checkbox]):not([type=radio]):not(.x-hp)',md);if(i&&matchMedia('(pointer:fine)').matches)i.focus({preventScroll:true});else $('.s-mx',md).focus({preventScroll:true})},300)}else if(last){last.focus({preventScroll:true});last=null}};
 window.sfOpen=a=>{mn&&mn.classList.contains('on')&&bg.click();last=a||null;const k=(a&&a.dataset.svc)||D.body.dataset.svc||'';$$('.x-pick input',md).forEach(i=>i.checked=!!k&&i.value===k);const o=a&&a.dataset['offer'+(L()==='en'?'En':'Pt')];if(ofl)ofl.innerHTML=o||of0;mdo(true)};
 D.addEventListener('click',e=>{const a=e.target.closest('[data-modal]');if(a){e.preventDefault();window.sfOpen(a)}else if(e.target===md||e.target.closest('.s-mx'))mdo(false)});
 addEventListener('keydown',e=>{if(e.key==='Escape'&&md.classList.contains('o'))mdo(false)})}
/* formulários → /api/lead */
D.addEventListener('submit',async e=>{const f=e.target.closest('form.x-cf');if(!f)return;e.preventDefault();if(f.classList.contains('busy'))return;
 const txt=el=>el.textContent.trim(),q=s=>f.querySelector(s);
 const sv=$$('.x-pick input:checked',f).map(i=>txt(i.parentNode.querySelector('span'))).join(', ');
 const via=q('.x-via input:checked');const extra=$$('.x-fi input:not([autocomplete])',f).filter(i=>i.name!=='website'&&i.value.trim()).map(i=>i.value.trim());
 const ta=q('textarea'),url=q('input[autocomplete=url]');
 const msg=[...extra,ta&&ta.value.trim(),url&&url.value.trim()?'Site: '+url.value.trim():'',via?'Resposta por: '+txt(via.parentNode.querySelector('span')):''].filter(Boolean).join('\n');
 const body={nome:(q('input[autocomplete=name]')||{}).value||'',email:(q('input[type=email]')||{}).value||'',empresa:(q('input[autocomplete=organization]')||{}).value||'',telefone:(q('input[type=tel]')||{}).value||'',servico:sv.slice(0,60),mensagem:msg,origem:(f.closest('.s-md')?'Pop-up · ':'Formulário · ')+location.pathname,website:(q('input[name=website]')||{}).value||''};
 f.classList.add('busy');f.classList.remove('err');
 try{const r=await fetch('/api/lead',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});if(!r.ok)throw 0;f.classList.add('sent');f.reset()}catch(x){f.classList.add('err')}f.classList.remove('busy')});
/* troca de língua: usa o endereço alternativo da página */
D.addEventListener('click',e=>{const a=e.target.closest('.s-lang');if(!a)return;const en=L()==='en',m=$('link[rel=alternate][hreflang="'+(en?'pt-PT':'en')+'"]');let to;
 if(m)to=new URL(m.getAttribute('href'),location.href).pathname;else{const p=location.pathname;to=en?(p.replace(/^\/en(\/|$)/,'/')||'/'):('/en'+(p==='/'?'':p))}
 e.preventDefault();location.href=to+location.hash});
/* voltar ao topo */
D.addEventListener('click',e=>{const a=e.target.closest('.s-up');if(a){e.preventDefault();scrollTo({top:0,behavior:RM?'auto':'smooth'})}});
/* revelar */
const els=$$('.rv');
if(!('IntersectionObserver' in window))els.forEach(e=>e.classList.add('in'));
else{const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.08,rootMargin:'0px 0px -6% 0px'});els.forEach(e=>io.observe(e))}
/* páginas interiores: hero e barra do método */
const hero=D.getElementById('hero');hero&&requestAnimationFrame(()=>hero.classList.add('in'));
if(D.getElementById('fill')&&D.getElementById('metodo')){const met=D.getElementById('metodo'),fill=D.getElementById('fill'),phs=$$('.ph2',met);
 const mp=()=>{const r=met.getBoundingClientRect(),k=cl((innerHeight*.75-r.top-200)/(r.height*.55));fill.style.width=(k*100)+'%';phs.forEach((e,i)=>e.classList.toggle('lit',k>=i/phs.length+.02))};
 addEventListener('scroll',()=>requestAnimationFrame(mp),{passive:true});requestAnimationFrame(mp)}
/* página inicial */
if($('#c3')){
/* símbolo 3D */
const R=[[-0.2253,-0.4464,0.4122,-0.4462,0.4212,-0.4454,0.4302,-0.4436,0.4388,-0.441,0.4472,-0.4374,0.4552,-0.4333,0.4627,-0.4282,0.4697,-0.4224,0.4761,-0.4161,0.4819,-0.409,0.4869,-0.4015,0.4911,-0.3936,0.4946,-0.3852,0.4972,-0.3765,0.499,-0.3676,0.4999,-0.3586,0.4999,-0.3496,0.499,-0.3406,0.4972,-0.3317,0.4946,-0.323,0.4911,-0.3146,0.4869,-0.3067,0.4819,-0.2991,0.4761,-0.2921,0.4697,-0.2857,0.4627,-0.2799,0.4552,-0.2749,0.4472,-0.2707,0.4388,-0.2672,0.4302,-0.2646,0.4212,-0.2628,0.4122,-0.2619,-0.2236,-0.2618,-0.2338,-0.2612,-0.242,-0.2593,-0.2499,-0.2562,-0.2573,-0.2521,-0.2639,-0.247,-0.2698,-0.2409,-0.2748,-0.234,-0.2786,-0.2265,-0.2813,-0.2185,-0.2828,-0.2102,-0.2832,-0.2017,-0.2822,-0.1933,-0.28,-0.1852,-0.2768,-0.1774,-0.2724,-0.1702,-0.267,-0.1636,-0.2606,-0.158,-0.2536,-0.1533,-0.2459,-0.1498,-0.2363,-0.1469,-0.1106,0.0576,-0.2779,0.0328,-0.2917,0.0293,-0.3086,0.0238,-0.325,0.0172,-0.3409,0.0093,-0.3561,0.0003,-0.3707,-0.0099,-0.3844,-0.0209,-0.3974,-0.033,-0.4094,-0.046,-0.4204,-0.06,-0.4305,-0.0746,-0.4393,-0.0899,-0.4471,-0.1058,-0.4536,-0.1223,-0.459,-0.1392,-0.4631,-0.1564,-0.4659,-0.1739,-0.4675,-0.1915,-0.4677,-0.2092,-0.4666,-0.2269,-0.4644,-0.2445,-0.4607,-0.2618,-0.4559,-0.2789,-0.4498,-0.2955,-0.4425,-0.3117,-0.434,-0.3273,-0.4245,-0.3422,-0.4138,-0.3563,-0.4023,-0.3696,-0.3897,-0.3821,-0.3762,-0.3937,-0.3619,-0.4042,-0.3469,-0.4136,-0.3313,-0.4219,-0.3151,-0.4291,-0.2984,-0.4351,-0.2813,-0.4398,-0.2639,-0.4432,-0.2464,-0.4454,-0.2286,-0.4462],[-0.0447,0.0845,0.0965,-0.0731,0.2811,-0.0321,0.2982,-0.0274,0.3149,-0.0215,0.3311,-0.0143,0.3468,-0.006,0.3618,0.0034,0.3761,0.0139,0.3895,0.0254,0.402,0.0379,0.4137,0.0513,0.4244,0.0655,0.4339,0.0804,0.4424,0.0959,0.4497,0.112,0.4558,0.1286,0.4607,0.1457,0.4643,0.163,0.4666,0.1806,0.4677,0.1983,0.4675,0.216,0.466,0.2336,0.4631,0.2511,0.459,0.2683,0.4538,0.2853,0.4471,0.3017,0.4394,0.3176,0.4306,0.3329,0.4206,0.3476,0.4095,0.3615,0.3975,0.3745,0.3847,0.3866,0.3708,0.3977,0.3563,0.4078,0.3411,0.417,0.3252,0.4248,0.3088,0.4314,0.292,0.437,0.2748,0.4412,0.2573,0.4442,0.2397,0.4459,0.2253,0.4464,-0.4122,0.4462,-0.4212,0.4454,-0.4302,0.4436,-0.4388,0.441,-0.4472,0.4374,-0.4552,0.4333,-0.4627,0.4282,-0.4697,0.4224,-0.4761,0.4161,-0.4819,0.409,-0.4869,0.4015,-0.4911,0.3936,-0.4946,0.3852,-0.4972,0.3765,-0.499,0.3676,-0.4999,0.3586,-0.4999,0.3496,-0.499,0.3406,-0.4972,0.3317,-0.4946,0.323,-0.4911,0.3146,-0.4869,0.3067,-0.4819,0.2991,-0.4761,0.2921,-0.4697,0.2857,-0.4627,0.2799,-0.4552,0.2749,-0.4472,0.2707,-0.4388,0.2672,-0.4302,0.2646,-0.4212,0.2628,-0.4122,0.2619,0.2236,0.2618,0.2338,0.2612,0.242,0.2593,0.2499,0.2562,0.2573,0.2521,0.2639,0.247,0.2698,0.2409,0.2748,0.234,0.2786,0.2265,0.2813,0.2185,0.2828,0.2102,0.2832,0.2017,0.2822,0.1933,0.28,0.1852,0.2768,0.1774,0.2724,0.1702,0.267,0.1636,0.2606,0.158,0.2536,0.1533,0.2459,0.1498,0.2363,0.1469]],cv=$('#c3'),cx=cv.getContext('2d');let W=0,H=0,dpr=1;
const DEP=.2,F=3.4,L=(()=>{const v=[-.45,-.6,-.66],n=Math.hypot(...v);return v.map(x=>x/n)})();
const size=()=>{dpr=Math.min(devicePixelRatio||1,2);W=cv.clientWidth;H=cv.clientHeight;cv.width=W*dpr;cv.height=H*dpr;draw()};
let P=0,T=0,mx=0,my=0,tmx=0,tmy=0,raf=0;
function draw(){
 if(!W)return;cx.setTransform(dpr,0,0,dpr,0,0);cx.clearRect(0,0,W,H);
 const mob=W<900,p=P,wire=RM?0:ss(.1,.2,p)-ss(.64,.74,p);
 const kf=(ks)=>{for(let i=0;i<ks.length-1;i++){if(p<=ks[i+1][0]||i===ks.length-2){const t=ss(ks[i][0]+.03,ks[i+1][0]-.03,p);return ks[i][1]+(ks[i+1][1]-ks[i][1])*t}}};
 const TAU=Math.PI*2,ay=kf([[0,-.42],[.28,TAU+.5],[.54,TAU-.55],[.83,2*TAU-.38],[1,2*TAU-.3]])+mx*.25,ax=kf([[0,.3],[.28,.12],[.54,-.42],[.83,.3],[1,.34]])+my*.18,az=kf([[0,0],[.28,.1],[.54,-.14],[.83,0],[1,0]]);
 const S=(mob?Math.min(W*.74,H*.36):Math.min(W*.3,H*.56))*(1+(mob?.1:.3)*wire+.1*ss(.74,1,p));
 const ox=mob?W/2:W/2+W*.1*ss(.1,.22,p),oy=mob?H*(.43-.09*ss(.1,.22,p)):H*.47;
 const cy_=Math.cos(ay),sy=Math.sin(ay),cX=Math.cos(ax),sX=Math.sin(ax),cz=Math.cos(az),sz=Math.sin(az);
 const rot=(x,y,z)=>{let a=x*cz-y*sz,b=x*sz+y*cz;x=a;y=b;a=x*cy_+z*sy;z=-x*sy+z*cy_;x=a;b=y*cX-z*sX;z=y*sX+z*cX;return[x,b,z]};
 const pr=v=>{const s=F/(F+v[2]);return[ox+v[0]*s*S,oy+v[1]*s*S]};
 /* brilho */
 const g=cx.createRadialGradient(ox,oy,0,ox,oy,S*(.75+.35*wire));g.addColorStop(0,`rgba(190,235,253,${.16+.5*wire})`);g.addColorStop(.35,`rgba(46,184,242,${.07+.1*wire})`);g.addColorStop(1,'rgba(46,184,242,0)');cx.fillStyle=g;cx.fillRect(0,0,W,H);
 const fn=rot(0,0,-1),fc=rot(0,0,-DEP/2),front=fn[0]*fc[0]+fn[1]*fc[1]+fn[2]*(fc[2]+F)<0,zc=front?-DEP/2:DEP/2,zo=-zc;
 const capI=cl(.3+.7*Math.max(0,(front?1:-1)*(fn[0]*L[0]+fn[1]*L[1]+fn[2]*L[2])));
 const col=i=>`rgb(${36+210*i|0},${58+191*i|0},${72+178*i|0})`;
 const rings=R.map(r=>{const a=[],b=[];for(let i=0;i<r.length;i+=2){a.push(pr(rot(r[i],r[i+1],zc)));b.push(pr(rot(r[i],r[i+1],zo)))}return{a,b,r}});
 const path=pts=>{cx.beginPath();pts.forEach((q,i)=>i?cx.lineTo(q[0],q[1]):cx.moveTo(q[0],q[1]));cx.closePath()};
 if(wire<1){cx.globalAlpha=1-wire;const qs=[];
  rings.forEach(({a,b,r})=>{const n=a.length;for(let i=0;i<n;i++){const j=(i+1)%n,x0=r[i*2],y0=r[i*2+1],x1=r[j*2],y1=r[j*2+1];let nx=y1-y0,ny=x0-x1;const l=Math.hypot(nx,ny)||1;nx/=l;ny/=l;const nr=rot(nx,ny,0),m=rot((x0+x1)/2,(y0+y1)/2,0);if(nr[0]*m[0]+nr[1]*m[1]+nr[2]*(m[2]+F)>=0)continue;qs.push([m[2],a[i],a[j],b[j],b[i],cl(.12+.6*Math.max(0,nr[0]*L[0]+nr[1]*L[1]+nr[2]*L[2]))])}});
  qs.sort((u,v)=>v[0]-u[0]);cx.lineWidth=.7;cx.lineJoin='round';
  for(const q of qs){cx.beginPath();cx.moveTo(q[1][0],q[1][1]);cx.lineTo(q[2][0],q[2][1]);cx.lineTo(q[3][0],q[3][1]);cx.lineTo(q[4][0],q[4][1]);cx.closePath();cx.fillStyle=cx.strokeStyle=col(q[5]);cx.fill();cx.stroke()}
  cx.fillStyle=col(.55+.45*capI);rings.forEach(({a})=>{path(a);cx.fill()});cx.globalAlpha=1}
 if(wire>0){cx.globalAlpha=wire;cx.lineJoin='round';
  rings.forEach(({a,b})=>{cx.strokeStyle='rgba(246,249,250,.35)';cx.lineWidth=1;path(b);cx.stroke();cx.beginPath();for(let i=0;i<a.length;i+=8){cx.moveTo(a[i][0],a[i][1]);cx.lineTo(b[i][0],b[i][1])}cx.stroke();
   cx.save();path(a);cx.fillStyle='rgba(126,217,251,.07)';cx.fill();cx.clip();cx.strokeStyle='rgba(246,249,250,.2)';cx.beginPath();for(let t=-.6;t<=.6;t+=.06){let u=pr(rot(t,-.6,zc)),v=pr(rot(t,.6,zc));cx.moveTo(u[0],u[1]);cx.lineTo(v[0],v[1]);u=pr(rot(-.6,t,zc));v=pr(rot(.6,t,zc));cx.moveTo(u[0],u[1]);cx.lineTo(v[0],v[1])}cx.stroke();cx.restore();
   cx.strokeStyle='rgba(246,249,250,.92)';cx.lineWidth=1.4;path(a);cx.stroke()});cx.globalAlpha=1}
}
const stage=$('#stage'),h1a=$('.h1a'),h1b=$('.h1b'),bl=$('.bl'),br=$('.br'),tl=$('.tl'),tr=$('.tr'),deg=$('#deg'),dl=$('#degl'),chs=$$('.ch'),nav0=null;
function hud(p){const o=1-ss(.02,.1,p),d=p*260;h1a.style.cssText=`opacity:${o};transform:translate3d(${-d}px,0,0)`;h1b.style.cssText=`opacity:${o};transform:translate3d(${d}px,0,0)`;
 [bl,br,tl,tr].forEach(e=>{e.style.opacity=o;e.style.visibility=o<.02?'hidden':''});
 deg.textContent=String(Math.round(p*360)).padStart(3,'0')+'°';let lb=dl.dataset.l0;
 chs.forEach(c=>{const a=+c.dataset.a,b=+c.dataset.b,v=ss(a,a+.04,p)-ss(b-.04,b,p),mob=innerWidth<900;c.style.opacity=v;c.style.transform=mob?`translate3d(0,${(1-v)*24*(p<(a+b)/2?1:-1)}px,0)`:`translate3d(0,calc(-50% + ${(1-v)*40*(p<(a+b)/2?1:-1)}px),0)`;if(p>=a&&p<=b)lb=c.dataset.l});
 if(p>.97)lb=dl.dataset.l1;dl.textContent=lb}
function loop(){raf=0;P+=(T-P)*.14;mx+=(tmx-mx)*.08;my+=(tmy-my)*.08;if(Math.abs(T-P)<.0004)P=T;draw();hud(P);if(P!==T||Math.abs(tmx-mx)>.002||Math.abs(tmy-my)>.002)raf=requestAnimationFrame(loop)}
const kick=()=>{if(!raf)raf=requestAnimationFrame(loop)};
/* marca */
const mk=$('#mk'),gb=$('#gb'),mo=$$('.mk .o'),mdg=$('#mdg'),gh=$('#gh');
/* testemunhos */
const ts=$('#tst'),qs=$$('.q'),tb=$$('.tabs div');
const prog=el=>{const r=el.getBoundingClientRect(),h=r.height-innerHeight;return h>0?cl(-r.top/h):0};
function homeScroll(){
 if(RM)return;T=prog(stage);kick();
 const m=prog(mk),a=ss(.08,.68,m)*180;gb.setAttribute('transform',`rotate(${a} 50 50)`);gh.style.opacity=1-ss(.7,.8,m);mdg.textContent=String(Math.round(a)).padStart(3,'0')+'°';const f=ss(.76,.94,m);mo.forEach(e=>e.style.fillOpacity=f);
 const t=prog(ts)*3,i=Math.min(2,t|0);qs.forEach((q,k)=>q.classList.toggle('on',k===i));tb.forEach((d,k)=>{d.classList.toggle('on',k===i);d.firstElementChild.style.width=cl(t-k)*100+'%'})
}
addEventListener('scroll',homeScroll,{passive:true});addEventListener('resize',()=>{size();homeScroll()});
if(matchMedia('(hover:hover)').matches&&!RM)addEventListener('pointermove',e=>{tmx=e.clientX/innerWidth-.5;tmy=e.clientY/innerHeight-.5;if(stage.getBoundingClientRect().bottom>0)kick()},{passive:true});
size();hud(0);homeScroll();if(RM){gb.setAttribute('transform','rotate(180 50 50)');gh.style.opacity=0;mo.forEach(e=>e.style.fillOpacity=1);mdg.textContent='180°'}
document.fonts&&document.fonts.ready.then(()=>{size()});
/* pré-visualização dos trabalhos */
const pv=$('#pv');if(pv&&matchMedia('(hover:hover)').matches){const im=$('img',pv);let px=0,py=0,tx=0,ty=0,on=false,r2=0;
 const mv=()=>{px+=(tx-px)*.16;py+=(ty-py)*.16;pv.style.transform=`translate3d(${px}px,${py}px,0)`;r2=on?requestAnimationFrame(mv):0};
 $$('.wl a').forEach(a=>{a.addEventListener('pointerenter',e=>{im.src=$('.th',a).src;tx=px=e.clientX+24;ty=py=e.clientY-120;on=true;pv.classList.add('on');if(!r2)mv()});a.addEventListener('pointermove',e=>{tx=Math.min(e.clientX+24,innerWidth-pv.offsetWidth-16);ty=e.clientY-120});a.addEventListener('pointerleave',()=>{on=false;pv.classList.remove('on')})})}

}
})();
