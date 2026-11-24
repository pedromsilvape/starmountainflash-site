# Bloco Trabalhos: casos de estudo. Conteúdo de src/data/casos.ts do site atual.
import html as H
from pages import hero, sh, U

IMGP = '%%IMG:{}%%'
def im(f): return IMGP.format(f.split('/')[-1])

TESTEMUNHO_HP = ('Excelente experiência do início ao fim.', 'Todo o processo foi simples, rápido e profissional, desde o primeiro contacto até à conclusão do serviço.',
                 'https://www.trustpilot.com/reviews/6a2fde4eec482bf7be526d36')

CASOS = [
 dict(slug='ubi', nome='Universidade da Beira Interior', curto='UBI',
      desc='Três sites para três iniciativas da Universidade da Beira Interior: a Mostra UBI Equidade, o 3.º Seminário à Visibilidade LGBTQIA+ e o lançamento de um livro.',
      h1='Universidade da Beira Interior.', h1b='Três sites, três iniciativas.',
      intro='Três sites para três iniciativas da UBI, na Covilhã: a Mostra UBI Equidade, o 3.º Seminário Internacional Interdisciplinar à Visibilidade LGBTQIA+ e o lançamento de um livro sobre saúde ocupacional em populações LGBTQIA+.',
      ficha=[('Cliente', 'Universidade da Beira Interior'), ('Serviço', 'Websites de eventos e publicações'), ('Ano', '2026'), ('Sites', 'dei.ubi.pt · 3lgbt.ubi.pt · lgbthealth.ubi.pt')],
      desafio='Três iniciativas diferentes (um evento, um seminário internacional e o lançamento de um livro) precisavam cada uma de um site próprio, com identidade visual própria e data marcada, mas com o mesmo nível de qualidade.',
      solucao='Um site por iniciativa, cada um com a sua linguagem visual: contagem decrescente e título dinâmico na Mostra, identidade arco-íris e informação prática no Seminário, e uma página editorial com download gratuito do livro. Todos rápidos e pensados para telemóvel.',
      resultado='Três sites no ar e a Starmountain Flash como fornecedor digital da universidade.',
      mockupTopo='ubi-dei-mockup-completo.webp',
      shots=[('dei.ubi.pt', 'ubi-dei-desktop.webp', 'Mostra UBI Equidade'), ('3lgbt.ubi.pt', 'ubi-3lgbt-desktop.webp', '3.º Seminário LGBTQIA+'), ('lgbthealth.ubi.pt', 'ubi-lgbthealth-desktop.webp', 'Livro LGBTQIA+ Health')],
      tecnologia=['Desenvolvimento à medida', 'Design responsivo', 'SEO técnico'],
      visitar=[('Mostra UBI Equidade', 'https://dei.ubi.pt'), ('3.º Seminário LGBTQIA+', 'https://3lgbt.ubi.pt'), ('Livro LGBTQIA+ Health', 'https://lgbthealth.ubi.pt')],
      sites=[
        dict(id='dei', nome='Mostra UBI Equidade', dominio='dei.ubi.pt', href='https://dei.ubi.pt',
             descricao='Site do evento que reúne investigações em diversidade, equidade e inclusão desenvolvidas na UBI. 23 de outubro de 2026, 10h00–18h00, Biblioteca Central UBI, inscrição gratuita.',
             destaques=['Contagem decrescente até ao evento.', 'Título que alterna entre palavras (Equidade, Inclusão…), cada uma com a sua cor.'],
             estrutura=['Apresentação', 'Programa', 'Submissões', 'Local', 'Inscrição'],
             cores=[('Fundo', '#1A3A52'), ('Vermelho', '#EF4444'), ('Verde', '#22C55E'), ('Azul', '#3B82F6'), ('Texto', '#FFFFFF')],
             fontes=[('Space Grotesk', 'Títulos'), ('Inter', 'Texto corrido')],
             mockup='ubi-dei-mockup.webp', desktop='ubi-dei-desktop.webp', mobile='ubi-dei-mobile.webp'),
        dict(id='3lgbt', nome='3.º Seminário LGBTQIA+', dominio='3lgbt.ubi.pt', href='https://3lgbt.ubi.pt',
             descricao='Site do 3.º Seminário Internacional Interdisciplinar à Visibilidade LGBTQIA+. 22 de maio de 2026, Biblioteca Central UBI, exclusivamente presencial.',
             destaques=['Título e linha de navegação com gradiente arco-íris.', 'Informação essencial (local, data, formato) em destaque logo no topo.'],
             estrutura=['Comissões', 'Programa', 'Submissão e Publicações', 'Inscrições', 'Contacto', 'Local'],
             cores=[('Fundo', '#1A1A2F'), ('Azul', '#13294C'), ('Laranja', '#FF8C00'), ('Secções', '#FAFAFA'), ('Arco-íris', 'linear-gradient(90deg,#E40303,#FF8C00,#FFED00,#008026,#24408E,#732982)')],
             fontes=[('Montserrat', 'Títulos'), ('Open Sans', 'Texto corrido')],
             mockup='ubi-3lgbt-mockup.webp', desktop='ubi-3lgbt-desktop.webp', mobile='ubi-3lgbt-mobile.webp'),
        dict(id='lgbthealth', nome='Livro LGBTQIA+ Health', dominio='lgbthealth.ubi.pt', href='https://lgbthealth.ubi.pt',
             descricao='Página de lançamento do livro «Occupational Health, Psychosocial Risks and Prevention Factors in LGBTQIA+ Populations in Portugal», de Henrique Pereira e Iara Teixeira (junho de 2026), com download gratuito em PDF.',
             destaques=['Linguagem editorial com tipografia serifada.', 'Capa do livro em 3D como elemento principal.'],
             cores=[('Fundo', '#FDFBF7'), ('Texto', '#1B1B1B'), ('Roxo', '#7209B7'), ('Etiqueta', '#F5EDF3'), ('Gradiente', 'linear-gradient(90deg,#E74148,#EFB165)')],
             fontes=[('Cormorant Garamond', 'Títulos'), ('Manrope', 'Texto corrido')],
             mockup='ubi-lgbthealth-mockup.webp', desktop='ubi-lgbthealth-desktop.webp', mobile='ubi-lgbthealth-mobile.webp',
             testemunho=('Henrique Pereira', 'coautor do livro publicado em lgbthealth.ubi.pt'))]),
 dict(slug='planet-trading', nome='Planet Trading', curto='Planet Trading',
      desc='Landing page de página única para a comunidade Planet Trading, construída em 3D com WebGL e com o formulário ligado diretamente a um CRM.',
      h1='Planet Trading.', h1b='Uma landing page em 3D.',
      intro='Landing page de página única para a comunidade Planet Trading, construída em 3D com WebGL e com o formulário ligado diretamente a um CRM.',
      ficha=[('Cliente', 'Planet Trading'), ('Serviço', 'Landing page + integração CRM'), ('Ano', '2026'), ('Site', 'comunidadeplanet.pt')],
      desafio='Lançar a nova fase da comunidade, "New Era", com uma página que causasse impacto logo à primeira visita e que transformasse visitas em contactos organizados, prontos a seguir.',
      solucao='Uma página única construída em 3D com WebGL, com vídeos de fundo e animações, e um formulário que envia cada contacto diretamente para o CRM. Tudo desenvolvido em código, sem construtores.',
      resultado='Site público em comunidadeplanet.pt desde outubro de 2026, a servir de porta de entrada da nova fase da comunidade.',
      shots=[('comunidadeplanet.pt', 'planet-trading-desktop.webp', 'Planet Trading')],
      desktop='planet-trading-desktop.webp', mobile='planet-trading-mobile.webp',
      construcao=dict(titulo='Uma intro 3D em WebGL.', numeros=[('120 mil', 'partículas animadas em tempo real'), ('4', 'fases na intro, ao ritmo do scroll'), ('GLSL', 'shaders escritos à medida'), ('0', 'construtores visuais: tudo em código')],
          fases=[('Fase 01', 'Esfera', 'As partículas formam uma esfera que se desfaz.'), ('Fase 02', 'Onda', 'Espalham-se numa onda em movimento.'), ('Fase 03', 'Túnel', 'A onda curva-se num túnel em hiperespaço.'), ('Fase 04', 'Galáxia', 'Um clarão dá origem a uma galáxia em espiral.')],
          blocos=[('Render 3D', 'A intro é construída em WebGL com Three.js. As partículas são animadas por shaders GLSL escritos à medida, e o brilho vem de pós-processamento com Unreal Bloom. As cores mudam de frio para quente em função da distância ao centro da galáxia.', [], ['Three.js', 'WebGL', 'GLSL', 'Unreal Bloom']),
                  ('Scroll e animação', 'Toda a sequência depende da posição do scroll, por isso o deslize foi suavizado com Lenis, para o movimento ser contínuo em rato, trackpad e ecrã tátil.', ['Títulos de cada fase sincronizados com a animação', 'A intro corre uma só vez e dá lugar ao resto da página', 'Secções seguintes com entrada animada só quando ficam visíveis'], ['Lenis', 'Intersection Observer']),
                  ('Desempenho e acessibilidade', 'A partir da intro, a página é uma landing page em secções: resultados, como funciona, o que inclui, demonstração da plataforma, planos, equipa, testemunhos e FAQ.', ['Imagens abaixo da dobra com carregamento diferido', 'Vídeo da comunidade só arranca quando aparece no ecrã', 'Densidade de pixels do 3D limitada em ecrãs de alta resolução', 'Sem animações para quem tem o movimento reduzido ativo'], ['Lazy loading', 'prefers-reduced-motion'])]),
      tecnologia=['WebGL / 3D', 'Vídeo de fundo', 'Formulário ligado a CRM'],
      visitar=[('Visitar o site', 'https://comunidadeplanet.pt')]),
 dict(slug='studyos', nome='StudyOS', curto='StudyOS',
      desc='Plataforma de estudo por subscrição para uma comunidade de estudantes de Gestão da Universidade Aberta: materiais por cadeira, ferramentas de estudo e IA.',
      h1='StudyOS.', h1b='Uma plataforma de estudo por subscrição.',
      intro='O hub de estudo de uma comunidade de estudantes de Gestão da Universidade Aberta: materiais organizados por cadeira, ferramentas de estudo e uma IA que estuda com base nos materiais de cada aluno.',
      ficha=[('Cliente', 'Comunidade de estudantes de Gestão (Universidade Aberta)'), ('Serviço', 'Plataforma web + área de membros'), ('Ano', '2026'), ('Site', 'gestaocrew.pt')],
      desafio='Reunir num só lugar os materiais de estudo de uma comunidade de estudantes, organizados por cadeira, e dar-lhes ferramentas para estudar em grupo, com acesso por subscrição.',
      solucao='Uma página de subscrição simples e uma plataforma completa por trás: manuais, resumos e exames por cadeira, simulador de exame, flashcards com repetição espaçada, IA com base nos materiais do aluno, chat geral, eventos, calendário, sala de estudo com presença em tempo real, temporizador de foco, pesquisa rápida (Ctrl K), notificações, modo escuro e painel de administração. No telemóvel, navegação inferior própria, como uma app.',
      resultado='Plataforma em funcionamento, com 29 cadeiras e 166 documentos organizados, e subscrição mensal de 10 € sem fidelização, com pagamento por cartão, Apple Pay e Google Pay.',
      mockupTopo='studyos-landing-mockup.webp',
      shots=[('gestaocrew.pt', 'studyos-landing-desktop.webp', 'Página de subscrição'), ('gestaocrew.pt', 'studyos-app-desktop.webp', 'Área de membros')],
      desktop='studyos-landing-desktop.webp', mobile='studyos-landing-mobile.webp',
      extras=[dict(etiqueta='Por dentro da plataforma', titulo='A área de membros.', destaque='O que o aluno vê depois de entrar.', dominio='gestaocrew.pt', nome='Área de membros do StudyOS', mockup='studyos-app-mockup.webp', desktop='studyos-app-desktop.webp', mobile='studyos-app-mobile.webp')],
      estrutura=['Página de subscrição', 'Início', 'Cadeiras', 'Chat geral', 'Eventos', 'Calendário', 'Guia', 'Admin'],
      cores=[('Fundo', '#F1EFE9'), ('Índigo', '#6366F1'), ('Texto', '#15151A'), ('Barra lateral', '#131316'), ('Laranja', '#F97316'), ('Cartões', '#FFFFFF')],
      fontes=[('Plus Jakarta Sans', 'Texto e títulos'), ('Fraunces', 'Saudação e números no painel')],
      tecnologia=['Plataforma à medida', 'Área de membros', 'Subscrições com pagamentos online', 'IA integrada'],
      visitar=[('Visitar o site', 'https://gestaocrew.pt')]),
 dict(slug='beatriz-nunes', nome='Beatriz Nunes, Personal Trainer', curto='Beatriz Nunes',
      desc='Redesign do site da personal trainer Beatriz Nunes: mais impacto visual em cada secção, mantendo os textos e a identidade dela, e a parte técnica tratada.',
      h1='Beatriz Nunes.', h1b='O redesign de um site que já existia.',
      intro='A Beatriz criou o próprio site e pediu-me para o levar mais longe. Redesenhei cada secção sem mexer nos textos nem na identidade dela, e tratei da parte que não se vê.',
      ficha=[('Cliente', 'Beatriz Nunes, personal trainer'), ('Serviço', 'Redesign + parte técnica'), ('Ano', '2026'), ('Site', 'personaltrainerbeatriznunes.pt')],
      desafio='O site já tinha os textos e a identidade da Beatriz, mas as secções não tinham impacto, a navegação no telemóvel era limitada e os pedidos de treino não tinham um caminho direto até ela.',
      solucao='Um redesign secção a secção, com as cores e as letras que ela escolheu: abertura com foto em arco, painéis arredondados, cartões de resultados e galeria em faixa. Por trás, o formulário passou a enviar os pedidos para o email dela, o menu foi pensado para o telemóvel, o link mostra foto e descrição quando é partilhado no WhatsApp e a parte legal ficou tratada.',
      resultado='Site público em personaltrainerbeatriznunes.pt desde outubro de 2026, com domínio próprio e os pedidos de treino experimental a chegar diretamente ao email.',
      shots=[('personaltrainerbeatriznunes.pt', 'beatriz-nunes-desktop.webp', 'Depois do redesign'), ('personaltrainerbeatriznunes.pt', 'beatriz-nunes-antes-desktop.webp', 'Antes do redesign')],
      desktop='beatriz-nunes-desktop.webp',
      extras=[dict(etiqueta='Antes e depois', titulo='O ponto de partida.', destaque='O site que a Beatriz tinha feito.', descricao='Os textos, as fotos e as cores já eram dela. O redesign partiu daqui: a abertura passou a ter a foto em arco e as secções ganharam painéis, cartões e mais hierarquia.', dominio='personaltrainerbeatriznunes.pt', nome='Site da Beatriz Nunes antes do redesign', desktop='beatriz-nunes-antes-desktop.webp')],
      estrutura=['Sobre mim', 'Como funciona', 'Treinos', 'Resultados', 'Testemunhos', 'Dúvidas', 'Treino experimental'],
      tecnologia=['Formulário com pedidos por email', 'Navegação pensada para telemóvel', 'Pré-visualização ao partilhar o link', 'Privacidade, Livro de Reclamações e resolução de litígios'],
      visitar=[('Visitar o site', 'https://personaltrainerbeatriznunes.pt')]),
]

