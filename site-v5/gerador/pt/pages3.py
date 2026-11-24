# Bloco Sobre, Contacto e Como trabalho. Copy from the live site, reviewed with the anti-IA rule.
from pages import hero, sh, faq_sec, U

# ---------------------------------------------------------------- /sobre
VIS_ME = '''<div class="hud me" id="vis-me"><div class="phw"><img src="%%PEDRO%%" alt="Pedro Pereira, fundador da Starmountain Flash"><div class="cap2"><b>Pedro Pereira</b><span>Covilhã · Serra da Estrela</span></div></div>
<div class="fx"><div><b>+8</b><span>projetos entregues, entre sites, landing pages e plataformas</span></div><div><b>UBI</b><span>fornecedor digital da Universidade da Beira Interior</span></div><div><b>1</b><span>responsável, do primeiro contacto ao lançamento</span></div></div></div>'''

CERTS = [('Em curso', 'uab', '2e8ac7d250b8.webp', 'Universidade Aberta', 'Licenciatura em Gestão', 'Gestão de empresas, finanças e organização.', 'Universidade Aberta', ''),
         ('Certificado · 2026', 'ga', 'd73b4f73374d.webp', 'Google Analytics Certified', 'Google Analytics', 'Medição e análise de tráfego, comportamento e conversões em sites.', 'Google · válido até agosto de 2027 · ID 192548880', ''),
         ('Concluído · 2026', 'ipl', '3b1f67e51adc.webp', 'Politécnico de Lisboa', 'Programação para a Web', 'Curso de 25 horas sobre desenvolvimento web.', 'Politécnico de Lisboa · NAU', 'https://lms.nau.edu.pt/certificates/6f516acd627b42f9aa5cf1917f6f161a'),
         ('Atribuída', 'mil', '4daa75908b2a.webp|cecffb75367e.webp', 'Exército Português|NATO / OTAN', 'Medalha de reconhecimento nacional', 'Missão internacional ao serviço da NATO.', 'Exército Português · NATO / OTAN', ''),
         ('Parceiro', 'shp', '57a6d7963f59.webp', 'Shopify', 'Shopify Partner', 'Programa de parceiros para criação de lojas online.', 'Shopify', '')]

def certs():
    out = ''
    for st, k, imgs, alts, t, d, by, link in CERTS:
        im = ''.join(f'<img src="%%ASSET:{f}%%" alt="{a}">' for f, a in zip(imgs.split('|'), alts.split('|')))
        lk = f' · <a href="{link}" target="_blank" rel="noopener">Verificar ↗</a>' if link else ''
        out += f'<div class="ce"><span class="st">{st}</span><div class="lg2">{im}</div><h3>{t}</h3><p>{d}</p><small>{by}{lk}</small></div>'
    return out

