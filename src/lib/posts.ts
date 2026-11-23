import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import GithubSlugger from 'github-slugger';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeSlug from 'rehype-slug';
import rehypeStringify from 'rehype-stringify';

export const CATEGORIAS = ['Websites', 'Lojas online', 'Automação', 'SEO e IA'] as const;
export type Categoria = (typeof CATEGORIAS)[number];

const PASTA = path.join(process.cwd(), 'content', 'blog');
/** Artigos em inglês: mesmo slug, em content/blog/en/. */
const PASTA_EN = path.join(PASTA, 'en');
export type Lingua = 'pt' | 'en';
const pasta = (lang: Lingua) => (lang === 'en' ? PASTA_EN : PASTA);

export type PerguntaDoPost = { pergunta: string; resposta: string };

export type Post = {
  slug: string;
  titulo: string;
  descricao: string;
  categoria: Categoria;
  data: string;
  /** Data da última revisão do conteúdo (opcional). Vai para o dateModified e o sitemap. */
  atualizado?: string;
  /** Título para o Google, se o título do artigo for longo demais (opcional). */
  tituloSeo?: string;
  /** Oferta do bloco de pedido no artigo (opcional; por defeito depende da categoria). */
  cta?: 'analise' | 'proposta' | 'automacao' | 'avaliacoes';
  capa?: string;
  capaAlt?: string;
  publicado: boolean;
  /** Perguntas frequentes do artigo, que também geram o FAQPage. */
  faq: PerguntaDoPost[];
  markdown: string;
};

export type Titulo = { texto: string; id: string; nivel: 2 | 3 };

/** Um artigo longo justifica índice. O limiar é o mesmo que a página usa. */
const MINIMO_INDICE = 3;

/**
 * Aceita tudo o que o YAML e o painel podem dar: um Date (o YAML resolve
 * datas sem aspas), "2026-09-29", "29/09/2026" ou uma data ISO completa.
 * Devolve null em vez de rebentar — uma data mal escrita num artigo não pode
 * derrubar o build do site inteiro.
 */
function lerData(valor: unknown): string | null {
  if (valor instanceof Date) return Number.isNaN(valor.getTime()) ? null : valor.toISOString();
  const texto = String(valor ?? '').trim();
  if (!texto) return null;
  // DD/MM/AAAA — o formato português, que o JavaScript não sabe ler.
  const pt = /^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$/.exec(texto);
  const normalizado = pt ? `${pt[3]}-${pt[2].padStart(2, '0')}-${pt[1].padStart(2, '0')}` : texto;
  const d = new Date(normalizado);
  return Number.isNaN(d.getTime()) ? null : d.toISOString();
}

function ler(ficheiro: string, lang: Lingua = 'pt'): Post | null {
  const bruto = fs.readFileSync(path.join(pasta(lang), ficheiro), 'utf8');
  const { data, content } = matter(bruto);
  const slug = String(data.slug || ficheiro.replace(/\.mdx?$/, ''));
  if (!data.titulo || !data.data) return null;

  const categoria = CATEGORIAS.includes(data.categoria) ? (data.categoria as Categoria) : 'Websites';

  const dataIso = lerData(data.data);
  if (!dataIso) {
    console.warn(`[blog] ${ficheiro}: data ilegível (${String(data.data)}). Artigo ignorado.`);
    return null;
  }

  return {
    slug,
    titulo: String(data.titulo),
    descricao: String(data.descricao || '').slice(0, 155),
    categoria,
    data: dataIso,
    atualizado: (data.atualizado && lerData(data.atualizado)) || undefined,
    tituloSeo: data.tituloSeo ? String(data.tituloSeo) : undefined,
    cta: ['analise', 'proposta', 'automacao', 'avaliacoes'].includes(data.cta) ? data.cta : undefined,
    capa: data.capa ? String(data.capa) : undefined,
    capaAlt: data.capaAlt ? String(data.capaAlt) : undefined,
    // No CMS o campo chama-se "estado"; aqui interessa só publicado ou não.
    publicado: data.estado ? data.estado === 'publicado' : false,
    faq: Array.isArray(data.faq)
      ? data.faq
          .map((f: { pergunta?: string; resposta?: string }) => ({
            pergunta: String(f?.pergunta ?? '').trim(),
            resposta: String(f?.resposta ?? '').trim(),
          }))
          .filter((f: PerguntaDoPost) => f.pergunta && f.resposta)
      : [],
    markdown: content,
  };
}

/** Todos os artigos publicados, do mais recente para o mais antigo. */
export function todosOsPosts(lang: Lingua = 'pt'): Post[] {
  if (!fs.existsSync(pasta(lang))) return [];
  return fs
    .readdirSync(pasta(lang))
    .filter((f) => /\.mdx?$/.test(f))
    .map((f) => ler(f, lang))
    .filter((p): p is Post => p !== null && p.publicado)
    .sort((a, b) => b.data.localeCompare(a.data));
}

