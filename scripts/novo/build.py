#!/usr/bin/env python3
"""Desenho 2026 da Starmountain Flash.

  python3 scripts/novo/build.py assets            -> public/assets/site/sf26.{css,js}, src/styles/40-sf26.css, chrome.ts
  python3 scripts/novo/build.py inicio ORIGEM     -> public/inicio/index.html e public/en/index.html
  python3 scripts/novo/build.py converter ORIGEM  -> páginas de serviço, sobre, método e contacto (PT e EN)

ORIGEM é uma cópia de public/ no estado anterior ao desenho 2026 (commit d0 do ramo main):
os textos e as demonstrações de cada página saem de lá. A conversão é feita uma vez; depois
disso as páginas em public/ passam a ser a fonte e editam-se diretamente.
"""
import json, os, re, sys, urllib.parse
from bs4 import BeautifulSoup

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..'))
PUB = os.path.join(RAIZ, 'public')
rd = lambda p: open(p, encoding='utf-8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)

SYM = rd(os.path.join(RAIZ, 'scripts/identidade/simbolo.d')).strip()
NOME = rd(os.path.join(RAIZ, 'scripts/identidade/nome.svgfrag')).strip()
NOME_VB = rd(os.path.join(RAIZ, 'scripts/identidade/nome.vb')).strip()
SYM_VB = '3.40 8.40 93.20 83.20'
AR = '<svg width="11" height="11" viewBox="0 0 11 11" fill="none" aria-hidden="true"><path d="M2 9 9 2M3.5 2H9v5.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
MAIL = 'geral@starmountainflash.pt'

T = {
 'pt': dict(skip='Saltar para o conteúdo', nav='Principal', servicos='Serviços', trabalhos='Trabalhos', metodo='Método', sobre='Sobre', blog='Blog', contacto='Contacto',
            cta='Proposta gratuita', menu='Abrir menu', outra='EN', outra_t='English version', outra_l='en', fechar='Fechar',
            g1='Presença digital', g2='Automações com IA', explorar='Explorar', legal='Legal', topo='Voltar ao topo', onde='Onde estamos',
            estado='Proposta visual gratuita', cidade='Covilhã', md_t='Conte-me o que <em>precisa.</em>', md_p='Leio e respondo eu, por email ou WhatsApp.',
            priv='Privacidade', cookies='Cookies', termos='Termos', aviso='Aviso legal', livro='Livro de Reclamações', fim=('Conte-me o que', 'precisa.'),
            svc=[('Websites', '/websites'), ('Lojas online', '/lojas-online'), ('Visibilidade em IA', '/visibilidade-ia'), ('Avaliações Google', '/avaliacoes-google')],
            svc2=[('Método StarMap', '/starmap'), ('Automações à medida', '/automacoes'), ('Assistente interno', '/assistente-interno')]),
 'en': dict(skip='Skip to content', nav='Main', servicos='Services', trabalhos='Work', metodo='Method', sobre='About', blog='Blog', contacto='Contact',
            cta='Free proposal', menu='Open menu', outra='PT', outra_t='Versão em português', outra_l='pt-PT', fechar='Close',
            g1='Digital presence', g2='AI automations', explorar='Explore', legal='Legal', topo='Back to top', onde='Find us',
            estado='Free visual proposal', cidade='Covilhã', md_t='Tell me what you <em>need.</em>', md_p='I read and answer every message myself, by email or WhatsApp.',
            priv='Privacy', cookies='Cookies', termos='Terms', aviso='Legal notice', livro='Complaints book', fim=('Tell me what you', 'need.'),
            svc=[('Websites', '/websites'), ('Online stores', '/lojas-online'), ('AI visibility', '/visibilidade-ia'), ('Google reviews', '/avaliacoes-google')],
            svc2=[('StarMap Method', '/starmap'), ('Custom automations', '/automacoes'), ('Internal assistant', '/assistente-interno')]),
}
def P(lang, path):
    if lang == 'pt': return path
    return '/en' if path == '/' else '/en' + path

# ---------------------------------------------------------------- chrome
def brand(lang):
    return (f'<a class="s-brand" href="{P(lang, "/")}" aria-label="Starmountain Flash"><svg class="lgm" viewBox="{SYM_VB}" fill="currentColor" aria-hidden="true"><path d="{SYM}"/></svg>'
            f'<svg class="lgw" viewBox="{NOME_VB}" aria-hidden="true">{NOME}</svg></a>')

def links(lang, home=False):
    t = T[lang]; h = '' if home else P(lang, '/')
    return [(t['servicos'], h + '#servicos'), (t['trabalhos'], h + '#trabalhos'), (t['metodo'], P(lang, '/metodo')), (t['sobre'], P(lang, '/sobre')), (t['blog'], P(lang, '/blog')), (t['contacto'], P(lang, '/contacto'))]

def prefix_form(html):
    """Formulário com as classes prefixadas (x-): fica fora do alcance do CSS antigo de cada página."""
    s = BeautifulSoup(html, 'html.parser')
    for e in s.find_all(True):
        if e.get('class'): e['class'] = ['x-' + c for c in e['class'] if c != 'rv']
        if e.name == 'svg': e.replace_with(BeautifulSoup(AR, 'html.parser'))
    for sp in s.find_all('span', attrs={'lang': True}): sp.unwrap()
    return str(s)

def topo(lang, alt, form, home=False, aqui=''):
    """Nav, menu de ecrã inteiro e pop-up de proposta."""
    t = T[lang]; ls = links(lang, home)
    nav = ''.join(f'<a href="{h}"{" aria-current=page" if aqui and h == aqui else ""}>{n}</a>' for n, h in ls)
    ol = ''.join(f'<li><a href="{h}"><span>0{i + 1}</span>{n}</a></li>' for i, (n, h) in enumerate(ls))
    sv = (f'<b>{t["g1"]}</b>' + ''.join(f'<a href="{P(lang, h)}">{n}</a>' for n, h in t['svc']) + f'<b style="margin-top:14px">{t["g2"]}</b>' + ''.join(f'<a href="{P(lang, h)}">{n}</a>' for n, h in t['svc2']))
    return f'''<a class="s-skip" href="#main">{t["skip"]}</a>
<header class="s-nav" id="s-nav">{brand(lang)}<nav aria-label="{t["nav"]}">{nav}</nav>
<div class="s-tools"><a class="s-lang" href="{alt}" hreflang="{t["outra_l"]}" title="{t["outra_t"]}">{t["outra"]}</a><a class="pill" href="{P(lang, "/contacto")}" data-modal>{t["cta"]} {AR}</a><button class="s-burger" id="s-burger" type="button" aria-expanded="false" aria-controls="s-menu" aria-label="{t["menu"]}"><i></i><i></i></button></div></header>
<div class="s-menu" id="s-menu"><ol>{ol}</ol><div class="s-msv">{sv}</div><div class="s-mft"><span>{MAIL} · {t["cidade"]}, <span class="s-clock"></span></span><a class="pill s" href="{P(lang, "/contacto")}" data-modal>{t["cta"]} {AR}</a></div></div>
<div class="s-md" id="s-md" role="dialog" aria-modal="true" aria-labelledby="s-md-t" aria-hidden="true"><div class="s-mp"><button class="s-mx" type="button" aria-label="{t["fechar"]}"><svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M2 2l10 10M12 2 2 12"/></svg></button>
<span class="s-k s-md-of">{t["cta"]}</span><h3 id="s-md-t">{t["md_t"]}</h3><p>{t["md_p"]}</p>{form}</div></div>'''

def rodape(lang, home=False, form='', form_t='', tag='footer'):
    t = T[lang]; ls = links(lang, home)
    cols = (f'<div><span>{t["explorar"]}</span>' + ''.join(f'<a href="{h}">{n}</a>' for n, h in ls) + '</div>'
            f'<div><span>{t["servicos"]}</span>' + ''.join(f'<a href="{P(lang, h)}">{n}</a>' for n, h in t['svc'] + t['svc2']) + '</div>'
            f'<div><span>{t["contacto"]}</span><a href="mailto:{MAIL}">{MAIL}</a><a href="tel:+351937800553">+351 937 800 553</a><a href="https://wa.me/351937800553">WhatsApp</a>'
            f'<span style="margin-top:22px">{t["onde"]}</span><a href="https://www.instagram.com/starmountainflash/" rel="noopener">Instagram</a><a href="https://www.linkedin.com/company/starmountain-flash" rel="noopener">LinkedIn</a><a href="https://www.trustpilot.com/review/starmountainflash.pt" rel="noopener">Trustpilot</a><a href="https://www.google.com/search?kgmid=/g/11nvdc1v3n" rel="noopener">Google</a></div>'
            f'<div><span>{t["legal"]}</span><a href="{P(lang, "/privacidade")}">{t["priv"]}</a><a href="{P(lang, "/cookies")}">{t["cookies"]}</a><a href="{P(lang, "/termos")}">{t["termos"]}</a><a href="{P(lang, "/aviso-legal")}">{t["aviso"]}</a><a href="https://www.livroreclamacoes.pt" rel="noopener">{t["livro"]}</a></div>')
    fim = f'<h2 class="rv">{t["fim"][0]} <span>{t["fim"][1]}</span></h2>'
    fw = f'<div class="s-fw"><h3>{form_t}</h3>{form}</div>' if form else ''
    return f'''<{tag} class="s-end{"" if home else " min"}"{' id="contacto"' if home else ''}><div class="w"><p class="s-sx"><span>{t["estado"]}</span><span>{t["cidade"]} · <span class="s-clock"></span></span></p>
{fim}<a class="s-mail" href="mailto:{MAIL}">{MAIL}</a>{fw}
<div class="s-ft">{cols}</div><p class="s-cp"><span>© 2026 Starmountain Flash</span><a class="s-up" href="#top">{t["topo"]} ↑</a></p></div></{tag}>'''

HEAD_EXTRA = ('<link rel="preload" as="font" type="font/woff2" href="/assets/site/geist-latin-300.woff2" crossorigin>'
              '<link rel="stylesheet" href="/assets/site/sf26.css">'
              '<script>document.documentElement.classList.add("js");setTimeout(function(){document.documentElement.classList.add("rvx")},4500)</script>')

# ---------------------------------------------------------------- CSS
def blocos(css):
    """Parte CSS em (cabeçalho, corpo) de nível superior."""
    out = []; i = 0; n = len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        d = 1; k = j + 1
        while k < n and d:
            if css[k] == '{': d += 1
            elif css[k] == '}': d -= 1
            k += 1
        out.append((css[i:j].strip(), css[j + 1:k - 1])); i = k
    return out

def sels(s):
    out = []; d = 0; cur = ''
    for ch in s:
        if ch == '(': d += 1
        elif ch == ')': d -= 1
        if ch == ',' and d == 0: out.append(cur.strip()); cur = ''
        else: cur += ch
    if cur.strip(): out.append(cur.strip())
    return out

def prefixar(css, pre):
    out = []
    for h, b in blocos(css):
        h2 = re.sub(r'/\*.*?\*/', '', h, flags=re.S).strip()
        if h2.startswith('@media') or h2.startswith('@supports'): out.append(h2 + '{' + prefixar(b, pre) + '}')
        elif h2.startswith('@'): out.append(h2 + '{' + b + '}')
        else: out.append(','.join(('body' + pre + s[4:]) if s == 'body' or s.startswith('body ') else pre + ' ' + s for s in sels(h2)) + '{' + b + '}')
    return '\n'.join(out)

CONT = {'nav', 'mob', 'md', 'ft', 'fwrap', 'dd', 'pan', 'lang', 'macc', 'mset', 'mlinks', 'cf', 'brand', 'menu', 'tools', 'burger', 'cta', 'cta2', 'mp'}
SUBJ = {'hero', 'hwrap', 'hl', 'hfoot', 'hbg', 'acts', 'eb', 'lead', 'btn', 'lk', 'sh2', 'faq', 'st', 'qs', 'contact', 'side', 'cc', 'cic'}
NEUTRAS = {'hero', 'band', 'in', 'js', 'fhead'}
def morre(sel):
    comps = [c for c in re.split(r'\s*[>+~]\s*|\s+', re.sub(r'::?[\w-]+(\([^)]*\))?', '', sel)) if c]
    if not comps: return False
    cl = [set(re.findall(r'\.([\w-]+)', c)) for c in comps]
    el = [(re.match(r'^[a-z][a-z0-9]*', c) or [''])[0] if not c.startswith('.') else '' for c in comps]
    el = [e if isinstance(e, str) else e for e in el]
    if any(c & CONT for c in cl): return True
    if any(e in ('details', 'summary') for e in el): return True
    if cl[-1] & SUBJ: return True
    todas = set().union(*cl)
    if el[-1] in ('h1', 'h2', 'h3', 'body', 'html', 'em', 'section') and not cl[-1] and todas <= NEUTRAS and '#' not in comps[-1]: return True
    return False

def limpar_css(css):
    out = []
    for h, b in blocos(css):
        h2 = re.sub(r'/\*.*?\*/', '', h, flags=re.S).strip()
        if h2.startswith('@font-face'):
            if '"PF"' in b or '"IN"' in b: continue
            out.append(h2 + '{' + b + '}')
        elif h2.startswith('@media') or h2.startswith('@supports'):
            inner = limpar_css(b)
            if inner.strip(): out.append(h2 + '{' + inner + '}')
        elif h2.startswith('@'): out.append(h2 + '{' + b + '}')
        else:
            keep = [s for s in sels(h2) if not morre(s)]
            if keep: out.append(','.join(keep) + '{' + b + '}')
    return '\n'.join(out)

CORES = {'#0E6B4C': '#0B6E9E', 'rgba(14,107,76': 'rgba(18,135,191', '#0A1A13': '#04141C', '#0B0D0C': '#04141C', 'rgba(11,13,12': 'rgba(4,20,28', 'rgba(8,10,9': 'rgba(4,20,28',
         '#6FD1A6': '#2EB8F2', '#8FE0BD': '#7ED9FB', '#5A5F5D': '#3F5967', '#8D928F': '#5E7885', '#F6F7F6': '#F6F9FA', '#F1F2F1': '#EEF4F7'}
def modernizar(css):
    """Aproxima os componentes antigos do desenho novo: cantos retos, sem maiúsculas espaçadas nem itálicos."""
    css = re.sub(r'border-radius:(\d+)px', lambda m: 'border-radius:' + ('4px' if 10 <= int(m.group(1)) <= 60 else m.group(1) + 'px'), css)
    css = re.sub(r'text-transform:uppercase;?', '', css)
    css = re.sub(r'letter-spacing:\.(\d+)em', lambda m: 'letter-spacing:0' if float('0.' + m.group(1)) >= .05 else m.group(0), css)
    css = css.replace('font-style:italic', 'font-style:normal').replace('font:italic ', 'font:normal ')
    return css

def cores(h):
    for a, b in CORES.items(): h = h.replace(a, b).replace(a.lower(), b)
    return h

def anel():
    subs = [s for s in re.split(r'(?=M)', SYM) if s.strip()]; rings = []
    for s in subs:
        p = [(float(a), float(b)) for a, b in re.findall(r'(-?[\d.]+),(-?[\d.]+)', s)]
        if p[0] == p[-1]: p = p[:-1]
        ar = sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))
        if ar < 0: p = p[::-1]
        rings.append([round(v, 4) for x, y in p[::2] for v in ((x - 50) / 93.2, (y - 50) / 93.2)])
    return rings, subs[0].strip()

