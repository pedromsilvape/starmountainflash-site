import re, json, os, html as H
src = open('build.py').read().split("head=open('head.html')")[0]
exec(src)  # logo, b64, ARR, icons, M1, M2, lines, C, CBG ...
import pages as P
import pages2 as P2
import pages3 as P3
import pages4 as P4
import pages5 as P5
import pages6 as P6
import pages7 as P7

U = 'https://starmountainflash.pt'
OUT = '/home/claude/site-nova/pub6'
SUBS = ['trabalhos', 'automacoes', 'starmap', 'assistente-interno', 'websites', 'lojas-online', 'visibilidade-ia', 'avaliacoes-google', 'sobre', 'contacto', 'metodo', 'trabalhos/ubi', 'trabalhos/planet-trading', 'trabalhos/studyos', 'trabalhos/beatriz-nunes', 'blog', 'analise-gratuita', 'analise-gratuita/obrigado', 'privacidade', 'cookies', 'termos', 'aviso-legal', '404'] + ['blog/' + p['slug'] for p in P5.POSTS]
head = open('head.html').read(); body = open('body.html').read(); tail = open('tail.html').read()
subcss = open('sub.css').read()
head = head.replace('</style></head>', subcss + '\n</style></head>')
head = head.replace('<title>Starmountain Flash · Automações com IA para PME</title>', '<title>Starmountain Flash · Websites e automações com IA para empresas</title>')

rep = {'%%LOGO_DARK%%': logo('logotipo-uma-cor-noite.svg'), '%%LOGO_W%%': logo('logotipo-uma-cor-branco.svg'), '%%ARR%%': ARR, '%%BOLT%%': BOLT, '%%GLOBE%%': GLOBE, '%%STAR%%': STAR, '%%PTR%%': PTR,
       '%%M1%%': M1, '%%M2%%': M2, '%%LINES%%': lines, '%%CARDS%%': C, '%%CBG%%': CBG, '%%TP%%': ico('siTrustpilot', True), '%%GG%%': ico('siGoogle', True),
       '%%LOGO_W_SM%%': logo('logotipo-uma-cor-branco.svg'), '%%PEDRO%%': b64(IMG + 'pedro-pereira.jpg', 'image/jpeg'), '%%BUNDLE%%': open('bundle.js').read()}

def fill(t):
    t = re.sub(r'%%ASSET:([\w\-\.]+)%%', lambda m: b64('/home/claude/repo/starmountainflash-site/public/assets/site/' + m.group(1), 'image/webp'), t)
    t = re.sub(r'%%IMG:([\w\-\.]+)%%', lambda m: b64(IMG + 'trabalhos/' + m.group(1), 'image/webp'), t)
    for k, v in rep.items(): t = t.replace(k, v)
    left = re.findall(r'%%[A-Z0-9_:\-a-z]+%%', t.split('<script>')[0])
    assert not left, left
    return t

def absmeta(t, slug):
    url = f'{U}/{slug}'
    t = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', t, count=1)
    t = re.sub(r'<link rel="alternate" hreflang="pt-PT"[^>]*><link rel="alternate" hreflang="en"[^>]*><link rel="alternate" hreflang="x-default"[^>]*>',
               f'<link rel="alternate" hreflang="pt-PT" href="{url}"><link rel="alternate" hreflang="en" href="{U}/en/{slug}"><link rel="alternate" hreflang="x-default" href="{url}">', t, count=1)
    return re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', t, count=1)

def links(t, sub, slug=None):
    depth = slug.count('/') + 1 if (sub and slug) else 0
    pre = '../' * depth
    home = pre + 'index.html'
    for s in SUBS: t = t.replace(f'href="{U}/{s}"', f'href="{pre}{s}/index.html"')
    for s in SUBS: t = t.replace(f'data-href="{U}/{s}"', f'data-href="{pre}{s}/index.html"')
    for s in SUBS: t = t.replace(f'href="{U}/{s}?', f'href="{pre}{s}/index.html?')
    t = re.sub(r'%%L:([a-z\-/]+)%%', lambda m: f'{pre}{m.group(1)}/index.html', t)
    t = t.replace('%%HOME%%', home)
    if sub:
        t = t.replace('<a href="#top" class="shell brand">', f'<a href="{home}" class="shell brand">')
        for a in ['servicos', 'trabalhos', 'metodo', 'sobre']: t = t.replace(f'href="#{a}"', f'href="{home}#{a}"')
        t = t.replace('href="#top"', 'href="index.html"')
        t = t.replace(f'href="{U}/en"', f'href="{U}/en/{slug}"')
        t = t.replace(f'<a class="mr" href="{pre}{slug}/index.html">', f'<a class="mr cur" aria-current="page" href="{pre}{slug}/index.html">')
        t = absmeta(t, slug)
    return t

