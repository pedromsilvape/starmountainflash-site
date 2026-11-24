# Subpage content (bloco Automações). Copy based on the live site, reviewed with the anti-IA rule.
U = 'https://starmountainflash.pt'

def faq_html(items):
    return '\n'.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items)

def strip_tags(s):
    import re
    return re.sub(r'<[^>]+>', '', s)

def hero(eb, h1, lead, cta_label, cta_pre, sec_link, sec_label, crumb, vis, mid=True, cls='sub'):
    return f'''<section id="hero" class="{cls}"><div class="clip"><canvas data-grad="#253745,#A9C8E8,{len(crumb) % 9}.3"></canvas>{'<canvas id="burst" data-x="1.9" data-s=".78"></canvas>' if cls in ('sub', 'sub sm') else ''}
<div class="ui"><span class="mono eb" data-hi>{eb}</span>
<h1 data-split="hero" data-ramp="hero">{h1}</h1>
<div class="hb"><div class="tx"><p class="lead" data-hi>{lead}</p>
<div class="row" data-hi><button type="button" class="pill w" data-open data-pre="{cta_pre}">{cta_label}</button><a href="{sec_link}" class="u">{sec_label}</a></div></div>
{vis.replace('<div class="hud"', '<div class="hud" data-hi', 1)}</div></div>
<nav class="crumbs" aria-label="Breadcrumb"><a href="%%HOME%%">Início</a><i>/</i>{(f'<a href="%%HOME%%{mid[1]}">{mid[0]}</a><i>/</i>' if isinstance(mid, tuple) else '<a href="%%HOME%%#servicos">Serviços</a><i>/</i>') if mid else ''}<span>{crumb}</span></nav></div></section>'''

def sh(ey, h2, sl=''):
    p = f'<p class="sl">{sl}</p>' if sl else ''
    return f'<div class="sh"><div><span class="ey">{ey}</span><h2 data-split="1">{h2}</h2></div>{p}</div>'

def faq_sec(ey, h2, items):
    return f'<section class="faq sec" id="faq"><div><span class="ey">{ey}</span><h2 data-split="1" style="margin-top:1rem">{h2}</h2></div><div>{faq_html(items)}</div></section>'

def rel_sec(items, h2='Outros serviços<br>de automação.'):
    rows = ''.join(f'<a class="si" href="%%L:{slug}%%"><div><b>{t}</b><small>{d}</small></div><span class="go">%%ARR%%</span></a>' for k, slug, t, d in items)
    return f'<section class="sec tight"><div class="rel"><div><span class="ey">Automações com IA</span><h2 data-split="1" style="margin-top:1rem">{h2}</h2></div><div class="grp ai"><div class="slist">{rows}</div></div></div></section>'

def mc(n, tag, h3, p, lis=(), icon=''):
    ul = '<ul>' + ''.join(f'<li>{x}</li>' for x in lis) + '</ul>' if lis else ''
    return f'<div class="mc"><div class="mtop"><span class="mn">{n}</span><span class="mic">{icon}</span></div><span class="n">{tag}</span><h3>{h3}</h3><p>{p}</p>{ul}</div>'

IC_CHAT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/><path d="M8 11h8M8 14h5"/></svg>'
IC_BUILD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="m8 9-4 3 4 3M16 9l4 3-4 3M13.5 6l-3 12"/></svg>'
IC_EYE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>'
IC_LOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>'
IC_ROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h10"/></svg>'
IC_CAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>'
IC_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg>'
IC_FILE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H6v18h12V7Z"/><path d="M14 3v4h4"/></svg>'
IC_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'
IC_USER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>'

# ---------------------------------------------------------------- /automacoes
VIS_AUTO = '''<div class="hud" id="vis-auto"><div class="hh"><span>Faturas de fornecedores → Excel</span><span class="live">a correr</span></div>
<div class="bd"><div class="doc"><span class="t">PDF · FATURA</span><dl><div><dt>Fornecedor</dt><dd class="vf">Metalúrgica Silva</dd></div><div><dt>Data</dt><dd class="vd">12/11</dd></div><div><dt>Total</dt><dd class="vt">1 284,50 €</dd></div></dl></div>
<div class="xl"><div class="xh"><span>Fornecedor</span><span>Data</span><span>Total</span></div>
<div class="xr" data-f="Metalúrgica Silva" data-d="12/11" data-t="1 284,50 €"><span>Metalúrgica Silva</span><span>12/11</span><span>1 284,50 €</span></div>
<div class="xr" data-f="Papelaria Central" data-d="13/11" data-t="86,20 €"><span>Papelaria Central</span><span>13/11</span><span>86,20 €</span></div>
<div class="xr" data-f="Transportes Beira" data-d="14/11" data-t="412,00 €"><span>Transportes Beira</span><span>14/11</span><span>412,00 €</span></div>
<div class="xr" data-f="Gráfica Estrela" data-d="15/11" data-t="238,75 €"><span>Gráfica Estrela</span><span>15/11</span><span>238,75 €</span></div>
<div class="xr" data-f="Metalúrgica Silva" data-d="18/11" data-t="967,30 €"><span>Metalúrgica Silva</span><span>18/11</span><span>967,30 €</span></div></div></div>
<div class="ft"><span>Exemplo ilustrativo</span><div class="cnt" style="text-align:right"><b>0</b><span>faturas lançadas sem copiar e colar</span></div></div></div>'''

