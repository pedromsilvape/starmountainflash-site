import type { AnchorHTMLAttributes } from 'react';

// Ligações internas com carregamento completo da página.
// O next/link troca de página sem recarregar e o sf26.js (navbar, rodapé,
// animações, modal) só arranca no primeiro carregamento, o que deixava a
// navbar e o rodapé invisíveis depois de clicar num artigo.
type Props = AnchorHTMLAttributes<HTMLAnchorElement> & { href: string; prefetch?: boolean };

export default function Ligacao({ prefetch: _p, ...props }: Props) {
  return <a {...props} />;
}
