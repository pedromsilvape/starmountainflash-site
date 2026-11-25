"""Gera a versão de produção do site v5 a partir de pub6/ para public/ do repositório.

- imagens base64 -> ficheiros em /assets/v5/img/
- CSS e JS inline -> ficheiros com hash em /assets/v5/
- fontes Geist alojadas no próprio site (sem Google Fonts)
- ligações relativas -> URLs limpos (/sobre, /en/sobre, /)
- consentimento, medição e envio de formulários (site.js) + Plausible
"""
import os, re, sys, hashlib, base64, shutil, posixpath, json

SRC = '/home/claude/site-nova/pub6'
REPO = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/starmountainflash-site'
PUB = REPO + '/public'
AS = PUB + '/assets/v5'
U = 'https://starmountainflash.pt'
FONTS = '/tmp/fonts/node_modules/@fontsource'

if os.path.isdir(AS): shutil.rmtree(AS)
os.makedirs(AS + '/img'); os.makedirs(AS + '/fonts')

def h(b): return hashlib.sha256(b).hexdigest()[:12]
def put(sub, ext, data):
    if isinstance(data, str): data = data.encode()
    name = f'{h(data)}.{ext}'
    p = f'{AS}/{sub}/{name}' if sub else f'{AS}/{name}'
    if not os.path.exists(p): open(p, 'wb').write(data)
    return f'/assets/v5/{sub + "/" if sub else ""}{name}'