EX = [('Atendimento', 'Perguntas repetidas respondidas', 'Responde à mão às mesmas perguntas sobre horários, preços e disponibilidade.', 'As perguntas frequentes têm resposta imediata. Só as outras chegam até si.'),
      ('Pedidos', 'Contactos que não se perdem', 'Os pedidos chegam por email, formulário e telefone, e alguns ficam esquecidos.', 'Cada pedido entra no CRM com origem e data, e recebe resposta automática.'),
      ('Documentos', 'Faturas sem copiar e colar', 'Os dados de cada fatura são copiados um a um para o Excel.', 'Os documentos são lidos e os dados entram na folha sozinhos.'),
      ('Relatórios', 'O relatório de segunda-feira', 'Todas as semanas alguém junta números de várias folhas para montar o relatório.', 'O relatório é gerado e enviado sozinho, sempre à mesma hora.'),
      ('Agenda', 'Menos faltas às marcações', 'Os lembretes aos clientes são enviados à mão, quando há tempo.', 'Cada cliente recebe confirmação e lembrete automáticos.'),
      ('Integrações', 'Ferramentas que falam entre si', 'A mesma informação é escrita em três sítios diferentes.', 'Escreve uma vez e as outras ferramentas atualizam-se sozinhas.'),
      ('Clientes novos', 'Entrada de clientes automática', 'Cada cliente novo obriga a criar pastas, registos e tarefas à mão.', 'Tudo é criado no momento em que o cliente entra.'),
      ('Portais', 'Portais sem integração', 'Documentos descarregados um a um de portais que não se ligam a nada.', 'Um robô entra no portal, descarrega e organiza os documentos por si.')]

def ba(items):
    tabs = ''.join(f'<button type="button" class="tb" data-t><small>{c}</small><b>{t}</b></button>' for c, t, _, _ in items)
    pans = ''.join(f'<div class="pp" data-p><span class="ey" style="color:var(--ac)">{c}</span><h3>{t}</h3><div class="ab"><div><span>Antes</span><p>{a}</p></div><div><span>Depois</span><p>{d}</p></div></div></div>' for c, t, a, d in items)
    return f'<div class="ba" data-tabs="auto"><div class="tl">{tabs}</div><div class="pw">{pans}</div></div>'

TOOLS = ['Google Workspace', 'Microsoft 365', 'Gmail e Outlook', 'Excel e Google Sheets', 'HubSpot', 'Pipedrive', 'TOConline', 'Moloni', 'InvoiceXpress', 'Notion', 'Trello', 'Brevo', 'n8n e Make']

FAQ_AUTO = [('Preciso de ter site para automatizar?', 'Não. As automações funcionam com as ferramentas que já usa: email, folhas de cálculo, CRM, programas de gestão. O site é só uma das possíveis ligações.'),
            ('Quanto custa uma automação?', 'Uma automação simples custa entre 800 € e 1.200 €; com IA ou dois a três fluxos, entre 1.200 € e 2.500 €; um sistema à medida começa nos 3.500 €. O valor exato fica na proposta, depois do levantamento. Explico o que faz variar o preço em <a href="' + U + '/blog/quanto-custa-uma-automacao-com-ia" style="text-decoration:underline;text-underline-offset:3px">quanto custa uma automação com IA</a>.'),
            ('Os meus dados ficam seguros?', 'As automações usam as contas e ferramentas da empresa, com acesso apenas ao que é necessário para funcionarem.'),
            ('E se alguma coisa falhar?', 'As automações são testadas com casos reais antes de entrarem em funcionamento. A forma de acompanhamento e ajustes fica definida na proposta.'),
            ('Onde entra a inteligência artificial?', 'Nas tarefas que envolvem texto: classificar emails, resumir documentos, extrair dados ou preparar respostas. Quando é importante, há sempre revisão humana antes de sair alguma coisa.')]

