# Páginas legais e 404. Conteúdo convertido dos page.tsx do site atual.
import re, html as H
from pages import hero, sh, U

R = '/home/claude/repo/starmountainflash-site/src/app/'
SITE = {'nome': 'Starmountain Flash', 'email': 'geral@starmountainflash.pt', 'telefone': '+351 937 800 553', 'telefoneRaw': '+351937800553',
        'localidade': 'Covilhã', 'nif': '251504387', 'nomeLegal': 'Pedro Miguel da Silva Pereira', 'url': U}

def jsx(s):
    s = re.sub(r"href=\{'mailto:' \+ site\.email\}", f'href="mailto:{SITE["email"]}"', s)
    s = re.sub(r"href=\{'tel:' \+ site\.telefoneRaw\}", f'href="tel:{SITE["telefoneRaw"]}"', s)
    s = re.sub(r"\{site\.(\w+)\}", lambda m: SITE[m.group(1)], s)
    s = s.replace("{' '}", ' ')
    s = re.sub(r"\{'([^']*)'\}", r'\1', s)
    s = re.sub(r'\{"([^"]*)"\}', r'\1', s)
    s = s.replace('<>', '').replace('</>', '').replace('className=', 'class=')
    s = re.sub(r'<Link\b', '<a', s).replace('</Link>', '</a>')
    s = re.sub(r'href=\{([^}]+)\}', lambda m: 'href="' + m.group(1).strip("'\"") + '"', s)
    s = re.sub(r'href="/([^"]*)"', lambda m: f'href="%%L:{m.group(1)}%%"' if m.group(1) in ('privacidade', 'cookies', 'termos', 'aviso-legal', 'contacto', 'sobre') else f'href="{U}/{m.group(1)}"', s)
    s = re.sub(r'<a href="(https?://(?!starmountainflash)[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def seccoes(slug):
    t = open(R + slug + '/page.tsx', encoding='utf8').read()
    body = t[t.index('const seccoes'):]
    out = []
    for m in re.finditer(r"\{\s*id: '([^']+)',\s*titulo: '((?:[^'\\]|\\.)*)',\s*corpo: \((.*?)\),\s*\},\s*(?=\{\s*id:|\];)", body, re.S):
        out.append((m.group(1), m.group(2).replace("\\'", "'"), fix(slug, jsx(m.group(3)))))
    return out

HITS = {}
FIXES = {
 'pt': [
  # foto Unsplash já não é usada
  ('<p> A fotografia usada no topo das páginas é de Ricardo Rocha, obtida no Unsplash e usada ao abrigo da licença dessa plataforma. </p>', ''),
  (' A fotografia do topo das páginas é de Ricardo Rocha, obtida no Unsplash e usada ao abrigo da licença dessa plataforma.', ''),
  # privacidade: dados do pedido
  ('<li>A página a partir da qual o pedido foi enviado e a data e hora</li>',
   '<li>A página a partir da qual o pedido foi enviado e a data e hora</li> <li>A página por onde entrou no site e de onde veio (por exemplo, um motor de pesquisa, uma rede social ou uma campanha), quando essa informação existe. Fica guardada no navegador só durante a visita e só segue para nós se enviar o pedido.</li>'),
  # privacidade: medição
  ('<p> Se aceitar no aviso de cookies, é carregado o Google Analytics 4, com anonimização do endereço IP. Se recusar, nenhum código de medição é carregado e o site funciona na mesma. A escolha fica guardada apenas no seu navegador e pode ser alterada limpando os dados do site. </p>',
   '<p> O aviso de cookies tem duas categorias, que pode aceitar em separado. Se aceitar <strong>Medição</strong>, são carregados o Google Analytics 4 e o Microsoft Clarity. O Clarity mostra de forma agregada onde se clica e até onde se faz scroll e grava a navegação nas páginas, com o texto escrito nos formulários ocultado. Se aceitar <strong>Marketing</strong>, é carregado o Pixel da Meta, para medir se as visitas que chegam dos anúncios da Meta (Facebook e Instagram) dão origem a pedidos. Se recusar, nenhum destes códigos é carregado e o site funciona na mesma. A escolha fica guardada apenas no seu navegador e pode ser alterada a qualquer momento em <strong>Preferências de cookies</strong>, no rodapé. </p> <p> O site usa também o Plausible, que conta visitas sem cookies e sem guardar dados que permitam identificar quem visita. </p>'),
  ('<p> Na página da análise gratuita, se aceitar, é carregado também o Pixel da Meta, para medir se as visitas que chegam dos anúncios da Meta (Facebook e Instagram) dão origem a pedidos. Se recusar, não é carregado. </p>', ''),
  ('<li> <strong>Dados de audiência:</strong> conforme a retenção configurada no Google Analytics, no máximo 14 meses. </li>',
   '<li> <strong>Dados de audiência:</strong> conforme a retenção configurada no Google Analytics, no máximo 14 meses; no Microsoft Clarity, as gravações e os mapas ficam disponíveis durante o prazo definido pela Microsoft. </li>'),
  ('<li> <strong>Google Ireland</strong> — Google Analytics, apenas se aceitar os cookies de medição. </li>',
   '<li> <strong>Google Ireland</strong> — Google Analytics, apenas se aceitar a categoria Medição. </li> <li> <strong>Microsoft Ireland</strong> — Microsoft Clarity, apenas se aceitar a categoria Medição. </li> <li> <strong>Meta Platforms Ireland</strong> — Pixel da Meta, apenas se aceitar a categoria Marketing. </li> <li> <strong>Plausible Insights</strong> — contagem de visitas sem cookies. Empresa sediada na União Europeia. </li>'),
  # cookies
  ('<p> Apenas um registo no armazenamento local do navegador, que guarda a sua resposta ao aviso de cookies para não voltar a perguntar. Não é um cookie, não é enviado para nenhum servidor e não permite identificá-lo. </p>',
   '<p> Dois registos no armazenamento do navegador. Não são cookies, não são enviados para nenhum servidor e não permitem identificá-lo. </p>'),
  ('<tr> <td> <code>smf-cookies</code> </td> <td>Guarda se aceitou ou recusou a medição de audiências</td> <td>Até limpar os dados do site</td> </tr>',
   '<tr> <td> <code>smf-consent</code> </td> <td>Guarda as categorias que aceitou ou recusou no aviso de cookies</td> <td>Até limpar os dados do site</td> </tr> <tr> <td> <code>smf-orig</code> </td> <td>Guarda a página de entrada e de onde veio, para juntar ao pedido se enviar um formulário</td> <td>Até fechar o separador</td> </tr>'),
  ('<p> Se carregar em <strong>Aceitar</strong>, é carregado o Google Analytics 4, com anonimização do endereço IP. Serve para perceber que páginas são úteis e de onde chegam as visitas. Se recusar, nenhum destes cookies é criado. </p>',
   '<p> Se aceitar a categoria <strong>Medição</strong>, são carregados o Google Analytics 4 e o Microsoft Clarity. Servem para perceber que páginas são úteis, de onde chegam as visitas e onde as pessoas clicam. Se recusar, nenhum destes cookies é criado. </p>'),
  ('<p> Na página da análise gratuita, aceitar carrega também o Pixel da Meta, que mede se as visitas que chegam dos anúncios da Meta (Facebook e Instagram) dão origem a pedidos. </p>',
   '<table><thead><tr><th>Nome</th><th>Para que serve</th><th>Duração</th></tr></thead><tbody><tr><td><code>_clck</code></td><td>Distingue visitantes no Microsoft Clarity</td><td>1 ano</td></tr><tr><td><code>_clsk</code></td><td>Junta as páginas vistas numa mesma visita</td><td>1 dia</td></tr></tbody></table><p> Estes cookies são da Microsoft Ireland Operations Limited. Pode consultar a <a href="https://learn.microsoft.com/clarity/setup-and-installation/cookie-list" target="_blank" rel="noopener">lista de cookies do Clarity</a>. </p> <p> Se aceitar a categoria <strong>Marketing</strong>, é carregado o Pixel da Meta, que mede se as visitas que chegam dos anúncios da Meta (Facebook e Instagram) dão origem a pedidos. </p>'),
  ('<p>O site não usa cookies para funcionar. São usados apenas dois mecanismos:</p> <ul> <li> <strong>Armazenamento local do navegador</strong>, para guardar a sua resposta ao aviso de cookies. Não é enviado para nenhum servidor. </li> <li> <strong>Cookies do Google Analytics</strong>, criados apenas se aceitar. Servem para distinguir visitas e medir a utilização do site. </li> </ul> <p> Para mudar a sua escolha, limpe os dados deste site no navegador: o aviso volta a aparecer na visita seguinte.',
   '<p>O site não usa cookies para funcionar. São usados apenas estes mecanismos:</p> <ul> <li> <strong>Armazenamento do navegador</strong>, para guardar a sua resposta ao aviso de cookies e, só durante a visita, a página de entrada e de onde veio. Não é enviado para nenhum servidor, a não ser que envie um pedido. </li> <li> <strong>Cookies do Google Analytics e do Microsoft Clarity</strong>, criados apenas se aceitar a categoria Medição. </li> <li> <strong>Cookie do Pixel da Meta</strong>, criado apenas se aceitar a categoria Marketing. </li> </ul> <p> Para mudar a sua escolha, carregue em <strong>Preferências de cookies</strong>, no rodapé.'),
  ('<p> Para voltar a decidir, limpe os dados deste site no seu navegador: o aviso reaparece na visita seguinte e pode escolher outra vez. Ao recusar, os cookies de medição deixam de ser criados. </p>',
   '<p> Para voltar a decidir, carregue em <strong>Preferências de cookies</strong>, no rodapé de qualquer página, ou limpe os dados deste site no seu navegador. Ao recusar, os cookies dessa categoria deixam de ser criados. </p>'),
 ],
 'en': [
  ('<p> Only one entry in browser local storage, which stores your answer to the cookie notice so that you are not asked again. It is not a cookie, it is not sent to any server and it cannot be used to identify you. </p>',
   '<p> Two entries in browser storage. They are not cookies, they are not sent to any server and they cannot be used to identify you. </p>'),
  ('<p> The photograph used at the top of the pages is by Ricardo Rocha, obtained from Unsplash and used under that platform&apos;s licence. </p>', ''),
  (' The photograph at the top of the pages is by Ricardo Rocha, obtained from Unsplash and used under that platform&apos;s licence.', ''),
  ('<li>The page from which the request was sent, and the date and time</li>',
   '<li>The page from which the request was sent, and the date and time</li> <li>The page through which you entered the website and where you came from (for example, a search engine, a social network or a campaign), when that information exists. It is kept in the browser only during the visit and only reaches us if you send the request.</li>'),
  ('<p> If you accept in the cookie notice, Google Analytics 4 is loaded, with IP address anonymisation. If you decline, no measurement code is loaded and the website works just the same. Your choice is stored only in your browser and can be changed by clearing the site data. </p>',
   '<p> The cookie notice has two categories, which you can accept separately. If you accept <strong>Measurement</strong>, Google Analytics 4 and Microsoft Clarity are loaded. Clarity shows, in aggregate, where people click and how far they scroll, and records navigation on the pages, with the text typed into forms hidden. If you accept <strong>Marketing</strong>, the Meta Pixel is loaded, to measure whether visits from Meta ads (Facebook and Instagram) lead to requests. If you decline, none of this code is loaded and the website works just the same. Your choice is stored only in your browser and can be changed at any time under <strong>Cookie preferences</strong>, in the footer. </p> <p> The website also uses Plausible, which counts visits without cookies and without storing data that could identify visitors. </p>'),
  ('<p> On the free review page, if you accept, the Meta Pixel is also loaded, to measure whether visits from Meta ads (Facebook and Instagram) lead to requests. If you decline, it is not loaded. </p>', ''),
  ('<li> <strong>Audience data:</strong> according to the retention configured in Google Analytics, up to a maximum of 14 months. </li>',
   '<li> <strong>Audience data:</strong> according to the retention configured in Google Analytics, up to a maximum of 14 months; in Microsoft Clarity, recordings and heatmaps remain available for the period set by Microsoft. </li>'),
  ('<li> <strong>Google Ireland</strong>: Google Analytics, only if you accept the measurement cookies. </li>',
   '<li> <strong>Google Ireland</strong>: Google Analytics, only if you accept the Measurement category. </li> <li> <strong>Microsoft Ireland</strong>: Microsoft Clarity, only if you accept the Measurement category. </li> <li> <strong>Meta Platforms Ireland</strong>: Meta Pixel, only if you accept the Marketing category. </li> <li> <strong>Plausible Insights</strong>: cookieless visit counting. A company based in the European Union. </li>'),
  ('<tr> <td> <code>smf-cookies</code> </td> <td>Stores whether you accepted or declined audience measurement</td> <td>Until you clear the site data</td> </tr>',
   '<tr> <td> <code>smf-consent</code> </td> <td>Stores the categories you accepted or declined in the cookie notice</td> <td>Until you clear the site data</td> </tr> <tr> <td> <code>smf-orig</code> </td> <td>Stores the entry page and where you came from, to attach to the request if you send a form</td> <td>Until you close the tab</td> </tr>'),
  ('<p> If you click <strong>Accept</strong>, Google Analytics 4 is loaded, with IP address anonymisation. It is used to understand which pages are useful and where visits come from. If you decline, none of these cookies is created. </p>',
   '<p> If you accept the <strong>Measurement</strong> category, Google Analytics 4 and Microsoft Clarity are loaded. They are used to understand which pages are useful, where visits come from and where people click. If you decline, none of these cookies is created. </p>'),
  ('<p> On the free review page, accepting also loads the Meta Pixel, which measures whether visits from Meta ads (Facebook and Instagram) lead to requests. </p>',
   '<table><thead><tr><th>Name</th><th>Purpose</th><th>Duration</th></tr></thead><tbody><tr><td><code>_clck</code></td><td>Distinguishes visitors in Microsoft Clarity</td><td>1 year</td></tr><tr><td><code>_clsk</code></td><td>Groups the pages viewed in the same visit</td><td>1 day</td></tr></tbody></table><p> These cookies belong to Microsoft Ireland Operations Limited. You can read the <a href="https://learn.microsoft.com/clarity/setup-and-installation/cookie-list" target="_blank" rel="noopener">Clarity cookie list</a>. </p> <p> If you accept the <strong>Marketing</strong> category, the Meta Pixel is loaded, which measures whether visits from Meta ads (Facebook and Instagram) lead to requests. </p>'),
  ('<p>The website does not use cookies to work. Only two mechanisms are used:</p> <ul> <li> <strong>Browser local storage</strong>, to store your answer to the cookie notice. It is not sent to any server. </li> <li> <strong>Google Analytics cookies</strong>, created only if you accept. They are used to distinguish visits and measure use of the website. </li> </ul> <p> To change your choice, clear this site&apos;s data in your browser: the notice will appear again on your next visit.',
   '<p>The website does not use cookies to work. Only these mechanisms are used:</p> <ul> <li> <strong>Browser storage</strong>, to store your answer to the cookie notice and, only during the visit, the entry page and where you came from. It is not sent to any server unless you send a request. </li> <li> <strong>Google Analytics and Microsoft Clarity cookies</strong>, created only if you accept the Measurement category. </li> <li> <strong>Meta Pixel cookie</strong>, created only if you accept the Marketing category. </li> </ul> <p> To change your choice, click <strong>Cookie preferences</strong> in the footer.'),
  ('<p> To decide again, clear this site&apos;s data in your browser: the notice reappears on your next visit and you can choose again. If you decline, the measurement cookies are no longer created. </p>',
   '<p> To decide again, click <strong>Cookie preferences</strong> in the footer of any page, or clear this site&apos;s data in your browser. If you decline, the cookies in that category are no longer created. </p>'),
 ]}

def fix(slug, c):
    en = '/en/' in R
    c = re.sub(r'\s+', ' ', c)
    # extras do Pixel acrescentados antes (cookies): aplicados abaixo como texto de origem
    if slug == 'cookies':
        a = ("Google&apos;s information about cookies </a> . </p>" if en else 'informação do Google sobre cookies </a> . </p>')
        b = ('<p> On the free review page, accepting also loads the Meta Pixel, which measures whether visits from Meta ads (Facebook and Instagram) lead to requests. </p>'
             '<table><thead><tr><th>Name</th><th>Purpose</th><th>Duration</th></tr></thead><tbody><tr><td><code>_fbp</code></td><td>Links the visit to Meta ads</td><td>90 days</td></tr></tbody></table>'
             "<p> This cookie belongs to Meta Platforms Ireland Limited. You can read <a href=\"https://www.facebook.com/privacy/policies/cookies/\" target=\"_blank\" rel=\"noopener\">Meta&apos;s cookie policy</a>. </p>") if en else \
            ('<p> Na página da análise gratuita, aceitar carrega também o Pixel da Meta, que mede se as visitas que chegam dos anúncios da Meta (Facebook e Instagram) dão origem a pedidos. </p>'
             '<table><thead><tr><th>Nome</th><th>Para que serve</th><th>Duração</th></tr></thead><tbody><tr><td><code>_fbp</code></td><td>Associa a visita aos anúncios da Meta</td><td>90 dias</td></tr></tbody></table>'
             '<p> Este cookie é da Meta Platforms Ireland Limited. Pode consultar a <a href="https://www.facebook.com/privacy/policies/cookies/" target="_blank" rel="noopener">política de cookies da Meta</a>. </p>')
        c = c.replace(a, a + ' ' + b)
    for k, (old, new) in enumerate(FIXES['en' if en else 'pt']):
        if old in c:
            c = c.replace(old, new); HITS[('en' if en else 'pt', k)] = 1
    return c

LEG = [('privacidade', 'Política de privacidade', 'Política de privacidade.', 'Sem letras pequenas.', 'Que dados são recolhidos neste site, para que servem, quanto tempo ficam guardados e como pode exercer os seus direitos.',
        'Que dados pessoais a Starmountain Flash recolhe no site, para que servem, quanto tempo ficam guardados e como exercer os seus direitos.'),
       ('cookies', 'Cookies', 'Política de cookies.', 'Poucos, e só com autorização.', 'Que cookies este site usa, para que servem, quanto tempo duram e como mudar a sua escolha a qualquer momento.',
        'Que cookies o site starmountainflash.pt usa, para que servem, quanto tempo duram e como mudar a sua escolha a qualquer momento.'),
       ('termos', 'Termos', 'Termos e condições.', 'O que fica combinado.', 'Condições de utilização do site e regras dos serviços: propostas, prazos, pagamentos, propriedade do trabalho e reclamações.',
        'Condições de utilização do site e regras dos serviços da Starmountain Flash: propostas, prazos, pagamentos, propriedade do trabalho e resolução de litígios.'),
       ('aviso-legal', 'Aviso legal', 'Aviso legal.', 'Quem é o titular deste site.', 'Identificação, âmbito, propriedade intelectual, responsabilidade e lei aplicável ao site starmountainflash.pt.',
        'Identificação do titular do site starmountainflash.pt, âmbito, propriedade intelectual, responsabilidade e lei aplicável.')]
TITLES = {'privacidade': 'Política de privacidade', 'cookies': 'Política de cookies', 'termos': 'Termos e condições', 'aviso-legal': 'Aviso legal'}

def page_legal(slug, crumb, h1, h1b, lead, desc):
    sec = seccoes(slug)
    assert len(sec) >= 3, (slug, len(sec))
    toc = ''.join(f'<a href="#{i}"><span>{n + 1:02d}</span>{H.escape(t)}</a>' for n, (i, t, _) in enumerate(sec))
    VIS = f'<div class="hud" id="vis-toc"><div class="hh"><span>Nesta página</span><span class="live">24 nov. 2026</span></div><nav class="tc2 tcn">{toc}</nav></div>'
    others = ''.join(f'<a href="%%L:{s}%%">{TITLES[s]}</a>' for s, *_ in LEG if s != slug)
    body = hero('Legal', f'{h1}<br>{h1b}', lead, 'Proposta gratuita', '', '#texto', 'Ler', crumb, VIS, mid=False, cls='sub art')
    body = body.replace('<p class="lead" data-hi>', '<div class="pmeta" data-hi><span>Última atualização: 24 de novembro de 2026</span></div><p class="lead" data-hi>', 1)
    prose = ''.join(f'<section><h2 id="{i}">{H.escape(t)}</h2>{c}</section>' for i, t, c in sec)
    body += f'<section class="sec" id="texto"><article class="prose legal">{prose}<div class="lother"><span class="ey">Outras páginas legais</span><div>{others}<a href="https://www.livroreclamacoes.pt" target="_blank" rel="noopener">Livro de Reclamações ↗</a></div></div></article></section>'
    return dict(slug=slug, crumb=crumb, pre='', kind='legal', title=f'{TITLES[slug]} · Starmountain Flash', desc=desc, faq=[], body=body, contact=None, foot=None)

def page_404():
    at = [('websites', 'Websites', 'Landing pages e sites institucionais.'), ('lojas-online', 'Lojas online', 'Shopify ou à medida, prontas a vender.'),
          ('automacoes', 'Automações à medida', 'O trabalho repetitivo a fazer-se sozinho.'), ('trabalhos', 'Trabalhos', 'UBI, Planet Trading, StudyOS e Beatriz Nunes.'),
          ('metodo', 'Como trabalho', 'Três fases, a começar por uma proposta visual gratuita.'), ('blog', 'Blog', 'Notas sobre sites, SEO e automação.')]
    cards = ''.join(f'<a class="bc" href="{"%%HOME%%" + h if h.startswith("#") else "%%L:" + h + "%%"}"><h3>{t}</h3><p>{d}</p><span class="d">Ir →</span></a>' for h, t, d in at)
    VIS = '<div class="hud" id="vis-404"><div class="hh"><span>Erro</span><span class="live">404</span></div><div class="e404">404</div><p class="sm2">O endereço pode estar mal escrito ou a página pode ter mudado de sítio.</p></div>'
    body = hero('Página não encontrada', 'Erro 404.<br>Esta página não existe.', 'O endereço pode estar mal escrito ou a página pode ter mudado de sítio. Deixo aqui os caminhos mais usados.',
                'Proposta gratuita', '', '%%HOME%%', 'Voltar ao início', 'Página não encontrada', VIS, mid=False)
    body += f'<section class="sec">{sh("Para onde ir", "Talvez procurasse<br>uma destas.")}<div class="bgrid2">{cards}</div></section>'
    return dict(slug='404', crumb='Página não encontrada', pre='', kind='legal', noindex=True, title='Página não encontrada · Starmountain Flash',
                desc='Esta página não existe. Veja os serviços, os trabalhos ou fale diretamente comigo.', faq=[], body=body, contact=None, foot=None)

def pages(): return [page_legal(*l) for l in LEG] + [page_404()]