# ---------- home
cbg = '<script>document.querySelectorAll(".cbg img").forEach(function(im){im.src=document.querySelectorAll(".ccard img")[+im.dataset.i].src})</script>'
home = links(re.sub(r'<div id="pre">.*?</div></div></div>\n?', '', head, flags=re.S) + body + cbg + tail, False)  # sem preloader (PageSpeed)
os.makedirs(OUT, exist_ok=True)
open(f'{OUT}/index.html', 'w').write(links(fill(home), False))

# ---------- parts for subpages
i_main = body.index('<main id="top">'); i_cw = body.index('<div id="cwrap">'); i_end = body.index('</main>')
NAV, CF, MODAL = body[:i_main], body[i_cw:i_end], body[i_end + len('</main>'):]
OLD_LT = '<span class="mono" style="color:var(--ac)">Proposta gratuita</span><h2>Conte-me o que precisa.</h2><p>Leio e respondo eu, por email ou WhatsApp.</p>'
OLD_FT = '<h2 data-split="1">Veja antes de decidir.<br>Proposta visual gratuita.</h2><button type="button" data-open class="pill ol ft-cta">Pedir proposta</button>'
assert CF.count(OLD_LT) == 1 and CF.count(OLD_FT) == 1, (CF.count(OLD_LT), CF.count(OLD_FT))
head_sub = re.sub(r'<div id="pre">.*?</div></div></div>\n?', '', head, flags=re.S)
assert '<div id="pre">' not in head_sub

