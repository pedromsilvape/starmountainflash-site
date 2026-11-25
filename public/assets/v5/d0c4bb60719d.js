/* Starmountain Flash · consentimento, medição e envio de formulários (site v5). */
(function () {
  var D = document, EN = (D.documentElement.lang || '').indexOf('en') === 0;
  var GA = 'G-NSBV4CEZNF', CLARITY = 'zirtxh4z0q', PIXEL = '1379397673888561', KEY = 'smf-consent';
  var T = EN ? {
    t: 'A quick question about cookies.',
    p: 'I would like to measure visits (Google Analytics and Microsoft Clarity) and, for advertising, use the Meta Pixel. Only with your permission. The site works the same if you decline. Details in the ',
    pl: 'cookie policy', all: 'Accept all', no: 'Decline', pick: 'Choose', save: 'Save choice',
    m: 'Measurement', md: 'Google Analytics and Microsoft Clarity: which pages are useful and where visits come from.',
    k: 'Marketing', kd: 'Meta Pixel: measuring Facebook and Instagram ads.',
    err: 'The request could not be sent. Please try again or write to geral@starmountainflash.pt.', href: '/en/cookies'
  } : {
    t: 'Um pedido rápido sobre cookies.',
    p: 'Gostava de medir as visitas (Google Analytics e Microsoft Clarity) e, para publicidade, usar o Pixel da Meta. Só com a sua autorização. O site funciona na mesma se recusar. Detalhes na ',
    pl: 'política de cookies', all: 'Aceitar tudo', no: 'Recusar', pick: 'Escolher', save: 'Guardar escolha',
    m: 'Medição', md: 'Google Analytics e Microsoft Clarity: que páginas são úteis e de onde chegam as visitas.',
    k: 'Marketing', kd: 'Pixel da Meta: medir os anúncios no Facebook e no Instagram.',
    err: 'Não foi possível enviar o pedido. Tente outra vez ou escreva para geral@starmountainflash.pt.', href: '/cookies'
  };

  /* ---------- origem da visita (só nesta sessão, para juntar ao pedido) ---------- */
  var ORIG = 'smf-orig';
  try {
    if (!sessionStorage.getItem(ORIG)) {
      var q = new URLSearchParams(location.search), ref = '';
      try { ref = D.referrer ? new URL(D.referrer).hostname.replace(/^www\./, '') : ''; } catch (e) {}
      if (ref === location.hostname.replace(/^www\./, '')) ref = '';
      var utm = [q.get('utm_source'), q.get('utm_medium'), q.get('utm_campaign')].filter(Boolean).join('/');
      sessionStorage.setItem(ORIG, JSON.stringify({ e: location.pathname, u: utm, r: ref || (q.get('de') ? 'de=' + q.get('de') : '') }));
    }
  } catch (e) {}
  function origem(tipo) {
    var o = {}; try { o = JSON.parse(sessionStorage.getItem(ORIG) || '{}'); } catch (e) {}
    var s = [tipo + ' ' + location.pathname, o.e && o.e !== location.pathname ? 'entrada ' + o.e : '', o.u ? 'utm ' + o.u : '', o.r ? 'ref ' + o.r : (o.u ? '' : 'direto')];
    return s.filter(Boolean).join(' · ').replace(/[^\w\-\/\.\s·=áéíóúãõçÁÉÍÓÚ]/g, '').slice(0, 120);
  }

  /* ---------- consentimento ---------- */
  var c = null; try { c = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) {}
  var loaded = { m: false, k: false };
  function load(src) { var s = D.createElement('script'); s.async = true; s.src = src; D.head.appendChild(s); }
  function apply() {
    if (!c) return;
    if (c.m && !loaded.m) {
      loaded.m = true;
      window.dataLayer = window.dataLayer || []; window.gtag = function () { dataLayer.push(arguments); };
      gtag('js', new Date()); gtag('config', GA);
      load('https://www.googletagmanager.com/gtag/js?id=' + GA);
      (function (c2, l, a, r, i) { c2[a] = c2[a] || function () { (c2[a].q = c2[a].q || []).push(arguments); }; var t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i; l.head.appendChild(t); })(window, D, 'clarity', 'script', CLARITY);
      try { window.clarity('consent'); } catch (e) {}
    }
    if (c.k && !loaded.k) {
      loaded.k = true;
      (function (f, b, e, v, n) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; load(v); })(window, D, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
      fbq('init', PIXEL); fbq('track', 'PageView');
    }
  }
  function save(m, k) {
    var was = c; c = { m: !!m, k: !!k, d: new Date().toISOString().slice(0, 10) };
    try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {}
    hide();
    if (was && ((was.m && !c.m) || (was.k && !c.k))) { location.reload(); return; }
    apply();
  }
  var bar;
  function hide() { if (bar) bar.classList.add('off'); }
  function show(now) {
    if (!bar) {
      bar = D.createElement('div'); bar.className = now ? 'ckb' : 'ckb off'; bar.setAttribute('role', 'dialog'); bar.setAttribute('aria-label', 'Cookies');
      bar.innerHTML = '<b>' + T.t + '</b><p>' + T.p + '<a href="' + T.href + '">' + T.pl + '</a>.</p>'
        + '<div class="ckc" hidden><label><input type="checkbox" data-c="m"><span><b>' + T.m + '</b>' + T.md + '</span></label><label><input type="checkbox" data-c="k"><span><b>' + T.k + '</b>' + T.kd + '</span></label></div>'
        + '<div class="ckbt"><button type="button" class="pill d" data-a="all">' + T.all + '</button><button type="button" class="pill o" data-a="no">' + T.no + '</button><button type="button" class="pill o" data-a="pick">' + T.pick + '</button></div>';
      D.body.appendChild(bar);
      bar.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        var a = b.dataset.a, box = bar.querySelector('.ckc');
        if (a === 'all') save(1, 1);
        else if (a === 'no') save(0, 0);
        else if (a === 'pick') {
          if (box.hidden) { box.hidden = false; box.querySelector('[data-c=m]').checked = !!(c && c.m); box.querySelector('[data-c=k]').checked = !!(c && c.k); b.textContent = T.save; }
          else save(box.querySelector('[data-c=m]').checked, box.querySelector('[data-c=k]').checked);
        }
      });
    }
    if (!now) requestAnimationFrame(function () { bar.classList.remove('off'); });
  }
  apply();
  if (!c) show(true);
  D.addEventListener('click', function (e) { var a = e.target.closest('[data-ck]'); if (a) { e.preventDefault(); show(false); } });

  /* ---------- eventos ---------- */
  function ev(name, p) { try { if (window.gtag && loaded.m) gtag('event', name, p || {}); } catch (e) {} }
  function lead(servico) { ev('generate_lead', { servico: servico }); try { if (window.fbq && loaded.k) fbq('track', 'Lead', { content_name: servico }); } catch (e) {} }
  D.addEventListener('click', function (e) {
    var a = e.target.closest('a'); if (!a) return;
    var h = a.getAttribute('href') || '';
    if (h.indexOf('https://wa.me') === 0) { ev('contact_click', { metodo: 'whatsapp' }); try { loaded.k && fbq('track', 'Contact'); } catch (x) {} }
    else if (h.indexOf('mailto:') === 0) ev('contact_click', { metodo: 'email' });
    else if (h.indexOf('tel:') === 0) ev('contact_click', { metodo: 'telefone' });
    else if (/^\/(en\/)?trabalhos\/./.test(h)) ev('ver_caso', { caso: h.split('/').pop() });
    else if (a.closest('.lang')) ev('mudar_idioma', { para: a.title || a.textContent.trim() });
    else if (/^https?:/.test(h) && a.host !== location.host) ev('link_externo', { url: a.host });
  });
  D.addEventListener('click', function (e) { var b = e.target.closest('[data-open]'); if (b) ev('abrir_formulario', { servico: b.dataset.pre || '' }); });
  var art = D.querySelector('article.prose:not(.legal)');
  if (art && 'IntersectionObserver' in window) {
    var end = D.createElement('i'); art.appendChild(end);
    var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { ev('artigo_lido', { artigo: location.pathname }); io.disconnect(); } });
    io.observe(end);
  }

  /* ---------- envio dos formulários para /api/lead ---------- */
  function post(body) {
    return fetch('/api/lead', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.ok; }).catch(function () { return false; });
  }
  function erro(el, ok) {
    var p = el.querySelector('.sf-err');
    if (!p) { p = D.createElement('p'); p.className = 'sf-err'; p.setAttribute('role', 'alert'); el.appendChild(p); }
    p.textContent = ok ? '' : T.err; p.hidden = ok;
  }
  window.sfSend = function (f) {
    var txt = function (el) { return el ? el.textContent.trim() : ''; };
    var sv = [].map.call(f.querySelectorAll('.oc.on'), function (o) { return o.dataset.v; }).join(', ');
    var s1 = f.querySelectorAll('.sf-step[data-s="1"] input'), ta = f.querySelector('textarea'), via = txt(f.querySelector('.cc.on'));
    var msg = [ta && ta.value.trim(), via ? (EN ? 'Reply by: ' : 'Resposta por: ') + via : ''].filter(Boolean).join('\n');
    var body = { nome: s1[0].value, empresa: s1[1].value, email: s1[2].value, telefone: s1[3].value, servico: sv.slice(0, 60), mensagem: msg,
      origem: origem(f.closest('#modal, .modal, [role=dialog]') ? 'Pop-up' : 'Formulário'), website: '' };
    return post(body).then(function (ok) {
      erro(f.querySelector('.sf-step[data-s="2"]') || f, ok);
      if (ok) { lead(sv || 'Geral'); f.querySelectorAll('input,textarea').forEach(function (i) { i.value = ''; }); }
      return ok;
    });
  };
  window.sfLp = function (f) {
    var b = f.querySelector('button[type=submit]'), t0 = b.textContent;
    b.disabled = true; b.textContent = EN ? 'Sending…' : 'A enviar…';
    var site = f.querySelector('[name=website]').value.trim();
    post({ nome: f.querySelector('[name=nome]').value, email: f.querySelector('[name=email]').value, servico: EN ? 'Free website review' : 'Análise gratuita ao site',
      mensagem: (EN ? 'Website to review: ' : 'Site a analisar: ') + site, origem: origem('Landing page'), website: '' })
      .then(function (ok) {
        b.disabled = false; b.textContent = t0; erro(f, ok);
        if (ok) { lead(EN ? 'Free website review' : 'Análise gratuita'); setTimeout(function () { location.href = f.dataset.go; }, 300); }
      });
  };
})();