# ---------- fontes
ff = []
PRELOAD = []
for fam, pkg, ws in [('Geist', 'geist', (300, 400, 500, 600)), ('Geist Mono', 'geist-mono', (400, 500))]:
    for w in ws:
        for sub, rng in [('latin-ext', 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF'),
                         ('latin', 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD')]:
            src = f'{FONTS}/{pkg}/files/{pkg}-{sub}-{w}-normal.woff2'
            url = put('fonts', 'woff2', open(src, 'rb').read())
            if sub == 'latin' and (fam, w) in (('Geist', 300), ('Geist', 400), ('Geist Mono', 400)): PRELOAD.append(url)
            ff.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url({url}) format('woff2');unicode-range:{rng}}}")
FONTCSS = ''.join(ff)

SITEJS = put('', 'js', open('/home/claude/site-nova/v5/site.js').read())
SCENES = put('', 'js', open('/home/claude/site-nova/v5/scenes.bundle.js').read())
PLAUS = ('<script async src="https://plausible.io/js/pa-2lRVurfYSTx4d-6iro9y0.js"></script>'
         '<script>window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};plausible.init()</script>')

pages = []
for d, _, fs in os.walk(SRC):
    if 'index.html' in fs:
        rel = os.path.relpath(d, SRC); pages.append('' if rel == '.' else rel)
pages = [p for p in pages if p not in ('404', 'en/404')]
pages.sort()
SET = set(pages)

def url_of(slug): return '/' if not slug else '/' + slug

def clean(path):
    # /x/index.html -> /x ; /index.html -> /
    path = re.sub(r'/index\.html$', '', path) or '/'
    return path

def resolve(slug, v):
    if re.match(r'^(https?:|mailto:|tel:|data:|javascript:|#|/)', v): return v
    base = '/' + (slug + '/' if slug else '')
    m = re.match(r'^([^#?]*)([?#].*)?$', v)
    p, q = m.group(1), m.group(2) or ''
    if not p: return v
    full = posixpath.normpath(posixpath.join(base, p))
    if p.endswith('/'): full += '/'
    return clean(full) + q

stats = {'img': 0}
from PIL import Image
import io as _io
def slim(raw, ext):
    # imagens grandes: largura máx. 1600 px, WebP q80
    if ext in ('svg', 'gif') or len(raw) < 90_000: return raw, ext
    im = Image.open(_io.BytesIO(raw)); im.load()
    if im.width > 1600: im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
    if im.mode not in ('RGB', 'RGBA'): im = im.convert('RGBA' if 'A' in im.getbands() else 'RGB')
    b = _io.BytesIO(); im.save(b, 'WEBP', quality=80, method=6); out = b.getvalue()
    return (out, 'webp') if len(out) < len(raw) else (raw, ext)
def b64repl(m):
    mime, data = m.group(1), m.group(2)
    ext = {'image/webp': 'webp', 'image/png': 'png', 'image/jpeg': 'jpg', 'image/svg+xml': 'svg', 'image/gif': 'gif'}[mime]
    stats['img'] += 1
    raw, ext = slim(base64.b64decode(data), ext)
    return put('img', ext, raw)

missing_en = [s for s in pages if not s.startswith('en') and s and ('en/' + s) not in SET]
print('PT sem EN:', missing_en)

for slug in pages:
    t = open(f'{SRC}/{slug}/index.html' if slug else f'{SRC}/index.html').read()
    en = slug == 'en' or slug.startswith('en/')
    # imagens
    t = re.sub(r'data:(image/(?:webp|png|jpeg|svg\+xml|gif));base64,([A-Za-z0-9+/=]+)', b64repl, t)
    # fontes Google -> próprias
    t = re.sub(r'<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"[^>]*>\s*', '', t)
    t = re.sub(r'<link href="https://fonts\.googleapis\.com/css2[^"]*" rel="stylesheet">', '', t)
    # CSS
    def css(m):
        body = m.group(1)
        if len(body) < 20000: return m.group(0)
        return f'<link rel="stylesheet" href="{put("", "css", FONTCSS + body)}">'
    t = re.sub(r'<style>(.*?)</style>', css, t, flags=re.S)
    pre = ''.join(f'<link rel="preload" href="{u}" as="font" type="font/woff2" crossorigin>' for u in PRELOAD)
    t = t.replace('</head>', pre + PLAUS + f'<script src="{SITEJS}" defer></script></head>', 1)
    # JS grande inline
    def js(m):
        body = m.group(1)
        if len(body) < 100000: return m.group(0)
        return f'<script src="{put("", "js", body)}" defer></script>'
    t = re.sub(r'<script>(.*?)</script>', js, t, flags=re.S)
    # imagens: carregamento preguiçoso
    # (as imagens do hero, visíveis ao abrir, carregam logo)
    hi = t.find('</section>', t.find('id="hero"')) if 'id="hero"' in t else 0
    t = re.sub(r'<img(?![^>]*\sloading=)(?![^>]*class="on")', '<img loading="lazy" decoding="async"', t[:hi]) + re.sub(r'<img(?![^>]*\sloading=)', '<img loading="lazy" decoding="async"', t[hi:])
    # ligações
    t = re.sub(r'(\s(?:href|data-href))="([^"]*)"', lambda m: f'{m.group(1)}="{resolve(slug, m.group(2))}"', t)
    # ligações absolutas internas nos <a> -> caminho
    t = re.sub(r'(<a\b[^>]*\shref=")' + re.escape(U) + r'(/[^"]*)?"', lambda m: m.group(1) + (m.group(2) or '/') + '"', t)
    t = re.sub(r'(data-href=")' + re.escape(U) + r'(/[^"]*)"', r'\1\2"', t)
    # PT sem versão EN
    if slug in missing_en:
        t = re.sub(r'<link rel="alternate" hreflang="en"[^>]*>', '', t)
        t = t.replace(f'href="/en/{slug}"', 'href="/en/blog"' if slug.startswith('blog/') else 'href="/en"')
    for s in missing_en:
        t = t.replace(f'href="/en/{s}"', f'href="/{s}" hreflang="pt"')
    t = t.replace('__SF_SCENES__', SCENES)
    assert 'base64,' not in t, slug
    assert '__SF_SCENES__' not in t, slug
    out = f'{PUB}/inicio/index.html' if not slug else f'{PUB}/{slug}/index.html'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(t)
    print(f'{url_of(slug):55s} {len(t)//1024:5d} KB')

json.dump(pages, open('/home/claude/site-nova/prod-pages.json', 'w'))
tot = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(AS) for f in fs)
print('imagens substituídas', stats['img'], '| assets', tot // 1024, 'KB')
