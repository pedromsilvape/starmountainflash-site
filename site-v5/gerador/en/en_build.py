import re, json, os, sys, html as H, datetime
sys.path.insert(0, '/home/claude/site-nova/v5'); sys.path.insert(0, '/home/claude/site-nova/en')
os.chdir('/home/claude/site-nova/v5')
import tok
# ---- dictionary
S = json.load(open('/home/claude/site-nova/en/src.json'))
D = {}
for f in ['tr1.txt', 'tr2.txt', 'tr3.txt', 'tr4.txt']:
    for l in open('/home/claude/site-nova/en/' + f, encoding='utf8'):
        l = l.rstrip('\n')
        if '|' not in l: continue
        i, e = l.split('|', 1)
        D[S[int(i)]] = e
for k, v in json.load(open('/tmp/cx/casos_pairs.json')).items(): D.setdefault(k, v)
EX = '/home/claude/site-nova/en/extra.txt'
if os.path.exists(EX):
    for l in open(EX, encoding='utf8'):
        l = l.rstrip('\n')
        if ' ⇒ ' in l:
            a, b = l.split(' ⇒ ', 1); D[a] = b
# ---- EN sources
import pages5 as P5, pages7 as P7
EN_MESES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
P5.data_pt = lambda d: f'{d.day} {EN_MESES[d.month - 1]} {d.year}'
P5.SRC = '/home/claude/repo/starmountainflash-site/content/blog/en'
_open = open
PT_POSTS = P5.POSTS
P5.POSTS = P5.ler()
for p in P5.POSTS: p['md'] = p['md'].replace('](/en/', '](/')
P5.SLUGS = {p['slug'] for p in P5.POSTS}
P5.tu = lambda p: False
P7.R = '/home/claude/repo/starmountainflash-site/src/app/en/'
EN_SLUGS = P5.SLUGS
# ---- run PT build definitions (writes PT pages too, identical output)
src = open('build_all.py').read()
src = src.replace("OUT = '/home/claude/site-nova/pub6'", "OUT = '/home/claude/site-nova/pub6'")
cut = src.index("for pg in P6.pages():")
src = src[:cut]
src = src.replace("open(f'{OUT}/index.html', 'w').write(links(fill(home), False))", "HOME = links(fill(home), False)")
exec(src)
OUT_EN = '/home/claude/site-nova/pub6/en'
miss = set()
def T(s):
    if s is None: return s
    k = re.sub(r'\s+', ' ', H.unescape(s)).strip()
    if k in D: return D[k]
    if tok.has_word(k): miss.add(k)
    return s
def tjson(o):
    if isinstance(o, dict): return {k: (tjson(v) if k not in ('@type', '@id', 'url', 'item', 'mainEntityOfPage', 'email', 'telephone', 'priceCurrency', 'lowPrice', 'addressCountry', 'opens', 'closes', 'dateCreated', 'datePublished', 'dateModified') else enurl(v)) for k, v in o.items()}
    if isinstance(o, list): return [tjson(x) for x in o]
    if isinstance(o, str):
        if o == 'pt-PT': return 'en'
        return T(o) if tok.has_word(o) and not o.startswith('http') else o
    return o
def enurl(v):
    if isinstance(v, dict): return tjson(v)
    if isinstance(v, str) and v.startswith(U + '/') and not any(x in v for x in ('#negocio', '#pedro-pereira', '#site')):
        return U + '/en/' + v[len(U) + 1:]
    if v == U + '/': return U + '/en'
    return v
def fix_meta(page, slug):
    def jl(m):
        g = json.loads(m.group(1)); return '<script type="application/ld+json">' + json.dumps(tjson(g), ensure_ascii=False) + '</script>'
    page = re.sub(r'<script type="application/ld\+json">(.*?)</script>', jl, page, flags=re.S)
    pt = f'{U}/{slug}' if slug else U + '/'
    en = f'{U}/en/{slug}' if slug else U + '/en'
    page = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{en}">', page, count=1)
    page = re.sub(r'<link rel="alternate" hreflang="pt-PT"[^>]*><link rel="alternate" hreflang="en"[^>]*><link rel="alternate" hreflang="x-default"[^>]*>',
                  f'<link rel="alternate" hreflang="pt-PT" href="{pt}"><link rel="alternate" hreflang="en" href="{en}"><link rel="alternate" hreflang="x-default" href="{pt}">', page, count=1)
    page = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{en}">', page, count=1)
    page = page.replace('content="pt_PT"', 'content="en_GB"')
    page = page.replace('<html lang="pt-PT">', '<html lang="en">')
    page = re.sub(r'<title>(.*?)</title>', lambda m: '<title>' + H.escape(T(m.group(1)), quote=False) + '</title>', page, count=1)
    page = re.sub(r'(<meta (?:name|property)="(?:description|og:title|og:description)" content=")([^"]*)(")', lambda m: m.group(1) + H.escape(T(m.group(2))) + m.group(3), page)
    return page