def page_auto(chip):
    tools = ''.join(f'<span>{chip(t)}{t}</span>' for t in TOOLS)
    return dict(
        slug='automacoes', crumb='Automações à medida', pre='Automações à medida',
        title='Automações com IA à medida · Starmountain Flash',
        desc='Automações com IA para empresas: emails, documentos, relatórios, CRM e integrações entre ferramentas. O trabalho repetitivo passa a fazer-se sozinho.',
        service=dict(name='Automações com IA à medida', type='Automação de processos com IA', offers=(800, 3500)),
        faq=FAQ_AUTO,
        body=hero('Automações à medida', 'O trabalho repetitivo<br>passa a fazer-se sozinho.',
                  'Processos que hoje são feitos à mão, todas as semanas, passam a correr sozinhos, ligados às ferramentas que a empresa já usa. Com ou sem site.',
                  'Falar sobre um processo', 'Automações à medida', '#exemplos', 'Ver exemplos', 'Automações à medida', VIS_AUTO)
        + '<section class="marq"><div class="mrow" data-dir="left" data-speed="0.005"><div>%%M1%%</div></div><div class="mrow" data-dir="right" data-speed="0.0038"><div>%%M2%%</div></div></section>'
        + f'<section class="sec" id="exemplos">{sh("01 · Exemplos", "O que pode ser automatizado,<br>antes e depois.", "Se alguém na empresa passa horas por semana a copiar dados de um lado para o outro, a responder às mesmas perguntas ou a preencher folhas à mão, há uma boa probabilidade de esse trabalho poder ser feito sozinho.")}{ba(EX)}<p class="foot-note">Cada automação é desenhada à volta do seu processo e das ferramentas que já usa.</p></section>'
        + f'<section class="method" style="border-radius:0;padding-top:2rem"><div class="hh"><span class="ey">02 · Como funciona</span><h2 data-split="1" style="margin-top:1rem">Primeiro perceber,<br>depois automatizar.</h2></div><div class="mgrid mgrid3" data-cards>'
        + mc('01', 'Com o Método StarMap', 'Levantamento', 'Mapeio as tarefas repetitivas, quanto tempo ocupam e quem as faz. Fica claro o que compensa automatizar.', icon=IC_EYE)
        + mc('02', 'Com as suas ferramentas', 'Construção', 'Desenvolvo a automação com as suas ferramentas e testo-a com casos reais antes de entrar em funcionamento.', icon=IC_BUILD)
        + mc('03', 'Primeiras semanas', 'Acompanhamento', 'Acompanho as primeiras semanas e ajusto o que for preciso. A forma de acompanhamento fica na proposta.', icon=IC_CHAT)
        + '</div></section>'
        + f'<section class="sec">{sh("03 · Tecnologia", "Com o que já usa,<br>ou construído de raiz.")}<div class="tech" data-cards>'
        + f'<div class="tk"><span class="tag">Integração</span><h3>As ferramentas da empresa</h3><p>Sempre que possível, a automação liga-se ao que a empresa já usa, sem mudar hábitos nem pagar software novo.</p><div class="chips">{tools}</div></div>'
        + '<div class="tk dk"><span class="tag">Framework próprio</span><h3>Construído à medida</h3><p>Quando não existe integração, ou o processo é demasiado específico, desenvolvo a automação de raiz, com código próprio e sem depender de plataformas intermédias.</p>'
        + '<div class="kv"><div><b>Robôs web</b><span>Node.js e Playwright, para operar portais sem ligação oficial</span></div><div><b>Dados</b><span>Supabase, para guardar e organizar a informação</span></div><div><b>IA</b><span>Modelos de linguagem para ler, classificar e resumir</span></div><div><b>Ligações</b><span>APIs e webhooks entre sistemas</span></div></div></div></div>'
        + '<div class="callout"><span class="big">5 min</span><div><h3>Nem tudo deve ser automatizado.</h3><p>Se uma tarefa leva cinco minutos por mês, não compensa. No levantamento digo-lhe com franqueza o que vale a pena e o que não vale.</p></div></div></section>'
        + faq_sec('04 · Perguntas frequentes', 'Sobre automações,<br>em poucas palavras.', FAQ_AUTO)
        + rel_sec([('b.1', 'starmap', 'Método StarMap', 'Uma semana de registo das tarefas da equipa e um relatório com o que automatizar primeiro.'),
                   ('b.3', 'assistente-interno', 'Assistente interno', 'Para empresas de maior dimensão: um assistente de IA privado que responde com base nos documentos da empresa.')]),
        contact=('Que tarefa gostava de nunca mais fazer?', 'Conte-me em duas ou três linhas. Respondo com o que faria no seu caso e se compensa automatizar.'),
        foot=('Comece pelo<br>Método StarMap.', 'Pedir o Método StarMap', 'Método StarMap'))

