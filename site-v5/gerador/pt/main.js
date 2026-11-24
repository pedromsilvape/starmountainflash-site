import * as THREE from 'three';
import { SVGLoader } from 'three/examples/jsm/loaders/SVGLoader.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js';
import SYM from './sym.js';

const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const MOB = innerWidth < 768;
const DPR = Math.min(devicePixelRatio, MOB ? 1.5 : 2);
const LITE = (() => { try { const c = document.createElement('canvas'), g = c.getContext('webgl'); if (!g) return true;
  const e = g.getExtension('WEBGL_debug_renderer_info'); const r = e ? String(g.getParameter(e.UNMASKED_RENDERER_WEBGL)) : '';
  const l = g.getExtension('WEBGL_lose_context'); if (l) l.loseContext(); return /swiftshader|llvmpipe|softpipe|software|basic render/i.test(r); } catch (e) { return true; } })();
if (LITE) document.documentElement.classList.add('lite');
/* inicia uma cena só quando o elemento está perto do ecrã */
const near = (el, fn) => { if (!el) return; const o = new IntersectionObserver(es => { if (es[0].isIntersecting) { o.disconnect(); fn(); } }, { rootMargin: '120% 0px' }); o.observe(el); };
const clamp01 = v => v < 0 ? 0 : v > 1 ? 1 : v;
const smooth = (a, b, x) => { const t = clamp01((x - a) / (b - a)); return t * t * (3 - 2 * t); };
const lerp = (a, b, t) => a + (b - a) * t;
const eOQ = t => 1 - Math.pow(1 - t, 4);
const eOC = t => 1 - Math.pow(1 - t, 3);
const eIOQ = t => t < .5 ? 8 * t ** 4 : 1 - Math.pow(-2 * t + 2, 4) / 2;
const hex3 = h => { const n = parseInt(h.slice(1), 16); return new THREE.Vector3(((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255); };
const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];

/* ---------- shared ticker ---------- */
const subs = new Set(); const tick = f => subs.add(f);
let last = performance.now();
(function loop(now) { const dt = Math.min(.05, (now - last) / 1000); last = now; subs.forEach(f => f(now, dt)); requestAnimationFrame(loop); })(last);
const visible = el => { const o = { v: true }; new IntersectionObserver(e => o.v = e[0].isIntersecting, { rootMargin: '200px' }).observe(el); return o; };

/* ---------- smooth wheel scroll (desktop) ---------- */
if (!MOB && !RM) {
  let target = scrollY, cur = scrollY, active = false;
  addEventListener('wheel', e => { if (e.ctrlKey || window.__modal || document.body.classList.contains('mm')) { if (window.__modal) e.preventDefault(); return; } e.preventDefault(); target = Math.max(0, Math.min(document.documentElement.scrollHeight - innerHeight, target + e.deltaY)); active = true; }, { passive: false });
  addEventListener('scroll', () => { if (!active) { target = cur = scrollY; } }, { passive: true });
  tick(() => { if (!active) return; cur += (target - cur) * .09; if (Math.abs(target - cur) < .5) { cur = target; active = false; } scrollTo(0, cur); });
  document.addEventListener('click', e => { const a = e.target.closest('a[href^="#"]'); if (!a) return; const t = $(a.getAttribute('href')); if (!t) return; e.preventDefault(); target = Math.min(document.documentElement.scrollHeight - innerHeight, t.getBoundingClientRect().top + scrollY); active = true; });
}

/* ---------- letter reveal ---------- */
function split(el) {
  const ramp = el.dataset.ramp; if (!el.hasAttribute('aria-label')) el.setAttribute('aria-label', el.innerHTML.replace(/<br\s*\/?>/gi, ' ').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim()); const lines = el.innerHTML.split(/<br\s*\/?>/i); el.innerHTML = '';
  const letters = [];
  lines.forEach((ln, li) => {
    const tmp = document.createElement('div'); tmp.innerHTML = ln; const txt = tmp.textContent;
    const words = txt.split(' '); let pos = 0; const nl = txt.replace(/ /g, '').length;
    words.forEach((w, wi) => {
      const ws = document.createElement('span'); ws.style.cssText = 'display:inline-block;white-space:nowrap'; ws.setAttribute('aria-hidden','true');
      [...w].forEach(ch => { const s = document.createElement('span'); s.textContent = ch; s.style.display = 'inline-block';
        let a = 1; const p = nl > 1 ? pos / (nl - 1) : 0;
        if (ramp === 'hero') a = li % 2 === 0 ? 1 - p * .55 : .45 + p * .55;
        if (ramp === 'fade') a = 1 - p * .6;
        s._a = a; pos++; letters.push(s); ws.appendChild(s); });
      el.appendChild(ws); if (wi < words.length - 1) el.appendChild(document.createTextNode(' '));
    });
    if (li < lines.length - 1) el.appendChild(document.createElement('br'));
  });
  return letters;
}
function cascade(items, apply, dur = 1400, spread = .55) {
  const n = items.length; let t0 = null;
  const set = v => items.forEach((it, i) => { const s = n > 1 ? i / (n - 1) * spread : 0; apply(it, eOQ(clamp01((v - s) / (1 - spread)))); });
  set(RM ? 1 : 0);
  return () => { if (RM) return; t0 = performance.now(); const f = now => { const v = clamp01((now - t0) / dur); set(v); if (v >= 1) subs.delete(f); }; tick(f); };
}
const letterApply = (rise = 16, blur = 8) => (s, p) => { s.style.opacity = (s._a ?? 1) * p; s.style.transform = `translateY(${rise * (1 - p)}px)`; s.style.filter = p > .99 ? 'none' : `blur(${blur * (1 - p)}px)`; };
const io = (el, cb) => new IntersectionObserver((e, o) => { if (e[0].isIntersecting) { cb(); o.disconnect(); } }, { rootMargin: '0px 0px -15% 0px' }).observe(el);
let heroTitle, heroItems;
$$('[data-split]').forEach(h => { const L = split(h); const run = cascade(L, letterApply(), h.dataset.split === 'hero' ? 1600 : 1400); if (h.dataset.split === 'hero') heroTitle = run; else io(h, run); });
$$('[data-cards]').forEach(g => { const run = cascade([...g.children], (c, p) => { c.style.opacity = p; c.style.transform = `translateY(${24 * (1 - p)}px)`; c.style.filter = p > .99 ? 'none' : `blur(${12 * (1 - p)}px)`; }); io(g, run); });
heroItems = cascade($$('[data-hi]'), (c, p) => { c.style.opacity = p; c.style.transform = `translateY(${20 * (1 - p)}px)`; c.style.filter = p > .99 ? 'none' : `blur(${10 * (1 - p)}px)`; });
// statement with chips
$$('[data-statement]').forEach(h => {
  const items = []; [...h.childNodes].forEach(n => {
    if (n.nodeType === 3) { const frag = document.createDocumentFragment(); n.textContent.split(/(\s+)/).forEach(w => { if (!w) return; if (/^\s+$/.test(w)) { frag.appendChild(document.createTextNode(w)); return; } const ws = document.createElement('span'); ws.style.cssText = 'display:inline-block;white-space:nowrap'; ws.setAttribute('aria-hidden','true'); [...w].forEach(c => { const s = document.createElement('span'); s.textContent = c; s.style.display = 'inline-block'; ws.appendChild(s); items.push(s); }); frag.appendChild(ws); }); h.replaceChild(frag, n); }
    else if (n.classList && n.classList.contains('chip')) { n._chip = true; items.push(n); }
    else if (n.nodeType === 1) { const t = n.textContent; n.textContent = ''; t.split(/(\s+)/).forEach(w => { if (!w) return; if (/^\s+$/.test(w)) { n.appendChild(document.createTextNode(w)); return; } const ws = document.createElement('span'); ws.style.cssText = 'display:inline-block;white-space:nowrap'; ws.setAttribute('aria-hidden','true'); [...w].forEach(c => { const s = document.createElement('span'); s.textContent = c; s.style.display = 'inline-block'; ws.appendChild(s); items.push(s); }); n.appendChild(ws); }); }
  });
  const run = cascade(items, (s, p) => { s.style.opacity = p; s.style.filter = p > .99 ? 'none' : `blur(${8 * (1 - p)}px)`; s.style.transform = s._chip ? `translateY(.08em) scale(${.3 + .7 * p})` : `translateY(${16 * (1 - p)}px)`; }, 1800);
  io(h, run);
});

/* ---------- preloader ---------- */
let released = false; const onRelease = [];
(function pre() {
  const release = () => { if (released) return; released = true; onRelease.forEach(f => f()); };
  const ov = $('#pre'); if (!ov) { setTimeout(release, 60); return; }
  const cnt = $('#pre .cnt'), cw = $('#pre .cw'), bar = $('#pre .bo'), fill = $('#pre .bi');
  const LOAD = 1900, EXIT = 950, TOTAL = LOAD + EXIT, A = LOAD / TOTAL, DONE = A + (1 - A) * .6;
  if (RM) { ov.remove(); release(); return; }
  const t0 = performance.now(); document.documentElement.style.overflow = 'hidden';
  const f = now => { const v = clamp01((now - t0) / TOTAL), fl = eOQ(clamp01(v / A)), ex = eIOQ(clamp01((v - A) / (1 - A))), thin = clamp01(64 / innerHeight);
    ov.style.transform = `translateY(${-ex * 100}%)`; cnt.textContent = Math.round(fl * 100) + '%'; cw.style.left = Math.max(fl, .16) * 100 + '%';
    bar.style.transform = `scaleY(${thin + (1 - thin) * ex})`; fill.style.transform = `scaleX(${fl})`;
    if (v >= DONE) release(); if (v >= .45) document.documentElement.style.overflow = '';
    if (v >= 1) { ov.remove(); subs.delete(f); } };
  tick(f);
})();
onRelease.push(() => { heroTitle && heroTitle(); heroItems(); $('header').classList.add('on'); });

/* ---------- Scene A: mesh gradient ---------- */
const GV = `varying vec2 vUv;void main(){vUv=uv;gl_Position=vec4(position.xy,0.,1.);}`;
const GF = `precision highp float;varying vec2 vUv;uniform vec2 uResolution;uniform vec3 uBase;uniform vec3 uLight;uniform float uSeed;
float blob(vec2 uv,vec2 c,vec2 r){vec2 d=(uv-c)/r;return exp(-dot(d,d));}
void main(){vec2 uv=vUv;vec3 navy=vec3(0.016,0.05,0.07);vec3 ltblue=vec3(0.66,0.78,0.91);
vec3 col=mix(uBase*0.88,uBase*1.08,smoothstep(0.,1.,uv.y));
vec2 o1=0.22*vec2(sin(uSeed*1.3),cos(uSeed*1.9));vec2 o2=0.22*vec2(sin(uSeed*2.1+1.7),cos(uSeed*1.1+.6));
vec2 o3=0.22*vec2(sin(uSeed*.7+3.1),cos(uSeed*2.4+2.2));vec2 o4=0.22*vec2(sin(uSeed*1.7+4.2),cos(uSeed*.9+5.));
float dark=0.;dark+=blob(uv,vec2(.06,.86)+o1,vec2(.30,.34))*.85;dark+=blob(uv,vec2(.34,.66)+o2,vec2(.34,.34));
dark+=blob(uv,vec2(.66,.56)+o3,vec2(.46,.32))*1.1;dark+=blob(uv,vec2(.95,.66)+o4,vec2(.30,.36))*.8;
dark=smoothstep(.10,.9,clamp(dark,0.,1.));col=mix(col,navy,dark);
float g1=blob(uv,vec2(.08,-.04),vec2(.42,.36));col=mix(col,uLight,pow(clamp(g1,0.,1.),1.7)*.95);
float g2=blob(uv,vec2(.98,1.05),vec2(.40,.40));col=mix(col,ltblue,clamp(g2,0.,1.)*.4);
float l=dot(col,vec3(.299,.587,.114));col=max(mix(vec3(l),col,1.25),0.);col=max((col-.5)*1.1+.5,0.);
gl_FragColor=vec4(col,1.);}`;
function gradient(canvas, base, light, seed) {
  const r = new THREE.WebGLRenderer({ canvas, antialias: false }); r.setPixelRatio(DPR);
  const cam = new THREE.Camera(), sc = new THREE.Scene();
  const m = new THREE.ShaderMaterial({ vertexShader: GV, fragmentShader: GF, depthTest: false, depthWrite: false,
    uniforms: { uResolution: { value: new THREE.Vector2() }, uBase: { value: hex3(base) }, uLight: { value: hex3(light) }, uSeed: { value: seed } } });
  sc.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), m));
  const draw = () => { const b = canvas.parentElement.getBoundingClientRect(); r.setSize(b.width, b.height, false); r.render(sc, cam); };
  new ResizeObserver(draw).observe(canvas.parentElement); draw();
}
$$('canvas[data-grad]').forEach(c => { const [b, l, s] = c.dataset.grad.split(','); gradient(c, b, l, +s); });

