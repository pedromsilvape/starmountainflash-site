# Blog: lista e artigos. Conteúdo de content/blog/*.md do site atual.
import os, re, math, html as H, yaml, markdown
from pages import hero, sh, faq_sec, U

SRC = '/home/claude/repo/starmountainflash-site/content/blog'
MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
DESTAQUES = ['quanto-custa-um-site-pme-portugal', 'quanto-custa-automacao-ia-empresa', 'o-que-automatizar-primeiro-pme']
CATS = ['Websites', 'Lojas online', 'Automação', 'SEO e IA']

def data_pt(d): return f'{d.day} de {MESES[d.month - 1]} de {d.year}'

def ler():
    out = []
    for f in sorted(os.listdir(SRC)):
        if not f.endswith('.md'): continue
        raw = open(os.path.join(SRC, f), encoding='utf8').read()
        m = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.S)
        fm, md = yaml.safe_load(m.group(1)), m.group(2)
        if fm.get('estado') != 'publicado' or not fm.get('titulo'): continue
        import datetime
        d = fm['data'] if isinstance(fm['data'], datetime.date) else datetime.date.fromisoformat(str(fm['data']))
        a = fm.get('atualizado'); a = a if isinstance(a, datetime.date) else (datetime.date.fromisoformat(str(a)) if a else None)
        out.append(dict(slug=fm.get('slug') or f[:-3], titulo=fm['titulo'], desc=str(fm.get('descricao', ''))[:155], cat=fm.get('categoria') if fm.get('categoria') in CATS else 'Websites',
                        data=d, atualizado=a, seo=fm.get('tituloSeo'), cta=fm.get('cta') or None, faq=[(x['pergunta'], x['resposta']) for x in (fm.get('faq') or []) if x.get('pergunta') and x.get('resposta')], md=md))
    return sorted(out, key=lambda p: p['data'], reverse=True)

POSTS = ler()
SLUGS = {p['slug'] for p in POSTS}
LOCAL = {'automacoes', 'starmap', 'assistente-interno', 'websites', 'lojas-online', 'visibilidade-ia', 'avaliacoes-google', 'sobre', 'contacto', 'metodo', 'blog'}

def fix_links(h):
    def rep(m):
        path = m.group(1).strip('/')
        base, _, frag = path.partition('#')
        if base.startswith('blog/') and base[5:] in SLUGS or base in LOCAL:
            return f'href="%%L:{base}%%{("#" + frag) if frag else ""}"'
        return f'href="{U}/{path}"'
    h = re.sub(r'href="/([^"]*)"', rep, h)
    return re.sub(r'<a href="(https?://(?!starmountainflash)[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', h)

def tu(p):
    t = ' ' + p['titulo'] + ' ' + p['md'] + ' '
    a = len(re.findall(r'\b(teu|tua|teus|tuas|tens|podes|queres|fazes|precisas)\b', t, re.I))
    b = len(re.findall(r'\b(seu|sua|seus|suas|você|pode|quer|precisa)\b', t, re.I))
    return a > b / 2

def cta_tipo(p):
    if p['cta'] in ('analise', 'proposta', 'automacao', 'avaliacoes'): return p['cta']
    return {'Automação': 'automacao', 'Lojas online': 'proposta'}.get(p['cat'], 'analise')

