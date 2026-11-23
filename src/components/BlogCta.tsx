/**
 * Bloco de pedido dentro dos artigos do blog.
 * Cada artigo leva a oferta que faz sentido para quem o está a ler:
 *  - analise: análise gratuita ao site (quem ainda está a perceber o problema)
 *  - proposta: proposta visual gratuita (quem já está a pensar em fazer o site)
 *  - automacao: conversa sobre a tarefa que mais tempo ocupa
 *  - avaliacoes: análise gratuita ao perfil Google
 * "tu" acompanha a forma de tratamento do próprio artigo.
 */
export type TipoCta = 'analise' | 'proposta' | 'automacao' | 'avaliacoes';

type Texto = { etiqueta: string; titulo: string; texto: string; botao: string; href: string; modal?: boolean };

function textos(tipo: TipoCta, tu: boolean): Texto {
  const s = (voce: string, tuForma: string) => (tu ? tuForma : voce);
  switch (tipo) {
    case 'analise':
      return {
        etiqueta: 'Análise gratuita',
        titulo: s('Quer saber o que está a travar o seu site?', 'Queres saber o que está a travar o teu site?'),
        texto: s(
          'Envie o link e receba por email, em até 3 dias úteis, um relatório com o que está a afastar clientes e o que corrigir primeiro. Sem custo e sem compromisso.',
          'Envia o link e recebes por email, em até 3 dias úteis, um relatório com o que está a afastar clientes e o que corrigir primeiro. Sem custo e sem compromisso.',
        ),
        botao: s('Pedir a análise do meu site', 'Pedir a análise do meu site'),
        href: '/analise-gratuita',
      };
    case 'proposta':
      return {
        etiqueta: 'Proposta visual gratuita',
        titulo: s('Veja como o seu site pode ficar, antes de decidir.', 'Vê como o teu site pode ficar, antes de decidires.'),
        texto: s(
          'Preparo uma proposta visual gratuita com base no seu negócio. O orçamento só vem depois, se gostar e quiser avançar.',
          'Preparo uma proposta visual gratuita com base no teu negócio. O orçamento só vem depois, se gostares e quiseres avançar.',
        ),
        botao: 'Pedir proposta visual',
        href: '/contacto',
        modal: true,
      };
    case 'automacao':
      return {
        etiqueta: 'Automações',
        titulo: s('Que tarefa gostava de nunca mais fazer à mão?', 'Que tarefa gostavas de nunca mais fazer à mão?'),
        texto: s(
          'Diga-me qual é a tarefa que mais tempo ocupa na sua empresa. Respondo eu, com o que faz sentido automatizar e o que não vale a pena. A proposta é gratuita.',
          'Diz-me qual é a tarefa que mais tempo ocupa na tua empresa. Respondo eu, com o que faz sentido automatizar e o que não vale a pena. A proposta é gratuita.',
        ),
        botao: 'Falar sobre uma tarefa',
        href: '/automacoes#comecar',
      };
    case 'avaliacoes':
      return {
        etiqueta: 'Avaliações Google',
        titulo: s('Quer mais avaliações no Google, sem pedir uma a uma?', 'Queres mais avaliações no Google, sem pedir uma a uma?'),
        texto: s(
          'A análise ao seu perfil Google é gratuita. Vejo o que pode melhorar e como pôr o pedido de avaliação a sair sozinho depois de cada serviço.',
          'A análise ao teu perfil Google é gratuita. Vejo o que pode melhorar e como pôr o pedido de avaliação a sair sozinho depois de cada serviço.',
        ),
        botao: 'Pedir análise ao perfil',
        href: '/avaliacoes-google',
      };
  }
}

/** O bloco do fim tem outro título, para não repetir o do meio. */
function tituloFim(tipo: TipoCta, tu: boolean): string {
  const s = (voce: string, tuForma: string) => (tu ? tuForma : voce);
  switch (tipo) {
    case 'analise':
      return s('Comece pela análise gratuita ao seu site.', 'Começa pela análise gratuita ao teu site.');
    case 'proposta':
      return s('Quer saber quanto custaria o seu site?', 'Queres saber quanto custaria o teu site?');
    case 'automacao':
      return s('Por onde começar a automatizar na sua empresa?', 'Por onde começar a automatizar na tua empresa?');
    case 'avaliacoes':
      return s('Comece pela análise gratuita ao seu perfil Google.', 'Começa pela análise gratuita ao teu perfil Google.');
  }
}

export function BlogCta({ tipo, tu, onde, slug }: { tipo: TipoCta; tu: boolean; onde: 'meio' | 'fim'; slug: string }) {
  const base = textos(tipo, tu);
  const t = onde === 'fim' ? { ...base, titulo: tituloFim(tipo, tu) } : base;
  return (
    <aside className={'bcta bcta-' + onde} aria-label={t.etiqueta}>
      <span className="bcta-k">
        <i aria-hidden="true" />
        {t.etiqueta}
      </span>
      <p className="bcta-t">{t.titulo}</p>
      <p className="bcta-p">{t.texto}</p>
      <a className="bcta-b" href={tipo === 'analise' ? `${t.href}?de=blog-${slug}` : t.href} {...(t.modal ? { 'data-modal': '' } : {})}>
        {t.botao}
        <svg width="11" height="11" viewBox="0 0 11 11" fill="none" aria-hidden="true">
          <path d="M2 9 9 2M3.5 2H9v5.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </a>
    </aside>
  );
}