/* ---------- Scene B: plasma burst ---------- */
function mulberry32(a) { return function () { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const LV = `attribute vec3 aColor;attribute vec3 aSway;attribute vec3 aSway2;attribute float aAlong;attribute float aSeed;
uniform float uTime,uSway,uSwaySpeed,uEnergy;uniform vec2 uPointer;uniform float uMagnet,uTanHalfFov,uAspect;uniform float uMagnetRadius;
varying vec3 vColor;varying float vAlong,vSeed;
void main(){vColor=aColor;vAlong=aAlong;vSeed=aSeed;vec3 p=position;float amp=uSway*aAlong*(1.0+uEnergy*1.6);float ph=aSeed*6.2831;float t=uTime*uSwaySpeed;
float w1=sin(t+ph+aAlong*5.0);float w2=cos(t*1.27+ph*1.7+aAlong*9.0);float w3=0.5*sin(t*0.6+ph);
p+=aSway*(w1+w3)*amp;p+=aSway2*w2*amp*0.8;vec4 mv=modelViewMatrix*vec4(p,1.0);
float hy=-mv.z*uTanHalfFov;float hx=hy*uAspect;vec2 targetView=vec2(uPointer.x*hx,uPointer.y*hy);
float dist=length(targetView-mv.xy);float prox=exp(-(dist*dist)/(uMagnetRadius*uMagnetRadius));float pull=uMagnet*aAlong*aAlong*prox;
mv.xy=mix(mv.xy,targetView,pull);gl_Position=projectionMatrix*mv;}`;
const LF = `precision highp float;uniform float uTime,uShimmer,uShimmerSpeed,uBright,uBrightness,uEnergy,uShock,uShockAmp,uAlpha;varying vec3 vColor;varying float vAlong,vSeed;
void main(){float sh=0.6+uShimmer*0.55*sin(vAlong*16.0-uTime*uShimmerSpeed+vSeed*28.0);sh=max(sh,0.0);float shock=0.0;
if(uShock>=0.0)shock=uShockAmp*exp(-pow((vAlong-uShock)*7.0,2.0))*2.0;vec3 c=vColor*(sh*(1.0+uEnergy*0.8)+shock)*uBright*uBrightness*uAlpha;gl_FragColor=vec4(c,1.0);}`;
const SV = `attribute vec3 aColor;attribute float aSize;attribute float aPhase;uniform float uTime,uSparkSize,uTwinkle,uPixelRatio,uEnergy;varying vec3 vColor;varying float vTw;
void main(){vColor=aColor;float tw=0.45+0.55*sin(uTime*uTwinkle+aPhase*6.2831);vTw=tw;vec4 mv=modelViewMatrix*vec4(position,1.0);
float s=uSparkSize*aSize*uPixelRatio*(200.0/max(0.001,-mv.z));gl_PointSize=s*(0.6+0.5*tw)*(1.0+uEnergy*0.4);gl_Position=projectionMatrix*mv;}`;
const SF = `precision highp float;uniform float uBrightness,uEnergy,uAlpha;varying vec3 vColor;varying float vTw;
void main(){vec2 d=gl_PointCoord-0.5;float r=length(d);float a=smoothstep(0.5,0.0,r);a*=a;vec3 c=vColor*(0.4+vTw)*(1.0+uEnergy*0.6)*uBrightness;gl_FragColor=vec4(c*uAlpha,a);}`;
const CV = `varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}`;
const CF = `precision highp float;uniform vec3 uColCore,uColMid;uniform float uTime,uGlow,uBrightness,uAlpha,uEnergy;varying vec2 vUv;
void main(){vec2 p=vUv-0.5;float r=length(p)*2.0;float core=exp(-r*r*16.0);float halo=exp(-r*4.2)*0.22;float flick=0.97+0.03*sin(uTime*1.5);float boost=1.0+uEnergy*1.2;
vec3 c=(uColCore*core+uColMid*halo)*uGlow*flick*boost*uBrightness;float a=clamp(core+halo,0.0,1.0)*uAlpha;gl_FragColor=vec4(c,a);}`;
let heroP = 0;
(function burst() {
  const cv = $('#burst'); if (!cv || LITE) return;
  const CFG = { cameraZ: 4, rotateSpeed: .24, coreSize: .39, coreGlow: .59, bloomStr: .5, bloomRadius: 0, bloomThresh: .11, lineBrightness: .55, sway: .19, swaySpeed: .6,
    sparkBrightness: .36, sparkSize: .05, twinkle: .1, colCore: '#ffffff', colInner: '#D6E6F5', colMid: '#A9C8E8', colOuter: '#4A5C6A', coreColor: '#E8F1FA', coreHalo: '#9BB8D6',
    filaments: MOB ? 40 : 60, sparks: MOB ? 400 : 700, spread: 2.65 };
  const r = new THREE.WebGLRenderer({ canvas: cv, antialias: true }); r.setPixelRatio(DPR); r.setClearColor(0, 1);
  const sc = new THREE.Scene(); sc.background = new THREE.Color(0); const cam = new THREE.PerspectiveCamera(48, 1, .1, 80); cam.position.z = CFG.cameraZ;
  const grp = new THREE.Group(); sc.add(grp); const OX = MOB ? 0 : +(cv.dataset.x || 0), OS = +(cv.dataset.s || 1); grp.position.x = OX; const rng = mulberry32(0x9e3779b9), TAU = 6.2831;
  const C = h => new THREE.Color(h); const core = C(CFG.colCore), inner = C(CFG.colInner), mid = C(CFG.colMid), outer = C(CFG.colOuter);
  const pos = [], col = [], sw = [], sw2 = [], al = [], sd = [], tips = []; const P = 64;
  for (let f = 0; f < CFG.filaments; f++) {
    const seed = rng(); const z = rng() * 2 - 1, th = rng() * TAU, rr = Math.sqrt(1 - z * z); const dir = new THREE.Vector3(rr * Math.cos(th), rr * Math.sin(th), z);
    const up = Math.abs(dir.y) > .99 ? new THREE.Vector3(1, 0, 0) : new THREE.Vector3(0, 1, 0); const u = new THREE.Vector3().crossVectors(dir, up).normalize(), v = new THREE.Vector3().crossVectors(dir, u).normalize();
    let len = CFG.spread * (.28 + rng() * rng() * 1.15); if (rng() > .86) len *= 1.7;
    const f1 = 2 + rng() * 5, f2 = 2 + rng() * 5, p1 = rng() * TAU, p2 = rng() * TAU, curlF = 0 * (.45 + rng());
    const bend = u.clone().multiplyScalar(rng() - .5).add(v.clone().multiplyScalar(rng() - .5)).normalize().multiplyScalar(.55 * (.4 + rng()));
    const pts = [], cs = [];
    for (let i = 0; i < P; i++) { const t = i / (P - 1), rad = .06 + len * t;
      const pt = dir.clone().multiplyScalar(rad).add(u.clone().multiplyScalar(Math.sin(t * f1 * Math.PI + p1) * curlF * t)).add(v.clone().multiplyScalar(Math.cos(t * f2 * Math.PI + p2) * curlF * t)).add(bend.clone().multiplyScalar(t * t));
      const ss = (a, b, x) => smooth(a, b, x); const c1 = inner.clone().lerp(mid, ss(0, .5, t)); const c = c1.lerp(outer, ss(.5, 1, t)); c.lerp(core, (1 - ss(0, .12, t)) * .9); c.multiplyScalar(lerp(1.15, .14, ss(0, 1, t)));
      pts.push(pt); cs.push([c, t]); }
    tips.push(pts[P - 1]);
    for (let i = 0; i < P - 1; i++) for (const k of [i, i + 1]) { const p = pts[k]; pos.push(p.x, p.y, p.z); col.push(cs[k][0].r, cs[k][0].g, cs[k][0].b); sw.push(u.x, u.y, u.z); sw2.push(v.x, v.y, v.z); al.push(cs[k][1]); sd.push(seed); }
  }
  const lg = new THREE.BufferGeometry(); const A = (n, a) => lg.setAttribute(n, new THREE.Float32BufferAttribute(a, n === 'aAlong' || n === 'aSeed' ? 1 : 3));
  A('position', pos); A('aColor', col); A('aSway', sw); A('aSway2', sw2); A('aAlong', al); A('aSeed', sd);
  const common = { transparent: true, depthTest: false, depthWrite: false, blending: THREE.AdditiveBlending };
  const lm = new THREE.ShaderMaterial({ ...common, vertexShader: LV, fragmentShader: LF, uniforms: { uTime: { value: 0 }, uSway: { value: CFG.sway }, uSwaySpeed: { value: CFG.swaySpeed }, uEnergy: { value: 0 }, uPointer: { value: new THREE.Vector2() }, uMagnet: { value: 0 }, uTanHalfFov: { value: Math.tan(48 * Math.PI / 360) }, uAspect: { value: 1 }, uMagnetRadius: { value: .9 }, uShimmer: { value: 0 }, uShimmerSpeed: { value: .4 }, uBright: { value: 1.1 }, uBrightness: { value: CFG.lineBrightness }, uShock: { value: -1 }, uShockAmp: { value: 0 }, uAlpha: { value: 0 } } });
  grp.add(new THREE.LineSegments(lg, lm));
  const sp = [], sc2 = [], ssz = [], sph = []; const white = C('#ffffff'), pink = C('#e6ecff');
  for (let i = 0; i < CFG.sparks; i++) { const roll = rng(); let p, bok = false;
    if (roll < .42 && tips.length) { const t = tips[Math.floor(rng() * tips.length)]; p = new THREE.Vector3(t.x + (rng() - .5) * .18, t.y + (rng() - .5) * .18, t.z + (rng() - .5) * .18); }
    else { const z = rng() * 2 - 1, th = rng() * TAU, rr = Math.sqrt(1 - z * z); let rad; if (roll < .88) rad = CFG.spread * (.12 + Math.pow(rng(), 1.4) * 1.05); else { rad = CFG.spread * (1 + rng() * 1.2); bok = true; } p = new THREE.Vector3(rr * Math.cos(th) * rad, rr * Math.sin(th) * rad, z * rad * (bok ? .7 : 1)); }
    const dN = Math.min(1, p.length() / (CFG.spread * 1.4)); const c = (rng() > .82 ? pink : white).clone().multiplyScalar(lerp(1, .35, dN) * (bok ? .55 : 1));
    sp.push(p.x, p.y, p.z); sc2.push(c.r, c.g, c.b); ssz.push(bok ? 1.1 + rng() * 1.3 : .3 + rng() * rng() * .85); sph.push(rng()); }
  const pg = new THREE.BufferGeometry(); pg.setAttribute('position', new THREE.Float32BufferAttribute(sp, 3)); pg.setAttribute('aColor', new THREE.Float32BufferAttribute(sc2, 3)); pg.setAttribute('aSize', new THREE.Float32BufferAttribute(ssz, 1)); pg.setAttribute('aPhase', new THREE.Float32BufferAttribute(sph, 1));
  const pm = new THREE.ShaderMaterial({ ...common, vertexShader: SV, fragmentShader: SF, uniforms: { uTime: { value: 0 }, uSparkSize: { value: CFG.sparkSize }, uTwinkle: { value: CFG.twinkle }, uPixelRatio: { value: DPR }, uEnergy: { value: 0 }, uBrightness: { value: CFG.sparkBrightness }, uAlpha: { value: 0 } } });
  grp.add(new THREE.Points(pg, pm));
  const cm = new THREE.ShaderMaterial({ ...common, vertexShader: CV, fragmentShader: CF, uniforms: { uColCore: { value: hex3(CFG.coreColor) }, uColMid: { value: hex3(CFG.coreHalo) }, uTime: { value: 0 }, uGlow: { value: CFG.coreGlow }, uBrightness: { value: 1 }, uAlpha: { value: 0 }, uEnergy: { value: 0 } } });
  const coreM = new THREE.Mesh(new THREE.PlaneGeometry(3, 3), cm); sc.add(coreM);
  const comp = new EffectComposer(r); comp.addPass(new RenderPass(sc, cam)); const bloom = new UnrealBloomPass(new THREE.Vector2(256, 256), CFG.bloomStr, CFG.bloomRadius, CFG.bloomThresh); comp.addPass(bloom); comp.addPass(new OutputPass());
  const size = () => { const b = cv.parentElement.getBoundingClientRect(); r.setSize(b.width, b.height, false); comp.setSize(b.width, b.height); cam.aspect = b.width / b.height; cam.updateProjectionMatrix(); lm.uniforms.uAspect.value = cam.aspect; };
  new ResizeObserver(size).observe(cv.parentElement); size();
  let ptr = { x: 0, y: 0, act: false }, pX = 0, pY = 0, mag = 0, spin = 0, introStart = null;
  addEventListener('pointermove', e => { const b = cv.getBoundingClientRect(); ptr.x = (e.clientX - b.left) / b.width * 2 - 1; ptr.y = -((e.clientY - b.top) / b.height * 2 - 1); ptr.act = e.pointerType === 'mouse' && Math.abs(ptr.x) <= 1 && Math.abs(ptr.y) <= 1; });
  onRelease.push(() => introStart = performance.now());
  const vis = visible(cv);
  tick((now, dt) => { if (!vis.v) return; const t = now / 1000;
    const ip = introStart == null ? 0 : (RM ? 1 : clamp01((now - introStart) / 1400)), ie = eOC(ip);
    spin += (CFG.rotateSpeed * (1 + heroP * 4) + (introStart == null ? 0 : (1 - ip) * 3.2)) * dt; grp.rotation.y = spin; grp.scale.setScalar(lerp(.45, 1, ie) * OS);
    cam.position.z = CFG.cameraZ / (1 + heroP * .7);
    mag += ((ptr.act ? .38 : 0) - mag) * .08; if (ptr.act) { pX += (ptr.x - pX) * .12; pY += (ptr.y - pY) * .12; }
    lm.uniforms.uMagnet.value = mag; lm.uniforms.uPointer.value.set(pX, pY);
    coreM.quaternion.copy(cam.quaternion); coreM.scale.setScalar(CFG.coreSize * OS); coreM.position.x = OX;
    [lm, pm, cm].forEach(m => { m.uniforms.uTime.value = t; m.uniforms.uAlpha.value = ie; });
    comp.render(); });
})();

/* ---------- hero shrink ---------- */
(function hero() { const s = $('#hero'), clip = $('#hero .clip'), ui = $('#hero .ui'); if (!s || !clip) return; let p = 0;
  tick(() => { const tg = clamp01(-s.getBoundingClientRect().top / (innerHeight * .6)); p += (tg - p) * .18; heroP = p; const ins = (MOB ? 12 : 24) * p;
    clip.style.clipPath = `inset(${ins}px round ${ins}px)`; ui.style.transform = `scale(${1 - p * .1})`; }); })();

/* ---------- marquee (scroll linked) ---------- */
$$('.mrow').forEach(row => { const tr = row.firstElementChild, dir = row.dataset.dir, sp = +row.dataset.speed, ONE = 100 / 6; let s = 0;
  tick(() => { s += (scrollY * sp - s) * .12; const m = ((s % ONE) + ONE) % ONE; const off = dir === 'left' ? -m : -(ONE - m); tr.style.transform = `translate3d(${off}%,0,0)`; }); });

/* ---------- Gravity field (physics spheres) ---------- */
(function gravity() { const s0 = $('#gravity'); if (!s0 || LITE) return; near(s0, gravityInit); })();
function gravityInit() {
  const sec = $('#gravity'); if (!sec) return; const cv = $('#gcanvas'), bg = $('#gbg');
  const r = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, powerPreference: 'high-performance' });
  r.setPixelRatio(DPR); r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1.15;
  if (!MOB) { r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap; }
  const sc = new THREE.Scene(), cam = new THREE.PerspectiveCamera(38, 1, .1, 100); cam.position.set(0, 0, 11);
  const pmrem = new THREE.PMREMGenerator(r); sc.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture;
  const hemi = new THREE.HemisphereLight(0xffffff, new THREE.Color('#4A5C6A'), 1.4); sc.add(hemi);
  const key = new THREE.DirectionalLight(0xffffff, 1.4); key.position.set(-6, 10, 8); key.castShadow = !MOB; key.shadow.mapSize.set(1024, 1024);
  Object.assign(key.shadow.camera, { near: .5, far: 30, left: -8, right: 8, top: 8, bottom: -8 }); key.shadow.bias = -.0003; key.shadow.radius = 12; sc.add(key);
  const rim = new THREE.DirectionalLight(0xffffff, 1.25); rim.position.set(8, 7, -8); sc.add(rim);
  const fr = new THREE.DirectionalLight(0xffffff, .4); fr.position.set(0, 0, 11); sc.add(fr);
  let vw = 10, vh = 6; const frust = () => { vh = 2 * Math.tan(THREE.MathUtils.degToRad(cam.fov) / 2) * cam.position.z; vw = vh * cam.aspect; };
  const P = (o) => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, new THREE.Color(v)]));
  const pal0 = P({ pastel: '#E4E8E8', light: '#9BA8AB', medium: '#4A5C6A', deep: '#11212D', glass: '#A9C8E8' });
  const pal1 = P({ pastel: '#9BA8AB', light: '#4A5C6A', medium: '#253745', deep: '#06141B', glass: '#7E9DBB' });
  const pal2 = P({ pastel: '#F2F7FC', light: '#D6E6F5', medium: '#A9C8E8', deep: '#4A6F94', glass: '#D6E6F5' });
  const ROLES = ['pastel', 'light', 'medium', 'deep', 'glass']; const cur = Object.fromEntries(ROLES.map(k => [k, new THREE.Color()]));
  const N = MOB ? 44 : 90; const geo = new THREE.SphereGeometry(1, MOB ? 24 : 40, MOB ? 24 : 40); const balls = [];
  for (let i = 0; i < N; i++) { let rad; const q = Math.random(); if (q < .3) rad = .27 + Math.random() * .12; else if (q < .8) rad = .42 + Math.random() * .18; else rad = .66 + Math.random() * .21; if (MOB) rad *= .8;
    const glass = Math.random() < .22; let role = 'medium', mat;
    if (glass) { role = 'glass'; mat = MOB ? new THREE.MeshPhysicalMaterial({ color: pal0.glass, roughness: .05, metalness: .1, clearcoat: 1, transparent: true, opacity: .85 })
      : new THREE.MeshPhysicalMaterial({ color: pal0.glass, roughness: .08, metalness: 0, clearcoat: 1, clearcoatRoughness: .03, transmission: .95, ior: 1.485, thickness: 2.2, specularIntensity: 1, attenuationColor: pal0.pastel, attenuationDistance: 1, emissive: pal0.glass, emissiveIntensity: .12, transparent: true }); }
    else { const c = Math.random(); role = c < .25 ? 'pastel' : c < .55 ? 'light' : c < .85 ? 'medium' : 'deep';
      mat = new THREE.MeshPhysicalMaterial({ color: pal0[role], roughness: .44, metalness: 0, clearcoat: .24, clearcoatRoughness: .35, emissive: pal0[role], emissiveIntensity: .06, transparent: true }); }
    const g = new THREE.Group(), m = new THREE.Mesh(geo, mat); m.scale.setScalar(rad); m.castShadow = m.receiveShadow = !MOB; g.add(m); sc.add(g);
    balls.push({ id: i, radius: rad, mass: rad ** 3, pos: new THREE.Vector3(), vel: new THREE.Vector3(), g, m, mat, role, glass, vs: rad, tgt: new THREE.Vector3() }); }
  const meanR = balls.reduce((s, b) => s + b.radius, 0) / N; let shapeScale = 1;
  const assignGrid = () => { // ordered system grid (no logo shapes)
    const cols = Math.ceil(Math.sqrt(N * (vw / vh) * .9)), rows = Math.ceil(N / cols); const W = Math.min(vw * .62, vh * 1.2), H = W * rows / cols; const cell = W / cols;
    shapeScale = Math.max(.25, Math.min(1, cell * .42 / meanR));
    balls.forEach((b, i) => { const cx = i % cols, cy = Math.floor(i / cols); b.tgt.set(-W / 2 + cell * (cx + .5), H / 2 - cell * (cy + .5) - vh * .04, 0); }); };
  const scatter = inward => { const R = Math.max(vw, vh) * 1.5; balls.forEach(b => { const a = Math.random() * Math.PI * 2; b.pos.set(Math.cos(a) * R * 1.25, Math.sin(a) * R * .85, (Math.random() - .5) * 4); b.g.position.copy(b.pos); inward ? b.vel.copy(b.pos).negate().normalize().multiplyScalar(.08 + Math.random() * .05) : b.vel.set(0, 0, 0); }); };
  const size = () => { const w = cv.clientWidth, h = cv.clientHeight; cam.aspect = w / h; cam.updateProjectionMatrix(); r.setSize(w, h, false); frust(); assignGrid(); };
  new ResizeObserver(size).observe(cv); size(); scatter(false);
  const mouse = { x: 99, y: 99, down: false }; addEventListener('pointermove', e => { const b = cv.getBoundingClientRect(); mouse.x = (e.clientX - b.left) / b.width * 2 - 1; mouse.y = -((e.clientY - b.top) / b.height * 2 - 1); });
  addEventListener('pointerdown', () => mouse.down = true); addEventListener('pointerup', () => mouse.down = false);
  const mv = new THREE.Vector3(), mw = new THREE.Vector3(), pm = new THREE.Vector3(), d = new THREE.Vector3(), cd = new THREE.Vector3(), rv = new THREE.Vector3(), dp = new THREE.Vector3(), ax = new THREE.Vector3();
  let started = false, eStart = 0; const vis = visible(sec); const labels = $$('#gravity [data-stage]'); let stage = -1;
  const clock = new THREE.Clock();
  tick(() => { if (!vis.v) return; const time = clock.getElapsedTime();
    const rect = sec.getBoundingClientRect(); const progress = clamp01(-rect.top / (rect.height - innerHeight)) * 3.6; // 0..3.6
    if (!started && rect.top < innerHeight * .6) { started = true; eStart = time; scatter(true); }
    if (!started) { r.render(sc, cam); return; }
    const st = progress > 2.65 ? 3 : progress > 1.55 ? 2 : progress > .7 ? 1 : 0;
    if (st !== stage) { stage = st; labels.forEach(l => l.classList.toggle('on', +l.dataset.stage === st)); bg.dataset.s = st; }
    const heroF = 1 - smooth(.3, .8, progress), drop = smooth(.4, .95, progress) * (1 - smooth(1.25, 1.75, progress)), fly = smooth(2.7, 3.45, progress), shape = smooth(1.4, 2.05, progress) * (1 - smooth(2.55, 3, progress));
    const bl = smooth(.55, 1.05, progress), bp = smooth(1.4, 1.95, progress); ROLES.forEach(k => cur[k].copy(pal0[k]).lerp(pal1[k], bl).lerp(pal2[k], bp)); hemi.groundColor.copy(cur.medium);
    const eT = eOC(clamp01((time - eStart) / 2.2)), boost = lerp(7.5, 1, eT);
    mv.set(mouse.x, mouse.y, .5).unproject(cam); const dir = mv.sub(cam.position).normalize(); mw.copy(cam.position).add(dir.multiplyScalar(-cam.position.z / dir.z));
    const inter = Math.abs(mouse.x) < .99 && Math.abs(mouse.y) < .99; let ms = inter ? Math.min(3, mw.distanceTo(pm)) : 0; pm.copy(mw);
    let damp = lerp(lerp(lerp(.91, .992, drop), .9, shape), .985, fly); const cA = Math.max(heroF, eT < 1 ? 1 : 0);
    for (const b of balls) {
      if (heroF > .01) { b.vel.x += Math.sin(time * .4 + b.id * 1.5) * .0004 * b.radius * heroF; b.vel.y += Math.cos(time * .5 + b.id * 1.2) * .0004 * b.radius * heroF; b.vel.z += Math.sin(time * .35 + b.id) * .0001 * heroF; }
      const cs = .0035 * boost * cA; if (cs > 1e-5) { b.vel.x += -b.pos.x * cs * .38; b.vel.y += -b.pos.y * cs * 1.85; b.vel.z += -b.pos.z * cs * 1.8; }
      if (drop > .001) b.vel.y -= .011 * drop;
      if (shape > .001) { const k = .06 * shape; b.vel.x += (b.tgt.x - b.pos.x) * k; b.vel.y += (b.tgt.y - b.pos.y) * k; b.vel.z += (b.tgt.z - b.pos.z) * k; }
      if (fly > .001) { const sg = (b.id * .6180339887) % 1, loc = smooth(sg * .55, sg * .55 + .45, fly); b.vel.z += .05 * loc; b.vel.x += b.pos.x * .006 * loc; b.vel.y += b.pos.y * .006 * loc; }
      if (inter) { d.subVectors(b.pos, mw); const rd = d.length(), R = mouse.down ? 6.16 : 4.4, F = mouse.down ? .085 : .05; if (rd < R && rd > 1e-4) { const q = rd / R, sf = 1 - q * q * (3 - 2 * q); d.normalize(); d.z *= .12; d.normalize(); b.vel.addScaledVector(d, sf * F * (1 + ms * 3.2)); } }
      b.vel.multiplyScalar(damp); b.pos.add(b.vel);
      const c = b.glass ? cur.glass : cur[b.role]; b.mat.color.copy(c); if (b.mat.emissive) b.mat.emissive.copy(c);
      b.mat.opacity = fly > .001 ? 1 - smooth(cam.position.z - 2.6, cam.position.z - .3, b.pos.z) : (b.glass && MOB ? .85 : 1);
      b.vs += (b.radius * (1 - (1 - shapeScale) * shape) - b.vs) * .12; b.m.scale.setScalar(b.vs); }
    const cScale = .28 * (1 - .93 * shape) * (1 - fly);
    for (let s = 0; s < (MOB ? 2 : 4); s++) for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) { const a = balls[i], b = balls[j]; cd.subVectors(b.pos, a.pos); const dist = cd.length(), mn = a.vs + b.vs;
      if (dist < mn && dist > .001) { const ov = mn - dist; cd.multiplyScalar(1 / dist); const tm = a.mass + b.mass; a.pos.addScaledVector(cd, -ov * (b.mass / tm) * cScale); b.pos.addScaledVector(cd, ov * (a.mass / tm) * cScale);
        rv.subVectors(b.vel, a.vel); const vn = rv.dot(cd); if (vn < -1e-4) { const imp = -(1.02) * vn / (1 / a.mass + 1 / b.mass); a.vel.addScaledVector(cd, -imp / a.mass); b.vel.addScaledVector(cd, imp / b.mass); } } }
    const xB = vw / 2 - .2, topY = vh / 2 - .05, floorY = -vh / 2 + .05, rest = .3 + .35 * drop;
    for (const b of balls) { const rr = b.vs;
      if (fly < .5) { if (b.pos.x < -xB - rr) { b.pos.x = -xB - rr; b.vel.x *= -.3; } else if (b.pos.x > xB + rr) { b.pos.x = xB + rr; b.vel.x *= -.3; }
        if (b.pos.y - rr < floorY) { b.pos.y = floorY + rr; if (b.vel.y < 0) b.vel.y = -b.vel.y * rest; if (drop > .3) { b.vel.x *= .86; b.vel.z *= .86; } }
        if (b.pos.y + rr > topY) { b.pos.y = topY - rr; if (b.vel.y > 0) b.vel.y *= -.3; } }
      if (fly < .02) { if (b.pos.z < -2) { b.pos.z = -2; b.vel.z *= -.3; } else if (b.pos.z > 2) { b.pos.z = 2; b.vel.z *= -.3; } }
      dp.copy(b.pos).sub(b.g.position); if (dp.lengthSq() > 1e-6) { ax.set(dp.y, -dp.x, 0).normalize(); b.g.rotateOnWorldAxis(ax, dp.length() / b.radius * .95); } b.g.position.copy(b.pos); }
    r.render(sc, cam); });
}

