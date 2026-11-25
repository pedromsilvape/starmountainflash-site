# Captação: /analise-gratuita e /analise-gratuita/obrigado (landing de anúncios, noindex, sem navegação)
from pages import sh, faq_sec, U

def header(home):
    return (f'<header class="lp on"><a href="{home}" class="shell brand" aria-label="Starmountain Flash">%%LOGO_W%%</a>'
            '<a href="#pedido" class="pill w lp-cta">Quero a minha análise <span class="orb">↓</span></a></header>')

def form(id_, go):
    return (f'<form class="lpf" id="{id_}" data-go="{go}" novalidate><span class="ey">Peça a sua análise gratuita</span>'
            '<label class="fl"><input name="website" type="text" required placeholder=" " inputmode="url"><span>Link do seu site (www.suaempresa.pt)</span></label>'
            '<label class="fl"><input name="nome" required placeholder=" " autocomplete="name"><span>Nome</span></label>'
            '<label class="fl"><input name="email" type="email" required placeholder=" " autocomplete="email"><span>Email</span></label>'
            '<button type="submit" class="pill d">Quero a minha análise gratuita ↗</button>'
            f'<p class="lpn">Sem custo e sem compromisso. Os dados servem só para preparar e enviar a análise. <a href="{U}/privacidade" target="_blank" rel="noopener">Privacidade</a>.</p></form>')

REV = [('JR', 'João Rebordão', 'Trustpilot', 'Recomendo vivamente', 'Impecavelmente bem feito o trabalho, sem falhas, com melhoramentos ao que se pede e se torna necessário. Recomendo vivamente! Profissional de excelência!'),
       ('HP', 'Henrique Pereira', 'Trustpilot', 'Excelente experiência do início ao fim!', 'Fiquei muito satisfeito com o serviço da Star Mountain Flash. Todo o processo foi simples, rápido e profissional, desde o primeiro contacto até à conclusão do serviço.'),
       ('DB', 'Débora Baêta', 'Google', '', 'Uma experiência muito positiva com a Starmountain Flash. Destaco o profissionalismo, a simpatia e a qualidade do serviço prestado. Recomendo!')]

FAQ = [('É mesmo gratuita?', 'Sim. Não há custo nem dados de pagamento pedidos em nenhum momento.'),
       ('Fico obrigado a contratar?', 'Não. O relatório indica o que pode corrigir sozinho e o que precisa de um profissional, seja eu ou outro.'),
       ('Quanto tempo demora?', 'Até 3 dias úteis depois do pedido.'),
       ('É um relatório automático?', 'Não. Cada afirmação é verificada no seu site e o relatório é revisto por mim antes de seguir.'),
       ('O que fazem com os meus dados?', 'São usados apenas para preparar a análise e para lha enviar.')]

def foot(home):
    return (f'<div class="lpft"><div>%%LOGO_W_SM%%<span>© 2026 Starmountain Flash · Covilhã · Fornecedor digital da UBI</span></div>'
            f'<nav><a href="{home}">Conhecer a Starmountain Flash</a><a href="{U}/privacidade" target="_blank" rel="noopener">Privacidade</a><a href="{U}/termos" target="_blank" rel="noopener">Termos</a><a href="https://www.livroreclamacoes.pt" target="_blank" rel="noopener">Livro de Reclamações</a></nav></div>'
            '')

