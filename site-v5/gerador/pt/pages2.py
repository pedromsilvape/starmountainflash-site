# Bloco Presença digital. Copy from the live site, reviewed with the anti-IA rule.
from pages import hero, sh, faq_sec, mc, U, IC_CHAT, IC_FILE, IC_USER

def rel_pd(items, h2='Outros serviços<br>de presença digital.'):
    rows = ''.join(f'<a class="si" href="%%L:{slug}%%"><div><b>{t}</b><small>{d}</small></div><span class="go">%%ARR%%</span></a>' for k, slug, t, d in items)
    return f'<section class="sec tight"><div class="rel"><div><span class="ey">Presença digital</span><h2 data-split="1" style="margin-top:1rem">{h2}</h2></div><div class="grp pd"><div class="slist">{rows}</div></div></div></section>'

PD = {'websites': ('a.1', 'websites', 'Websites', 'Landing pages e sites institucionais, desenhados à medida e feitos em código.'),
      'lojas-online': ('a.2', 'lojas-online', 'Lojas online', 'Shopify ou à medida, com pagamentos, envios e faturação configurados.'),
      'visibilidade-ia': ('a.3', 'visibilidade-ia', 'Visibilidade em IA', 'Aparecer quando os clientes perguntam ao ChatGPT, ao Perplexity ou ao Gemini.'),
      'avaliacoes-google': ('a.4', 'avaliacoes-google', 'Avaliações Google', 'Pedido de avaliação a cada cliente e resposta a todas as avaliações do perfil.')}
def others(me): return [v for k, v in PD.items() if k != me]

def kvd(rows): return '<div class="kvd">' + ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in rows) + '</div>'

IVA = ('Os valores incluem IVA?', 'Não há IVA a acrescentar: a atividade está isenta ao abrigo do artigo 53.º do CIVA. O valor do orçamento é o valor final.')

# ---------------------------------------------------------------- /websites
WORKS = [('dei.ubi.pt', 'UBI', 'Universidade da Beira Interior', 'ubi-dei-desktop.webp', 'ubi'),
         ('comunidadeplanet.pt', 'Planet Trading', 'Landing page 3D', 'planet-trading-desktop.webp', 'planet-trading'),
         ('gestaocrew.pt', 'StudyOS', 'Plataforma web', 'studyos-landing-desktop.webp', 'studyos'),
         ('personaltrainerbeatriznunes.pt', 'Beatriz Nunes', 'Personal trainer', 'beatriz-nunes-desktop.webp', 'beatriz-nunes')]

VIS_WEB = ('<div class="hud" id="vis-web" data-cycle="3200"><div class="hh"><span>Sites no ar</span><span class="live">clientes reais</span></div>'
           '<div class="br"><div class="bb"><span class="dots"><i></i><i></i><i></i></span><div class="url" data-g>' + ''.join(f'<span>{u}</span>' for u, *_ in WORKS) + '</div></div>'
           '<div class="shot" data-g>' + ''.join(f'<img data-from="#wk{i}" alt="">' for i in range(len(WORKS))) + '</div></div>'
           '<div class="cap" data-g>' + ''.join(f'<div><b>{n}</b><small>{d}</small></div>' for _, n, d, *_ in WORKS) + '</div></div>')

FAQ_WEB = [('Quanto custa um site?', 'Como referência, uma landing page fica entre 500 € e 2.000 € e um site institucional entre 1.000 € e 5.000 €, conforme o que o site precisa de fazer. O guia <a href="' + U + '/blog/quanto-custa-um-site-pme-portugal" style="text-decoration:underline;text-underline-offset:3px">quanto custa um site em Portugal</a> explica o que faz variar o preço. Começo por uma proposta visual gratuita. Se gostar e quiser avançar, envio o orçamento ajustado ao que pedir.'),
           ('Quanto tempo demora?', 'O prazo fica definido na proposta, antes de começar. Uma landing page é o formato mais rápido; um site institucional leva mais tempo, conforme o número de páginas.'),
           ('Preciso de ter os textos e as fotografias?', 'Ajuda, mas não é obrigatório. Estruturo os textos a partir do que me conta sobre o negócio. Fotografias próprias funcionam sempre melhor do que imagens de banco.'),
           ('Consigo atualizar o site sozinho?', 'Se precisar de atualizar com frequência, por exemplo notícias, produtos ou equipa, isso fica previsto na proposta. Para o resto, há a manutenção mensal ou alterações pontuais.'),
           ('O que é GEO?', 'GEO (Generative Engine Optimization) é preparar o site para ser compreendido e citado por motores de IA como o ChatGPT, o Gemini ou o Perplexity. Passa por conteúdo claro, perguntas frequentes e dados estruturados, além do SEO tradicional.'),
           IVA]