/* ---------- Cylinder stack ---------- */
(function cyl() { const sec = $('#cyl'); if (!sec) return; const cards = $$('#cyl .ccard'), bgs = $$('#cyl .cbg'), idx = $('#cyl .cidx'), nm = $('#cyl .cname'); const n = cards.length; let cur = 0;
  const R = MOB ? 900 : 1350, STEP = 27; const vis = visible(sec);
  tick(() => { if (!vis.v) return; const rc = sec.getBoundingClientRect(); const p = clamp01(-rc.top / (rc.height - innerHeight)); const tg = p * (n - 1 + .4) - .2; cur += (tg - cur) * .14; const f = cur;
    cards.forEach((c, i) => { const rel = i - f, rad = rel * STEP * Math.PI / 180, y = R * Math.sin(rad), z = R * Math.cos(rad) - R, dd = Math.abs(rel);
      c.style.transform = `translate3d(0,${y}px,${z}px) rotateX(${rel * STEP}deg) translate(-50%,-50%)`; c.style.opacity = dd > 3.6 ? 0 : rel < 0 ? Math.max(0, 1 + rel * 1.4) : Math.max(0, 1 - dd * .24); c.querySelector('.sc').style.opacity = Math.min(.45, dd * .25); });
    bgs.forEach((b, i) => { b.style.opacity = Math.max(0, 1 - Math.abs(i - f)); b.style.transform = `translateY(${(i - f) * 22}%) scale(1.6)`; });
    const k = Math.max(0, Math.min(n - 1, Math.round(f))); idx.textContent = String(k + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0'); nm.textContent = cards[k].dataset.name; const go = $('#cyl .cgo'); if (go) go.href = cards[k].dataset.href; }); })();

/* ---------- Chrome S (real logo extruded) ---------- */
function chrome(cv, opts) { if (LITE) return; near(cv.parentElement || cv, () => chromeInit(cv, opts)); }
function chromeInit(cv, opts) {
  const r = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); r.setPixelRatio(DPR); r.setClearColor(0, 0);
  r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = .9;
  const sc = new THREE.Scene(), cam = new THREE.PerspectiveCamera(42, 1, .1, 100); cam.position.set(0, 0, 8);
  sc.environment = new THREE.PMREMGenerator(r).fromScene(new RoomEnvironment(), .04).texture; const dl = new THREE.DirectionalLight(0xffffff, 2.2); dl.position.set(4, 6, 5); sc.add(dl);
  const data = new SVGLoader().parse(SYM), shapes = []; data.paths.forEach(p => SVGLoader.createShapes(p).forEach(s => shapes.push(s)));
  const g = new THREE.ExtrudeGeometry(shapes, { depth: 16, bevelEnabled: true, bevelThickness: 3, bevelSize: 2.2, bevelSegments: 8, curveSegments: 24 }); g.center(); g.computeBoundingBox();
  const sz = new THREE.Vector3(); g.boundingBox.getSize(sz); const s = 3.6 / Math.max(sz.x, sz.y, sz.z); g.scale(s, -s, s);
  const mesh = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: '#B9C9DA', metalness: 1, roughness: .1, envMapIntensity: 2.8 }));
  const grp = new THREE.Group(); grp.add(mesh); grp.rotation.x = .22; sc.add(grp);
  const size = () => { const b = cv.parentElement.getBoundingClientRect(); r.setSize(b.width, b.height, false); cam.aspect = b.width / b.height; cam.updateProjectionMatrix(); const mob=b.width<700;grp.scale.setScalar((mob?.62:1)*(opts.scale||1));grp.position.x=mob?0:(opts.x||0); };
  new ResizeObserver(size).observe(cv.parentElement); size();
  const vis = visible(cv); let spinV = 0, lastS = scrollY, fall = 0;
  tick(() => { if (!vis.v || (opts.active && !opts.active())) return; const tg = opts.progress(); fall += (tg - fall) * .12; grp.position.y = 9 + (-18) * clamp01(fall) + (opts.y||0) + (innerWidth<700?(opts.ym||0):0);
    if (opts.scrollSpin) { spinV = spinV * .965 + (scrollY - lastS) * .00004; spinV = Math.max(-.045, Math.min(.045, spinV)); grp.rotation.y += opts.dir * (.004 + spinV); } else grp.rotation.y += opts.dir * .004; lastS = scrollY;
    r.render(sc, cam); });
}
(function () { const w = $('#chainwrap'), cv = $('#chrome1'); if (w && cv) chrome(cv, { scrollSpin: true, dir: 1, x: 2.4, scale: .85, ym: -2.4, progress: () => { const vh = innerHeight, wt = w.getBoundingClientRect().top, pd = Math.max(1, w.offsetHeight - vh); return wt > 0 ? .5 * (1 - Math.min(wt / vh, 1)) : .5 + .5 * Math.min(-wt / pd, 1); } });
  const cv3 = $('#chrome3'); if (cv3 && MOB) chrome(cv3, { scrollSpin: false, dir: 1, scale: 1.25, x: 0, y: 0, ym: -1.2, active: () => document.body.classList.contains('mm'), progress: () => .5 });
  const f = $('footer'), cv2 = $('#chrome2'); if (f && cv2) chrome(cv2, { scrollSpin: false, dir: -1, scale: .42, y: 0, ym: .9, progress: () => { const vh = innerHeight; const top = f.getBoundingClientRect().top; return .5 * clamp01((vh - top) / vh); } }); })();

/* ---------- misc ---------- */
$$('.opt').forEach(o => o.addEventListener('click', () => { if (o.dataset.single) { $$(`.opt[data-single="${o.dataset.single}"]`).forEach(x => x.classList.remove('on')); o.classList.add('on'); } else o.classList.toggle('on'); }));
const modal = $('#modal'); window.__modal = false;
const openM = () => { modal.classList.add('on'); modal.setAttribute('aria-hidden', 'false'); window.__modal = true; document.documentElement.style.overflow = 'hidden'; };
const closeM = () => { modal.classList.remove('on'); modal.setAttribute('aria-hidden', 'true'); window.__modal = false; document.documentElement.style.overflow = ''; };
$$('[data-open]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); $('body').classList.remove('mm'); $('.dd') && $('.dd').classList.remove('on');
  const f = $('#mf'); if (f && f._reset) f._reset(); if (b.dataset.pre) $$('#mf .oc').forEach(o => o.classList.toggle('on', o.dataset.v === b.dataset.pre)); openM(); }));