def page_lp():
    H, GO = '../index.html', 'obrigado/index.html'
    av = ''.join(f'<i>{a}</i>' for a, *_ in REV)
    alerts = ''.join(f'<div class="mc"><div class="mtop"><span class="mn">{n}</span></div><h3>{t}</h3><p>{d}</p></div>' for n, t, d in [
        ('01', 'Tem visitas, mas poucos contactos', 'As pessoas entram no site e saem sem ligar, escrever ou pedir orçamento.'),
        ('02', 'Não aparece no Google', 'Quem procura o seu serviço na sua zona encontra primeiro a concorrência.'),
        ('03', 'No telemóvel custa a usar', 'O site demora a abrir ou obriga a fazer zoom para ler e encontrar o contacto.')])
    rec = [('01', 'Nota por área', 'Uma nota global e cinco notas parciais, para saber onde o site está forte e onde falha.', ['Mensagem e primeira impressão', 'Contacto e conversão', 'Telemóvel e velocidade', 'Confiança e prova', 'Visibilidade no Google']),
           ('02', 'Onde perde clientes', 'Os três problemas com mais impacto, mostrados em capturas do seu próprio site.', ['Marcações feitas à mão', 'Análise na versão telemóvel', 'Começa pelo que já funciona']),
           ('03', 'Números explicados', 'Os valores técnicos são traduzidos, para os perceber sem ser da área.', ['Velocidade medida no PageSpeed', 'Comparação com dois concorrentes', 'Antes e depois do título']),
           ('04', 'Como resolver', 'A correção para cada problema, com o esforço que cada uma exige.', ['O que pode fazer já, sozinho', 'O que precisa de um profissional', 'Sem obrigação de contratar'])]
    rech = ''.join(f'<div><span class="n">{n}</span><h3>{t}</h3><p>{d}</p><ul>' + ''.join(f'<li>{x}</li>' for x in it) + '</ul></div>' for n, t, d, it in rec)
    steps = [('01', 'Envie o link', 'Nome, email e site.', 'Preencha o formulário. É tudo o que preciso para começar.'),
             ('02', 'Eu analiso', 'Vejo o seu site no telemóvel.', 'Meço a velocidade, comparo com dois concorrentes locais e escolho os três problemas que mais clientes lhe estão a custar.'),
             ('03', 'Recebe o PDF', 'Em até 3 dias úteis.', 'Chega ao seu email. Depois decide: corrige sozinho, pede-me ajuda ou não faz nada.')]
    sth = ''.join(f'<div><span class="n">{n}</span><h3>{t}</h3><p><b>{a}</b> {d}</p></div>' for n, t, a, d in steps)
    revh = ''.join(f'<div class="tc{" dk" if i == 1 else ""}"><div class="th"><span class="stars">★★★★★</span><span class="src">{s}</span></div>' + (f'<h3>{t}</h3>' if t else '') + f'<p>“{q}”</p><div class="who"><i>{a}</i><div><b>{n}</b><span>Avaliação no {s}</span></div></div></div>' for i, (a, n, s, t, q) in enumerate(REV))
    cta = '<div class="lpc"><a href="#pedido" class="pill d">Quero a minha análise gratuita ↓</a><span>Gratuita. Recebe o relatório em até 3 dias úteis.</span></div>'
    body = (header(H) + '<main id="top" class="subp lpm">'
        + '<section id="hero" class="sub lp"><div class="clip"><canvas data-grad="#253745,#A9C8E8,4.3"></canvas><div class="ui"><div class="hb lph">'
        + '<div class="tx"><span class="mono eb" data-hi>Análise gratuita · Sem compromisso</span><h1 data-split="hero" data-ramp="hero">Descubra onde o seu site<br>está a perder clientes.</h1>'
        + '<p class="lead" data-hi>Envie o link do seu site e receba, em até 3 dias úteis, um relatório em PDF com o que deve corrigir primeiro.</p>'
        + '<ul class="lpb" data-hi><li>Os 3 problemas que mais afastam clientes, assinalados no seu site</li><li>Nota de 0 a 10 em cinco áreas, com os números explicados</li><li>A correção de cada problema e o que pode resolver sozinho</li></ul>'
        + f'<div class="avs" data-hi><span class="av3">{av}</span><span>Avaliações reais de clientes no <a href="https://www.trustpilot.com/review/starmountainflash.pt" target="_blank" rel="noopener">Trustpilot</a> e no <a href="https://www.google.com/search?kgmid=/g/11nvdc1v3n" target="_blank" rel="noopener">Google</a></span></div></div>'
        + f'<div class="hud lpfw" id="pedido" data-hi>{form("f1", GO)}</div></div></div></div></section>'
        + f'<section class="method" style="border-radius:0;padding-top:5.5rem"><div class="hh"><span class="ey">Sinais de alerta</span><h2 data-split="1" style="margin-top:1rem">Reconhece algum destes?</h2><p class="tlead" style="margin:1.4rem auto 0;text-align:center">Então vale a pena pedir a análise.</p></div><div class="mgrid mgrid3" data-cards>{alerts}</div></section>'
        + f'<section class="sec dk">{sh("O que recebe", "Um relatório em PDF,<br>preparado para o seu site.", "Cada afirmação é verificada no seu site e o relatório é revisto por mim antes de seguir.")}<div class="rec4" data-cards>{rech}</div>{cta.replace("pill d", "pill w")}</section>'
        + f'<section class="sec">{sh("Como funciona", "Três passos.<br>Menos de um minuto do seu tempo.")}<div class="tline t3" data-cards>{sth}</div>{cta}</section>'
        + f'<section class="sec tight">{sh("Clientes", "O que dizem os clientes.")}<div class="tgrid" data-cards>{revh}</div></section>'
        + faq_sec('Perguntas frequentes', 'Antes de<br>pedir a análise.', FAQ)
        + '<section class="sec dk lpend"><div class="lpe"><div><span class="ey">Última chamada</span><h2 data-split="1" style="margin-top:1rem">O seu site está a trabalhar para si?</h2><p class="lead2">Descubra em 3 dias úteis.</p>'
        + '<div class="ticks"><span>Gratuita e sem compromisso</span><span>Preparada para o seu site e revista por mim</span><span>Relatório em PDF no seu email</span></div></div>'
        + f'<div class="hud lpfw">{form("f2", GO)}</div></div></section></main>' + foot(H))
    return dict(slug='analise-gratuita', crumb='Análise gratuita', kind='landing', noindex=True, faq=FAQ,
                title='Análise gratuita ao seu site · Starmountain Flash', desc='Envie o link do seu site e receba, em até 3 dias úteis, um relatório em PDF com o que deve corrigir primeiro. Gratuita e sem compromisso.', raw=body)