INC_WEB = [('Design à medida', 'Desenhado para a sua marca e para o seu cliente, e não um tema comprado com o logótipo trocado.'),
           ('Feito em código', 'Desenvolvido em código (Next.js), e não num construtor de arrastar. Páginas leves, rápidas e seguras.'),
           ('Pensado para telemóvel', 'A maioria das visitas chega pelo telemóvel. O site é desenhado primeiro para aí.'),
           ('SEO técnico', 'Títulos, descrições, sitemap, dados estruturados e URLs limpos, prontos para o Google.'),
           ('Preparado para IA', 'Conteúdo organizado para ser compreendido e citado pelo ChatGPT, Gemini e Perplexity.'),
           ('Contactos ligados', 'Formulário que chega ao seu email, botão de WhatsApp e telefone com um toque.'),
           ('Páginas legais', 'Política de privacidade, cookies e ligação ao Livro de Reclamações, como a lei exige.'),
           ('Domínio em seu nome', 'Ajudo a registar e configurar. O domínio fica sempre em nome da empresa.')]

def page_web():
    inc = ''.join(f'<div><span class="n">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(INC_WEB))
    wks = ''.join(f'<a class="wk2" href="{U}/trabalhos/{sl}" target="_blank" rel="noopener"><div class="im"><img id="wk{i}" src="%%IMG:{im}%%" alt="Site {n}: {d} ({u})" loading="lazy"></div><div class="tx2"><small>{u}</small><b>{n}</b><span>{d}</span></div></a>' for i, (u, n, d, im, sl) in enumerate(WORKS))
    return dict(
        slug='websites', crumb='Websites', pre='Website',
        title='Criação de websites · Starmountain Flash',
        desc='Landing pages e sites institucionais à medida: rápidos, pensados para telemóvel e preparados para o Google e para motores de IA. Proposta visual gratuita.',
        service=dict(name='Criação de websites', type='Criação de websites e landing pages', offers=(500, None)),
        faq=FAQ_WEB,
        body=hero('Websites', 'Websites que<br>trazem clientes.',
                  'Landing pages e sites institucionais desenhados à medida, pensados para telemóvel e preparados para aparecer no Google e nas respostas do ChatGPT.',
                  'Proposta visual gratuita', 'Website', '#formatos', 'Ver formatos', 'Websites', VIS_WEB)
        + f'<section class="sec" id="formatos">{sh("01 · Dois formatos", "Uma página ou um site completo.<br>Depende do objetivo.", "Para empresas que ainda não têm site, que têm um site antigo que não traz contactos, ou que precisam de uma página para lançar um serviço ou uma campanha. Às vezes faz sentido começar por uma landing page e crescer depois.")}'
        + '<div class="tech" data-cards><div class="tk"><span class="tag">Formato 01</span><h3>Landing page</h3><p>Uma única página com um único objetivo: pedir contacto, marcar, comprar ou inscrever-se. Tudo o que está na página empurra nessa direção.</p>'
        + kvd([('Ideal para', 'Lançar um serviço, campanhas pagas, eventos, profissionais independentes'), ('Estrutura', 'Uma página longa, com secções pensadas para converter'), ('Contacto', 'Formulário, WhatsApp ou marcação direta')]) + '</div>'
        + '<div class="tk dk"><span class="tag">Formato 02</span><h3>Site institucional</h3><p>O site completo da empresa, com várias páginas. Explica quem é, o que faz e para quem, e dá ao Google e aos motores de IA conteúdo suficiente para o recomendarem.</p>'
        + '<div class="kv"><div><b>Ideal para</b><span>Empresas com vários serviços, equipas, clínicas, escritórios, instituições</span></div><div><b>Estrutura</b><span>Início, serviços, sobre, trabalhos, contactos e blog, se fizer sentido</span></div><div><b>Contacto</b><span>Formulário, WhatsApp, telefone e mapa</span></div></div></div></div></section>'
        + f'<section class="sec">{sh("02 · O que está incluído", "Tudo o que um site precisa,<br>descrito antes de começar.", "Cada ponto fica descrito na proposta, para saber exatamente o que recebe.")}<div class="inc" data-cards>{inc}</div></section>'
        + f'<section class="sec dk"><div class="sh"><div><span class="ey">03 · Trabalhos</span><h2 data-split="1">Sites no ar,<br>de clientes reais.</h2></div><a class="lk" href="%%L:trabalhos%%" style="color:#fff">Ver todos os trabalhos</a></div><div class="wks" data-cards>{wks}</div></section>'
        + f'<section class="sec">{sh("04 · Manutenção", "Depois do<br>lançamento.")}<div class="duo" data-cards><div><b>Avença mensal</b><span>Atualizações e pequenas alterações, com um valor fixo por mês.</span></div><div><b>Alterações pontuais</b><span>Sem compromisso mensal. Pede só quando precisar.</span></div></div></section>'
        + faq_sec('05 · Perguntas frequentes', 'Sobre websites,<br>em poucas palavras.', FAQ_WEB)
        + rel_pd(others('websites')),
        contact=('Veja como pode ficar antes de decidir.', 'Peça uma proposta visual gratuita. Mostro-lhe uma primeira versão do site e, se gostar, envio o orçamento ajustado ao que precisa.'),
        foot=None)

# ---------------------------------------------------------------- /lojas-online
VIS_SHOP = '''<div class="hud" id="vis-shop" data-cycle="1500" data-n="7"><div class="hh"><span>Loja Exemplo</span><span class="live">encomenda nova</span></div>
<div class="pc"><span class="im">LATA</span><div><small>Conserva</small><b>Sardinhas em azeite</b></div><span class="pr2">3,90 €</span></div>
<div class="pay" data-g="upto" data-off="1"><span>MB WAY</span></div>
<div class="tot2"><span>6 latas · total com portes</span><b>27,30 €</b></div>
<div class="stp" data-g="upto" data-off="2"><div>Encomenda #1048 confirmada</div><div>Fatura emitida</div><div>Etiqueta de envio criada</div><div>Email com o código de seguimento</div></div>
<div class="ft"><span>Produto e loja fictícios.</span></div></div>'''

FAQ_SHOP = [('Quanto custa uma loja online?', 'Depende da plataforma, do número de produtos e das integrações. Começo por uma proposta visual gratuita e, se quiser avançar, envio o orçamento ajustado ao que pedir.'),
            ('Que custos mensais tem uma loja?', 'A plataforma e os métodos de pagamento têm custos próprios, pagos diretamente pelo cliente a esses serviços. Explico-os na proposta para não haver surpresas.'),
            ('Consigo gerir os produtos sozinho?', 'Sim. A formação para gerir produtos, encomendas e clientes está incluída.'),
            ('Posso passar os produtos da loja antiga?', 'Sim, sempre que a plataforma antiga permita exportar os dados. Avalio isso antes de começar.'),
            ('Os valores incluem IVA?', 'Não há IVA a acrescentar sobre o meu trabalho: a atividade está isenta ao abrigo do artigo 53.º do CIVA.')]

def page_shop():
    g4 = [('Montra', [('Catálogo organizado', 'Produtos, variantes, categorias e filtros pensados para quem compra.'), ('SEO de produto', 'Páginas de produto preparadas para aparecer no Google e em motores de IA.')]),
          ('Compra', [('Pagamentos', 'Métodos de pagamento usados em Portugal, conforme a plataforma escolhida.'), ('Emails automáticos', 'Confirmação de encomenda, envio e recuperação de carrinhos.')]),
          ('Entrega', [('Envios e portes', 'Regras de envio, zonas e portes grátis configurados à sua medida.'), ('Faturação', 'Ligação ao programa de faturação, quando a plataforma o permite.')]),
          ('Depois', [('Páginas legais', 'Termos, devoluções, privacidade e Livro de Reclamações, como a lei exige.'), ('Formação', 'Uma sessão para aprender a gerir produtos, encomendas e clientes sozinho.')])]
    inc = ''.join(f'<div><span class="n">{i + 1:02d}</span><h3>{t}</h3><dl>' + ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in it) + '</dl></div>' for i, (t, it) in enumerate(g4))
    return dict(
        slug='lojas-online', crumb='Lojas online', pre='Loja online',
        title='Criação de lojas online · Starmountain Flash',
        desc='Lojas online em Shopify ou à medida: catálogo, pagamentos, envios, páginas legais e formação incluídos. Proposta visual gratuita.',
        service=dict(name='Criação de lojas online', type='Lojas online em Shopify ou à medida', offers=None),
        faq=FAQ_SHOP,
        body=hero('Lojas online', 'Lojas online que vendem,<br>sem complicar a gestão.',
                  'Lojas em Shopify ou à medida, com catálogo, pagamentos e envios configurados para o mercado português, e formação para gerir tudo sozinho.',
                  'Proposta visual gratuita', 'Loja online', '#plataforma', 'Shopify ou à medida', 'Lojas online', VIS_SHOP)
        + '<section class="method" style="border-radius:0;padding-top:5.5rem"><div class="hh"><span class="ey">01 · Para quem é</span><h2 data-split="1" style="margin-top:1rem">Três pontos de partida<br>diferentes.</h2><p class="tlead" style="margin:1.4rem auto 0;text-align:center">O ponto de partida muda a forma como a loja é pensada, mas o objetivo é o mesmo: vender sem passar o dia a gerir.</p></div><div class="mgrid mgrid3" data-cards>'
        + mc('01', 'Instagram', 'Vende por mensagem', 'Marcas que hoje vendem por mensagem no Instagram e querem uma loja própria.', icon=IC_CHAT)
        + mc('02', 'Loja física', 'Quer vender também online', 'Lojas com porta aberta que querem chegar a quem não pode ir lá.', icon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9h16l-1-5H5ZM5 9v11h14V9M10 20v-6h4v6"/></svg>')
        + mc('03', 'Loja antiga', 'Já tem loja, mas não funciona', 'Lojas difíceis de gerir ou que não vendem, a precisar de ser refeitas.', icon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>')
        + '</div></section>'
        + f'<section class="sec" id="plataforma">{sh("02 · Plataforma", "Shopify ou à medida.<br>Depende do negócio.", "Explico as diferenças antes de decidir, incluindo os custos mensais de cada opção.")}'
        + '<div class="tech" data-cards><div class="tk"><span class="tag">Opção 01</span><h3>Shopify</h3><p>A plataforma de comércio eletrónico mais usada no mundo. Fiável, segura e fácil de gerir no dia a dia, mesmo sem conhecimentos técnicos.</p>'
        + kvd([('Ideal para', 'Catálogos de produtos físicos, marcas que querem crescer rápido'), ('Gestão', 'Painel simples para produtos, encomendas e clientes'), ('Custos', 'Subscrição mensal da plataforma, paga diretamente pelo cliente'), ('Parceria', 'Sou Shopify Partner: crio a loja e transfiro-a para o seu nome')]) + '</div>'
        + '<div class="tk dk"><span class="tag">Opção 02</span><h3>Loja à medida</h3><p>Desenvolvida de raiz para o que o negócio precisa, quando as plataformas prontas não encaixam no modelo de venda.</p>'
        + '<div class="kv"><div><b>Ideal para</b><span>Serviços, marcações, subscrições, regras de preço específicas</span></div><div><b>Gestão</b><span>Painel desenhado à volta do seu processo</span></div><div><b>Custos</b><span>Alojamento e serviços usados, definidos na proposta</span></div></div></div></div></section>'
        + f'<section class="sec tight">{sh("03 · O que está incluído", "Tudo configurado<br>antes de abrir a loja.", "Cada ponto fica descrito na proposta, para saber exatamente o que recebe.")}<div class="inc g4 chn" data-cards>{inc}</div>'
        + '<div class="callout dk"><div><h3>Loja e automação juntas.</h3><p>Uma loja gera trabalho repetitivo: encomendas para registar, stock para atualizar, clientes para responder. Muito disso pode ficar automatizado desde o início.</p></div><a href="%%L:automacoes%%" class="pill w">Ver automações</a></div></section>'
        + faq_sec('04 · Perguntas frequentes', 'Sobre lojas online,<br>em poucas palavras.', FAQ_SHOP)
        + rel_pd(others('lojas-online')),
        contact=('Veja a sua loja antes de decidir.', 'Peça uma proposta visual gratuita. Mostro-lhe como a loja pode ficar e, se gostar, envio o orçamento ajustado ao que precisa.'),
        foot=None)

# ---------------------------------------------------------------- /visibilidade-ia
ASSIST = ['ChatGPT', 'Perplexity', 'Gemini', 'Google AI']
ANSW = [(['Fisio Norte', 'Clínica Exemplo', 'Reabilita Braga'], 1), (['Clínica Exemplo', 'Fisio Norte', 'Movimento+'], 0), (['Fisio Norte', 'Reabilita Braga', 'Movimento+'], -1), (['Reabilita Braga', 'Clínica Exemplo', 'Fisio Norte'], 1)]

def answ():
    out = ''
    for names, me in ANSW:
        rows = ''.join(f'<p class="{"me" if i == me else ""}"><i>{i + 1}</i><span>{n}</span>{"<em>a sua empresa</em>" if i == me else ""}</p>' for i, n in enumerate(names))
        if me < 0: rows += '<div class="miss">A sua empresa não aparece nesta resposta</div>'
        out += f'<div>{rows}</div>'
    return out

VIS_GEO = (f'<div class="hud" id="vis-geo" data-cycle="2800"><div class="hh"><span>Resposta do assistente</span><span class="live">exemplo</span></div>'
           '<div class="q2"><small>Pergunta de um cliente</small>Fisioterapia desportiva em Braga, quem recomendas?</div>'
           '<div class="as" data-g>' + ''.join(f'<span>{a}</span>' for a in ASSIST) + '</div>'
           f'<div class="answ" data-g>{answ()}</div>'
           '<div class="ft"><span>Exemplo ilustrativo com empresas fictícias.</span><div class="cnt" style="text-align:right"><div class="ct" data-g style="margin-left:auto"><b>1 / 4</b><b>2 / 4</b><b>2 / 4</b><b>3 / 4</b></div><span>assistentes que a citam</span></div></div></div>')

FAQ_GEO = [('O que é GEO?', 'GEO (Generative Engine Optimization) é a otimização para motores de resposta com IA, como o ChatGPT, o Perplexity, o Gemini e os resumos de IA do Google. O objetivo é que a sua empresa seja citada nas respostas que dão aos seus clientes.'),
           ('Substitui o SEO?', 'Não, as duas coisas somam. Muitas bases são as mesmas (site rápido, conteúdo claro, perfil Google completo), mas a IA escolhe as fontes de forma diferente de uma lista de resultados.'),
           ('Garante o primeiro lugar?', 'Não. Ninguém controla as respostas de um assistente de IA. O que posso garantir é medir a sua presença todos os meses e mostrar-lhe o que foi feito para a aumentar.'),
           ('Quanto tempo demora?', 'As correções técnicas ficam feitas nas primeiras semanas. Os assistentes demoram algumas semanas a refletir as alterações, por isso a evolução lê-se ao longo de vários meses.'),
           ('Preciso de um site novo?', 'Na maioria dos casos, não. As correções são feitas no site que já tem. Se não for possível, digo-lhe as alternativas na auditoria.'),
           ('Funciona para qualquer setor?', 'Funciona sobretudo para empresas que os clientes procuram por necessidade ou por zona: serviços técnicos, saúde, formação, comércio e indústria.')]

C_SCHEMA = '''<span class="c">// o que a empresa é, onde e para quem</span>
{
  <span class="k">"@type"</span>: <span class="s">"MedicalClinic"</span>,
  <span class="k">"name"</span>: <span class="s">"Clínica Exemplo"</span>,
  <span class="k">"areaServed"</span>: <span class="s">"Braga"</span>,
  <span class="k">"medicalSpecialty"</span>: <span class="s">"Physiotherapy"</span>,
  <span class="k">"openingHours"</span>: <span class="s">"Mo-Fr 08:00-20:00"</span>,
  <span class="k">"telephone"</span>: <span class="s">"+351 253 000 000"</span>
}'''
C_LLMS = '''<span class="k"># Clínica Exemplo</span>
<span class="c">&gt; Fisioterapia desportiva e reabilitação em Braga.</span>

<span class="k">## Serviços</span>
- Fisioterapia desportiva
- Reabilitação pós-cirúrgica

<span class="k">## Contactos</span>
- Rua Exemplo, 12, Braga'''
C_ROBOTS = '''<span class="c"># deixar os assistentes de IA ler o site</span>
<span class="k">User-agent:</span> GPTBot
<span class="k">Allow:</span> /

<span class="k">User-agent:</span> PerplexityBot
<span class="k">Allow:</span> /

<span class="k">User-agent:</span> Google-Extended
<span class="k">Allow:</span> /'''

def page_geo():
    bars = ''.join(f'<div><b>{v}</b><i style="height:{v / 18 * 80:.0f}%"></i><small>Mês {i + 1}</small></div>' for i, v in enumerate([4, 7, 9, 12, 15, 18]))
    hb = ''.join(f'<div><span>{a}</span><span class="t"><i style="width:{v / 30 * 100:.0f}%"></i></span><b>{v}/30</b></div>' for a, v in [('ChatGPT', 18), ('Perplexity', 16), ('Gemini', 12), ('Google AI', 14)])
    return dict(
        slug='visibilidade-ia', crumb='Visibilidade em IA', pre='Visibilidade em IA',
        title='Visibilidade em IA (GEO) · Starmountain Flash',
        desc='Verifico se a sua empresa aparece nas respostas do ChatGPT, Perplexity, Gemini e Google AI e corrijo o site para que passe a aparecer. Verificação gratuita.',
        service=dict(name='Visibilidade em IA (GEO)', type='Generative Engine Optimization', offers=None),
        faq=FAQ_GEO,
        body=hero('Visibilidade em IA · GEO', 'Quando perguntam à IA,<br>a sua empresa aparece?',
                  'Quem precisa de um serviço na sua zona já pergunta ao ChatGPT antes de abrir o Google. Recebe dois ou três nomes e liga a um deles. Verifico se o seu está nessa resposta e corrijo o site para que passe a estar.',
                  'Verificação gratuita', 'Visibilidade em IA', '#trabalho', 'Como funciona', 'Visibilidade em IA', VIS_GEO)
        + f'<section class="sec">{sh("01 · Porquê agora", "Na resposta da IA<br>não há sexto lugar.", "No Google, quem aparecia em sexto ainda recebia uma ou outra visita. No ChatGPT a lista acaba ao terceiro nome, e quem não está nela não é contactado.")}'
        + '<div class="vs" data-cards><div class="s1"><span class="ey">Pesquisa tradicional</span><div class="rs">' + ''.join(f'<span><i>{i}</i>resultado</span>' for i in range(1, 11)) + '</div><div class="ft2"><b>10 resultados para comparar</b><span>O cliente abria quatro ou cinco sites e escolhia.</span></div></div>'
        + '<div class="s2"><span class="ey" style="color:var(--ac)">Resposta de IA</span><div class="rs2"><span><i>1</i>Empresa A</span><span><i>2</i>Empresa B</span><span><i>3</i>Empresa C</span></div><em>As restantes não aparecem</em><div class="ft2"><b>2 a 3 recomendações</b><span>Agora lê uma resposta e escolhe dali.</span></div></div></div>'
        + '<div class="stat2"><div><b>87,5%</b><span>dos profissionais e estudantes inquiridos em Portugal usam o ChatGPT.<small>“IA: Impacto e Futuro 2025”, Magma Studio, CIP e DSPA</small></span></div><div><b>4</b><span>assistentes analisados em cada auditoria: ChatGPT, Perplexity, Gemini e Google AI.</span></div></div></section>'
        + f'<section class="sec dk" id="trabalho">{sh("02 · O trabalho", "Por ordem, e sempre<br>com as mesmas perguntas.", "As perguntas do primeiro mês são as mesmas do sexto. Só assim se percebe se alguma coisa mudou.")}'
        + '<div class="tline t4" data-cards><div><span class="n">Semana 1</span><h3>Auditoria</h3><p>20 a 30 perguntas reais do setor e da zona, e quem é recomendado em cada uma.</p><div class="tg"><span>Concorrentes que aparecem</span><span>Plano de correções</span></div></div>'
        + '<div><span class="n">Semanas 2 a 4</span><h3>Correções técnicas</h3><p>Dados estruturados, llms.txt e páginas que respondem ao que os clientes perguntam.</p><div class="tg"><span>No site que já tem</span></div></div>'
        + '<div><span class="n">Semanas 2 a 4</span><h3>Autoridade</h3><p>Perfil Google, Bing, diretórios e os mesmos dados em todo o lado.</p><div class="tg"><span>Morada, telefone, horário</span></div></div>'
        + '<div><span class="n">Todos os meses</span><h3>Acompanhamento</h3><p>As mesmas perguntas medidas de novo, relatório mensal e novas melhorias.</p><div class="tg"><span>Relatório de uma página</span></div></div></div></section>'
        + f'<section class="sec dk" style="padding-top:1rem">{sh("03 · O que mudo no site", "Mexo no código<br>do seu site.", "Um assistente de IA não vê as fotografias nem as cores do site. Lê o código e os dados que lá estão, e é com base nisso que decide quem recomenda.")}'
        + f'<div class="code" data-tabs><div class="tabs"><button type="button" data-t>schema.json</button><button type="button" data-t>llms.txt</button><button type="button" data-t>robots.txt</button></div><pre class="cp" data-p>{C_SCHEMA}</pre><pre class="cp" data-p>{C_LLMS}</pre><pre class="cp" data-p>{C_ROBOTS}</pre></div>'
        + '<span class="ill">Exemplo ilustrativo com uma empresa fictícia.</span>'
        + '<div class="notes n4"><div><b>Dados estruturados</b><span>Dizem à IA, sem ambiguidade, o que a empresa faz, onde e para quem.</span></div><div><b>llms.txt</b><span>Um resumo do site em texto simples, pensado para modelos de linguagem.</span></div><div><b>Acesso dos robôs de IA</b><span>Garantir que o GPTBot, o PerplexityBot e outros conseguem ler o site.</span></div><div><b>Conteúdo que responde</b><span>Páginas e perguntas frequentes escritas para responder ao que os clientes perguntam.</span></div></div></section>'
        + f'<section class="sec">{sh("04 · Relatório mensal", "Todos os meses,<br>os mesmos números.", "Recebe uma página com as perguntas em que a empresa apareceu e o que fiz nesse mês. Os valores abaixo são um exemplo.")}'
        + f'<div class="rep" data-cards><div><h3>Perguntas em que a empresa é recomendada <small>Exemplo</small></h3><div class="bars">{bars}</div></div><div><h3>Por assistente <small>Mês 6</small></h3><div class="hb2">{hb}</div><p class="nt">As mesmas 30 perguntas medidas todos os meses.</p></div></div></section>'
        + f'<section class="sec tight">{sh("05 · O que inclui", "Começa sempre<br>pela auditoria.", "O que se faz a seguir depende do que ela mostrar. Sou eu que faço a auditoria, as correções e o relatório.")}'
        + '<div class="plans" data-cards><div><span class="n">01</span><h3>Auditoria de visibilidade</h3><small>Semana 1</small><ul><li>20 a 30 perguntas do seu setor e zona</li><li>4 assistentes de IA analisados</li><li>Concorrentes que aparecem no seu lugar</li><li>Plano com as correções prioritárias</li></ul><button type="button" class="pill w" data-open data-pre="Visibilidade em IA">Pedir verificação gratuita</button></div>'
        + '<div><span class="n">02</span><h3>Correções técnicas</h3><small>Semanas 2 a 4</small><ul><li>Dados estruturados e llms.txt</li><li>Acesso dos robôs de IA</li><li>Páginas e perguntas frequentes</li><li>Perfil Google, Bing e diretórios</li><li>Morada, telefone e horário iguais em todo o lado</li></ul></div>'
        + '<div><span class="n">03</span><h3>Acompanhamento mensal</h3><small>Todos os meses</small><ul><li>As mesmas perguntas medidas de novo, com relatório de uma página</li><li>Novo conteúdo quando aparecem perguntas que o site não responde</li><li>Ajustes quando os assistentes mudam a forma de escolher</li></ul></div></div></section>'
        + faq_sec('06 · Perguntas frequentes', 'O que me<br>perguntam mais.', FAQ_GEO)
        + rel_pd(others('visibilidade-ia')),
        contact=('Veja o que a IA responde sobre o seu setor.', 'Faço algumas perguntas do seu setor ao ChatGPT e ao Perplexity e envio-lhe as respostas tal como aparecem, com ou sem a sua empresa. A verificação é gratuita.'),
        foot=('Veja o que a IA<br>responde sobre o seu setor.', 'Pedir verificação gratuita', 'Visibilidade em IA'))

# ---------------------------------------------------------------- /avaliacoes-google
VIS_REV = '''<div class="hud" id="vis-rev" data-cycle="2200" data-n="4"><div class="hh"><span>Perfil Google</span><span class="live">avaliação nova</span></div>
<div class="gp"><div class="gh"><i>C</i><div><b>Clínica Exemplo</b><small>★★★★★<span>4,8</span></small></div></div>
<div class="rv" data-g="upto" data-off="1"><div class="ra"><small>Ana R. · ★★★★★ · agora</small>Atendimento impecável, voltarei.</div><div class="rb"><small>Resposta do proprietário</small>Obrigado, Ana! Ficamos contentes por ter gostado. Até à próxima.</div></div></div>
<div class="ft"><span>Exemplo ilustrativo</span><span>WhatsApp · SMS · email · QR code</span></div></div>'''

FAQ_REV = [('O Google deixa pedir avaliações?', 'Deixa, desde que o pedido seja feito a todos os clientes e sem nada em troca. É assim que o sistema está montado.'),
           ('Consegue apagar uma avaliação negativa?', 'Não. Só o Google remove avaliações, e apenas as que violam as regras dele, como spam, conteúdo ofensivo ou avaliações de quem nunca foi cliente. Nesses casos faço o pedido de remoção por si.'),
           ('As respostas vão parecer escritas por um robô?', 'Antes de arrancar, escolhemos juntos algumas respostas que já deu ou que gostaria de dar, e é a partir delas que a IA escreve. As primeiras semanas passam todas por si.'),
           ('A equipa tem de fazer alguma coisa?', 'Não. O pedido sai a partir das marcações, das faturas ou da lista de clientes. No balcão, basta o QR code à vista.'),
           ('Preciso de comprar algum programa?', 'Não precisa de instalar nada. Trabalho com o Perfil Google que já tem.'),
           ('Serve para que tipo de negócio?', 'Para negócios em que o cliente escolhe pelo Google Maps: clínicas, oficinas, restauração, estética, ginásios, serviços técnicos e lojas.')]

STAR = lambda n: f'<span style="font-size:1.1rem;letter-spacing:.05em;color:#E8A33D">{"★" * n}</span>'

def page_rev():
    dist = ''.join(f'<div><span>{s} ★</span><span class="t"><i style="width:{v / 71 * 100:.0f}%"></i></span><span>{v}</span></div>' for s, v in [(5, 71), (4, 10), (3, 3), (2, 1), (1, 2)])
    steps = [('Ligação ao perfil', 'Semana 1', ['Acesso ao Perfil Google', 'Ligação às marcações, às faturas ou a uma lista de clientes', 'QR code para o balcão ou para a fatura']),
             ('Mensagem e tom', 'Semana 1', ['Mensagem do pedido escrita consigo', 'Exemplos de resposta que servem de base à IA', 'Regras: o que nunca se diz numa resposta']),
             ('Primeiras semanas', 'Semanas 2 a 4', ['Todas as respostas passam por si antes de sair', 'Ajusto o tom até ficar como quer']),
             ('Todos os dias', 'Contínuo', ['Pedido enviado depois de cada serviço', 'Resposta a cada avaliação nova', 'Alerta imediato quando chega uma negativa']),
             ('Todos os meses', 'Ao fim do mês', ['Relatório de uma página', 'Comparação com concorrentes da zona', 'Pedido de remoção das avaliações que violam as regras do Google'])]
    tl = ''.join(f'<div><span class="n">{w}</span><h3>{t}</h3><div class="tg2">' + ''.join(f'<span>{x}</span>' for x in it) + '</div></div>' for t, w, it in steps)
    return dict(
        slug='avaliacoes-google', crumb='Avaliações Google', pre='Avaliações Google',
        title='Avaliações Google · Starmountain Flash',
        desc='Sistema que pede avaliação a cada cliente depois do serviço e responde a todas as avaliações do seu Perfil Google. Análise gratuita ao perfil.',
        service=dict(name='Gestão de avaliações Google', type='Pedido e resposta a avaliações no Perfil Google', offers=None),
        faq=FAQ_REV,
        body=hero('Avaliações Google', 'Quem gosta do serviço<br>esquece-se de avaliar.',
                  'Quem fica desagradado raramente se esquece. Monto um sistema que pede a avaliação a cada cliente logo depois do serviço e responde a todas as que chegam ao seu Perfil Google, boas e más.',
                  'Análise gratuita ao perfil', 'Avaliações Google', '#como', 'Como funciona', 'Avaliações Google', VIS_REV)
        + f'<section class="sec">{sh("01 · O que fica a funcionar", "Um perfil que<br>parece vivo.", "Quem compara duas empresas no Google Maps olha para as estrelas, para a data da última avaliação e para a forma como a empresa responde a quem se queixa.")}'
        + f'<div class="prof" data-cards><div class="pcard"><div class="top"><div><div class="big">4,8</div><div class="st">★★★★★</div><div class="cnt2">87 avaliações</div></div><div class="dist">{dist}</div></div>'
        + '<div class="rv2"><small>Ana R. · ★★★★★ · há 2 dias</small><p>Atendimento impecável, voltarei.</p></div><div class="own"><small>Resposta do proprietário</small>Obrigado, Ana! Ficamos contentes por ter gostado. Até à próxima.</div><span class="ill">Perfil fictício, exemplo ilustrativo.</span></div>'
        + '<div class="rflow"><div class="rn st"><b>Serviço concluído</b></div>'
        + '<div class="rn"><span class="k">01</span><b>Pedido automático</b><small>WhatsApp, SMS ou email, com o link direto para avaliar</small></div>'
        + '<div class="rn"><span class="k">02</span><b>Avaliação nova no Perfil Google</b></div>'
        + '<div class="rbr"><div class="rn ok"><span class="k">Positiva</span><b>Resposta no tom da empresa</b><small>Pode sair sozinha</small></div><div class="rn bad"><span class="k">Negativa</span><b>Alerta com rascunho de resposta</b><small>Nada é publicado sem a sua aprovação</small></div></div>'
        + '<div class="rn"><span class="k">03</span><b>Relatório mensal</b><small>Pedidos enviados, avaliações novas e tempo de resposta, numa página</small></div>'
        + '<div class="rn res"><b>Um perfil com avaliações recentes e todas respondidas</b></div></div></div></section>'
        + '<section class="method" style="border-radius:0;padding-top:2rem"><div class="hh"><span class="ey">02 · Para quem é</span><h2 data-split="1" style="margin-top:1rem">Se uma destas<br>lhe soa familiar.</h2></div><div class="mgrid mgrid3" data-cards>'
        + mc('01', 'Perfil parado', 'Sem avaliações recentes', 'A última avaliação tem meses e o perfil parece parado, mesmo com clientes todos os dias.', icon=STAR(1))
        + mc('02', 'Sem tempo', 'Avaliações sem resposta', 'Há avaliações boas e más à espera de resposta, porque nunca há tempo para isso.', icon=STAR(2))
        + mc('03', 'Google Maps', 'Muitos clientes, pouco tempo', 'Clínicas, oficinas, restauração, estética, ginásios: negócios que o cliente escolhe pelo Google Maps.', icon=STAR(3))
        + '</div></section>'
        + f'<section class="sec dk" id="como">{sh("03 · Como funciona", "Cinco passos,<br>e depois corre sozinho.")}'
        + '<div class="rules2">' + ''.join(f'<span>{x}</span>' for x in ['Pedido a todos os clientes', 'Nada em troca de estrelas', 'Nenhuma avaliação escrita por mim', 'Respostas no tom da empresa', 'Negativas só com aprovação']) + '</div>'
        + f'<div class="tline" data-cards>{tl}</div>'
        + '<div class="minirep"><div><b>64</b><span>pedidos enviados</span></div><div><b>18</b><span>avaliações novas</span></div><div><b>18/18</b><span>respondidas</span></div><small>Relatório · mês 6 · exemplo</small></div></section>'
        + faq_sec('04 · Perguntas frequentes', 'O que me<br>perguntam mais.', FAQ_REV)
        + rel_pd(others('avaliacoes-google')),
        contact=('Como está o seu perfil hoje?', 'Vejo quantas avaliações tem sem resposta, há quanto tempo chegou a última e como fica ao lado de dois concorrentes da sua zona. A análise é gratuita.'),
        foot=('Como está o seu<br>Perfil Google hoje?', 'Pedir análise gratuita', 'Avaliações Google'))