$$('.sform').forEach(f => { let st = 0; const steps = [...f.querySelectorAll('.sf-step')], pr = [...f.querySelectorAll('.sf-prog span')], bar = f.querySelector('.sf-prog i'), back = f.querySelector('.back'), next = f.querySelector('.next');
  const go = n => { st = n; steps.forEach((x, i) => x.classList.toggle('on', i === n)); pr.forEach((x, i) => x.classList.toggle('on', i <= n)); bar.style.width = (Math.min(n, 2) + 1) / 3 * 100 + '%';
    back.style.visibility = n > 0 && n < 3 ? 'visible' : 'hidden'; next.style.display = n === 3 ? 'none' : ''; next.textContent = n === 2 ? 'Enviar pedido' : 'Continuar →'; };
  f.querySelectorAll('.oc').forEach(o => o.addEventListener('click', () => o.classList.toggle('on')));
  f.querySelectorAll('.cc').forEach(o => o.addEventListener('click', () => { f.querySelectorAll('.cc').forEach(x => x.classList.remove('on')); o.classList.add('on'); }));
  next.addEventListener('click', () => { if (st === 1) { const em = f.querySelector('input[type=email]'); const nm = f.querySelector('.sf-step[data-s="1"] input'); if (!nm.value || !em.value.includes('@')) { f.querySelector('.sf-step[data-s="1"]').classList.add('err'); return; } f.querySelector('.sf-step[data-s="1"]').classList.remove('err'); }
    if (st === 2 && window.sfSend) { if (next.disabled) return; const t0 = next.textContent; next.disabled = true; next.textContent = '…';
      window.sfSend(f).then(ok => { next.disabled = false; next.textContent = t0; if (ok) go(3); }); return; }
    go(Math.min(3, st + 1)); });
  back.addEventListener('click', () => go(Math.max(0, st - 1))); f._reset = () => { go(0); f.querySelectorAll('.oc').forEach(o => o.classList.remove('on')); }; go(0); });
