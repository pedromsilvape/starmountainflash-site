
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const MOB = innerWidth < 768;
const DPR = Math.min(devicePixelRatio, MOB ? 1.5 : 2);
const LITE = (() => { if (/[?&]fx=1/.test(location.search)) return false; try { const c = document.createElement('canvas'), g = c.getContext('webgl'); if (!g) return true;
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

let heroP = 0;

/* ---------- hero shrink ---------- */
(function hero() { const s = $('#hero'), clip = $('#hero .clip'), ui = $('#hero .ui'); if (!s || !clip) return; let p = 0;
  tick(() => { const tg = clamp01(-s.getBoundingClientRect().top / (innerHeight * .6)); p += (tg - p) * .18; heroP = p; const ins = (MOB ? 12 : 24) * p;
    clip.style.clipPath = `inset(${ins}px round ${ins}px)`; ui.style.transform = `scale(${1 - p * .1})`; }); })();

/* ---------- marquee (scroll linked) ---------- */
$$('.mrow').forEach(row => { const tr = row.firstElementChild, dir = row.dataset.dir, sp = +row.dataset.speed, ONE = 100 / 6; let s = 0;
  tick(() => { s += (scrollY * sp - s) * .12; const m = ((s % ONE) + ONE) % ONE; const off = dir === 'left' ? -m : -(ONE - m); tr.style.transform = `translate3d(${off}%,0,0)`; }); });


/* ---------- Cylinder stack ---------- */
(function cyl() { const sec = $('#cyl'); if (!sec) return; const cards = $$('#cyl .ccard'), bgs = $$('#cyl .cbg'), idx = $('#cyl .cidx'), nm = $('#cyl .cname'); const n = cards.length; let cur = 0;
  const R = MOB ? 900 : 1350, STEP = 27; const vis = visible(sec);
  tick(() => { if (!vis.v) return; const rc = sec.getBoundingClientRect(); const p = clamp01(-rc.top / (rc.height - innerHeight)); const tg = p * (n - 1 + .4) - .2; cur += (tg - cur) * .14; const f = cur;
    cards.forEach((c, i) => { const rel = i - f, rad = rel * STEP * Math.PI / 180, y = R * Math.sin(rad), z = R * Math.cos(rad) - R, dd = Math.abs(rel);
      c.style.transform = `translate3d(0,${y}px,${z}px) rotateX(${rel * STEP}deg) translate(-50%,-50%)`; c.style.opacity = dd > 3.6 ? 0 : rel < 0 ? Math.max(0, 1 + rel * 1.4) : Math.max(0, 1 - dd * .24); c.querySelector('.sc').style.opacity = Math.min(.45, dd * .25); });
    bgs.forEach((b, i) => { b.style.opacity = Math.max(0, 1 - Math.abs(i - f)); b.style.transform = `translateY(${(i - f) * 22}%) scale(1.6)`; });
    const k = Math.max(0, Math.min(n - 1, Math.round(f))); idx.textContent = String(k + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0'); nm.textContent = cards[k].dataset.name; const go = $('#cyl .cgo'); if (go) go.href = cards[k].dataset.href; }); })();


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

/* ---------- cenas 3D: carregadas à parte, depois da página ---------- */
window.SF = { tick, visible, near, LITE, MOB, DPR, RM, onRelease, get released() { return released; }, get heroP() { return heroP; } };
if (LITE) {
  $$('canvas[data-grad]').forEach(c => { const [b, l] = c.dataset.grad.split(','); c.style.background = `radial-gradient(120% 90% at 8% 0%, ${l} 0, ${b} 55%)`; });
} else {
  const go = () => { const s = document.createElement('script'); s.src = '__SF_SCENES__'; s.async = true; document.body.appendChild(s); };
  if (document.readyState === 'complete') setTimeout(go, 0); else addEventListener('load', () => setTimeout(go, 0));
}