# ---------------------------------------------------------------- /starmap
def week():
    # minutes per day for 3 tasks (illustrative): encomendas, faturas, orçamentos
    d = [(85, 60, 40), (75, 0, 45), (90, 115, 30), (70, 0, 50), (80, 120, 35)]
    mx = max(sum(x) for x in d)
    cols = ''.join('<div class="wb">' + ''.join(f'<i class="{c}" style="height:{v / mx * 100:.1f}%"></i>' for c, v in zip('cba', reversed(x)) if v) + '</div>' for x in d)
    return cols

VIS_STAR = f'''<div class="hud" id="vis-star"><div class="hh"><span>Semana de registo</span><span class="live">a registar</span></div>
<div class="wk">{week()}</div><div class="dl"><span>Seg</span><span>Ter</span><span>Qua</span><span>Qui</span><span>Sex</span></div>
<div class="lg"><span style="--c:var(--ac)">Encomendas do email para o Excel</span><span style="--c:#4A6F94">Faturas de fornecedores</span><span style="--c:rgba(255,255,255,.28)">Pedidos de orçamento</span></div>
<div class="ft"><span>Exemplo ilustrativo de uma<br>equipa administrativa.</span><div class="tot" style="text-align:right"><b data-m="400">6h40</b><span>em encomendas, em 5 dias</span></div></div></div>'''

FAQ_STAR = [('A equipa vai perder muito tempo a registar?', 'Cada registo é uma linha: o que fez, quanto tempo levou e com que ferramenta. Ao longo do dia, são poucos minutos no total.'),
            ('Porquê uma semana e não um dia?', 'Num só dia escapam as tarefas que acontecem duas ou três vezes por semana, como faturas, encomendas a fornecedores ou relatórios.'),
            ('Quem vê os registos?', 'A sua empresa e eu. A plataforma separa os dados de cada empresa e o acesso é feito com email e palavra-passe.'),
            ('Depois do diagnóstico, tenho de automatizar consigo?', 'O relatório diz o que faz sentido automatizar e porquê. A decisão sobre o que fazer a seguir é sua.'),
            ('Para que empresas faz sentido?', 'Para equipas com trabalho administrativo que se repete todas as semanas: encomendas, faturas, marcações, orçamentos, relatórios.')]