$$('[data-close]').forEach(b => b.addEventListener('click', closeM)); addEventListener('keydown', e => { if (e.key === 'Escape') closeM(); });
$$('.sf-r').forEach(fm => fm.addEventListener('submit', e => e.preventDefault()));
$('.burger') && $('.burger').addEventListener('click', () => $('body').classList.toggle('mm')); $$('#mmenu a').forEach(a => a.addEventListener('click', () => $('body').classList.remove('mm')));
if ($('.ddb')) { $('.ddb').addEventListener('click', () => $('.dd').classList.toggle('on')); document.addEventListener('click', e => { if (!e.target.closest('.dd')) $('.dd').classList.remove('on'); }); }
$$('.field input,.field textarea').forEach(i => i.addEventListener('input', () => i.parentElement.classList.toggle('has', !!i.value)));
const form = $('#cform'); form && form.addEventListener('submit', e => { e.preventDefault(); $('#cstatus').textContent = 'Pedido enviado. Respondo-lhe eu, pelo meio que escolheu.'; form.reset(); $$('.field').forEach(f => f.classList.remove('has')); });
const clk = $('#clock'); if (clk) { const u = () => clk.textContent = new Date().toLocaleTimeString('pt-PT'); u(); setInterval(u, 1000); }

/* ---------- subpages ---------- */
$$('.sform[data-pre]').forEach(f => f.querySelectorAll('.oc').forEach(o => o.classList.toggle('on', o.dataset.v === f.dataset.pre)));
$$('[data-tabs]').forEach(w => { const bs = [...w.querySelectorAll('[data-t]')], ps = [...w.querySelectorAll('[data-p]')]; let auto = true, i = 0;
  const show = k => { i = k; bs.forEach((b, j) => b.classList.toggle('on', j === k)); ps.forEach((p, j) => p.classList.toggle('on', j === k)); };
  bs.forEach((b, k) => b.addEventListener('click', () => { auto = false; show(k); })); show(0);
  if (w.dataset.tabs === 'auto' && !RM) { const v = visible(w); setInterval(() => { if (auto && v.v) show((i + 1) % bs.length); }, 4200); } });
