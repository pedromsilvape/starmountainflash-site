'use client';
import { useRef, useState } from 'react';

export type ItemLista = { href: string; titulo: string; descricao: string; data: string; cat: string; chave: string };

const POR_PAGINA = 5;

/**
 * Lista do blog com filtro por tema e páginas de 5 artigos.
 * Todos os artigos vêm no HTML (o Google e os motores de IA veem a lista
 * completa); o filtro e as páginas só escondem no ecrã.
 */
export default function BlogLista({ itens, todos, temas }: { itens: ItemLista[]; todos: string; temas: { chave: string; nome: string }[] }) {
  const en = todos === 'All';
  const [ativo, setAtivo] = useState('');
  const [pagina, setPagina] = useState(1);
  const topo = useRef<HTMLDivElement>(null);

  const visiveis = itens.filter((i) => !ativo || i.chave === ativo);
  const paginas = Math.max(1, Math.ceil(visiveis.length / POR_PAGINA));
  const naPagina = new Set(visiveis.slice((pagina - 1) * POR_PAGINA, pagina * POR_PAGINA).map((i) => i.href));
  const contar = (c: string) => itens.filter((i) => !c || i.chave === c).length;

  const irPara = (n: number) => {
    setPagina(n);
    const el = topo.current;
    if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 110, behavior: 'smooth' });
  };

  return (
    <div ref={topo}>
      <div className="bfiltro" role="group" aria-label={en ? 'Filter by topic' : 'Filtrar por tema'}>
        {[{ chave: '', nome: todos }, ...temas].map((t) => (
          <button
            type="button"
            key={t.chave || 'todos'}
            aria-pressed={ativo === t.chave}
            onClick={() => {
              setAtivo(t.chave);
              setPagina(1);
            }}
          >
            {t.nome} <span>{contar(t.chave)}</span>
          </button>
        ))}
      </div>
      <div className="posts">
        {itens.map((p) => (
          <a className="post" href={p.href} key={p.href} hidden={!naPagina.has(p.href)}>
            <span className="d">{p.data}</span>
            <div>
              <h3>{p.titulo}</h3>
              <p>{p.descricao}</p>
            </div>
            <span className="cat">{p.cat}</span>
          </a>
        ))}
      </div>
      {paginas > 1 && (
        <nav className="bpag" aria-label={en ? 'Pages' : 'Páginas'}>
          <button type="button" className="seta" disabled={pagina === 1} onClick={() => irPara(pagina - 1)} aria-label={en ? 'Previous page' : 'Página anterior'}>
            ←
          </button>
          {Array.from({ length: paginas }, (_, i) => i + 1).map((n) => (
            <button type="button" key={n} aria-current={n === pagina ? 'page' : undefined} onClick={() => irPara(n)}>
              {n}
            </button>
          ))}
          <button type="button" className="seta" disabled={pagina === paginas} onClick={() => irPara(pagina + 1)} aria-label={en ? 'Next page' : 'Página seguinte'}>
            →
          </button>
        </nav>
      )}
    </div>
  );
}