ARRU = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17 17 7M8 7h9v9"/></svg>'

def frame(dom, f, alt, cls='fr'):
    return f'<figure class="{cls}"><div class="bb"><span class="dots"><i></i><i></i><i></i></span><span class="u2">{dom}</span></div><img src="{im(f)}" alt="{H.escape(alt)}" loading="lazy"></figure>'

def phone(f, alt):
    return f'<figure class="pfr"><img src="{im(f)}" alt="{H.escape(alt)}" loading="lazy"></figure>'

def shots(dom, nome, desktop=None, mobile=None):
    if not desktop: return ''
    return f'<div class="shots{" one" if not mobile else ""}">{frame(dom, desktop, nome + " em computador")}{phone(mobile, nome + " em telemóvel") if mobile else ""}</div>'

def mock(f, alt):
    return f'<figure class="mk"><img src="{im(f)}" alt="{H.escape(alt)}" loading="lazy"></figure>' if f else ''

def swatches(cores):
    return '<div class="sws">' + ''.join(f'<div><span style="background:{v}"></span><b>{n}</b>{"<em>" + v + "</em>" if v.startswith("#") else ""}</div>' for n, v in cores) + '</div>'

def fonts(fs):
    return '<div class="fts">' + ''.join(f'<div><span class="aa">Aa</span><b>{n}</b><em>{p}</em></div>' for n, p in fs) + '</div>'