def page_sobre():
    tl = [('01', 'Formação militar', 'Missão internacional e medalha de reconhecimento nacional. Aprendi a planear, a cumprir o que combino e a não deixar nada a meio.'),
          ('02', 'Lisboa e Estados Unidos', 'Anos a viver fora do Porto e fora do país, que me deram outra forma de ver negócios, clientes e maneiras de trabalhar.'),
          ('03', 'Dentro das empresas', 'O dia a dia das empresas visto por dentro: números, prazos, documentos e muito trabalho repetitivo.'),
          ('04', 'Starmountain Flash', 'De gosto pessoal por web design a serviço de websites e automações com IA, a partir da Covilhã.'),
          ('05', 'Universidade da Beira Interior', 'Fornecedor digital da UBI, com três sites institucionais no ar.')]
    tlh = ''.join(f'<div><span class="n">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n, t, d in tl)
    rules = [('Ver antes de decidir', 'Começo por uma proposta visual gratuita. O orçamento só chega depois, se quiser avançar.'),
             ('Um plano escrito', 'Antes de começar, fica escrito o que vai receber e quando. Se alguma coisa mudar, sabe no próprio dia.'),
             ('Sem intermediários', 'Fala sempre comigo. Quem ouve o pedido é quem o constrói.'),
             ('Franqueza', 'Se alguma coisa não compensa, digo-lhe. Mesmo que isso signifique um projeto mais pequeno.')]
    rh = ''.join(f'<div><span class="n">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(rules))
    return dict(
        slug='sobre', crumb='Sobre', pre='', kind='about',
        title='Sobre Pedro Pereira · Starmountain Flash',
        desc='Pedro Pereira, fundador da Starmountain Flash: formação militar, websites e automações com IA para empresas, a partir da Covilhã.',
        faq=[],
        body=hero('Sobre', 'Websites e automações feitos na Covilhã,<br>longe dos grandes centros.',
                  'Formação militar e muitas horas a construir sites e automações. É isso que está por trás de cada projeto da Starmountain Flash.',
                  'Proposta gratuita', '', '#percurso', 'Ver o percurso', 'Sobre', VIS_ME, mid=False, cls='sub sm')
        + '<section class="sec"><div class="two" data-cards><div><span class="ey">01 · Quem sou</span><h2 data-split="1" style="margin-top:1rem">Olá, sou o Pedro.</h2><p class="role">Fundador da Starmountain Flash.</p></div>'
        + '<div class="txt"><p>Nasci no Porto, vivi em Lisboa e nos Estados Unidos, e hoje trabalho a partir da Covilhã, junto à Serra da Estrela.</p>'
        + '<p>Conheço por dentro os processos das empresas e vejo de perto onde se perde tempo: dados copiados à mão, pedidos esquecidos, relatórios montados à pressa. É daí que vem a parte das automações.</p>'
        + '<p>A parte dos sites começou como um gosto pessoal por web design. Tornou-se serviço quando percebi que muitas empresas tinham bons produtos e nenhuma forma de serem encontradas.</p>'
        + '<p>Antes de tudo isto houve o Exército. Uma missão internacional ao serviço da NATO e uma medalha de reconhecimento nacional ensinaram-me duas coisas que trago para cada projeto: um plano escrito antes de começar, e dizer logo quando alguma coisa muda.</p></div></div></section>'
        + f'<section class="sec dk" id="percurso">{sh("02 · Percurso", "Do Porto à Serra da Estrela,<br>pelo caminho mais longo.")}<div class="tline" data-cards>{tlh}</div></section>'
        + '<section class="sec"><div class="name" data-cards><div><span class="ey">03 · O nome</span><h2 data-split="1" style="margin-top:1rem">Starmountain Flash.</h2></div>'
        + '<div class="nm2"><div><b>Starmountain</b><span>Vem da Serra da Estrela, onde a empresa está.</span></div><div><b>Flash</b><span>Vem da rapidez de execução e da inteligência artificial que está no centro das automações.</span></div></div></div></section>'
        + f'<section class="sec tight">{sh("04 · Formação e certificações", "Formação académica,<br>profissional e militar.", "O que está por trás de cada projeto, com as entidades que o atribuíram.")}<div class="certs" data-cards>{certs()}</div></section>'
        + f'<section class="sec dk">{sh("05 · Como trabalho", "Quatro regras<br>em todos os projetos.")}<div class="inc rules3" data-cards>{rh}</div></section>'
        + f'<section class="sec">{sh("06 · Visão e missão", "Duas frases que decidem<br>o que aceito e o que recuso.")}'
        + '<div class="duo vm" data-cards><div><small>Missão · o que faço todos os dias</small><b>Pôr a tecnologia a fazer o trabalho repetitivo das empresas, para as pessoas ficarem com tempo para o que só elas sabem fazer.</b></div>'
        + '<div><small>Visão · para onde quero chegar</small><b>Ser reconhecida como uma empresa tecnológica portuguesa com produtos próprios, criada fora dos grandes centros.</b></div></div></section>',
        contact=None, foot=None)

# ---------------------------------------------------------------- /contacto
WA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20l1.2-4.3A8.5 8.5 0 1 1 20 11.5Z"/></svg>'
ML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'
PH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>'

VIS_CT = f'''<div class="hud" id="vis-ct"><div class="hh"><span>Contactos diretos</span><span class="live">09:00–20:30</span></div>
<a class="ch2" href="mailto:geral@starmountainflash.pt"><span class="ic">{ML}</span><div><small>Email</small><b>geral@starmountainflash.pt</b></div><span class="ar">↗</span></a>
<a class="ch2" href="https://wa.me/351937800553" target="_blank" rel="noopener"><span class="ic">{WA}</span><div><small>WhatsApp</small><b>Enviar mensagem</b></div><span class="ar">↗</span></a>
<a class="ch2" href="tel:+351937800553"><span class="ic">{PH}</span><div><small>Telefone</small><b>+351 937 800 553</b></div><span class="ar">↗</span></a>
<div class="ft"><span>Covilhã, Portugal</span><span>Leio e respondo eu</span></div></div>'''

def page_contacto():
    return dict(
        slug='contacto', crumb='Contacto', pre='', kind='contact',
        title='Contacto · Starmountain Flash',
        desc='Contacte a Starmountain Flash por email, telefone ou WhatsApp, ou peça uma proposta gratuita para o seu site, loja online, visibilidade em IA ou automação.',
        faq=[],
        body=hero('Contacto', 'Contacto.<br>Fala sempre comigo.',
                  'Um site novo, uma loja online, visibilidade na IA ou uma tarefa para automatizar. Escolha o canal que lhe der mais jeito, ou peça já uma proposta gratuita.',
                  'Proposta gratuita', '', '#contact', 'Ir para o formulário', 'Contacto', VIS_CT, mid=False)
        + '<section class="sec"><div class="two" data-cards><div><span class="ey">Onde estou</span><h2 data-split="1" style="margin-top:1rem">Covilhã, Serra da Estrela.<br>Clientes em todo o país.</h2></div>'
        + '<div class="txt"><p>Trabalho à distância com empresas de todo o país. As reuniões fazem-se online ou, quando faz sentido, nas instalações do cliente.</p>'
        + '<div class="notes" style="grid-template-columns:1fr 1fr;margin-top:2rem"><div><b>Horário de contacto</b><span>09:00–20:30, por email, WhatsApp ou telefone.</span></div><div><b>Quem responde</b><span>Leio e respondo eu, pelo meio que escolher.</span></div></div></div></div></section>'
        + '<section class="sec dk"><div class="sh"><div><span class="ey">Depois de enviar</span><h2 data-split="1">O que acontece<br>a seguir.</h2></div></div>'
        + '<div class="cflow" data-cards><div class="cn"><span class="k">01</span><b>Envia o pedido</b><small>Pelo formulário, email ou WhatsApp</small></div>'
        + '<div class="cn"><span class="k">02</span><b>Leio e respondo eu</b><small>Pelo meio que escolheu</small></div>'
        + '<div class="cbr"><div class="cn hl"><span class="k">Websites e lojas</span><b>Proposta visual gratuita</b><small>Vê primeiro como pode ficar</small></div><div class="cn hl"><span class="k">Automações com IA</span><b>Método StarMap</b><small>Uma semana de registo e um relatório</small></div></div>'
        + '<div class="cn end"><span class="k">03</span><b>O orçamento</b><small>Só chega depois, se quiser avançar</small></div></div></section>',
        contact=None, foot=None)

# ---------------------------------------------------------------- /metodo (Como trabalho)
PH3 = [('01', 'Reconhecimento', 'Antes de desenhar, perceber o negócio, os clientes e onde se está a perder tempo ou oportunidades.',
        ['Conversa sobre objetivos e prioridades', 'Análise do site atual, se existir', 'Análise da concorrência e das ferramentas que usa'],
        ['Proposta visual gratuita', 'Se quiser avançar, o orçamento ajustado ao que pediu', 'Recomendação do formato certo: landing page, site, loja ou automação'],
        ['Uma conversa de cerca de 30 minutos, online', 'Acesso ao que já existe: site, redes, materiais']),
       ('02', 'Execução', 'Com o orçamento aprovado, o projeto avança no prazo combinado, com pontos de validação definidos desde o início.',
        ['Design à medida, com uma primeira validação', 'Desenvolvimento em código, com uma segunda validação', 'Testes em telemóvel, velocidade e SEO', 'Lançamento e configuração do domínio'],
        ['O site no ar, rápido e preparado para o Google e a IA', 'Acessos e explicação de como funciona'],
        ['Textos base sobre o negócio', 'Logótipo e fotografias, se existirem', 'Respostas nas validações, nas datas combinadas']),
       ('03', 'Automação', 'Depois do lançamento, ou como projeto à parte, o trabalho repetitivo do negócio passa a correr sozinho.',
        ['Levantamento das tarefas repetitivas e do tempo que ocupam', 'Construção da automação com as suas ferramentas', 'Testes com casos reais antes de entrar em funcionamento'],
        ['A automação a funcionar', 'Uma explicação simples de como funciona', 'Acompanhamento nas primeiras semanas'],
        ['Acesso às ferramentas envolvidas', 'Alguém que conheça bem o processo'])]

VIS_PH = '<div class="hud" id="vis-ph" data-cycle="2600"><div class="hh"><span>As três fases</span><span class="live">em curso</span></div><div class="phl" data-g>' + ''.join(f'<div><span class="k">{n}</span><div><b>{t}</b><p>{d}</p></div></div>' for n, t, d, *_ in PH3) + '</div><div class="ft"><span>Cada fase termina com uma validação sua.</span></div></div>'

FAQ_MET = [('E se quiser mudar alguma coisa a meio?', 'As validações existem para isso: os ajustes pedidos nesses momentos fazem parte do projeto. Mudanças que alterem o âmbito acordado são conversadas antes e, se for preciso, orçamentadas à parte.'),
           ('Quantas rondas de alterações estão incluídas?', 'Ficam definidas no orçamento, de acordo com o tipo de projeto, para que ambos saibam desde o início com o que contar.'),
           ('Como são feitos os pagamentos?', 'As condições ficam no orçamento. O mais comum é dividir o pagamento entre o arranque e a entrega do projeto.'),
           ('Quanto tempo demora um projeto?', 'Depende do formato. O prazo fica combinado antes de começar. Landing pages são o formato mais rápido; lojas online e automações levam mais tempo.'),
           ('As reuniões são presenciais ou online?', 'Online, o que permite trabalhar com empresas de todo o país. Estou na Covilhã e, quando faz sentido, também é possível reunir presencialmente.'),
           ('E se o projeto não avançar depois da proposta?', 'Nada. A proposta visual é gratuita e serve precisamente para perceber se faz sentido para os dois. Só avançamos se quiser, depois do orçamento.')]

def page_metodo():
    def col(t, it): return f'<div><small>{t}</small><ul>' + ''.join(f'<li>{x}</li>' for x in it) + '</ul></div>'
    gates = ['Orçamento aprovado', 'Site no ar']
    nodes = ''
    for i, (n, t, d, a, b, c) in enumerate(PH3):
        nodes += f'<button type="button" class="fn" data-t><span class="k">{n}</span><b>{t}</b><small>{b[0]}</small></button>'
        if i < 2: nodes += f'<span class="fg"><i></i><em>{gates[i]}</em></span>'
    pans = ''.join(f'<div class="fp" data-p><p class="fd"><span class="mn">{n}</span>{d}</p><div class="cols">{col("O que acontece", a)}{col("O que recebe", b)}{col("O que preciso de si", c)}</div></div>' for n, t, d, a, b, c in PH3)
    ph = f'<div class="flow3" data-tabs="auto"><div class="fnodes">{nodes}</div><div class="fpanels">{pans}</div></div>'
    rules = [('Ver antes de decidir', 'Começo por uma proposta visual gratuita. O orçamento só chega depois, se quiser avançar, ajustado ao que pedir.'),
             ('Um plano escrito', 'O que vai receber e quando fica combinado antes de começar. Se alguma coisa mudar, sabe no próprio dia.'),
             ('Um só responsável', 'Fala sempre comigo, do primeiro contacto ao lançamento. Quem ouve o pedido é quem o constrói.'),
             ('Tudo em seu nome', 'O domínio e as contas ficam em nome da empresa. O site é seu e não fica preso a mim.')]
    rh = ''.join(f'<div><span class="n">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(rules))
    return dict(
        slug='metodo', crumb='Como trabalho', pre='', kind='page',
        title='Como trabalho · Starmountain Flash',
        desc='Como funciona um projeto com a Starmountain Flash: reconhecimento, execução e automação, a começar por uma proposta visual gratuita.',
        faq=FAQ_MET,
        body=hero('Como trabalho', 'Três fases,<br>cada uma com um fim claro.',
                  'Sabe o que acontece, o que recebe e o que precisa de fazer da sua parte, antes de cada fase começar.',
                  'Proposta gratuita', '', '#fases', 'Ver as fases', 'Como trabalho', VIS_PH, mid=False)
        + f'<section class="sec" id="fases">{sh("01 · Em detalhe", "Fase a fase,<br>sem letras pequenas.", "Sabe sempre em que ponto está o projeto, o que vem a seguir e o que falta da sua parte.")}{ph}</section>'
        + f'<section class="sec dk">{sh("02 · Em todos os projetos", "Quatro compromissos<br>que não mudam.")}<div class="inc rules3" data-cards>{rh}</div></section>'
        + f'<section class="sec">{sh("03 · Manutenção", "Depois do<br>lançamento.")}<div class="duo" data-cards><div><b>Avença mensal</b><span>Atualizações e pequenas alterações, com um valor fixo por mês.</span></div><div><b>Alterações pontuais</b><span>Sem compromisso mensal. Pede só quando precisar.</span></div></div></section>'
        + faq_sec('04 · Perguntas frequentes', 'Sobre a forma<br>de trabalhar.', FAQ_MET),
        contact=None, foot=None)