def assets():
    c = lambda n: rd(os.path.join(AQUI, 'css', n))
    symurl = 'data:image/svg+xml,' + urllib.parse.quote(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{SYM_VB}"><path d="{SYM}" fill="none" stroke="#7ED9FB" stroke-opacity=".16" stroke-width=".25"/></svg>', safe="/:=,' ")
    base = c('00-base.css') + c('10-chrome.css')
    home = prefixar(c('20-home.src.css').replace(' .k{', ' .s-k{').replace(' .k,', ' .s-k,'), '.home')
    wr(os.path.join(PUB, 'assets/site/sf26.css'), base + '\n/* página inicial */\n' + home + '\n' + c('30-inner.css').replace('__SYMURL__', symurl))
    wr(os.path.join(RAIZ, 'src/styles/40-sf26.css'), '/* Gerado por scripts/novo/build.py a partir de scripts/novo/css/. Não editar à mão. */\n' + base + '\n' + c('40-next.css'))
    rings, _ = anel()
    wr(os.path.join(PUB, 'assets/site/sf26.js'), rd(os.path.join(AQUI, 'js/sf26.js')).replace('__PTS__', json.dumps(rings, separators=(',', ':'))))
    print('assets ok')

# ---------------------------------------------------------------- página inicial
NOVO = {
 'pt': dict(tl='Starmountain Flash', h1a='Websites e automações', h1b='com IA para empresas.', tr='Covilhã, Portugal', scroll='Faça scroll', l1='Trabalhos', ver='Ver trabalho',
            ch=[('Clientes', 'A empresa é boa, mas quem pesquisa encontra a concorrência.'), ('Horas', 'Encomendas copiadas do email para o Excel, faturas lançadas uma a uma.'),
                ('O que faço', 'Faço o site que é encontrado e ponho o trabalho repetido a correr sozinho.')],
            mk=('Dois módulos, uma rotação.', 'O símbolo é um S feito de dois módulos iguais. O segundo é o primeiro, rodado 180° em torno do centro.', 'O símbolo, construído'),
            pull=['Impecavelmente bem feito.', 'Simples, rápido e profissional.', 'Uma experiência muito positiva.'],
            nums=[('+8', 'Projetos entregues', ''), ('3', 'Sites para a UBI', None)],
            sobre=('Antes da contabilidade houve o Exército', 'Antes dos sites houve o Exército'), percurso='Conhecer o percurso', hero_stat='+8 projetos entregues · 3 deles para a Universidade da Beira Interior'),
 'en': dict(tl='Starmountain Flash', h1a='Websites and AI', h1b='automations for businesses.', tr='Covilhã, Portugal', scroll='Scroll', l1='Work', ver='View project',
            ch=[('Customers', 'The business is good, but anyone who searches finds a competitor instead.'), ('Hours', 'Orders copied from email into Excel, invoices entered one by one.'),
                ('What I do', 'I build the site that gets found and set the repetitive work to run on its own.')],
            mk=('Two modules, one rotation.', 'The symbol is an S made of two identical modules. The second is the first, rotated 180° around the centre.', 'The symbol, constructed'),
            pull=['Impecavelmente bem feito.', 'Simples, rápido e profissional.', 'Uma experiência muito positiva.'],
            nums=[('+8', 'Projects delivered', ''), ('3', 'Websites for UBI', None)],
            sobre=('Before accounting there was the Army', 'Before websites there was the Army'), percurso='Read the full story', hero_stat='+8 projects delivered · 3 of them for the University of Beira Interior'),
}
DOM = ['dei.ubi.pt', 'comunidadeplanet.pt', 'gestaocrew.pt', 'personaltrainerbeatriznunes.pt']

def inicio(orig):
    for lang, src, dst in (('pt', 'inicio/index.html', 'inicio/index.html'), ('en', 'en/index.html', 'en/index.html')):
        h = rd(os.path.join(orig, src)); s = BeautifulSoup(h, 'html.parser'); m = s.find('main'); t = T[lang]; n = NOVO[lang]
        tx = lambda e: e.get_text(' ', strip=True)
        inner = lambda e: ''.join(str(c) for c in (e.find('span', attrs={'lang': True}) or e).contents)
        lead = tx(m.select_one('.hero p.lead.ls'))
        pains = [tx(x).rstrip('.') for x in m.select('#para-quem .pain h3')]
        works = [(tx(a.h3), tx(a.p), a.img['src'], a['href'], a.img.get('alt', '')) for a in m.select('#trabalhos a.work')]
        tlead = tx(m.select_one('#trabalhos p.lead')); th2 = tx(m.select_one('#trabalhos h2'))
        sh2 = tx(m.select_one('#servicos h2')); slead = tx(m.select_one('#servicos p.lead'))
        grp = [(tx(g.select_one('.gh h3')), tx(g.select_one('.gh p')), [(tx(a.h3), a['href']) for a in g.select('a.card')]) for g in m.select('#servicos .grp')]
        mh = m.select_one('#metodo h2'); msp = mh.find('span', attrs={'lang': True}) or mh
        mem = msp.find('em'); msub = tx(mem) if mem else ''
        if mem: mem.extract()
        mt = tx(msp)
        fases = [(tx(p.h3), tx(p.select_one('.ps')), tx(p.select_one('.pt')), [tx(c) for c in p.select('.chips > *')]) for p in m.select('#metodo .ph2')]
        quotes = [(tx(q.blockquote), tx(q.figcaption.find(['b', 'strong']) or q.figcaption), ) for q in m.select('.quote')]
        qsrc = []
        for q in m.select('.quote'):
            fc = q.figcaption; nome = tx(fc.find(['b', 'strong'])) if fc.find(['b', 'strong']) else tx(fc)
            resto = tx(fc).replace(nome, '', 1).strip(' ·'); qsrc.append((tx(q.blockquote), nome, resto.split(' · ')[0]))
        sob = m.select_one('#sobre'); sh = tx(sob.h2); sp = [tx(p) for p in sob.select('p.rv')]; simg = sob.img['src']; salt = sob.img.get('alt', '')
        sp = [p.replace(*n['sobre']) for p in sp]
        fh = tx(m.select_one('#faq h2'))
        faqs = [(tx(d.summary).rstrip('+').strip(), tx(d.p)) for d in m.select('#faq details')]
        ct = m.select_one('#contacto'); cform = prefix_form(str(ct.find('form'))); clead = tx(ct.select_one('p.lead'))
        mdform = prefix_form(str(s.select_one('#md form')))
        strip_l = tx(m.find_previous('div') and s.select_one('.strip .l')) if s.select_one('.strip .l') else ''
        nums = [(a, b, strip_l if c is None else c) for a, b, c in n['nums']]
        alt = P('en' if lang == 'pt' else 'pt', '/')
        _, r1 = anel()
        head = h[h.index('<head>'):h.index('<style>')]
        head = re.sub(r'<link rel="preload" as="image"[^>]*>\n?', '', head).replace('content="#0B0D0C"', 'content="#04141C"')
        head_tail = h[h.index('</style>') + 8:h.index('</head>')]
        dl = lambda i, a, b, l, k, x: f'<article class="ch" data-a="{a}" data-b="{b}" data-l="{l}"><p class="s-k">0{i} · {k}</p><h2>{x}</h2></article>'
        body = f'''<body class="home" id="top">
{topo(lang, alt, mdform, home=True)}
<main id="main">
<section class="stage hero" id="stage"><div class="pin"><canvas id="c3" aria-hidden="true"></canvas>
<p class="tl">{n["tl"]}</p><p class="tr">{n["tr"]} · <span class="s-clock"></span></p>
<h1><span class="h1a">{n["h1a"]}</span> <span class="h1b">{n["h1b"]}</span></h1>
<div class="bl"><p>{lead}</p><small>{n["hero_stat"]}</small></div>
<div class="deg" aria-hidden="true"><b id="deg">000°</b><span id="degl" data-l0="{n["scroll"]}" data-l1="{n["l1"]}">{n["scroll"]}</span></div>
<a class="pill s br" href="{P(lang, "/contacto")}" data-modal>{t["cta"]} {AR}</a>
{dl(1, ".16", ".4", n["ch"][0][0], pains[0], n["ch"][0][1])}
{dl(2, ".42", ".66", n["ch"][1][0], pains[1], n["ch"][1][1])}
{dl(3, ".7", ".96", n["ch"][2][0], n["ch"][2][0], n["ch"][2][1])}
</div></section>

<section class="lt pad" id="trabalhos" data-t="lt"><div class="w"><div class="hd rv"><h2>{th2}</h2><p>{tlead}</p></div>
<ol class="wl">{''.join(f'<li class="rv"><a href="{hr}"><span class="n">0{i + 1}</span><span class="nm">{nm}</span><span class="mt"><b>{DOM[i]}</b><span>{d}</span><u>{n["ver"]} {AR}</u></span><img class="th" src="{img}" alt="{al or nm}" width="900" height="515" loading="lazy" decoding="async"></a></li>' for i, (nm, d, img, hr, al) in enumerate(works))}</ol></div>
<div class="pv" id="pv" aria-hidden="true"><img alt="" width="900" height="515"></div></section>

<section class="lt mk" id="mk" data-t="lt"><div class="mpin">
<svg viewBox="-12 -12 124 124" aria-hidden="true"><g class="g"><rect x="3.4" y="8.4" width="93.2" height="83.2"/><path d="M-12 50H112M50-12V112M-12-12 112 112M112-12-12 112"/><circle cx="50" cy="50" r="46.6"/><circle cx="50" cy="50" r="24"/><circle cx="29" cy="31" r="14"/><circle cx="71" cy="69" r="14"/></g>
<path class="o" d="{r1}"/><path class="o gh g" id="gh" d="{r1}" style="fill:none"/><g id="gb"><path class="o" d="{r1}"/></g><circle cx="50" cy="50" r=".9" fill="#0B6E9E"/></svg>
<div class="mt1"><h2>{n["mk"][0]}</h2><p>{n["mk"][1]}</p></div>
<p class="s-k mlb">{n["mk"][2]}</p><p class="mdg" id="mdg" aria-hidden="true">000°</p></div></section>

<section class="dk2 pad" id="servicos"><div class="w"><div class="hd rv"><h2>{sh2}</h2><p>{slead}</p></div>
<div class="two rv">{''.join(f'<div><h3>{g[0]}</h3><span class="s-k">{g[1]}</span><ol>' + ''.join(f'<li><a href="{hr}"><span>{"ab"[gi]}.{i + 1}</span>{nm}</a></li>' for i, (nm, hr) in enumerate(g[2])) + '</ol></div>' for gi, g in enumerate(grp))}</div>
<div class="mth" id="metodo"><div class="hd rv"><h2>{mt}</h2><p>{msub}</p></div>
<div class="rows">{''.join(f'<div class="row rv"><span class="n">0{i + 1}</span><div><h3>{a}</h3><p>{b}</p></div><div><p>{c}</p><ul>{"".join(f"<li>{x}</li>" for x in ch)}</ul></div></div>' for i, (a, b, c, ch) in enumerate(fases))}</div>
<p class="mais rv"><a class="pill" href="{P(lang, "/metodo")}">{t["metodo"]} {AR}</a></p></div></div></section>

<section class="lt tst" id="tst" data-t="lt"><div class="tpin"><div class="w"><div class="tq">{''.join(f'<figure class="q{" on" if i == 0 else ""}"><h3>{n["pull"][i]}</h3><div><blockquote>{q}</blockquote><figcaption><i>{nm[0]}</i><span><b>{nm}</b><small>{so}</small></span></figcaption></div></figure>' for i, (q, nm, so) in enumerate(qsrc))}</div>
<div class="tabs" aria-hidden="true">{''.join(f'<div{" class=on" if i == 0 else ""}><i></i><span>0{i + 1} / 0{len(qsrc)}</span>{nm}</div>' for i, (q, nm, so) in enumerate(qsrc))}</div></div></div></section>

<section class="lt pad" data-t="lt" style="padding-top:0"><div class="w"><div class="st">{''.join(f'<div class="sr rv"><b>{a}</b><p>{b}{f"<small>{c}</small>" if c else ""}</p></div>' for a, b, c in nums)}</div>
<div class="ab" id="sobre"><img class="rv" src="{simg}" alt="{salt}" width="800" height="800" loading="lazy" decoding="async">
<div class="rv"><h2>{sh}</h2>{''.join(f"<p>{p}</p>" for p in sp)}<a class="pill d" href="{P(lang, "/sobre")}">{n["percurso"]} {AR}</a></div></div>
<div class="fq" id="faq"><h2 class="rv">{fh}</h2><div>{''.join(f'<details><summary>{q}<i></i></summary><p>{a}</p></details>' for q, a in faqs)}</div></div></div></section>
</main>
{rodape(lang, home=True, form=cform, form_t=clead)}
<script src="/assets/site/sf26.js" defer></script>
</body></html>'''
        doc = '<!doctype html>\n' + re.search(r'<html[^>]*>', h).group(0) + '\n' + head + HEAD_EXTRA + head_tail + '</head>\n' + body
        wr(os.path.join(PUB, dst), doc); print(dst, len(doc))

# ---------------------------------------------------------------- páginas interiores
PAGS = ['websites', 'lojas-online', 'visibilidade-ia', 'avaliacoes-google', 'starmap', 'automacoes', 'assistente-interno', 'sobre', 'metodo', 'contacto']
def converter(orig, textos=None):
    textos = textos or {}
    for lang in ('pt', 'en'):
        t = T[lang]
        for pg in PAGS:
            rel = (pg if lang == 'pt' else 'en/' + pg) + '/index.html'
            h = rd(os.path.join(orig, rel))
            mdform = prefix_form(re.search(r'<div class="md".*?(<form class="cf".*?</form>)', h, re.S).group(1))
            # CSS
            a = h.index('<style>'); b = h.index('</style>')
            h = h[:a] + '<style>' + modernizar(limpar_css(h[a + 7:b])) + '</style>' + HEAD_EXTRA + h[b + 8:]
            h = re.sub(r'<link rel="preload" as="image"[^>]*>\n?', '', h)
            # chrome
            a = h.index('<header class="nav"'); b = h.index('<main')
            alt = P('en' if lang == 'pt' else 'pt', '/' + pg)
            h = h[:a] + topo(lang, alt, mdform, aqui=P(lang, '/' + pg)) + '\n' + h[b:]
            h = h.replace('<main id="top">', '<main id="main">', 1)
            # hero sem fotografia
            a = h.index('<section class="hero"'); b = h.index('</section>', a)
            hero = re.sub(r'<picture>.*?</picture>', '', h[a:b], flags=re.S)
            hero = re.sub(r'<small>.*?</small>', '', hero, flags=re.S)
            h = h[:a] + hero + h[b:]
            # formulários
            h = re.sub(r'<form class="cf[^"]*">.*?</form>', lambda m: prefix_form(m.group(0)), h, flags=re.S)
            # rodapé
            a = h.index('<div class="fwrap">'); b = h.index('<script', a)
            h = h[:a] + rodape(lang) + '\n' + h[b:]
            # script principal antigo
            h = re.sub(r'<script>\s*\(function\(\)\{\s*const d=document\.documentElement;d\.classList\.add\(\'js\'\);.*?</script>', '<script src="/assets/site/sf26.js" defer></script>', h, count=1, flags=re.S)
            assert 'setLang(' not in h, rel
            h = re.sub(r'<body([^>]*)>', lambda m: '<body' + m.group(1) + ' class="inner" id="top">', h, count=1)
            h = re.sub(r'<svg width="(\d+)" height="\d+" viewBox="0 0 32 32"[^>]*><path d="M5 18 L16 7 L27 18"/><path d="M5 27 L16 16 L27 27"/></svg>', lambda m: f'<svg width="{m.group(1)}" height="{m.group(1)}" viewBox="{SYM_VB}" fill="currentColor" aria-hidden="true"><path d="{SYM}"/></svg>', h)
            h = cores(h).replace('content="#04141C"', 'content="#04141C"')
            for a, b in textos.get(lang, {}).get(pg, []):
                if isinstance(a, str):
                    assert a in h, (rel, a); h = h.replace(a, b)
                else:
                    assert a.search(h), (rel, a.pattern); h = a.sub(b, h)
            wr(os.path.join(PUB, rel), h); print(rel, len(h))


# ---------------------------------------------------------------- páginas soltas (análise gratuita, cartão)
LP_CORES = {'#00A870': '#2EB8F2', '#12B87E': '#7ED9FB', 'rgba(0,168,112': 'rgba(46,184,242', '#0E4B35': '#0B6E9E', '#4FB78E': '#7ED9FB', '#0D0F0E': '#04141C', '#0B0D0C': '#04141C',
            '#F2F1ED': '#F6F9FA', '#E4DFD1': '#EDF3F6', '#E6E4DE': '#E6EEF1', '#ECEAE4': '#EDF3F6', '#D9D7D0': '#D5DEE3', '#BDBBB3': '#B4C4CC', '#C9C7BF': '#C5D3D9', '#555A57': '#3F5967',
            '#3B3F3C': '#24404D', '#878986': '#5E7885', '#626563': '#3F5967', '#474B48': '#24404D', 'rgba(8,10,9': 'rgba(4,20,28',
            '#082D1E': '#062635', '#106B54': '#0B6E9E', '#090A0A': '#04141C', '#0F1211': '#0A2430', '#1C2422': '#123040', '#8E9A94': '#8FA6B0'}
def troca(h, mapa):
    for a, b in mapa.items(): h = re.sub(re.escape(a), b, h, flags=re.I)
    return h
def soltas(orig):
    import base64
    marca = (f'<svg width="30" height="27" viewBox="{SYM_VB}" fill="currentColor" aria-hidden="true" style="flex:none"><path d="{SYM}"/></svg>'
             f'<svg viewBox="{NOME_VB}" role="img" aria-label="Starmountain Flash" style="height:13px;width:170px;display:block">{NOME}</svg>')
    fontes = ('@font-face{font-family:G;font-weight:300;font-display:swap;src:url(/assets/site/geist-latin-300.woff2) format("woff2")}'
              '@font-face{font-family:G;font-weight:400;font-display:swap;src:url(/assets/site/geist-latin-400.woff2) format("woff2")}'
              '@font-face{font-family:G;font-weight:500;font-display:swap;src:url(/assets/site/geist-latin-500.woff2) format("woff2")}'
              '@font-face{font-family:G;font-weight:600 700;font-display:swap;src:url(/assets/site/geist-latin-600.woff2) format("woff2")}')
    extra = (':root{--font-onest:G,system-ui,sans-serif;--lgf:#1287BF}.hero .brand,.dark .brand{--lgf:#2EB8F2}.brand{display:inline-flex;align-items:center;gap:10px}'
             'body{font-family:G,system-ui,sans-serif}h1,h2,h3{font-weight:300!important;letter-spacing:-.045em!important}h3{font-weight:400!important;letter-spacing:-.025em!important}'
             '.wrap{padding:0}.hero{border-radius:0!important}')
    for rel in ('analise-gratuita/index.html', 'analise-gratuita/obrigado/index.html', 'en/analise-gratuita/index.html', 'en/analise-gratuita/obrigado/index.html'):
        h = rd(os.path.join(orig, rel))
        h = re.sub(r'@font-face\{font-family:onest;src:url\(data:font/woff2;base64,[^)]*\)[^}]*\}', '', h)
        h = re.sub(r'@font-face\{font-family:onest Fallback;[^}]*\}', '', h)
        h = re.sub(r'font-family:onest,onest Fallback,', 'font-family:G,', h).replace('--font-onest:"onest","onest Fallback"', '--font-onest:G,system-ui')
        a = h.index('<style'); a2 = h.index('>', a) + 1; b = h.index('</style>', a)
        h = h[:a2] + fontes + modernizar(h[a2:b]) + extra + h[b:]
        h = re.sub(r'<svg[^>]*viewBox="0 0 32 32"[^>]*>\s*<path d="M5 18 L16 7 L27 18"></path><path d="M5 27 L16 16 L27 27"></path></svg>\s*Starmountain Flash', marca, h)
        h = troca(h, LP_CORES)
        h = re.sub(r'<meta name="theme-color" content="[^"]*">', '<meta name="theme-color" content="#04141C">', h)
        wr(os.path.join(PUB, rel), h); print(rel, len(h), 'M5 18' in h)
    h = rd(os.path.join(orig, 'card/index.html'))
    logo = base64.b64encode(rd(os.path.join(RAIZ, 'scripts/identidade/logotipo-principal-fundo-escuro.svg')).encode()).decode()
    h = re.sub(r'(<img class="logo" src="data:image/svg\+xml;base64,)[^"]+', lambda m: m.group(1) + logo, h)
    h = troca(h, LP_CORES)
    wr(os.path.join(PUB, 'card/index.html'), h); print('card', len(h))

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'assets'
    if cmd == 'assets': assets()
    elif cmd == 'inicio': inicio(sys.argv[2])
    elif cmd == 'soltas': soltas(sys.argv[2])
    elif cmd == 'converter':
        sys.path.insert(0, AQUI)
        try: from textos import TEXTOS
        except ImportError: TEXTOS = {}
        converter(sys.argv[2], TEXTOS)