// hero visual: invoices -> sheet
(function () { const el = $('#vis-auto'); if (!el) return; const rows = [...el.querySelectorAll('.xr')], cnt = el.querySelector('.cnt b'), doc = el.querySelector('.doc'); let k = 0, n = 0;
  const step = () => { if (k >= rows.length) { rows.forEach(r => r.classList.remove('in')); k = 0; }
    doc.classList.remove('scan'); void doc.offsetWidth; doc.classList.add('scan'); const d = rows[k].dataset; ['f','d','t'].forEach(x => doc.querySelector('.v' + x).textContent = d[x]);
    setTimeout(() => { rows[k].classList.add('in'); n++; cnt.textContent = n; k++; }, 1100); };
  if (RM) { rows.forEach(r => r.classList.add('in')); cnt.textContent = rows.length; return; } onRelease.push(() => { step(); setInterval(step, 2400); }); })();
// hero visual: week bars
(function () { const el = $('#vis-star'); if (!el) return; const bars = [...el.querySelectorAll('.wb i')], tot = el.querySelector('.tot b');
  const run = () => { bars.forEach((b, j) => { b.style.transition = 'none'; b.style.transform = 'scaleY(0)'; }); void el.offsetWidth;
    bars.forEach((b, j) => { b.style.transition = `transform .9s cubic-bezier(.16,1,.3,1) ${j * .07}s`; b.style.transform = 'scaleY(1)'; });
    let t0 = performance.now(); const T = +tot.dataset.m; const f = now => { const v = clamp01((now - t0) / 1800); const m = Math.round(T * eOQ(v)); tot.textContent = Math.floor(m / 60) + 'h' + String(m % 60).padStart(2, '0'); if (v >= 1) subs.delete(f); }; tick(f); };
  if (RM) return; onRelease.push(() => { run(); setInterval(run, 7000); }); })();