def cta(p, onde):
    T = tu(p); s = lambda v, t: t if T else v
    k = cta_tipo(p)
    D = {'analise': ('Análise gratuita', s('Quer saber o que está a travar o seu site?', 'Queres saber o que está a travar o teu site?'),
                     s('Envie o link e receba por email, em até 3 dias úteis, um relatório com o que está a afastar clientes e o que corrigir primeiro. Sem custo e sem compromisso.', 'Envia o link e recebes por email, em até 3 dias úteis, um relatório com o que está a afastar clientes e o que corrigir primeiro. Sem custo e sem compromisso.'),
                     'Pedir a análise do meu site', f'href="{U}/analise-gratuita?de=blog-{p["slug"]}"', s('Comece pela análise gratuita ao seu site.', 'Começa pela análise gratuita ao teu site.')),
         'proposta': ('Proposta visual gratuita', s('Veja como o seu site pode ficar, antes de decidir.', 'Vê como o teu site pode ficar, antes de decidires.'),
                      s('Preparo uma proposta visual gratuita com base no seu negócio. O orçamento só vem depois, se gostar e quiser avançar.', 'Preparo uma proposta visual gratuita com base no teu negócio. O orçamento só vem depois, se gostares e quiseres avançar.'),
                      'Pedir proposta visual', 'data-open data-pre="Website"', s('Quer saber quanto custaria o seu site?', 'Queres saber quanto custaria o teu site?')),
         'automacao': ('Automações', s('Que tarefa gostava de nunca mais fazer à mão?', 'Que tarefa gostavas de nunca mais fazer à mão?'),
                       s('Diga-me qual é a tarefa que mais tempo ocupa na sua empresa. Respondo eu, com o que faz sentido automatizar e o que não vale a pena. A primeira resposta é gratuita.', 'Diz-me qual é a tarefa que mais tempo ocupa na tua empresa. Respondo eu, com o que faz sentido automatizar e o que não vale a pena. A primeira resposta é gratuita.'),
                       'Falar sobre uma tarefa', 'data-open data-pre="Automações à medida"', s('Por onde começar a automatizar na sua empresa?', 'Por onde começar a automatizar na tua empresa?')),
         'avaliacoes': ('Avaliações Google', s('Quer mais avaliações no Google, sem pedir uma a uma?', 'Queres mais avaliações no Google, sem pedir uma a uma?'),
                        s('A análise ao seu perfil Google é gratuita. Vejo o que pode melhorar e como pôr o pedido de avaliação a sair sozinho depois de cada serviço.', 'A análise ao teu perfil Google é gratuita. Vejo o que pode melhorar e como pôr o pedido de avaliação a sair sozinho depois de cada serviço.'),
                        'Pedir análise ao perfil', 'href="%%L:avaliacoes-google%%"', s('Comece pela análise gratuita ao seu perfil Google.', 'Começa pela análise gratuita ao teu perfil Google.'))}[k]
    et, tit, txt, bt, act, tfim = D
    if onde == 'fim': tit = tfim
    tag = 'button type="button"' if act.startswith('data-open') else 'a'
    end = 'button' if tag.startswith('button') else 'a'
    return f'<aside class="bcta {onde}"><span class="ey">{et}</span><p class="t">{tit}</p><p class="p">{txt}</p><{tag} class="pill {"w" if onde == "meio" else "d"}" {act}>{bt} ↗</{end}></aside>'

def render(md):
    m = markdown.Markdown(extensions=['tables', 'fenced_code', 'sane_lists', 'toc'], extension_configs={'toc': {'slugify': lambda v, s: re.sub(r'[^\w\- ]', '', v.lower(), flags=re.U).strip().replace(' ', '-')}})
    h = m.convert(md)
    toc = [(t['id'], t['name']) for t in m.toc_tokens]
    return h, toc

def minutos(md): return max(1, math.ceil(len(re.findall(r'\w+', md)) / 200))

def card(p, cls='bc'):
    return f'<a class="{cls}" href="%%L:blog/{p["slug"]}%%" data-cat="{p["cat"]}"><span class="cat">{p["cat"]}</span><h3>{p["titulo"]}</h3><p>{p["desc"]}</p><span class="d">{data_pt(p["data"])}</span></a>'

