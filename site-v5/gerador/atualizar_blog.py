"""Atualiza o blog estático (site v5) a partir de content/blog/*.md, sem regenerar o site todo.

Uso (na raiz do repositório):  python3 site-v5/gerador/atualizar_blog.py
Requer: pip install pyyaml markdown

- Cria a página estática de cada artigo novo (PT e EN), a partir do modelo de um artigo existente.
- Atualiza a lista do blog, os destaques e os "Artigos relacionados" de todos os artigos.
- Liga a versão PT à EN (hreflang e seletor de língua) quando o artigo tem tradução.
- Acrescenta os endereços novos a site-v5/paginas.json.
O resto do site (página inicial, animações, CSS, JS) não é tocado.
"""
import re, json, os, sys, html as H, datetime, importlib, copy
G=os.path.dirname(os.path.abspath(__file__))
REPO=os.path.abspath(os.path.join(G,'..','..')); PUB=REPO+'/public'
sys.path.insert(0,G+'/pt'); sys.path.insert(0,G+'/en')
os.chdir(G+'/pt')
import tok
import pages5 as P5
P5.SRC=REPO+'/content/blog'; P5.POSTS=P5.ler(); P5.SLUGS={p['slug'] for p in P5.POSTS}
U='https://starmountainflash.pt'
PT_POSTS=copy.deepcopy(P5.POSTS)
def prodify(g):
    g=re.sub(r'%%L:([a-z\-/]+)%%', r'/\1', g).replace('%%HOME%%','/')
    g=re.sub(r'((?:data-)?href=")https://starmountainflash\.pt(?=[/"?#])/?', r'\1/', g)
    return g
def region(s):
    i=s.find('<section id="hero"'); j=s.find('</section>', s.find('Artigos relacionados.' if 'Artigos relacionados.' in s else 'Related articles.'))+10
    return i,j
def region_blog(s):
    i=s.find('<section id="hero"'); j=s.find('</section>', s.find('id="artigos"'))+10
    return i,j
# EN dictionary
S=json.load(open(G+'/en/src.json')); D={}
for f in ['tr1.txt','tr2.txt','tr3.txt','tr4.txt']:
    for l in open(G+'/en/'+f,encoding='utf8'):
        l=l.rstrip('\n')
        if '|' not in l: continue
        i,e=l.split('|',1); D[S[int(i)]]=e
for l in open(G+'/en/extra.txt',encoding='utf8'):
    l=l.rstrip('\n')
    if ' ⇒ ' in l: a,b=l.split(' ⇒ ',1); D[a]=b
def en_mode():
    EN_MESES=['January','February','March','April','May','June','July','August','September','October','November','December']
    P5.data_pt=lambda d: f'{d.day} {EN_MESES[d.month-1]} {d.year}'
    P5.SRC=REPO+'/content/blog/en'
    P5.POSTS=P5.ler()
    for p in P5.POSTS: p['md']=p['md'].replace('](/en/','](/')
    P5.SLUGS={p['slug'] for p in P5.POSTS}
    P5.tu=lambda p: False
def en_fix(g, miss):
    g=tok.translate(g,D,miss)
    g=re.sub(r'(\d+) min de leitura', r'\1 min read', g).replace('<span>Atualizado a ','<span>Updated ')
    g=prodify(g)
    # EN links: internal -> /en/
    return g

def en_links(g):
    g=g.replace('href="https://starmountainflash.pt/en/','href="/en/')
    def rep(m):
        p=m.group(1)
        if p.startswith(('en/','en"','assets','img','#')) or p=='en': return m.group(0)
        return f'href="/en/{p}"' if p else 'href="/en"'
    g=re.sub(r'href="/([^"]*)"', lambda m: rep(m) if not m.group(1).startswith('en') else m.group(0), g)
    return g.replace('href="/en/"','href="/en"')