// hero visual: assistant chat
(function () { const el = $('#vis-rag'); if (!el) return; const a = el.querySelector('.ans'), txt = a.dataset.txt, src = el.querySelector('.srcs'), st = el.querySelector('.stt');
  const run = () => { a.textContent = ''; src.classList.remove('on'); st.textContent = 'a procurar nos documentos…'; let i = 0;
    setTimeout(() => { st.textContent = '2 documentos encontrados'; const f = () => { a.textContent = txt.slice(0, ++i); if (i < txt.length) setTimeout(f, 22); else src.classList.add('on'); }; f(); }, 1300); };
  if (RM) { a.textContent = txt; src.classList.add('on'); return; } onRelease.push(() => { run(); setInterval(run, 9000); }); })();

// generic cycler
$$('[data-cycle]').forEach(c => { const gs = [...c.querySelectorAll('[data-g]')]; const n = +c.dataset.n || Math.max(...gs.map(g => g.children.length)); let k = 0;
  const show = () => gs.forEach(g => [...g.children].forEach((ch, j) => ch.classList.toggle('on', g.dataset.g === 'upto' ? j <= k - (+g.dataset.off || 0) : j === k % g.children.length)));
  show(); if (RM) { k = n - 1; show(); return; } const v = visible(c); setInterval(() => { if (!v.v) return; k = (k + 1) % n; show(); }, +c.dataset.cycle || 2600); });