def page_star():
    rows = [('1', 'Encomendas do email para o Excel', 'Outlook, Excel', '6h40', 'p1', 'Automatizar primeiro'),
            ('2', 'Lançamento de faturas de fornecedores', 'PDF, faturação', '4h55', 'p1', 'Automatizar primeiro'),
            ('3', 'Respostas a pedidos de orçamento', 'Email', '3h20', 'p2', 'A seguir'),
            ('4', 'Marcação de visitas', 'Agenda em papel', '1h45', 'p3', 'Rever processo'),
            ('5', 'Relatório semanal à direção', 'Excel', '1h10', 'p4', 'Manter')]
    tb = ''.join(f'<tr><td>{a}</td><td>{b}<small>{c}</small></td><td class="h">{d}</td><td><span class="pr {e}">{f}</span></td></tr>' for a, b, c, d, e, f in rows)
    return dict(
        slug='starmap', crumb='Método StarMap', pre='Método StarMap',
        title='Diagnóstico de automação: Método StarMap · Starmountain Flash',
        desc='Diagnóstico de automação: uma semana de registo das tarefas da equipa numa plataforma própria, relatório e reunião com o que automatizar primeiro.',
        service=dict(name='Método StarMap', type='Diagnóstico de automação', offers=None),
        faq=FAQ_STAR,
        body=hero('Diagnóstico de automação · Método StarMap', 'Antes de automatizar<br>veja para onde<br>vai o seu tempo.',
                  'Durante uma semana, a sua equipa regista o que faz numa plataforma minha. No fim, mostro-lhe quantas horas vão para tarefas que se repetem e quais faz sentido automatizar primeiro.',
                  'Pedir o Método StarMap', 'Método StarMap', '#como', 'Como funciona', 'Método StarMap', VIS_STAR)
        + f'<section class="sec">{sh("01 · Porquê registar", "Estimar dá um número.<br>Registar dá outro.", "Se perguntar a alguém quanto tempo passa a copiar encomendas do email para o Excel, a resposta é um palpite. Ao fim de uma semana de registo, sabe-se de quantas encomendas se trata e quantos minutos leva cada uma.")}'
        + '<div class="cmp" data-cards><div class="qt"><span class="ey">Estimativa</span><blockquote>“As encomendas? Meia hora por dia, no máximo.”</blockquote><small>Dito numa reunião · exemplo ilustrativo</small></div>'
        + '<div class="fnd"><span class="ey" style="color:var(--ac)">O que a semana de registo encontra</span><div class="fl2">'
        + '<div><span class="ty">XLSX</span><b>Encomendas_2024_FINAL(2).xlsx</b><small>Atualizado à mão, todos os dias</small></div>'
        + '<div><span class="ty">EMAIL</span><b>FW: FW: encomenda urgente</b><small>Copiado para o Excel às 16:45</small></div>'
        + '<div><span class="ty">PDF</span><b>fatura_fornecedor_0381.pdf</b><small>Lançada à mão no programa</small></div>'
        + '<div><span class="ty">AGENDA</span><b>Marcar visita · ligar de volta</b><small>Agenda em papel</small></div></div>'
        + '<div class="sum"><span>Encomendas, registado em 5 dias</span><b>6h40</b></div><span class="ill">Exemplo ilustrativo</span></div></div></section>'
        + '<section class="method" style="border-radius:0;padding-top:2rem"><div class="hh"><span class="ey">02 · A plataforma</span><h2 data-split="1" style="margin-top:1rem">Uma linha por tarefa,<br>durante uma semana.</h2><p class="tlead" style="margin:1.4rem auto 0;text-align:center">A equipa regista e eu cruzo os registos com as ferramentas que a empresa já usa. Do outro lado sai uma lista do que automatizar e por que ordem.</p></div><div class="mgrid" data-cards>'
        + mc('01', 'Registo', 'Registo numa linha', 'O que fez, quanto tempo levou e com que ferramenta. Leva poucos segundos.', icon=IC_ROW)
        + mc('02', 'Acesso', 'Dados separados', 'Entrada com email e palavra-passe. Cada empresa só vê os seus registos.', icon=IC_LOCK)
        + mc('03', 'Duração', 'Uma semana inteira', 'Num só dia escapam as tarefas que acontecem duas ou três vezes por semana.', icon=IC_CAL)
        + mc('04', 'Dia 1', 'Reunião inicial', 'Para conhecer a história da empresa e a equipa antes de olhar para os números.', icon=IC_CHAT)
        + '</div></section>'
        + f'<section class="sec dk" id="como">{sh("03 · Como funciona", "Três momentos,<br>uma semana no meio.")}<p class="tlead">Na primeira reunião quero conhecer a história da empresa e ouvir da sua boca o que está a correr mal, antes de olhar para números.</p>'
        + '<div class="tline" data-cards>'
        + '<div><span class="n">Dia 1</span><h3>Reunião inicial</h3><p>História da empresa, quem faz o quê e o que mais pesa no dia a dia.</p><div class="tg"><span>história</span><span>equipa</span><span>dores</span></div></div>'
        + '<div><span class="n">Dia 1</span><h3>Acessos à plataforma</h3><p>Cada pessoa recebe um acesso e explico como registar. Leva poucos minutos.</p><div class="tg"><span>email e palavra-passe</span></div></div>'
        + '<div><span class="n">5 dias úteis</span><h3>Semana de registo</h3><p>Cinco dias úteis de registos, com o levantamento das ferramentas e ficheiros em uso. Durante a semana acompanho os registos a entrar e tiro dúvidas à equipa.</p><div class="tg"><span>Seg</span><span>Ter</span><span>Qua</span><span>Qui</span><span>Sex</span></div></div>'
        + '<div><span class="n">Depois</span><h3>Análise</h3><p>Agrupo os registos por tarefa, pessoa e ferramenta e vejo o que se repete.</p></div>'
        + '<div><span class="n">No fim</span><h3>Relatório e reunião</h3><p>Onde vai o tempo, o que automatizar primeiro e porquê, apresentado em reunião.</p></div></div></section>'
        + f'<section class="sec">{sh("04 · O que recebe", "Onde vai o tempo,<br>por ordem.", "No fim da semana, os registos são agrupados e ordenados pelo tempo que ocupam. Os valores abaixo são um exemplo.")}'
        + f'<div class="tblw"><table class="tbl"><thead><tr><th>#</th><th>Tarefa que se repete</th><th>Horas/semana</th><th>Prioridade</th></tr></thead><tbody>{tb}</tbody></table></div>'
        + '<div class="notes"><div><b>Plataforma própria</b><span>Construída por mim para estes diagnósticos, em <a href="https://diagnostico.starmountainflash.pt" target="_blank" rel="noopener">diagnostico.starmountainflash.pt</a>.</span></div><div><b>Relatório e reunião</b><span>Recebe o relatório e uma reunião de apresentação, para poder perguntar tudo antes de decidir.</span></div><div><b>A decisão é sua</b><span>O relatório diz o que faz sentido automatizar e porquê. Não fica obrigado a avançar comigo.</span></div></div></section>'
        + faq_sec('05 · Perguntas frequentes', 'O que me<br>perguntam mais.', FAQ_STAR)
        + rel_sec([('b.2', 'automacoes', 'Automações à medida', 'Emails, faturas, relatórios, marcações e CRM a correr sozinhos.'),
                   ('b.3', 'assistente-interno', 'Assistente interno', 'Para empresas de maior dimensão: um assistente de IA privado que responde com base nos documentos da empresa.')], 'Depois do<br>diagnóstico.'),
        contact=('O que lhe ocupa mais tempo na empresa?', 'Conte-me em duas ou três linhas. Respondo com a forma como faria o diagnóstico no seu caso.'),
        foot=('Antes de automatizar,<br>uma semana de registo.', 'Pedir o Método StarMap', 'Método StarMap'))

