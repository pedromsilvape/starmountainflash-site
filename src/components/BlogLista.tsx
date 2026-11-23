'use client';
import { useState } from 'react';

export type ItemLista = { href: string; titulo: string; descricao: string; data: string; cat: string; chave: string };

/**
 * Lista do blog com filtro por tema. Todos os artigos vêm no HTML
 * (o Google e os motores de IA veem a lista completa); o filtro só esconde.
 */
export default function BlogLista({ itens, todos, temas }: { itens: ItemLista[]; todos: string; temas: { chave: string; nome: string }[] }) {
  const [ativo, setAtivo] = useState('');
  const contar = (c: string) => itens.filter((i) => !c || i.chave === c).length;
  return (
    <>
      <div className="bfiltro" role="group" aria-label={todos === 'All' ? 'Filter by topic' : 'Filtrar por tema'}>
        {[{ chave: '', nome: todos }, ...temas].map((t) => (
          <button type="button" key={t.chave || 'todos'} aria-pressed={ativo === t.chave} onClick={() => setAtivo(t.chave)}>
            {t.nome} <span>{contar(t.chave)}</span>
          </button>
        ))}
      </div>
      <div className="posts">
        {itens.map((p) => (
          <a className="post" href={p.href} key={p.href} hidden={!!ativo && p.chave !== ativo}>
            <span className="d">{p.data}</span>
            <div>
              <h3>{p.titulo}</h3>
              <p>{p.descricao}</p>
            </div>
            <span className="cat">{p.cat}</span>
          </a>
        ))}
      </div>
    </>
  );
}