def chips(xs, cls='chips'):
    return f'<div class="{cls}">' + ''.join(f'<span>{x}</span>' for x in xs) + '</div>'

def quote(nome, legenda):
    t, q, link = TESTEMUNHO_HP
    ini = ''.join(w[0] for w in nome.split()[:2])
    return f'<div class="dq"><div><p class="qt">{t}</p><a href="{link}" target="_blank" rel="noopener">Ver a avaliação {ARRU}</a></div><div><blockquote>“{q}”</blockquote><div class="who"><i>{ini}</i><div><b>{nome}</b><span>{nome}, {legenda}</span></div></div></div></div>'

def vis(c):
    s = c['shots']
    cyc = ' data-cycle="3200"' if len(s) > 1 else ''
    return (f'<div class="hud" id="vis-web"{cyc}><div class="hh"><span>Caso de estudo</span><span class="live">no ar</span></div>'
            '<div class="br"><div class="bb"><span class="dots"><i></i><i></i><i></i></span><div class="url" data-g>' + ''.join(f'<span class="{"on" if i == 0 else ""}">{d}</span>' for i, (d, *_) in enumerate(s)) + '</div></div>'
            '<div class="shot" data-g>' + ''.join(f'<img class="{"on" if i == 0 else ""}" src="{im(f)}" alt="">' for i, (_, f, _n) in enumerate(s)) + '</div></div>'
            '<div class="cap" data-g>' + ''.join(f'<div class="{"on" if i == 0 else ""}"><b>{n}</b><small>{d}</small></div>' for i, (d, _f, n) in enumerate(s)) + '</div></div>')