# ---------------------------------------------------------------- /assistente-interno
VIS_RAG = '''<div class="hud" id="vis-rag"><div class="hh"><span>Assistente interno</span><span class="live">Equipa: Compras</span></div>
<div class="q">Qual é o prazo de pagamento da Metalúrgica Silva?</div>
<div class="stt">a procurar nos documentos…</div>
<div class="ans" data-txt="60 dias após a data da fatura, segundo o contrato de 2024 e a adenda n.º 2."></div>
<div class="srcs"><span>Contrato_Metalurgica_Silva_2024.pdf · p. 3</span><span>Adenda_02.pdf · p. 1</span></div>
<div class="ft"><span>Exemplo ilustrativo com documentos fictícios.</span></div></div>'''

FAQ_RAG = [('O que é RAG?', 'RAG (Retrieval-Augmented Generation) é a técnica em que o assistente primeiro procura os excertos certos nos documentos da empresa e só depois escreve a resposta com base neles. É o que permite citar a fonte e não responder de memória.'),
           ('Os documentos saem da empresa?', 'Depende da opção escolhida no levantamento: tudo em servidores da empresa, ou numa nuvem com contrato empresarial que não usa os dados para treinar modelos. Explico as diferenças antes de decidir.'),
           ('A IA pode inventar respostas?', 'Pode errar, como qualquer sistema. Por isso cada resposta mostra o documento de origem e o assistente está configurado para dizer quando não encontra nada.'),
           ('Um estagiário vai ver os contratos da direção?', 'Não. O assistente segue as permissões que já existem nas pastas. Quem não tem acesso a um documento não recebe respostas baseadas nele.'),
           ('Que tipos de documento aceita?', 'PDF, Word, Excel, PowerPoint, páginas internas e, se fizer sentido, emails. Documentos digitalizados também, depois de convertidos em texto.'),
           ('Liga-se ao que já usamos?', 'Google Drive, SharePoint e OneDrive, pastas de rede e a maioria dos sistemas com exportação de documentos.'),
           ('Para que empresas faz sentido?', 'Para empresas com muita documentação interna e equipas que fazem as mesmas perguntas muitas vezes: indústria, serviços técnicos, saúde, ensino e serviços profissionais.')]

Y = lambda s: s
CODE1 = '''<span class="c"># como os documentos entram no assistente</span>
<span class="k">fontes:</span>
  - <span class="s">sharepoint://qualidade/procedimentos</span>
  - <span class="s">drive://compras/contratos</span>
  - <span class="s">smb://servidor/manuais</span>
<span class="k">preparacao:</span>
  <span class="k">duplicados:</span> remover
  <span class="k">versoes:</span> manter_so_em_vigor
  <span class="k">digitalizados:</span> ocr
<span class="k">indexacao:</span>
  <span class="k">divisao:</span> por_secao
  <span class="k">atualizacao:</span> quando_o_ficheiro_muda
<span class="k">resposta:</span>
  <span class="k">citar_fonte:</span> sempre
  <span class="k">sem_fonte:</span> <span class="s">"Não encontrei esta informação."</span>'''
CODE2 = '''<span class="c"># as respostas seguem os acessos que já existem</span>
<span class="k">equipas:</span>
  <span class="k">compras:</span>
    <span class="k">pode_ver:</span> [contratos, fornecedores]
  <span class="k">qualidade:</span>
    <span class="k">pode_ver:</span> [procedimentos, nao_conformidades]
  <span class="k">comercial:</span>
    <span class="k">pode_ver:</span> [propostas, procedimentos]
  <span class="k">direcao:</span>
    <span class="k">pode_ver:</span> tudo
<span class="k">registo:</span>
  <span class="k">perguntas_sem_resposta:</span> guardar'''