def meta(pg):
    url = f'{U}/{pg["slug"]}'
    kind = pg.get('kind', 'service')
    biz = {"@type": "ProfessionalService", "@id": U + "/#negocio", "name": "Starmountain Flash", "url": U, "email": "geral@starmountainflash.pt", "telephone": "+351937800553",
         "address": {"@type": "PostalAddress", "addressLocality": "Covilhã", "addressCountry": "PT"}, "founder": {"@id": U + "/sobre#pedro-pereira"}}
    if kind == 'contact':
        biz["contactPoint"] = {"@type": "ContactPoint", "contactType": "customer service", "email": "geral@starmountainflash.pt", "telephone": "+351937800553", "availableLanguage": ["pt-PT", "en"], "hoursAvailable": {"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "20:30"}}
    graph = [biz]
    about = U + "/#negocio"
    if 'service' in pg:
        sv = pg['service']
        service = {"@type": "Service", "@id": url + '#servico', "name": sv['name'], "serviceType": sv['type'], "description": pg['desc'], "url": url,
                   "provider": {"@id": U + "/#negocio"}, "areaServed": {"@type": "Country", "name": "Portugal"}, "inLanguage": "pt-PT"}
        if sv['offers']:
            service["offers"] = {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": sv['offers'][0], "description": "Valores de referência; o valor exato fica na proposta."}
        graph.append(service); about = url + '#servico'
    if kind == 'case':
        c = pg['case']
        graph.append({"@type": "CreativeWork", "@id": url + '#trabalho', "name": c['nome'], "description": c['desc'], "url": c['visitar'][0][1], "dateCreated": "2026",
                      "creator": {"@id": U + "/#negocio"}, "keywords": ", ".join(c['tecnologia'])})
        about = url + '#trabalho'
    if kind == 'works':
        graph.append({"@type": "ItemList", "@id": url + '#lista', "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": c['nome'], "url": U + "/trabalhos/" + c['slug']} for i, c in enumerate(pg['cases'])]})
        about = url + '#lista'
    if kind == 'blog':
        graph.append({"@type": "Blog", "@id": U + "/blog#blog", "name": "Blog da Starmountain Flash", "description": pg['desc'], "url": U + "/blog", "publisher": {"@id": U + "/#negocio"}, "inLanguage": "pt-PT",
                      "blogPost": [{"@type": "BlogPosting", "headline": p['titulo'], "url": U + "/blog/" + p['slug'], "datePublished": p['data'].isoformat()} for p in pg['posts']]})
        about = U + "/blog#blog"
    if kind == 'post':
        p = pg['post']
        bp = {"@type": "BlogPosting", "@id": url + '#artigo', "headline": p['titulo'], "description": p['desc'], "datePublished": p['data'].isoformat(), "inLanguage": "pt-PT",
              "author": {"@id": U + "/sobre#pedro-pereira"}, "publisher": {"@id": U + "/#negocio"}, "articleSection": p['cat'], "mainEntityOfPage": url, "isPartOf": {"@id": U + "/blog#blog"}}
        if p['atualizado']: bp["dateModified"] = p['atualizado'].isoformat()
        graph.append(bp); about = url + '#artigo'
    person = {"@type": "Person", "@id": U + "/sobre#pedro-pereira", "name": "Pedro Pereira", "url": U + "/sobre", "jobTitle": "Fundador", "worksFor": {"@id": U + "/#negocio"}}
    if kind == 'about':
        person.update({"homeLocation": {"@type": "Place", "name": "Covilhã, Portugal"}, "birthPlace": {"@type": "Place", "name": "Porto, Portugal"},
                       "award": "Medalha de reconhecimento nacional (missão internacional ao serviço da NATO)",
                       "knowsAbout": ["Criação de websites", "Lojas online", "SEO", "Generative Engine Optimization (GEO)", "Automações com IA"]})
        about = U + "/sobre#pedro-pereira"
    graph.append(person)
    ptype = {'about': 'AboutPage', 'contact': 'ContactPage', 'blog': 'CollectionPage', 'works': 'CollectionPage'}.get(kind, 'WebPage')
    graph.append({"@type": ptype, "@id": url, "url": url, "name": pg['title'], "description": pg['desc'], "inLanguage": "pt-PT", "isPartOf": {"@id": U + "/#site"}, "about": {"@id": about}, "breadcrumb": {"@id": url + '#breadcrumb'}})
    items = [("Início", U + "/")] + ([("Serviços", U + "/#servicos")] if kind == 'service' else [("Trabalhos", U + "/trabalhos")] if kind == 'case' else [("Blog", U + "/blog")] if kind == 'post' else []) + [(pg['crumb'], url)]
    graph.append({"@type": "BreadcrumbList", "@id": url + '#breadcrumb', "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": it} for i, (n, it) in enumerate(items)]})
    if pg['faq']:
        graph.append({"@type": "FAQPage", "@id": url + '#faq', "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": H.unescape(P.strip_tags(a))}} for q, a in pg['faq']]})
    g = {"@context": "https://schema.org", "@graph": graph}
    return f'''<title>{pg["title"]}</title>
<meta name="description" content="{pg["desc"]}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="pt-PT" href="{url}"><link rel="alternate" hreflang="en" href="{U}/en/{pg["slug"]}"><link rel="alternate" hreflang="x-default" href="{url}">
<meta name="robots" content="{"noindex, follow" if pg.get("noindex") else "index, follow, max-snippet:-1, max-image-preview:large"}">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/icon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_PT"><meta property="og:site_name" content="Starmountain Flash">
<meta property="og:title" content="{pg["title"]}"><meta property="og:description" content="{pg["desc"]}"><meta property="og:url" content="{url}"><meta property="og:image" content="{U}/img/og-starmountain-flash.jpg">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(g, ensure_ascii=False)}</script>
'''

def chip(name):
    m = {'Gmail e Outlook': 'siGmail', 'Excel e Google Sheets': 'siGooglesheets', 'HubSpot': 'siHubspot', 'Notion': 'siNotion', 'Trello': 'siTrello', 'Google Workspace': 'siGoogle', 'n8n e Make': 'siN8n', 'Brevo': 'siBrevo'}
    k = m.get(name)
    return ico(k, True) if k and k in IC else ''

for pg in P6.pages():
    h = re.sub(r'<title>.*?(?=<link rel="preconnect")', lambda _: meta(pg), head_sub, count=1, flags=re.S)
    page = links(h + pg['raw'] + tail, True, pg['slug'])
    os.makedirs(f'{OUT}/{pg["slug"]}', exist_ok=True)
    open(f'{OUT}/{pg["slug"]}/index.html', 'w').write(fill(page))
    print(pg['slug'], len(page))
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
    page = links(page, True, pg['slug'])
    os.makedirs(f'{OUT}/{pg["slug"]}', exist_ok=True)
    open(f'{OUT}/{pg["slug"]}/index.html', 'w').write(fill(page))
    print(pg['slug'], len(page))
print('done')