def page_caso(c, nxt):
    ficha = '<dl class="cfi">' + ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in c['ficha']) + '</dl>'
    story = ('<div class="story" data-cards>'
             f'<div><span class="ey">O desafio</span><p>{c["desafio"]}</p></div>'
             f'<div><span class="ey">A solução</span><p>{c["solucao"]}</p></div>'
             f'<div class="res"><span class="ey">O resultado</span><p>{c["resultado"]}</p></div></div>')
    body = hero('Trabalhos · caso de estudo', f'{c["h1"]}<br>{c["h1b"]}', c['intro'], 'Proposta visual gratuita', 'Website',
                c['visitar'][0][1], c['visitar'][0][0] + ' ↗', c['curto'], vis(c), mid=('Trabalhos', '#trabalhos'))
    body = body.replace('href="%%HOME%%#trabalhos">Trabalhos', 'href="%%L:trabalhos%%">Trabalhos')
    body = body.replace(f'href="{c["visitar"][0][1]}" class="u"', f'href="{c["visitar"][0][1]}" class="u" target="_blank" rel="noopener"')
    body += f'<section class="sec">{ficha}{mock(c.get("mockupTopo"), c["nome"] + " em computador e telemóvel")}</section>'
    body += f'<section class="sec tight">{sh("01 · A história", "O desafio, a solução<br>e o resultado.")}{story}</section>'
    if c.get('desktop'):
        body += f'<section class="sec tight">{shots(c["ficha"][-1][1], c["nome"], c.get("desktop"), c.get("mobile"))}</section>'
    if c.get('sites'):
        for i, s in enumerate(c['sites']):
            dk = ' dk' if i % 2 == 0 else ''
            hd = (f'<div class="sh2"><div><span class="ey">Site {i + 1:02d}</span><h2 data-split="1">{s["nome"]}</h2><a class="url2" href="{s["href"]}" target="_blank" rel="noopener">{s["dominio"]} {ARRU}</a></div>'
                  f'<div><p>{s["descricao"]}</p><ul class="hl2">' + ''.join(f'<li>{d}</li>' for d in s['destaques']) + '</ul>'
                  + (chips(s['estrutura'], 'chips st2') if s.get('estrutura') else '') + '</div></div>')
            idn = f'<div class="idn">{swatches(s["cores"])}{fonts(s["fontes"])}</div>'
            body += f'<section class="sec{dk}" id="{s["id"]}">{hd}{mock(s["mockup"], s["nome"] + " em computador e telemóvel")}{shots(s["dominio"], s["nome"], s["desktop"], s["mobile"])}{idn}'
            if s.get('testemunho'): body += quote(*s['testemunho'])
            body += '</section>'
    for e in c.get('extras', []):
        d = f'<p class="sl">{e["descricao"]}</p>' if e.get('descricao') else ''
        body += (f'<section class="sec dk"><div class="sh"><div><span class="ey">{e["etiqueta"]}</span><h2 data-split="1">{e["titulo"]}<br>{e["destaque"]}</h2></div>{d}</div>'
                 f'{mock(e.get("mockup"), e["nome"])}{shots(e["dominio"], e["nome"], e.get("desktop"), e.get("mobile"))}</section>')
    if c.get('construcao'):
        k = c['construcao']
        nums = '<dl class="cnum">' + ''.join(f'<div><dt>{v}</dt><dd>{l}</dd></div>' for v, l in k['numeros']) + '</dl>'
        fas = '<div class="tline t4" style="margin-top:3rem">' + ''.join(f'<div><span class="n">{t}</span><h3>{n}</h3><p>{x}</p></div>' for t, n, x in k['fases']) + '</div>'
        blk = '<div class="cblk" data-cards>' + ''.join(f'<div><h3>{t}</h3><p>{x}</p>' + ('<ul>' + ''.join(f'<li>{p}</li>' for p in pts) + '</ul>' if pts else '') + chips(st, 'chips st3') + '</div>' for t, x, pts, st in k['blocos']) + '</div>'
        body += f'<section class="sec dk">{sh("02 · Como foi construído", k["titulo"])}{nums}{fas}{blk}</section>'
    idn = ''
    if c.get('cores') or c.get('fontes'):
        idn = f'<div class="idn">{swatches(c.get("cores", []))}{fonts(c.get("fontes", []))}</div>'
    est = f'<div class="bl2"><span class="ey">Estrutura</span>{chips(c["estrutura"], "chips st2")}</div>' if c.get('estrutura') else ''
    tec = f'<div class="bl2"><span class="ey">Tecnologia e parte técnica</span>{chips(c["tecnologia"], "chips st2")}</div>'
    vis_b = '<div class="vbtn">' + ''.join(f'<a class="pill d" href="{h}" target="_blank" rel="noopener">{l} ↗</a>' for l, h in c['visitar']) + '</div>'
    body += f'<section class="sec">{sh("Ficha técnica", "Identidade, estrutura<br>e tecnologia.") if (idn or est) else sh("Ficha técnica", "Tecnologia.")}{idn}{est}{tec}{vis_b}</section>'
    body += (f'<section class="sec tight"><a class="nextw" href="%%L:trabalhos/{nxt["slug"]}%%"><span class="ey">Próximo trabalho</span><b>{nxt["curto"]}</b>'
             f'<span class="go">%%ARR%%</span></a></section>')
    return dict(slug='trabalhos/' + c['slug'], crumb=c['curto'], pre='Website', kind='case', case=c,
                title=f'{c["nome"]} · Caso de estudo · Starmountain Flash', desc=c['desc'], faq=[], body=body, contact=None, foot=None)