def lang(page, slug, depth):
    pt = '../' * (depth + 1) + ((slug + '/index.html') if slug else 'index.html')
    # PT anchors -> PT page, EN anchors -> self
    page = re.sub(r'<a class="on" href="[^"]*" title="Português">', f'<a href="{pt}" title="Português">', page)
    page = re.sub(r'<a href="https://starmountainflash\.pt/en[^"]*" title="English">', '<a class="on" href="index.html" title="English">', page)
    page = re.sub(r'<a( class="on")? href="[^"]*"(><svg viewBox="0 0 30 20">(?:(?!</a>).)*?</svg> Português</a>)', lambda m: f'<a href="{pt}"' + m.group(2), page, flags=re.S)
    page = re.sub(r'<a href="https://starmountainflash\.pt/en[^"]*"(><svg viewBox="0 0 60 30">)', r'<a class="on" href="index.html"\1', page)
    return page
def missing_posts(page, depth):
    # links to PT-only posts -> PT version
    for s in [p['slug'] for p in PT_POSTS if p['slug'] not in EN_SLUGS]:
        page = re.sub(r'href="((?:\.\./)*)blog/' + s + '/index.html"', lambda m: f'href="{m.group(1)}../blog/{s}/index.html" hreflang="pt"', page)
    return page
def write(slug, page):
    depth = slug.count('/') + 1 if slug else 0
    page = tok.translate(page, D, miss)
    page = re.sub(r'(\d+) min de leitura', r'\1 min read', page).replace('<span>Atualizado a ', '<span>Updated ')
    page = page.replace('aria-label="P\\xE1gina anterior"', 'aria-label="Previous page"').replace('aria-label="P\\xE1gina seguinte"', 'aria-label="Next page"')
    page = re.sub(r'\} de \$\{(\w+)\.length\}', r'} of ${\1.length}', page)
    page = page.replace('"Enviar pedido"', '"Send request"').replace('"Continuar \\u2192"', '"Continue \\u2192"').replace('"Pedido enviado. Respondo-lhe eu, pelo meio que escolheu."', '"Request sent. I will reply myself, through the channel you chose."')
    page = fix_meta(page, slug); page = lang(page, slug, depth); page = missing_posts(page, depth)
    d = f'{OUT_EN}/{slug}' if slug else OUT_EN
    os.makedirs(d, exist_ok=True); open(d + '/index.html', 'w').write(page)

# ---- pages
write('', HOME)
for pg in P6.pages():
    h = re.sub(r'<title>.*?(?=<link rel="preconnect")', lambda _: meta(pg), head_sub, count=1, flags=re.S)
    write(pg['slug'], fill(links(h + pg['raw'] + tail, True, pg['slug'])))
for pg in [P.page_auto(chip), P.page_star(), P.page_rag(), P2.page_web(), P2.page_shop(), P2.page_geo(), P2.page_rev(), P3.page_sobre(), P3.page_contacto(), P3.page_metodo()] + P4.pages() + P5.pages() + P7.pages():
    h = re.sub(r'<title>.*?(?=<link rel="preconnect")', lambda _: meta(pg), head_sub, count=1, flags=re.S)
    cf = CF.replace('<div class="sform" id="cf">', f'<div class="sform" id="cf" data-pre="{pg["pre"]}">')
    if pg['contact']:
      t1, t2 = pg['contact']
      cf = cf.replace(OLD_LT, f'<span class="mono" style="color:var(--ac)">Começar</span><h2>{t1}</h2><p>{t2}</p>')
    if pg['foot']:
      f1, f2, f3 = pg['foot']
      cf = cf.replace(OLD_FT, f'<h2 data-split="1">{f1}</h2><button type="button" data-open data-pre="{f3}" class="pill ol ft-cta">{f2}</button>')
    page = h + NAV + '<main id="top" class="subp">\n' + pg['body'] + '\n' + cf + '</main>' + MODAL + tail
    write(pg['slug'], fill(links(page, True, pg['slug'])))
json.dump(sorted(miss), open('/home/claude/site-nova/en/miss.json', 'w'), ensure_ascii=False, indent=0)
print('miss', len(miss))
