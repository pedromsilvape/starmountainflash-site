"""Ajustes de texto aplicados na conversão: a página Sobre deixa de apresentar o Pedro como
contabilista e passa a usar a missão e a visão do manual de marca de 2026."""
import re
R = lambda p: re.compile(p, re.S)
TEXTOS = {
 'pt': {'sobre': [
  ('técnico de contabilidade, formação militar, websites', 'formação militar, websites'),
  ('O contabilista que automatiza.<br><em>E constrói sites para empresas.</em>', 'Uma startup tecnológica portuguesa,<br><em>criada fora dos grandes centros.</em>'),
  ('Contabilidade, formação militar e muitas horas', 'Formação militar e muitas horas'),
  ('Sou técnico de contabilidade. Passo os dias dentro dos processos das empresas, e vejo de perto', 'Conheço por dentro os processos das empresas e vejo de perto'),
  ('Antes da contabilidade houve o Exército.', 'Antes de tudo isto houve o Exército.'),
  ('<span lang="pt">Contabilidade</span></h3><p><span lang="pt">Técnico de contabilidade. O dia a dia', '<span lang="pt">Dentro das empresas</span></h3><p><span lang="pt">O dia a dia'),
  (R(r'<article class="ct rv"[^>]*>(?:(?!</article>).)*?Técnico de contabilidade(?:(?!</article>).)*?</article>'), ''),
  (R(r'(O que faço todos os dias</span></h3><p><span lang="pt">).*?(</span></p>)'), r'\1Pôr a tecnologia a fazer o trabalho repetitivo das empresas, para as pessoas ficarem com tempo para o que só elas sabem fazer.\2'),
  (R(r'(Para onde quero chegar</span></h3><p><span lang="pt">).*?(</span></p>)'), r'\1Ser reconhecida como uma startup tecnológica portuguesa com produtos próprios, criada fora dos grandes centros.\2'),
 ]},
 'en': {'sobre': [
  ('accounting technician with military training, building', 'military training, building'),
  ('The accountant who automates.<br><em>And builds websites for companies.</em>', 'A Portuguese tech startup,<br><em>built outside the big cities.</em>'),
  ('Accounting, military training and many hours', 'Military training and many hours'),
  ("I'm an accounting technician. I spend my days inside companies' processes and see up close", "I know companies' processes from the inside and see up close"),
  ('Before accounting there was the Army.', 'Before all this there was the Army.'),
  ('<span lang="en">Accounting</span></h3><p><span lang="en">Accounting technician. The day-to-day', '<span lang="en">Inside companies</span></h3><p><span lang="en">The day-to-day'),
  (R(r'<article class="ct rv"[^>]*>(?:(?!</article>).)*?Accounting technician(?:(?!</article>).)*?</article>'), ''),
  (R(r'(What I do every day</span></h3><p><span lang="en">).*?(</span></p>)'), r"\1To put technology to work on companies' repetitive tasks, so people have time for what only they can do.\2"),
  (R(r'(Where I want to get to</span></h3><p><span lang="en">).*?(</span></p>)'), r'\1To be recognised as a Portuguese tech startup with its own products, built outside the big cities.\2'),
 ]},
}