def page_lista():
    s = [(c['shots'][0][0], c['shots'][0][1], c['nome']) for c in CASOS]
    VIS = (f'<div class="hud" id="vis-web" data-cycle="3200"><div class="hh"><span>Trabalhos</span><span class="live">{len(CASOS)} casos</span></div>'
           '<div class="br"><div class="bb"><span class="dots"><i></i><i></i><i></i></span><div class="url" data-g>' + ''.join(f'<span class="{"on" if i == 0 else ""}">{d}</span>' for i, (d, *_) in enumerate(s)) + '</div></div>'
           '<div class="shot" data-g>' + ''.join(f'<img class="{"on" if i == 0 else ""}" src="{im(f)}" alt="">' for i, (_, f, _n) in enumerate(s)) + '</div></div>'
           '<div class="cap" data-g>' + ''.join(f'<div class="{"on" if i == 0 else ""}"><b>{n}</b><small>{d}</small></div>' for i, (d, _f, n) in enumerate(s)) + '</div></div>')
    rows = ''
    for i, c in enumerate(CASOS):
        f = dict(c['ficha'])
        img = c.get('mockupTopo') or c['shots'][0][1]
        rows += (f'<a class="wrow" href="%%L:trabalhos/{c["slug"]}%%"><figure><img src="{im(img)}" alt="{H.escape(c["nome"])}" loading="lazy"></figure>'
                 f'<div class="wtx"><span class="ey">{i + 1:02d} · <span>{f.get("Serviço", "")}</span></span><h3>{c["nome"]}</h3><p>{c["desc"]}</p>'
                 f'<span class="wdom">{c["ficha"][-1][1]}</span><span class="pill d">Ver caso de estudo ↗</span></div></a>')
    body = hero('Trabalhos', 'Trabalhos entregues,<br>com os detalhes.', 'Websites, landing pages e plataformas que estão no ar. Em cada caso mostro o pedido, o que foi feito e a parte técnica.',
                'Proposta visual gratuita', 'Website', '#casos', 'Ver os casos', 'Trabalhos', VIS, mid=False)
    body += f'<section class="sec" id="casos">{sh("Casos de estudo", "Quatro projetos,<br>quatro pedidos diferentes.")}<div class="wlist" data-cards>{rows}</div></section>'
    return dict(slug='trabalhos', crumb='Trabalhos', pre='Website', kind='works', cases=CASOS, title='Trabalhos · Starmountain Flash',
                desc='Casos de estudo da Starmountain Flash: sites da Universidade da Beira Interior, Planet Trading, StudyOS e Beatriz Nunes, com o pedido, a solução e a parte técnica.',
                faq=[], body=body, contact=None, foot=None)

def pages():
    return [page_lista()] + [page_caso(c, CASOS[(i + 1) % len(CASOS)]) for i, c in enumerate(CASOS)]