def jsonld_update(s, tp, np, lang):
    m=re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    g=json.loads(m.group(1))
    pre=U+('/en' if lang=='en' else '')
    title=(np['seo'] or np['titulo'])+' · Starmountain Flash'
    for n in g['@graph']:
        t=n['@type']
        if t=='BlogPosting':
            n['headline']=np['titulo']; n['description']=np['desc']; n['datePublished']=str(np['data'])
            if np['atualizado']: n['dateModified']=str(np['atualizado'])
            else: n.pop('dateModified',None)
            n['articleSection']=np['cat']
        elif t=='WebPage':
            n['name']=title; n['description']=np['desc']
        elif t=='BreadcrumbList':
            n['itemListElement'][-1]['name']=np['titulo']
        elif t=='FAQPage':
            n['mainEntity']=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in np['faq']]
    txt=json.dumps(g, ensure_ascii=False).replace(tp['slug'], np['slug'])
    return s[:m.start(1)]+txt+s[m.end(1):]

def new_page(tmpl_html, tp, np, body, lang):
    i,j=region(tmpl_html)
    a,b=tmpl_html[:i], tmpl_html[j:]
    a=jsonld_update(a,tp,np,lang)
    title=H.escape((np['seo'] or np['titulo'])+' · Starmountain Flash', quote=False)
    a=re.sub(r'<title>.*?</title>', lambda _: f'<title>{title}</title>', a, count=1)
    a=re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1)+H.escape((np['seo'] or np['titulo'])+' · Starmountain Flash')+m.group(2), a, count=1)
    a=re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*(")', lambda m: m.group(1)+H.escape(np['desc'])+m.group(2), a)
    a=a.replace(tp['slug'], np['slug']); b=b.replace(tp['slug'], np['slug'])
    return a+body+b

import os
report=[]
def write(path, new):
    old=open(path).read() if os.path.exists(path) else None
    if old!=new:
        os.makedirs(os.path.dirname(path),exist_ok=True); open(path,'w').write(new); report.append(path.replace(PUB,''))
def run(lang, posts, tmpl_slug):
    base=PUB+('/en' if lang=='en' else '')
    fx=(lambda g: en_links(en_fix(g,set()))) if lang=='en' else prodify
    tp=[p for p in posts if p['slug']==tmpl_slug][0]
    tmpl=open(f'{base}/blog/{tmpl_slug}/index.html').read()
    for p in posts:
        body=fx(P5.page_post(p)['body'])
        f=f'{base}/blog/{p["slug"]}/index.html'
        if os.path.exists(f):
            s=open(f).read(); i,j=region(s); write(f, s[:i]+body+s[j:])
        else:
            write(f, new_page(tmpl,tp,p,body,lang))
    f=f'{base}/blog/index.html'; s=open(f).read(); i,j=region_blog(s)
    write(f, s[:i]+fx(P5.page_blog()['body'])+s[j:])
run('pt', P5.POSTS, 'o-que-automatizar-primeiro-pme')
en_mode()
run('en', P5.POSTS, 'o-que-automatizar-primeiro-pme')

# ---- ligações PT <-> EN e paginas.json
EN_SET={p['slug'] for p in P5.POSTS}
for slug in EN_SET:
    f=f'{PUB}/blog/{slug}/index.html'
    if not os.path.exists(f): continue
    s=open(f).read(); sl='blog/'+slug
    a=f'<link rel="alternate" hreflang="pt-PT" href="{U}/{sl}">'
    if 'hreflang="en"' not in s and a in s:
        s=s.replace(a, a+f'<link rel="alternate" hreflang="en" href="{U}/en/{sl}">')
        s=s.replace('<a href="/en/blog" title="English">',f'<a href="/en/{sl}" title="English">').replace('<a href="/en/blog"><svg viewBox="0 0 60 30">',f'<a href="/en/{sl}"><svg viewBox="0 0 60 30">')
        write(f,s)
pj=os.path.join(REPO,'site-v5','paginas.json'); L=json.load(open(pj))
for p in PT_POSTS: L.append('blog/'+p['slug'])
for s_ in EN_SET: L.append('en/blog/'+s_)
L=sorted(set(L)); new='[\n'+',\n'.join(json.dumps(x) for x in L)+'\n]'
if open(pj).read()!=new: open(pj,'w').write(new); report.append('site-v5/paginas.json')
print('Ficheiros alterados:', len(report)); print('\n'.join(report))
