import Link from '@/components/Ligacao';
import type { Metadata } from 'next';
import BlogLista from '@/components/BlogLista';
import { HeroSm, JsonLd, NextStep, SectionHead } from '@/components/Blocks';
import { CATEGORIA_EN, dataEn, todosOsPosts } from '@/lib/posts';
import { site } from '@/data/site';
import { meta, migalhasLd } from '@/lib/seo';

const TITULO = 'Blog | Starmountain Flash';
const DESCRICAO = 'Practical articles on websites, SEO, GEO and automation for companies in Portugal.';

export const metadata: Metadata = meta({ titulo: TITULO, descricao: DESCRICAO, caminho: '/en/blog', lang: 'en', alternativo: { pt: '/blog', en: '/en/blog' } });

/** Artigos de entrada: os que respondem às perguntas de quem está a decidir. Mostram-se os 3 primeiros que existirem. */
const DESTAQUES = ['quanto-custa-um-site-pme-portugal', 'quanto-custa-automacao-ia-empresa', 'o-que-automatizar-primeiro-pme', 'aparecer-no-chatgpt-empresa-portugal'];

/** Enquanto não houver artigos publicados, mostram-se os temas a caminho. */
const emBreve: { cat: string; titulo: string; texto: string }[] = [];

export default function BlogEn() {
  const posts = todosOsPosts('en');
  const destaques = DESTAQUES.map((s) => posts.find((p) => p.slug === s)).filter((p): p is (typeof posts)[number] => !!p).slice(0, 3);
  const temas = Array.from(new Set(posts.map((p) => p.categoria)));

  return (
    <>
      <HeroSm
        lang="en"
        caminho={[{ label: 'Blog' }]}
        titulo="Notes on websites and automation."
        destaque="For people running a business."
        descricao="Practical articles on websites, SEO, AI engines and automation, without the jargon."
        acoes="nenhuma"
      />

      {destaques.length > 0 && (
        <section className="sec bdest">
          <SectionHead etiqueta="Start here" titulo="The questions" destaque="we get asked most." />
          <div className="related">
            {destaques.map((p) => (
              <Link href={'/en/blog/' + p.slug} key={p.slug}>
                <span className="cat">{CATEGORIA_EN[p.categoria]}</span>
                <h3>{p.titulo}</h3>
                <p>{p.descricao}</p>
                <span className="d">{dataEn(p.data)}</span>
              </Link>
            ))}
          </div>
        </section>
      )}

      <section className="sec">
        <SectionHead
          etiqueta="Articles"
          titulo={posts.length ? 'All articles.' : 'Coming soon.'}
          destaque={posts.length ? 'Filter by topic.' : 'The first topics.'}
        >
          <p>Short, practical articles for people who run a business and have no time to waste.</p>
        </SectionHead>

        {posts.length ? (
          <BlogLista
            todos="All"
            temas={temas.map((c) => ({ chave: c, nome: CATEGORIA_EN[c] }))}
            itens={posts.map((p) => ({
              href: '/en/blog/' + p.slug,
              titulo: p.titulo,
              descricao: p.descricao,
              data: dataEn(p.data),
              cat: CATEGORIA_EN[p.categoria],
              chave: p.categoria,
            }))}
          />
        ) : (
          <div className="posts">
            {emBreve.map((p) => (
              <article className="post" key={p.titulo}>
                <span className="d">{p.cat}</span>
                <div>
                  <h3>{p.titulo}</h3>
                  <p>{p.texto}</p>
                </div>
                <span className="soon">Coming soon</span>
              </article>
            ))}
          </div>
        )}
      </section>

      {posts.length > 0 && <NextStep />}

      <JsonLd
        data={[
          migalhasLd([{ nome: 'Blog', caminho: '/en/blog' }], 'en'),
          {
            '@context': 'https://schema.org',
            '@type': 'Blog',
            '@id': site.url + '/en/blog#blog',
            name: 'Starmountain Flash blog',
            inLanguage: 'en',
            description: DESCRICAO,
            url: site.url + '/en/blog',
            publisher: { '@id': site.url + '/#negocio' },
            blogPost: posts.map((p) => ({
              '@type': 'BlogPosting',
              headline: p.titulo,
              url: site.url + '/en/blog/' + p.slug,
              datePublished: p.data,
            })),
          },
        ]}
      />
    </>
  );
}