def page_blog():
    dest = [p for s in DESTAQUES for p in POSTS if p['slug'] == s][:3]
    VIS = ('<div class="hud" id="vis-blog"><div class="hh"><span>Comece por aqui</span><span class="live">' + str(len(POSTS)) + ' artigos</span></div><div class="bl3">'
           + ''.join(f'<a href="%%L:blog/{p["slug"]}%%"><small>{p["cat"]}</small><b>{p["titulo"]}</b><span>↗</span></a>' for p in dest) + '</div></div>')
    cats = [c for c in CATS if any(p['cat'] == c for p in POSTS)]
    filt = '<div class="flt" data-filter><button type="button" class="on" data-f="*">Todos</button>' + ''.join(f'<button type="button" data-f="{c}">{c}</button>' for c in cats) + '</div>'
    grid = '<div class="bgrid2">' + ''.join(card(p) for p in POSTS) + '</div>'
    return dict(slug='blog', crumb='Blog', pre='', kind='blog', posts=POSTS,
                title='Blog | Starmountain Flash', desc='Artigos práticos sobre websites, SEO, GEO e automação para empresas portuguesas.', faq=[],
                body=hero('Blog', 'Notas sobre sites e automação,<br>para quem gere uma PME.', 'Artigos práticos sobre websites, SEO, motores de IA e automação, sem jargão.',
                          'Proposta gratuita', '', '#artigos', 'Ver todos os artigos', 'Blog', VIS, mid=False)
                + f'<section class="sec" id="artigos">{sh("Artigos", "Todos os artigos.<br>Filtre por tema.", "Artigos curtos e práticos, escritos para quem gere uma PME e não tem tempo a perder.")}{filt}{grid}<nav class="pgn" aria-label="Páginas do blog"></nav></section>',
                contact=None, foot=None)

def page_post(p):
    h, toc = render(p['md'])
    h = fix_links(h)
    # mid CTA before the 3rd h2
    pos = [m.start() for m in re.finditer(r'<h2[\s>]', h)]
    if len(pos) >= 3: h = h[:pos[2]] + cta(p, 'meio') + h[pos[2]:]
    else: h += cta(p, 'meio')
    tocv = [(i, n) for i, n in toc]
    if len(toc) == 1 and False: pass
    toks = []
    for t in toc: toks.append(t)
    toch = ''.join(f'<a href="#{i}">{H.escape(n)}</a>' for i, n in toks)
    meta = f'<span>{data_pt(p["data"])}</span>' + (f'<span>Atualizado a {data_pt(p["atualizado"])}</span>' if p['atualizado'] else '') + f'<span>{minutos(p["md"])} min de leitura</span>'
    VIS = (f'<div class="hud" id="vis-toc"><div class="hh"><span>Neste artigo</span><span class="live">{minutos(p["md"])} min</span></div><nav class="tc2">{toch}</nav></div>' if len(toks) >= 3 else
           f'<div class="hud" id="vis-toc"><div class="hh"><span>Resumo</span><span class="live">{minutos(p["md"])} min</span></div><p class="sm2">{p["desc"]}</p></div>')
    rel = [x for x in POSTS if x['slug'] != p['slug'] and x['cat'] == p['cat']] + [x for x in POSTS if x['slug'] != p['slug'] and x['cat'] != p['cat']]
    body = hero(p['cat'], H.escape(p['titulo']), p['desc'], 'Proposta gratuita', '', '#artigo', 'Ler o artigo', 'Blog', VIS, mid=False, cls='sub art')
    body = body.replace('<span>Blog</span></nav>', f'<a href="%%L:blog%%">Blog</a><i>/</i><span>{H.escape(p["titulo"][:48] + ("…" if len(p["titulo"]) > 48 else ""))}</span></nav>')
    body = body.replace('<p class="lead" data-hi>', f'<div class="pmeta" data-hi>{meta}</div><p class="lead" data-hi>', 1)
    body += f'<section class="sec" id="artigo"><article class="prose">{h}{cta(p, "fim")}</article></section>'
    if p['faq']: body += faq_sec('Perguntas frequentes', 'Sobre este<br>tema.', p['faq'])
    body += f'<section class="sec tight">{sh("Continuar a ler", "Artigos relacionados.")}<div class="bgrid2">' + ''.join(card(x) for x in rel[:3]) + '</div></section>'
    return dict(slug='blog/' + p['slug'], crumb=p['titulo'], pre='', kind='post', post=p,
                title=(p['seo'] or p['titulo']) + ' · Starmountain Flash', desc=p['desc'], faq=p['faq'], body=body, contact=None, foot=None)

def pages(): return [page_blog()] + [page_post(p) for p in POSTS]