$$('img[data-from]').forEach(i => { const s = document.querySelector(i.dataset.from); if (s) i.src = s.src; });

$$('[data-filter]').forEach(f => { const bs = [...f.querySelectorAll('[data-f]')], sec = f.parentElement, cards = [...sec.querySelectorAll('[data-cat]')], pg = sec.querySelector('.pgn'), PER = 6; let cat = '*', page = 0;
  const render = (scroll) => { const list = cards.filter(c => cat === '*' || c.dataset.cat === cat), n = Math.ceil(list.length / PER); page = Math.min(page, n - 1);
    cards.forEach(c => c.style.display = 'none'); list.slice(page * PER, page * PER + PER).forEach(c => { c.style.display = ''; c.style.opacity = 1; c.style.transform = 'none'; c.style.filter = 'none'; });
    pg.innerHTML = n > 1 ? `<button type="button" data-p="${page - 1}" ${page === 0 ? 'disabled' : ''} aria-label="Página anterior">←</button>` + Array.from({ length: n }, (_, i) => `<button type="button" data-p="${i}" class="${i === page ? 'on' : ''}">${i + 1}</button>`).join('') + `<button type="button" data-p="${page + 1}" ${page === n - 1 ? 'disabled' : ''} aria-label="Página seguinte">→</button><span>${page * PER + 1}–${Math.min(list.length, page * PER + PER)} de ${list.length}</span>` : '';
    if (scroll) window.scrollTo({ top: sec.getBoundingClientRect().top + scrollY - 80, behavior: 'smooth' }); };
  bs.forEach(b => b.addEventListener('click', () => { bs.forEach(x => x.classList.toggle('on', x === b)); cat = b.dataset.f; page = 0; render(false); }));
  pg.addEventListener('click', e => { const b = e.target.closest('[data-p]'); if (!b || b.disabled) return; page = +b.dataset.p; render(true); }); render(false); });

$$('form[data-go]').forEach(f => f.addEventListener('submit', e => { e.preventDefault(); if (!f.checkValidity()) { f.reportValidity(); return; } if (window.sfLp) { window.sfLp(f); return; } location.href = f.dataset.go; }));