def page_ok():
    H = '../../index.html'
    body = (f'<header class="lp on"><a href="{H}" class="shell brand" aria-label="Starmountain Flash">%%LOGO_W%%</a></header><main id="top" class="subp lpm">'
            '<section id="hero" class="sub lp ok"><div class="clip"><canvas data-grad="#253745,#A9C8E8,6.3"></canvas><div class="ui"><div class="okw">'
            '<span class="okc2" data-hi>✓</span><span class="mono eb" data-hi>Pedido recebido</span><h1 data-split="hero" data-ramp="hero">Obrigado.<br>A sua análise já está na minha lista.</h1>'
            '<p class="lead" data-hi>Recebe o relatório em PDF no seu email em até 3 dias úteis.</p>'
            '<ol class="oks" data-hi><li><span>01</span>Vejo o seu site no telemóvel e meço a velocidade</li><li><span>02</span>Comparo-o com dois concorrentes locais</li><li><span>03</span>Envio-lhe o relatório, revisto por mim</li></ol>'
            f'<p class="okn" data-hi>Se não o vir na caixa de entrada, confirme a pasta de spam.</p><div class="row" data-hi><a href="{H}" class="pill w">Conhecer a Starmountain Flash</a></div></div></div></div></section></main>'
            + foot(H).split('<div class="ckb">')[0])
    return dict(slug='analise-gratuita/obrigado', crumb='Pedido recebido', kind='landing', noindex=True, faq=[],
                title='Pedido recebido · Starmountain Flash', desc='O seu pedido de análise gratuita foi recebido.', raw=body)

def pages(): return [page_lp(), page_ok()]