CODE3 = '''{
  <span class="k">"pergunta"</span>: <span class="s">"Prazo de pagamento Metalúrgica Silva?"</span>,
  <span class="k">"utilizador"</span>: <span class="s">"compras"</span>,
  <span class="k">"resposta"</span>: <span class="s">"60 dias após a data da fatura..."</span>,
  <span class="k">"fontes"</span>: [
    { <span class="k">"documento"</span>: <span class="s">"Contrato_Metalurgica_Silva_2024.pdf"</span>, <span class="k">"pagina"</span>: <span class="n">3</span> },
    { <span class="k">"documento"</span>: <span class="s">"Adenda_02.pdf"</span>, <span class="k">"pagina"</span>: <span class="n">1</span> }
  ]
}'''

def page_rag():
    Yc, N = '<td class="y">✓</td>', '<td>—</td>'
    mx = [('Compras', 'YNNY'), ('Qualidade', 'NYNN'), ('Comercial', 'NYYY'), ('Direção', 'YYYY')]
    mxr = ''.join(f'<tr><td>{t}</td>' + ''.join(Yc if c == 'Y' else N for c in s) + '</tr>' for t, s in mx)
    return dict(
        slug='assistente-interno', crumb='Assistente interno', pre='Assistente interno',
        title='Assistente interno com IA para empresas · Starmountain Flash',
        desc='Assistente de IA privado que responde com base nos documentos internos da empresa, com a fonte citada e as permissões de cada equipa.',
        service=dict(name='Assistente interno com IA', type='Assistente de IA com RAG sobre documentos internos', offers=None),
        faq=FAQ_RAG,
        body=hero('Assistente interno · empresas de maior dimensão', 'Pergunte aos documentos<br>da sua empresa.',
                  'Um assistente de IA privado que responde com base nos documentos internos da empresa: procedimentos, contratos, manuais e propostas antigas. Cada resposta indica o documento e a página de onde saiu.',
                  'Marcar reunião', 'Assistente interno', '#como', 'Como funciona', 'Assistente interno', VIS_RAG)
        + '<div class="strip"><span class="ey">Liga-se ao que a empresa já usa</span><div class="chips">' + ''.join(f'<span>{t}</span>' for t in ['Google Drive', 'SharePoint', 'OneDrive', 'Word', 'Excel', 'PowerPoint', 'Pastas de rede', 'Digitalizados']) + '</div></div>'
        + f'<section class="method" style="border-radius:0;padding-top:6rem"><div class="hh"><span class="ey">01 · O problema</span><h2 data-split="1" style="margin-top:1rem">A resposta existe.<br>Ninguém sabe onde.</h2><p class="tlead" style="margin:1.4rem auto 0;text-align:center">Quem precisa dela pergunta a um colega, e esse colega interrompe o que está a fazer.</p></div><div class="mgrid mgrid3" data-cards>'
        + mc('01', 'Pasta partilhada', 'Num PDF numa pasta partilhada', 'Com três versões e nenhuma a dizer qual é a que está em vigor.', icon=IC_FILE)
        + mc('02', 'Caixa de correio', 'Num email de há dois anos', 'Reencaminhado tantas vezes que já ninguém o encontra pela pesquisa.', icon=IC_MAIL)
        + mc('03', 'Pessoas', 'Na cabeça de quem já saiu', 'Ou de quem está de férias precisamente na semana em que é preciso.', icon=IC_USER)
        + '</div></section>'
        + f'<section class="sec dk">{sh("02 · Permissões", "Cada equipa vê<br>o que já via.", "O assistente segue as permissões que já existem nas pastas. Quem não tem acesso a um documento não recebe respostas baseadas nele.")}'
        + f'<div class="perm" data-cards><div class="mxw"><table class="mxt"><thead><tr><th>Equipa</th><th>Contratos</th><th>Proced.</th><th>Propostas</th><th>Preços</th></tr></thead><tbody>{mxr}</tbody></table></div>'
        + '<div><div class="blk"><p class="q"><small>Comercial pergunta</small>“Qual é a margem do contrato com a Fornecedor A?”</p><span class="no">Sem acesso a contratos · pergunta bloqueada</span></div>'
        + '<div class="ticks"><span>Permissões por equipa ou por pessoa</span><span>Contratos da direção ficam na direção</span><span>Registo das perguntas feitas</span></div></div></div></section>'
        + f'<section class="sec">{sh("03 · O Vault", "Antes de ligar,<br>arrumar.", "Um assistente ligado a pastas desarrumadas dá respostas desarrumadas. Por isso a primeira parte do trabalho é o Vault: um arquivo organizado, sem duplicados e só com a versão em vigor de cada documento.")}'
        + '<div class="vault" data-cards><div class="vc"><span class="tag">Antes</span><ul><li>Contrato_FINAL_v3.pdf</li><li>Contrato_FINAL_v3 (1).pdf</li><li>manual_qualidade_antigo.docx</li><li>scan_0042.pdf</li><li>Copia de Tabela precos.xlsx</li></ul></div><div class="varr">→</div>'
        + '<div class="vc ok"><span class="tag">Vault · em vigor</span><ul><li class="d">Compras/</li><li class="f">Contratos/Fornecedor A 2024.pdf</li><li class="d">Qualidade/</li><li class="f">PR-07 Devoluções v4.docx</li><li class="d">Comercial/</li><li class="f">Tabela de preços 2024.xlsx</li></ul></div></div>'
        + '<div class="ticks t3"><span>Duplicados e versões antigas removidos</span><span>Digitalizados convertidos em texto</span><span>Estrutura pensada para a empresa</span></div></section>'
        + f'<section class="sec dk" id="como">{sh("04 · Como funciona", "Como um documento<br>chega à resposta.", "Das pastas onde os documentos já estão até à equipa que faz a pergunta. A forma como os documentos são partidos, indexados e filtrados decide se as respostas são úteis. A maior parte do trabalho está nesta parte.")}'
        + '<div class="pipe" data-cards><div class="pn"><small>Fontes</small><b>Onde já estão</b><span>Google Drive · SharePoint · pastas de rede · PDF</span></div><div class="pn"><small>1 · Organizar</small><b>Vault</b><span>Sem duplicados, versão em vigor</span></div><div class="pn"><small>2 · Indexar</small><b>Índice</b><span>Excertos por secção, com permissões</span></div><div class="pn hl"><small>3 · Responder</small><b>Assistente</b><span>Resposta com a fonte</span></div><div class="pn"><small>Equipas</small><b>Quem pergunta</b><span>Compras · Qualidade · Comercial, cada uma vê só o que já via</span></div></div>'
        + f'<div class="code" data-tabs><div class="tabs"><button type="button" data-t>pipeline.yaml</button><button type="button" data-t>permissoes.yaml</button><button type="button" data-t>resposta.json</button></div><pre class="cp" data-p>{CODE1}</pre><pre class="cp" data-p>{CODE2}</pre><pre class="cp" data-p>{CODE3}</pre></div>'
        + '<div class="notes"><div><b>Onde ficam os dados</b><span>Em servidores da empresa ou numa nuvem com contrato empresarial. Decidido no levantamento.</span></div><div><b>Atualização</b><span>Quando um documento muda na origem, o assistente passa a responder com a versão nova.</span></div><div><b>Registo</b><span>As perguntas sem resposta mostram que documentação falta na empresa.</span></div></div></section>'
        + f'<section class="sec">{sh("05 · Fases", "Começa por uma equipa,<br>depois alarga.", "Um piloto com um só departamento mostra depressa se as respostas servem e que documentos estão em falta ou desatualizados.")}'
        + '<div class="tline" data-cards><div><span class="n">01</span><h3>Levantamento</h3><p>Que documentos existem, onde estão, quem acede a quê e que perguntas cada equipa faz mais vezes. Aqui decide-se também onde ficam os dados.</p></div>'
        + '<div><span class="n">02</span><h3>Organização do Vault</h3><p>Limpar duplicados e versões antigas e definir uma estrutura que faça sentido para a empresa.</p></div>'
        + '<div><span class="n">03</span><h3>Assistente e permissões</h3><p>Ligação às fontes, indexação e testes com perguntas reais da empresa, antes de alguém o usar.</p></div>'
        + '<div><span class="n">04</span><h3>Piloto com uma equipa</h3><p>Um departamento usa-o no dia a dia. Ajusto com base no que perguntam e no que fica sem resposta.</p></div>'
        + '<div><span class="n">05</span><h3>Alargar</h3><p>Novas equipas e novas fontes, com revisão regular das perguntas sem resposta e dos acessos.</p></div></div></section>'
        + faq_sec('06 · Perguntas frequentes', 'O que me<br>perguntam mais.', FAQ_RAG)
        + rel_sec([('b.1', 'starmap', 'Método StarMap', 'Uma semana de registo das tarefas da equipa e um relatório com o que automatizar primeiro.'),
                   ('b.2', 'automacoes', 'Automações à medida', 'Emails, faturas, relatórios, marcações e CRM a correr sozinhos.')]),
        contact=('Que perguntas a sua equipa faz todas as semanas?', 'Numa primeira reunião olhamos para a documentação que existe e digo-lhe se faz sentido avançar e por onde começar.'),
        foot=('Começar por<br>uma equipa.', 'Marcar reunião', 'Assistente interno'))