export function postPorSlug(slug: string, lang: Lingua = 'pt'): Post | undefined {
  return todosOsPosts(lang).find((p) => p.slug === slug);
}

/** O artigo tem versão na outra língua? */
export function temTraducao(slug: string, lang: Lingua): boolean {
  return !!postPorSlug(slug, lang);
}

/** Até três artigos da mesma categoria; completa com os mais recentes. */
export function relacionados(post: Post, quantos = 3, lang: Lingua = 'pt'): Post[] {
  const outros = todosOsPosts(lang).filter((p) => p.slug !== post.slug);
  const mesma = outros.filter((p) => p.categoria === post.categoria);
  const resto = outros.filter((p) => p.categoria !== post.categoria);
  return [...mesma, ...resto].slice(0, quantos);
}

/** Títulos de nível 2 e 3, com os mesmos ids que o rehype-slug gera no HTML. */
export function indice(markdown: string): Titulo[] {
  const slugger = new GithubSlugger();
  const titulos: Titulo[] = [];
  let dentroDeCodigo = false;

  for (const linha of markdown.split('\n')) {
    if (/^\s*(```|~~~)/.test(linha)) {
      dentroDeCodigo = !dentroDeCodigo;
      continue;
    }
    if (dentroDeCodigo) continue;
    const m = /^(#{2,3})\s+(.+?)\s*#*\s*$/.exec(linha);
    if (!m) continue;
    // Tira a marcação inline (**negrito**, `código`, [links](url)) do texto do índice.
    const texto = m[2]
      .replace(/!?\[([^\]]*)\]\([^)]*\)/g, '$1')
      .replace(/[*_`~]/g, '')
      .trim();
    titulos.push({ texto, id: slugger.slug(texto), nivel: m[1].length as 2 | 3 });
  }
  return titulos;
}

export function temIndice(markdown: string) {
  return indice(markdown).length >= MINIMO_INDICE;
}

/** Minutos de leitura, a 200 palavras por minuto. */
export function tempoDeLeitura(markdown: string) {
  const palavras = markdown.trim().split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(palavras / 200));
}

export async function paraHtml(markdown: string, lang: Lingua = 'pt') {
  const ficheiro = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkRehype)
    .use(rehypeSlug)
    .use(rehypeStringify)
    .process(markdown);
  // Os artigos usam a âncora #orcamento, que não existe nas páginas do blog.
  // Passa a abrir o formulário da proposta (ou a página de contacto, sem JS).
  const contacto = lang === 'en' ? '/en/contacto' : '/contacto';
  return String(ficheiro).replace(/href="#orcamento"/g, `href="${contacto}" data-modal`);
}

/** Oferta que o artigo mostra: a escolhida no artigo ou a da categoria. */
export function ctaDoPost(post: Post): 'analise' | 'proposta' | 'automacao' | 'avaliacoes' {
  if (post.cta) return post.cta;
  if (post.categoria === 'Automação') return 'automacao';
  if (post.categoria === 'Lojas online') return 'proposta';
  return 'analise';
}

/** O artigo trata o leitor por "tu"? Conta as formas de cada tratamento no texto. */
export function trataPorTu(post: Post): boolean {
  const txt = ' ' + post.titulo + ' ' + post.markdown + ' ';
  const tu = (txt.match(/\b(teu|tua|teus|tuas|tens|podes|queres|fazes|precisas)\b/gi) || []).length;
  const voce = (txt.match(/\b(seu|sua|seus|suas|você|pode|quer|precisa)\b/gi) || []).length;
  return tu > voce / 2;
}

/** Divide o HTML do artigo antes do 3.º título H2, para o bloco do meio. */
export function dividirParaCta(html: string): [string, string] {
  let pos = -1;
  let n = 0;
  const re = /<h2[\s>]/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(html))) {
    n++;
    if (n === 3) {
      pos = m.index;
      break;
    }
  }
  return pos === -1 ? [html, ''] : [html.slice(0, pos), html.slice(pos)];
}

export function dataPt(iso: string) {
  return new Date(iso).toLocaleDateString('pt-PT', { day: 'numeric', month: 'long', year: 'numeric' });
}

export function dataEn(iso: string) {
  return new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
}

/** Nome das categorias em inglês (a chave interna fica em português). */
export const CATEGORIA_EN: Record<Categoria, string> = {
  Websites: 'Websites',
  'Lojas online': 'Online stores',
  Automação: 'Automation',
  'SEO e IA': 'SEO and AI',
};
