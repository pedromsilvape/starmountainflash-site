# Site v5

Todas as páginas públicas (PT e EN) são HTML estático em `public/`, servido pelas
rewrites de `next.config.ts` a partir da lista `paginas.json`. A home PT fica em
`public/inicio/index.html`. CSS, JS, imagens e fontes estão em `public/assets/v5/`
(nomes com hash, por isso podem ficar em cache para sempre).

O que continua em Next.js: `/api/lead` (formulários), `sitemap.xml`, `robots.txt`,
`llms.txt`, o painel `/admin` (Decap) e o 404. As rotas React do blog, trabalhos e
páginas legais ficam por baixo: só respondem a um artigo novo do blog que ainda não
tenha versão estática.

## Gerar outra vez

O gerador está em `gerador/` (Python 3 + esbuild):

1. `pt/build_all.py`: páginas PT a partir dos `.md` do blog, `src/data` e `src/app/*/page.tsx`.
2. `en/en_build.py`: versão inglesa (dicionário em `en/tr*.txt` e `en/extra.txt`; blog, casos e legais a partir das fontes EN).
3. `prod.py`: passa tudo para `public/` (imagens para ficheiros, ligações limpas, fontes próprias,
   `site.js` com consentimento, medição e envio para `/api/lead`).

Quando houver um artigo novo no blog, é preciso voltar a gerar para ele aparecer no design novo
e na lista do blog.

Atalho só para o blog: `python3 site-v5/gerador/atualizar_blog.py` (requer `pyyaml` e `markdown`).
Cria as páginas estáticas dos artigos novos (PT e EN), atualiza a lista, os destaques e os artigos
relacionados, e acrescenta os endereços a `paginas.json`, sem mexer no resto do site.

## Medição

`gerador/pt/site.js`: aviso de cookies com duas categorias.
- Medição: Google Analytics 4 (`G-NSBV4CEZNF`) e Microsoft Clarity (`zirtxh4z0q`).
- Marketing: Pixel da Meta (`1379397673888561`).
- Plausible (sem cookies) em todas as páginas.

Eventos GA4: `generate_lead`, `contact_click`, `ver_caso`, `mudar_idioma`, `link_externo`,
`abrir_formulario`, `artigo_lido`. Meta: `Lead`, `Contact`.
Cada pedido guarda em `origem` a página, a página de entrada e a UTM ou o site de onde veio.
