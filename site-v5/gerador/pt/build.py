import re,random,base64
L='/home/claude/logos/logotipo/svg/'; IMG='/home/claude/repo/starmountainflash-site/public/img/'
def logo(f): return re.sub(r'\s(width|height)="[^"]*"','',open(L+f).read(),count=2)
def b64(p,mime): return f'data:{mime};base64,'+base64.b64encode(open(p,'rb').read()).decode()
ARR='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17 17 7M8 7h9v9"/></svg>'
BOLT='<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg>'
GLOBE='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>'
STAR='<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.6 6.4L21 9l-5 4.2L17.8 20 12 16.3 6.2 20 8 13.2 3 9l6.4-.6z"/></svg>'
PTR='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m4 4 7 17 2.5-7.5L21 11z"/></svg>'
marks=['<circle cx="12" cy="12" r="9"/>','<rect x="4" y="4" width="16" height="16" rx="5"/>','<path d="M12 2.5 21 20.5 3 20.5Z"/>','<path d="M12 3a9 9 0 1 0 9 9h-9Z"/>','<path d="M12 2l2.6 6.4L21 9l-5 4.2L17.8 20 12 16.3 6.2 20 8 13.2 3 9l6.4-.6z"/>']
import json
IC=json.load(open('icons.json'))
def ico(k,col=False):
    c=('#111111' if k=='siOpenai' else '#'+IC[k]['h']) if col else 'currentColor'
    return f'<svg viewBox="0 0 24 24" fill="{c}"><path d="{IC[k]["p"]}"/></svg>'
def mq(keys): return ''.join((f'<div class="mi">{ico(k,True)}{IC[k]["t"]}</div>' if k in IC else f'<div class="mi txt">{k}</div>') for k in keys)*6
M1=mq(['siGmail','siGooglecalendar','siGoogledrive','siGooglesheets','siHubspot','siWhatsapp','TOConline'])
M2=mq(['siShopify','siStripe','siNotion','siClaude','siOpenai','siSupabase','siNetlify','siNextdotjs'])
random.seed(3)
lines=''.join(f'<path d="M0 {y} C 120 {y+random.randint(-60,60)}, 280 {y+random.randint(-60,60)}, 400 {y+random.randint(-40,40)}"/>' for y in range(20,300,14))
works=[('Universidade da Beira Interior · DEI','dei.ubi.pt','Site institucional','ubi-dei-desktop.webp'),
('Universidade da Beira Interior · LGBT Health','lgbthealth.ubi.pt','Site institucional','ubi-lgbthealth-desktop.webp'),
('Universidade da Beira Interior · 3LGBT','3lgbt.ubi.pt','Site institucional','ubi-3lgbt-desktop.webp'),
('Planet Trading','comunidadeplanet.pt','Landing page 3D · CRM','planet-trading-desktop.webp'),
('StudyOS','gestaocrew.pt','Plataforma web','studyos-landing-desktop.webp'),
('Beatriz Nunes, Personal Trainer','personaltrainerbeatriznunes.pt','Redesign · pedidos por email','beatriz-nunes-desktop.webp')]
C='';CBG=''
for i,(n,d,tag,img) in enumerate(works):
    href='https://starmountainflash.pt/trabalhos/'+['ubi','ubi','ubi','planet-trading','studyos','beatriz-nunes'][i]
    src=b64(IMG+'trabalhos/'+img,'image/webp')
    C+=f'<div class="ccard" data-name="{n}" data-href="{href}"><img src="{src}" alt="{tag}: {n} ({d})" loading="lazy"><div class="lbl"><div><span>{str(i+1).zfill(2)} · {tag}</span><b>{n}</b></div><span>{d}</span></div><div class="sc"></div></div>'
    CBG+=f'<div class="cbg"><img data-i="{i}" alt=""></div>'
head=open('head.html').read(); body=open('body.html').read(); tail=open('tail.html').read()
t=head+body+'<script>document.querySelectorAll(".cbg img").forEach(function(im){im.src=document.querySelectorAll(".ccard img")[+im.dataset.i].src})</script>'+tail
rep={'%%LOGO_DARK%%':logo('logotipo-uma-cor-noite.svg'),'%%LOGO_W%%':logo('logotipo-uma-cor-branco.svg'),'%%ARR%%':ARR,'%%BOLT%%':BOLT,'%%GLOBE%%':GLOBE,'%%STAR%%':STAR,'%%PTR%%':PTR,'%%M1%%':M1,'%%M2%%':M2,'%%LINES%%':lines,'%%CARDS%%':C,'%%CBG%%':CBG,'%%TP%%':ico('siTrustpilot',True),'%%GG%%':ico('siGoogle',True),'%%LOGO_W_SM%%':logo('logotipo-uma-cor-branco.svg'),'%%PEDRO%%':b64(IMG+'pedro-pereira.jpg','image/jpeg'),'%%BUNDLE%%':open('bundle.js').read()}
for k,v in rep.items(): t=t.replace(k,v)
t=t.replace('<title>Starmountain Flash · Automações com IA para PME</title>','<title>Starmountain Flash · Websites e automações com IA para empresas</title>')
assert '%%' not in t.replace('%%LOGO','').split('<script>')[0], [m for m in re.findall(r'%%\w+%%',t)]
open('../starmountain-flash-v5.html','w').write(t); print(len(t))
